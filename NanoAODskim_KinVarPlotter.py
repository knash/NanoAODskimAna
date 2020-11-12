import NanoAODskim_Functions	
from NanoAODskim_Functions import *

from optparse import OptionParser
import subprocess,os,sys

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

ROOT.gROOT.LoadMacro("insertlogo.C+")

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


cutflowpointsfull=	[
			"",	
			"total",
			"prepresel",
			"presel",
			"Preselection",
			"V tag",
			"T tag",
			"DeltaR",
			"B tag",
			"",
			"",
			""
			]



setname =options.set
NanoF = NanoAODskim_Functions(options.anatype)
labels = NanoF.labels 
candl = NanoF.candl
probl = NanoF.probl
if options.era=="all":
	errsrt="*"
else:
	errsrt=options.era
if isdata:
	datafiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__JetHT__Run"+errsrt+".root")
	print datafiles
	print "rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__JetHT.root"
else:
	datafiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__QCD.root")
QCDfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__QCD.root")
ttfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__TT.root")
#wjetsfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__WJets.root","open")
if options.anatype=="Pho":
	gjetsfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+errsrt+"__GJets.root")
captex=""
sigfiles=[]
if options.anatype=="Pho":
	sigfiles=glob.glob("rootfiles/NanoAODskim_PhoAna"+errsrt+"__WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2.root")
if options.anatype=="WW":
	sigfiles=glob.glob("rootfiles/NanoAODskim_WWAna"+errsrt+"__WkkToWRadionToWWW_M4000-R0-06_TuneCP5_13TeV-madgraph.root")
