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
parser.add_option('--signal', metavar='F', action='store_true',
                  default=False,
                  dest='signal',
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
parser.add_option('--nosubmit', metavar='F', action='store_true',
                  default=False,
                  dest='nosubmit',
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


if options.Ana:
	macro="Ana"
elif options.Bkg:
	macro="Bkg"
else:
     logging.error("Must Select a Analysis Type")
     sys.exit()

if options.era=="2017" or options.era=="2018" :
	print "Submitting "+options.era
	#numfdata = 60
	numfdata = 110
	#numfqcd = [20,40,30]
	numfqcd = [40,30,30]
	numfgjets = [1,1]
	numfwjets = [2,2,7]
	numfttbarH = 15
	numfttbarS = 10
	

	#print totjobcalc,"jobs"
	print "Sumbitting..."
	#pyfile = "NanoAODskim_Generic_Alpha.py"
	pyfile = "NanoAODskim_Generic.py"
	if options.submit:
		
		with open('temp.listOfJobs', 'w+') as tempcommands:
		    
		    if subdata:
			   print "\t...Data"
			   for j in xrange(numfdata):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  JetHT -j '+str(j+1)+' -t '+str(numfdata)+'  --'+macro+' -e '+options.era+' -S Run' +options.era +' --condor\n')
			    

		    if subsignal:
			    print "\t...Signal"
			    if options.anatype=="Pho":
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2  --'+macro+' -e '+options.era+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToRWToTri_Wkk3000R100_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2  --'+macro+' -e '+options.era+' --condor\n')
			    if options.anatype=="WW":
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M3000-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M3500-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M4000-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M4500-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+' --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WkkToWRadionToWWW_M5000-R0-06_TuneCP5_13TeV-madgraph  --'+macro+' -e '+options.era+' --condor\n')
			    
		    
			    if options.anatype=="tHb":
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2000Nar_Tp1000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2000Nar_Tp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2500Nar_Tp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp3000Nar_Tp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				

		    
			    if options.anatype=="tZb":
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2000Nar_Tp1000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2000Nar_Tp1700Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2500Nar_Tp1300Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WpToTpB_Wp2500Nar_Tp1700Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				


		    if subqcd:
			    if options.era=="2017":
				    print "\t...QCD"
				    for j in xrange(numfqcd[0]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[0])+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				    for j in xrange(numfqcd[1]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[1])+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				    for j in xrange(numfqcd[2]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[2])+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
			    if options.era=="2018":
				    print "\t...QCD"
				    for j in xrange(numfqcd[0]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[0])+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				    for j in xrange(numfqcd[1]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[1])+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
				    for j in xrange(numfqcd[2]):
				    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[2])+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash --condor\n')
		    if subttbar:
			    print "\t...ttbar"
			    for j in xrange(numfttbarH):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  TTToHadronic_TuneCP5_13TeV-powheg-pythia8 -j '+str(j+1)+' -t '+str(numfttbarH)+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples'+options.era+'mc '+' --condor\n')
			    for j in xrange(numfttbarS):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 -j '+str(j+1)+' -t '+str(numfttbarS)+'  --'+macro+' -e '+options.era+' -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples'+options.era+'mc '+' --condor\n')
		    if subgjets:  
			    print "\t...gjets" 
		   	    for j in xrange(numfgjets[0]):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8 -f store\/group\/phys_b2g\/ -j '+str(j+1)+' -t '+str(numfgjets[0])+'  --'+macro+' -e '+options.era+' --condor\n')
			    for j in xrange(numfgjets[1]):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8 -f store\/group\/phys_b2g\/ -j '+str(j+1)+' -t '+str(numfgjets[1])+'  --'+macro+' -e '+options.era+' --condor\n')
		    if subwjets:   
			    print "\t...wjets"   
		   	    for j in xrange(numfwjets[0]):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfwjets[0])+'  --'+macro+' -e '+options.era+' --condor\n')
			    for j in xrange(numfwjets[1]):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfwjets[1])+'  --'+macro+' -e '+options.era+' --condor\n')
			    for j in xrange(numfwjets[2]):
			    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfwjets[2])+'  --'+macro+' -e '+options.era+' --condor\n')
		num_lines = sum(1 for line in open('temp.listOfJobs'))
		   
		print "num jobs",num_lines
		
		output = open('logs/nj'+options.anatype+macro+options.era, 'w+')
		output.write(str(num_lines))
		output.close()

		commands = []
		commands.append("rm tarball.tgz") 
		commands.append("tar czvf tarball.tgz "+pyfile+" NanoAODskim_RateMaker__*.root NanoAODskim_Functions.py NanoAODskim_Data.py") 
		commands.append("./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz temp.listOfJobs commands"+options.anatype+macro+options.era+".cmd")
		if not (options.nosubmit):
			commands.append("./runManySections.py --submitCondor commands"+options.anatype+macro+options.era+".cmd")
			commands.append("condor_q knash")

	elif options.sum:
		numfs=0
		try:
			with open('logs/nj'+options.anatype+macro+options.era) as linel:
  				numfs = int((linel.readlines())[0])
		except:
			print "missing file count"
		print "numfs from file",numfs		

		files = glob.glob('NanoAODskim_'+options.anatype+macro+options.era+'*.root')
		if len(files)!=numfs:
			print
			print "!!!!!!!!!!!!!!!!!!!!"
			logging.warning("Not All Jobs Accounted For"+"\n"+str(len(files))+" vs "+str(numfs))
			print "!!!!!!!!!!!!!!!!!!!!"
			print
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
				if int(cjob)!=len(glob.glob(sets[-1] + "job*of"+cjob+".root")):
					print
					print "!!!!!!!!!!!!!!!!!!!!"
					logging.error("Wrong Number Of Jobs For "+cfile.replace(cfile.split("__")[-1],"")+"\n"+str(cjob)+" vs "+str(len(glob.glob(sets[-1] + "job*of"+cjob+".root"))))
					print "!!!!!!!!!!!!!!!!!!!!"
					print
					#sys.exit()
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
		GJetsfiles = []
		WJetsfiles = []
		commands = []
		###NEEDS TO BE FIXED FOR OTHER DELIMETERS
		for cfile in files:
			if cfile.split("__")[1].find("QCD_HT")!=-1:
				print "QCD File",cfile
				QCDfiles.append(cfile)
			elif cfile.split("__")[1].find("TTTo")!=-1:
				print "TT File",cfile
				TTfiles.append(cfile)
			elif cfile.split("__")[1].find("GJets")!=-1:
				print "GJets File",cfile
				GJetsfiles.append(cfile)
			elif cfile.split("__")[1].find("WJets")!=-1:
				print "WJets File",cfile
				WJetsfiles.append(cfile)
			else:
				commands.append("mv "+cfile+" rootfiles/" )
		if subqcd:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__QCD.root "
			for QCDfile in QCDfiles:	
				commstr+=QCDfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__QCD.root rootfiles/") 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__QCD_HT*.root rootfiles_tosum/" )

		if subttbar:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__TT.root "
			for TTfile in TTfiles:	
				commstr+=TTfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__TT.root rootfiles/") 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__TTTo*.root rootfiles_tosum/" )

		if subgjets:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__GJets.root "
			for GJetsfile in GJetsfiles:	
				commstr+=GJetsfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__GJets.root rootfiles/") 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__GJets_HT*.root rootfiles_tosum/" )


		if subwjets:
			commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__WJets.root "
			for WJetsfile in WJetsfiles:	
				commstr+=WJetsfile+" "
			commands.append(commstr)
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJets.root rootfiles/") 
			commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJetsToQQ_HT*.root rootfiles_tosum/" )




	    	sets = list(set(sets))
		print 
		print "------------"
		print "Summing Sets"
		print "------------"
	else:
		logging.error("Please Select --submit or --sum")
		sys.exit()




