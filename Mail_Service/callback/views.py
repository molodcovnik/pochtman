from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import CallbackDetail
from .serializers import CallbackDetailSerializer


class CallbackDetailViewSet(ModelViewSet):
    queryset = CallbackDetail.objects.all()
    serializer_class = CallbackDetailSerializer
    # permission_classes = (AllowAny, )
    lookup_field = 'uid'

    # def get_queryset(self):
    #     return CallbackDetail.objects.filter()
