# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_auto_20170627_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceindexpage',
            name='intro',
            field=models.TextField(blank=True),
        ),
    ]