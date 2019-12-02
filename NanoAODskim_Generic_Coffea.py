import NanoAODskim_Functions_coffea	
from NanoAODskim_Functions_coffea import *
import time
import NanoAODskim_Coffea_Processor
from coffea import hist
from coffea.analysis_objects import JaggedCandidateArray
import coffea.processor as processor
from awkward import JaggedArray
import numpy as np
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

(options, args) = parser.parse_args()

print( "Options Summary...")
print( "==================")
for  opt,value in options.__dict__.items():
	#print( str(option)+ ": " + str(options[option]) 
	print( str(opt) +': '+ str(value))
print( "==================")
print( "")

jobarr = [options.job,options.totaljobs]
if jobarr[0]>jobarr[1]:
	logging.error("Job Number Higher Than Total Jobs")
	sys.exit()
prescale = options.prescale
setname = options.set
setnametowrite=setname.split('/')[0]
print( "set name to write",setnametowrite)
NanoF = NanoAODskim_Functions_Coffea(options.anatype,options.era,options.search)
settype=setfilter(setname)
if not (settype=="JetHT"):
	constdict = NanoF.LoadConstants
	lumi = constdict["lumi"]
	nev_xsec = constdict["dataconst"][setname]
	setweight = lumi*nev_xsec[1]/float(nev_xsec[0])
	print( "Using MC weights...")
	print( "\t... Using Constants: Lumi =",lumi,"; Xsec =",nev_xsec[1],"; Nevents =",float(nev_xsec[0]))

else:
	print( "Using data...")
	setweight = 1.0 

print( "\t... Weight =",setweight)

print( "Loading Files...")
allfiles = NanoF.loadfiles(setname,options.folder,options.redir,"")
print( "Totfiles",len(allfiles))
files = []
for cfile in range(len(allfiles)):
	#print( allfiles[cfile]
	if not (options.eventsplitting):
		#print( "not eventsplitting!",cfile
		if not (cfile%jobarr[1]==(jobarr[0]-1)):
				#print( "skip!",cfile
				continue
	files.append(allfiles[cfile])

#random.shuffle(files)
ntotfile = len(files)
print( "Loaded",ntotfile,"Files...")
print( "Booking Histograms...")

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
		print( "Trijet version")
di=""
if options.condor:
	di="tardir/"
verbose=False
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

	#regions=["A","B","C","D","All"]
	hemispheres = ["0","1"]
	histos = NanoF.histosinit(labels,regions)
	#print( histos
	for region in regions:
		jetreg =[]
		for ild in range(2):
			jetreg.append(region+"_"+str(ild))
		histos.update(NanoF.histosinit(labels,jetreg))
FSregions = {}
if macro=="Ana":
	#if settype=="QCD":
	#	ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
	#elif options.era=="2016":
	#	print( "2016 HACK!!!!!!!"
	#	ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
	#else:
	#	ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__JetHT.root','open')
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
		#print( rname 
		if rname.find("NM1")!=-1:
			#print( "found"
			regions.append(rname)

	#print( regions
	bkgweights=["","__err","_0","__err_0","_1","__err_1"]
	ratephist = ratefile.Get("ratep")
	histofills = copy.deepcopy(regions)
	#for bkgw in bkgweights[1:]:
	#	histofills.append("bkg__"+bkgw)
	histos = NanoF.histosinit(labels,histofills)



	binstrs=[]
	#print( histos 


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
			
			for ybin in range(ratehist[ratetype].GetNbinsY()+1):
				
				if currate=="":
					ratehistos[ratetype].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)))
					nxbins = ratehistos[ratetype][-1].GetNbinsX()+1
				elif currate.find("err")==-1:
					ratehistos[ratetype+exstr].append(ratefile.Get(ratestr+"ratebin__"+str(ybin)+"_"+currate))
					nxbins = ratehistos[ratetype+exstr][-1].GetNbinsX()+1
				else:
					nxbins = ratehistos[ratetype+exstr.replace("__err","")][ybin].GetNbinsX()+1
				#print( nxbins,currate
				binstrs.append("bbin"+str(ybin))
				for lab in labels:	
					#print( "D"+exstr
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
	#		print( histo1

	masshist = ratefile.Get("masshist")



branchestokeep = NanoF.branchestokeep
if (settype!="JetHT"):
	branchestokeep["GenPart"]=	[
					"pt",
					"eta",
					"phi",
					"mass",
					"statusFlags",
					"pdgId"
					]

