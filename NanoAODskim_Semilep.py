
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
		  default	=	'Mu',
		  dest		=	'anatype',
		  help		=	'')
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
parser.add_option('--skipskim', metavar='F', action='store_true',
		  default=False,
		  dest='skipskim',
		  help='skipskim')

(options, args) = parser.parse_args()



#All Files in tarred directory
di=""
if options.condor:
	di="tardir/"

#For specific objects
import NanoAODskim_Functions
from NanoAODskim_Functions import *

#Forced PU reweight
#puf=TFile.Open(di+"PUF_"+options.anatype+options.era+".root")
#puh=puf.Get("pvrat")
regionstr=options.anatype
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
	jobarr = [options.job,options.totaljobs]
	if jobarr[0]>jobarr[1]:
		logging.error("Job Number Higher Than Total Jobs")
		sys.exit()


	setname = curset
	setnametowrite=setname.split('/')[0]
	print "set name",setnametowrite
	settype=SetFilter(setname)
	print "set type",settype
	vstr= (options.version).split(",")
	NanoF = NanoAODskim_Functions(options.anatype,options.era,vstr,settype,options.condor)
	if (not NanoF.isdata):
		constdict = NanoF.LoadConstants
		#Lumi, Nevents
		lumi = constdict["lumi"]
		nev_xsec = constdict["dataconst"][setnametowrite]

		#Average of (+/-) event weights
		#posfac = constdict["posfac"][setnametowrite]

		#not using weights for SF
		posfac = 1.0
		posmmin = posfac
		prefirenorm=1.0
		if options.era=="2017":
			prefirenorm=0.96
		if options.era=="2016":
			prefirenorm=0.98
		nevweighted=float(nev_xsec[0])*posmmin

		setweight = lumi*nev_xsec[1]*prefirenorm/float(nevweighted)

		print "Nevents=",nev_xsec[0],"Posfac=",posfac,"Neventsweighted=",nevweighted
		print "Using MC weights..."
		print "\t... Using Constants: Lumi =",lumi,"; Xsec =",nev_xsec[1],"; Nevents =",float(nevweighted)

	else:
		print "Using data..."
		setweight = 1.0

	print "\t... Weight =",setweight

	if (not NanoF.isdata):
		setnametowrite+="__"+options.search
	#Objects to plot
	labels = NanoF.labels
	ak8labs = NanoF.ak8labels
	ak4labs =NanoF.ak4labels

	#Background estimation roles semilep overrides this (no data driven)
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
	#overridden for semilep
	macro="Ana"

	#Do systematic shifts
	doshifts=False
	if macro=="Ana":
		doshifts=True
		# C is CP+CF, the histos are sliced later, this is just for visualization
		regions=["C","CP","CF"]


		#Why both?
		FSregions=copy.copy(regions)
		anaregions=copy.copy(regions)

		#Init standard plots for objects and cut profiles
		histofills = copy.deepcopy(regions)
		histos = NanoF.HistosInit(labels,histofills)

		if (not NanoF.isdata):
			weightstoplot = ["genweightsf"]

		binstrs=[]
	print "Start Looping..."
	counts = 0
	print settype

	#different ttbar modes
	matches=[1,2,3,4,5]

	sttime=time.time()


	#Compute minimums for skimming
	minpt = 9999999.
	minptak4 = 9999999.

	for region in regions:
		LCR = (NanoF.LoadCuts)[region]
		for akl in ak8labs:
			minpt=min(minpt,LCR["ptAK8__"+akl])

		if "B" in ak4labs:
			minptak4=min(minptak4,LCR["pt__B"])



	print "min pt, softdrop mass for triggering",minpt
	print "min pt ak4",minptak4

	#variables to compute full uncertainty for
	errvals = ["mass","pt","eta","msoftdropdef"]


	shiftnames = []
	shiftuncert=[""]
	errnames = []
	if (not NanoF.isdata):
		errnames.append("trig")
		#errnames.append("pu")
		#if "B" in ak4labs:
			#errnames.append("btag")
			#errnames.append("bmistag")

		#errnames.append("prefire")
		errnames.append("btag")
		if settype=="TT" :
			errnames.append("pdfweight")

			errnames.append("tptrw")
			errnames.append("q2")
		if doshifts:
			shiftnames = ["jes","jer"]
			shiftuncert=["","jes__up","jes__down","jer__up","jer__down"]

	#init jet correctors

	weightshistos=[]
	if macro=="Ana" and (not NanoF.isdata):
		for errname in errnames:
			#print errname
			weightstoplot.append(errname+"sf")
			weightstoplot.append(errname+"up")
			weightstoplot.append(errname+"down")
		weightshistos = NanoF.WeightsHistosInit(weightstoplot,["C"])

	#Select up and down histograms to compute
	uphistos={}
	downhistos={}
	prehisto = copy.deepcopy(histos)
	for errname in (errnames+shiftnames):
		uphistos[errname]={}
		downhistos[errname]={}
		for errval in errvals:
			for region in FSregions:
				uphistos[errname][region]={}
				downhistos[errname][region]={}
				for hn in prehisto[region]:
					#print hn.split("__")[0],errvals
					if (hn.split("__")[0] in errvals):

						#print hn.split("__")[1],len(hn.split("__")[1])
						#if (hn.split("__")[0]!="mass") and (len(hn.split("__")[1])>1):
						#	continue
						#print [hn+"__"+errname+"__up"], [hn+"__"+errname+"__down"]
						copyhist = copy.copy(prehisto[region][hn])
						copyhist.SetName(hn+"__"+errname+"__up")
						uphistos[errname][region][hn+"__"+errname+"__up"]=copyhist
						copyhist = copy.copy(prehisto[region][hn])
						copyhist.SetName(hn+"__"+errname+"__down")
						downhistos[errname][region][hn+"__"+errname+"__down"]=copyhist


	mhistos={}

	curhdicts=[histos,uphistos,downhistos]

	for ihd,curhdict in enumerate(curhdicts):

		if settype=="TT":
			for hh in curhdict:
				if ihd>0:
					mhistos[hh]={}
				for mm in matches:
					#if ihd>0:
					#	mhistos[hh]={}
					if ihd==0:
						mhistos[hh+"m"+str(mm)]={}

					for qq in curhdict[hh]:
						if ihd>0:
							mhistos[hh][qq+"m"+str(mm)]={}
							for errd in curhdict[hh][qq]:
								 newn=curhdict[hh][qq][errd].GetName().replace(qq,qq+"m"+str(mm))
								 #newi=curhdict[hh][qq][errd].GetName().replace(qq,qq+"m"+str(mm))
								 mhistos[hh][qq+"m"+str(mm)][newn] = copy.deepcopy(curhdict[hh][qq][errd])

								 mhistos[hh][qq+"m"+str(mm)][newn].SetName(newn)
								 #mhistos[hh+"m"+str(mm)][qq+"m"+str(mm)][errd].SetTitle(curhdict[hh][qq][errd].GetTitle()+"m"+str(mm))
						else:
							newn=curhdict[hh][qq].GetName().replace(hh,hh+"m"+str(mm))
							mhistos[hh+"m"+str(mm)][newn] = copy.deepcopy(curhdict[hh][qq])
							mhistos[hh+"m"+str(mm)][newn].SetName(newn)
							#mhistos[hh+"m"+str(mm)][qq+"m"+str(mm)].SetTitle(curhdict[hh][qq].SetTitle()+"m"+str(mm))
				if ihd>0:
					#print hh
					#print mhistos[hh]
					curhdict[hh].update(mhistos[hh])
		if ihd==0:
			curhdict.update(mhistos)
		#print curhdict
	#for uu in  uphistos:
	#	print uu
	#	print uphistos[uu]
	#print "Loading Files..."
	#Return all sorted files
	allfiles = NanoF.LoadFiles(setname,options.folder,options.redir,options.search)
	isdata=NanoF.isdata


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
		print fset
		cfiles =ROOT.vector('string')()
		for cfile in fset:
			cfiles.push_back(cfile)

		#Start RDF
		df= ROOT.ROOT.RDataFrame("Events",cfiles)
		NanoF.SetRunTrigs("NONE")
		alltr = []
		trigcut=""
		runver = ""



		if NanoF.isdata:
				#Run dependent
				parsename =  fset[0].split("/")
				for pars in parsename:
					if pars.find("Run201")!=-1:
						runver=pars[0:8]
				NanoF.SetRunTrigs(runver)
		print runver,
		if options.anatype=="Mu":
			alltr = NanoF.mutrigs

			lepcut = 	'''
					for(uint nmu=0;nmu<nMuon;nmu++)	{
						if (((Muon_pt[nmu]>50.0)&&(Muon_mediumId[nmu])))return true;
									}
					return false;
					'''
		if options.anatype=="Ele":
			alltr = NanoF.eletrigs
			lepcut = 	'''
					for(uint nel=0;nel<nElectron;nel++)	{
						if ((Electron_pt[nel]>50.0)&&((Electron_mvaFall17V2noIso_WP80[nel]>0) || (Electron_mvaFall17V2Iso_WP80[nel]>0))) return true;
										}
					return false;
					'''
		print "Trig",alltr

		for ctr in alltr:
			trigcut+="("+ctr+">0)"
			if ctr!= alltr[-1]:
				trigcut+="||"

		#Allow 30GeV JEC leeway (hacky)
		ak8ptval=str(minpt-30.0)
		presel =[
				"nCustomAK8Puppi>=1",
				"CustomAK8Puppi_pt[0]>"+ak8ptval,
				lepcut
			]
		presel.append(trigcut)


		print "start presel"
		filtarr = [df]
		df1  = df.Filter(presel[0])
		for sel in presel:
			filtarr.append(filtarr[-1].Filter(sel))

		print "finish presel"

		print "start tagging"

		#default corr softdrop
		filtarr[-1]=filtarr[-1].Define("CustomAK8Puppi_msoftdropdef","CustomAK8Puppi_msoftdrop")

		ttags = {}
		for ak8lab in NanoF.ak8labels:
			ttags[ak8lab]=[]
		btoappend = []
		nregions=0

		regionmstr=""
		written=[]

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
					print "CustomAK8Puppi_"+varn,ttags[tag]
					filtarr[-1]=filtarr[-1].Define("CustomAK8Puppi_"+varn,ttags[tag])
					btoappend.append("CustomAK8Puppi_"+varn)

				maxstrs={}
				for tag in ttags:
					varn = region+"__"+tag+"__tag"
					maxstrs[tag]="int(*std::max_element(std::begin(CustomAK8Puppi_"+varn+"),std::end(CustomAK8Puppi_"+varn+")))==1"
				#make sure all objects have at least one tag
				nregions=regions.index(region)
				maxch = "if (("+maxstrs[NanoF.ak8labels[0]]+"))return 1<<"+str(nregions)+";else return 0;"
				regch = regionstr+"region_"+region
				filtarr[-1]=filtarr[-1].Define(regch,maxch)
				regionmstr+=regionstr+"region_"+region+"+"


		regionmstr=regionmstr[:-1]
		#Create bit encoded regionmap
		filtarr[-1]=filtarr[-1].Define("regionmap_"+regionstr,regionmstr)
		filtarr.append(filtarr[-1].Filter("(regionmap_"+regionstr+">0)"))

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
		"CustomAK8Puppi_btagHbb",
		"CustomAK8Puppi_rawFactor",
		"CustomAK8Puppi_area",
		"CustomAK8Puppi_subJetIdx1",
		"CustomAK8Puppi_subJetIdx2",
		"nCustomAK4CHS",
		"CustomAK4CHS_area",
		"CustomAK4CHS_btagCSVV2",
		"CustomAK4CHS_btagDeepB",
		"CustomAK4CHS_eta",
		"CustomAK4CHS_mass",
		"CustomAK4CHS_phi",
		"CustomAK4CHS_pt",
		"CustomAK4CHS_rawFactor",
		"CustomAK4CHS_jetId",
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
		"run",
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
		"Flag_eeBadScFilter",
		"nElectron",
		"Electron_eta",
		"Electron_mass",
		"Electron_phi",
		"Electron_pt",
		"Electron_mvaFall17V2Iso_WP80",
		"Electron_mvaFall17V2noIso_WP80",
		"Electron_mvaFall17V2Iso_WP90",
		"Electron_mvaFall17V2noIso_WP90",
		"MET_phi",
		"MET_pt",
		"MET_significance",
		"MET_sumEt",
		"nMuon",
		"Muon_eta",
		"Muon_mass",
		"Muon_phi",
		"Muon_pt",
		"Muon_highPtId",
		"Muon_mediumId",
		"Muon_miniIsoId",
		"Muon_tightId",
		"Muon_pfIsoId",
		"Muon_miniPFRelIso_all"]



		if(not NanoF.isdata):
			branchesmc =[
				#"btagWeight_DeepCSVB",
				"btagWeight_CSVV2",
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
				"nCustomGenJetAK8",
				"CustomGenJetAK8_pt",
				"CustomGenJetAK8_eta",
				"CustomGenJetAK8_phi",
				"CustomGenJetAK8_mass",
				"Pileup_nTrueInt",
				"genWeight",
				"nLHEScaleWeight",
				"LHEScaleWeight",
				"nLHEPdfWeight",
				"LHEPdfWeight"
				]
		
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


	#Save SR event numbers
	allCevs=[]
	kill=False
        avedef=[]
        avecorr=[]

	evhistos={}
	evhistos["PV_npvs_pre"]=TH1F("PV_npvs_pre",	"PV_npvs_pre",		100, 0.,100 )
	evhistos["PV_npvs_post"]=TH1F("PV_npvs_post",	"PV_npvs_post",		100, 0.,100 )
	evhistos["PV_npvs_postup"]=TH1F("PV_npvs_postup",	"PV_npvs_postup",		100, 0.,100 )
	evhistos["PV_npvs_postdown"]=TH1F("PV_npvs_postdown",	"PV_npvs_postdown",		100, 0.,100 )
	evhistos["pdfuncevup"]=TH1F("pdfuncevup",	"pdfuncevup",		100, 0.,2 )
	evhistos["pdfuncevdown"]=TH1F("pdfuncevdown",	"pdfuncevdown",		100, 0.,2 )

	evhistos["met"]=TH1F("met",	"met",		200, 0.,1000. )
	evhistos["miniiso"]=TH1F("miniiso",	"miniiso",		100, 0.,2 )
	evhistos["ptrel"]=TH1F("ptrel",	"ptrel",		220, -20.,200 )
	evhistos["wmass"]=TH1F("wmass",	"wmass",		100, 0.,200)
	evhistos["tmass"]=TH1F("tmass",	"tmass",		100, 0.,250)
	evhistos["tmasssub"]=TH1F("tmasssub",	"tmasssub",		100, 0.,250)
	evhistos["wpt"]=TH1F("wpt",	"wpt",		100, 0.,1000 )
	evhistos["wptsub"]=TH1F("wptsub",	"wptsub",		100, 0.,1000 )
	evhistos["drlak4"]=TH1F("drlak4",	"drlak4",		100, 0.,5 )
	evhistos["drwak8"]=TH1F("drwak8",	"drwak8",		100, 0.,5 )
	evhistos["tpt"]=TH1F("tpt",	"tpt",		100, 0.,1000 )
	evhistos["drlak8"]=TH1F("drlak8",	"drlak8",		100, 0.,5 )
	#ROOT.ROOT.DisableImplicitMT()
	for curfilename in rdffiles:
		#Reset JECs for new run

		if NanoF.isdata:
			runlet = ""
			parsename =  curfilename.split("_")
			for pars in parsename:
				if pars.find("Run201")!=-1:
					runlet=pars[11:]
					break
		else:
			runlet="All"
		
			
	
		
		recal = NanoF.recal[runlet]
		recalak4 = NanoF.recalak4[runlet]
		recalak4puppi = NanoF.recalak4puppi[runlet]
		print "New JEC",curfilename,runlet,recal.globalTag, recal.jecPath, recal.jetFlavour
	
		#recalchs = NanoF.jmeCorrectionschs().jetReCalibrator


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
			genpart,genweight,bweight,genjet,pdfweights,q2weights=None,None,None,None,None,None
			counts+=1

			try:
				ev=itertree.next()
			except:
				print "EV ERR!"
				continue

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

			#Debugging run
			#if counts>10000:
			#	kill=True
			#	break

			#Decodes bool encoded region map
			rmap = getattr(ev,"regionmap_"+regionstr)
			passedregs= NanoF.RegionMap(rmap,regions)

			#Only run regions that will pass cut selection
			regstorun = []
			for pp in passedregs:
				if pp in regions:
					regstorun.append(pp)
			if regstorun==[]:
				continue
			#Initialize Event objects
			ak8jetsFF=NanoF.ExpandGeneric(ev,"CustomAK8Puppi",maxlen=3)
			ak4jetsFF=NanoF.ExpandGeneric(ev,"Jet")
			MuonFF=NanoF.ExpandGeneric(ev,"Muon")
			ElecFF=NanoF.ExpandGeneric(ev,"Electron")
			ak8subjetsFF=NanoF.ExpandGeneric(ev,"CustomAK8PuppiSubJet")

			#MC stuff
			if not NanoF.isdata:
				CustomGenJetAK8FF=NanoF.ExpandGeneric(ev,"CustomGenJetAK8",maxlen=-1)
				CustomGenJetAK4FF=NanoF.ExpandGeneric(ev,"GenJet",maxlen=-1)
				nTrueInt = getattr(ev, "Pileup_nTrueInt")

			ak4lepsub=NanoF.ExpandGeneric(ev,"CustomAK4CHS")
			els=[]
			mus=[]
			bestlep=None

			for mm in MuonFF:
				#print mm.tightId,mm.pt
				if mm.mediumId and mm.pt>50.:
					mus.append(mm)

			for ee in ElecFF:
				#print ee.mvaFall17V2Iso_WP90,ee.mvaFall17V2Iso_WP90,ee.pt
				if (ee.mvaFall17V2Iso_WP80 or ee.mvaFall17V2noIso_WP80) and ee.pt>50.:
					els.append(ee)
			if len(mus)>0 and len(els)>0:
				continue
			if options.anatype=="Mu":
				bestlep=mus[0]
			if options.anatype=="Ele":
				bestlep=els[0]
			if bestlep==None:
				continue
			metpt = getattr(ev,"MET_pt")
			metphi = getattr(ev,"MET_phi")
			if metpt<40.:
				continue

			jets_msoftdrop_raw,jets_msoftdrop_nom=NanoF.CorrectSdMass(ak8jetsFF,ak8subjetsFF )


			#print jets_msoftdrop_raw
			#print ak8jetsFF
                        for iak8 in xrange(len(ak8jetsFF)):
				ak8jetsFF[iak8].msoftdrop=jets_msoftdrop_nom[iak8]

			#MC stuff
			#if not NanoF.isdata:
			#	CustomGenJetAK8FF=NanoF.ExpandGeneric(ev,"CustomGenJetAK8",maxlen=-1)
			#	CustomGenJetAK4FF=NanoF.ExpandGeneric(ev,"GenJet",maxlen=-1)
			#	nTrueInt = getattr(ev, "Pileup_nTrueInt")

			rho = getattr(ev, "fixedGridRhoFastjetAll")
			eventnumber = getattr(ev, "event")
			runnumber = getattr(ev, "run")

			PV_npvs = getattr(ev, "PV_npvs")
			#print PV_npvs

			evhistos["PV_npvs_pre"].Fill(PV_npvs)
			if (not NanoF.isdata):
				#pubin=puh.FindBin(float(PV_npvs))
				#ppuw=puh.GetBinContent(pubin)
				#print float(PV_npvs),ppuw
				evpuweight= NanoF.PuWeight(float(nTrueInt))
				#evpuweight= {"sf":ppuw,"down":1.0,"up":1.0}
				evhistos["PV_npvs_post"].Fill(float(PV_npvs),evpuweight["sf"])
				evhistos["PV_npvs_postup"].Fill(float(PV_npvs),evpuweight["up"])
				evhistos["PV_npvs_postdown"].Fill(float(PV_npvs),evpuweight["down"])
				if settype=="TT":
					pdfweights=[]
					#tempth1=TH1F("tempth1",	"tempth1",		10000, -1.0,5.0 )
					pdfarr=getattr(ev, "LHEPdfWeight")
					for ipdf in range(1,len(pdfarr)-2):
						pdfweights.append(float(pdfarr[ipdf]))
					#	tempth1.Fill(float(getattr(ev, "LHEPdfWeight")[ipdf]))
						#print ipdf,pdfweights[-1]
					#print len(pdfarr),pdfarr[-2]
					#print len(pdfarr),pdfarr[-1]
					#alphas=[float(pdfarr[-2]),float(pdfarr[-1])]
					evpdfweight=NanoF.PdfWeight(pdfweights)
					#print evpdfweight
					#print tempth1.Integral(),tempth1.GetRMS(),evpdfweight

					evhistos["pdfuncevup"].Fill(evpdfweight["up"])
					evhistos["pdfuncevdown"].Fill(evpdfweight["down"])
					ttq2s=getattr(ev, "LHEScaleWeight")
					q2indices=[0,1,3,5,7,8]
					q2weights=[]
					#q2indices=[0,5,15,24,34,39]
					#for qq in ttq2s:
					#	print qq
					for iq2 in q2indices:
						q2weights.append(float(ttq2s[iq2]))
						#print iq2,q2weights[-1]
					evq2weights = NanoF.Q2Weight(q2weights)

			if options.era=="2018":
			 	if NanoF.isdata:
					run=runnumber
				else:
					run=-1
				
				HEMnuke=False
				for iak4 in xrange(len(ak4jetsFF)):
					if ak4jetsFF[iak4]>30.0:
						if NanoF.HEMskip(ak4jetsFF[iak4],run):
							HEMnuke=True	
				for ieele in xrange(len(ElecFF)):
					tempsc=NanoF.HEMskip(ElecFF[ieele],run)
					if NanoF.HEMskip(ElecFF[ieele],run):
						HEMnuke=True	
				if HEMnuke:
					continue
	
	
			#print PV_npvs

			#Event MET filters
			filtp=NanoF.FilterPass(ev)
			if not filtp:
				continue
			savept=[]
			for ak8j in ak8jetsFF:
				savept.append(ak8j.pt)
			#Loop over shifts
			for shift in shiftuncert:
				#Tie all rng to event number
				NanoF.rnd1.SetSeed(eventnumber)
				NanoF.rnd2.SetSeed(eventnumber)
				random.seed(eventnumber)

				ak8jets=copy.deepcopy(ak8jetsFF)
				ak4jets=copy.deepcopy(ak4jetsFF)
				ak8subjets=copy.deepcopy(ak8subjetsFF)

				shstr=""
				shtype=""
				splshift=shift.split("__")
				if len(splshift)>1:
					shstr=splshift[1]
					shtype=splshift[0]

				histostoplot = histos
				delta=0
				if shstr=="up":
					histostoplot = uphistos[shtype]
					delta=1
				if shstr=="down":
					histostoplot = downhistos[shtype]
					delta=-1


				#for ak8j in ak8jets:
				#	(jet_pt, jet_mass) = recal.correct(ak8j,rho,delta=delta)
				#	print (jet_pt/ak8j.pt)

				jscalefac=1.0
				jsmearfac=1.0
				if True:

					for ak8j in ak8jets:
						(jet_pt, jet_mass) = recal.correct(ak8j,rho,delta=delta)

						jscalefac= jet_pt/ak8j.pt
						ak8j.pt = jet_pt
						ak8j.mass = jet_mass
						ak8j.setp4()


					for ak4j in ak4jets:
						(jet_pt, jet_mass) = recalak4.correct(ak4j,rho,delta=delta)
						ak4j.pt = jet_pt
						ak4j.mass = jet_mass
						ak4j.setp4()

					for subj in ak8subjets:
						(jet_pt, jet_mass) = recalak4puppi.correct(subj,rho,delta=delta)
						#print jet_pt/subj.pt
						subj.pt = jet_pt
						subj.mass = jet_mass
						subj.setp4()


				if not NanoF.isdata:

					CustomGenJetAK8=copy.deepcopy(CustomGenJetAK8FF)
					CustomGenJetAK4=copy.deepcopy(CustomGenJetAK4FF)

					jind=0
					if (shtype=="jer") and (shstr=="up"):
						jind=2
					if (shtype=="jer") and (shstr=="down"):
						jind=1

					NanoF.JerSmear(ak8jets, CustomGenJetAK8,rho,jind,jtype="ak8")
					NanoF.JerSmear(ak4jets, CustomGenJetAK4,rho,jind,jtype="ak4")
					NanoF.JerSmearstoc(ak8subjets,rho,jind,jtype="ak4")

				for iak8,ak8j in enumerate(ak8jets):
					jets_msoftdropdef_nom=NanoF.CorrectSdMassdef(ak8jets,ak8subjets)
     					ak8j.msoftdropdef=jets_msoftdropdef_nom[iak8]
        				#print ak8j.msoftdropdef
				#sys.exit()
				htval = 0
				for ak4jet in ak4jets:
					if ak4jet.p4.Perp()<30.0:
						continue
					htval += ak4jet.p4.Perp()


				#Loop over passed regions
				weightdict={}

				for region in regstorun:
					#Dont run shifts for bkg regions
					if (shift!="") and not (region in FSregions):
						continue

					weightdict[region] = resetweightdict[region]
					weightdict[region]["setweight"] = {"sf":setweight}



					tagsak4 = {}
					for ak4lab in ak4labs:
						tagsak4[ak4lab]=[]
					tagsak8 = {}
					for ak8lab in ak8labs:
						tagsak8[ak8lab]=[]


					#For trimmass triggers
					maxsdmass=0.0

					ijet=0
					for ak4jet in ak4jets:

						if abs(ak4jet.p4.Eta())<2.4  and bestlep.p4.DeltaR(ak4jet.p4)<1.0:
							ak4jet.index=ijet
							for tag in tagsak4:
								if tag in ak8labs:
									continue
								ptcut=(NanoF.LoadCuts)[region]["pt__"+tag]
								if ak4jet.p4.Perp()>ptcut :
									if NanoF.TagJet(ak4jet,tag,region.split("__")[0]):
										tagsak4[tag].append(ijet)
						ijet+=1



					#Create tags
					ijet=0
					for ak8jet in ak8jets:
						maxsdmass=max(maxsdmass,ak8jet.msoftdrop)
						if ijet>njetinv-1:
							break
						#print bestlep.p4.DeltaR(ak8jet.p4)
						if abs(ak8jet.p4.Eta())<2.4  and bestlep.p4.DeltaR(ak8jet.p4)>1.6:
							ak8jet.index=ijet
							for tag in tagsak8:
								if tag in ak4labs:
									continue
								ptcut=(NanoF.LoadCuts)[region]["ptAK8__"+tag]
								if ak8jet.p4.Perp()>ptcut :
									if NanoF.TagJet(ak8jet,tag,region.split("__")[0]):
										tagsak8[tag].append(ijet)
						ijet+=1

					if len(tagsak4[probl])==0:
						continue

					#For double counting
					nfills=0

					#Loop over found probes.  In the case of overlap this allows multiple probabilistic entries
					#(Not currently implemented)
					for i in xrange(len(tagsak4[probl])):
						cands = {}
						for lab in labels:
							cands[lab]=None
						iprobe = tagsak4[probl][i]
						cands[probl]=ak4jets[iprobe]
						for ic in xrange(len(tagsak8[candl])):
							icand = tagsak8[candl][ic]
							tempc=ak8jets[icand]
							if cands[probl].p4.DeltaR(tempc.p4)>1.4:
								cands[candl]=tempc
								break

						#For lead, sublead param

						if cands[probl]==None or cands[candl]==None:
							continue
						lepmak=None
						mindr=999999.
						for akls in ak4lepsub:
							if akls.p4.DeltaR(bestlep.p4)<mindr:
								lepmak=akls
								mindr=akls.p4.DeltaR(bestlep.p4)
						ptrel=-1.0
						if lepmak!=None:
							ptrel=bestlep.p4.Perp(lepmak.p4.Vect())

						#print mindr,ptrel
						if bestlep.p4.DeltaR(cands[probl].p4)<0.4 and ptrel<35.:
							continue
						if bestlep.p4.DeltaR(cands[probl].p4)>0.4:
							if options.anatype=="Ele":
								if not (bestlep.mvaFall17V2Iso_WP90>0):
									continue
							if options.anatype=="Mu":
								if bestlep.pfIsoId<4:
									continue

						recnu,recW = NanoF.MakeWNu(metpt,metphi,bestlep,cands[probl])
						recnusub,recWsub = NanoF.MakeWNu(metpt,metphi,bestlep,lepmak)

						if (recW+cands[probl].p4).M()<130.:
							continue
						if (recW+cands[probl].p4).M()>250.:
							continue
						if (recW+cands[probl].p4).Perp()<250.:
							continue



						#AK4 event level stuff ht etc
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
							if (cands[candl].p4.DeltaR(ak4jet.p4)>1.4 and cands[probl].p4.DeltaR(ak4jet.p4)>1.4):
								htvalrem += ak4jet.p4.Perp()
								njetsrem += 1


						#Check for AK4 tag
						foundall=True
						tries=0


						if not foundall:
							continue
						globalb+=1
						if tries!=1:
							globalbsub+=1
							#print  "gbs",float(globalbsub)/float(globalb)
						#Form invariant mass pairs
						threecand=None
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
									cands[lab] = InvObj(candarr)
									cands[lab].njets=njets
									cands[lab].htval=htval

									cands[lab].njetsrem=njetsrem
									cands[lab].htvalrem=htvalrem

									if len(lab)>2:
										threecand=lab
					

						if (not NanoF.isdata):

							if genjet==None:
								genjet = NanoF.ExpandGeneric(ev,"GenJet",10,ptcut=0.0)
							if genpart==None:
								genpart = NanoF.ExpandGeneric(ev,"GenPart",20,ptcut=0.0)
							if genweight==None:
								#genweight = float(getattr(ev, "genWeight"))
								genweight = 1.0

							#if bweight==None:
							#	bweight = float(getattr(ev, "btagWeight_CSVV2"))
								#print bweight
							weightdict[region]["genweight"] = {"sf":genweight}
							#weightdict[region]["btag"] = {"sf":bweight}

							if settype=="TT":
								weightdict[region]["tptrw"] = NanoF.Tptrw(genpart)
								#tempbtag,tempbmistag = NanoF.BTagSf(cands["B"],"T",5)
								#weightdict[region]["btag"]["down"]=tempbtag["down"]
								#weightdict[region]["btag"]["up"]=tempbtag["up"]
								#print "tbt",tempbtag,weightdict[region]["btag"]
								weightdict[region]["q2"] = evq2weights

								weightdict[region]["pdfweight"] = evpdfweight

							hadfl=NanoF.GenMatchAK4(cands["B"],genjet)
							weightdict[region]["btag"],weightdict[region]["bmistag"] = NanoF.BTagSf(cands["B"],"T",hadfl)
					


							#PU weighting
							weightdict[region]["pu"] = evpuweight

							#This checks if a region has the nominal tag to apply the sf, otherwise dont. Should not be hardcoded
							#Careful, B is different
							#if "B" in ak4labs:





						#A bit hacky, plotting is performed using dictionaries instead of object class
						plotdict = NanoF.CandToDict(cands)
						matchval=1
						if settype=="TT":
							matchval=NanoF.GenMatchForSF(cands[candl],genpart)
						#print matchval
						if True:

							if options.anatype=="Mu":
								evhistos["miniiso"].Fill(bestlep.miniPFRelIso_all)
							evhistos["ptrel"].Fill(ptrel)
							evhistos["wmass"].Fill(recW.M())
							evhistos["tmass"].Fill((recW+cands[probl].p4).M())
							evhistos["tpt"].Fill((recW+cands[probl].p4).Perp())
							if lepmak!=None:
								evhistos["tmasssub"].Fill((recWsub+lepmak.p4).M())
							evhistos["wpt"].Fill(recW.Perp())
							evhistos["met"].Fill(metpt)
							evhistos["wptsub"].Fill(recWsub.Perp())
							evhistos["drlak4"].Fill(bestlep.p4.DeltaR(cands[probl].p4))
							evhistos["drwak8"].Fill(recW.DeltaR(cands[candl].p4))
							evhistos["drlak8"].Fill(bestlep.p4.DeltaR(cands[candl].p4))

							if (macro=="Ana" and region!="FT" and (region in anaregions) and nfills!=0):
								break
							#if (macro=="Ana" and region!="FT" ):
							#	print htval,weightdict[region]["trig"]
							if region =="C" and (shift==""):
								allCevs.append(eventnumber)
								#print allCevs[-1]



							hweight=1.0
							for ww in weightdict[region]:
									hweight*=weightdict[region][ww]["sf"]
									#print region,ww,weightdict[region][ww]
							if (NanoF.isdata):
								if hweight!=1.0:
									logging.error("DATA with non-unity weight!!!")

							NanoF.HistosFill(histostoplot,plotdict,region,hweight)
							if settype=="TT":
								#print region+"m"+str(matchval)
								NanoF.HistosFill(histostoplot,plotdict,region+"m"+str(matchval),hweight)

							if (not NanoF.isdata):
								NanoF.WeightsHistosFill(weightshistos,weightdict,region)

							if (shift=="") and (region in FSregions):
								for normerr in errnames:
									for errval in ["down","up"]:
										hweight=1.0

										for ww in weightdict[region]:

											if (normerr==ww) and (errval in weightdict[region][ww]):
												hweight*=weightdict[region][ww][errval]
											else:
												hweight*=weightdict[region][ww]["sf"]
										#print errval
										if errval=="up":
											#print "up1"
											NanoF.HistosFill(uphistos[normerr],plotdict,region,hweight)
											if settype=="TT":
												#print "up2"
												NanoF.HistosFill(uphistos[normerr],plotdict,region+"m"+str(matchval),hweight)
										if errval=="down":
											#print "down1"
											NanoF.HistosFill(downhistos[normerr],plotdict,region,hweight)
											if settype=="TT":
												#print "down2"
												NanoF.HistosFill(downhistos[normerr],plotdict,region+"m"+str(matchval),hweight)


							nfills+=1


   

	print "Finished Looping..."
	jobstr=""
	if jobarr[1]!=1:
		jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
	output = ROOT.TFile("NanoAODskim_semilep_"+options.anatype+macro+options.era+"__"+setnametowrite+jobstr+".root","recreate")
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
	for evh in evhistos:
		evhistos[evh].Write()
	print "Writing rootfile from "+curset+"..."


	output.Write()
	output.Close()
	#print histos("pt__T__C").GetEntries()
	for hh in histos:
		#print hh
		del hh
	print "Written.."
print "Completed..."
#print len(allCevs),"SR events"
#for acev in allCevs:
#	print acev
