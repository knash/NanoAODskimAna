import NanoAODskim_Functions	
from NanoAODskim_Functions import *

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

print "Options Summary..."
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""

jobarr = [options.job,options.totaljobs]
if jobarr[0]>jobarr[1]:
	logging.error("Job Number Higher Than Total Jobs")
	sys.exit()
prescale = options.prescale
setname = options.set
setnametowrite=setname.split('/')[0]
print "set name to write",setnametowrite
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True
isQCD=False
if (setname).find('QCD')!=-1:
	isQCD=True
NanoF = NanoAODskim_Functions(options.anatype,options.era,options.search)

if not isdata:
	constdict = NanoF.LoadConstants
	lumi = constdict["lumi"]
	nev_xsec = constdict["dataconst"][setname]
	setweight = lumi*nev_xsec[1]/float(nev_xsec[0])
	print "Using MC weights..."
	print "\t... Using Constants: Lumi =",lumi,"; Xsec =",nev_xsec[1],"; Nevents =",float(nev_xsec[0])

else:
	print "Using data..."
	setweight = 1.0 

print "\t... Weight =",setweight

print "Loading Files..."
allfiles = NanoF.loadfiles(setname,options.folder,options.redir,"")
print "Totfiles",len(allfiles)
files = []
for cfile in xrange(len(allfiles)):
	#print allfiles[cfile]
	if not (options.eventsplitting):
		#print "not eventsplitting!",cfile
		if not (cfile%jobarr[1]==(jobarr[0]-1)):
				#print "skip!",cfile
				continue
	files.append(allfiles[cfile])

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
	#print histos
	for region in regions:
		jetreg =[]
		for ild in xrange(2):
			jetreg.append(region+"_"+str(ild))
		histos.update(NanoF.histosinit(labels,jetreg))

if macro=="Ana":
	if isQCD:
		ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
	elif options.era=="2016":
		print "2016 HACK!!!!!!!"
		ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__QCD.root','open')
	else:
		ratefile=TFile(di+'NanoAODskim_RateMaker__'+options.anatype+options.era+'__JetHT.root','open')
	ratehist = {}
	ratehist["D"]=ratefile.Get('rate')
	ratehist["G"]=ratefile.Get('Erate')
	ratehist["L"]=ratefile.Get('Jrate')
	ratehist["I"]=ratefile.Get('rate')
	ratehist["FTR"]=ratefile.Get('rate')

	regions=["C","K","H","F","FT"]
	rateregions = ["D","L","I","G","FTR"]
	if options.anatype=="tHb" or options.anatype=="tZb":
		ratehist["O"]=ratefile.Get('Mrate')
		regions.append("N")
		rateregions.append("O")
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
					histos[ratetype+exstr]["bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr] =  TH2F("bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr,	"bbin"+str(ybin)+"__"+candl+"__eta__"+lab+"__"+ratetype+exstr,		nxbins, 0,nxbins,60, -3.0,3.0)
		newhistos = NanoF.histosinit(labels,[ratetype+"_0",ratetype+"_1"])
		histos[ratetype+"_0"].update(newhistos[ratetype+"_0"])
		histos[ratetype+"_1"].update(newhistos[ratetype+"_1"])

	#for histo in histos:
	#	for  histo1 in histos[histo]:
	#		print histo1

	masshist = ratefile.Get("masshist")
weightdict = {}
for region in regions:
	weightdict[region] = setweight


branchestokeep = NanoF.branchestokeep




branchestokeepevent = NanoF.branchestokeepevent
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
minpt = 9999999.
minsdm = 9999999.
for region in regions:
	minpt=min(minpt,(NanoF.LoadCuts)[region]["ptAK8"])
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
alltrigs = ["All"]
alltrigs += NanoF.strigs + NanoF.etrigs

histos["TRIG"]={}
for ttr in alltrigs:
	histos["TRIG"]["ht__pretrig__"+ttr]=TH1F("ht__pretrig__"+ttr,"ht__pretrig__"+ttr,200, 500.0,2500.0)
	histos["TRIG"]["ht__posttrig__"+ttr]=TH1F("ht__posttrig__"+ttr,"ht__posttrig__"+ttr,200, 500.0,2500.0)
