# Generated by Django 5.0 on 2024-02-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]