branchestokeepevent = NanoF.branchestokeepevent
matchmatrix = []


#print( "Calculating Total Events..."
#countstotal=0
#for curfilename in files:
#	curfile = TFile(curfilename,"open")
#	countstotal+=(curfile.Get("Events")).GetEntries()
#print( float(countstotal)/float(300000),"jobs"
#print( "Processing",countstotal,"Events..."


print( "Start Looping...")
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
minpt = 9999999.
minsdm = 9999999.
for region in regions:
	minpt=min(minpt,(NanoF.LoadCuts)[region]["ptAK8"])
	#print( "msoftdrop__"+ak8labs[0]
	#print( (NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[0]]
	#print( region,"msoftdrop__"+ak8labs[0],"msoftdrop__"+ak8labs[1]
	#print( (NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[0]][0],(NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[1]][0]
	minsdm=min(minsdm,max((NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[0]][0],(NanoF.LoadCuts)[region]["msoftdrop__"+ak8labs[1]][0]))
	cutflow[region] = {}
	cutflow[region]["noprobl"]=0.0
	cutflow[region]["nocandlandprobl"]=0.0
	cutflow[region]["ak4tag"]=0.0
	cutflow[region]["ht"]=0.0
	cutflow[region]["trig"]=0.0
	cutflow[region]["Full"]=0.0
print( "min pt, softdrop mass for triggering",minpt,minsdm)
alltrigs = ["All"]
alltrigs += NanoF.strigs + NanoF.etrigs

histos["TRIG"]={}
for ttr in alltrigs:
	histos["TRIG"]["ht__pretrig__"+ttr]=TH1F("ht__pretrig__"+ttr,"ht__pretrig__"+ttr,200, 500.0,2500.0)
	histos["TRIG"]["ht__posttrig__"+ttr]=TH1F("ht__posttrig__"+ttr,"ht__posttrig__"+ttr,200, 500.0,2500.0)
histos["TRIG"]["ht__msoftdrop__pretrig__All"]=  TH2F("ht__msoftdrop__pretrig__"+ttr,"ht__msoftdrop__pretrig__"+ttr,200, 500.0,2500.0,240, 0.,480.)
histos["TRIG"]["ht__msoftdrop__posttrig__All"]=  TH2F("ht__msoftdrop__posttrig__"+ttr,"ht__msoftdrop__posttrig__"+ttr,200, 500.0,2500.0,240, 0.,480.)
#skipem=True


#print( histos
errvals = ["mass","pt","eta"]

errnames = []
if settype=="TT":
	errnames = ["tptrw"]
prehisto = copy.deepcopy(histos)
uphistos={}
downhistos={}
for errname in errnames:
	for errval in errvals:
		for region in FSregions:	
			uphistos[region]={}
			downhistos[region]={}
			for hn in prehisto[region]:
				if (hn.split("__")[0] in errvals) and (isinstance(prehisto[region][hn], TH1F)):
					#print( hn.split("__")[1],len(hn.split("__")[1])
					if (hn.split("__")[0]!="mass") and (len(hn.split("__")[1])>1):
						continue 
					#print( [hn+"__"+errname+"__up"], [hn+"__"+errname+"__down"]
					copyhist = copy.copy(prehisto[region][hn])
					copyhist.SetName(hn+"__"+errname+"__up")
					uphistos[region][hn+"__"+errname+"__up"]=copyhist
					copyhist = copy.copy(prehisto[region][hn])
					copyhist.SetName(hn+"__"+errname+"__down")
					downhistos[region][hn+"__"+errname+"__down"]=copyhist
#print( histos
if options.ttonly and options.anatype=="tHb":
	regions=["FT","FTR"]
	rateregions=["FTR"]

#print( files
output = processor.run_uproot_job({"set":files},
				  treename='Events',
				  processor_instance=FancyDimuonProcessor(),
				  executor=processor.futures_executor,
				  executor_args={'workers': 6, 'flatten': True},
				  chunksize=500000,
				 )
fig, ax, _ = hist.plot1d(output['pt_AK8'], overlay='dataset')

#FatJetpthisto.Draw()

print( "Finished Looping...")
jobstr=""
if jobarr[1]!=1:
	jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
#output = ROOT.TFile("NanoAODskimCOFFEA_"+options.anatype+macro+options.era+"__"+setnametowrite+jobstr+".root","recreate")
#output.cd()
fig.Write()
#output.Write()
#output.Close()
print( "Completed...")

