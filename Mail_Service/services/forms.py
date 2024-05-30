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
    ip_address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '111.111.0.0'
        }
    ))
    class Meta:
        model = TemplateForm
        fields = ['name', 'fields', 'check_ip_address', 'ip_address', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя формы'
        self.fields['fields'].label = 'Поля'
        self.fields['check_ip_address'].label = 'Проверять Ip-адрес?'
        self.fields['ip_address'].label = 'Ip-адрес сайта'
