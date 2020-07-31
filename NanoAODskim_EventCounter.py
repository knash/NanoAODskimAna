
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

(options, args) = parser.parse_args()
dopdfs=True
di=""
if options.condor:
	di="tardir/"
	dopdfs=False
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
vstr= (options.version).split(",")
NanoF = NanoAODskim_Functions(options.anatype,options.era,vstr,settype,options.condor)



print "Loading Files..."

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
output = ROOT.TFile("NanoAODskim_EV"+options.era+"__"+setnametowrite+".root","recreate")
output.cd()
allgenweight=TH1F("allgenweight",	"allgenweight",		20000, -2000.0,2000.0 )
gwhist=TH1F("gwhist",	"gwhist",		20000, -2000.0,2000.0 )
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
cfiles =ROOT.vector('string')()
for curfilename in files:
		cfiles.push_back(curfilename)

pdavesel = 	'''
		float avepdfweight=0.0;
		for(uint ilw=1;ilw<101;ilw++)	{
			avepdfweight+=LHEPdfWeight[ilw];
						}
		return avepdfweight/=100.0;
		'''
pdsel = 	'''

		float pdfweight;
		for(uint ilw=1;ilw<101;ilw++)	{
			pdfweight+=(LHEPdfWeight[ilw]-LHEPdfAveWeight)*(LHEPdfWeight[ilw]-LHEPdfAveWeight);
						}
		return sqrt(pdfweight/100.0);
		'''
q2selup = 	'''
		float v[] = {LHEScaleWeight[0],LHEScaleWeight[5],LHEScaleWeight[15],LHEScaleWeight[24],LHEScaleWeight[34],LHEScaleWeight[39]}; 
		float* maxq = std::max_element(v, v + 6); 
    		return *maxq-1.0;

		'''
q2seldown = 	'''
		float v[] = {LHEScaleWeight[0],LHEScaleWeight[5],LHEScaleWeight[15],LHEScaleWeight[24],LHEScaleWeight[34],LHEScaleWeight[39]}; 
		float* minq = std::min_element(v, v + 6); 
    		return *minq-1.0;

		'''

asselup = 	'''
		return std::max(LHEPdfWeight[101]-LHEPdfAveWeight,LHEPdfWeight[102]-LHEPdfAveWeight);
		'''

asseldown = 	'''
		return std::min(LHEPdfWeight[101]-LHEPdfAveWeight,LHEPdfWeight[102]-LHEPdfAveWeight);
		'''

df= ROOT.ROOT.RDataFrame("Events",cfiles)
print "pdsel"
df=df.Define("LHEPdfAveWeight",pdavesel)
df=df.Define("LHEPdfEvWeight",pdsel)
print "q2sel"
df=df.Define("LHEQ2EvWeightUp",q2selup)
df=df.Define("LHEQ2EvWeightDown",q2seldown)
print "assel"
df=df.Define("LHEAsEvWeightUp",asselup)
df=df.Define("LHEAsEvWeightDown",asseldown)
print "mean pdsel"
meanuncpdf= df.Mean("LHEPdfEvWeight").GetValue();
print meanuncpdf
print "mean q2sel"
meanuncq2up= df.Mean("LHEQ2EvWeightUp").GetValue();
meanuncq2down= df.Mean("LHEQ2EvWeightDown").GetValue();
print meanuncq2up,meanuncq2down
print "mean assel"
meanuncasup= df.Mean("LHEAsEvWeightUp").GetValue();
meanuncasdown= df.Mean("LHEAsEvWeightDown").GetValue();
print meanuncasup,meanuncasdown
q2fullup=max(meanuncq2up,meanuncq2down)
asfullup=max(meanuncasup,meanuncasdown)
upunc=sqrt(asfullup*asfullup+q2fullup*q2fullup+meanuncpdf*meanuncpdf)

q2fulldown=min(meanuncq2up,meanuncq2down)
asfulldown=min(meanuncasup,meanuncasdown)
downunc=sqrt(asfulldown*asfulldown+q2fulldown*q2fulldown+meanuncpdf*meanuncpdf)
if dopdfs:
	uncfiletowrite = "pdfuncs"+options.era+".txt"
	towrite=[]
	with open(uncfiletowrite, "r") as pdff:
		readl=pdff.readlines()
		found=False
		for ll in readl:
			print ll.split(",")[0]
			if ll.split(",")[0]!=setnametowrite:
				print "skipping"
				towrite.append(ll)

			else:
				found=True
				print "updating",ll.split(",")[1],"to",str(upunc)+","+str(downunc)
				towrite.append(str(setnametowrite)+","+str(upunc)+","+str(downunc)+"\n")
		if (not found):
			print "new entry"
			towrite.append(str(setnametowrite)+","+str(upunc)+","+str(downunc)+"\n")
	towrite
	with open(uncfiletowrite, "w") as pdff:
		found=False
		for ll in sorted(towrite):
			print ll
			pdff.write(ll)

			
#sys.exit()
#filtarr.append(filtarr[-1].Filter(fsel[0]))
#for sel in fsel:
#	filtarr.append(filtarr[-1].Filter(sel))



for curfilename in files:
	try:
		curfile = TFile.Open(curfilename)
		curttree = curfile.Get("Events")
		currun = curfile.Get("Runs")
	except:
		logging.warning("ERROR OPENING FILE")
		continue
	output.cd()
	curttree.Draw("Generator_weight>>gwhist","","goff")
	allgenweight.Add(gwhist)
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


print "Finished Looping..."
print "allgenweightmean",allgenweight.GetMean()
print "proccessed events",allgenweight.Integral()
output.Write()
output.Close()
print "Completed..."

