from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from jinja2 import Template
from .forms import CommentForm, TemplatesForm
from .models import Comment, Field, TemplateForm, FieldData
from dataclasses import dataclass


def index(request):
    form = CommentForm(request.POST or None)
    comments = Comment.objects.all().order_by('-date')
    
    context = {
        "form": form,
        "comments": comments,
    }
    if request.method == 'POST':
        if form.is_valid():
            comment = Comment.objects.create(text=form.cleaned_data['text'])
            comment.save()
            return redirect(request.path)
            # return render(request, "services/main_page.html", context)
        else:
            return render(request, "services/main_page.html", context)
    else:
        return render(request, "services/main_page.html", context)


def document_view(request):
    @dataclass
    class User:
        username: str
        url: str
    
    template = Template("""\n
<title>{{ title }}</title>
    <ul>
        {% for user in users %}
        <li><a href="{{ user.url }}">{{ user.username }}</a></li>
        {% endfor %}
    </ul>
    """)
    users = [
        User('1', 'https://a.bc/user/1'),
        User('2', 'https://a.bc/user/2'),
        User('3', 'https://a.bc/user/3'),
    ]
    context = {
        "code": template.render(title="Hello World!", users=users),
    }
    return render(request, "services/document_1.html", context)




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


class TemplateDelete(DeleteView):
    model = TemplateForm
    template_name = 'services/temp_delete.html'
    success_url = reverse_lazy('templates')
    context_object_name = 'template'


class NotificationListPerson(ListView):
    model = FieldData
    template_name = 'services/notifications.html'
    context_object_name = 'notifications'
    lookup_url_kwarg = 'pk' # извлечение нужного нам пк из урл

    def get_queryset(self):
        temp_id = self.kwargs['pk'] # пк из урл присвоение ему переменной
        qs = FieldData.objects.filter(template__author=self.request.user, template__id=temp_id).order_by('-time_add')
        # uids = set(qs.values_list('uid', flat=True))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temp_id = self.kwargs['pk']  # пк из урл присвоение ему переменной
        template = TemplateForm.objects.get(id=temp_id)
        context["count_fields"] = template.fields.all().count()
        context["fields"] = template.fields.all()

        return context

#### test view for date

class NotificationDetail(View):
    def get(self, request, **kwargs):
        uid = kwargs["uid"]
        qs = FieldData.objects.filter(uid=uid)
        last_obj = FieldData.objects.filter(uid=uid).last()
        context = {
            "fields": qs,
            "uid": uid,
            "time_obj": last_obj
        }
        return render(request, "services/notification_detail.html", context)


def delete_template_data(request, uid):
    print(uid)
    context = {}

    # fetch the object related to passed id
    fd = FieldData.objects.filter(uid=uid)
    if request.method == "POST":
        # delete object
        fd.delete()
        return HttpResponseRedirect("")

    return render(request, "delete_view.html", context)