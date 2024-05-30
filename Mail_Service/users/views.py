import json
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
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
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import LoginSerializer, TokenSerializer
from services.models import TemplateForm, FieldData
from .forms import UserRegisterForm, UserLoginForm, SignUpForm, UserEditForm, ProfileEditForm
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
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = False

    context = {
        "title": "Личный кабинет",
        "tokenView": token,
        "tokenJson": mark_safe(json.dumps(token.key)),
    }

    return render(request, "users/lk.html", context)


def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'users/edit_profile.html',
                      {'user_form': user_form, 'profile_form': profile_form})


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


@extend_schema_view(
    post=extend_schema(
        summary='Получение токена авторизации',
        description='Логинимся и получаем АПИ-токен',
        request=LoginSerializer,
        responses={200: TokenSerializer},
        methods=["POST"],
    ),
)
class LoginAPIView(APIView):
    authentication_classes = ()

    def post(self, request, format=None):
        data = request.data

        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                serializer = TokenSerializer(token, )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
