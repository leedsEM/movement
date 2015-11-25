#! /usr/bin/python
vers = "1.0"

# motioncorr front end
# input .dm4 or .mrcs files - converts dm4 to mrcs
#
# normal mode (no additional arguments): outputs uncorrected stack as mrcs(if not already there) corrected stack, merged-corrected and merged-uncorrected 
#
# shaun mode (run with -s argument): minimal output with RELION naming conventions - outputs only corrected stack as <filename>_movie.mrcs and corrected-merged as <filename>.mrc
#
#

###### paths
dm2mrcpath =  "/fbs/emsoftware2/LINUX/IMOD-LATEST/imod_4.5.7/bin/dm2mrc"
motioncorrpath =  "/fbs/amytox/bmbnar_amytox/Software/motioncorr_v2.0/bin/motioncorr"

###### imports
import glob
import os
import sys

## startup
print "** motion corr front end v%s **" % vers
if len(sys.argv) > 1 and sys.argv[1] == "-s":
   print "*** SHAUN MODE! ***"
outputtext = "mocorr.log"

##### Variables
filessearch = raw_input("files search string: ") or "a*"
startframe = raw_input("start frame (leave blank for all):  ") or 0
endframe = raw_input("end frame (leave blank for all): ") or 0

### program


# get the files to operate on
files = glob.glob(filessearch)
if files == []:
   sys.exit( "** ERROR: no files found **")
for i in files:
   filename =i.split(".") 

# check if files are dm4 - if so convert  
   if filename[1] == "dm4":
      print "converting %s to %s.mrcs" % (i,filename[0])
      os.system("%s %s %s.mrcs" % (dm2mrcpath, i, filename[0])) 
      i = "%s.mrcs" % i.split(".")[0]
      print "motion corr on: %s" % i
   if i.split(".")[1] == "mrcs":   
      if len(sys.argv) > 1 and sys.argv[1] == "-s":
         os.system("%s %s -fcs %s.mrc -srs 0 -ssc 1 -fct %s_movie.mrcs -nss %s -nes %s >> %s" % (motioncorrpath,i,filename[0],filename[0],startframe,endframe,outputtext))
         #print "%s %s -fcs %s.mrc -srs 0 -ssc 1 -fct %s_movie.mrcs -nss %s -nes %s >> %s" % (motioncorrpath,i,filename[0],filename[0],startframe,endframe,outputtext)
      else:
         os.system("%s %s -fcs %s_corr_merge.mrc -srs 1 -frs %s_merge.mrc -ssc 1 -fct %s_corr_stack.mrcs -nss %s -nes %s >> %s" % (motioncorrpath,i,filename[0],filename[0],filename[0],startframe,endframe,outputtext))
         #print "%s %s -fcs %s_corr_merge.mrc -srs 1 -frs %s_merge.mrc -ssc 1 -fct %s_corr_stack.mrcs -nss %s -nes %s >> %s" % (motioncorrpath,i,filename[0],filename[0],filename[0],startframe,endframe,outputtext)

   else:
      print "file %s not .mrcs or .dm4 -- skipping" % i
