# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.timezone import now
from django.db import models

# Create your models here.

class Pictures(models.Model):
    primarykey = models.CharField(max_length=200,primary_key=True)
    filename = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    selectcount = models.IntegerField(default=0)
    last_used = models.DateTimeField(default=now)
    removed = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