if options.anatype=="tZb":
	captex="TZB"
	#sigfiles=glob.glob("rootfiles/NanoAODskim_tZbAna"+errsrt+"__WpToTpB_Wp3000Nar_Tp2000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
	#sigfiles+=glob.glob("rootfiles/NanoAODskim_tZbAna"+errsrt+"__WpToBpT_Wp3000Nar_Bp2000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")

	sigfiles=glob.glob("rootfiles/NanoAODskim_tZbAna"+errsrt+"__WpToTpB_Wp5000Nar_Tp3300Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
	sigfiles+=glob.glob("rootfiles/NanoAODskim_tZbAna"+errsrt+"__WpToBpT_Wp5000Nar_Bp3300Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")

if options.anatype=="tHb":
	captex="THB"
	#sigfiles=glob.glob("rootfiles/NanoAODskim_tHbAna"+errsrt+"__WpToTpB_Wp3000Nar_Tp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
	#sigfiles+=glob.glob("rootfiles/NanoAODskim_tHbAna"+errsrt+"__WpToBpT_Wp3000Nar_Bp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")

	sigfiles=glob.glob("rootfiles/NanoAODskim_tHbAna"+errsrt+"__WpToTpB_Wp5000Nar_Tp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
	sigfiles+=glob.glob("rootfiles/NanoAODskim_tHbAna"+errsrt+"__WpToBpT_Wp5000Nar_Bp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")

print "startsigkeys"
sigfs = {}
for sigf in sigfiles:
	keyname=sigf.split("__")[1].replace(".root","").replace("BpT","").replace("TpB","").replace("Tp","").replace("Bp","").replace("Ht","").replace("Zt","")
	print keyname
	if keyname in sigfs:
		sigfs[keyname].append(TFile(sigf,"open"))
	else:
		sigfs[keyname]=[TFile(sigf,"open")]
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
		#TOFIX
		print obj,var
		if obj=="T" and var=="msoftdropdef":
			var="msoftdropdef"
			#rname=rname.replace("msoftdropdef","msoftdrop")
		print "adding",var+"__"+obj+"__"+rname
		histonames.append(var+"__"+obj+"__"+rname)
		if (obj=="W" or obj=="Z")  and var=="msoftdrop":
			rebins.append(2)
			ranges.append([0.0,140.0])
			xvals.append("m_{SD}(Z) GeV")
			#cutvals.append([65.0,105.0])
			cutvals.append([65.0,105.0])
			maxfacs.append(2.3)
		if obj=="H" and var=="msoftdrop":
			rebins.append(5)
			ranges.append([0.0,200.0])
			xvals.append("m_{SD}(H) GeV")
			#cutvals.append([105.0,140.0])
			cutvals.append([105.0,140.0])
			maxfacs.append(1.7)



			
		if obj=="T" and var=="msoftdropdef":
			rebins.append(5)
			ranges.append([0.0,250.0])
			xvals.append("m_{SD}(T) GeV")
			cutvals.append([140.0,220.0])
			maxfacs.append(1.7)


		if obj=="F" and var=="msoftdrop":
			rebins.append(10)
			ranges.append([0.0,300.0])
			xvals.append("m_{SD} GeV")
			cutvals.append([105.0,-999.0])
			maxfacs.append(1.7)
		if obj=="P" and var=="msoftdrop":
			rebins.append(10)
			ranges.append([0.0,300.0])
			xvals.append("m_{SD} GeV")
			cutvals.append([105.0,-999.0])
			maxfacs.append(1.7)
		if (obj=="W" or obj=="Z")  and var=="tau21":
			rebins.append(5)
			ranges.append([0.0,1.0])
			xvals.append("#tau_{21}")
			cutvals.append([0.45,-999.0])
			maxfacs.append(2.9)

		if var=="iW":
			rebins.append(1)
			ranges.append([0.0,1.0])
			xvals.append("imageMD_{W}")
			cutvals.append([0.9,-999.0])
			maxfacs.append(1.7)
		if var=="iMDWW":
			rebins.append(100)
			ranges.append([0.0,1.0])
			xvals.append("imageMD_{WW}")
			cutvals.append([0.8,-999.0])
		if var=="iMDtop":
			rebins.append(100)
			xvals.append("imageMD_{top}")
			cutvals.append([0.9,-999.0])
			maxfacs.append(1.7)
		if var=="iMDPho":
			rebins.append(100)
			ranges.append([0.0,1.0])
			xvals.append("imageMD_{#gammaZ}")
			cutvals.append([0.9,-999.0])
			maxfacs.append(1.7)
		if var=="btagHbb":
			rebins.append(4)
			ranges.append([-1.0,1.0])
			xvals.append("Dbtag")
			cutvals.append([0.6,-999.0])
			maxfacs.append(1.7)






for ihn in xrange(len(histonames)):
		curname = histonames[ihn]
		print "plotting",curname
		vartop = curname.split("__")[0]
		sighs = {}
		datahist=None
		#print "dopen"

		for tdf in datafiles:
			print tdf
			df =  TFile(tdf,"open")
			if datahist==None:
				datahist = copy.deepcopy(df.Get(curname))
				print "fst",curname 
				print datahist.Integral()
			else:
				print df,df.Get(curname)
				print df,df.Get(curname).Integral()
				datahist.Add(copy.deepcopy(df.Get(curname)))
                #print "curname",curname
		#print datahist.Integral()
		#print "ddone"
		#wjetshist = wjetsfile.Get(curname)
		tthist=None
		#print "ttopen"
		for tdf in ttfiles:

			df =  TFile(tdf,"open")
			if tthist==None:
				tthist = copy.deepcopy(df.Get(curname))
			else:
				tthist.Add(copy.deepcopy(df.Get(curname)))
		#print "ttdone"
		if options.anatype=="Pho":
			gjetshist = gjetsfile.Get(curname)

		for sigf in sigfs:
			#print sigf.split("__")[1].replace(".root","")
			sighs[sigf]=None
		#print "StartSig"
		for sigf in sigfs:
			print sigf

			for isf in xrange(len(sigfs[sigf])):
				if sighs[sigf]==None:				
					sighs[sigf]=sigfs[sigf][isf].Get(curname)
				else:
					sighs[sigf].Add(sigfs[sigf][isf].Get(curname))
		#print sighs
		#print curname
		datahist.Rebin(rebins[ihn])			
		tthist.Rebin(rebins[ihn])
		#wjetshist.Rebin(rebins[ihn])
		datahist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])			
		tthist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
		#wjetshist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
		if options.anatype=="Pho":
			gjetshist.Rebin(rebins[ihn])
			gjetshist.GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])
		for sigh in sighs:
			#sighs[sigh].Scale(0.64)
			sighs[sigh].Rebin(rebins[ihn])
			sighs[sigh].GetXaxis().SetRangeUser(ranges[ihn][0],ranges[ihn][1])




		c1 = TCanvas('c1', '', 700, 600)
		datahist.SetMarkerStyle(21)	
		datahist.SetLineColor(2)
		tthist.SetLineColor(7)
		#wjetshist.SetLineColor(3)		
		datahist.SetLineWidth(2)
		tthist.SetLineWidth(2)
		#wjetshist.SetLineWidth(2)
	
		leg = TLegend(0.47, 0.6, 0.84, 0.84)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)

		leg.AddEntry( datahist, 'QCD MC', 'l')
		leg.AddEntry( tthist, 't#bar{t} MC', 'l')
		#leg.AddEntry( wjetshist, 'W+jets->QQ MC', 'l')



		htoplot = [datahist,tthist]#,wjetshist]	
		for sigh in sighs:
			htoplot.append(sighs[sigh])
			htoplot[-1].SetLineWidth(2)
			htoplot[-1].SetLineColor(1)
			leg.AddEntry( htoplot[-1], options.anatype+' signal MC (m_{W\'} = 3TeV)', 'l')
		if options.anatype=="Pho":
			htoplot.append(gjetshist)
			htoplot[-1].SetLineWidth(2)
			htoplot[-1].SetLineColor(4)
			leg.AddEntry( gjetshist, '#gamma+jets', 'l')
		maxes= []
		for vhisto in htoplot:
			vhisto.Scale(1.0/vhisto.Integral())	
			maxes.append(vhisto.GetMaximum())
		htoplot[0].SetMaximum(max(maxes)*maxfacs[ihn])
		htoplot[0].SetMinimum(-0.000001)
		htoplot[0].SetStats(0)
		c1.SetLeftMargin(0.15)
		#vhisto.SetRightMargin(0.05)
		#vhisto.SetTopMargin(0.11)
		c1.SetBottomMargin(0.15)

		for vhisto in htoplot:


			vhisto.GetYaxis().SetTitleOffset(1.1)
			vhisto.GetXaxis().SetTitleOffset(1.1)
			vhisto.GetXaxis().SetLabelSize(0.04)
			vhisto.GetYaxis().SetLabelSize(0.04)
			vhisto.GetXaxis().SetTitleSize(0.05)
			vhisto.GetYaxis().SetTitleSize(0.05)
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

		bin1 = tthist.FindBin(cutvals[ihn][0])
		bin2 = tthist.FindBin(cutvals[ihn][1])
		print vartop

		if vartop=="tau21":
			print "from ",cutvals[ihn][1], cutvals[ihn][0]
			print "QCD",datahist.Integral(bin2,bin1)/datahist.Integral()
			print "ttbar",tthist.Integral(bin2,bin1)/tthist.Integral()

			for sigh in sighs:
				print sigh,sighs[sigh].Integral(bin2,bin1)/sighs[sigh].Integral()


		else:
			print "QCD",datahist.Integral(bin1,bin2)/datahist.Integral()
			print "ttbar",tthist.Integral(bin1,bin2)/tthist.Integral()

			for sigh in sighs:
				print sigh,sighs[sigh].Integral(bin1,bin2)/sighs[sigh].Integral()

		line2.Draw()
		line1.Draw()

		setstring=options.set
		leg.Draw()
	
		ROOT.insertlogo( c1, 13, 11 )
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




