import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template

from .models import Form, FieldData, TemplateForm
from .telegramm import send_telegram
from .tasks import send_notification_client, send_telegram_notification


@receiver(post_save, sender=FieldData)
def created_form_data(sender, instance, created, **kwargs):
    if created:
        template_id = instance.template.id
        template_name = instance.template.name
        count_fields = TemplateForm.objects.get(id=template_id).fields.count()
        qs = FieldData.objects.filter(uid=instance.uid)
        if count_fields == len(qs):
            fd = FieldData.objects.filter(uid=instance.uid)
            href = fd.last().get_absolute_url()
            email_author = instance.template.email_author
            telegram_author = instance.template.telegram_author
            values = [item.data for item in qs]
            fields_name = [item.field.field_name for item in qs]
            fields_type = [item.field.field_type for item in qs]
            result_dict = list(zip(fields_name, values))

            send_notification_client.delay(result_dict, email_author, template_name, href)
            send_telegram_notification.delay(result_dict, telegram_author, template_name, href)
