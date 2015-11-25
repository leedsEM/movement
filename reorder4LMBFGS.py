#!/usr/bin/python
import glob
import os
import sys

## find the labels and identify the right columns; put in labeldic
#
vers = "0.3"


# vers 0.3 updated to output in fortran formatted numbers


print "**** reorder starfile for individual particle correction using LMBFGS  v {0}".format(vers)

### ---- function: reorder the starfile -----------
def reorder_starfile(filename):
    relionfile = open(filename, "r")
    odata = relionfile.readlines()
    data = []
    for i in odata:
        if len(i.split()) > 3:
            data.append(i)
    # get the column number
    for i in odata:
        if '_rlnImageName' in i:
            colnum = int(i.split('#')[-1]) -1
    labelsdic = {}
    for i in data:
        if i.split()[colnum].split("/")[-1] in labelsdic.keys():
            labelsdic[i.split()[colnum].split("/")[-1]].append(i.split())
        if i.split()[colnum].split("/")[-1] not in labelsdic.keys():
            labelsdic[i.split()[colnum].split("/")[-1]] = [i.split()]
    

    ## write new header
    output = open("{0}_LMBFGS.star".format(filename.split('.')[0]),"w")
    for i in odata:
        if len(i.split()) < 3:
            output.write(i)
    
    # write the particles 
    for key in sorted(labelsdic):
        for line in labelsdic[key]:
            output.write("\n")
            print line
            for i in line:
                if is_number(i):
                    count = len(i.split('.'))
                    if count > 1:
                        i = float(i)
                        if len(str(i).split('.')[0]) > 5:
                            output.write("{0:.6e} ".format(i))
                        else:
                            output.write("{0:12.6f} ".format(i))
                    else:
                        output.write("{0: 12d} ".format(int(i)))
                else:
                    output.write("{0} ".format(i))
    return("{0}_LMBFGS.star".format(filename.split('.')[0]))

#-----------------------------------------------------------------------

#------- function test if string is a number --------------------------#
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#-----------------------------------------------------------------------

## get the relion file and read the data
files = glob.glob(raw_input("star files search string: ") or "*.star")
assert len(files) >= 1, "no files found"

for i in files:
    print i
    
go = raw_input("Do it? (Y/N)")
if go in ("Y","y","yes","YES","Yes"):
    for each in files:
        newfile = reorder_starfile(each)
        print each," --> ",newfile
        
