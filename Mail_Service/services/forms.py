from django import forms
from .models import Comment, TemplateForm
from django.forms import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]


class TemplatesForm(forms.ModelForm):
    class Meta:
        model = TemplateForm
        fields = ['name', 'fields', ]
