
from optparse import OptionParser
import subprocess,os,sys
import ROOT
#ROOT.ROOT.EnableImplicitMT()
parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
		  default	=	'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
		  dest		=	'set',
		  help		=	'data or ttbar')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
		  default	=	'2017',
		  dest		=	'era',
		  help		=	'2016,2017, or 2018')
parser.add_option('-j', '--job', metavar='F', type='int', action='store',
		  default	=	'1',
		  dest		=	'job',
		  help		=	'')

parser.add_option('-t', '--totaljobs', metavar='F', type='int', action='store',
		  default	=	'1',
		  dest		=	'totaljobs',
		  help		=	'')


parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
		  default	=	'Pho',
		  dest		=	'anatype',
		  help		=	'Pho or tHb')


parser.add_option('-f', '--folder', metavar='F', type='string', action='store',
		  default	=	'/eos/cms/store/user/knash',
		  dest		=	'folder',
		  help		=	'')
parser.add_option('-r', '--redir', metavar='F', type='string', action='store',
		  default	=	'eoscms.cern.ch',
		  dest		=	'redir',
		  help		=	'')
parser.add_option('-S', '--search', metavar='F', type='string', action='store',
		  default	=	'',
		  dest		=	'search',
		  help		=	'')
parser.add_option('-v', '--version', metavar='F', type='string', action='store',
		  default	=	'v8',
		  dest		=	'version',
		  help		=	'')
parser.add_option('--ttonly', metavar='F', action='store_true',
		  default=False,
		  dest='ttonly',
		  help='ttonly')
parser.add_option('--condor', metavar='F', action='store_true',
		  default=False,
		  dest='condor',
		  help='submit')
parser.add_option('--eventsplitting', metavar='F', action='store_true',
		  default=False,
		  dest='eventsplitting',
		  help='eventsplitting')
parser.add_option('--Ana', metavar='F', action='store_true',
		  default=False,
		  dest='Ana',
		  help='Analyzer')
parser.add_option('--Bkg', metavar='F', action='store_true',
		  default=False,
		  dest='Bkg',
		  help='Background')
parser.add_option('--prescale', metavar='F', action='store_true',
		  default=False,
		  dest='prescale',
		  help='prescale')
parser.add_option('--trigemu', metavar='F', action='store_true',
		  default=False,
		  dest='trigemu',
		  help='trigemu')

(options, args) = parser.parse_args()
#make an option
runttweight=True
di=""
if options.condor:
	di="tardir/"
	#subprocess.call( ["mv "+di+"PhysicsTools ./"], shell=True )
	#subprocess.call( ["cp -r PhysicsTools ./CMSSW_10_2_9/src"], shell=True )
	#os.chdir("CMSSW_10_2_9/src")
	#subprocess.call( ["scram b"], shell=True )
	#subprocess.call( ["scramv1 runtime -sh"], shell=True )
	#subprocess.call( ["cmsenv"], shell=True )
	#os.chdir("../../")
	#subprocess.call( ["ls ./"], shell=True )
	#subprocess.call( ["pwd"], shell=True )
import NanoAODskim_Functions
from NanoAODskim_Functions import *


print "Options Summary..."
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option])
	print str(opt) +': '+ str(value)
