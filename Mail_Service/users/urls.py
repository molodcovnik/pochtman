from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import UserRegisterView, UserLoginView, UserLogoutView, EmailConfirmationSentView, UserConfirmEmailView, \
    EmailConfirmedView, EmailConfirmationFailedView, get_personal_account, SignUp, edit_profile

urlpatterns = [
    # path('register/', UserRegisterView.as_view(), name='register'),
    # path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    # path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    # path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    # path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),
    path('lk/', login_required(get_personal_account), name="profile"),
    path('lk/edit/', login_required(edit_profile), name="edit_profile"),
    path('signup/', SignUp.as_view(), name='signup'),

]