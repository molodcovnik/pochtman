# Generated by Django 5.0 on 2024-02-07 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_fielddata_time_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='fielddata',
            name='read_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
