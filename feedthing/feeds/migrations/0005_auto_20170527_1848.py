# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_entry_string_summary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='string_content',
            new_name='content_string',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='string_summary',
            new_name='summary_string',
        ),
    ]
