# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 07:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_auto_20170507_0738'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('feed', 'href')]),
        ),
    ]
