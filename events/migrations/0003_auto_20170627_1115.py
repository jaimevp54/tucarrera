# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 15:15
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_auto_20170627_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racepage',
            name='route_description',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Detalles de ruta'),
        ),
        migrations.AlterField(
            model_name='racepage',
            name='sign_in',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Detalles de inscripcción'),
        ),
    ]
