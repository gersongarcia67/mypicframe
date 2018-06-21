# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-21 04:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primarykey', models.CharField(max_length=200)),
                ('filename', models.CharField(default='', max_length=200)),
                ('path', models.CharField(default='', max_length=200)),
                ('fullpath', models.CharField(default='', max_length=400)),
                ('selectcount', models.IntegerField(default=0)),
                ('last_used', models.DateTimeField(default=django.utils.timezone.now)),
                ('removed', models.BooleanField(default=False)),
                ('favorite', models.BooleanField(default=False)),
            ],
        ),
    ]
