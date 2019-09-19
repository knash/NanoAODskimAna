import NanoAODskim_Functions	
from NanoAODskim_Functions import *

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
                  dest		=	'set',
                  help		=	'data or ttbar')

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
parser.add_option('--condor', metavar='F', action='store_true',
                  default=False,
                  dest='condor',
                  help='submit')

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

setname =options.set

isQCD=False
if (options.set).find("QCD")!=-1:
	isQCD=True
	print "is QCD"

NanoF = NanoAODskim_Functions(options.anatype)
NanoF.branchestokeep["GenPart"]=	[
							"pt",
							"eta",
							"phi",
							"mass",
							"pdgId"
							]
NanoF.truncval = 500

constdict = NanoF.LoadConstants
lumi = constdict["lumi"]
nev_xsec = constdict["dataconst"][options.set]
setweight = lumi*nev_xsec[1]/float(nev_xsec[0])
print "Dataset Weights..."
print "\t... Using Constants: Lumi =",lumi,"; Xsec =",nev_xsec[1],"; Nevents =",float(nev_xsec[0])
print "\t... Weight =",lumi*nev_xsec[1]/float(nev_xsec[0])

print "Loading Files..."
allfiles = NanoF.loadfiles(setname)
files = []
for cfile in xrange(len(allfiles)):
	if not (cfile%jobarr[1]==(jobarr[0]-1)):
			continue
	files.append(allfiles[cfile])
#files =["/eos/cms/store/user/knash/WpToBpT_Wp4000Nar_Bp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8/NanoSlimNtuples_v7/190415_222134/0000/NanoAODskim_9.root"]
files =["/eos/cms/store/user/knash/WpToTpB_Wp4000Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8/NanoSlimNtuples_v7/190412_112830/0000/NanoAODskim_1.root"]
#print files

#random.shuffle(files)
ntotfile = len(files)

print "Loaded",ntotfile,"Files..."

print "Booking Histograms..."

labels = NanoF.labels 
labels = [labels[0],labels[1]]
ak8labs = NanoF.ak8labels
ak4labs =NanoF.ak4labels
candl = NanoF.candl
probl = NanoF.probl
di=""
if options.condor:
	di="tardir/"
regions=["All"]
histosmatch = NanoF.histosmatchinit(labels,regions)

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
ntot=0
npassR=0
npassW=0
npassRtau=0
npassWtau=0
ntotmassW=0
ntotmassR=0

