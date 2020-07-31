from optparse import OptionParser
import sys


import NanoAODskim_Functions	
from NanoAODskim_Functions import *

parser = OptionParser()

parser.add_option('--submit', metavar='F', action='store_true',
                  default=False,
                  dest='submit',
                  help='submit')
parser.add_option('--sum', metavar='F', action='store_true',
                  default=False,
                  dest='sum',
                  help='sum')
parser.add_option('--Ana', metavar='F', action='store_true',
                  default=False,
                  dest='Ana',
                  help='Analyzer')
parser.add_option('--Bkg', metavar='F', action='store_true',
                  default=False,
                  dest='Bkg',
                  help='Background')
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')
parser.add_option('-p', '--pyfile', metavar='F', type='string', action='store',
                  default	=	'NanoAODskim_Generic.py',
                  dest		=	'pyfile',
                  help		=	'Pho or tHb')
parser.add_option('-f', '--folder', metavar='F', type='string', action='store',
                  default	=	'rootfiles',
                  dest		=	'folder',
                  help		=	'rootfiles')
parser.add_option('-b', '--sigbatch', metavar='F', type='int', action='store',
                  default	=	'1',
                  dest		=	'sigbatch',
                  help		=	'sigbatch')
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
parser.add_option('--singletop', metavar='F', action='store_true',
                  default=False,
                  dest='singletop',
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
parser.add_option('--nosubmit', metavar='F', action='store_true',
                  default=False,
                  dest='nosubmit',
                  help='Analyzer')
parser.add_option('--cutopt', metavar='F', action='store_true',
		  default=False,
		  dest='cutopt',
		  help='cutopt')
parser.add_option('--semilep', metavar='F', action='store_true',
		  default=False,
		  dest='semilep',
		  help='semilep')
(options, args) = parser.parse_args()

subsignal=options.signal
subdata=options.data
subqcd=options.qcd
subttbar=options.ttbar
subsingletop=options.singletop
subwjets=options.wjets
subgjets=options.gjets

semilep=options.semilep

foldtosave = options.folder

if not (subsignal or subdata or subqcd or subttbar or subsingletop or subwjets or subgjets):
	subsignal , subdata , subqcd , subttbar , subsingletop , subwjets , subgjets = True , True , True , True , True , True , True
	logging.warning("Running default jobs")

	if options.anatype!="Pho":
		subgjets = False
	if options.anatype!="WW":
		subwjets = False
	if semilep:
		subwjets = True
		subgjets = True
if options.Ana:
	macro="Ana"
elif options.Bkg:
	macro="Bkg"
	subsignal=options.signal
	if not subsignal:
	     logging.warning("signal needs to be turned on explicitly for Bkg")
else:
     logging.error("Must Select a Analysis Type")
     sys.exit()
NanoF = NanoAODskim_Functions(options.anatype,options.era)
if True:
	pyfile = options.pyfile

	ftoadd = 0 

	numfdata = 30
	numfqcd = [6,6,6]
	numfgjets = [1,1]
	numfwjets = [1,1,1]
	numfttbar1000 = 12
	numfttbar700 = 2
	numfttbarH = 1
	numfttbarS = 1

	numfsingletopwt = 1
	numfsingletopwtb = 1
	

	datf=""
	mcf="-f /eos/cms/store/group/phys_b2g/knash"
	if options.era=="2018":

		numfdata = 40
		numfqcd = [7,7,7]
		numfgjets = [1,1]
		numfwjets = [1,1,1]
		numfttbar1000 = 15
		numfttbar700 = 2
		numfttbarH = 1
		numfttbarS = 1
		numfsingletopwt = 1
		numfsingletopwtb = 1
	if options.era=="2016":

		numfdata = 30
		numfqcd = [5,5,5]
		numfgjets = [1,1]
		numfwjets = [1,1,1]
		numfttbar1000 = 10
		numfttbar700 = 2
		numfttbarH = 1
		numfttbarS = 1
		numfsingletopwt = 1
		numfsingletopwtb = 1
	if pyfile=="NanoAODskim_EventCounter.py":
		numfdata = 1
		numfqcd = [1,1,1]
		numfgjets = [1,1]
		numfwjets = [1,1,1]
		numfttbar1000 = 1
		numfttbar700 = 1
		numfttbarH = 1
		numfttbarS = 1
		numfsingletopwt = 1
		numfsingletopwtb = 1

	if semilep:
		numfdata = 20
		numfqcd = [1,1,1,1,1,1]
		numfgjets = [1,1]
		numfwjets = [2,10,15,20,30]
		numfttbar1000 = 1
		numfttbar700 = 1
		numfttbarH = 1
		numfttbarS = 20
		numfsingletopwt = 1
		numfsingletopwtb = 1

	if pyfile=="NanoAODskim_Generic_RDFskim.py":
		numfdata = 10
		numfqcd = [3,3,3]
		numfgjets = [1,1]
		numfwjets = [1,1,1]
		numfttbar1000 = 1
		numfttbar700 = 1
		numfttbarH = 1
		numfttbarS = 10
		numfsingletopwt = 1
		numfsingletopwtb = 1
		datf="-f /eos/cms/store/user/knash/rdfskims/"
		mcf="-f /eos/cms/store/user/knash/rdfskims/"
	exstr=""
	if options.cutopt:
		exstr=" --cutopt "
	#print totjobcalc,"jobs"
	#pyfile = "NanoAODskim_Generic_Alpha.py"
	if options.era=="2016":
		minset="RunIISummer16MiniAODv3"
	elif options.era=="2017":
		minset="RunIIFall17MiniAODv2"
	elif options.era=="2018":
		minset="RunIIAutumn18MiniAOD"
	batch=options.sigbatch

	sstr="NanoSlimNtuples"+options.era
	if semilep:
		sstr="NanoSlimNtuplessinglelep"+options.era
	vstr=""
	if semilep:
		vstr=" -v _v11 "
	if options.submit:
		print "Submitting "+options.era+"..."

		
		with open('temp.listOfJobs', 'w+') as tempcommands:
		    
		    if subdata:

			   print "\t...Data"
			   if semilep:
		           	vstr=" -v _v10 "
				if options.anatype=="Mu":
			   		for j in xrange(numfdata):
			    			tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  SingleMuon -j '+str(j+1)+' -t '+str(numfdata)+'  --'+macro+' -e '+options.era+' -S Run' +options.era +' '+datf+' '+mcf+vstr+exstr+' --condor\n')
				if options.anatype=="Ele":
			    		if options.era=="2018":
			   			for j in xrange(numfdata):
			    				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  EGamma  -j '+str(j+1)+' -t '+str(numfdata)+'  --'+macro+' -e '+options.era+' -S Run' +options.era +' '+datf+' '+mcf+vstr+exstr+' --condor\n')
			   	   	else:
			   			for j in xrange(numfdata):
			    				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  SingleElectron -j '+str(j+1)+' -t '+str(numfdata)+'  --'+macro+' -e '+options.era+' -S Run' +options.era +' '+datf+' '+mcf+vstr+exstr+' --condor\n')
			   	vstr=" -v _v11 "
			   else:
			   	for j in xrange(numfdata):
			    		tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  JetHT -j '+str(j+1)+' -t '+str(numfdata)+'  --'+macro+' -e '+options.era+' -S Run' +options.era +' '+datf+exstr+' --condor\n')
			    

		    if subsignal:
			    print "\t...Signal"
			    if options.anatype=="Pho":
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2  --'+macro+' -e '+options.era+exstr+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToRWToTri_Wkk3000R100_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2  --'+macro+' -e '+options.era+' --condor\n')
			    if options.anatype=="WW":
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M3000-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+exstr+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M3500-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+exstr+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M4000-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+exstr+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M4500-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+exstr+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M5000-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+exstr+' --condor\n')
			    #searchstring=minset
			    #if options.era=="2018":
				#print "2018 HACK!"
			        #searchstring="RunIIFall17MiniAODv2"
			    allvlq=NanoF.allsignamesHT + NanoF.allsignamesZT 
			    if options.anatype=="tHb":
		   			sigv= "-v v8,v10"
					#if True:
					#	thsigs = NanoF.ovrvecHT
					nsigs=0
					for thsig in allvlq:
						if nsigs%batch==0:
							msetstr=thsig
						else:
							msetstr+=","+thsig
						if nsigs%batch==batch-1:
							tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+msetstr+'  --'+macro+' -e '+options.era+' '+mcf+' '+sigv+exstr+' --condor\n')
							ftoadd+=batch-1
						nsigs+=1
			    
			    if options.anatype=="tZb":
		   			sigv= "-v v8,v10"
					#if True:
					#	tzsigs = NanoF.ovrvecZT
					nsigs=0
					for tzsig in allvlq:
						if nsigs%batch==0:
							msetstr=tzsig
						else:
							msetstr+=","+tzsig
						if nsigs%batch==batch-1:
							tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+msetstr+'  --'+macro+' -e '+options.era+' '+mcf+' '+sigv+exstr+' --condor\n')
							ftoadd+=batch-1
						nsigs+=1
					

		    if subqcd:


			    if options.era=="2016":
				    if semilep:
					vstr=" -v _v11 "
				    print "\t...QCD"
				    for j in xrange(numfqcd[0]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[0])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'  --condor\n')
				    for j in xrange(numfqcd[1]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[1])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')
				    for j in xrange(numfqcd[2]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[2])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
			   	    if semilep:
					   # for j in xrange(numfqcd[3]):
					    #	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[3])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
					    for j in xrange(numfqcd[4]):
					    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[4])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
					    for j in xrange(numfqcd[5]):
					    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[5])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
				    if semilep:
					vstr=" -v _v11 "

	
			    if options.era=="2017":
				    print "\t...QCD"
				    for j in xrange(numfqcd[0]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[0])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'    --condor\n')
				    for j in xrange(numfqcd[1]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[1])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'    --condor\n')
				    for j in xrange(numfqcd[2]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[2])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'    --condor\n')	
			   	    if semilep:
					  #  for j in xrange(numfqcd[3]):
					   # 	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[3])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
					    for j in xrange(numfqcd[4]):
					    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[4])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
					    for j in xrange(numfqcd[5]):
					    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[5])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
	
			    if options.era=="2018":
				    print "\t...QCD"
				    for j in xrange(numfqcd[0]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[0])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')
				    for j in xrange(numfqcd[1]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[1])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')
				    for j in xrange(numfqcd[2]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[2])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')
			   	    if semilep:
					    #for j in xrange(numfqcd[3]):
					    #	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[3])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
					    for j in xrange(numfqcd[4]):
					    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[4])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
					    for j in xrange(numfqcd[5]):
					    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[5])+'  --'+macro+' -e '+options.era+' '+mcf+exstr+vstr+' -S '+sstr+'   --condor\n')	
		    if subsingletop:
			    if (not semilep):
			    	stv= " -v _v10 "
			    	stsets=["ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"]
			    	if options.era=="2018":
				  	  stsets=["ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8","ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8"]


			    	print "\t...single top"
			    	for j in xrange(numfsingletopwt):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+stsets[0]+' -j '+str(j+1)+' -t '+str(numfsingletopwt)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+stv+exstr+' -S '+sstr+' --condor\n')	
			    	for j in xrange(numfsingletopwtb):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+stsets[1]+' -j '+str(j+1)+' -t '+str(numfsingletopwtb)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+stv+exstr+' -S '+sstr+' --condor\n')

		    if subttbar:
			    if semilep:
			    	ttsets=["TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8","TTToHadronic_TuneCP5_13TeV-powheg-pythia8"]
			    	if options.era in ["2016","2017"] :
					ttsets=["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8"]


			    	for j in xrange(numfttbarS):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+ttsets[0]+' -j '+str(j+1)+' -t '+str(numfttbarS)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+vstr+exstr+' -S '+sstr+' --condor\n')	
			    	for j in xrange(numfttbarH):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+ttsets[1]+' -j '+str(j+1)+' -t '+str(numfttbarH)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+vstr+exstr+' -S '+sstr+' --condor\n')
			    else:
			    	ttv= " -v _v10 "
			    	ttsets=["TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8","TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8"]
			    	if options.era=="2016":
			 		  ttv= ""
					  ttsets=["TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8","TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8"]
			    	if options.era=="2018":
				 	  ttv= " -v _v10 "
				  	  ttsets=["TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8","TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8"]


			    	print "\t...ttbar"
			    
			    	for j in xrange(numfttbar700):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+ttsets[0]+' -j '+str(j+1)+' -t '+str(numfttbar700)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+ttv+exstr+' -S '+sstr+' --condor\n')	
			    	for j in xrange(numfttbar1000):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  '+ttsets[1]+' -j '+str(j+1)+' -t '+str(numfttbar1000)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+ttv+exstr+' -S '+sstr+' --condor\n')
			    #else:
				#    print "\t...ttbar"
				 #   for j in xrange(numfttbarH):
				  #  	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  TTToHadronic_TuneCP5_13TeV-powheg-pythia8 -j '+str(j+1)+' -t '+str(numfttbarH)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+exstr+' --condor\n')
				   # for j in xrange(numfttbarS):
				    #	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 -j '+str(j+1)+' -t '+str(numfttbarS)+'  --'+macro+' -e '+options.era+' '+mcf+'  '+exstr+' --condor\n')
		    #if subgjets:  
			#    print "\t...gjets" 
		   	 #   for j in xrange(numfgjets[0]):
			  #  	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8 -f store\/group\/phys_b2g\/ -j '+str(j+1)+' -t '+str(numfgjets[0])+'  --'+macro+' -e '+options.era+exstr+' -S '+sstr+' --condor\n')
			   # for j in xrange(numfgjets[1]):
			    #	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8 -f store\/group\/phys_b2g\/ -j '+str(j+1)+' -t '+str(numfgjets[1])+'  --'+macro+' -e '+options.era+exstr+' -S '+sstr+' --condor\n')
		    if subwjets:   
			    if semilep:
				tune="TuneCP5"
				if options.era=="2016":
					tune="TuneCUETP8M1"
			    	for j in xrange(numfwjets[0]):		
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToLNu_HT-400To600_'+tune+'_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' '+mcf+' '+ ' -t '+str(numfwjets[0])+'  --'+macro+' -e '+options.era+vstr+exstr+' -S '+sstr+' --condor\n')
			 	for j in xrange(numfwjets[1]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToLNu_HT-600To800_'+tune+'_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' '+mcf+' '+ ' -t '+str(numfwjets[1])+'  --'+macro+' -e '+options.era+vstr+exstr+' -S '+sstr+' --condor\n')
				for j in xrange(numfwjets[2]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToLNu_HT-800To1200_'+tune+'_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' '+mcf+' '+ ' -t '+str(numfwjets[2])+'  --'+macro+' -e '+options.era+vstr+exstr+' -S '+sstr+' --condor\n')
				for j in xrange(numfwjets[3]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToLNu_HT-1200To2500_'+tune+'_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' '+mcf+' '+ ' -t '+str(numfwjets[3])+'  --'+macro+' -e '+options.era+vstr+exstr+' -S '+sstr+' --condor\n')
				for j in xrange(numfwjets[4]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToLNu_HT-2500ToInf_'+tune+'_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' '+mcf+' '+  ' -t '+str(numfwjets[4])+'  --'+macro+' -e '+options.era+vstr+exstr+' -S '+sstr+' --condor\n')
		num_lines = sum(1 for line in open('temp.listOfJobs'))
		   
		print "num jobs",num_lines
		
		output = open('logs/nj'+options.anatype+macro+options.era, 'w+')
		output.write(str(num_lines+ftoadd))
		output.close()

		commands = []
		commands.append("rm tarball.tgz") 
		commands.append("tar czvf tarball.tgz "+pyfile+" PhysicsTools NanoAODskim_RateMaker__*.root  PUF_*201*.root topSF_201*.root NanoAODskim_PUMaker__*.root NanoAODskim_TrigMaker__*.root NanoAODskim_Functions.py NanoAODskim_Data.py NanoAODskim_EventCounter.py") 
		commands.append("./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz temp.listOfJobs commands"+options.anatype+macro+options.era+".cmd")
		if not (options.nosubmit):
			commands.append("./runManySections.py --submitCondor commands"+options.anatype+macro+options.era+".cmd")
			commands.append("condor_q knash")

	elif options.sum:
		print "Summing "+options.era+"..."
		numfs=0
		try:
			with open('logs/nj'+options.anatype+macro+options.era) as linel:
  				numfs = int((linel.readlines())[0])
		except:
			print "missing file count"
		print "numfs from file",numfs		

		files = glob.glob('NanoAODskim_'+options.anatype+macro+options.era+'*.root')
		#if len(files)!=numfs:
		#	print
		#	print "!!!!!!!!!!!!!!!!!!!!"
		#	logging.warning("Not All Jobs Accounted For"+"\n"+str(len(files))+" vs "+str(numfs))
		#	print "!!!!!!!!!!!!!!!!!!!!"
		#	print
		commands = []	
		commands.append("rm logs/*.log")
		commands.append("mv *.log logs/")
		commands.append("rm notneeded/*")
		commands.append("rm rootfiles_tosum/*.root")
		sets = []

		for cfile in files:
			statinfo = os.stat(cfile)
			if statinfo.st_size<500:
				logging.warning("Possible Unfilled File "+cfile)
			if cfile.find('job')==-1:
				continue
			initindex = cfile.split("__")[-1].find("of")+2
			cjob =cfile.split("__")[-1].replace(".root","")[initindex:]
			found=False
			for cset in sets:
				if cset.replace(cfile.split("__")[-1],"")==cfile.replace(cfile.split("__")[-1],""):
					found=True
			if not found:
				sets.append(cfile.replace(cfile.split("__")[-1],""))
				fileset = glob.glob(sets[-1] + "job*of"+cjob+".root")
				if int(cjob)!=len(fileset):
					print
					print "!!!!!!!!!!!!!!!!!!!!"
					logging.error("Wrong Number Of Jobs For "+cfile.replace(cfile.split("__")[-1],"")+"\n"+str(cjob)+" vs "+str(len(glob.glob(sets[-1] + "job*of"+cjob+".root"))))
					print "!!!!!!!!!!!!!!!!!!!!"
					print
					#sys.exit()
					for jj in xrange(int(cjob)):
						if not ((sets[-1] + "job"+str(jj+1)+"of"+cjob+".root") in fileset):
							print "output_$(JID)        python ./tardir/"+pyfile+" -a "+options.anatype+" -s  "+sets[-1]+" -j "+str(jj+1)+" -t "+cjob+"  --"+macro+" -e "+options.era+" "+mcf+exstr+"  --condor"
				commands.append("hadd -f " + sets[-1][0:-2] + ".root " + sets[-1] + "job*of"+cjob+".root")
				commands.append("mv  " + sets[-1] + "job*of"+cjob+".root" + " rootfiles_tosum/" )
		print 
		print "------------"
		print "Summing Jobs"
		print "------------"
		for s in commands :
		    print 'executing ' + s
		    subprocess.call( [s], shell=True )


		files = glob.glob("NanoAODskim_"+options.anatype+macro+options.era+"*.root")
		QCDfiles = []
		TTfiles = []
		STfiles = []
		GJetsfiles = []
		WJetsfiles = []
		commands = []
		ttstr="TT_Mtt"
		#ttstr="TTTo"
		#if options.era=="2016":
		#	ttstr="TT_Mtt"
		###NEEDS TO BE FIXED FOR OTHER DELIMETERS
		for cfile in files:

			if cfile.split("__")[1].find("QCD_HT")!=-1:
				print "QCD File",cfile
				QCDfiles.append(cfile)
			elif cfile.split("__")[1].find("ST_tW")!=-1:
				print "ST File",cfile
				STfiles.append(cfile)
			elif cfile.split("__")[1].find(ttstr)!=-1:
				print "TT File",cfile
				TTfiles.append(cfile)
			elif cfile.split("__")[1].find("GJets")!=-1:
				print "GJets File",cfile
				GJetsfiles.append(cfile)
			elif cfile.split("__")[1].find("WJets")!=-1:
				print "WJets File",cfile
				WJetsfiles.append(cfile)
			else:
				commands.append("mv "+cfile+" "+foldtosave )


		if subqcd:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__QCD.root "
			for QCDfile in QCDfiles:	
				commstr+=QCDfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__QCD.root  "+foldtosave) 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__QCD_HT*.root rootfiles_tosum/" )

		if subttbar:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__TT.root "
			for TTfile in TTfiles:	
				commstr+=TTfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__TT.root  "+foldtosave) 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__"+ttstr+"*.root rootfiles_tosum/" )


		if subsingletop:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__ST.root "
			for STfile in STfiles:	
				commstr+=STfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__ST.root  "+foldtosave) 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__ST_tW*.root rootfiles_tosum/" )


		if subgjets:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__GJets.root "
			for GJetsfile in GJetsfiles:	
				commstr+=GJetsfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__GJets.root  "+foldtosave) 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__GJets_HT*.root rootfiles_tosum/" )


		if subwjets:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__WJets.root "
			for WJetsfile in WJetsfiles:	
				commstr+=WJetsfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJets.root  "+foldtosave) 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJetsToQQ_HT*.root rootfiles_tosum/" )




	    	sets = list(set(sets))
		print 
		print "------------"
		print "Summing Sets"
		print "------------"
	elif options.count :
		commands=[]
		fdir ={}
		files = glob.glob("NanoAODskim_EV"+options.era+"*.root")
		files.sort()
		for cfile in files: 
			print cfile
			tf=TFile(cfile)
			cstr = cfile.split("__")[1].replace(".root","")
			fdir[cstr] = tf.Get("allgenweight").GetMean()
		print fdir

	else:
		logging.error("Please Select --submit or --sum")
		sys.exit()





for s in commands :
    print "executing " + s
    subprocess.call( [s], shell=True )

