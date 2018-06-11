#!/usr/bin/python

import os
from os import listdir
from os.path import isfile, join
import datetime
import re

# Define global variables

basedir="/home/pi/mypicframe"
datadir=basedir+"/data"
tmpdir=basedir+"/tmp"
logdir=basedir+"logs"
picdir="/mnt/pictures/Family"


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


files=ListDir()

for l in files:
    print l
