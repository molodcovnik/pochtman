# Generated by Django 5.0 on 2024-03-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='user_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='telegramuser',
            unique_together={('user_id', 'username')},
        ),
    ]
