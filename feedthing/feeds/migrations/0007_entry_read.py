# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_auto_20170507_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
