# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0002_auto_20170519_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]