datahist=None
for tdf in datafiles:
	print tdf
	df =  TFile(tdf,"open")


	if datahist==None:
		datahist = copy.deepcopy(df.Get("CutflowC"))
	else:
		datahist.Add(copy.deepcopy(df.Get("CutflowC")))
	print datahist.Integral()
print "c1"
limnames=glob.glob("limitsetting/theta/NanoAODskim_"+options.anatype+"_ForLimits__"+errsrt+"central.root")
corrlimf=[]


numevs={}
ints={}

for ln in limnames:
	print "c2"
	corrlimf.append(TFile(ln))
	#print ln,curyear
	curyear=ln.split("_")[-1][0:4]
	print "c2p1"
	qcdlh=corrlimf[-1].Get("mass_"+captex+"_C_"+curyear+"__qcd")
	print "c2p2"	
	ttlh=corrlimf[-1].Get("mass_"+captex+"_C_"+curyear+"__ttbar")
	print "c2p3",corrlimf[-1],"mass_"+captex+"_C_"+curyear+"__ttbar"
	print ttlh 
	print "c2p4"
	if "ttbar" in numevs:
		numevs["ttbar"]+=ttlh.GetEntries()
		ints["ttbar"]+=ttlh.Integral()
	else:
		numevs["ttbar"]=ttlh.GetEntries()
		ints["ttbar"]=ttlh.Integral()
	if "qcd" in numevs:
		numevs["qcd"]+=qcdlh.GetEntries()
		ints["qcd"]+=qcdlh.Integral()
	else:
		numevs["qcd"]=qcdlh.GetEntries()
		ints["qcd"]=qcdlh.Integral()
	print "c3"
	for sigf in sigfs:
		
		sigm=sigf[sigf.find("WpTo_Wp")+7:sigf.find("Nar")]
		print sigm
		cursh=corrlimf[-1].Get("mass_"+captex+"_C_"+curyear+"__WptoqVLQWp_B0p5T0p5H0p5Z0p5_"+sigm)

		if sigf in numevs:
			numevs[sigf]+=cursh.GetEntries()
			ints[sigf]+=cursh.Integral()
		else:
			numevs[sigf]=cursh.GetEntries()
			ints[sigf]=cursh.Integral()

