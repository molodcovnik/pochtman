import json
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core import serializers
from django.db.models import Count, Q, Sum, F
from django.db.models.functions import TruncDay
from django.db.models import Case, Value, When
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import redirect

from services.models import TemplateForm, FieldData
from .forms import UserRegisterForm, UserLoginForm, SignUpForm
from .mixins import UserIsNotAuthenticated
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegisterView(UserIsNotAuthenticated, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        # user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        # print(token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # print(uid)
        activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        # current_site = Site.objects.get_current().domain
        current_site = '127.0.0.1:8000'
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            f'{from_email}',
            [user.email],
            fail_silently=False,
        )
        return redirect('email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, **kwargs):
        try:
            token = kwargs["token"]
            uid = urlsafe_base64_decode(kwargs["uidb64"])
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.profile.is_confirmed = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    next_page = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LogoutView):
    next_page = 'index'

def get_count(templates):
    uniq_uid = []
    for temp in templates:
        qs = temp.data.values('uid')
        for q in qs:
            uniq_uid.append(q['uid'])

    count = len(set(uniq_uid))
    print(f'function completed count = {count}')
    return count


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def get_count_for_status(templates):
    uniq_uid = []
    for temp in templates:
        uniq_uid.append(temp.uid)

    count = len(set(uniq_uid))
    return count

def get_personal_account(request):
    uniq_uid = []
    received_form_sum = (FieldData.objects.filter(template__author=request.user)
                         .aggregate(Count("uid", distinct=True)).get("uid__count"))
    templates = TemplateForm.objects.filter(author=request.user)
    # read_forms = FieldData.objects.filter(template__author=request.user, read_status=True)
    # unread_forms = FieldData.objects.filter(template__author=request.user, read_status=False)
    # notifications_count = get_count(templates)
    # notifications_read_count = get_count_for_status(read_forms)
    notifications_read_count = (FieldData.objects.filter(template__author=request.user, read_status=True)
                                .aggregate(Count("uid", distinct=True)))
    # notifications_unread_count = get_count_for_status(unread_forms)
    notifications_unread_count = (FieldData.objects.filter(template__author=request.user, read_status=False)
                                  .aggregate(Count("uid", distinct=True)))

    # statics = (FieldData.objects.filter(template__author=request.user)
    #   .annotate(created_day=TruncDay('time_add')).values('created_day')
    #   .annotate(count=Count('uid', distinct=True)))
    qs = (FieldData.objects.filter(template__author=request.user)
        .annotate(created_day=TruncDay('time_add')).values('created_day')
        .annotate(total=Count('uid', distinct=True))
        .annotate(read=Count('uid', distinct=True, filter=Q(read_status=True)))
        .annotate(unread=Count('uid', distinct=True, filter=Q(read_status=False)))
        )
    print(qs)
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = False

    context = {
        "title": "Личный кабинет",
        "token": token,
        "templates_count": templates.count(),
        # "notifications_count": notifications_count,
        "notifications_count": received_form_sum,
        "notifications_read_count": mark_safe(json.dumps(notifications_read_count["uid__count"])),
        "notifications_unread_count": mark_safe(json.dumps(notifications_unread_count["uid__count"])),
        "statics": mark_safe(json.dumps(list(qs.values("created_day", "total", "read", "unread")), default=json_serial)),
    }

    return render(request, "users/lk.html", context)
#
# qs = (FieldData.objects.filter(template__author=admin)
#       .annotate(created_day=TruncDay('time_add')).values('created_day')
#       .annotate(count=Count('uid', distinct=True)))


# ПУШКА !!!
# qs = (FieldData.objects.filter(template__author=admin)
#     .annotate(created_day=TruncDay('time_add')).values('created_day')
#     .annotate(read=Count('uid', distinct=True, filter=Q(read_status=True)))
#     .annotate(unread=Count('uid', distinct=True, filter=Q(read_status=False)))
#     )

class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        email = form.data['email']
        # user.is_active = False
        user_email = User.objects.filter(email=email)
        if user_email.exists():
            return redirect('account_login')
        else:
            user.username = email
            user.save()
            return redirect('index')