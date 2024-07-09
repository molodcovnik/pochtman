from rest_framework import serializers
from .models import CallbackDetail


class CallbackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallbackDetail
        fields = ['uid', 'status', 'result', ]