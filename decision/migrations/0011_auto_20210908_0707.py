# Generated by Django 3.2.7 on 2021-09-08 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decision', '0010_auto_20210906_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chrono',
            name='add_time',
            field=models.CharField(default=datetime.datetime(2021, 9, 8, 7, 7, 17, 247291), max_length=50, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='add_time',
            field=models.CharField(default=datetime.datetime(2021, 9, 8, 7, 7, 17, 246607), max_length=50, verbose_name='Дата добавления'),
        ),
    ]
