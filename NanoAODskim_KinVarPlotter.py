import NanoAODskim_Functions	
from NanoAODskim_Functions import *

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'QCD',
                  dest		=	'set',
                  help		=	'data or ttbar')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('-w', '--wjets', metavar='F', type='string', action='store',
                  default	=	'Corr',
                  dest		=	'wjets',
                  help		=	'Corr or MC or None')
parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()

setname = options.set
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True


if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True

print "Options Summary..."
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""


setname =options.set
NanoF = NanoAODskim_Functions(options.anatype)
labels = NanoF.labels 
candl = NanoF.candl
probl = NanoF.probl

if isdata:
	datafile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+options.era+"__JetHT.root","open")
else:
	datafile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+options.era+"__QCD.root","open")
QCDfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+options.era+"__QCD.root","open")
ttfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+options.era+"__TT.root","open")
wjetsfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+options.era+"__WJets.root","open")
if options.anatype=="Pho":
	gjetsfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+options.era+"__GJets.root","open")

sigfiles=[]
if options.anatype=="Pho":
	sigfiles=glob.glob("rootfiles/NanoAODskim_PhoAna"+options.era+"__WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2.root")
if options.anatype=="WW":
	sigfiles=glob.glob("rootfiles/NanoAODskim_WWAna"+options.era+"__WkkToWRadionToWWW_M4000-R0-06_TuneCP5_13TeV-madgraph.root")
