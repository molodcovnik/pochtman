from django.db import models


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(blank=True, null=True,max_length=64)
    first_name = models.CharField(blank=True, null=True,max_length=64)
    last_name = models.CharField(blank=True, null=True,max_length=64)

    class Meta:
        unique_together = ("user_id", "username", )
    def __str__(self):
        return f'{self.user_id} {self.username} {self.first_name} {self.last_name}'

    @property
    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'
