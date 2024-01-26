from rest_framework import serializers
from services.models import Form, Field, TemplateForm
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email",)


class FormSerializer(serializers.ModelSerializer):
    # client = UserSerializer()

    class Meta:
        model = Form
        fields = ("name", "last_name", "email", "phone", "text", "client", )


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ("id", "field_name", "field_type", )


class TemplatesSerializer(serializers.ModelSerializer):
    fields = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), many=True)

    class Meta:
        model = TemplateForm
        fields = ("id", "name", "fields", "author", )


class LastTemplateSerializer(serializers.ModelSerializer):
    fields = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), many=True)

    class Meta:
        model = TemplateForm
        fields = ("id", "name", "fields", "author", )