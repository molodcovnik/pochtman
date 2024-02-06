from django import forms
from .models import Comment, TemplateForm, Field
from django.forms import ValidationError


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]


class TemplatesForm(forms.ModelForm):
    fields = forms.ModelMultipleChoiceField(
        queryset=Field.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text="Выберите одно или более полей!"
    )
    class Meta:
        model = TemplateForm
        fields = ['name', 'fields', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя формы'
        self.fields['fields'].label = 'Поля'
