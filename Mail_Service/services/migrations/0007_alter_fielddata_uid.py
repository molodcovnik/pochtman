# Generated by Django 5.0 on 2024-01-22 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_alter_fielddata_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fielddata',
            name='uid',
            field=models.IntegerField(unique=True),
        ),
    ]