kill=False
#timelogger = {"total":0.0,"files":0.0,"init":0.0,"processing":0.0}
#sttime=time.time()
avemtemp = []
for curfilename in files:
	#stftime=time.time()
	#filest = time.time()
	#print "Loading",curfilename.split('/')[-1]
	if kill:
		break

	curfile = TFile(curfilename,"open")
	curttree = curfile.Get("Events")

	branchdir = NanoF.ttreeinit(curttree)
	#endftime=time.time()
	#timelogger["files"]+=endftime-stftime
	for tt in curttree:
		#stetime=time.time()
		counts+=1
		if counts%10000==0:
			print "\t...",counts,"Events"


		#print counts,counts%jobarr[1],jobarr[0]
		if counts>300000:
			kill=True
			break

		if branchdir["CustomAK8Puppi"][0][0]<2:
			continue 
		#print branchdir["CustomAK8Puppi"][1]["pt"][0],branchdir["CustomAK8Puppi"][1]["pt"][1]
		if branchdir["CustomAK8Puppi"][1]["pt"][1]<400.0:
			continue
		if abs(branchdir["CustomAK8Puppi"][1]["eta"][0])>2.4 or abs(branchdir["CustomAK8Puppi"][1]["eta"][1])>2.4:
			continue

		curdictval = NanoF.eventinit(branchdir)
		#endetime=time.time()
		#timelogger["init"]+=endetime-stetime
		#stptime=time.time()
		ak8jets = NanoF.physobjinit(curdictval["CustomAK8Puppi"],2)
		genpart = NanoF.physobjinit(curdictval["GenPart"],40)
		nWs = 0
		matches = {}
		Ws = []
		allWs = []
		ngps = 0
		nqs,nleps = 0.0,0.0
		allhad=False
		if isQCD:
			inds = [0,1]
			random.shuffle(inds)
			#print inds
			matches[labels[0]]= ak8jets[inds[0]]
			matches[labels[1]]= ak8jets[inds[1]]
		for gp in genpart:
			print gp["pdgId"],gp["mass"],gp["pt"]
			continue
			'''
			if ngps>1:
				if abs(gp["pdgId"])<6:
					nqs+=1
				if 11<=abs(gp["pdgId"])<=18:
					nleps+=1
			if  nqs==6 and nleps==0:
				allhad=True

			
			if abs(gp["pdgId"])==24:
				if nWs==0:
					for  ak8j in ak8jets:
						if ak8j["TLV"].DeltaR(gp["TLV"])<0.6:
							matches["W"]= ak8j
				else:
					if gp["TLV"].DeltaR(allWs[0]["TLV"])<1.0:
						#print "Skipit"
						continue
					Ws.append(gp)
					if nWs==2:
						for ak8j in ak8jets:
							#print "twodrs",ak8j["TLV"].DeltaR(Ws[0]["TLV"]),ak8j["TLV"].DeltaR(Ws[1]["TLV"])
							if (0.001<(ak8j["TLV"].DeltaR(Ws[0]["TLV"])<0.6) and (0.001<ak8j["TLV"].DeltaR(Ws[1]["TLV"])<0.6)):
								matches["F"]= ak8j
				allWs.append(gp)
				nWs+=1
			ngps += 1
		#print len(matches)

		
		if len(matches)==2:
			#print matches["F"]
			#print matches["W"]
			if matches["F"]["TLV"].DeltaR(matches["W"]["TLV"])>1.5 and allhad:
				ntot+=1
				if (65.<matches["W"]["msoftdrop"]<105.):
					ntotmassW+=1
					#print "Wtag",matches["W"]["TLV"].Perp(),float(npassW)/float(ntot),float(npassWtau)/float(ntot)
				if (matches["F"]["msoftdrop"]>105.):
					ntotmassR+=1
					#print "Ftag",float(npassR)/float(ntotmassR),float(npassRtau)/float(ntotmassR)

				if matches["F"]["tau1"]>0.0:
					matches["F"]["tau41"]=matches["F"]["tau4"]/matches["F"]["tau1"]
					matches["F"]["tau21"]=matches["F"]["tau2"]/matches["F"]["tau1"]
					if matches["F"]["tau41"]<0.2 and (matches["F"]["msoftdrop"]>105.):
						npassRtau+=1
				if matches["W"]["tau1"]>0.0:
					matches["W"]["tau41"]=matches["W"]["tau4"]/matches["W"]["tau1"]
					matches["W"]["tau21"]=matches["W"]["tau2"]/matches["W"]["tau1"]
					if matches["W"]["tau21"]<0.4 and (65.<matches["W"]["msoftdrop"]<105.):
						npassWtau+=1
				if matches["F"]["iMDWW"]>0.8 and (matches["F"]["msoftdrop"]>105.):
					npassR+=1
				if matches["W"]["iW"]>0.9 and (65.<matches["W"]["msoftdrop"]<105.):
					npassW+=1
				#print histosmatch
				if (65.<matches["W"]["msoftdrop"]<105.) and (matches["F"]["msoftdrop"]>105.):
					NanoF.histosfill(histosmatch,matches,"All")

				#print
				'''

print "Finished Looping..."


jobstr=""
if jobarr[1]!=1:
	jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
output = ROOT.TFile("NanoAODskim_Match__"+setname+jobstr+".root","recreate")
output.cd()

for histo in histosmatch:
	for histo1 in histosmatch[histo]:

			
		histosmatch[histo][histo1].Write()
		histcumint=copy.deepcopy(histosmatch[histo][histo1])
		lbin = histosmatch[histo][histo1].GetNbinsX()
		for ibin in xrange(lbin):
			if histo1.find("tau")!=-1:
				histcumint.SetBinContent(ibin,histosmatch[histo][histo1].Integral(0,ibin))
			else:
				#print histosmatch[histo][histo1].Integral(ibin,lbin)
				histcumint.SetBinContent(ibin,histosmatch[histo][histo1].Integral(ibin,lbin))
		histcumint.Write(histosmatch[histo][histo1].GetName()+"cumint")
output.Write()
output.Close()
print "Completed..."

