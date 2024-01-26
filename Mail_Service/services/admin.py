from django.contrib import admin

from .models import Form, Comment, Field, TemplateForm, FieldData

admin.site.register(Form)
admin.site.register(Comment)
admin.site.register(Field)
admin.site.register(TemplateForm)
admin.site.register(FieldData)