print "checkp"
norms = {"data":1.0}
print numevs
print ints

for ind in numevs:
	norms[ind]=ints[ind]/float(numevs[ind])


for nn in norms:
	print nn,norms[nn]


print "DATA"
for dbin in xrange(datahist.GetNbinsX()+1):
	print cutflowpointsfull[dbin],datahist.GetBinContent(dbin)

print "QCD",cutflowpointsfull[-1],ints["qcd"]

tthist=None
for tdf in ttfiles:
		df =  TFile(tdf,"open")

		#mass_THB_C_2018
		if tthist==None:
			tthist = copy.deepcopy(df.Get("CutflowC"))

		else:
			tthist.Add(copy.deepcopy(df.Get("CutflowC")))



print "ttbar"
for dbin in xrange(tthist.GetNbinsX()+1):
	print cutflowpointsfull[dbin],tthist.GetBinContent(dbin)*norms["ttbar"]

sighs = {}

for sigf in sigfs:
	sighs[sigf]=None
for sigf in sigfs:
	print sigf
	for isf in xrange(len(sigfs[sigf])):

		if sighs[sigf]==None:		
			#print 	sigf,isf
			sighs[sigf]=sigfs[sigf][isf].Get("CutflowC")
		else:
			#print 	"adding",sigf,isf
			sighs[sigf].Add(sigfs[sigf][isf].Get("CutflowC"))


	print "\\bf{Selection} & \\bf{Data} & \\bf{qcd} & \\bf{ttbar} & \\bf{Signal}\\\\"
	for dbin in xrange(sighs[sigf].GetNbinsX()+1):
		QCDev="-"
		if dbin==8:
			QCDev=strf(ints["qcd"])
		print cutflowpointsfull[dbin]," & ",int(datahist.GetBinContent(dbin))," & ",QCDev," & ",strf(tthist.GetBinContent(dbin)*norms["ttbar"],2)," & ",strf(sighs[sigf].GetBinContent(dbin)*norms[sigf],2),"\\\\"

print "Completed..."


																										

