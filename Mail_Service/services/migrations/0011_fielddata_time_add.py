# Generated by Django 5.0 on 2024-02-07 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_alter_templateform_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='fielddata',
            name='time_add',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
