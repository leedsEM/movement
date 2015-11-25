# movement scripts
These scripts are described in Rawson et al (2016).

PPunblur.py: uses unblur to perform per-partcle motiion correction.  The script must be updated by adding the path to your installation of unblur.  The script was tested using unblur 7.17.15.  it also requires an installation of relion which it calls form the command line using 'relion'.  If relion is called using a different command on your system this should be changed on line 108.  The script was written and tested using relion 1.4, although there is built in back compatibility with relion 1.3.  To use the script on files generated using relion 1.3 run it with a '-r13' flag.

recenter.py: applies particle shifts from relion to the original picked particle coordinates and outputs a new star file that can be used for particle extraction in relion

reorder4LMBFGS: reorders a relion star file to it can be used in the program LMBFGS for per-particle morion correction.  It requires input of a star file for each micrograph.  The output star files are written with fortran formatted columns, which are required for LMBFGS to operate properly.

For questions and support on these scripts contact Matt Iadanza (fbsmi@leeds.ac.uk)
