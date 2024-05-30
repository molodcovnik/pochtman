import datetime
import json
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from jinja2 import Template
from rest_framework.authtoken.models import Token
from users.views import json_serial
from .forms import CommentForm, TemplatesForm
from .models import Comment, Field, TemplateForm, FieldData
from dataclasses import dataclass


def index(request):
    form = CommentForm(request.POST or None)
    comments = Comment.objects.all().order_by('-date')
    if request.user.is_authenticated:

        token, created = Token.objects.get_or_create(user=request.user)
        context = {
            "form": form,
            "comments": comments,
            "tokenIndex": mark_safe(json.dumps(token.key)),
        }

        if request.method == 'POST':
            if form.is_valid():
                comment = Comment.objects.create(text=form.cleaned_data['text'])
                comment.save()
                return redirect(request.path)
            else:
                return render(request, "services/main_page.html", context)
        else:
            return render(request, "services/main_page.html", context)
    context = {
        "form": form,
        "comments": comments
    }
    return render(request, "services/main_page.html", context)


def document_view(request):
    return render(request, "services/document_1.html")


def document_video_view(request):
    return render(request, "services/document_video.html")


def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "400.html", {})


def get_constructor_form(request):
    context = {
        "title": "Конструктор форм",
    }
    return render(request, "services/constructor.html", context)


class TemplateList(ListView):
    model = TemplateForm
    template_name = 'services/templates.html'
    context_object_name = 'templates'

    def get_queryset(self):
        return TemplateForm.objects.filter(author=self.request.user)


class TemplateDetail(DetailView):
    model = TemplateForm
    template_name = 'services/template.html'
    context_object_name = "template"

    def get_success_url(self, **kwargs):
        return reverse_lazy('template_detail', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        author = TemplateForm.objects.get(id=self.get_object().id).author
        if user != author:
            raise PermissionDenied
        return context


class TemplateEdit(SuccessMessageMixin, UpdateView):
    form_class = TemplatesForm
    model = TemplateForm
    template_name = 'services/template_edit.html'
    success_message = "Шаблон формы успешно изменен!"
    extra_tags = "messages__success_updated"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, self.success_message, extra_tags=self.extra_tags)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != self.object.author:
            raise PermissionDenied
        return kwargs


class TemplateDelete(DeleteView):
    model = TemplateForm
    template_name = 'services/temp_delete.html'
    success_url = reverse_lazy('templates')
    context_object_name = 'template'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != self.object.author:
            raise PermissionDenied
        return kwargs


class NotificationListPerson(ListView):
    model = FieldData
    template_name = 'services/notifications.html'
    context_object_name = 'notifications'
    lookup_url_kwarg = 'pk' # извлечение нужного нам пк из урл

    def get_queryset(self):
        temp_id = self.kwargs['pk'] # пк из урл присвоение ему переменной
        template = TemplateForm.objects.get(id=temp_id)
        if template.author != self.request.user:
            raise PermissionDenied
        qs = FieldData.objects.filter(template__author=self.request.user, template__id=temp_id).order_by('-time_add')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temp_id = self.kwargs['pk']  # пк из урл присвоение ему переменной
        template = TemplateForm.objects.get(id=temp_id)
        context["count_fields"] = template.fields.all().count()
        context["fields"] = template.fields.all()
        return context


class NotificationDetail(View):
    def get(self, request, **kwargs):
        uid = kwargs["uid"]
        qs = FieldData.objects.filter(uid=uid)
        last_obj = FieldData.objects.filter(uid=uid).last()
        if last_obj.template.author != self.request.user:
            raise PermissionDenied
        context = {
            "fields": qs,
            "uid": uid,
            "time_obj": last_obj
        }
        return render(request, "services/notification_detail.html", context)


def delete_template_data(request, uid):
    context = {}

    fd = FieldData.objects.filter(uid=uid)
    if request.method == "POST":
        fd.delete()
        return HttpResponseRedirect("")

    return render(request, "delete_view.html", context)


class StaticView(View):

    def get(self, request, **kwargs):
        today = datetime.datetime.now(datetime.timezone.utc)
        last_month = today - datetime.timedelta(days=30)

        qs = (FieldData.objects.filter(template__author=request.user, time_add__gte=last_month)
              .annotate(created_day=TruncDay('time_add')).values('created_day')
              .annotate(total=Count('uid', distinct=True))
              .annotate(read=Count('uid', distinct=True, filter=Q(read_status=True)))
              .annotate(unread=Count('uid', distinct=True, filter=Q(read_status=False)))
              )

        notifications_read_count = (FieldData.objects.filter(template__author=request.user, read_status=True)
                                    .aggregate(Count("uid", distinct=True)))

        notifications_unread_count = (FieldData.objects.filter(template__author=request.user, read_status=False)
                                      .aggregate(Count("uid", distinct=True)))

        temp_statics = TemplateForm.objects.filter(author=request.user)

        context = {
            "temp_count": temp_statics.count(),
            "notifications_read_count": mark_safe(json.dumps(notifications_read_count["uid__count"])),
            "notifications_unread_count": mark_safe(json.dumps(notifications_unread_count["uid__count"])),
            "statics": mark_safe(json.dumps(list(qs.values("created_day", "total", "read", "unread")), default=json_serial)),
        }
        return render(request, "services/statics.html", context)
