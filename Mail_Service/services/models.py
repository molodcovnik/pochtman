from django.db import models
from django.contrib.auth.models import User
import datetime

from django.db.models.functions import TruncMonth, TruncDay
from django.urls import reverse

class Form(models.Model):
    name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, blank=True, default='')
    phone = models.CharField(max_length=64, blank=True, default='')
    text = models.TextField(max_length=1024, blank=True, default='')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return f'{self.name} {self.last_name} {self.phone} {self.email} {self.text}'


class Comment(models.Model):
    text = models.TextField(max_length=2048)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.text} {self.date}'

    def get_date(self):
        return (self.date).strftime("%d.%m.%Y")


class FormTypeEnum(models.TextChoices):
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'
    DATE = 'DATE'
    TEXT = 'TEXT'
    BOOLEAN = 'BOOLEAN'


class Field(models.Model):
    field_name = models.CharField(max_length=64, unique=True)
    field_type = models.CharField(choices=FormTypeEnum.choices,
                                  default=FormTypeEnum.TEXT,
                                  max_length=10)


    def __str__(self):
        return f'{self.field_name} {self.field_type}'


class TemplateForm(models.Model):
    name = models.CharField(max_length=64, unique=True)
    fields = models.ManyToManyField(Field, related_name='forms')
    author = models.ForeignKey(User, related_name='templates', on_delete=models.CASCADE)
    email_author = models.CharField(blank=True, null=True, max_length=64)
    telegram_author = models.CharField(blank=True, null=True, max_length=64)

    def __str__(self):
        return f'{self.name} {self.fields} {self.author} {self.telegram_author} {self.email_author}'

    def get_absolute_url(self):
        return reverse('template_detail', args=[str(self.id)])


class FieldData(models.Model):
    data = models.TextField(max_length=2048)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    template = models.ForeignKey(TemplateForm, related_name="data",  on_delete=models.CASCADE)
    uid = models.IntegerField()
    time_add = models.DateTimeField(null=True, blank=True)
    read_status = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ("-time_add", )

    def __str__(self):
        return f'{self.data},{self.uid},{self.time_add}'

    def get_absolute_url(self):
        return reverse('notification_detail', args=[str(self.template.pk), str(self.uid)])
