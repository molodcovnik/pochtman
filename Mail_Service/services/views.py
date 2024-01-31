from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from jinja2 import Template
from .forms import CommentForm, TemplatesForm
from .models import Comment, Field, TemplateForm
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
            return render(request, "services/main_page.html", context)
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


class TemplateEdit(UpdateView):
    form_class = TemplatesForm
    model = TemplateForm
    template_name = 'services/template_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
