# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Pictures

class PicturesAdmin(admin.ModelAdmin):
    list_display=['fullpath']
    fields=('id','primarykey','fullpath','filename','path','last_used','selectcount','removed','favorite')
    readonly_fields=('id','primarykey','fullpath','fullpath','filename','path','last_used')
    save_as=False
    save_as_continue=False

admin.site.register(Pictures,PicturesAdmin)
