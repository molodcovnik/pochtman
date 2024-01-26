import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template

from .models import Form, FieldData, TemplateForm
from .telegramm import send_telegram


@receiver(post_save, sender=Form)
def created_form(sender, instance, created, **kwargs):
    if created:
        print('Form created')
        print(instance.client.email)
        subject = 'Новая форма с вашего сайта'
        from_email = settings.EMAIL_HOST_USER
        to = instance.client.email
        context = {
            'name': instance.name,
            'email': instance.email,
            'title': instance.last_name,
            'message': instance.phone
        }
        message = get_template('mails/mail.html').render(context)
        msg = EmailMessage(subject, message, to=[to], from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
        text = f'Новая заявка от {instance.name} \n {instance.email} {instance.phone}'
        send_telegram(text)


@receiver(post_save, sender=FieldData)
def created_form_data(sender, instance, created, **kwargs):
    if created:
        template_id = instance.template.id
        template_name = instance.template.name
        count_fields = TemplateForm.objects.get(id=template_id).fields.count()
        qs = FieldData.objects.filter(uid=instance.uid)
        if count_fields == len(qs):
            values = [item.data for item in qs]
            fields_name = [item.field.field_name for item in qs]
            fields_type = [item.field.field_type for item in qs]
            result_dict = list(zip(fields_name, values))
            subject = 'Новая форма с вашего сайта'
            from_email = settings.EMAIL_HOST_USER
            to = 'example@mail.com'
            context = {
                'temp_name': template_name,
                'fields': result_dict
            }
            message = get_template('mails/mail2.html').render(context)
            msg = EmailMessage(subject, message, to=[to], from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
            # for i in range(len(values)):
            #     print(f'{values[i]}, {fields_name[i]}')
            #
            # # print(list(result_dict.keys()))
            # print(list(result_dict.values()))
            # print(result_dict['name'])
            # res = list(result)
            # for item in range(len(res)):
            #     print(res[item])

