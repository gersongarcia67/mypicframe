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
    #template=loader.get_template('build/index.html')
    context={ 'pictures_list': files, 'num_pics': len(files) }

    #return HttpResponse(template.render(context,request))
    return render(request,'build/index.html',context)

