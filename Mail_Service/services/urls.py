from django.urls import path
from .views import TemplateList, index, document_view, get_constructor_form, TemplateDetail, TemplateEdit

urlpatterns = [
    path('', index, name="index"),
    path('templates/', TemplateList.as_view(), name="templates"),
    path('templates/<int:pk>/', TemplateDetail.as_view(), name="template_detail"),
    path('templates/<int:pk>/edit', TemplateEdit.as_view(), name="template_edit"),
    path('constructor/', get_constructor_form, name="constructor"),
    path('docs/', document_view, name="docs"),
    
]