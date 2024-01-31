from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import redirect

from services.models import TemplateForm
from .forms import UserRegisterForm, UserLoginForm
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


def get_personal_account(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = False
    context = {
        "title": "Личный кабинет",
        "token": token
    }
    return render(request, "users/lk.html", context)
