from django.urls import path
from .views import index, document_view, get_personal_account, get_constructor_form

urlpatterns = [
    path('', index, name="index"),
    path('lk/', get_personal_account, name="lk"),
    path('constructor/', get_constructor_form, name="constructor"),
    path('docs/', document_view, name="docs"),
    
]