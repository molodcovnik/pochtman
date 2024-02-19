from rest_framework import serializers
from services.models import Form, Field, TemplateForm, FieldData
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email",)


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)


class EmailAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateForm
        fields = ("email_author",)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['email_author'] == "":
            raise serializers.ValidationError("Email cannot be empty.")
        return data



class TelegramAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateForm
        fields = ("telegram_author",)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['telegram_author'] == "":
            raise serializers.ValidationError("Telegram cannot be empty.")
        return data


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


class TemplatesFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateForm
        fields = ("id", "name", "fields", )
        depth = 1


class LastTemplateSerializer(serializers.ModelSerializer):
    fields = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), many=True)

    class Meta:
        model = TemplateForm
        fields = ("id", "name", "fields", "author", )


class TokenSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Token
        fields = ("user", "key", "created",)


class FieldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldData
        fields = ("id", "data", "field", "template", "uid", )


class FieldDataNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldData
        fields = ("id", "data", "field", "template", "uid", "time_add", "read_status", )


class NotifySerializerSerializer(serializers.Serializer):
    read_status = serializers.BooleanField()
    total = serializers.IntegerField()

