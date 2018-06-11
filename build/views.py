# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Pictures

import os
from os import listdir
from os.path import isfile, join
import datetime
import re

import logging

logger=logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filename': '/home/pi/mypicframe/logs/mypicframe.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Define global variables

basedir="/home/pi/mypicframe"
datadir=basedir+"/data"
tmpdir=basedir+"/tmp"
logdir=basedir+"logs"
#picdir="/mnt/pictures/Family"
picdir="/home/pi/Pictures"


def ListDir():

    aFiles=[]
    if not os.path.exists(picdir):
        print ("Directory %s not found" % picdir)
        return

    for path,subdirs,files in os.walk(picdir):
        for name in files:

            if not re.search('\.jpg',name,re.I): continue

            primkey=os.path.join(path,name)
            primkey=primkey.replace("/","")
            primkey=primkey.replace(".","")
            primkey=primkey.replace(" ","")
            apicdir=picdir
            apicdir=apicdir.replace("/","")
            primkey=primkey.replace(apicdir,"")
            primkey=primkey.upper()

            aFiles.append("%s,%s,%s,%s" % (primkey,path,name,os.path.join(path,name)))

    return aFiles


def index(request):

    files=ListDir()

    for f in files:
        logger.debug(f)

    picture=Pictures()
    insertList=[]
    for l in files:
        (inprimarykey,path,filename,fullpath)=l.split(",")

        tpicture=Pictures.objects.filter(primarykey=inprimarykey)

        if len(tpicture)==0:

            picture.primarykey=inprimarykey
            picture.path=path
            picture.filename=filename
            picture.fullpath=fullpath
            picture.save()
            insertList.append(fullpath)

    context={ 'pictures_list': insertList, 'num_pics': len(insertList) }

    return render(request,'build/index.html',context)


def list(request):

    piclist=Pictures.objects.all()

    files=[]
    for f in piclist:
        primarykey=f.primarykey
        path=f.path
        filename=f.filename
        fullpath=f.fullpath

        files.append("%s,%s,%s,%s" % (primarykey,path,filename,fullpath))
    context={ 'pictures_list': files, 'num_pics': len(files) }
    return render(request,'build/list.html',context)
