
from optparse import OptionParser
import subprocess,os,sys
import ROOT
#ROOT.ROOT.EnableImplicitMT()
parser = OptionParser()
ROOT.TH1.AddDirectory(False);

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
parser.add_option('--skipskim', metavar='F', action='store_true',
		  default=False,
		  dest='skipskim',
		  help='skipskim')
parser.add_option('--hemtest', metavar='F', action='store_true',
		  default=False,
		  dest='hemtest',
		  help='hemtest')
parser.add_option('--prefire', metavar='F', action='store_true',
		  default=False,
		  dest='prefire',
		  help='prefire')

(options, args) = parser.parse_args()

#Hardcode pt reweight
runttweight=True

#All Files in tarred directory 
di=""
if options.condor:
	di="tardir/"

#For specific objects
import NanoAODskim_Functions
from NanoAODskim_Functions import *

#Tells it to only save one skim
regionstr=options.anatype
if options.anatype=="tHb":
		vpairs=["TH","BH"]
		regionstr="TH"
if options.anatype=="tZb":
		vpairs=["TZ","BZ"]
		regionstr="TZ"


print "Options Summary..."
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option])
	print str(opt) +': '+ str(value)
print "=================="
print ""

#For python inf -> text
infinity=99999999999.

for curset in (options.set).split(","):
	iovr,inover,ibr,itot=0,0,0,0
	jobarr = [options.job,options.totaljobs]
	if jobarr[0]>jobarr[1]:
		logging.error("Job Number Higher Than Total Jobs")
		sys.exit()

	prescale = options.prescale
	setname = curset

	hemstr=""
	if options.hemtest:
		hemstr="hemtst"
	prefstr=""
	if options.prefire:
		prefstr="prefire"
	setnametowrite=setname.split('/')[0]
	print "set name",setnametowrite
	settype=SetFilter(setname)
	print "set type",settype
	vstr= (options.version).split(",")
	NanoF = NanoAODskim_Functions(options.anatype,options.era,vstr,settype,options.condor)

	if not (settype=="JetHT"):
		constdict = NanoF.LoadConstants
		#Lumi, Nevents
		lumi = constdict["lumi"]
		nev_xsec = constdict["dataconst"][setnametowrite]

		#Average of (+/-) event weights 
		posfac = constdict["posfac"][setnametowrite]
		posmmin = posfac

		nevweighted=float(nev_xsec[0])*posmmin

		setweight = lumi*nev_xsec[1]/float(nevweighted)

		print "Nevents=",nev_xsec[0],"Posfac=",posfac,"Neventsweighted=",nevweighted
		print "Using MC weights..."
		print "\t... Using Constants: Lumi =",lumi,"; Xsec =",nev_xsec[1],"; Nevents =",float(nevweighted)

	else:
		print "Using data..."
		setweight = 1.0

	print "\t... Weight =",setweight

	if curset=="JetHT":
		setnametowrite+="__"+options.search
	#Objects to plot
	labels = NanoF.labels
	ak8labs = NanoF.ak8labels
	ak4labs =NanoF.ak4labels

	#Background estimation roles
	candl = NanoF.candl
	probl = NanoF.probl

	#Number of jets for inv mass (2 or 3 currently)
	njetinv=2
	trijet=False
	for lab in labels:
		if len(lab)==3:
			njetinv=3
			print "Trijet version"

	#Should be option
	verbose=False

	#Mode. Currently create transfer function or run analysis
	if options.Ana:
		macro="Ana"
	elif options.Bkg:
		macro="Bkg"
	else:
		logging.error("Must Select a Analysis Type")
		sys.exit()

	FSregions = {}

	#Do systematic shifts
	histos = {}
	histos["all"] = {} 


	if options.anatype=="tHb":

		histos["all"]["pt__H__all"] = TH1F("pt__H__all",	"pt__H__all",		200, 0.,2000. )
		histos["all"]["pt__t__all"] = TH1F("pt__t__all",	"pt__t__all",		200, 0.,2000. )
		histos["all"]["pt__b__all"] = TH1F("pt__b__all",	"pt__b__all",		200, 0.,2000. )
		histos["all"]["eta__H__all"] = TH1F("eta__H__all",	"eta__H__all",		20, 0.,2.4 )
		histos["all"]["eta__t__all"] = TH1F("eta__t__all",	"eta__t__all",		20, 0.,2.4 )
		histos["all"]["eta__b__all"] = TH1F("eta__b__all",	"eta__b__all",		20, 0.,2.4 )
		histos["all"]["DR__bt__all"] = TH1F("DR__bt__all",	"DR__bt__all",		20, 0.,4. )
		histos["all"]["DR__Ht__all"] = TH1F("DR__Ht__all",	"DR__Ht__all",		20, 0.,4. )
		histos["all"]["DR__Hb__all"] = TH1F("DR__Hb__all",	"DR__Hb__all",		20, 0.,4. )

	if options.anatype=="tZb":

		histos["all"]["pt__Z__all"] = TH1F("pt__Z__all",	"pt__Z__all",		200, 0.,2000. )
		histos["all"]["pt__t__all"] = TH1F("pt__t__all",	"pt__t__all",		200, 0.,2000. )
		histos["all"]["pt__b__all"] = TH1F("pt__b__all",	"pt__b__all",		200, 0.,2000. )
		histos["all"]["eta__Z__all"] = TH1F("eta__Z__all",	"eta__Z__all",		20, 0.,2.4 )
		histos["all"]["eta__t__all"] = TH1F("eta__t__all",	"eta__t__all",		20, 0.,2.4 )
		histos["all"]["eta__b__all"] = TH1F("eta__b__all",	"eta__b__all",		20, 0.,2.4 )
		histos["all"]["DR__bt__all"] = TH1F("DR__bt__all",	"DR__bt__all",		20, 0.,4. )
		histos["all"]["DR__Zt__all"] = TH1F("DR__Zt__all",	"DR__Zt__all",		20, 0.,4. )
		histos["all"]["DR__Zb__all"] = TH1F("DR__Zb__all",	"DR__Zb__all",		20, 0.,4. )

	print "Start Looping..."
	counts = 0

	sttime=time.time()


	#Compute minimums for skimming
	minpt = 9999999.
	minptak4 = 9999999.
	minsdm = 9999999.



	print "min pt, softdrop mass for triggering",minpt,minsdm
	print "min pt ak4",minptak4
	print "PRINTPRINT"
	print "1"
	errvals = ["mass","pt","eta","msoftdropdef"]


	shiftnames = []
	shiftuncert=[""]
	errnames = []
	if (not NanoF.isdata) and (settype!="QCD"):
		errnames.append("trig")
		errnames.append("pu")
		if "H" in ak8labs:
			errnames.append("htag")
			errnames.append("hmistag")
		if "Z" in ak8labs:
			errnames.append("wtag")
			errnames.append("extrap")
		if "T" in ak8labs:
			errnames.append("ttag")
		if "B" in ak4labs:
			errnames.append("btag")
			errnames.append("bmistag")
		errnames.append("q2")
		if settype=="Signal":
			errnames.append("pdfweight")
		if settype=="TT" and runttweight:
			errnames.append("tptrw")
		if options.prefire:
			errnames.append("prefire")

	#Select up and down histograms to compute
	uphistos={}
	downhistos={}
	prehisto = copy.deepcopy(histos)

	print "Loading Files..."
	#Return all sorted files 
	allfiles = NanoF.LoadFiles(setname,options.folder,options.redir,options.search)
	isdata=NanoF.isdata
	print "5"

	#Do job parsing (needs to be identical file lists every time)
	files = []
	for cfile in xrange(len(allfiles)):
		if not (options.eventsplitting):
			if not (cfile%jobarr[1]==(jobarr[0]-1)):
					continue
		files.append(allfiles[cfile])
	print "Total files:",len(allfiles),", Files for current job:",len(files)
	ntotfile = len(files)
	
	#Split data into file sets (ie RunX)
	filesets=[]
	if (NanoF.isdata):
		ladstr=""
		curdstr=""
	 	for ff in files:
	
			#Dir parse			
			direcs = ff.split("/")
			for direc in direcs:
				#Run name found			
				if direc.find("Run201")!=-1:
					curdstr=direc
			#New Run, new set (why sorting is important)		
			if ladstr!=curdstr:
				filesets.append([])
			filesets[-1].append(ff)
			ladstr=curdstr
	else:
	 	filesets=[files]
	totnev=0
	globalb=0
	globalbsub=0
	rdffiles=[]
	for fset in filesets:

		cfiles =ROOT.vector('string')()
		for cfile in fset:
			cfiles.push_back(cfile)
	
		#Start RDF
		df= ROOT.ROOT.RDataFrame("Events",cfiles)

		#Muon/Electron rdf vetos 
		mucut = 	'''
				for(uint nmu=0;nmu<nMuon;nmu++)	{
					if (((Muon_pt[nmu]>100.0)&&(Muon_tightId[nmu])))return false;
								}
				return true;
				'''
		elcut = 	'''
				for(uint nel=0;nel<nElectron;nel++)	{
					if ((Electron_pt[nel]>100.0)&&((Electron_mvaFall17V2Iso_WP90[nel]>0) || (Electron_mvaFall17V2noIso_WP90[nel]>0))) return false;
									}
				return true;
				'''

		#No MC trigger emulation
		NanoF.SetRunTrigs("NONE")
		trigcut=""
		runver = ""

		#Not sure if the trigemu option still works
		if (options.trigemu) or (NanoF.isdata):
				#Run dependent 
				parsename =  fset[0].split("/")
				for pars in parsename:
					if pars.find("Run201")!=-1:
						runver=pars[0:8]
				NanoF.SetRunTrigs(runver)
		alltr = NanoF.strigs+NanoF.etrigs
		for ctr in alltr:
			trigcut+="("+ctr+">0)"
			if ctr!= alltr[-1]:
				trigcut+="||"

		#Allow 30GeV JEC leeway (hacky)
		ak8ptval=str(minpt-30.0)
		presel =[
				mucut,
				elcut
			]
		if (options.trigemu) or (NanoF.isdata):
			presel.append(trigcut)

		print "start presel"
		filtarr = [df]
		df1  = df.Filter(presel[0])
		for sel in presel:
			filtarr.append(filtarr[-1].Filter(sel))
		print "finish presel"

		print "start tagging"

		#Add tau21 to the ntuple (3 leading AK8s)	
		tau21thing=	'''
					std::vector<float> CustomAK8Puppi_tau21{-1,-1,-1};
					for(uint nj=0;nj<3;nj++)	{
						if(nj<nCustomAK8Puppi)	{
							if ((CustomAK8Puppi_pt[nj]>'''+ak8ptval+''')&&(CustomAK8Puppi_tau1[nj]>0.0))CustomAK8Puppi_tau21[nj]=CustomAK8Puppi_tau2[nj]/CustomAK8Puppi_tau1[nj];
							else CustomAK8Puppi_tau21[nj]=0;
									}
									}
					return CustomAK8Puppi_tau21;
				'''
		filtarr[-1]=filtarr[-1].Define("CustomAK8Puppi_tau21",tau21thing)

		#default corr softdrop
		filtarr[-1]=filtarr[-1].Define("CustomAK8Puppi_msoftdropdef","CustomAK8Puppi_msoftdrop")

		ttags = {}
		for ak8lab in NanoF.ak8labels:
			ttags[ak8lab]=[]
		btoappend = []
		nregions=0

		regionmstr=""
		written=[]
		regions=["C"]
		for region in regions:			
				for tag in ttags:
					if [tag,region] in written:
						continue
					written.append([tag,region])
					cutstr=""
					for cut in (NanoF.LoadCuts)[region]:
						if cut.split("__")[-1]==tag and cut.split("__")[0]!="ptAK8":
							if cutstr=="":
								cutstr+="&&"
							LB=str((NanoF.LoadCuts)[region][cut][0])
							if LB=="inf":
								LB=str(infinity)
							UB=str((NanoF.LoadCuts)[region][cut][1])
							if UB=="inf":
								UB=str(infinity)
							if(cut.split("__")[0])=="msoftdrop":
								LB=str(NanoF.masssmearlims[0]*float(LB))
								UB=str(NanoF.masssmearlims[1]*float(UB))
							cutstr+="("+LB+"<CustomAK8Puppi_"+cut.split("__")[0]+"[nj])"
							cutstr+="&&"
							cutstr+="(CustomAK8Puppi_"+cut.split("__")[0]+"[nj]<="+UB+")"
							cutstr+="&&"

					cutstr = cutstr[:-2]

					varn = region+"__"+tag+"__tag"
					ttags[tag]=	'''
							std::vector<int> '''+varn+'''{-1,-1,-1};
							for(uint nj=0;nj<3;nj++)	{
								if(nj<nCustomAK8Puppi)	{
									if ((CustomAK8Puppi_pt[nj]>'''+ak8ptval+''')'''+cutstr+''')'''+varn+'''[nj]=1;
									else '''+varn+'''[nj]=0;
											}
											}
							return '''+varn+''';
							'''
					filtarr[-1]=filtarr[-1].Define("CustomAK8Puppi_"+varn,ttags[tag])
					btoappend.append("CustomAK8Puppi_"+varn)

				maxstrs={}
				for tag in ttags:
					varn = region+"__"+tag+"__tag"
					maxstrs[tag]="int(*std::max_element(std::begin(CustomAK8Puppi_"+varn+"),std::end(CustomAK8Puppi_"+varn+")))==1"
				#make sure all objects have at least one tag
				nregions=regions.index(region)
				maxch = "if (("+maxstrs[NanoF.ak8labels[0]]+")&&("+maxstrs[NanoF.ak8labels[1]]+"))return 1<<"+str(nregions)+";else return 0;"
				regch = regionstr+"region_"+region
				filtarr[-1]=filtarr[-1].Define(regch,maxch)
				regionmstr+=regionstr+"region_"+region+"+"
				

		regionmstr=regionmstr[:-1]
		#Create bit encoded regionmap
		filtarr[-1]=filtarr[-1].Define("regionmap_"+regionstr,regionmstr)
		#filtarr.append(filtarr[-1].Filter("(regionmap_"+regionstr+">0)"))

		btoappend+=["regionmap_"+regionstr]
		branchesrdf =ROOT.vector('string')()

		branchestokeeprdf=[
		"nCustomAK8Puppi",
		"CustomAK8Puppi_pt",
		"CustomAK8Puppi_eta",
		"CustomAK8Puppi_phi",
		"CustomAK8Puppi_mass",
		"CustomAK8Puppi_jetId",
		"CustomAK8Puppi_iMDPho",
		"CustomAK8Puppi_iMDWW",
		"CustomAK8Puppi_iMDtop",
		"CustomAK8Puppi_iW",
		"CustomAK8Puppi_iMDW",
		"CustomAK8Puppi_iMDtop",
		"CustomAK8Puppi_msoftdrop",
		"CustomAK8Puppi_tau1",
		"CustomAK8Puppi_tau2",
		"CustomAK8Puppi_tau21",
		"CustomAK8Puppi_btagHbb",
		"CustomAK8Puppi_rawFactor",
		"CustomAK8Puppi_area",
		"CustomAK8Puppi_subJetIdx1",
		"CustomAK8Puppi_subJetIdx2",
		"nCustomAK8PuppiSubJet",
		"CustomAK8PuppiSubJet_eta",
		"CustomAK8PuppiSubJet_mass",
		"CustomAK8PuppiSubJet_phi",
		"CustomAK8PuppiSubJet_pt",
		"CustomAK8PuppiSubJet_rawFactor",
		"CustomAK8PuppiSubJet_area",
		"nJet",
		"Jet_pt",
		"Jet_eta",
		"Jet_phi",
		"Jet_mass",
		"Jet_jetId",
		"Jet_btagDeepFlavB",
		"Jet_btagCSVV2",
		"Jet_rawFactor",
		"Jet_area",
		"fixedGridRhoFastjetAll",
		"event",
		"Flag_goodVertices",
		"Flag_globalSuperTightHalo2016Filter",
		"Flag_HBHENoiseFilter",
		"Flag_HBHENoiseIsoFilter",
		"Flag_EcalDeadCellTriggerPrimitiveFilter",
		"Flag_BadPFMuonFilter",
		"Flag_BadChargedCandidateFilter",
		"PV_npvs",
		"PV_npvsGood",
		"PV_chi2",
		"PV_ndof",
		"Flag_eeBadScFilter"]

		if(not NanoF.isdata):
			branchesmc =[
				"nCustomGenJetAK8",
				"CustomGenJetAK8_pt",
				"CustomGenJetAK8_eta",
				"CustomGenJetAK8_phi",
				"CustomGenJetAK8_mass",
				"nGenPart",
				"GenPart_pt",
				"GenPart_eta",
				"GenPart_phi",
				"GenPart_mass",
				"GenPart_pdgId",
				"GenPart_statusFlags",
				"GenPart_genPartIdxMother",
				"nGenJet",
				"GenJet_pt",
				"GenJet_eta",
				"GenJet_phi",
				"GenJet_mass",
				"GenJet_hadronFlavour",
				"GenJet_partonFlavour",
				"Pileup_nTrueInt",
				"genWeight",
				"nLHEScaleWeight",
				"LHEScaleWeight",
				"nLHEPdfWeight",
				"LHEPdfWeight"
				]
			if(options.era!="2018"):
				branchesmc+=["L1PreFiringWeight_Nom","L1PreFiringWeight_Up","L1PreFiringWeight_Dn"]
			branchestokeeprdf+=branchesmc




		branchestokeeprdf+=btoappend
		for bb in branchestokeeprdf:
			branchesrdf.push_back(bb)

		jobstr=""
		if jobarr[1]!=1:
			jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])

		if not options.skipskim:
			print "start skim"
			if not os.path.exists("rdftemp"):
			    	os.mkdir("rdftemp")
			    	print "created rdftemp"

			totnev+=int(filtarr[-1].Count())
			filtarr[-1].Snapshot("Events", "rdftemp/NanoAODskim_skimmer_"+options.era+runver+"__"+setnametowrite+jobstr+".root",branchesrdf)



		else:
			print "WARNING SKIPPING SKIM"
		rdffiles.append("rdftemp/NanoAODskim_skimmer_"+options.era+runver+"__"+setnametowrite+jobstr+".root")
	print "Total events",totnev
	#Dictionary of weights, init on event
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

	#Save SR event numbers  
	allCevs=[]
	kill=False
        avedef=[]
        avecorr=[]


	for curfilename in rdffiles:

		if NanoF.isdata:
			runlet = ""
			parsename =  curfilename.split("_")
			for pars in parsename:
				if pars.find("Run201")!=-1:
					runlet=pars[11:]
					break
		else:
			runlet="All"
		
			
		
		
		recal =NanoF.recal[runlet]
		recalak4 = NanoF.recalak4[runlet]
		recalak4puppi = NanoF.recalak4puppi[runlet]
		print "New JEC",curfilename,runlet,recal.globalTag, recal.jecPath, recal.jetFlavour


		if kill:
			break

		try:
			curfile = TFile.Open(curfilename)
			curttree = curfile.Get("Events")
		except:
			logging.warning("ERROR OPENING FILE")
			continue
		nent = curttree.GetEntries()

		itertree = iter(curttree)

		#Event splitting option, not used usually
		if (options.eventsplitting):
			itertree = itertools.islice(itertree,(jobarr[0]-1),nent,jobarr[1])

		avetime=0
		stevtime = time.time()
		
		for iev in xrange(nent):

			genpart,genweight,genjet,pdfweights,q2weights=None,None,None,None,None
			counts+=1

			try:
				ev=itertree.next()
			except:
				print "EV ERR!"
				continue
		
			if counts%10000==0:
				break
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
			
			rmap = getattr(ev,"regionmap_"+regionstr)
			passedregs= NanoF.RegionMap(rmap,regions)

			#Only run regions that will pass cut selection
			regstorun = []
			for pp in passedregs:
				if pp in regions:
					regstorun.append(pp)
			genpart = NanoF.ExpandGeneric(ev,"GenPart",20,ptcut=0.0)
			truthpart = NanoF.GenTruth(genpart)

			ak4jets=NanoF.ExpandGeneric(ev,"Jet")

			htval = 0
			for ak4jet in ak4jets:
				if ak4jet.p4.Perp()<30.0:
					continue
				htval += ak4jet.p4.Perp()
			if htval<1000:
				continue
			tofilldrs={}
			for tt in truthpart:
				#print tt,truthpart[tt].pt
				histos["all"]["pt__"+tt+"__all"].Fill(truthpart[tt].pt)
				histos["all"]["eta__"+tt+"__all"].Fill(abs(truthpart[tt].eta))
				for tto in truthpart:
					strname=sorted(tt+tto)[0]+sorted(tt+tto)[1]
					#print strname
					if tt!=tto and (not strname in tofilldrs):
						tofilldrs[strname]=truthpart[tt].p4.DeltaR(truthpart[tto].p4)
			for tofilldr in tofilldrs:
				histos["all"]["DR__"+tofilldr+"__all"].Fill(tofilldrs[tofilldr])
				#print tofilldr,tofilldrs[tofilldr]
			#if 'C' in regstorun:
				#print 'C'





	print "Finished Looping..."
	jobstr=""
	if jobarr[1]!=1:
		jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
	output = ROOT.TFile("NanoAODskimMatch_"+options.anatype+macro+options.era+hemstr+prefstr+"__"+setnametowrite+jobstr+".root","recreate")
	output.cd()
	allhiststowrite=[histos]
	for histoset in allhiststowrite:
		for histo in histoset:
			for histo1 in histoset[histo]:
				histoset[histo][histo1].Write()

	print "Writing rootfile from "+curset+"..."


	output.Write()
	output.Close()
	#print histos("pt__T__C").GetEntries()
	for hh in histos:
		#print hh
		del hh
	print "Written.."
print "Completed..."


