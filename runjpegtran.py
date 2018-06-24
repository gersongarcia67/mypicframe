
import os
import shutil

jpegtran='/usr/bin/jpegtran'

def jpegtranRun(infile,outfile):

    if not os.path.isfile(infile):
        print ('Error: %s not found.' % infile)
        return

    try:
        cmd=jpegtran+' -optimize -progressive '+infile+' > '+outfile
        print ('Running: %s' % cmd)
        os.system(cmd)

    except:
        try:
            print 'Failed, try pure copy'
            shutil.copy2(infile,outfile)
        except:
            print 'Copy also failed'

    if os.path.isfile(outfile):
        print ('Done: file %s created' % outfile)
    else:
        print ('Ops, something went wrong. File %s not found.' % outfile)

    return


nfile='20171230_152217.jpg'
infile='/home/pi/Pictures/'+nfile
outfile='/home/pi/mypicframe/tmp/'+nfile

jpegtranRun(infile,outfile)


