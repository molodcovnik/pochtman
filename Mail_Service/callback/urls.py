from django.urls import path, include
from rest_framework.routers import DefaultRouter

from callback.views import CallbackDetailViewSet

app_name = 'callback'

router = DefaultRouter()
router.register(r'callbacks', CallbackDetailViewSet, basename='callback')

urlpatterns = [
    path('api/', include(router.urls)),
]