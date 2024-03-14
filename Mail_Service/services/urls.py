from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import TemplateList, index, document_view, get_constructor_form, TemplateDetail, TemplateEdit, \
    TemplateDelete, NotificationListPerson, NotificationDetail, StaticView, document_video_view

urlpatterns = [
    path('', index, name="index"),
    path('templates/', login_required(TemplateList.as_view()), name="templates"),
    path('templates/<int:pk>/', login_required(TemplateDetail.as_view()), name="template_detail"),
    path('templates/<int:pk>/notifications/', login_required(NotificationListPerson.as_view()), name="notification_temp"),
    path('templates/<int:pk>/notifications/<int:uid>/', login_required(NotificationDetail.as_view()), name="notification_detail"),
    path('templates/<int:pk>/edit/', login_required(TemplateEdit.as_view()), name="template_edit"),
    path('templates/<int:pk>/delete', login_required(TemplateDelete.as_view()), name="template_delete"),
    path('statistics/', login_required(StaticView.as_view()), name="statics"),
    path('constructor/', login_required(get_constructor_form), name="constructor"),
    path('docs/', document_view, name="docs"),
    path('docs/video', document_video_view, name="docs_video"),
    # path('notifications/', NotificationList.as_view(), name="notifications"),

    
]