if options.anatype=="tZb":
	sigfiles=glob.glob("rootfiles/NanoAODskim_tZbAna"+options.era+"__WpToTpB_Wp4000Nar_Tp3000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
if options.anatype=="tHb":
	sigfiles=glob.glob("rootfiles/NanoAODskim_tHbAna"+options.era+"__WpToTpB_Wp4000Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")

sigfs = {}
for sigf in sigfiles:
	sigfs[sigf.split("__")[1].replace(".root","")]=TFile(sigf,"open")
histonames=[]
rebins=[]
ranges=[]
xvals = []
cutvals = []
maxfacs = []

for rname in NanoF.LoadCuts:
	#print rname 
	if rname.find("NM1")!=-1:
		#print "found"
		obj = rname.replace("NM1","")[0]
		if obj=="B":
			continue
		var = rname.replace("NM1","")[1:]
		print "adding",var+"__"+obj+"__"+rname
		histonames.append(var+"__"+obj+"__"+rname)
		if (obj=="W" or obj=="Z")  and var=="msoftdrop":
			rebins.append(2)
			ranges.append([0.0,140.0])
			xvals.append("M_{softdrop}")
			cutvals.append([65.0,105.0])
			maxfacs.append(1.4)
		if obj=="H" and var=="msoftdrop":
			rebins.append(5)
			ranges.append([0.0,200.0])
			xvals.append("M_{softdrop}")
			cutvals.append([105.0,150.0])
			maxfacs.append(1.4)
		if obj=="T" and var=="msoftdrop":
			rebins.append(5)
			ranges.append([0.0,250.0])
			xvals.append("M_{softdrop}")
			cutvals.append([150.0,220.0])
			maxfacs.append(1.4)
		if obj=="F" and var=="msoftdrop":
			rebins.append(10)
			ranges.append([0.0,300.0])
			xvals.append("M_{softdrop}")
			cutvals.append([105.0,-999.0])
			maxfacs.append(1.4)
		if obj=="P" and var=="msoftdrop":
			rebins.append(10)
			ranges.append([0.0,300.0])
			xvals.append("M_{softdrop}")
			cutvals.append([105.0,-999.0])
			maxfacs.append(1.4)
		if (obj=="W" or obj=="Z")  and var=="tau21":
			rebins.append(5)
			ranges.append([0.0,1.0])
			xvals.append("tau_{21}")
			cutvals.append([0.45,-999.0])
			maxfacs.append(2.5)

		if var=="iW":
			rebins.append(1)
			ranges.append([0.0,1.0])
			xvals.append("image_{W}")
			cutvals.append([0.9,-999.0])
			maxfacs.append(1.4)
		if var=="iMDWW":
			rebins.append(100)
			ranges.append([0.0,1.0])
			xvals.append("image_{WW}")
			cutvals.append([0.8,-999.0])
		if var=="iMDtop":
			rebins.append(100)
			ranges.append([0.0,1.0])
			xvals.append("image_{top}")
			cutvals.append([0.6,-999.0])
			maxfacs.append(1.4)
		if var=="iMDPho":
			rebins.append(100)
			ranges.append([0.0,1.0])
			xvals.append("image_{#gammaZ}")
			cutvals.append([0.9,-999.0])
			maxfacs.append(1.4)
		if var=="btagHbb":
			rebins.append(4)
			ranges.append([-1.0,1.0])
			xvals.append("doubleB")
			cutvals.append([0.6,-999.0])
			maxfacs.append(1.4)
for ihn in xrange(len(histonames)):
		curname = histonames[ihn]
		print "plotting",curname
		sighs = {}
		datahist = datafile.Get(curname)
		wjetshist = wjetsfile.Get(curname)
		tthist = ttfile.Get(curname)
		if options.anatype=="Pho":
			gjetshist = gjetsfile.Get(curname)

		for sigf in sigfiles:
			print sigf
			sighs[sigf.split("__")[1].replace(".root","")]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname)
		print curname
		datahist.Rebin(rebins[ihn])			
		tthist.Rebin(rebins[ihn])
		wjetshist.Rebin(rebins[ihn])
		datahist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])			
		tthist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
		wjetshist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
		if options.anatype=="Pho":
			gjetshist.Rebin(rebins[ihn])
			gjetshist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
		for sigh in sighs:
			#sighs[sigh].Scale(0.64)
			sighs[sigh].Rebin(rebins[ihn])
			sighs[sigh].GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
			datahist.SetLineColor(5)




		c1 = TCanvas('c1', '', 700, 600)
		datahist.SetMarkerStyle(21)	
		datahist.SetLineColor(7)
		tthist.SetLineColor(2)
		wjetshist.SetLineColor(3)		
		datahist.SetLineWidth(2)
		tthist.SetLineWidth(2)
		wjetshist.SetLineWidth(2)
	
		leg = TLegend(0.20, 0.5, 0.5, 0.84)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)

		leg.AddEntry( datahist, 'QCD MC', 'l')
		leg.AddEntry( tthist, 'ttbar MC', 'l')
		leg.AddEntry( wjetshist, 'W+jets->QQ MC', 'l')



		htoplot = [datahist,tthist,wjetshist]	
		for sigh in sighs:
			htoplot.append(sighs[sigh])
			htoplot[-1].SetLineWidth(2)
			htoplot[-1].SetLineColor(1)
			leg.AddEntry( htoplot[-1], 'signal MC', 'l')
		if options.anatype=="Pho":
			htoplot.append(gjetshist)
			htoplot[-1].SetLineWidth(2)
			htoplot[-1].SetLineColor(4)
			leg.AddEntry( gjetshist, '#gamma+jets MC', 'l')
		maxes= []
		for vhisto in htoplot:
			vhisto.Scale(1.0/vhisto.Integral())	
			maxes.append(vhisto.GetMaximum())
		htoplot[0].SetMaximum(max(maxes)*maxfacs[ihn])
		htoplot[0].SetStats(0)
		for vhisto in htoplot:
			vhisto.SetTitle(";"+xvals[ihn]+";Fraction")			
			vhisto.Draw("histsame")			
		cutvals[ihn][0]
		line2=ROOT.TLine(cutvals[ihn][0],0.0,cutvals[ihn][0],0.8*max(maxes))
		line2.SetLineColor(2)	
		line2.SetLineWidth(2)			
		line2.SetLineStyle(2)
		line1=ROOT.TLine(cutvals[ihn][1],0.0,cutvals[ihn][1],0.8*max(maxes))
		line1.SetLineColor(2)
		line1.SetLineWidth(2)			
		line1.SetLineStyle(2)

		line2.Draw()
		line1.Draw()

		setstring=options.set
		leg.Draw()

		c1.Print('plots/kinvar_'+options.anatype+'__'+curname+'__bkgonly__'+setstring+options.era+'.root', 'root')
		c1.Print('plots/kinvar_'+options.anatype+'__'+curname+'__bkgonly__'+setstring+options.era+'.pdf', 'pdf')
		c1.Print('plots/kinvar_'+options.anatype+'__'+curname+'__bkgonly__'+setstring+options.era+'.png', 'png')
		#datahist.SetMinimum(0.01)
		#c1.SetLogy()
		#datahist.SetMaximum(datahist.GetMaximum()*100)			
		#c1.RedrawAxis()
		#c1.Update()
		#c1.Print('plots/kinvar_'+options.anatype+'__'+curname+'__bkgonly__semilog__'+setstring+'.root', 'root')
		#c1.Print('plots/kinvar_'+options.anatype+'__'+curname+'__bkgonly__semilog__'+setstring+'.pdf', 'pdf')
		#c1.Print('plots/kinvar_'+options.anatype+'__'+curname+'__bkgonly__semilog__'+setstring+'.png', 'png')
		#c1.SetLogy(0)
		#c1.RedrawAxis()


print "Completed..."																										
