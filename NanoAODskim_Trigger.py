
from optparse import OptionParser
import subprocess,os,sys

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

di=""
if options.condor:
	di="tardir/"
	subprocess.call( ["mv "+di+"PhysicsTools ./CMSSW_10_2_9/src"], shell=True )
	os.chdir("CMSSW_10_2_9/src")
	subprocess.call( ["scram b"], shell=True )
	subprocess.call( ["scramv1 runtime -sh"], shell=True )
	os.chdir("../../")
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

jobarr = [options.job,options.totaljobs]
if jobarr[0]>jobarr[1]:
	logging.error("Job Number Higher Than Total Jobs")
	sys.exit()
setname = options.set
setnametowrite=setname.split('/')[0]
print "set name",setnametowrite
settype=SetFilter(setname)
print "set type",settype
NanoF = NanoAODskim_Functions(options.anatype,options.era,"v8",settype)




print "Loading Files..."
NanoF.versionstring=[""]
NanoF.nanotype=""

allfiles = NanoF.LoadFiles(setname,options.folder,options.redir,options.search)
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

numf=-1
totev = 0
jobstr=""
if jobarr[1]!=1:
	jobstr += "__job"+str(jobarr[0])+"of"+str(jobarr[1])
output = ROOT.TFile("NanoAODskim_Trig"+options.era+"__"+setnametowrite+jobstr+".root","recreate")
output.cd()
postHT=TH1F("postHT",	"postHT",		200, 0.0,2000.0 )
preHT=TH1F("preHT",	"preHT",		200, 0.0,2000.0 )
curpostHT=TH1F("curpostHT",	"curpostHT",		200, 0.0,2000.0 )
curpreHT=TH1F("curpreHT",	"curpreHT",		200, 0.0,2000.0 )

postHTmass=TH2F("postHTmass",	"postHTmass",		50, 0.0,2000.0,10,0.0,200.0 )
preHTmass=TH2F("preHTmass",	"preHTmass",		50, 0.0,2000.0,10,0.0,200.0)
curpostHTmass=TH2F("curpostHTmass",	"curpostHTmass",		50, 0.0,2000.0,10,0.0,200.0 )
curpreHTmass=TH2F("curpreHTmass",	"curpreHTmass",		50, 0.0,2000.0,10,0.0,200.0 )
#allpdfweight=TH1F("allpdfweight",	"allpdfweight",		400, -4.0,-4.0 )
#pdhist=TH1F("pdhist",	"pdhist",		400, -4.0,-4.0 )
#pdavehist=TH1F("pdavehist",	"pdavehist",		400, -4.0,-4.0 )
#runevents=TH1F("runevents",	"runevents",		1, -0.5,0.5 )
totalgenevents = 0
nweight=0
#pdstr = "sqrt("
#for iii in range(2,102):
#	nweight+=1
#	pdstr+="(LHEPdfWeight["+str(iii)+"]-1.0)*(LHEPdfWeight["+str(iii)+"]-1.0)"
#	if iii<101:
#		pdstr+="+"
#pdstr += "*(1.0/"+str(float(nweight))+"))"
#print pdstr
#Events->Draw("(1.0/100.0)*(LHEPdfWeight*LHEPdfWeight-Sum$(LHEPdfWeight)/Length$(LHEPdfWeight))","Iteration$>2")


for curfilename in files:
	print curfilename
	try:
		curfile = TFile.Open(curfilename)
		curttree = curfile.Get("Events")
		currun = curfile.Get("Runs")
	except:
		logging.warning("ERROR OPENING FILE")
		continue
	runver = ""
	parsename =  curfilename.split("/")
	for pars in parsename:
		if pars.find("Run201")!=-1:
			runver=pars[0:8]
	NanoF.SetRunTrigs(runver)
	
	mutrigs = copy.copy(NanoF.mutrigs)
	prescaletrigstr = ""
	for mut in mutrigs:
		prescaletrigstr+="("+mut+">0)"
		if mut !=mutrigs[-1]:
			prescaletrigstr+="||"
	prescaletrigstr="("+prescaletrigstr+")"
	curtrigs = copy.copy(NanoF.strigs+NanoF.etrigs)
	trigstr = ""
	for curt in curtrigs:
		trigstr+="("+curt+">0)"
		if curt !=curtrigs[-1]:
			trigstr+="||"
	trigstr="("+trigstr+")"

	output.cd()
	kinstr = "(Length$(FatJet_pt)>1)&&(FatJet_pt[1]>400.0)"

	denom= prescaletrigstr+"&&"+kinstr
	num= prescaletrigstr+"&&"+trigstr+"&&"+kinstr
	print "denom",denom
	print "num",num

	curttree.Draw("Sum$(Jet_pt*(Jet_pt>30.0))>>curpreHT",denom,"goff")
	curttree.Draw("Sum$(Jet_pt*(Jet_pt>30.0))>>curpostHT",num,"goff")

	preHT.Add(curpreHT)
	postHT.Add(curpostHT)

	curttree.Draw("(Max$(FatJet_msoftdrop)):(Sum$(Jet_pt*(Jet_pt>30.0)))>>curpreHTmass",denom,"goff")
	curttree.Draw("(Max$(FatJet_msoftdrop)):(Sum$(Jet_pt*(Jet_pt>30.0)))>>curpostHTmass",num,"goff")

	preHTmass.Add(curpreHTmass)
	postHTmass.Add(curpostHTmass)


	#curttree.Draw("LHEPdfWeight>>pdavehist","","goff")
	#curttree.Draw(pdstr+">>pdhist","","goff")
	#print pdhist.GetMean()
	#allpdfweight.Add(pdhist)

	#nentcurrun = currun.GetEntries()
	#itertreerun = iter(currun)
	#for iev in xrange(nentcurrun):

	#	try:
	#		ev=itertreerun.next()
	#	except:
	#		print "EV ERR!"
	#		continue
	#	gencount = float(getattr(ev, "genEventCount"))
	#	totalgenevents+=gencount
	#	runevents.Fill(0.0,gencount)
	#	totev+=gencount
	#break

print "Finished Looping..."
output.Write()
output.Close()
print "Completed..."

