from django.urls import path
from api.views import FormsViews, FormViews, FieldsViews, TemplatesView, TemplateViews, LastTemplateView, FieldViews, \
    SendMessageViews, TokenView, field_data_delete, change_status_field_data, NotificationUpdates, \
    NotificationUpdatesCurrentTemplate, UserEmailView, TemplateFormEmailView, TemplateFormTelegramView, \
    NotificationsView, TemplatesReadOnlyView, get_update_token, TelegramUsersView, TelegramUserView

urlpatterns = [
    path('users_email/', UserEmailView.as_view()),
    path('forms/', FormsViews.as_view()),
    path('form/<int:pk>/', FormViews.as_view()),
    path('fields/', FieldsViews.as_view()),
    path('fields/<int:pk>/', FieldViews.as_view()),
    path('templates/', TemplatesView.as_view()),
    path('last_template/', LastTemplateView.as_view()),
    path('templates/<int:pk>/', TemplateViews.as_view()),
    path('templates/<int:pk>/fields/', TemplatesReadOnlyView.as_view()),
    path('templates/<int:pk>/email/', TemplateFormEmailView.as_view()),
    path('templates/<int:pk>/telegram/', TemplateFormTelegramView.as_view()),
    path('send_data/', SendMessageViews.as_view()),
    path('token/', TokenView.as_view()),
    path('token/update/', get_update_token, name='update_token'),
    path('notifications/delete', field_data_delete),
    path('notifications/status', change_status_field_data),
    path('notifications/count', NotificationUpdates.as_view()),
    path('notifications/<int:pk>/', NotificationsView.as_view()),
    path('notifications/<int:pk>/count', NotificationUpdatesCurrentTemplate.as_view()),
    path('telegram_users/', TelegramUsersView.as_view()),
    path('telegram_users/<int:user_id>/', TelegramUserView.as_view()),
]
