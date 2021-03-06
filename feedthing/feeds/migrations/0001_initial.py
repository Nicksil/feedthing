# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 23:44
from __future__ import unicode_literals

import core.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True)),
                ('href', models.URLField(unique=True)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('summary', models.TextField(blank=True)),
                ('title', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('etag', models.CharField(blank=True, max_length=255)),
                ('href', models.URLField(unique=True)),
                ('html_href', models.URLField(blank=True)),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='feed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='feeds.Feed'),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('feed', 'href')]),
        ),
    ]
