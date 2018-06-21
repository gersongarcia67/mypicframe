# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Pictures

import os,random
from os import listdir
from os.path import isfile, join
import datetime
import re

import logging
log=logging.getLogger(__name__)


# Define global variables

basedir="/home/pi/mypicframe"
datadir=basedir+"/data"
tmpdir=basedir+"/tmp"
logdir=basedir+"logs"
#picdir="/mnt/pictures/Family"
picdir="/home/pi/Pictures"
maxpic=10


def ListDir():

    aFiles=[]
    log.info("Read files from %s" % picdir)
    if not os.path.exists(picdir):
        log.error("Directory %s not found" % picdir)
        return

    for path,subdirs,files in os.walk(picdir):
        for name in files:

            log.info(name)
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

#    picture=Pictures()
    insertList=[]
    for l in files:
        (inprimarykey,path,filename,fullpath)=l.split(",")

        print "Check if "+inprimarykey+" exists"
        tpicture=Pictures.objects.filter(primarykey=inprimarykey)

        if len(tpicture)==0:

            print inprimarykey+" not found"

            picture=Pictures()
            picture.primarykey=inprimarykey
            picture.path=path
            picture.filename=filename
            picture.fullpath=fullpath

            picture.save()

            picid=picture.id
            insertList.append(fullpath)

            log.info("File added %s %s %s %s %s" % ( str(picid),inprimarykey,path,filename,fullpath ))

        else:
            picid=tpicture[0].id
            print inprimarykey+" exists"
            log.info("File already in DB %s %s %s %s %s" % ( str(picid),inprimarykey,path,filename,fullpath)) 

    context={ 'pictures_list': insertList, 'num_pics': len(insertList) }

    return render(request,'build/index.html',context)


def list(request):

    piclist=Pictures.objects.all()

    files=[]
    for f in piclist:
        pictureid=f.id
        primarykey=f.primarykey
        path=f.path
        filename=f.filename
        fullpath=f.fullpath

        files.append("%s,%s,%s,%s,%s" % (str(pictureid),primarykey,path,filename,fullpath))
    context={ 'pictures_list': files, 'num_pics': len(files) }
    return render(request,'build/list.html',context)

def randomSelect(request):

    numpics=len(Pictures.objects.all())

    picndx=[]
    piclist=[]

    while len(picndx)<maxpic:

        rnd=random.randint(1,numpics)
        if not rnd in picndx: 

            tpicture=Pictures.objects.filter(id=rnd)

            if len(tpicture)!=0:
                pictureid=tpicture[0].id
                primarykey=tpicture[0].primarykey
                path=tpicture[0].path
                filename=tpicture[0].filename
                fullpath=tpicture[0].fullpath

                piclist.append("%s,%s,%s,%s,%s,%s" % (str(rnd),str(pictureid),primarykey,path,filename,fullpath))
                picndx.append(rnd)


    context={ 'random_list': piclist }
    return render(request,'build/selected.html',context)

    
