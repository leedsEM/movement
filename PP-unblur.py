#!/usr/bin/python

# accepts a RELION starfile



#----------- update path to unblur here ------------#
global unblurpath
unblurpath = "./unblur_openmp_7_17_15.exe"  

#----------------------------------------------------------------#



############## no touchy touchy anything below here ################################



vers = "0.7"

#!/usr/bin/python
import glob
import os
import sys
from subprocess import Popen, PIPE

global parname
if '-r13' in sys.argv:
    parname = "_rlnParticleName"
else:
    parname = "_rlnOriginalParticleName"



print "**** Per-particle motion correction with Unblur  v {0} ****".format(vers)
if parname == "_rlnParticleName":
    print "** RELION 1.3 back compatibility made**"
print "\nMaking mrcs files for unblur..."

###############################FUNCTION: MAKE THE MRC FILES FOR UNBLUR ################################################
def makemrcs(x):
### ---- function: reorder the starfile -----------
    def reorder_starfile(filename):
        relionfile = open(filename, "r")
        odata = relionfile.readlines()
        
        # find the original particle numbers and micrograph numbers names
        labelnames = (parname,"_rlnMicrographName")
        labeldic = {}
        for i in odata:
            if any(s in i for s in labelnames):
                labeldic[i.split()[0]] = int(i.split()[1].strip('#'))  
        
        if parname not in labeldic.keys():
            sys.exit("{0} label not found in starfile: RELION version mismatch? run with -r13 flag for 1.3 back-compatibility".format(parname))
        
        # put all of the data into an array
        data = []
        for i in odata:
            if len(i.split()) > 4: 
                data.append(i.split())
        
        # count the number of particles
        particlecount = int(data[-1][labeldic[parname]-1].split("@")[0])
        
        #put the partuicles in a dict by their number
        allparts = {}
        for i in range(1,particlecount+1):
            allparts[i] = []
        for i in data:
            allparts[int(i[labeldic[parname]-1].split("@")[0])].append(i)
        
        # open the output star file
        output = open("{0}_UB.star".format(filename.split(".")[0]),"w")
        
        # write new header
        for i in odata:
            if len(i.split()) < 3:
                output.write(i)
        
        # write the particles 
        n = 1
        for i in allparts:
            for j in allparts[i]:
                for element in j:
                    output.write(str(element) +"\t")
                output.write("\n")
                n += 1
        return "{0}_UB.star".format(filename.split(".")[0])
    #-----------------------------------------------------------------------
    
    
    
    ## get the relion file and read the data
    files = glob.glob(x) ####### string will go here
    assert len(files) >= 1, "no files found"
    
    for i in files:
        print i
    mrcs4unblur = []   
    go = raw_input("Do it? (Y/N)")
    if go in ("Y","y","yes","YES","Yes"):
        for each in files:
            newfile = reorder_starfile(each)
            print each," --> ",newfile
            
            # use relion to make mrcs stack
            os.system("relion_stack_create --i {0} --o {1}_sorted".format(newfile,newfile.split(".")[0]))
            os.system("mv {0}_sorted.mrcs {0}_sorted.mrc".format(newfile.split(".")[0]))
            mrcs4unblur.append("{0}_sorted.mrc".format(newfile.split(".")[0]))
        return(mrcs4unblur)
#################################################################################

############################## FUNCTION: RUN UNBLUR ON ALL THE FILES ####################################################
def unblurall(y):
    
    files = y
    files.sort()
    
    print "Done"
    print "Now enter some parameters for unblur: "
    
    frames = raw_input("# of frames: ") or "34"
    
    px = raw_input("pixel size: ") or "1.35"
    
    df = raw_input("Dose filer (Y/N): ") or 'y'
    assert df in ["Y","y","N","n","Yes","YES","yes","NO","no"], "must enter yes or no"
    
    dfx = 0
    if df in ["Y","y","Yes","YES","yes"]:
        dfx= 1
        expframe = raw_input("exposure per frame: ") or "1.47"
        avolt = raw_input("Acceleration voltage: ") or "300"
        prex = raw_input("Prexposure amount: ") or "0"
    
    savealix = 0
    savealiframes = raw_input("Save aligned frames (Y/N): ") or "N"
    assert savealiframes in ["Y","y","N","n","Yes","YES","yes","NO","no"], "must enter yes or no"
    if savealiframes in ["Y","y","Yes","YES","yes"]:
        savealix = 1
    print "Running unblur from {0}".format(unblurpath)
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
    return("{0}_align.mrcs".format(fileroot[0]))
######################################################################################

######################## FUNCTION: WRITE THE NEW STARFILE ###########################################
def write_updated_starfile(z,zz,outexample):
    print "Writing updated star file with the selected particles"
    file = z
    alldata = open(file,'r').readlines()
    labelsdic = {}
    data = {}
    header = []
    n = 1
    for i in alldata:
        if len(i.split()) < 3:
            header.append(i)
        if '#' in i:
            labelsdic[i.split('#')[0].strip()] = int(i.split('#')[1])-1
        if len(i.split()) > 3:
            data[n] = (i.split())
            n +=1
    print "Example filename: {0}".format(data[1][labelsdic['_rlnImageName']].split('/')[-1])
    filetemplate = raw_input("type the file name with a single & in place of the numbers: ") or "micrograph&_particles.mrcs"
    assert '&' in filetemplate, "no & in filetemplate" 
    filename,ext = (filetemplate.split('&')[0],filetemplate.split('&')[1])
    
    print "Example filename: {0}".format(outexample).split("/")[-1]
    newfiletemplate = raw_input("type the template for the new filename (same format as above): ")
    assert '&' in newfiletemplate, "no & in filetemplate" 
    newfilename,newext = (newfiletemplate.split('&')[0],newfiletemplate.split('&')[1])
    
    
    for i in data:
        # find the micrograph number
        if data[i] != "[]":
            number1 = data[i][labelsdic['_rlnImageName']].split('/')[-1].replace(filename,"")
            number = number1.replace(ext,"")
            #construct the new filename
            newname = newfilename+number+newext
            newfilefinal =  '/'.join(data[i][labelsdic['_rlnImageName']].split('/')[:-1])+'/'+newname
            print newfilefinal
            data[i][labelsdic['_rlnImageName']] = newfilefinal
            print data[i]
    
    output = open(zz,'w')
    for i in header:
        output.write(i)
    output.write("\n")
    for i in data:
        data[i][-1] = data[i][-1].strip("\n")
        output.write("\n")
        for j in data[i]:
            output.write(j+"\t")
#######################################################################################################

####        ####
#    DO it!    #
###         ####

allthemrcs = makemrcs(raw_input("Search string for starfiles to operate on: ") or "Particles/Micrographs/*movie*.star") 
print allthemrcs
print len(allthemrcs)," files"
allthemrcs.sort()
outexample = unblurall(allthemrcs)
selstarfile = raw_input("Name of input particle file: ") or "particles.star" 
outputstar = raw_input("Name of output star file: ") or "unblurtest.star"
write_updated_starfile(selstarfile,outputstar,outexample)
