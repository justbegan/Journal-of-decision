# Generated by Django 3.2.7 on 2021-12-16 05:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decision', '0011_auto_20210908_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chrono',
            name='add_time',
            field=models.CharField(default=datetime.datetime(2021, 12, 16, 5, 8, 14, 871433), max_length=50, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='decision',
            name='add_time',
            field=models.CharField(default=datetime.datetime(2021, 12, 16, 5, 8, 14, 870717), max_length=50, verbose_name='Дата добавления'),
        ),
    ]
