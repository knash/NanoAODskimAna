#! /usr/bin/env python
import re
import os
import subprocess
from os import listdir
from os.path import isfile, join
import glob
import copy
import math
import ROOT
#from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
		  default	=	'Mu',
		  dest		=	'anatype',
		  help		=	'')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
		  default	=	'2017',
		  dest		=	'era',
		  help		=	'2016,2017, or 2018')
parser.add_option('-d', '--disc', metavar='F', type='string', action='store',
                  default	=	'0.9',
                  dest		=	'disc',
                  help		=	'')


parser.add_option('-f', '--sfval', metavar='F', type='string', action='store',
                  default	=	'1.0',
                  dest		=	'sfval',
                  help		=	'')


(options, args) = parser.parse_args()


addstrsf=""
if options.sfval!="1.0":
	addstrsf+="_SF"+(options.sfval).replace(".","p")
#if options.pt!='470to1400':
#	addstrsf+="_Pt"+(options.pt)
cnnstr = "*_CNN"+(options.disc).replace(".","p")
addstrsf+=cnnstr
	

#files = sorted(glob.glob("ThetaFile_ttfit_"+options.anatype+options.anatypePSET_"+options.cuts+addstrsf+"*.root"))

files = sorted(glob.glob("ThetaFile_ttfit_"+options.anatype+options.era+addstrsf+"*.root"))
print "ThetaFile_ttfit_"+options.anatype+options.era+addstrsf+"*.root"
#subprocess.call( ["source setuptheta.csh"], shell=True )
commands = []
commands.append("rm histos-"+cnnstr+"*.root")
commands.append("rm postfithistos/histos-"+cnnstr+"*.root")
commands.append("rm prefithistos/histos-"+cnnstr+"*.root")
ifile=0
csvpt=""
#print "processing:"
for cfile in files:
	cfile[cfile.find(options.era):cfile.find(".root")]
	csvpt+= cfile[cfile.find(options.era):cfile.find(".root")]
	if cfile!=files[-1]:
		csvpt+=","
#	commands.append("rm -rf analysis")
#	commands.append("sed 's/RFILE/"+cfile+"/g' analysis_tmassfit_CNN.py > temp_limits"+str(ifile)+".py")
#	commands.append("python run_theta.py --file=temp_limits"+str(ifile)+".py")
#	ifile+=1
print csvpt
commands.append("sed 's/RFILE/"+csvpt+"/g' analysis_tmassfit_CNN_combo.py > temp_limits.py")
commands.append("python run_theta.py --file=temp_limits.py")
for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )


