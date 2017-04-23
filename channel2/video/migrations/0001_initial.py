# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 03:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_path', models.CharField(max_length=128, unique=True)),
                ('file_path', models.CharField(max_length=1024)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('expires_on', models.DateTimeField(db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'video_link',
            },
        ),
        migrations.AlterIndexTogether(
            name='videolink',
            index_together=set([('user', 'file_path')]),
        ),
    ]