if options.era=="2016":
	print "Submitting 2016"


	#numfdata = 40
	numfqcd = [20,40,30]
	numfgjets = [1,1]
	numfwjets = 8
	numfttbar700 = 5
	numfttbar1000 = 5
	nsigs = 0
	#if options.anatype=="Pho":
	#	nsigs = 2
	#if options.anatype=="WW":
	#	nsigs = 5
	#if options.anatype=="tHb":
	#	nsigs = 2
	#if options.anatype=="tZb":
	#	nsigs = 2
	#if options.anatype=="Bstar":
	#	nsigs = 0
	#if options.anatype=="Zprime":
	#	nsigs = 0


	if options.submit:
		with open('temp.listOfJobs', 'w+') as tempcommands:
		    


		    
		    #for j in xrange(numfdata):
		    #	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  JetHT -j '+str(j+1)+' -t '+str(numfdata)+'  --'+macro+' -e '+options.era+' --condor\n')

		    
		    for j in xrange(numfqcd[0]):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[0])+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    for j in xrange(numfqcd[1]):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[1])+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    for j in xrange(numfqcd[2]):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfqcd[2])+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    
		    for j in xrange(numfttbar700):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j '+str(j+1)+' -t '+str(numfttbar700)+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    
		    for j in xrange(numfttbar1000):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j '+str(j+1)+' -t '+str(numfttbar1000)+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')

	   	    for j in xrange(numfgjets[0]):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfgjets[0])+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    for j in xrange(numfgjets[1]):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfgjets[1])+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    
		    for j in xrange(numfwjets):
		    	tempcommands.write('python ./tardir/'+pyfile+' -a '+options.anatype+' -s  WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j '+str(j+1)+' -t '+str(numfwjets)+' -e '+options.era+'  --'+macro+' -e '+options.era+' --condor\n')
		    
		commands = []
		commands.append("rm tarball.tgz") 
		commands.append("tar czvf tarball.tgz "+pyfile+" NanoAODskim_RateMaker__*.root NanoAODskim_Functions.py") 
		commands.append("./development/runManySections.py --createCommandFile --cmssw --addLog --setTarball=tarball.tgz temp.listOfJobs commands"+options.anatype+macro+options.era+".cmd")
		commands.append("./runManySections.py --submitCondor commands"+options.anatype+macro+options.era+".cmd")
		commands.append("condor_q knash")

	elif options.sum:
		numfs=0
		try:
			with open('logs/nj'+options.anatype+macro+options.era) as linel:
  				numfs = int((linel.readlines())[0])
		except:
			print "missing file count"
		print "numfs from file",numfs		
		files = glob.glob('NanoAODskim_'+options.anatype+macro+'*.root')
		if len(files)!=numfs:
			print
			print "!!!!!!!!!!!!!!!!!!!!"
			logging.warning("Not All Jobs Accounted For"+"\n"+str(len(files))+" vs "+str(numfs))
			print "!!!!!!!!!!!!!!!!!!!!"
			print
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
				if int(cjob)!=len(glob.glob(sets[-1] + "job*of"+cjob+".root")):
					print
					print "!!!!!!!!!!!!!!!!!!!!"
					logging.error("Wrong Number Of Jobs For "+cfile.replace(cfile.split("__")[-1],"")+"\n"+str(cjob)+" vs "+str(len(glob.glob(sets[-1] + "job*of"+cjob+".root"))))
					print "!!!!!!!!!!!!!!!!!!!!"
					print
					#sys.exit()
				commands.append("hadd -f " + sets[-1][0:-2] + ".root " + sets[-1] + "job*of"+cjob+".root")
				commands.append("mv  " + sets[-1] + "job*of"+cjob+".root" + " rootfiles_tosum/" )
		print 
		print "------------"
		print "Summing Jobs"
		print "------------"
		for s in commands :
		    print 'executing ' + s
		    subprocess.call( [s], shell=True )


		files = glob.glob("NanoAODskim_"+options.anatype+macro+"*.root")
		QCDfiles = []
		TTfiles = []
		GJetsfiles = []
		WJetsfiles = []
		commands = []
		###NEEDS TO BE FIXED FOR OTHER DELIMETERS
		for cfile in files:
			if cfile.split("__")[1].find("QCD_HT")!=-1:
				print "QCD File",cfile
				QCDfiles.append(cfile)
			elif cfile.split("__")[1].find("TT_Mtt-")!=-1:
				print "TT File",cfile
				TTfiles.append(cfile)
			elif cfile.split("__")[1].find("GJets")!=-1:
				print "GJets File",cfile
				GJetsfiles.append(cfile)
			elif cfile.split("__")[1].find("WJets")!=-1:
				print "WJets File",cfile
				WJetsfiles.append(cfile)
			else:
				commands.append("mv "+cfile+" rootfiles/" )
		commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__QCD.root "
		for QCDfile in QCDfiles:	
			commstr+=QCDfile+" "
		commands.append(commstr)

		commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__TT.root "
		for TTfile in TTfiles:	
			commstr+=TTfile+" "
		commands.append(commstr)

		commstr = "hadd -f NanoAODskim_"+options.anatype+macro+options.era+"__GJets.root "
		for GJetsfile in GJetsfiles:	
			commstr+=GJetsfile+" "
		commands.append(commstr)

		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root NanoAODskim_"+options.anatype+macro+options.era+"__WJets.root")
		

		#####QCD == QCD+WJETS
		#commands.append("hadd -a NanoAODskim_"+options.anatype+macro+"__QCD.root NanoAODskim_"+options.anatype+macro+"__WJets.root ")


		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__QCD.root rootfiles/") 
		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__QCD_HT*.root rootfiles_tosum/" )

		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__TT.root rootfiles/") 
		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__TT_Mtt-*.root rootfiles_tosum/" )

		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__GJets.root rootfiles/") 
		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__GJets_HT*.root rootfiles_tosum/" )

		commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJets.root rootfiles/") 
		#commands.append("mv NanoAODskim_"+options.anatype+macro+options.era+"__WJetsToQQ_HT*.root rootfiles_tosum/" )


	    	sets = list(set(sets))
		print 
		print "------------"
		print "Summing Sets"
		print "------------"
	else:
		logging.error("Please Select --submit or --sum")
		sys.exit()



for s in commands :
    print "executing " + s
    subprocess.call( [s], shell=True )

