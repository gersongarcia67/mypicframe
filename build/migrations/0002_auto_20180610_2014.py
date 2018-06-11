# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-11 03:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('build', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pictures',
            name='id',
        ),
        migrations.AddField(
            model_name='pictures',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pictures',
            name='removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pictures',
            name='selectcount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='last_used',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='primarykey',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
