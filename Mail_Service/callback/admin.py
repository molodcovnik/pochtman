from django.contrib import admin

from callback.models import CallbackDetail, Comment

# Register your models here.

admin.site.register(CallbackDetail)
admin.site.register(Comment)