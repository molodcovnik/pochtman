from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from jinja2 import Template
from .forms import CommentForm
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


def get_personal_account(request):
    forms = TemplateForm.objects.filter(author=request.user)
    context = {
        "title": "Личный кабинет",
        "forms": forms
    }
    return render(request, "services/person_acc.html", context)


def get_constructor_form(request):
    context = {
        "title": "Конструктор форм",
    }
    return render(request, "services/constructor.html", context)