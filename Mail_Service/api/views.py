import datetime
import json
import random
import re

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from jinja2 import Template
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import TelegramUser
from api.serializers import FormSerializer, FieldSerializer, TemplatesSerializer, LastTemplateSerializer, \
    TokenSerializer, FieldDataSerializer, NotifySerializerSerializer, UserEmailSerializer, EmailAuthorSerializer, \
    TelegramAuthorSerializer, FieldDataNotificationsSerializer, TemplatesFieldsSerializer, TelegramUserSerializer, \
    CheckTelegramSerializer
from services.models import Form, Field, TemplateForm, FieldData


class FieldsViews(APIView):
    def get(self, request, format=None):
        # сортируем поля по их юзабельности в других шаблонах
        data = Field.objects.annotate(num_fields=Count('forms__id')).order_by('-num_fields')
        serializer = FieldSerializer(data, many=True)

        return Response(serializer.data)


class FieldViews(APIView):
    def get_object(self, pk):
        try:
            return Field.objects.get(pk=pk)
        except Field.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        field = self.get_object(pk)
        serializer = FieldSerializer(field, )

        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationUpdates(APIView):
    def get(self, request, format=None):
        try:
            uniq_uid = []
            user = User.objects.get(id=self.request.headers["Authentication"])
            templates = FieldData.objects.filter(template__author=user, read_status=False)
            for temp in templates:
                uniq_uid.append(temp.uid)

            notifications_count = len(set(uniq_uid))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {
            'count': notifications_count,
             }
        return Response(data)


class LastTemplateView(APIView):

    def get(self, request, format=None):
        try:
            user = User.objects.get(id=self.request.headers["Authentication"])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            form = TemplateForm.objects.filter(author=self.request.user).last()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LastTemplateSerializer(form, )
        return Response(serializer.data)

    def post(self, request):
        template_id = self.request.data["templateId"]
        temp = TemplateForm.objects.get(id=template_id)
        t_name = temp.name
        temp_name = t_name.replace(" ", "_")
        fields = temp.fields.all()
        js_template = Template("""<pre>
<code class="js-code">
<span class="js-keyword">const</span> form = document.<span class="js-function">querySelector</span>(<span class="js-body-str">'.form'</span>);

form.<span class="js-function">onsubmit</span> = <span class="js-keyword">async</span> (e) => {
    e.<span class="js-function">preventDefault</span>();{% for field in fields %}{% if field.field_type == "BOOLEAN" %}
    <span class="js-keyword">const</span> {{field.field_name|lower}} = document.<span class="js-function">querySelector</span>(<span class="js-body-str">'#{{field.field_name|lower}}'</span>).checked;{% else %}
    <span class="js-keyword">const</span> {{field.field_name|lower}} = document.<span class="js-function">querySelector</span>(<span class="js-body-str">'#{{field.field_name|lower}}'</span>).value;{% endif %}{% endfor %}
    
    <span class="js-keyword">const</span> data = {
        <span class="js-body-str">"tempId"</span>: <span>{{template_id}}</span>, <span class="js-body-com">// "tempId": 123,</span>{% for field in fields %}
        <span class="js-body-str">"{{field.field_name|lower}}"</span>: {{field.field_name|lower}},{% endfor %}
    };
                               
    <span class="js-keyword">let</span> response = <span class="js-keyword">await</span> <span class="js-function">fetch</span>(<span class="js-body-str">'http://www.pochtmen.ru/api/send_data/'</span>, {
        method: <span class="js-body-str">'POST'</span>,
        headers: {
            <span class="js-body-str">'Content-Type'</span>: <span class="js-body-str">'application/json'</span>,
            <span class="js-body-str">'Authorization'</span>: <span class="js-body-str">'Token ' + 'Ваш_токен'</span>
        },
        body: JSON.<span class="js-function">stringify</span>(data),
      });
    <span class="js-keyword">let</span> result = <span class="js-keyword">await</span> response.<span class="js-function">json()</span>;
    console.<span class="js-function">log</span>(result);
};
                </code>
            </pre>""")
        template = Template("""
    <pre>
    <code class="code-result">
<span class="h-tag">&lt;div</span> <span class="h-atr">class=</span><span class="h-str">&quot;{{temp_name}}&quot;</span><span class="h-tag">&gt;</span>
    <span class="h-tag">&lt;form</span> <span class="h-atr">action=</span><span class="h-str">"#"</span> <span class="h-atr">class=</span><span class="h-str">"form"</span><span class="h-atr"> method=</span><span class="h-str">"post"</span><span class="h-tag">&gt;</span>{% for field in fields %}
        <span class="h-tag">&lt;div</span> <span class="h-atr">class=</span><span class="h-str">"field-wrapper {{field.field_name | lower}}"</span><span class="h-tag">></span>
            <span class="h-tag">&lt;label</span> <span class="h-atr">for=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">"form__label"</span><span class="h-tag">></span>{{field.field_name}}<span class="h-tag">&lt;/label&gt;</span>{% if field.field_type == "EMAIL" %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"email"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% elif field.field_type == "DATE" %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"date"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% elif field.field_type == "BOOLEAN" %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"checkbox"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% else %}
            <span class="h-tag">&lt;input</span> <span class="h-atr">type=</span><span class="h-str">"text"</span> <span class="h-atr">id=</span><span class="h-str">"{{field.field_name|lower}}"</span> <span class="h-atr">class=</span><span class="h-str">&quot;form__input&quot;</span> <span class="h-atr">name=</span><span class="h-str">"{{field.field_name|lower}}"</span><span class="h-tag">&gt;</span>{% endif %}
        <span class="h-tag">&lt;/div&gt;</span>{% endfor %}
        <span class="h-tag">&lt;div</span> <span class="h-atr">class=</span><span class="h-str">&quot;send-btn&quot;</span><span class="h-tag">&gt;</span>
            <span class="h-tag">&lt;button</span> <span class="h-atr">class=</span><span class="h-str">&quot;btn&quot;</span> <span class="h-atr">type=</span><span class="h-str">&quot;submit&quot;</span><span class="h-tag">&gt;</span>Отправить<span class="h-tag">&lt;/button&gt;</span>
        <span class="h-tag">&lt;/div&gt;</span>
    <span class="h-tag">&lt;/form&gt;</span>
<span class="h-tag">&lt;/div&gt;</span>
</code>
</pre>""")
        code = template.render(temp_name=temp_name, fields=fields)
        js_code = js_template.render(fields=fields, template_id=template_id)

        data = {
            "code": code,
            "js_code": js_code,
             }
        return Response(data, status=status.HTTP_200_OK)


class TemplatesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = TemplateForm.objects.filter(author=self.request.user)
        serializer = TemplatesSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TemplatesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return TemplateForm.objects.get(pk=pk)
        except TemplateForm.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        temp = self.get_object(pk)
        if temp.author != self.request.user:
            return Response(data={"Error": "Detail template for only owner template"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TemplatesSerializer(temp, )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        temp = self.get_object(pk)
        if temp.author != self.request.user:
            return Response(data={"Error": "Updated template can be only owner template"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TemplatesSerializer(temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        temp = self.get_object(pk)
        if temp.author != self.request.user:
            return Response(data={"Error": "Delete template can be only owner template"}, status=status.HTTP_403_FORBIDDEN)
        temp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TemplatesReadOnlyView(APIView):

    def get_object(self, pk):
        try:
            return TemplateForm.objects.get(pk=pk)
        except TemplateForm.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        temp = self.get_object(pk)
        if temp.author != self.request.user:
            return Response(data={"Error": "Detail template for only owner template"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TemplatesFieldsSerializer(temp, )

        return Response(serializer.data, status=status.HTTP_200_OK)


class FormsViews(APIView):
    def get(self, request, format=None):
        data = Form.objects.all()

        serializer = FormSerializer(data, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormViews(APIView):

    def get_object(self, pk):
        try:
            return Form.objects.get(pk=pk)
        except Form.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        form = self.get_object(pk)
        serializer = FormSerializer(form, )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        form = self.get_object(pk)
        serializer = FormSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        form = self.get_object(pk)
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def random_code():
    random.seed()
    return random.randint(1000, 999999999)


class SendMessageViews(APIView):
    authentication_classes = (TokenAuthentication, )

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        temp_id = self.request.data.get("tempId")
        template = get_object_or_404(TemplateForm, id=temp_id)
        try:
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if template.author != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        uid = random_code()
        time_add = datetime.datetime.now(datetime.timezone.utc)
        data = (self.request.data).copy()
        data.pop('tempId')
        keys = list(data.keys())
        fields = template.fields.all()
        field_list = list(fields.values_list("field_name", flat=True))
        f_list = [item.lower() for item in field_list]
        if f_list != keys:
            return Response(data={"Error": "Not Acceptable",
                                  "Detail": "The template fields and the resulting template keys do not match"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if len(keys) > template.fields.all().count():
            return Response(data={"Error": "Not Acceptable",
                                  "Detail": "The resulting number of fields does not match the template."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        items = list(data.items())
        for item in items:
            field = Field.objects.filter(field_name=item[0].title()).values_list('id', flat=True)
            try:
                f = Field.objects.get(id__in=field)
            except:
                raise Http404
            if item[0] == f.field_name.lower():
                field_data = FieldData.objects.create(template=template, field=f, uid=uid, data=str(item[1]), time_add=time_add)
                field_data.save()
            else:
                return Response(data={"Error": "Errors in the fields name."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response(data={"Received": "Form accepted."}, status=status.HTTP_201_CREATED)


class TokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        try:
            token = Token.objects.get(user=user)
            serializer = TokenSerializer(token, )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            token = Token.objects.create(user=user)
            token.save()
            serializer = TokenSerializer(token, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
def get_update_token(request):
    user = request.user
    t = Token.objects.filter(user=user)
    new_key = t[0].generate_key()
    t.update(key=new_key)
    return redirect('profile')

class FieldDataViewSet(viewsets.ModelViewSet):
    queryset = FieldData.objects.all()
    serializer_class = FieldDataSerializer

    @action(methods=["DELETE"], detail=False, )
    def delete(self, request):
        delete_uid = request.data
        delete_fields = self.queryset.filter(uid__in=delete_uid)

        delete_fields.delete()
        return Response(self.serializer_class(delete_fields, many=True).data)


@api_view(['GET', 'PUT', 'DELETE'])
def field_data_delete(request):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        uid = request.data["uid"]
        fd = FieldData.objects.filter(uid=uid)
    except FieldData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        fd.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def change_status_field_data(request):
    try:
        uid = request.data["uid"]
        fd = FieldData.objects.filter(uid=uid)
        for f in fd:
            f.read_status = True
            f.save()
    except FieldData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_201_CREATED)


class NotificationUpdatesCurrentTemplate(APIView):
    def get(self, request, pk, format=None):
        try:
            temp = TemplateForm.objects.get(id=pk)
            count = temp.data.filter(read_status=False).count()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {
            'id': pk,
            'count': count
             }
        return Response(data)


class UserEmailView(APIView):
    def get(self, request, format=None):
        user_mail = User.objects.get(id=self.request.headers["userId"])
        serializer = UserEmailSerializer(user_mail, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(id=self.request.data["userId"])
        serializer = UserEmailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateFormEmailView(APIView):
    def get(self, request, pk, format=None):
        try:
            template = TemplateForm.objects.get(id=pk)
            if template.author != self.request.user:
                return Response(data={"Error": "Detail template for only owner template"},
                                status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmailAuthorSerializer(template, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        template = TemplateForm.objects.get(id=pk)
        if template.author != self.request.user:
            return Response(data={"Error": "Update template for only owner template"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = EmailAuthorSerializer(template, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateFormTelegramView(APIView):
    def get(self, request, pk, format=None):
        try:
            template = TemplateForm.objects.get(id=pk)
            if template.author != self.request.user:
                return Response(data={"Error": "Detail template for only owner template"},
                                status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TelegramAuthorSerializer(template, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        template = TemplateForm.objects.get(id=pk)
        if template.author != self.request.user:
            return Response(data={"Error": "Update template telegram for only owner template"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = TelegramAuthorSerializer(template, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TelegramUserCheckView(APIView):
    def get(self, request, pk, format=None):
        template = TemplateForm.objects.get(id=pk)
        if template.author != self.request.user:
            return Response(data={"Error": "Check template telegram for only owner template"},
                            status=status.HTTP_403_FORBIDDEN)
        tg_form_form = template.telegram_author
        tg_user = TelegramUser.objects.filter(username=tg_form_form).values("username")
        serializer = CheckTelegramSerializer(tg_user, )
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationsView(APIView):
    def get(self, request, pk, format=None):
        qs = FieldData.objects.filter(template__pk=pk).order_by("uid").order_by("-time_add")
        serializer = FieldDataNotificationsSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TelegramUsersView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        if self.request.user.is_superuser:
            data = TelegramUser.objects.all()
            serializer = TelegramUserSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"Error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        if self.request.user.is_superuser:
            serializer = TelegramUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"Error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class TelegramUserView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_object(self, user_id):
        try:
            return TelegramUser.objects.get(user_id=user_id)
        except TelegramUser.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        if self.request.user.is_superuser:
            tg_user = self.get_object(user_id)
            serializer = TelegramUserSerializer(tg_user, )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"Error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id, format=None):
        if self.request.user.is_superuser:
            tg_user = self.get_object(user_id)
            tg_user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={"Error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

#
# <div class="{{temp_name}}">
#     <form action="#" class="form" method="post">{% for field in fields %}
#         <div class="field-wrapper {{field.field_name | lower}}">
#             <label for="{{field.field_name|lower}}" class="form__label">{{field.field_name}}</label>{% if field.field_type == "EMAIL" %}
#             <input type="email" id="{{field.field_name|lower}}" class="form__input" name="{{field.field_name|lower}}">{% elif field.field_type == "DATE" %}
#             <input type="date" id="{{field.field_name|lower}}" class="form__input" name="{{field.field_name|lower}}">{% elif field.field_type == "BOOLEAN" %}
#             <input type="checkbox" id="{{field.field_name|lower}}" class="form__input" name="{{field.field_name|lower}}">{% else %}
#             <input type="text" id="{{field.field_name|lower}}" class="form__input" name="{{field.field_name|lower}}">{% endif %}
#         </div>{% endfor %}
#         <div class="send-btn">
#             <button class="btn" type="submit">Отправить</button>
#         </div>
#     </form>
# </div>