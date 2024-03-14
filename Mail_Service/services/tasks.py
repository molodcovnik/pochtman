from celery import shared_task
from django.conf import settings
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from api.models import TelegramUser
from services.telegramm import send_telegram


@shared_task
def send_notification_client(result_dict, email_author, template_name, href):

    subject = 'Новая форма с вашего сайта'
    from_email = settings.EMAIL_HOST_USER
    to = email_author
    context = {
        'temp_name': template_name,
        'fields': result_dict,
        'notification_link': settings.SITE_URL + href,
        'url': settings.SITE_URL
    }
    message = get_template('mails/mail.html').render(context)
    msg = EmailMessage(subject, message, to=[to], from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()


@shared_task()
def send_telegram_notification(result_dict, telegram_author, template_name, href):
    if telegram_author:
        try:
            tg = TelegramUser.objects.get(username=telegram_author)
        except TelegramUser.DoesNotExist:
            tg = None

        if tg is not None:
            send_telegram(result_dict, tg.user_id, template_name)
        else:
            print("Telegram username is not exists")
            pass

