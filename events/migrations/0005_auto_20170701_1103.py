# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0004_auto_20170701_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racepage',
            name='route_description',
            field=models.CharField(blank=True, max_length=200, verbose_name='Detalles de ruta'),
        ),
    ]
