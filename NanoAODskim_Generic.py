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

parser.add_option('--genwoff', metavar='F', action='store_true',
		  default=False,
		  dest='genwoff',
		  help='genwoff')

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

genwoff=options.genwoff

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
		if not genwoff:
			posfac = constdict["posfac"][setnametowrite]
		else:
			posfac = 1.0
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

	if macro=="Bkg":
		#regions=["A","B","E","J","C","K","H","I","F","G","D","All"]
		regions=["A","B","E","J"]

		if options.anatype=="tHb" or options.anatype=="tZb":
			regions.append("M")
			regions.append("Z")
			regions.append("ZB")



		#Create leading, subleading separately (not always used)
		hemispheres = ["0","1"]

		if (not NanoF.isdata):
			weightstoplot = ["genweightsf"]
		
		#Init standard plots for objects and cut profiles
		histofills = copy.deepcopy(regions)
		histos = NanoF.HistosInit(labels,histofills)

		#Adds leading, subleading plots
		for region in regions:
			jetreg =[]
			for ild in xrange(2):
				jetreg.append(region+"_"+str(ild))
			histos.update(NanoF.HistosInit(labels,jetreg))
	FSregions = {}

	#Do systematic shifts
	doshifts=False
	if macro=="Ana":
		doshifts=True
		if settype=="QCD":
			ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
		else:
			ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__JetHT.root','open')
		ratehist = {}
		ratehist["D"]=ratefile.Get('rate')

		ratehist["ZD"]=ratefile.Get('ZBrate')

		ratehist["G"]=ratefile.Get('Erate')
		ratehist["L"]=ratefile.Get('Jrate')
		ratehist["I"]=ratefile.Get('rate')
		ratehist["O"]=ratefile.Get('Mrate')



		regions=["C","K","H","F","N","ZC"]
		rateregions = ["D","L","I","G","O","ZD"]
		
		#ttbar region categorized under THB
		if options.anatype=="tHb":
			ratehist["FTR"]=ratefile.Get('Mrate')
			regions+=["FT"]
			rateregions+=["FTR"]
			ratehist["DH"]=ratefile.Get('rate')
			ratehist["DL"]=ratefile.Get('rate')
			ratehist["DFM"]=ratefile.Get('Mrate')

		if False:#options.anatype in ["tHb","tZb"]:
			regions+=["CH","CL"]
			rateregions+=["DH","DL","DFM"]
			ratehist["DH"]=ratefile.Get('rate')
			ratehist["DL"]=ratefile.Get('rate')
			ratehist["DFM"]=ratefile.Get('Mrate')
		#Why both?
		FSregions=copy.copy(regions)
		anaregions=copy.copy(regions)

		ratehistos={}
		for ratetype in rateregions:
			regions.append(ratetype)
			ratehistos[ratetype] = []

	
		
		#Append all N-1 regions (hacky)
		for rname in NanoF.LoadCuts:
			if rname.find("NM1")!=-1:
				regions.append(rname)
		regions.append("NM2bt")

		bkgweights=["","__err","_0","__err_0","_1","__err_1"]
		if NanoF.isdata:
			bkgweights+=["_up","_down","_0__up","_1__up","_0__down","_1__down"]
		#Init standard plots for objects and cut profiles
		histofills = copy.deepcopy(regions)
		histos = NanoF.HistosInit(labels,histofills)

		if (not NanoF.isdata):
			weightstoplot = ["genweightsf"]

		binstrs=[]
		for ratetype in rateregions:

			#Assign region-TF relation
			ratestr = ""
			if ratetype=="G":
				ratestr = "E"
			if ratetype=="L":
				ratestr = "J"
			if ratetype=="ZD":
				ratestr = "ZB"
			if ratetype=="O":
				ratestr = "M"
			if ratetype=="FT":
				ratestr = "M"
			if ratetype=="DFM":
				ratestr = "M"

			for currate in bkgweights:

				exstr=""
				if currate!="":
					exstr = currate
					#print ratetype+exstr
					histos[ratetype+exstr]={}
					if currate.find("err")!=1:
						ratehistos[ratetype+exstr] = []
				#print ratetype,ratehist[ratetype]
				for ybin in xrange(ratehist[ratetype].GetNbinsY()+1):
					#print ybin
					#Dont think this is needed
					if currate=="":
						ratehistos[ratetype].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)))
						nxbins = ratehistos[ratetype][-1].GetNbinsX()+1
					elif currate.find("err")==-1:
						ratehistos[ratetype+exstr].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)+"_"+currate))
						nxbins = ratehistos[ratetype+exstr][-1].GetNbinsX()+1
	
					elif currate in ["_up","_down","_0__up","_1__up","_0__down","_1__down"]:
						ratehistos[ratetype+exstr].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)+"_"+currate))
						nxbins = ratehistos[ratetype+exstr][-1].GetNbinsX()+1
					else:
						nxbins = ratehistos[ratetype+exstr.replace("__err","")][ybin].GetNbinsX()+1

					#3d TF - pt,eta,plotval for uncertainty correlations
					#Only done for relevant kinematics.  Hardcoded identical binning 
					if currate in ["_up","_down","_0__up","_1__up","_0__down","_1__down"]:
						continue
					binstrs.append("bbin"+str(ybin))
					for lab in labels:
						histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__mass__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__mass__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__mass__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,800, 0.,8000.)

						if lab in ak4labs:
							histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,350, 0.,3500.)
						else:
							histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__pt__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,350, 400.,3900.)
							if len(lab)==1:
								histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__msoftdrop__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__msoftdrop__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__msoftdrop__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,240, 0.,480.)
								histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__msoftdropdef__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__msoftdropdef__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__msoftdropdef__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,240, 0.,480.)
						histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,60, -3.0,3.0)
			newhistos = NanoF.HistosInit(labels,[ratetype+"_0",ratetype+"_1",ratetype+"_up",ratetype+"_down",ratetype+"_0__up",ratetype+"_1__up",ratetype+"_0__down",ratetype+"_1__down"])
			#print newhistos
			if NanoF.isdata:
				histos[ratetype+"_up"].update(newhistos[ratetype+"_up"])
				histos[ratetype+"_down"].update(newhistos[ratetype+"_down"])
				histos[ratetype+"_0__up"].update(newhistos[ratetype+"_0__up"])
				histos[ratetype+"_0__down"].update(newhistos[ratetype+"_0__down"])
				histos[ratetype+"_1__up"].update(newhistos[ratetype+"_1__up"])
				histos[ratetype+"_1__down"].update(newhistos[ratetype+"_1__down"])
			histos[ratetype+"_0"].update(newhistos[ratetype+"_0"])
			histos[ratetype+"_1"].update(newhistos[ratetype+"_1"])

		#for mass faking
		masshist = ratefile.Get("masshist")


	print "Start Looping..."
	counts = 0

	sttime=time.time()


	#Compute minimums for skimming
	minpt = 9999999.
	minptak4 = 9999999.
	minsdm = 9999999.
	for region in regions:
		LCR = (NanoF.LoadCuts)[region]
		for akl in ak8labs:
			minpt=min(minpt,LCR["ptAK8__"+akl])

		if "B" in ak4labs:
			minptak4=min(minptak4,LCR["pt__B"])
		
		if "msoftdropdef__"+ak8labs[0] in LCR:
			sdm0=LCR["msoftdropdef__"+ak8labs[0]][0]
		else:
			sdm0=LCR["msoftdrop__"+ak8labs[0]][0]
		if "msoftdropdef__"+ak8labs[1] in LCR:
			sdm1=LCR["msoftdropdef__"+ak8labs[1]][0]
		else:
			sdm1=LCR["msoftdrop__"+ak8labs[1]][0]
		minsdm=min(minsdm,max(sdm0,sdm1))


	print "min pt, softdrop mass for triggering",minpt,minsdm
	print "min pt ak4",minptak4
	#print "PRINTPRINT"
	#print "1"
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
		errnames.append("ps")
		if settype=="Signal" or settype=="ST":
			errnames.append("pdfweight")
		if settype=="TT" and runttweight:
			errnames.append("tptrw")
		if options.prefire:
			errnames.append("prefire")
		if doshifts:
			shiftnames = ["jes","jer","jmr","jms"]
			shiftuncert=["","jes__up","jes__down","jer__up","jer__down","jmr__up","jmr__down","jms__up","jms__down"]
	#print "2"

	weightshistos=[]
	if macro=="Ana" and (not NanoF.isdata):
		for errname in errnames:
			#print errname
			weightstoplot.append(errname+"sf")
			weightstoplot.append(errname+"up")
			weightstoplot.append(errname+"down")
		weightshistos = NanoF.WeightsHistosInit(weightstoplot,["C"])
	#print "3"
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
	#print "4"
	#Just updates mass measurement
	if options.ttonly and options.anatype=="tHb":
		regions=["FT","FTR"]
		rateregions=["FTR"]


	print "Loading Files..."
	#Return all sorted files 
	allfiles = NanoF.LoadFiles(setname,options.folder,options.redir,options.search)
	isdata=NanoF.isdata
	#print "5"

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
	
		Allcount = int(df.Count())
		print Allcount

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
				"nCustomAK8Puppi>=2",
				"CustomAK8Puppi_pt[1]>"+ak8ptval,
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
							#print (NanoF.LoadCuts)[region][cut]
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




		##TOFLIP
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
				"LHEPdfWeight",
				"LHEWeight_originalXWGTUP"
				]
			if settype=="ST":
				branchesmc +=["nPSWeight","PSWeight"]
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
	print "Total events from file",Allcount
	print "Total events",totnev
	#Dictionary of weights, init on event
	resetweightdict={}
	for region in regions:
		resetweightdict[region]={}
		for errname in errnames:
			resetweightdict[region][errname]={"sf":1.0,"down":1.0,"up":1.0}
	resetweightdict[region]["setweight"]={"sf":1.0}
	if (not NanoF.isdata) and (not genwoff):
		resetweightdict[region]["genweight"]={"sf":1.0}
	if macro=="Ana":
		resetweightdict[region]["bkgweight"]={"sf":1.0}

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
	evhistos["NM1TiMDtophigheta"] = copy.deepcopy(histos["NM1TiMDtop"]["iMDtop__T__NM1TiMDtop"])
	evhistos["NM1TiMDtophigheta"].SetName("iMDtop__T__NM1TiMDtophigheta")
	evhistos["NM1TiMDtophigheta"].SetTitle("iMDtop__T__NM1TiMDtophigheta")
	cfregions=["C","NM2bt"]

	cutflowpoints=	[
			"presel",
			"presel_kin",
			"presel_kin_vtag",
			"presel_kin_vtag_ttag",
			"presel_kin_vtag_ttag_DR",
			"presel_kin_vtag_ttag_DR_btag"
			]
	fullcutflow={}	


	cutflowpointsfull=["total","prepresel"]
	cutflowpointsfull+=cutflowpoints

	for cfregion in cfregions:
		fullcutflow[cfregion]={}
		for cf in cutflowpointsfull:
			if cf=="total":
				if NanoF.isdata:
					fullcutflow[cfregion][cf]=1
				else:
					fullcutflow[cfregion][cf]=int(nev_xsec[0])
			elif cf=="prepresel":
				fullcutflow[cfregion][cf]=int(Allcount)
			else:
				fullcutflow[cfregion][cf]=0
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
		evcutflow={None}

		ntotdc=0
		for iev in xrange(nent):
			if evcutflow!={None}:
				for cfregion in cfregions:
					for cf in cutflowpoints:
						fullcutflow[cfregion][cf]+=evcutflow[cfregion][cf]
			evcutflow={}	
			#for region in regions:
			#	for cf in cutflowpoints:
			#		print region,cf,fullcutflow[region][cf]

			for cfregion in cfregions:
				evcutflow[cfregion]={}
				for cf in cutflowpoints:
					evcutflow[cfregion][cf]=0


			genpart,genweight,genjet,pdfweights,q2weights=None,None,None,None,None
			counts+=1
			for cfregion in cfregions:
				evcutflow[cfregion]["presel"]=1
			try:
				ev=itertree.next()
			except:
				print "EV ERR!"
				continue
		
			if counts%10000==0:
				avetime=time.time()-stevtime
				tpev=0.0
				if iev>0:
					tpev=1000.*(avetime)/float(iev)
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
					for cfregion in cfregions:
						for cf in cutflowpoints:
							print region,cf,fullcutflow[cfregion][cf]
							
			#Debugging run
			#if counts>3000:
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






			##TOFLIP
			#if regstorun==[]:
			#	continue










			#Initialize Event objects
			ak8jetsFF=NanoF.ExpandGeneric(ev,"CustomAK8Puppi",maxlen=3)
			ak4jetsFF=NanoF.ExpandGeneric(ev,"Jet")
			ak8subjetsFF=NanoF.ExpandGeneric(ev,"CustomAK8PuppiSubJet")


			#Makes .msoftdrop -> .msoftdropcorr
			jets_msoftdrop_raw,jets_msoftdrop_nom=NanoF.CorrectSdMass(ak8jetsFF,ak8subjetsFF )

			#print jets_msoftdrop_raw
			#print ak8jetsFF
                        for iak8 in xrange(len(ak8jetsFF)):
				ak8jetsFF[iak8].umsoftdrop=jets_msoftdrop_nom[iak8]
				ak8jetsFF[iak8].msoftdrop=jets_msoftdrop_nom[iak8]

			#MC stuff
			if not NanoF.isdata:
				CustomGenJetAK8FF=NanoF.ExpandGeneric(ev,"CustomGenJetAK8",maxlen=-1)
				CustomGenJetAK4FF=NanoF.ExpandGeneric(ev,"GenJet",maxlen=-1)
				nTrueInt = getattr(ev, "Pileup_nTrueInt")

			rho = getattr(ev, "fixedGridRhoFastjetAll")
			eventnumber = getattr(ev, "event")

			PV_npvs = getattr(ev, "PV_npvs")

			evhistos["PV_npvs_pre"].Fill(PV_npvs)

			if (not NanoF.isdata):

				
				evpuweight= NanoF.PuWeight(float(nTrueInt))
				evhistos["PV_npvs_post"].Fill(float(PV_npvs),evpuweight["sf"])
				evhistos["PV_npvs_postup"].Fill(float(PV_npvs),evpuweight["up"])
				evhistos["PV_npvs_postdown"].Fill(float(PV_npvs),evpuweight["down"])
				if settype=="Signal" or settype=="ST":
					pdfweights=[]
					#tempth1=TH1F("tempth1",	"tempth1",		10000, -1.0,5.0 )
					allpdfs = getattr(ev, "LHEPdfWeight")
					#print "ORIG",getattr(ev, "LHEWeight_originalXWGTUP")
					#print len(allpdfs)
					#for cpdf in allpdfs:
					#	print cpdf
					opdf=allpdfs[0]
					for ipdf in range(1,min(len(allpdfs)-2,101)):

						
						pdfweights.append(allpdfs[ipdf])
						#print ipdf,pdfweights[-1]
					#	tempth1.Fill(float(getattr(ev, "LHEPdfWeight")[ipdf]))
						#print ipdf,pdfweights[-1]
					avew=sum(pdfweights)/len(pdfweights)
					
					alphas=[allpdfs[len(allpdfs)-2],allpdfs[len(allpdfs)-1]]

					#print "alphas",alphas,avew
					if settype=="Signal":
						evpdfweight=NanoF.PdfWeight(pdfweights)
					if settype=="ST":
						evpdfweight=NanoF.PdfWeightHessian(pdfweights,opdf)
						
				
					alsigdown=abs(avew-min(alphas))/avew
					alsigup=abs(avew-max(alphas))/avew
	
					pdfsigdown=abs(1.0-evpdfweight["down"])
					pdfsigup=abs(1.0-evpdfweight["up"])
					#print "pdfwuppre", evpdfweight["up"]
					#print "pdfwdownpre", evpdfweight["down"]
					#print "al", alphas

					evpdfweight["up"]=1.0+sqrt(pdfsigup*pdfsigup+alsigup*alsigup)
					evpdfweight["down"]=1.0-sqrt(pdfsigdown*pdfsigdown+alsigdown*alsigdown)
					#print "up",evpdfweight["up"],pdfsigup,alsigup
					#print "down",evpdfweight["down"],pdfsigdown,alsigdown
					#print "pdfwuppost", evpdfweight["up"]
					#print "pdfwdownpost", evpdfweight["down"]

					#print evpdfweight
					#print tempth1.Integral(),tempth1.GetRMS(),evpdfweight

					evhistos["pdfuncevup"].Fill(evpdfweight["up"])
					evhistos["pdfuncevdown"].Fill(evpdfweight["down"])

					q2weights=[]
					if settype=="Signal":
						q2indices=[0,5,15,24,34,39]
					if settype=="ST":
						q2indices=[0,1,3,5,7,8]
					for iq2 in q2indices:

						q2weights.append(float(getattr(ev, "LHEScaleWeight")[iq2]))
						#print iq2,q2weights[-1]
					evq2weights = NanoF.Q2Weight(q2weights)
					if settype=="ST":
						allps = getattr(ev, "PSWeight")
						evpsweights = NanoF.PSWeight(allps)
						#print "evpsweights",evpsweights

			#print PV_npvs

			#Event MET filters 
			filtp=NanoF.FilterPass(ev)
			if not filtp:
				continue
			if options.hemtest:
				
				for iak8 in xrange(len(ak8jetsFF)):
					tempsc=NanoF.JesScaleHEM(ak8jetsFF[iak8])
					
					ak8jetsFF[iak8].pt*=tempsc
					ak8jetsFF[iak8].mass*=tempsc
					ak8jetsFF[iak8].msoftdrop*=tempsc
					ak8jetsFF[iak8].msoftdropdef*=tempsc
				for iak4 in xrange(len(ak4jetsFF)):
					tempsc=NanoF.JesScaleHEM(ak4jetsFF[iak4])
					ak4jetsFF[iak4].pt*=tempsc
					ak4jetsFF[iak4].mass*=tempsc
				
			
										
		
			for shift in shiftuncert:
				#print shift
				#Tie all rng to event number
				NanoF.rnd1.SetSeed(eventnumber)
				NanoF.rnd2.SetSeed(eventnumber)
				random.seed(eventnumber)
			

				#method1
				for cjet in ak8jetsFF:
					cjet.reset()
				for cjet in ak4jetsFF:
					cjet.reset()
				for cjet in ak8subjetsFF:
					cjet.reset()
				
				ak8jets=ak8jetsFF
				ak4jets=ak4jetsFF
				ak8subjets=ak8subjetsFF

				#method2
				#ak8jets=copy.deepcopy(ak8jetsFF)
				#ak4jets=copy.deepcopy(ak4jetsFF)
				#ak8subjets=copy.deepcopy(ak8subjetsFF)

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
				#Only do nominal corrections for 2018.  Note, shifts are in series...might need to check inputs
				if True:
					for ak8j in ak8jets:
						(jet_pt, jet_mass) = recal.correct(ak8j,rho,delta=delta)
						shfac=jet_pt/ak8j.pt
						#ak8j.pt = jet_pt
						#ak8j.mass = jet_mass
						#ak8j.setp4()
						ak8j.setshift(shfac)


					for ak4j in ak4jets:
						(jet_pt, jet_mass) = recalak4.correct(ak4j,rho,delta=delta)
						shfac=jet_pt/ak4j.pt
						#print "ptm"
						#print jet_pt/ak4j.pt
						#print jet_mass/ak4j.mass
						#ak4j.pt = jet_pt
						#ak4j.mass = jet_mass
						#ak4j.setp4()
						ak4j.setshift(shfac)

					for subj in ak8subjets:
						(jet_pt, jet_mass) = recalak4puppi.correct(subj,rho,delta=delta)
						shfac=jet_pt/subj.pt
						#subj.pt = jet_pt
						#subj.mass = jet_mass
						#subj.setp4()
						subj.setshift(shfac)

				#jets_msoftdropdef_nom=NanoF.CorrectSdMassdef(ak8jets,ak8subjets)
				#for iak8,ak8j in enumerate(ak8jets):
     				#	ak8j.msoftdropdef=jets_msoftdropdef_nom[iak8]

				jets_msoftdropdef_nom=NanoF.CorrectSdMassdef(ak8jets,ak8subjets)
				for iak8,ak8j in enumerate(ak8jets):
     					ak8j.msoftdropdef=jets_msoftdropdef_nom[iak8]

				if not NanoF.isdata:

					CustomGenJetAK8=CustomGenJetAK8FF
					CustomGenJetAK4=CustomGenJetAK4FF

					jind=0
					if (shtype=="jer") and (shstr=="up"):
						jind=2
					if (shtype=="jer") and (shstr=="down"):
						jind=1
					NanoF.JerSmear(ak8jets, CustomGenJetAK8,rho,jind,jtype="ak8")
					NanoF.JerSmear(ak4jets, CustomGenJetAK4,rho,jind,jtype="ak4")
					NanoF.JerSmearstoc(ak8subjets,rho,jind,jtype="ak4")
					jmsind=0
					if (shtype=="jms") and (shstr=="up"):
						jmsind=2
					if (shtype=="jms") and (shstr=="down"):
						jmsind=1
					NanoF.JmsScale(ak8jets,jmsind)

					jmind=0
					if (shtype=="jmr") and (shstr=="up"):
						jmind=2
					if (shtype=="jmr") and (shstr=="down"):
						jmind=1
					NanoF.JmrSmear(ak8jets,jmind)


				if ak8jets[1].pt<minpt:
					continue

				htval = 0
				for ak4jet in ak4jets:
					if ak4jet.p4.Perp()<30.0:
						continue
					htval += ak4jet.p4.Perp()

				#Shouldn't hardcode
				if njetinv==2:
					if abs(ak8jets[0].p4.Rapidity()-ak8jets[1].p4.Rapidity())>1.8:
						continue


				if htval<1000.:
					continue
				for cfregion in cfregions:
					if shift=="":
						evcutflow[cfregion]["presel_kin"]=1
				#Loop over passed regions
				weightdict={}
				#print "presel_kin",regstorun
				#for ak8jet in ak8jets:
				#	print ak8jet.pt



				##TOFLIP
				#for region in regstorun:
				for region in regions:
	






					#Dont run shifts for bkg regions 
					if (shift!="") and not (region in FSregions):
						continue

					weightdict[region] = resetweightdict[region]
					weightdict[region]["setweight"] = {"sf":setweight}


					tags = {}
					for ak8lab in ak8labs:
						tags[ak8lab]=[]

					#For trimmass triggers
					maxsdmass=0.0

					nhpt=0

					#Create tags
					ijet=0
					for ak8jet in ak8jets:
						maxsdmass=max(maxsdmass,ak8jet.msoftdrop)
						if ijet>njetinv-1:
							break
						
						if abs(ak8jet.p4.Eta())<2.4:
							ak8jet.index=ijet
							for tag in tags:
								ptcut=(NanoF.LoadCuts)[region]["ptAK8__"+tag]
								#print tag,ptcut
								if ak8jet.p4.Perp()>ptcut :
									nhpt+=1
									if NanoF.TagJet(ak8jet,tag,region.split("__")[0]):
										tags[tag].append(ijet)
						ijet+=1
					#print "pre presel_kin_vtag", tags, nhpt

					if len(tags[probl])==0:
						continue
					if shift=="" and (region in cfregions):
						evcutflow[region]["presel_kin_vtag"]=1
					#For double counting
					nfills=0

					#Loop over found probes.  In the case of overlap this allows multiple probabilistic entries 
					#(Not currently implemented)


					if options.prefire:
						if (options.era!="2018"):
							weightdict[region]["prefire"]["sf"]=float(getattr(ev, "L1PreFiringWeight_Nom"))
							weightdict[region]["prefire"]["up"]=float(getattr(ev, "L1PreFiringWeight_Up"))
							weightdict[region]["prefire"]["down"]=float(getattr(ev, "L1PreFiringWeight_Dn"))
					ovrl=len(list(set(tags[probl]) & set(tags[candl])) )>0 and (len(tags[probl])+len(tags[candl])>2) and (region=="C")
					#if ovrl:
					#	print "pbl",tags[probl]
					#	print "tbl",tags[candl]
					#	print list(set(tags[probl]) & set(tags[candl])) 
					#	print



					for i in xrange(len(tags[probl])):
						cands = {}
						for lab in labels:
							cands[lab]=None
						iprobe = tags[probl][i]

						#For 2jet, the candidate is always the other one
						if njetinv==2:
							icandidate = 1-tags[probl][i]

						#For 3jet, if multiple cands choose at random
						if njetinv==3:
							tempcands = copy.deepcopy(tags[candl])
							if tags[probl][i] in tempcands:
								tempcands.remove(tags[probl][i])
							if len(tempcands)>1:
								random.shuffle(tempcands)
							if len(tempcands)>0:
								icandidate = tempcands[0]
							else:
								continue


						#Now 1 probe, 1 cand
						if len(tags[candl])>0:
							if icandidate in tags[candl]:
								cands[candl]=ak8jets[icandidate]
						cands[probl]=ak8jets[iprobe]

						#For lead, sublead param
						iorder=0
						if icandidate>iprobe:
							iorder=1


						if cands[probl]==None or cands[candl]==None:
							continue
						if shift=="" and (region in cfregions):
							evcutflow[region]["presel_kin_vtag_ttag"]=1
						#if ovrl:
							#print "cpbl",iprobe
							#print "ctbl",icandidate
							#iovr+=1
							#print float(iovr)/float(iovr+inover)
						#elif region=="C":
						#	inover+=1
						#Make sure no proxy correlation
						if cands[probl].p4.DeltaR(cands[candl].p4)<1.6:
							continue
						if shift=="" and (region in cfregions):
							evcutflow[region]["presel_kin_vtag_ttag_DR"]=1
						#Fake the mass for mass-correlated tagged object 
						if macro=="Ana":
							if (region in rateregions) and (options.anatype=="tHb" or options.anatype=="tZb"):
								fakemass = masshist.GetRandom()
								cands[candl].p4.SetPtEtaPhiM(cands[candl].pt,cands[candl].eta,cands[candl].phi,fakemass)
								cands[candl].mass = fakemass

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
							if (cands[candl].p4.DeltaR(ak4jet.p4)>1.2 and cands[probl].p4.DeltaR(ak4jet.p4)>1.2):
								htvalrem += ak4jet.p4.Perp()
								njetsrem += 1


						#Check for AK4 tag
						foundall=True
						tries=0

						for lab in labels:
							if len(lab)==1 and not (lab in [probl,candl]):
								if lab in ak4labs:
									ptcutAK4=(NanoF.LoadCuts)[region]["pt__"+lab]
									iak4jet=0
									for ak4jet in ak4jets:
										if ak4jet.p4.Perp()>ptcutAK4 and abs(ak4jet.p4.Eta())<2.4:
											if ak4jet.p4.DeltaR(cands[probl].p4)>1.2 and ak4jet.p4.DeltaR(cands[candl].p4)>1.2:
												tries+=1
												if NanoF.TagJet(ak4jet,lab,region.split("__")[0]):
													ak4jet.index=iak4jet
													cands[lab]=ak4jet
												break
										iak4jet+=1
									if cands[lab]==None:
										foundall=False
			
						#print evcutflow
						if not foundall:
							continue
						if shift=="" and (region in cfregions):
							evcutflow[region]["presel_kin_vtag_ttag_DR_btag"]=1

						globalb+=1
						if tries!=1 and trijet:
							globalbsub+=1
							print  float(globalbsub)/float(globalb)
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
						if threecand!=None:
						#	print cands
						#	print vpairs[0],cands[vpairs[0]]
						#	print vpairs[1],cands[vpairs[1]]
							#print cands
							maxvlq=max(cands[vpairs[0]].mass,cands[vpairs[1]].mass)
							cands[threecand].maxvlq=maxvlq
							if "maxvlq__"+threecand in (NanoF.LoadCuts)[region]:
								maxvcut=(NanoF.LoadCuts)[region]["maxvlq__"+threecand]
								if not (maxvcut[0]<cands[threecand].maxvlq<=maxvcut[1]):
									#print region,cands[threecand].maxvlq,"continue"
									continue
							#if [threecand].maxvlq
						#Htcut, should not be hardcoded?

						if (not NanoF.isdata):
							if genjet==None:
								genjet = NanoF.ExpandGeneric(ev,"GenJet",10,ptcut=0.0)
							if genpart==None:
								genpart = NanoF.ExpandGeneric(ev,"GenPart",50,ptcut=0.0)
							
							if (not genwoff):
								if genweight==None:
									genweight = float(getattr(ev, "genWeight"))

								weightdict[region]["genweight"] = {"sf":genweight}
								

							if settype=="TT" and runttweight:
								weightdict[region]["tptrw"] = NanoF.Tptrw(genpart)


							#MC gen weights
							if settype=="Signal" or settype=="ST":

							
								weightdict[region]["q2"] = evq2weights

								weightdict[region]["pdfweight"] = evpdfweight
								#print weightdict[region]["pdfweight"]
								if settype=="ST":
									weightdict[region]["ps"] = evpsweights

							#Trigger weighting
							if (not options.trigemu):
								weightdict[region]["trig"] = NanoF.TriggerWeight(htval,maxsdmass)

							#PU weighting
							weightdict[region]["pu"] = evpuweight
							
							#This checks if a region has the nominal tag to apply the sf, otherwise dont. Should not be hardcoded  
							#Careful, B is different
							if "B" in ak4labs:
								hadfl=NanoF.GenMatchAK4(cands["B"],genjet)
								if not (region in ["M","N","O","Z","NM1BbtagDeepFlavB","FT","FTR"]):
									weightdict[region]["btag"],weightdict[region]["bmistag"] = NanoF.BTagSf(cands["B"],"T",hadfl)
									#print weightdict[region]["btag"],weightdict[region]["bmistag"] ,hadfl
								else:
									weightdict[region]["btag"],weightdict[region]["bmistag"] = NanoF.BTagSf(cands["B"],"L",hadfl)
							if "H" in ak8labs:
								hgenm=NanoF.GenMatchAK8(cands["H"],genpart)
								
								if (region in ["C","CH","CL","D","DFM","K","L","N","O","NM1Tmsoftdropdef","NM1TiMDtop","NM1Hmsoftdrop","NM1BbtagDeepFlavB"]):
									weightdict[region]["htag"],weightdict[region]["hmistag"] = NanoF.HTagSf(cands["H"],"T",hgenm)
									#print hgenm,weightdict[region]["htag"],weightdict[region]["hmistag"]
								else:
									weightdict[region]["htag"],weightdict[region]["hmistag"] = NanoF.HTagSf(cands["H"],"L",hgenm)
									#if hgenm== "T":
									#	print "looseH",region,weightdict[region]["htag"],weightdict[region]["hmistag"]
							if "Z" in ak8labs:
								if (region in ["C","CH","CL","D","DFM","K","L","N","O","NM1Tmsoftdropdef","NM1TiMDtop","NM1Zmsoftdrop","NM1BbtagDeepFlavB"]):
									weightdict[region]["wtag"] = NanoF.WTagSf(cands["Z"],"T")
									weightdict[region]["extrap"] = NanoF.Extrap(cands["Z"],"T")
									
								else:
									weightdict[region]["wtag"] = NanoF.WTagSf(cands["Z"],"L")
									weightdict[region]["extrap"] = NanoF.Extrap(cands["Z"],"L")
									#print "looseZ",region,weightdict[region]["wtag"],weightdict[region]["extrap"]
							if "T" in ak8labs:
								if (region in ["B","C","CH","CL","H","M","N","FT","NM1Tmsoftdropdef","NM1HbtagHbb","NM1Hmsoftdrop","NM1BbtagDeepFlavB","NM1Zmsoftdrop","NM1Ztau21"]):
									weightdict[region]["ttag"] = NanoF.TopTagSf(cands["T"],"T")
								else:
									weightdict[region]["ttag"] = NanoF.TopTagSf(cands["T"],"L")
									#print "loosetop",region,weightdict[region]["ttag"]
								if (region in ["FT","FTR"]):
									tempttag = NanoF.TopTagSf(cands["H"],"T")
									weightdict[region]["ttag"]["sf"]*=tempttag["sf"]
									weightdict[region]["ttag"]["up"]*=tempttag["up"]
									weightdict[region]["ttag"]["down"]*=tempttag["down"]

						#A bit hacky, plotting is performed using dictionaries instead of object class 
						plotdict = NanoF.CandToDict(cands)
						bkgweight=1.0

						#If the region is a background estimate region, apply the TF




						if macro=="Ana" and (region in rateregions):
							for bkgw in bkgweights:
						
								if len(bkgw)>0:
									if bkgw[-1] in ["0","1"]:
										tagindex = int(bkgw[-1])
										#print bkgw,tagindex,icandidate
										if iorder!=tagindex:
											continue


								etabin=ratehist[region].GetYaxis().FindBin(abs(cands[candl].eta))
								#print "BINLOWEDGE",ratehist[region].GetYaxis().GetBinLowEdge(etabin)
								#print "BINUPEDGE",ratehist[region].GetYaxis().GetBinLowEdge(etabin)+ratehist[region].GetYaxis().GetBinWidth(etabin)
								for binstr in binstrs:
									plotdict[candl][binstr]=None
								curratehisto = ratehistos[region+bkgw.replace("__err","")]
								if etabin<len(curratehisto):

									ptbin=curratehisto[etabin].FindBin(cands[candl].pt)
									if bkgw.find('err')!=-1:
					
										tempbin=ptbin
										bkgweight = curratehisto[etabin].GetBinError(tempbin)	
		
										while bkgweight<10e-8:
											if tempbin<0:
												break
											
											bkgweight = curratehisto[etabin].GetBinError(tempbin)
											tempbin-=1
											if region in ["D","L","I","G","O"]:
												logging.warning("emptybin err "+str(cands[candl].pt))
												print tempbin,bkgweight,region+bkgw.replace("__err",""),etabin,curratehisto

									else:
										tempbin=ptbin	
										bkgweight = curratehisto[etabin].GetBinContent(ptbin)
										#print bkgweight,cands[candl].pt,cands[candl].eta
										while bkgweight<10e-8:
											if tempbin<0:
												break
											 
											bkgweight = curratehisto[etabin].GetBinContent(ptbin)
											tempbin-=1
											if region in ["D","L","I","G","O"]:
												logging.warning("emptybin "+str(cands[candl].pt))
												print tempbin,bkgweight,region+bkgw.replace("__err",""),etabin,curratehisto
									plotdict[candl]["bbin"+str(etabin)]=ptbin
								weightdict[region]["bkgweight"]={"sf":bkgweight}
								bkgstr=region

								if bkgw!="":
									bkgstr += bkgw
								hweight=1.0
								
								for ww in weightdict[region]:
									#print region,ww,bkgw,weightdict[region][ww]["sf"],cands[candl].pt,abs(cands[candl].eta)
									hweight*=weightdict[region][ww]["sf"]

								NanoF.HistosFill(histostoplot,plotdict,bkgstr,hweight)
								if (not NanoF.isdata):
									NanoF.WeightsHistosFill(weightshistos,weightdict,region)
						else:
							#Filling jetnum histos

							if macro=="Bkg":
								hweight=1.0
								for ww in weightdict[region]:
									hweight*=weightdict[region][ww]["sf"]
								NanoF.HistosFill(histostoplot,plotdict,region+"_"+str(iorder),hweight)


							if (macro=="Ana" and region!="FT" and (region in anaregions) and nfills!=0):
								#if region=="C" and shift=="":
									#print tags
								#	logging.warning("Ana overlap in C")
								#	ntotdc+=1
									#print "dc",ntotdc
								break

							#if (macro=="Ana" and region!="FT" ):
							#	print htval,weightdict[region]["trig"]
							if region =="C" and (shift==""):
								allCevs.append(eventnumber)
								#print "newc"
								#print len(allCevs)
								#print fullcutflow[region]["presel_kin_vtag_ttag_DR_btag"]+1
								#print "C"
								#print allCevs[-1]
								#print evpsweights
								#NanoF.GenMatchB(cands["B"],genpart)
								#print weightdict[region]["genweight"]
							#if region =="N" and (shift==""):
							#	print "N"

							hweight=1.0
							for ww in weightdict[region]:
									#print region,hweight,shift,ww
									#print weightdict[region][ww]["sf"]
									hweight*=weightdict[region][ww]["sf"]
									#if region=="C":
									#	print region,hweight,shift,ww,weightdict[region][ww]["sf"]
										#print ""
							if (region=="NM1TiMDtop"):
								if (abs(cands["T"].eta)>2.0):
									#print(cands["T"].eta)
									evhistos["NM1TiMDtophigheta"].Fill(cands["T"].iMDtop,hweight)
									cetbins=[evhistos["NM1TiMDtophigheta"].FindBin(0.9),evhistos["NM1TiMDtophigheta"].FindBin(1.0)]
									print 	
									print evhistos["NM1TiMDtophigheta"].GetEntries(),evhistos["NM1TiMDtophigheta"].Integral(cetbins[0],cetbins[1]),evhistos["NM1TiMDtophigheta"].Integral(),evhistos["NM1TiMDtophigheta"].Integral(cetbins[0],cetbins[1])/evhistos["NM1TiMDtophigheta"].Integral()
									print histos["NM1TiMDtop"]["iMDtop__T__NM1TiMDtop"].GetEntries(),histos["NM1TiMDtop"]["iMDtop__T__NM1TiMDtop"].Integral(cetbins[0],cetbins[1])/histos["NM1TiMDtop"]["iMDtop__T__NM1TiMDtop"].Integral()

							#if region=="C":
							#	print"Weight",hweight
							if (NanoF.isdata):
								if hweight!=1.0:
									logging.error("DATA with non-unity weight!!!")

							NanoF.HistosFill(histostoplot,plotdict,region,hweight)
							if (not NanoF.isdata):
								NanoF.WeightsHistosFill(weightshistos,weightdict,region)

							if (shift=="") and (region in FSregions):
								for normerr in errnames:
									#print normerr
									for errval in ["down","up"]:
										hweight=1.0

										for ww in weightdict[region]:
											#if region=="C":
											#	print region,hweight,normerr,shift,ww,weightdict[region][ww]["sf"]
												#print normerr,ww
											if (normerr==ww) and (errval in weightdict[region][ww]):
												#print "weight",errval,weightdict[region][ww][errval]
												hweight*=weightdict[region][ww][errval]
											else:
												hweight*=weightdict[region][ww]["sf"]
										if errval=="up":
											NanoF.HistosFill(uphistos[normerr],plotdict,region,hweight)
										if errval=="down":
											NanoF.HistosFill(downhistos[normerr],plotdict,region,hweight)

							nfills+=1
							#if region=="C":
								#print region,hweight,shift,ww,weightdict[region][ww]["sf"]
								#print ""



	print "Finished Looping..."
	jobstr=""
	if jobarr[1]!=1:
		jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
	output = ROOT.TFile("NanoAODskim_"+options.anatype+macro+options.era+hemstr+prefstr+"__"+setnametowrite+jobstr+".root","recreate")
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
				print "Writing",histo,histo1
				histoset[histo][histo1].Write()

	for rr in fullcutflow:
		evhistos[rr]=TH1F("Cutflow"+rr,	"Cutflow"+rr,		10, -0.5,9.5 )
		for cf in range(0,len(cutflowpointsfull)):
			
			evhistos[rr].SetBinContent(cf+1,fullcutflow[rr][cutflowpointsfull[cf]])
	for evh in evhistos:
		print "Writing evh",evh,evhistos[evh]
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


