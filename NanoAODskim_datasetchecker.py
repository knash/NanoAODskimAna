from optparse import OptionParser
import sys
import Utilities.General.cmssw_das_client as das_client


import NanoAODskim_Functions	
from NanoAODskim_Functions import *

parser = OptionParser()

parser.add_option('--submit', metavar='F', action='store_true',
                  default=False,
                  dest='submit',
                  help='submit')
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')
parser.add_option('--signal', metavar='F', action='store_true',
                  default=False,
                  dest='signal',
                  help='Analyzer')
parser.add_option('--count', metavar='F', action='store_true',
                  default=False,
                  dest='count',
                  help='Analyzer')
parser.add_option('--ttbar', metavar='F', action='store_true',
                  default=False,
                  dest='ttbar',
                  help='Analyzer')
parser.add_option('--wjets', metavar='F', action='store_true',
                  default=False,
                  dest='wjets',
                  help='Analyzer')
parser.add_option('--gjets', metavar='F', action='store_true',
                  default=False,
                  dest='gjets',
                  help='Analyzer')
parser.add_option('--qcd', metavar='F', action='store_true',
                  default=False,
                  dest='qcd',
                  help='Analyzer')
parser.add_option('--data', metavar='F', action='store_true',
                  default=False,
                  dest='data',
                  help='Analyzer')

(options, args) = parser.parse_args()

subsignal=options.signal
subdata=options.data
subqcd=options.qcd
subttbar=options.ttbar
subwjets=options.wjets
subgjets=options.gjets

if not (subsignal or subdata or subqcd or subttbar or subwjets or subgjets):
	subsignal , subdata , subqcd , subttbar , subwjets , subgjets = True , True , True , True , True , True
	if options.anatype!="Pho":
		subgjets = False
	if options.anatype!="WW":
		subwjets = False

NanoF = NanoAODskim_Functions(options.anatype,options.era)

if options.era=="2016":
	minset="RunIISummer16MiniAODv3"
elif options.era=="2017":
	minset="RunIIFall17MiniAODv2"
elif options.era=="2018":
	minset="RunIIAutumn18MiniAOD"
setstofind=[]
if options.anatype=="tHb":
	setstofind=NanoF.allsignamesHT 
	exs="Ht"
if options.anatype=="tZb":
	setstofind=NanoF.allsignamesZT 
	exs="Zt"
filessig=glob.glob("/eos/cms/store/group/phys_b2g/knash/WpTo*Nar*Nar*"+exs+"*/"+minset+"*")
#print "nfolders",len(filessig)
#print "setstofind",len(setstofind)
allsets=[]
setsdict = {}
badsets=[]
for ff in filessig:
	roots=glob.glob(ff+"/*/*/*.root")

	#print	ff.split("/")[7]
	setn=ff.split("/")[7]
	if setn in setsdict:
		setsdict[setn]+=roots
	else :
		setsdict[setn]=roots
clfile=open('jobstoclean'+options.era+exs, 'w+') 
numbsarr=[]
for ff in setsdict:

	fnums = []
	for rr in setsdict[ff]:
		fnums.append(int(rr.split("_")[-1].replace(".root","")))
	if len(fnums)>0:
	
		allsets.append(ff)
		if max(fnums)!=len(fnums):
			badsets.append([ff,copy.deepcopy(setsdict[ff])])
			numbsarr.append([ff,max(fnums),len(fnums)])
			print ff,max(fnums),len(fnums)

	else:
		print ff+"/*/*/*.root"
		print "no roots",allsets[-1]
print
print "Incomplete Sets"
bsind=0
for bb in badsets:
	print "mismatch",numbsarr[bsind]
	print "setname ","/"+numbsarr[bsind][0]+"/"+minset+"*/MINIAODSIM"
	clfile.write(bb[0]+"\n")
	for jj in bb[1]:
		clfile.write( "\t"+jj+"\n")
	clfile.write( "\n")

	bsind+=1
print ""
clfile.close()
for sf in setstofind:
	#print sf
	if not (sf in allsets):
		print "checking ","/"+sf+"/"+minset+"*/MINIAODSIM"
		query = das_client.get_data("dataset=/"+sf+"/"+minset+"*/MINIAODSIM")
		items = query.items()
		foundit=False
		for ii in items:
			if ii[0]=="status" and ii[1]=="error":
				print ii
			if ii[0]=="data":
				for jj in  ii[1]:
					dname = jj["dataset"][0]["name"]
					foundit=True
					print dname,"20000"
		if not foundit:

			print "dataset=/"+sf+"/"+minset+"*/MINIAODSIM", "not in DAS!"
