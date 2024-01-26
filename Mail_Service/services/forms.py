from django import forms
from .models import Comment
from django.forms import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]