histos["TRIG"]["ht__msoftdrop__pretrig__All"]=  TH2F("ht__msoftdrop__pretrig__"+ttr,"ht__msoftdrop__pretrig__"+ttr,200, 500.0,2500.0,250, 0.,500.)
histos["TRIG"]["ht__msoftdrop__posttrig__All"]=  TH2F("ht__msoftdrop__posttrig__"+ttr,"ht__msoftdrop__posttrig__"+ttr,200, 500.0,2500.0,250, 0.,500.)
#skipem=True
for curfilename in files:
	#filest = time.time()
	#print "Loading",curfilename.split('/')[-1]
	#print curfilename
	#if curfilename=="root://eoscms.cern.ch:///store/group/phys_b2g/knash/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1_NanoSlimNtuples2018mc_v8/190904_160953/0000/NanoAODSIMv5skim_176.root":
	#	skipem=False
	#if skipem:
	#	continue
	if kill:
		break 
	runver = ""
	if curfilename.find("Run2017B-31Mar2018-v1")!=-1:
		runver="2017B"
	if curfilename.find("Run2017C-31Mar2018-v1")!=-1:
		runver="2017C"
	try:
		#curfile = TFile(curfilename,"open")
		curfile = TFile.Open(curfilename)
		curttree = curfile.Get("Events")
	except:
		logging.warning("ERROR OPENING FILE")
		continue
	
	branchdir = NanoF.ttreeinit(curttree,runver)
	
	#endftime=time.time()
	#timelogger["files"]+=endftime-stftime
	nent = curttree.GetEntries()
	#print "Nentries",nent
	
	itertree = iter(curttree)
	if (options.eventsplitting):
		itertree = itertools.islice(itertree,(jobarr[0]-1),nent,jobarr[1])
	#for tt in itertree:
	for iev in xrange(nent):
		counts+=1


		try:
			itertree.next()
		except:
			print "EV ERR!"
			continue
		#if counts<30000:
		#	continue


		snapdir = copy.copy(branchdir)
		#print "start"
		#curttreeread.Next()
		#stetime=time.time()

		
		cutflow["pre"]["All"]+=1.
		if counts%10000==0:
			print "\t...",counts,"events processed, total time:",NanoF.strf(time.time()-sttime),"sec"
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
		#if counts>120000:
		#	kill=True
		#	break

			
		#print branchdir["event"]
		#print branchdir["event"]
		#print snapdir
		#print "\t1.11"
		if snapdir["CustomAK8Puppi"][0][0]<2:
			continue 
		
		cutflow["pre"]["twoak8"]+=1.
		#print branchdir["CustomAK8Puppi"][1]["pt"][0],branchdir["CustomAK8Puppi"][1]["pt"][1]
		
		if snapdir["CustomAK8Puppi"][1]["pt"][1]<minpt:
			continue
		
		alllight = True
		for iii in xrange(snapdir["CustomAK8Puppi"][0][0]):
			if snapdir["CustomAK8Puppi"][1]["msoftdrop"][iii]>minsdm:
				alllight=False
				break
		
		if alllight:
			#if branchdir["CustomAK8Puppi"][0][0]>2:
			#	for iii in xrange(branchdir["CustomAK8Puppi"][0][0]):
			#		print iii,branchdir["CustomAK8Puppi"][1]["msoftdrop"][iii]
			#	print "All low mass"
			continue
		
		cutflow["pre"]["highpt"]+=1.
		if abs(snapdir["CustomAK8Puppi"][1]["eta"][0])>2.4 or abs(snapdir["CustomAK8Puppi"][1]["eta"][1])>2.4:
			continue
		
		cutflow["pre"]["eta"]+=1.
		try:
			curdictval = NanoF.eventinit(snapdir)
		except:
			print "ERROR"
			continue 

		


		#print curdictval["CustomAK8Puppi"]
		#continue
		#endetime=time.time()
		#timelogger["init"]+=endetime-stetime
		#stptime=time.time()

		ak8jets = NanoF.physobjinit(curdictval["CustomAK8Puppi"],njetinv)
		
		ak4jets = NanoF.physobjinit(curdictval["Jet"],12)
		htval = 0
		for ak4jet in ak4jets: 
			if ak4jet["TLV"].Perp()<30.0: 
				continue		
			htval += ak4jet["TLV"].Perp()
		if prescale:
			if not (NanoF.TriggerPass(curdictval,True)):
				continue
		#print "pass1"
		histos["TRIG"]["ht__pretrig__All"].Fill(htval)
		histos["TRIG"]["ht__msoftdrop__pretrig__All"].Fill(htval,max(ak8jets[0]["msoftdrop"],ak8jets[1]["msoftdrop"]))
		for hh in NanoF.trigstopass:
			histos["TRIG"]["ht__pretrig__"+hh].Fill(htval)
			if curdictval[hh]:
				histos["TRIG"]["ht__posttrig__"+hh].Fill(htval)
		if not (NanoF.TriggerPass(curdictval)):
			continue
		#print "pass2"
		histos["TRIG"]["ht__posttrig__All"].Fill(htval)
		histos["TRIG"]["ht__msoftdrop__posttrig__All"].Fill(htval,max(ak8jets[0]["msoftdrop"],ak8jets[1]["msoftdrop"]))
		
		muons = NanoF.physobjinit(curdictval["Muon"],4)
		electrons = NanoF.physobjinit(curdictval["Electron"],4)
	
		muveto=False
		for mu in muons:
			#print mu["pt"],mu["mvaId"],mu["highPtId"]
			if mu["pt"]>70 and (mu["mvaId"]>1 or mu["highPtId"]>1):
				muveto=True
		
		if muveto:
			#print "Skip Mu"
			continue

		
		
		elveto=False
		for el in electrons:
			#print el["pt"],el["mvaFall17V2Iso_WP90"]
			#print el["pt"],el["mvaFall17V2Iso_WP90"],el["mvaFall17V2noIso_WP90"]
			if el["pt"]>70 and (el["mvaFall17V2Iso_WP90"]>0 or el["mvaFall17V2noIso_WP90"])>0:
				elveto=True
		if elveto:
			#print "Skip El"
			continue
		#print
		
		#print ak8jets[0]["TLV"].DeltaR(ak8jets[1]["TLV"])
		if ak8jets[0]["TLV"].DeltaR(ak8jets[1]["TLV"])<1.6:
			continue

		cutflow["pre"]["Ak8DR"]+=1.
		if njetinv==2:
			if abs(ak8jets[0]["TLV"].Rapidity()-ak8jets[1]["TLV"].Rapidity())>1.8:
				continue 
		cutflow["pre"]["Ak8Drap"]+=1.
		
		
		for region in regions:

			ptcut=(NanoF.LoadCuts)[region]["ptAK8"]

			tags = {}
			for ak8lab in ak8labs:
				tags[ak8lab]=[]
			ijet=0
			for ak8jet in ak8jets:

				if ijet>njetinv-1:
					break
				#print ijet,njetinv-1
				if ak8jet["TLV"].Perp()<ptcut or abs(ak8jet["TLV"].Eta())>2.4 :
					break
				if ak8jet["tau1"]>0.0:
					ak8jet["tau21"]=ak8jet["tau2"]/ak8jet["tau1"]
				else:
					ak8jet["tau21"]=1.0
				ak8jet["index"]=ijet
				for tag in tags:
					if NanoF.tagjet(ak8jet,tag,region.split("__")[0]):
						#print tag
						tags[tag].append(ijet)

				ijet+=1

			if len(tags[probl])==0:
				continue

			cutflow[region]["noprobl"]+=1.

			if region=="default" and len(tags[probl])>1 and len(tags[candl])>0:
				logging.error("Possible Multiple Entries")
			#print
			nfills=0
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
					if icandidate in tags[candl]:
						cands[candl]= ak8jets[icandidate]

				cands[probl]=ak8jets[iprobe]
				iorder=0
				if icandidate>iprobe:
					iorder=1
				#print "ic",icandidate,iprobe,"io",iorder
				if cands[probl]==None or cands[candl]==None:
					continue
				if cands[probl]["TLV"].DeltaR(cands[candl]["TLV"])<1.6:
					continue
				#print icandidate,iprobe
				cutflow[region]["nocandlandprobl"]+=1.
				if macro=="Ana":
					if (region in rateregions) and (options.anatype=="tHb" or options.anatype=="tZb"):
						fakemass = masshist.GetRandom()
						cands[candl]["TLV"].SetPtEtaPhiM(cands[candl]["pt"],cands[candl]["eta"],cands[candl]["phi"],fakemass)
						cands[candl]["mass"] = fakemass

				njets = 0
				htvalrem = 0
				njetsrem = 0
				for ak4jet in ak4jets: 
					if ak4jet["TLV"].Perp()<30.0: 
						continue
					if njets==0:
						fullevent=ak4jet["TLV"].Perp()
					else:
						fullevent+=ak4jet["TLV"].Perp()			
					njets += 1
					if (cands[candl]["TLV"].DeltaR(ak4jet["TLV"])>1.2 and cands[probl]["TLV"].DeltaR(ak4jet["TLV"])>1.2):
						htvalrem += ak4jet["TLV"].Perp()
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
								if ak4jet["TLV"].Perp()>ptcutAK4 and abs(ak4jet["TLV"].Eta())<2.4:
									if ak4jet["TLV"].DeltaR(cands[probl]["TLV"])>1.2 and ak4jet["TLV"].DeltaR(cands[candl]["TLV"])>1.2:
										if NanoF.tagjet(ak4jet,lab,region.split("__")[0]):							
											ak4jet["index"]=iak4jet
											cands[lab]=ak4jet
											break
							iak4jet+=1
						#print lab,cands[lab]
						if cands[lab]==None:
							foundall=False
				#print cands

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
							
							cands[lab] = NanoF.makeinv(cands,lab)	
							cands[lab]["njets"]=njets
							cands[lab]["htval"]=htval
							cands[lab]["njetsrem"]=njetsrem
							cands[lab]["htvalrem"]=htvalrem
							#print "njets",cands[lab]["njets"]
							#print "htval",cands[lab]["htval"]
							#print "njetsrem",cands[lab]["njetsrem"]
							#print "htvalrem",cands[lab]["htvalrem"]
				#if njetsrem>4:
				#	continue		
							
				bkgweight=1.0


				if options.anatype=="Pho":
					phos = NanoF.physobjinit(curdictval["Photon"],2)
					listtoneg = [probl]
					if len(phos)>0:
						cands[candl]["Piso"] = phos[0]['pfRelIso03_all']
						cands[candl]["PelectronVeto"] = phos[0]['electronVeto']
						cands[candl]["PpixelSeed"] = phos[0]['pixelSeed']
						cands[candl]["PmvaID_WP80"] = phos[0]['mvaID_WP80']
						cands[candl]["PmvaID_WP90"] = phos[0]['mvaID_WP90']


						if 0.0<=cands[candl]["Piso"]<0.04:
							continue

						#if region=='C':
						#	print
						#	print cands[candl]["Piso"]
						#	print cands[candl]["PelectronVeto"]
						#	print cands[candl]["PpixelSeed"]
						#	print cands[candl]["PmvaID_WP80"]
						#	print cands[candl]["PmvaID_WP90"]


					else:
						listtoneg.append(candl)
					for cc in listtoneg:
						for dd in ["Piso","PelectronVeto","PpixelSeed","PmvaID_WP80","PmvaID_WP90"]:
							cands[cc][dd]=-1.

				if htval<1100:
					continue

				cutflow[region]["ht"]+=1.
				ntrigtot+=1


				cutflow[region]["trig"]+=1.
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
								
					
						etabin=ratehist[region].GetYaxis().FindBin(abs(cands[candl]["eta"]))
						for binstr in binstrs:
							cands[candl][binstr]=None	
						curratehisto = ratehistos[region+bkgw.replace("__err","")]
						if etabin<len(curratehisto):
							ptbin=curratehisto[etabin].FindBin(cands[candl]["pt"])
							if bkgw.find('err')!=-1:
								if bkgw== "__err":
									remerr=curratehisto[etabin].GetBinError(ptbin)
								bkgweight = curratehisto[etabin].GetBinError(ptbin)
								
							else:
								if bkgw== "":
									remcont=curratehisto[etabin].GetBinContent(ptbin)
								bkgweight = curratehisto[etabin].GetBinContent(ptbin)
									
							cands[candl]["bbin"+str(etabin)]=ptbin
						#if 
						#	print bkgweight,bkgw,region
						weightdict[region]=setweight*bkgweight
						bkgstr=region
						
						if bkgw!="":
							bkgstr += bkgw
					
						
						NanoF.histosfill(histos,cands,bkgstr,weightdict[region])
					#print remerr/remcont

				else:
					#if cands["P"]["TLV"].Perp()>700:
					#	continue

					weightdict[region]=setweight
					if macro=="Bkg":
						NanoF.histosfill(histos,cands,region+"_"+str(iorder),weightdict[region])
					if isdata:
						if weightdict[region]!=1.0:
							logging.error("DATA with non-unity weight!!!")
					cutflow[region]["Full"]+=1.
					NanoF.histosfill(histos,cands,region,weightdict[region])
					nfills+-1
					if nfills>1 and (region in ["C","K","H","F","N"]):
						print region
						print "Double counting in SR"
						break
					#print "All",cutflow["pre"]["All"]
					#print "twoak8",cutflow["pre"]["twoak8"]
					#print "highpt",cutflow["pre"]["highpt"]
					#print "eta",cutflow["pre"]["eta"]
					#print "Ak8DR",cutflow["pre"]["Ak8DR"]
					#print "Ak8Drap",cutflow["pre"]["Ak8Drap"]
					#for region in ["All","A"]:
					#	print region,"noprobl",cutflow[region]["noprobl"]
					#	print region,"nocandlandprobl",cutflow[region]["nocandlandprobl"]
					#	print region,"ak4tag",cutflow[region]["ak4tag"]
					#	print region,"ht",cutflow[region]["ht"]
					#	print region,"trig",cutflow[region]["trig"]
					#	print region,"Full",cutflow[region]["Full"]
		#print "\tDone!"
print "Finished Looping..."
jobstr=""
if jobarr[1]!=1:
	jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
output = ROOT.TFile("NanoAODskim_"+options.anatype+macro+options.era+"__"+setnametowrite+jobstr+".root","recreate")
output.cd()

for histo in histos:
	for histo1 in histos[histo]:
		histos[histo][histo1].Write()

output.Write()
output.Close()
print "Completed..."

