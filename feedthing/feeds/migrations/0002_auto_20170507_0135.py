# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='slug',
        ),
        migrations.AddField(
            model_name='entry',
            name='uid',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='uid',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]