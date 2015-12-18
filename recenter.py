#!/usr/bin/python


### apply relion's particles shifts to the original boxes to generate particles that are better centered


## get the relion file and read the data
relionfile = open(raw_input("Name of starfile: ") or "15Jun_shiny2_ref_data.star", "r")
odata = relionfile.readlines()

## find the labels and identify the right columns; put in labeldic
vers = "1.0"
print "**** particle recentereing v {0} ****".format(vers)


labelnames = ("_rlnCoordinateX","_rlnCoordinateY","_rlnOriginX","_rlnOriginY","_rlnMicrographName")
labeldic = {}
for i in odata:
    if any(s in i for s in labelnames):
        labeldic[i.split()[0]] = int(i.split()[1].strip('#'))  

# put all of the data into an array
data = []
for i in odata:
    if len(i.split()) > 4: 
        data.append(i.split())

# find the filenames, make a list of them
filenames = []
for i in data:
    if i[labeldic["_rlnMicrographName"]-1] not in filenames:
        filenames.append(i[labeldic["_rlnMicrographName"]-1])

# make a starfile for each original file with the new corrdinates

for i in filenames:
    writename = i.split('/')[-1].split('.')[0]
    fileout = open("{0}_recentered.star".format(writename),"w")
    fileout.write("\ndata_\n\nloop_\n_rlnCoordinateX #1\n_rlnCoordinateY #2\n")
    for j in data:
        if j[labeldic["_rlnMicrographName"]-1] == i:
            newx = float(j[labeldic["_rlnCoordinateX"]-1]) - float(j[labeldic["_rlnOriginX"]-1])
            newy = float(j[labeldic["_rlnCoordinateY"]-1]) - float(j[labeldic["_rlnOriginY"]-1])
            fileout.write("{0}\t{1}\n".format(newx,newy)) 
    print "wrote file:  {0}_recentered.star".format(writename)
