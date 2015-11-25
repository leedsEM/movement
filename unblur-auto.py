#!/usr/bin/python

#----------- update path to unblur here if necessary ------------#

unblurpath = "./unblur_openmp_7_17_15.exe"

#----------------------------------------------------------------#


import glob
from subprocess import Popen, PIPE
import sys
vers = "0.5"

print "\n*** Run unblur on multiple files v {0} ***\n".format(vers)

# get files
files = glob.glob(raw_input("files search string: "))
files.sort()
for i in files:
    print i

go = raw_input("continue (Y/N): ") or "Y"
if go not in ["Y","y"]:
    sys.exit("Goodbye!")

frames = raw_input("# of frames: ") or "37"

px = raw_input("pixel size: ") or "2.85"

df = raw_input("Dose filer (Y/N): ")
assert df in ["Y","y","N","n","Yes","YES","yes","NO","no"], "must enter yes or no"

dfx = 0
if df in ["Y","y","Yes","YES","yes"]:
    dfx= 1
    expframe = raw_input("exposure per frame: ")
    avolt = raw_input("Acceleration voltage: ")
    prex = raw_input("Prexposure amount: ")

savealix = 0
savealiframes = raw_input("Save aligned frames (Y/N): ")
assert savealiframes in ["Y","y","N","n","Yes","YES","yes","NO","no"], "must enter yes or no"
if savealiframes in ["Y","y","Yes","YES","yes"]:
    savealix = 1

for file in files:
    print file
    unblurpipe = Popen([unblurpath], stdout=PIPE, stdin=PIPE)
    fileroot = file.split(".")
    
    if dfx == 1 and savealix == 1:
        unblurpipe.communicate("{0}\n{1}\n{2}_align.mrc\n{2}_shifts.txt\n{3}\nYES\n{4}\n{5}\n{6}\nYES\n{2}_aliframes.mrc\nNO\n".format(file,frames,fileroot[0],px,expframe,avolt,prex))
        os.system("mv {0}_align.mrc {0}_align.mrcs".format(fileroot[0]))
    elif dfx == 1 and savealix == 0:
        unblurpipe.communicate("{0}\n{1}\n{2}_align.mrc\n{2}_shifts.txt\n{3}\nYES\n{4}\n{5}\n{6}\nNO\nNO\n".format(file,frames,fileroot[0],px,expframe,avolt,prex))
        os.system("mv {0}_align.mrc {0}_align.mrcs".format(fileroot[0]))
    elif dfx == 0 and savealix == 1:
        unblurpipe.communicate("{0}\n{1}\n{2}_align.mrc\n{2}_shifts.txt\n{3}\nNO\nYES\n{2}_aliframes.mrc\nNO\n".format(file,frames,fileroot[0],px))
        os.system("mv {0}_align.mrc {0}_align.mrcs".format(fileroot[0])) 
    elif dfx == 0 and savealix == 0:
        unblurpipe.communicate("{0}\n{1}\n{2}_align.mrc\n{2}_shifts.txt\n{3}\nNO\nNO\nNO\n".format(file,frames,fileroot[0],px))
        os.system("mv {0}_align.mrc {0}_align.mrcs".format(fileroot[0]))
