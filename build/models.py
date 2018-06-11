# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Pictures(models.Model):
    primarykey = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    selectcount = models.IntegerField
    last_used = models.DateTimeField()
