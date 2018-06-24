# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render

from .models import Pictures

import os,random
from os import listdir
from os.path import isfile, join
import datetime
import time
from datetime import date, datetime
import re
import shutil

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
jpegtran='/usr/bin/jpegtran'


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

def jpegtranRun(infile,outfile):

    if not os.path.isfile(infile):
        log.error('Error: %s not found.' % infile)
        return

    cmd=jpegtran+' -optimize -progressive '+infile+' > '+outfile
    log.info('Running: %s' % cmd)

    try:
        os.system(cmd)
    except:
        log.error('Failed, try pure copy')
        try:
            shutil.copy2(infile,outfile)
        except:
            log.error('Copy also failed')

    if os.path.isfile(outfile):
        log.info('Done: file %s created' % outfile)
    else:
        log.error('Ops, something went wrong. File %s not found.' % outfile)

    return


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

    if not os.path.exists(tmpdir):
        log.info('Temp dir %s not found, create it' % tmpdir)
        try:
            os.mkdir(tmpdir)
        except:
            raise Http404('<h1>Unable to create %s</h1>' % tmpdir)

    for path,subdirs,files in os.walk(tmpdir):
        if len(files)>0:
            log.error('Temp dir %s is not empty.' % tmpdir)
            raise Http404('<h1>Temp dir '+tmpdir+' is not empty</h1>')

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
                selectcount=tpicture[0].selectcount

                outfile=tmpdir+'/'+filename

                # Update LastUsed and SelectCount fields

                tpicture[0].last_used=datetime.now()
                tpicture[0].selectcount=selectcount+1
                tpicture[0].save()


                jpegtranRun(fullpath,outfile)

                piclist.append("%s,%s,%s,%s,%s,%s" % (str(rnd),str(pictureid),primarykey,path,filename,fullpath))
                picndx.append(rnd)


    context={ 'random_list': piclist }
    return render(request,'build/selected.html',context)

    
