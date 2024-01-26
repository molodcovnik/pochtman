# Generated by Django 5.0 on 2024-01-22 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_field_templateform'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(max_length=2048)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.field')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.templateform')),
            ],
        ),
    ]
