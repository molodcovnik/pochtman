from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    telegram_username = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self):
        return f'{self.user, self.telegram_username, self.is_confirmed}'
