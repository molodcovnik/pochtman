from django.contrib.auth.models import User
from django.db import models

from services.models import TemplateForm
from froala_editor.fields import FroalaField


class CallbackStatusEnum(models.TextChoices):
    OPEN = 'Open', 'Открыта'
    CLOSED = 'Closed', 'Закрыта'


class ResultTypeEnum(models.TextChoices):
    SALE = 'Sale', 'Продажа'
    BUY = 'Buy', 'Покупка'
    ORDER = 'Order', 'Заказ'
    CONSULTATION = 'Consultation', 'Консультация'
    REFUSAL = 'Refusal', 'Отказ'
    OTHER = 'Other', 'Другое'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = FroalaField()
    time_add = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f'{self.text}, {self.author}'


class CallbackDetail(models.Model):
    uid = models.IntegerField(unique=True)
    status = models.CharField(choices=CallbackStatusEnum.choices, default=CallbackStatusEnum.OPEN, max_length=10)
    result = models.CharField(choices=ResultTypeEnum.choices, default=ResultTypeEnum.OTHER, max_length=15)
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return f'{self.id} {self.uid}'