print "=================="
print ""
for curset in (options.set).split(","):
	jobarr = [options.job,options.totaljobs]
	if jobarr[0]>jobarr[1]:
		logging.error("Job Number Higher Than Total Jobs")
		sys.exit()
	prescale = options.prescale
	setname = curset
	setnametowrite=setname.split('/')[0]
	print "set name",setnametowrite
	settype=setfilter(setname)
	print "set type",settype
	NanoF = NanoAODskim_Functions(options.anatype,options.era,options.version,settype,options.condor)


	if not (settype=="JetHT"):
		constdict = NanoF.LoadConstants
		lumi = constdict["lumi"]

		nev_xsec = constdict["dataconst"][setnametowrite]
		posfac = constdict["posfac"][setnametowrite]
		posmmin = posfac
		nevweighted=nev_xsec[0]*posmmin

		setweight = lumi*nev_xsec[1]/float(nevweighted)

		print "nev=",nev_xsec[0],"posfac",posfac,"events",nevweighted
		print "Using MC weights..."
		print "\t... Using Constants: Lumi =",lumi,"; Xsec =",nev_xsec[1],"; Nevents =",float(nevweighted)

	else:
		print "Using data..."
		setweight = 1.0

	print "\t... Weight =",setweight

	print "Loading Files..."
	#options.search
	allfiles = NanoF.loadfiles("",options.folder,options.redir,setname,True)
	print "Totfiles",len(allfiles)
	files = []
	for cfile in xrange(len(allfiles)):

		if not (options.eventsplitting):
			#print "not eventsplitting!",cfile
			if not (cfile%jobarr[1]==(jobarr[0]-1)):
					#print "skip!",cfile
					continue
		files.append(allfiles[cfile])
		print files[-1]
	#files=["/eos/cms/store/user/knash/rdfskims/NanoAODskim_skimmer_"+options.era+"__"+setname+".root"]
	#random.shuffle(files)
	ntotfile = len(files)
	print "Loaded",ntotfile,"Files..."
	print "Booking Histograms..."

	labels = NanoF.labels
	ak8labs = NanoF.ak8labels
	ak4labs =NanoF.ak4labels
	candl = NanoF.candl
	probl = NanoF.probl
	njetinv=2
	trijet=False
	for lab in labels:
		if len(lab)==3:
			njetinv=3
			print "Trijet version"
	regionstr="regionmap_"
	if options.anatype=="tHb":
			regionstr+="TH"
	if options.anatype=="tZb":
			regionstr+="TZ"


	verbose=False
	if options.Ana:
		macro="Ana"
	elif options.Bkg:
		macro="Bkg"
	else:
		logging.error("Must Select a Analysis Type")
		sys.exit()
	doshifts=False
	if macro=="Bkg":
		#regions=["A","B","E","J","C","K","H","I","F","G","D","All"]
		regions=["A","B","E","J"]

		if options.anatype=="tHb" or options.anatype=="tZb":
			regions.append("M")
			regions.append("Z")

		#regions=["A","B","C","D","All"]
		hemispheres = ["0","1"]
		if (not NanoF.isdata):
			weightstoplot = ["genweightsf"]
		histos = NanoF.histosinit(labels,regions)
		#print histos
		for region in regions:
			jetreg =[]
			for ild in xrange(2):
				jetreg.append(region+"_"+str(ild))
			histos.update(NanoF.histosinit(labels,jetreg))
	FSregions = {}
	if macro=="Ana":
		doshifts=True
		if settype=="QCD":
			ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
		#elif options.era=="2016":
		#	print "2016 HACK!!!!!!!"
		#	ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
		else:
			ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__JetHT.root','open')
		ratehist = {}
		ratehist["D"]=ratefile.Get('rate')
		ratehist["G"]=ratefile.Get('Erate')
		ratehist["L"]=ratefile.Get('Jrate')
		ratehist["I"]=ratefile.Get('rate')



		regions=["C","K","H","F"]
		rateregions = ["D","L","I","G"]
		if options.anatype=="tHb" or options.anatype=="tZb":
			ratehist["O"]=ratefile.Get('Mrate')
			regions.append("N")
			rateregions.append("O")
		if options.anatype=="tHb":
			ratehist["FTR"]=ratefile.Get('rate')
			regions.append("FT")
			rateregions.append("FTR")
		FSregions=copy.copy(regions)
		anaregions=copy.copy(regions)
		ratehistos={}
		for ratetype in rateregions:
			regions.append(ratetype)
			ratehistos[ratetype] = []
		#for lab in labels:
		#	if len(lab)==1:
		#		regions.append("NM1"+lab)
		for rname in NanoF.LoadCuts:
			#print rname
			if rname.find("NM1")!=-1:
				#print "found"
				regions.append(rname)

		#print regions
		bkgweights=["","__err","_0","__err_0","_1","__err_1"]
		ratephist = ratefile.Get("ratep")
		histofills = copy.deepcopy(regions)
		#for bkgw in bkgweights[1:]:
		#	histofills.append("bkg__"+bkgw)
		histos = NanoF.histosinit(labels,histofills)

		if (not NanoF.isdata):
			weightstoplot = ["genweightsf"]
			#weightshistos = NanoF.weightshistosinit(weightstoplot,FSregions)

		#print weightshistos
		binstrs=[]
		#print histos


		#PUT IN A FUNCTION


		for ratetype in rateregions:
			ratestr = ""
			if ratetype=="G":
				ratestr = "E"
			if ratetype=="L":
				ratestr = "J"
			if ratetype=="O":
				ratestr = "M"
			for currate in bkgweights:

				exstr=""
				if currate!="":
					exstr = currate
					histos[ratetype+exstr]={}
					if currate.find("err")!=1:
						ratehistos[ratetype+exstr] = []

				for ybin in xrange(ratehist[ratetype].GetNbinsY()+1):

					if currate=="":
						ratehistos[ratetype].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)))
						nxbins = ratehistos[ratetype][-1].GetNbinsX()+1
					elif currate.find("err")==-1:
						ratehistos[ratetype+exstr].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)+"_"+currate))
						nxbins = ratehistos[ratetype+exstr][-1].GetNbinsX()+1
					else:
						nxbins = ratehistos[ratetype+exstr.replace("__err","")][ybin].GetNbinsX()+1
					#print nxbins,currate
					binstrs.append("bbin"+str(ybin))
					for lab in labels:
						#print "D"+exstr
						histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__mass__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__mass__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__mass__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,800, 0.,8000.)

						if lab in ak4labs:
							histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,350, 0.,3500.)
						else:
							histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,350, 400.,3900.)
							if len(lab)==1:
								histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__msoftdrop__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__msoftdrop__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__msoftdrop__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,240, 0.,480.)
						histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,60, -3.0,3.0)
			newhistos = NanoF.histosinit(labels,[ratetype+"_0",ratetype+"_1"])
			histos[ratetype+"_0"].update(newhistos[ratetype+"_0"])
			histos[ratetype+"_1"].update(newhistos[ratetype+"_1"])

		#for histo in histos:
		#	for  histo1 in histos[histo]:
		#		print histo1

		masshist = ratefile.Get("masshist")


	matchmatrix = []


	#print "Calculating Total Events..."
	#countstotal=0
	#for curfilename in files:
	#	curfile = TFile(curfilename,"open")
	#	countstotal+=(curfile.Get("Events")).GetEntries()
	#print float(countstotal)/float(300000),"jobs"
	#print "Processing",countstotal,"Events..."


	print "Start Looping..."
	counts = 0
	kill=False
	#timelogger = {"total":0.0,"files":0.0,"init":0.0,"processing":0.0}
	sttime=time.time()
	avemtemp = []
	ntrigtot=0
	ntrigfail=0
	cutflow = {}
	cutflow["pre"] = {}
	cutflow["pre"]["All"]=0.0
	cutflow["pre"]["twoak8"]=0.0
	cutflow["pre"]["highpt"]=0.0
	cutflow["pre"]["eta"]=0.0
	cutflow["pre"]["Ak8DR"]=0.0
	cutflow["pre"]["Ak8Drap"]=0.0
	cutflow["pre"]["muveto"]=0.0
	cutflow["pre"]["elveto"]=0.0
	minpt = 9999999.
	minptak4 = 9999999.
	minsdm = 9999999.
	for region in regions:
		minpt=min(minpt,(NanoF.LoadCuts)[region]["ptAK8"])
		if "B" in ak4labs:
			minptak4=min(minptak4,(NanoF.LoadCuts)[region]["pt__B"])
		#print "msoftdrop__"+ak8labs[0]
		#print (NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[0]]
		#print region,"msoftdrop__"+ak8labs[0],"msoftdrop__"+ak8labs[1]
		#print (NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[0]][0],(NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[1]][0]
		minsdm=min(minsdm,max((NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[0]][0],(NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[1]][0]))
		cutflow[region] = {}
		cutflow[region]["noprobl"]=0.0
		cutflow[region]["nocandlandprobl"]=0.0
		cutflow[region]["ak4tag"]=0.0
		cutflow[region]["ht"]=0.0
		cutflow[region]["trig"]=0.0
		cutflow[region]["Full"]=0.0

	print "min pt, softdrop mass for triggering",minpt,minsdm
	print "min pt ak4",minptak4

	#print histos
	errvals = ["mass","pt","eta"]


	prehisto = copy.deepcopy(histos)

	shiftnames = []
	shiftuncert=[""]
	errnames = []

	if (not NanoF.isdata) and (settype!="QCD"):
		errnames.append("trig")
		errnames.append("pu")
		if "H" in ak8labs:
			errnames.append("htag")
		if "Z" in ak8labs:
			errnames.append("wtag")
		if "T" in ak8labs:
			errnames.append("ttag")
		if "B" in ak4labs:
			errnames.append("btag")
		errnames.append("q2")
		if settype=="Signal":
			errnames.append("pdfweight")
		if settype=="TT" and runttweight:
			errnames.append("tptrw")
		if doshifts:
			shiftnames = ["jes","jer"]
			shiftuncert=["","jes__up","jes__down","jer__up","jer__down"]
		recalmc = NanoF.jmeCorrections().jetReCalibrator
		recalmcak4 = NanoF.jmeCorrectionsak4().jetReCalibrator
	weightshistos=[]
	if macro=="Ana" and (not NanoF.isdata):
		for errname in errnames:
			#print errname
			weightstoplot.append(errname+"sf")
			weightstoplot.append(errname+"up")
			weightstoplot.append(errname+"down")
		weightshistos = NanoF.weightshistosinit(weightstoplot,["C"])
	uphistos={}
	downhistos={}
	for errname in (errnames+shiftnames):
		uphistos[errname]={}
		downhistos[errname]={}
		for errval in errvals:
			for region in FSregions:
				uphistos[errname][region]={}
				downhistos[errname][region]={}
				for hn in prehisto[region]:
					if (hn.split("__")[0] in errvals) and (isinstance(prehisto[region][hn], TH1F)):
						#print hn.split("__")[1],len(hn.split("__")[1])
						if (hn.split("__")[0]!="mass") and (len(hn.split("__")[1])>1):
							continue
						#print [hn+"__"+errname+"__up"], [hn+"__"+errname+"__down"]
						copyhist = copy.copy(prehisto[region][hn])
						copyhist.SetName(hn+"__"+errname+"__up")
						uphistos[errname][region][hn+"__"+errname+"__up"]=copyhist
						copyhist = copy.copy(prehisto[region][hn])
						copyhist.SetName(hn+"__"+errname+"__down")
						downhistos[errname][region][hn+"__"+errname+"__down"]=copyhist

	#print histos
	if options.ttonly and options.anatype=="tHb":
		regions=["FT","FTR"]
		rateregions=["FTR"]
	#jeccorr =NanoF.jmeCorrections()
	#nak8jets=0
	resetweightdict={}
	for region in regions:
		resetweightdict[region]={}
		for errname in errnames:
			resetweightdict[region][errname]={"sf":1.0,"down":1.0,"up":1.0}
	resetweightdict[region]["setweight"]={"sf":1.0}
	if (not NanoF.isdata):
		resetweightdict[region]["genweight"]={"sf":1.0}
	if macro=="Ana":
		resetweightdict[region]["bkgweight"]={"sf":1.0}
	numf=-1


	for curfilename in files:
		numf+=1
		#filest = time.time()
		#print "Loading",curfilename.split('/')[-1]
		print curfilename
		#if curfilename=="root://eoscms.cern.ch:///store/group/phys_b2g/knash/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_NanoSlimNtuples2018mc_v8/190904_160953/0000/NanoAODSIMv5skim_176.root":
		#	skipem=False
		#if skipem:
		#	continue
		if kill:
			break

		if (options.trigemu) or (NanoF.isdata):
			runver = ""
			parsename =  curfilename.split("/")
			for pars in parsename:
				if pars.find("Run201")!=-1:
					runver=pars[0:8]
			NanoF.setruntrigs(runver)

		try:
			#curfile = TFile(curfilename,"open")
			curfile = TFile.Open(curfilename)
			curttree = curfile.Get("Events")
		except:
			logging.warning("ERROR OPENING FILE")
			continue

		#branchdir = NanoF.ttreeinit(curttree,runver)

		#if NanoF.isdata:
		#	jmecorr = NanoF.initcorr(curfilename)
		#endftime=time.time()
		#timelogger["files"]+=endftime-stftime
		nent = curttree.GetEntries()
		#print "Nentries",nent

		itertree = iter(curttree)
		if (options.eventsplitting):
			itertree = itertools.islice(itertree,(jobarr[0]-1),nent,jobarr[1])
		#for tt in itertree:
		avetime=0
		stevtime = time.time()
		for iev in xrange(nent):
			genpart,genweight,pdfweights,q2weights=None,None,None,None

			counts+=1


			try:
				ev=itertree.next()
			except:
				print "EV ERR!"
				continue
			#if counts<30000:
			#	continue


			#snapdir = copy.copy(branchdir)
			#print "start"
			#curttreeread.Next()
			#stetime=time.time()


			cutflow["pre"]["All"]+=1.
			if counts%10000==0:
				avetime=time.time()-stevtime
				tpev=0.0
				if iev>0:
					tpev=10000.*(avetime)/float(iev)
				print "\t...",counts,"events processed, ave time per proc event:",strf(tpev),"dmsec, Total time",strf(time.time()-sttime)
				if verbose:
					for lab in labels:
						if len(lab)==njetinv:
							for region in regions :
								print "\t\t...","Region",region
								print "name",region,"mass__"+lab+"__"+region
								print "\t\t\t...","Events",histos[region]["mass__"+lab+"__"+region].GetEntries()
								hinterr = array("d",[0])
								hintegral = histos[region]["mass__"+lab+"__"+region].IntegralAndError(0,-1,hinterr)
								print "\t\t\t...","Integral",hintegral,"+/-",hinterr[0]
								#print "\t\t\t...","Integral1",histos[region]["mass__"+lab+"__"+region].Integral(),"+/-",hinterr[0]
								#print "\t\t\t...","Mean",histos[region]["mass__"+lab+"__"+region].GetMean()
							#if histos["A"]["mass__"+lab+"__A"].Integral()>0  and histos["D"]["mass__"+lab+"__D"].Integral()>0:
					#			print "Cevents",histos["C"]["mass__"+lab+"__C"].GetEntries()
					#			print "Bevents",histos["B"]["mass__"+lab+"__B"].GetEntries()

							#	print "Crate",histos["C"]["mass__"+lab+"__C"].Integral()/histos["D"]["mass__"+lab+"__D"].Integral()
							#	print "Brate",histos["B"]["mass__"+lab+"__B"].Integral()/histos["A"]["mass__"+lab+"__A"].Integral()


					#			print "Cmass",histos["C"]["mass__"+lab+"__C"].GetMean()/histos["D"]["mass__"+lab+"__D"].GetMean()
					#			print "Bmass",histos["B"]["mass__"+lab+"__B"].GetMean()/histos["A"]["mass__"+lab+"__A"].GetMean()


			#print counts,counts%jobarr[1],jobarr[0]
			#if counts>10000:
			#	kill=True
			#	break


			#print branchdir["event"]
			#print branchdir["event"]
			#print snapdir
			#print "\t1.11"
			#print "pre",nak8jets

			reionmap = getattr(ev,regionstr)
			#print reionmap
			passedregs= NanoF.regionmap(reionmap)
			regstorun = []
			for pp in passedregs:
				if pp in regions:
					regstorun.append(pp)
			#print regstorun,passedregs
			if regstorun==[]:
				continue
			#nak8jets = getattr(ev, "nCustomAK8Puppi")
			#if nak8jets<2:
			#	continue
			cutflow["pre"]["twoak8"]+=1.
			#minptak8 = getattr(ev, "CustomAK8Puppi_pt")[1]
			#~30GeV buffer zone
			#if minptak8<(minpt-30.0):
			#	continue

			cutflow["pre"]["highpt"]+=1.


			#print ptrigs
			#print curtrigs

			
			#trigvals = {}
			#if (options.trigemu) or (NanoF.isdata):
			#	ptrigs = copy.copy(NanoF.ptrigs)
			#	curtrigs = copy.copy(NanoF.strigs+NanoF.etrigs)
			#	if prescale:
			#		prigvals = {}
			#		for tt in ptrigs:
			#			try:
			#				prigvals[tt]=getattr(ev, tt)
			#			except:
			#				pass
			#		if not (NanoF.TriggerPass(prigvals,True)):
			#			continue
			#	else:
			#		for tt in curtrigs:
			#			try:
			#				trigvals[tt]=getattr(ev, tt)
			#			except:
						#print "no",tt
			#				pass
						#print tt,trigvals[tt]
			#		if not (NanoF.TriggerPass(trigvals)):
			#			continue
			
			#print cutflow["pre"]["elveto"]/cutflow["pre"]["muveto"]
			#ak8jets=Collection(ev,"CustomAK8Puppi" )
			ak8jetsFF=NanoF.expandgeneric(ev,"CustomAK8Puppi",maxlen=3 )
			ak4jetsFF=NanoF.expandgeneric(ev,"Jet" )
			if not NanoF.isdata:
				CustomGenJetAK8FF=NanoF.expandgeneric(ev,"CustomGenJetAK8",maxlen=-1)
				CustomGenJetAK4FF=NanoF.expandgeneric(ev,"GenJet",maxlen=-1)
				nTrueInt = getattr(ev, "Pileup_nTrueInt")
			rho = getattr(ev, "fixedGridRhoFastjetAll")
			eventnumber = getattr(ev, "event")
			NanoF.rnd.SetSeed(eventnumber)
			random.seed(eventnumber)

			for shift in shiftuncert:
				ak8jets=copy.deepcopy(ak8jetsFF)
				ak4jets=copy.deepcopy(ak4jetsFF)
				#print shift
				shstr=""
				shtype=""
				if len(shift.split("__"))>1:
					shstr=shift.split("__")[1]
				if len(shift.split("__"))>1:
					shtype=shift.split("__")[0]
				histostoplot = histos
				if shstr=="up":
					histostoplot = uphistos[shtype]
					delta=1
				if shstr=="down":
					histostoplot = downhistos[shtype]
					delta=-1
				histostofill = histos
				ak8corrs=[]
				#print "ev"

				if (shtype=="jes") and (not NanoF.isdata):
					#print "delta",delta
					#print "AK8 Loop"
					#print "pre"
					for ak8j in ak8jets:
						#print "newjet"
						#print ak8j.pt
						(jet_pt, jet_mass) = recalmc.correct(ak8j,rho,delta=delta)
						ak8j.pt = jet_pt
						ak8j.mass = jet_mass
						ak8j.setp4()

					for ak4j in ak4jets:
						#print "newjet"
						#print ak4j.pt
						(jet_pt, jet_mass) = recalmcak4.correct(ak4j,rho,delta=delta)
						ak4j.pt = jet_pt
						ak4j.mass = jet_mass
						ak4j.setp4()

				if not NanoF.isdata:
					CustomGenJetAK8=copy.deepcopy(CustomGenJetAK8FF)
					CustomGenJetAK4=copy.deepcopy(CustomGenJetAK4FF)

					jind=0
					if (shtype=="jer") and (shstr=="up"):
						jind=2
					if (shtype=="jer") and (shstr=="down"):
						jind=1
					#print shift,ak8jets[0].pt,ak4jets[0].pt

					NanoF.jersmear(ak8jets, CustomGenJetAK8,rho,jind,jtype="ak8")
					NanoF.jersmear(ak4jets, CustomGenJetAK4,rho,jind,jtype="ak4")

					#print shift,ak8jets[0].pt,ak4jets[0].pt



				#print shift,ak8jets[0].pt
				if ak8jets[1].pt<minpt:
					continue
				#print ak8jets[1].pt


				if abs(ak8jets[0].eta)>2.4 or abs(ak8jets[1].eta)>2.4:
					continue

				cutflow["pre"]["eta"]+=1.



				#print curdictval["CustomAK8Puppi"]
				#continue
				#endetime=time.time()
				#timelogger["init"]+=endetime-stetime
				#stptime=time.time()


				htval = 0
				for ak4jet in ak4jets:
					if ak4jet.p4.Perp()<30.0:
						continue
					htval += ak4jet.p4.Perp()


				#print "pass1"
				#histos["TRIG"]["ht__pretrig__All"].Fill(htval)
				#histos["TRIG"]["ht__msoftdrop__pretrig__All"].Fill(htval,max(ak8jets[0].msoftdrop,ak8jets[1].msoftdrop))
				#for hh in NanoF.trigstopass:
				#	histos["TRIG"]["ht__pretrig__"+hh].Fill(htval)
					#print trigvals,trigvals[hh]
				#	if trigvals[hh]:
				#		histos["TRIG"]["ht__posttrig__"+hh].Fill(htval)

				#print "pass2"
				#histos["TRIG"]["ht__posttrig__All"].Fill(htval)
				#histos["TRIG"]["ht__msoftdrop__posttrig__All"].Fill(htval,max(ak8jets[0].msoftdrop,ak8jets[1].msoftdrop))


				#print

				#print ak8jets[0].p4.DeltaR(ak8jets[1].p4)

				if ak8jets[0].p4.DeltaR(ak8jets[1].p4)<1.6:
					continue

				cutflow["pre"]["Ak8DR"]+=1.
				if njetinv==2:
					if abs(ak8jets[0].p4.Rapidity()-ak8jets[1].p4.Rapidity())>1.8:
						continue
				cutflow["pre"]["Ak8Drap"]+=1.


				nfillsev=0
				weightdict={}

				for region in regstorun:
					if (shift!="") and not (region in FSregions):
						continue

					weightdict[region] = resetweightdict[region]
					weightdict[region]["setweight"] = {"sf":setweight}
					ptcut=(NanoF.LoadCuts)[region]["ptAK8"]

					tags = {}
					for ak8lab in ak8labs:
						tags[ak8lab]=[]
					maxsdmass=0.0
					ijet=0
					for ak8jet in ak8jets:
						maxsdmass=max(maxsdmass,ak8jet.msoftdrop)
						if ijet>njetinv-1:
							break
						#print ijet,njetinv-1
						if ak8jet.p4.Perp()<ptcut or abs(ak8jet.p4.Eta())>2.4 :
							break

						ak8jet.index=ijet
						for tag in tags:
							if NanoF.tagjet(ak8jet,tag,region.split("__")[0]):
								#print tag
								tags[tag].append(ijet)

						ijet+=1

					if len(tags[probl])==0:
						continue

					cutflow[region]["noprobl"]+=1.

					#if region=="default" and len(tags[probl])>1 and len(tags[candl])>0:
					#	logging.error("Possible Multiple Entries")
					#print
					nfills=0





					#print "ST", settype,weightdict
					for i in xrange(len(tags[probl])):
						cands = {}
						for lab in labels:
							cands[lab]=None
						iprobe = tags[probl][i]
						if njetinv==2:
							icandidate = 1-tags[probl][i]

						if njetinv==3:

							tempcands = copy.deepcopy(tags[candl])
							#print tempcands	, tags[probl],tags[probl][i]
							if tags[probl][i] in tempcands:
								tempcands.remove(tags[probl][i])
							#print tempcands
							if len(tempcands)>0:
								#random.shuffle(tempcands)
								#print tempcands
								icandidate = tempcands[0]
								#print icandidate
							else:
								continue

						if len(tags[candl])>0:
							#if (region=="FT"):
							#	print "Dubs ntry",i,tags[candl],tags[probl],icandidate,iprobe

							if icandidate in tags[candl]:
								cands[candl]= ak8jets[icandidate]
						#else:
						#	if (region=="FT"):
						#		print "Sings",tags[candl]
						cands[probl]=ak8jets[iprobe]

						iorder=0
						if icandidate>iprobe:
							iorder=1
						#print "ic",icandidate,iprobe,"io",iorder
						if cands[probl]==None or cands[candl]==None:
							continue
						if cands[probl].p4.DeltaR(cands[candl].p4)<1.6:
							continue
						#print icandidate,iprobe
						cutflow[region]["nocandlandprobl"]+=1.
						if macro=="Ana":
							if (region in rateregions) and (options.anatype=="tHb" or options.anatype=="tZb"):
								fakemass = masshist.GetRandom()
								cands[candl].p4.SetPtEtaPhiM(cands[candl].pt,cands[candl].eta,cands[candl].phi,fakemass)
								cands[candl].mass = fakemass

						njets = 0
						htvalrem = 0
						njetsrem = 0
						for ak4jet in ak4jets:
							if ak4jet.p4.Perp()<30.0:
								continue
							if njets==0:
								fullevent=ak4jet.p4.Perp()
							else:
								fullevent+=ak4jet.p4.Perp()
							njets += 1
							if (cands[candl].p4.DeltaR(ak4jet.p4)>1.2 and cands[probl].p4.DeltaR(ak4jet.p4)>1.2):
								htvalrem += ak4jet.p4.Perp()
								njetsrem += 1

						foundall=True
						#print
						#print "pret"
						for lab in labels:
							if len(lab)==1 and not (lab in [probl,candl]):

								if lab in ak4labs:
									ptcutAK4=(NanoF.LoadCuts)[region]["pt__"+lab]
									#print ptcutAK4
									iak4jet=0
									for ak4jet in ak4jets:
										if ak4jet.p4.Perp()>ptcutAK4 and abs(ak4jet.p4.Eta())<2.4:
											if ak4jet.p4.DeltaR(cands[probl].p4)>1.2 and ak4jet.p4.DeltaR(cands[candl].p4)>1.2:
												if NanoF.tagjet(ak4jet,lab,region.split("__")[0]):
													ak4jet.index=iak4jet
													cands[lab]=ak4jet
													break
										iak4jet+=1
								#print lab,cands[lab]
								if cands[lab]==None:
									foundall=False


						if not foundall:
							continue
						cutflow[region]["ak4tag"]+=1.
						for lab in labels:
							if len(lab)>1:
								lvtag = True
								for ll in lab:
									if cands[ll]==None:
										lvtag=False

								if lvtag:
									candarr=[]
									for ll in lab:
										candarr.append(cands[ll])
									cands[lab] = invobj(candarr)
									cands[lab].njets=njets
									cands[lab].htval=htval
									cands[lab].njetsrem=njetsrem
									cands[lab].htvalrem=htvalrem

						bkgweight=1.0


						#if options.anatype=="Pho":
						#	phos = NanoF.physobjinit(curdictval["Photon"],2)
						#	listtoneg = [probl]
						#	if len(phos)>0:
						#		cands[candl]["Piso"] = phos[0]['pfRelIso03_all']
						#		cands[candl]["PelectronVeto"] = phos[0]['electronVeto']
						#		cands[candl]["PpixelSeed"] = phos[0]['pixelSeed']
						#		cands[candl]["PmvaID_WP80"] = phos[0]['mvaID_WP80']
						#		cands[candl]["PmvaID_WP90"] = phos[0]['mvaID_WP90']


						#		if 0.0<=cands[candl]["Piso"]<0.04:
						#			continue

								#if region=='C':
								#	print
								#	print cands[candl]["Piso"]
								#	print cands[candl]["PelectronVeto"]
								#	print cands[candl]["PpixelSeed"]
								#	print cands[candl]["PmvaID_WP80"]
								#	print cands[candl]["PmvaID_WP90"]


						#	else:
						#		listtoneg.append(candl)
						#	for cc in listtoneg:
						#		for dd in ["Piso","PelectronVeto","PpixelSeed","PmvaID_WP80","PmvaID_WP90"]:
						#			cands[cc][dd]=-1.

						if htval<1100:
							continue

						if (not NanoF.isdata):
							if genweight==None:
								genweight = float(getattr(ev, "genWeight"))
							weightdict[region]["genweight"] = {"sf":genweight}
							if settype=="TT" and runttweight:
								if genpart==None:
									genpart = NanoF.expandgeneric(ev,"GenPart",20,ptcut=0.0)
								weightdict[region]["tptrw"] = NanoF.tptrw(genpart)
							if settype=="Signal":
								if q2weights==None:
									q2weights=[]

									for iq2 in range(0,6):
										q2weights.append(float(getattr(ev, "LHEScaleWeight")[iq2]))

								weightdict[region]["q2"] = NanoF.q2weight(q2weights)
								#print weightdict[region]["q2"]
								if pdfweights==None:
									pdfweights=[]

									for ipdf in range(2,102):
										pdfweights.append(float(getattr(ev, "LHEPdfWeight")[ipdf]))
								weightdict[region]["pdfweight"] = NanoF.pdfweight(pdfweights)

							if (not options.trigemu):
								weightdict[region]["trig"] = NanoF.triggerweight(htval,maxsdmass)
							weightdict[region]["pu"] = NanoF.puweight(nTrueInt)
							if "B" in ak4labs:
								#print eventnumber
								if not (region in ["M","N","O","Z","NM1BbtagDeepFlavB"]):
									#print "runb",shift,region,cands["B"].pt
									weightdict[region]["btag"] = NanoF.btagsf(cands["B"],"T")
									#print weightdict[region]["btag"]
								else:
									#print "nob",region
									weightdict[region]["btag"] = NanoF.btagsf(cands["B"],"L")
									#print weightdict[region]["btag"]
							if "H" in ak8labs:

								if (region in ["C","D","K","L","N","O","NM1Tmsoftdrop","NM1TiMDtop","NM1Hmsoftdrop","NM1BbtagDeepFlavB"]):
									weightdict[region]["htag"] = NanoF.htagsf(cands["H"],"T",settype)
									#print "ptag",weightdict[region]["htag"]
								else:
									weightdict[region]["htag"] = NanoF.htagsf(cands["H"],"L",settype)
							if "Z" in ak8labs:
								if (region in ["C","D","K","L","N","O","NM1Tmsoftdrop","NM1TiMDtop","NM1Zmsoftdrop","NM1BbtagDeepFlavB"]):
									weightdict[region]["wtag"] = NanoF.wtagsf(cands["Z"],"T")
								else:
									weightdict[region]["wtag"] = NanoF.wtagsf(cands["Z"],"L")

							if "T" in ak8labs:
								if (region in ["B","C","H","M","N","FT","NM1Tmsoftdrop","NM1HbtagHbb","NM1Hmsoftdrop","NM1BbtagDeepFlavB"]):
									weightdict[region]["ttag"] = NanoF.toptagsf(cands["T"],"T")
									#print "ptag",weightdict[region]["ttag"]
								else:
									weightdict[region]["ttag"] = NanoF.toptagsf(cands["T"],"L")
								if (region in ["FT","FTR"]):
									#Fake H region
									tempttag = NanoF.toptagsf(cands["H"],"T")
									#fully correlated errors
									weightdict[region]["ttag"]["sf"]*=tempttag["sf"]
									weightdict[region]["ttag"]["up"]*=tempttag["up"]
									weightdict[region]["ttag"]["down"]*=tempttag["down"]






						cutflow[region]["ht"]+=1.
						ntrigtot+=1


						cutflow[region]["trig"]+=1.
						plotdict = NanoF.candtodict(cands)

						if macro=="Ana" and (region in rateregions):

							remerr = 0.
							remcont = 0.
							for bkgw in bkgweights:
								if len(bkgw)>0:
									if bkgw[-1] in ["0","1"]:
										tagindex = int(bkgw[-1])
										#print bkgw,tagindex,icandidate
										if iorder!=tagindex:
											continue


								etabin=ratehist[region].GetYaxis().FindBin(abs(cands[candl].eta))
								for binstr in binstrs:
									plotdict[candl][binstr]=None
								curratehisto = ratehistos[region+bkgw.replace("__err","")]
								if etabin<len(curratehisto):
									ptbin=curratehisto[etabin].FindBin(cands[candl].pt)
									if bkgw.find('err')!=-1:
										if bkgw== "__err":
											remerr=curratehisto[etabin].GetBinError(ptbin)
										bkgweight = curratehisto[etabin].GetBinError(ptbin)

									else:
										if bkgw== "":
											remcont=curratehisto[etabin].GetBinContent(ptbin)
										bkgweight = curratehisto[etabin].GetBinContent(ptbin)

									plotdict[candl]["bbin"+str(etabin)]=ptbin
								weightdict[region]["bkgweight"]={"sf":bkgweight}
								bkgstr=region

								if bkgw!="":
									bkgstr += bkgw
								hweight=1.0
								for ww in weightdict[region]:
									hweight*=weightdict[region][ww]["sf"]

								NanoF.histosfill(histostoplot,plotdict,bkgstr,hweight)
								if (not NanoF.isdata):
									NanoF.weightshistosfill(weightshistos,weightdict,region)
						else:
							#Filling jetnum histos
							if macro=="Bkg":
								hweight=1.0
								for ww in weightdict[region]:
									hweight*=weightdict[region][ww]["sf"]
								NanoF.histosfill(histostoplot,plotdict,region+"_"+str(iorder),hweight)
							if (macro=="Ana" and region!="FT" and (region in anaregions) and nfills!=0):
								break
							cutflow[region]["Full"]+=1.



							hweight=1.0
							for ww in weightdict[region]:
									hweight*=weightdict[region][ww]["sf"]

							if (settype=="JetHT"):
								if hweight!=1.0:
									logging.error("DATA with non-unity weight!!!")

							NanoF.histosfill(histostoplot,plotdict,region,hweight)
							if (not NanoF.isdata):
								NanoF.weightshistosfill(weightshistos,weightdict,region)

							if (shift=="") and (region in FSregions):
								for normerr in errnames:
									for errval in ["down","up"]:
										hweight=1.0

										for ww in weightdict[region]:

											if (normerr==ww) and (errval in weightdict[region][ww]):
												hweight*=weightdict[region][ww][errval]
											else:
												hweight*=weightdict[region][ww]["sf"]
										if errval=="up":
											NanoF.histosfill(uphistos[normerr],plotdict,region,hweight)
										if errval=="down":
											NanoF.histosfill(downhistos[normerr],plotdict,region,hweight)

							nfills+=1
							nfillsev+=1

	print "Finished Looping..."
	jobstr=""
	if jobarr[1]!=1:
		jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
	output = ROOT.TFile("NanoAODskim_"+options.anatype+macro+options.era+"__"+setnametowrite+jobstr+".root","recreate")
	output.cd()
	allhiststowrite=[histos]
	for errname in (errnames+shiftnames):
		allhiststowrite.append(uphistos[errname])
		allhiststowrite.append(downhistos[errname])
	if (not NanoF.isdata):
		allhiststowrite.append(weightshistos)
	for histoset in allhiststowrite:
		for histo in histoset:
			for histo1 in histoset[histo]:
				#print "Writing",histo,histo1
				histoset[histo][histo1].Write()
	print "Writing rootfile from "+curset+"..."
	output.Write()
	output.Close()
	print "Written.."
print "Completed..."


