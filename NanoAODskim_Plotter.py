import NanoAODskim_Functions	
from NanoAODskim_Functions import *

from optparse import OptionParser
import subprocess,os,sys

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'QCD',
                  dest		=	'set',
                  help		=	'data or ttbar')
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')
parser.add_option('-w', '--wjets', metavar='F', type='string', action='store',
                  default	=	'None',
                  dest		=	'wjets',
                  help		=	'Corr or MC or None')
parser.add_option('-f', '--rootfolder', metavar='F', type='string', action='store',
                  default	=	'rootfiles',
                  dest		=	'rootfolder',
                  help		=	'rootfiles')
parser.add_option('-S', '--sigver', metavar='F', type='string', action='store',
                  default	=	'central',
                  dest		=	'sigver',
                  help		=	'')
parser.add_option('--normcorr', metavar='F', action='store_true',
                  default=False,
                  dest='normcorr',
                  help='normcorr')
parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')
parser.add_option('--skipplots', metavar='F', action='store_true',
                  default=False,
                  dest='skipplots',
                  help='skipplots')
parser.add_option('--cutopt', metavar='F', action='store_true',
		  default=False,
		  dest='cutopt',
		  help='not worknig')
parser.add_option('--qcdmcbkg', metavar='F', action='store_true',
		  default=False,
		  dest='qcdmcbkg',
		  help='not worknig')
parser.add_option('--onlyttnorm', metavar='F', action='store_true',
		  default=False,
		  dest='onlyttnorm',
		  help='onlyttnorm')
parser.add_option('--onlylim', metavar='F', action='store_true',
		  default=False,
		  dest='onlylim',
		  help='onlylim')
parser.add_option('--withST', metavar='F', action='store_true',
		  default=False,
		  dest='withST',
		  help='withST')


parser.add_option('--postfit', metavar='F', action='store_true',
		  default=False,
		  dest='postfit',
		  help='postfit')

parser.add_option('--dogcvlq', metavar='F', action='store_true',
		  default=False,
		  dest='dogcvlq',
		  help='dogcvlq')

parser.add_option('--dogczh', metavar='F', action='store_true',
		  default=False,
		  dest='dogczh',
		  help='dogczh')
(options, args) = parser.parse_args()

withST=options.withST
regiontoname=	{
		"C":"C, Signal",
		"K":"K, Medium t",
		"H":"H, Medium V",
		"F":"F, Validation",
		"ZC":"Low mass t",
		"FT":"ttbar measurement",
		}

mod=None
if options.sigver=="central":
	mod=0
if options.sigver=="high":
	mod=+1
if options.sigver=="low":
	mod=-1

genstr=options.sigver
if options.dogczh:
	genstr+="genzc"
if options.dogcvlq:
	genstr+="genvlq"

rootfolder=options.rootfolder+"/"
setname = options.set
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True

blindington = False
#if options.set=="JetHT":
#	blindington = True

extex=""
if options.normcorr:
	extex="__ttnorm"
wpfilter=["2000","3000","4000"]
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
mthbbinning=[1000.0]
increm=270.0
#constdict = NanoF.LoadConstants
while mthbbinning[-1]<8000.0:
	mthbbinning.append(mthbbinning[-1]+increm)
	if mthbbinning[-1]>3000.0:
		increm=400.0
	if mthbbinning[-1]>4000.0:
		mthbbinning.append(5000.0)
		mthbbinning.append(8000.0)
		break
print "mthbbinning",mthbbinning
cobin=False
if cobin:
	mthbbinning=[1000.0,1600.0,2200.0,2800.0,8000.0]
	#increm=270.0
	#while mthbbinning[-1]<8000.0:
	#	mthbbinning.append(mthbbinning[-1]+increm)
	#	if mthbbinning[-1]>2000.0:
	#		increm=500.0
	#	if mthbbinning[-1]>2500.0:
	#		mthbbinning.append(8000.0)
	#		break

bins2=array('d',mthbbinning)
setstring=options.set
c2 = TCanvas('c2', '', 700, 600)
c1 = TCanvas('c1', '', 700, 600)

eras=(options.era).split(",")
sumomly=False
if len(eras)>1:
	sumomly=True
	
qcdmcbkg = options.qcdmcbkg
cutopt = options.cutopt
optstr=""
if cutopt:
	optstr="optimizer_"
sumhists={}



ROOT.gROOT.LoadMacro("insertlogo.C+")
sumera=""
print eras
sigcolors = [1,3,4,5,6,7,8,9,10]
leadjparam=False
allsigneff={}
allsigtoteff={}
pftex=""
if options.postfit:
	pftex="__postfit"






for era in eras:

	sumera+=era
	#print sumera
	setname =options.set
	NanoF = NanoAODskim_Functions(options.anatype,era)
	labels = NanoF.labels 
	candl = NanoF.candl
	probl = NanoF.probl
	wjetscorr=options.wjets

	uncs=["pu","trig","jes","jer","jms","jmr"]
	uncorruncs=["pu","trig","jes","jer","jms","jmr"]
	genuncs=["ps","q2","pdfweight"]
	uncorrgenuncs=["ps","q2","pdfweight"]
	uncorruncs+=uncorrgenuncs
	if "B" in labels:
		uncs+=["btag","bmistag"]
		uncorruncs+=["btag","bmistag"]
	if "H" in labels:
		uncs.append("htag")
		uncorruncs.append("htag")
		uncs.append("hmistag")
		uncorruncs.append("hmistag")
	if ("Z" in labels) or ("W" in labels):
		uncs.append("wtag")
		uncs.append("extrap")
		uncorruncs.append("extrap")
		uncorruncs.append("wtag")
		#print uncs
	if "T" in labels:
		uncs.append("ttag")
		uncorruncs.append("ttag")
		
	if options.onlylim:
		newlabs=[]
		for lab in labels:
			#print lab
			if len(lab)==3:
				newlabs.append(lab)
		labels=newlabs
	#print labels
	uncnames=["mass","pt","eta"]
	prestr="NanoAODskim_"+optstr+options.anatype

	settofind=options.set
	if settofind=="JetHT":
		settofind="JetHT__Run"+era
	if options.wjets!="None":
		extex+="__WJ"+wjetscorr


	sigfiles=[]
	sigyearforplotting=era
	if options.anatype=="Pho":
		sigfiles=glob.glob(rootfolder+prestr+"Ana"+era+"__WkkToRWToTri_*.root")
	if options.anatype=="WW":
		sigfiles=glob.glob(rootfolder+prestr+"Ana"+era+"__WkkToWRadionToWWW_M*.root")
	genmatrix = NanoF.genmatrix
	if options.anatype=="tZb":
		sigfiles=[]
		for gg in genmatrix:
			wpm=gg[0]
			if wpm in [5500]:
				continue
			centindex=(len(gg[1])/2)+mod
			vlqm=gg[1][centindex]
			#print wpm,vlqm
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToBpT_Wp"+str(wpm)+"Nar_Bp"+str(vlqm)+"Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToTpB_Wp"+str(wpm)+"Nar_Tp"+str(vlqm)+"Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToBpT_Wp"+str(wpm)+"Nar_Bp"+str(vlqm)+"Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToTpB_Wp"+str(wpm)+"Nar_Tp"+str(vlqm)+"Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")

	if options.anatype=="tHb":
		sigfiles=[]
		for gg in genmatrix:
			#print gg
			wpm=gg[0]
			if wpm in [5500]:
				continue
			centindex=(len(gg[1])/2)+mod
			vlqm=gg[1][centindex]
			#print wpm,vlqm
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToBpT_Wp"+str(wpm)+"Nar_Bp"+str(vlqm)+"Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToTpB_Wp"+str(wpm)+"Nar_Tp"+str(vlqm)+"Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToBpT_Wp"+str(wpm)+"Nar_Bp"+str(vlqm)+"Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToTpB_Wp"+str(wpm)+"Nar_Tp"+str(vlqm)+"Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")




	if isdata:		
		#print "DATA",rootfolder+prestr+"Ana"+era+"__"+settofind+".root"	
		datafile=TFile(rootfolder+prestr+"Ana"+era+"__"+settofind+".root","open")
	else:
		datafile=TFile(rootfolder+prestr+"Ana"+era+"__QCD.root","open")
	QCDfile=TFile(rootfolder+prestr+"Ana"+era+"__QCD.root","open")


	if options.anatype=="Pho":
				gjetsfile=TFile(rootfolder+prestr+"Ana"+era+"__GJets.root","open")
	if wjetscorr!="None":
				wjetsfile=TFile(rootfolder+prestr+"Ana"+era+"__WJets.root","open")
	sigfs = {}
	for sigf in sigfiles:
				sigfs[sigf.split("__")[1].replace(".root","")]=TFile(sigf,"open")
	#print sigfiles
	if qcdmcbkg:
		qcdfile=TFile(rootfolder+prestr+"Ana"+era+"__QCD.root","open")
	ttfile=TFile(rootfolder+prestr+"Ana"+era+"__TT.root","open")
	if withST:
		stfile=TFile(rootfolder+prestr+"Ana"+era+"__ST.root","open")

	nbins=6
	rebininv=10

	rebinob=5
	rebinsd=5
	
	if options.anatype=="tHb" or options.anatype=="tZb" or options.anatype=="Pho" :
		nbins=2
		rebininv=25
	if qcdmcbkg:
		rebininv*=4
	rescale = 0.0
	if options.anatype=="tHb":
		rescale = 0.5
	if options.anatype=="tZb":
		rescale = 0.5

	histonames=[]
	rebins=[]
	invmnames =[]

	constdict = NanoF.LoadConstants
	#print constdict
	ttbarnormcorr=constdict['ttrenorm']
	#print ttbarnormcorr
	for lab in labels:
		#print lab
		#if len(lab)!=2:
		#	continue
		if len(lab)>1:
			if (options.anatype=="tHb" or options.anatype=="tZb"):

				if len(lab)>2 or lab=="T":
					invmnames.append("mass__"+lab)

			else:
				invmnames.append("mass__"+lab)
			histonames.append("mass__"+lab)
			rebins.append(rebininv)
		else:
			histonames.append("pt__"+lab)
			rebins.append(rebinob)
			histonames.append("eta__"+lab)
			rebins.append(rebinob)
			if options.anatype=="tHb" and lab=="H":
				histonames.append("msoftdropdef__"+lab)
				rebins.append(rebinsd)
	limithistos = {}




	vers = [["C","D"],["F","G"],["K","L"],["H","I"],["ZC","ZD"]]
	if cutopt:
		vers = [['CFD'],['KFD'],['HFD'],['CFH1'],['CFH2'],['CFH3'],['CFT1'],['CFT2'],['CFT3'],['CFB1'],['CFB2'],['HFH1'],['HFH2'],['HFH3'],['KFT1'],['KFT2'],['KFT3']]

	#if options.anatype=="tHb" or options.anatype=="tZb":
		#vers.append(["N","O"])
	if options.anatype=="tHb" and not cutopt:
		vers.append(["FT","FTR"])
		if options.onlyttnorm:
			vers=[["FT","FTR"]]
	#if options.onlylim:
	#	vers = [["C","D"]]
	tttnormsimple=None
	errsimple=None
	ttvals=None
	limsetregions=["C","K","H","F","ZC"]
	#if options.onlylim:
	#	limsetregions=["C"]
	if cutopt:
		limsetregions=['CFD','KFD','HFD','CFH1','CFH2','CFH3','CFT1','CFT2','CFT3','CFB1','CFB2','HFH1','HFH2','HFH3','KFT1','KFT2','KFT3']
	if options.postfit:
		continue

	for vv in vers:
		#print "blindzors",options.set,vv[0]

 		#print vv
		for ihn in xrange(len(histonames)):

			curname = histonames[ihn]
			#print curname
			if not (curname+"__"+vv[0] in sumhists):
				sumhists[curname+"__"+vv[0]]={}
			obj=curname.split("__")[1]
			var=curname.split("__")[0]
			writelim=False
			#print vv[0],limsetregions,vv[0] in limsetregions
			if (curname in invmnames) and (vv[0] in limsetregions) and (not qcdmcbkg):
				writelim=True
			sighs = {}
			sighssum = {}
			datahist = datafile.Get(curname+"__"+vv[0])
			#print datahist.Integral()
			#print curname+"__"+vv[0]
			#print datahist.GetName()
			nobject = datahist.GetName().split("__")[0]+"_"+datahist.GetName().split("__")[1]
			nobject+="_"+vv[0]+"_"+era
			#print datafile
			#print curname+"__"+vv[0]
			#print "varobj",var,obj
			if var=="mass" and (obj in ["THB","TZB"]):
				datahist = datahist.Rebin(len(bins2)-1,datahist.GetName()+"TEMP",bins2)
			else:
				#print vv,rebins[ihn]
				datahist.Rebin(rebins[ihn])
			#print datafile,curname+"__"+vv[1]+"_0"
			bkgfile=datafile

			if qcdmcbkg:
				bkgfile=qcdfile
			#print datahist.Integral()
			if leadjparam:
				bkghist = bkgfile.Get(curname+"__"+vv[1]+"_0")
				bkghist.Add(bkgfile.Get(curname+"__"+vv[1]+"_1"))

				bkghistttup = bkgfile.Get(curname+"__"+vv[1]+"_0__up")
				bkghistttdown .Add(bkgfile.Get(curname+"__"+vv[1]+"_1__down"))

			else:
				bkghist = bkgfile.Get(curname+"__"+vv[1])
				#print curname+"__"+vv[1]+"_up"
				bkghistttup = bkgfile.Get(curname+"__"+vv[1]+"_up")
				bkghistttdown = bkgfile.Get(curname+"__"+vv[1]+"_down")
				#print bkghist.Integral()
			#print datahist.Integral()

			if isdata and (not qcdmcbkg):

				bkgtosubtract = [ttfile]
				if withST:
					bkgtosubtract.append(stfile)
				if options.anatype=="Pho":
					bkgtosubtract.append(gjetsfile)
				if wjetscorr=="MC" and wjetscorr!="None":
					bkgtosubtract.append(wjetsfile)
				#print curname+"__"+vv[1]
				print bkghist.Integral()
				for bkgs in bkgtosubtract:
					#print "subbing",bkgs.GetName(),bkgs,curname+"__"+vv[1]
					temphist = bkgs.Get(curname+"__"+vv[1])
					#print temphist.Integral()
					if bkgs==ttfile:
						#print "ttbar"
						temphistttup = bkgs.Get(curname+"__"+vv[1])
						temphistttdown = bkgs.Get(curname+"__"+vv[1])
						temphist.Scale(ttbarnormcorr[0])
						temphistttup.Scale(ttbarnormcorr[0]+ttbarnormcorr[1])
						temphistttdown.Scale(ttbarnormcorr[0]-ttbarnormcorr[1])
						bkghistttup.Add(temphistttup,-1)
						bkghistttdown.Add(temphistttdown,-1)

					bkghist.Add(temphist,-1)
				#print bkghist.Integral()
		
			if var=="mass" and (obj in ["THB","TZB"]):
					bkghist = bkghist.Rebin(len(bins2)-1,bkghist.GetName()+"TEMP",bins2)
					if not qcdmcbkg:
						bkghistttup = bkghistttup.Rebin(len(bins2)-1,bkghistttup.GetName()+"TEMP",bins2)
						bkghistttdown = bkghistttdown.Rebin(len(bins2)-1,bkghistttdown.GetName()+"TEMP",bins2)
			else:
					bkghist.Rebin(rebins[ihn])
					if not qcdmcbkg:
						bkghistttup.Rebin(rebins[ihn])
						bkghistttdown.Rebin(rebins[ihn])
			#QCD==wjets+qcd!!
			if wjetscorr!="None":
				wjetshist = wjetsfile.Get(curname+"__"+vv[0])
			#print datahist.Integral()
			if wjetscorr=="Corr":
				QCDhist = QCDfile.Get(curname+"__"+vv[0])
				temphist = wjetsfile.Get(curname+"__"+vv[1])
				#print QCDhist.Integral(),wjetshist.Integral(),temphist.Integral()
				if (QCDhist.Integral()+wjetshist.Integral())!=0 and temphist.Integral()!=0:
					frac=wjetshist.Integral()/(QCDhist.Integral()+wjetshist.Integral())
					rat=wjetshist.Integral()/temphist.Integral()
					wjcorr = (rat-1.)*frac+1.
					#print "WJfrac",frac,"WJbias",rat,"corr",wjcorr
				else:
					wjcorr = (rat-1.)*frac+1.
					#print "err","corr",wjcorr
			#print "3"

			tthist = ttfile.Get(curname+"__"+vv[0])


			#print datahist.Integral(),tthist.Integral()
			if var=="mass" and (obj in ["THB","TZB"]):
				tthist = tthist.Rebin(len(bins2)-1,tthist.GetName()+"TEMP",bins2)
			else:
				tthist.Rebin(rebins[ihn])
			tthistuncs = {}
			if withST:
				sthist = stfile.Get(curname+"__"+vv[0])

				if var=="mass" and (obj in ["THB","TZB"]):
					sthist = sthist.Rebin(len(bins2)-1,sthist.GetName()+"TEMP",bins2)
				else:
					sthist.Rebin(rebins[ihn])
				sthistuncs = {}

			bkghist.SetMaximum(max(bkghist.GetMaximum(),datahist.GetMaximum())*1.4)
			#print datahist.Integral(),tthist.Integral()
			#print  var,uncnames
			if var in uncnames:
				for unc in uncs:
					#print unc,curname+"__"+vv[0]+"__"+unc+"__down",curname+"__"+vv[0]+"__"+unc+"__up"
					tthistuncs[unc]=[ttfile.Get(curname+"__"+vv[0]+"__"+unc+"__down"),ttfile.Get(curname+"__"+vv[0]+"__"+unc+"__up")]

					if var=="mass" and (obj in ["THB","TZB"]):
						tthistuncs[unc][0] = tthistuncs[unc][0].Rebin(len(bins2)-1,tthistuncs[unc][0].GetName()+"TEMP",bins2)
						tthistuncs[unc][1] = tthistuncs[unc][1].Rebin(len(bins2)-1,tthistuncs[unc][1].GetName()+"TEMP",bins2)
					else:
						tthistuncs[unc][0].Rebin(rebins[ihn])
						tthistuncs[unc][1].Rebin(rebins[ihn])
					if writelim:
						appstr=""
						if unc in uncorruncs:
							appstr=options.era

						tthistuncs[unc][0].SetName(nobject+"__ttbar__"+unc+appstr+"__down")
						limithistos[tthistuncs[unc][0].GetName()] = tthistuncs[unc][0]

						tthistuncs[unc][1].SetName(nobject+"__ttbar__"+unc+appstr+"__up")
						limithistos[tthistuncs[unc][1].GetName()]=tthistuncs[unc][1]
				if withST:
					for unc in (uncs+genuncs):

						print unc,curname+"__"+vv[0]+"__"+unc+"__down",curname+"__"+vv[0]+"__"+unc+"__up"
						sthistuncs[unc]=[stfile.Get(curname+"__"+vv[0]+"__"+unc+"__down"),stfile.Get(curname+"__"+vv[0]+"__"+unc+"__up")]

						if var=="mass" and (obj in ["THB","TZB"]):
							sthistuncs[unc][0] = sthistuncs[unc][0].Rebin(len(bins2)-1,sthistuncs[unc][0].GetName()+"TEMP",bins2)
							sthistuncs[unc][1] = sthistuncs[unc][1].Rebin(len(bins2)-1,sthistuncs[unc][1].GetName()+"TEMP",bins2)
						else:
							sthistuncs[unc][0].Rebin(rebins[ihn])
							sthistuncs[unc][1].Rebin(rebins[ihn])
						if writelim:
							appstr=""
							if unc in uncorruncs:
								appstr=options.era

							sthistuncs[unc][0].SetName(nobject+"__st__"+unc+appstr+"__down")
							limithistos[sthistuncs[unc][0].GetName()] = sthistuncs[unc][0]

							sthistuncs[unc][1].SetName(nobject+"__st__"+unc+appstr+"__up")
							limithistos[sthistuncs[unc][1].GetName()]=sthistuncs[unc][1]
			if options.anatype=="Pho":
				gjetshist = gjetsfile.Get(curname+"__"+vv[0])
			#print datahist.Integral()

			for sigf in sigfiles:
				#print datahist,datahist.Integral()
				#print sigf
				sindex = sigf.split("__")[1].replace(".root","")
				sighs[sindex]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0])

				#print datahist,datahist.Integral()

				if var in uncnames:
					for unc in uncs:
						appstr=""
						if unc in uncorruncs:
							appstr=options.era
						#print curname+"__"+vv[0]+"__"+unc+"__down"
						#print sigf.split("__")[1].replace(".root",""),sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0]+"__"+unc+"__down"),curname+"__"+vv[0]+"__"+unc+appstr+"__down"
						sighs[sindex+"__"+unc+appstr+"__down"]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0]+"__"+unc+"__down")
						sighs[sindex+"__"+unc+appstr+"__up"]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0]+"__"+unc+"__up")
						#print sindex+"__"+unc+appstr+"__down",curname+"__"+vv[0]+"__"+unc+appstr+"__down"
						sighs[sindex+"__"+unc+appstr+"__down"].SetName(curname+"__"+vv[0]+"__"+unc+appstr+"__down")
						sighs[sindex+"__"+unc+appstr+"__up"].SetName(curname+"__"+vv[0]+"__"+unc+appstr+"__up")
				#sigfs[sigf.split("__")[1].replace(".root","")].Close()
			#print datahist.Integral()
			#print sigfiles
			#print sighs

				

			#bkghistup.Rebin(rebins[ihn])
			#bkghistdown.Rebin(rebins[ihn])
			#bkghistcorrup.Rebin(rebins[ihn])
			#bkghistcorrdown.Rebin(rebins[ihn])
			
			if options.normcorr:
				tthist.Scale(ttbarnormcorr[0])
				for unc in tthistuncs:
					tthistuncs[unc][0].Scale(ttbarnormcorr[0])
					tthistuncs[unc][1].Scale(ttbarnormcorr[0])
			if wjetscorr!="None":
				wjetshist.Rebin(rebins[ihn])
			if options.anatype=="Pho":
				gjetshist.Rebin(rebins[ihn])

			for sigh in sighs:
				#print sigh


				if var=="mass" and (obj in ["THB","TZB"]):
					sighs[sigh] = sighs[sigh].Rebin(len(bins2)-1,sighs[sigh].GetName()+"TEMP",bins2)
				else:
					sighs[sigh].Rebin(rebins[ihn])
				if options.anatype=="tHb" or options.anatype=="tZb":
					#print "RESCALE ALL SIG BY",rescale
					#print sighs[sigh].Integral()			
					sighs[sigh].Scale(rescale)
					#print sighs[sigh].Integral()	
			#print "4"


			bbinhistsup = []

			errhist = copy.deepcopy(bkghist)
			errhistcorr = copy.deepcopy(bkghist)
			conthist = copy.deepcopy(bkghist)
			sumc=0.0
			if qcdmcbkg:
				errhist.Scale(0.1)
				errhistcorr.Scale(0.1)
			else:
				for xbin in xrange(errhist.GetNbinsX()+1):
					cont=0.0
					contcorr=0.0
					fullcont = 0.0
					brange=1
					if leadjparam:
						brange=2
					for lbin in xrange(brange):
						lbinstr=""
						if leadjparam:
							lbinstr="_"+str(lbin)
						for ybin in xrange(nbins+1):
							#print "ybin",ybin
							#print "bbin"+str(ybin)+"__"+candl+"__"+curname+"__D__err_"+str(lbin)
							#print "bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]+"__err"+lbinstr
							bbinhistserr = copy.deepcopy(datafile.Get("bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]+"__err"+lbinstr))
							bbinhistscont = copy.deepcopy(datafile.Get("bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]))

							#print "bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]+"__err_"+str(lbin)

							#if var=="mass" and (obj in ["THB","TZB"]):
							#	sighs[sigh] = sighs[sigh].Rebin(len(bins2)-1,sighs[sigh].GetName()+"TEMP",bins2)
							#else:
							#bbinhistserr.RebinY(rebins[ihn])
							#bbinhistscont.RebinY(rebins[ihn])


							for errbin in xrange(bbinhistserr.GetNbinsX()+1):
		
								projectederr=bbinhistserr.ProjectionY(bbinhistserr.GetName()+"_py",errbin,errbin)

								if var=="mass" and (obj in ["THB","TZB"]):
									projectederr = projectederr.Rebin(len(bins2)-1,projectederr.GetName()+"TEMP",bins2)
								else:
									projectederr.Rebin(rebins[ihn])
								errpoint = projectederr.GetXaxis().GetBinCenter(xbin)

								cont += projectederr.GetBinContent(xbin)*projectederr.GetBinContent(xbin)
								contcorr += projectederr.GetBinContent(xbin)
								#cont += bbinhistserr.GetBinContent(errbin,xbin)*bbinhistserr.GetBinContent(errbin,xbin)
								#contcorr += bbinhistserr.GetBinContent(errbin,xbin)
								#print "1d",projectederr.GetBinContent(xbin)
								#print "2d",bbinhistserr.GetBinContent(errbin,xbin)
								#print 		
								#print ybin		
								#print errhist.GetBinCenter(xbin),bbinhistserr.GetBinContent(errbin,xbin)
								#print errhist.GetBinCenter(xbin),contcorr
							for errbin1 in xrange(bbinhistscont.GetNbinsX()+1):
								projectedcont=bbinhistscont.ProjectionY(bbinhistscont.GetName()+"_py",errbin1,errbin1)

								if var=="mass" and (obj in ["THB","TZB"]):
									projectedcont = projectedcont.Rebin(len(bins2)-1,projectedcont.GetName()+"TEMP",bins2)
								else:
									projectedcont.Rebin(rebins[ihn])
								#fullcont += bbinhistscont.GetBinContent(errbin1,xbin)
								fullcont += projectedcont.GetBinContent(xbin)

								#print errpoint,bbinhistscont.GetBinContent(errbin,xbin),fullcont
								#print errhist.GetBinCenter(xbin),bbinhistserr.GetXaxis().GetBinCenter(errbin),bbinhistserr.GetYaxis().GetBinCenter(xbin)
								#print cont
					#if bkghist.GetBinContent(xbin)>0:
						#print errpoint,cont,sqrt(cont)/bkghist.GetBinContent(xbin)
						#print sqrt(cont)/fullcont

					cont+=bkghist.GetBinError(xbin)*bkghist.GetBinError(xbin)
					fullcontcorr=contcorr*contcorr+bkghist.GetBinError(xbin)*bkghist.GetBinError(xbin)
					#print "endcont",cont,sqrt(cont),
					
					errhist.SetBinContent(xbin,sqrt(cont))
					errhistcorr.SetBinContent(xbin,sqrt(fullcontcorr))

					errhist.SetBinError(xbin,0.)
					errhistcorr.SetBinError(xbin,0.)

					conthist.SetBinContent(xbin,fullcont)
					#print bkghist.GetBinContent(xbin),fullcont
					if errhist.GetXaxis().GetBinCenter(xbin)!=errpoint:
						logging.error("Inconsistent Binning "+str(errhist.GetXaxis().GetBinCenter(xbin))+" "+str(errpoint)+"\n	for "+ str(vv)+","+str(histonames[ihn]))
					
				#print "5"
			#for curbin in xrange(conthist.GetNbinsX()+1):
			#	print "SUMMED,NOM",conthist.GetBinContent(curbin),bkghist.GetBinContent(curbin)



			
			bkghistup = copy.deepcopy(bkghist)
			bkghistup.Add(errhist)

			bkghistdown = copy.deepcopy(bkghist)
			bkghistdown.Add(errhist,-1)

			bkghistcorrup = copy.deepcopy(bkghist)
			bkghistcorrup.Add(errhistcorr)

			bkghistcorrdown = copy.deepcopy(bkghist)
			bkghistcorrdown.Add(errhistcorr,-1)





			if writelim:

				#datahist.SetName(nobject+"__data")
				tthist.SetName(nobject+"__ttbar")
				if wjetscorr!="None":
					wjetshist.SetName(nobject+"__wjets")
				if options.anatype=="Pho":
					gjetshist.SetName(nobject+"__gjets")

				#wjetshist.SetName(nobject+"__wjets")
				bkghist.SetName(nobject+"__qcd")

				bkghistttup.SetName(nobject+"__qcd__tt"+era+options.anatype+"__up")
				bkghistttdown.SetName(nobject+"__qcd__tt"+era+options.anatype+"__down")
				bkghistup.SetName(nobject+"__qcd__bkg"+era+options.anatype+"__up")
				bkghistdown.SetName(nobject+"__qcd__bkg"+era+options.anatype+"__down")

				if (not blindington) or (not vv[0]=="C"):
					datahist.SetName(nobject+"__DATA")
					limithistos[datahist.GetName()]=datahist

				#limithistos.append(datahist)
				limithistos[tthist.GetName()]=tthist

				if withST:
					sthist.SetName(nobject+"__st")
					limithistos[sthist.GetName()]=sthist
				if options.anatype=="Pho":
					limithistos[gjetshist.GetName()]=gjetshist
				#limithistos.append(wjetshist)
				limithistos[bkghist.GetName()]=bkghist
				limithistos[bkghistttup.GetName()]=bkghistttup
				limithistos[bkghistttdown.GetName()]=bkghistttdown
				limithistos[bkghistup.GetName()]=bkghistup
				limithistos[bkghistdown.GetName()]=bkghistdown
				for sigh in sighs:
						#print sigh
						if options.anatype=="Pho":
							if sigh == "WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2":
								sighs[sigh].SetName(nobject+"__M3000")
								sighs[sigh].SetTitle(sighs[sigh].GetName())
								limithistos[sighs[sigh].GetName()]=sighs[sigh]
						if options.anatype=="WW":
							#print sigh
							#print sigh.split("-")
							#print (sigh.split("-")[0]).split("_")
							curhname = (sigh.split("-")[0]).split("_")[1]
							sighs[sigh].SetName(nobject+"__"+curhname)
							limithistos[sighs[sigh].GetName()]=sighs[sigh]



							
							
		

			c1.cd()
			main = ROOT.TPad("main", "main", 0, 0.3, 1, 1)
			sub = ROOT.TPad("sub", "sub", 0, 0, 1, 0.3)

			main.SetLeftMargin(0.16)
			main.SetRightMargin(0.05)
			main.SetTopMargin(0.11)
			main.SetBottomMargin(0.0)

			sub.SetLeftMargin(0.16)
			sub.SetRightMargin(0.05)
			sub.SetTopMargin(0)
			sub.SetBottomMargin(0.3)

			main.Draw()
			sub.Draw()

			main.cd()

			datahist.SetMarkerStyle(20)	
			datahist.SetLineColor(1)					
			bkghistup.SetLineStyle(2)
			bkghistdown.SetLineStyle(2)
			bkghistcorrup.SetLineStyle(3)
			bkghistcorrdown.SetLineStyle(3)
			bkghist.SetStats(0)

			xaxist = var+"("+obj+")"
			bkghist.SetTitle(';'+xaxist+';Events/Bin')	

			leg1 = TLegend(0.60, 0.55, 0.84, 0.84)
			leg1.SetFillColor(0)
			leg1.SetBorderSize(0)
			leg1.AddEntry( datahist, 'Data', 'PE')
			leg1.AddEntry( bkghist, 'QCD MC selection', 'l')
			leg1.AddEntry( bkghist, 'QCD MC estimate', 'l')
			leg1.AddEntry( bkghistup, '1#sigma bkg uncertainty', 'l')


			bkghist.Draw('hist')

			bkghistup.Draw('histsame')
			bkghistdown.Draw('histsame')
			if not blindington:
				datahist.Draw("same")
			elif not vv[0]=="C":
				datahist.Draw("same")
			#bkghistcorrup.Draw('histsame')
			#bkghistcorrdown.Draw('histsame')

			#print "data:",datahist.Integral()
			#print "bkg:",bkghist.Integral()
			unc = 0.5*(bkghistup.Integral()-bkghistdown.Integral())
			#print "unc:",unc
			#print "ratio",datahist.Integral()/bkghist.Integral(),"chi2",((datahist.Integral()-bkghist.Integral())/unc)*((datahist.Integral()-bkghist.Integral())/unc)
			leg1.Draw()
			sub.cd()

			
			pull = NanoF.Make_Pull_plot( datahist,bkghist,bkghistup,bkghistdown )

			pull.SetFillColor(ROOT.kBlue)

			pull.SetTitle(';'+xaxist+';(Data-Bkg)/#sigma')
			pull.SetStats(0)


			pull.GetYaxis().SetRangeUser(-2.9,2.9)
			pull.GetXaxis().SetLabelSize(0.05)
			pull.GetYaxis().SetLabelSize(0.05)


			LS = .13

			pull.GetYaxis().SetTitleOffset(0.4)
			pull.GetXaxis().SetTitleOffset(0.9)
			pull.SetStats(0)
			    

			pull.GetYaxis().SetLabelSize(LS)
			pull.GetYaxis().SetTitleSize(LS)
			pull.GetYaxis().SetNdivisions(306)
			pull.GetXaxis().SetLabelSize(LS)
			pull.GetXaxis().SetTitleSize(LS)
			if not blindington:
				pull.Draw("hist")
			elif not vv[0]=="C":
				pull.Draw("hist")


			Fbinval = datahist.GetXaxis().GetBinLowEdge(1)
			Lbin=datahist.GetNbinsX()+1
			Lbinval = datahist.GetXaxis().GetBinLowEdge(Lbin)

			#print Fbinval,"to",Lbinval

			line2=ROOT.TLine(Fbinval,0.0,Lbinval,0.0)
			line2.SetLineColor(0)
			line1=ROOT.TLine(Fbinval,0.0,Lbinval,0.0)
			line1.SetLineStyle(2)

			line2.Draw()
			line1.Draw()


			if not sumomly:
				if setstring=="QCD":
					if not options.skipplots:
						c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__'+setstring+era+'.root', 'root')
						c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__'+setstring+era+'.pdf', 'pdf')
						c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__'+setstring+era+'.png', 'png')
				bkghist.SetMinimum(0.002)
				main.SetLogy()
				bkghist.SetMaximum(bkghist.GetMaximum()*100)			
				main.RedrawAxis()
				c1.Update()
				if setstring=="QCD":
					if not options.skipplots:
						c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__semilog__'+setstring+era+'.root', 'root')
						c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__semilog__'+setstring+era+'.pdf', 'pdf')
						c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__semilog__'+setstring+era+'.png', 'png')
				main.SetLogy(0)
				main.RedrawAxis()

			#timelogger["total"] = endtime-sttime
			#print timelogger


			if not isdata and wjetscorr!="MC" and wjetscorr!="None":
				temphist = wjetsfile.Get(curname+"__"+vv[1])
				temphist.Rebin(rebins[ihn])
				bkghist.Add(temphist)
				bkghistup.Add(temphist)
				bkghistdown.Add(temphist)

			if wjetscorr=="Corr":
				#print"CORRECTING QCD",bkghist.Integral()
				bkghist.Scale(wjcorr)
				#print"CORRECTING QCD",bkghist.Integral()
				bkghistup.Scale(wjcorr)
				bkghistdown.Scale(wjcorr)

			c2.cd()
			main.Draw()
			sub.Draw()

			main.cd()

			st1= ROOT.THStack("st1", "st1")
			bkghist.SetFillColor(ROOT.kYellow)
			tthist.SetFillColor(ROOT.kRed)
			tthist.SetStats(0)
			if withST:
				sthist.SetFillColor(ROOT.kMagenta)
				sthist.SetStats(0)
			if options.anatype=="Pho":
				gjetshist.SetFillColor(ROOT.kOrange)
				gjetshist.SetStats(0)
			if wjetscorr!="None":
				wjetshist.SetFillColor(ROOT.kGreen)
				wjetshist.SetStats(0)
				wjetsfrac = wjetshist.Integral()/bkghist.Integral()
				qcdfrac = 1.0-wjetshist.Integral()/bkghist.Integral()




			bkgwj = copy.deepcopy(bkghist)
			bkgqcd = copy.deepcopy(bkghist)



			if wjetscorr=="Corr":
				bkgqcd.Scale(qcdfrac)
				bkgwj.Scale(wjetsfrac)
				bkgwj.SetFillColor(ROOT.kYellow-2)
			if wjetscorr=="MC":
				bkgwj=wjetshist

			if options.anatype=="Pho":
				st1.Add(gjetshist)
			#	if "gjets" in sumhists[curname+"__"+vv[0]]:
			#		sumhists[curname+"__"+vv[0]]["gjets"].Add(gjetshist)
			#	else:
			#		sumhists[curname+"__"+vv[0]]["gjets"]=gjetshist)
			#print datahist.Integral(),tthist.Integral()
			if var=="msoftdropdef":
				st1.Add(bkgqcd)
				if withST:
					st1.Add(sthist)
				st1.Add(tthist)

				if wjetscorr!="None":
					st1.Add(bkgwj)


			else:
				st1.Add(tthist)
				if wjetscorr!="None":
					st1.Add(bkgwj)

				if withST:
					st1.Add(sthist)
				st1.Add(bkgqcd)

			st1.SetMaximum(max(st1.GetMaximum(),datahist.GetMaximum())*1.4)	
			st1.SetTitle(';'+xaxist+';Events/Bin')

		

			st1.Draw("hist")

			crange=None
			if var=="mass":
				if len(obj)==3:
					crange=[1000.0,8000.0]
				if len(obj)==2:
					#print "VLQ",obj
					crange=[200.0,6000.0]
			elif var=="pt":
				if obj=="B":
					crange=[200.0,2500.0]
				else:
					crange=[450.0,2500.0]
			elif var=="eta":
				crange=[-2.4,2.4]
			elif var=="msoftdropdef":
				crange=[120.0,300.0]
			if crange!=None:
				st1.GetXaxis().SetRangeUser(crange[0],crange[1])
			

			#if not isdata:
			#	if options.anatype=="Pho":
			#		datahist.Add(gjetshist)
			#	datahist.Add(tthist)
			#	if wjetscorr!="None":
			#		datahist.Add(wjetshist)
			#print  "blindington",blindington,vv[0]
			if not blindington:
				datahist.Draw("same")

			elif not vv[0]=="C":
				datahist.Draw("same")
			if vv[0]=="FT" and isdata and var!="msoftdropdef":
				print "RECORDING AVE TTSF"
				avettsfunc=0.5*abs((tthistuncs["ttag"][1].Integral()-tthistuncs["ttag"][0].Integral()))/tthist.Integral()
				print "RECORDING AVE TTSF",avettsfunc,tthistuncs["ttag"][1].Integral(),tthistuncs["ttag"][0].Integral(),tthist.Integral()
				
			if vv[0]=="FT" and isdata and var=="msoftdropdef" and  withST:
				ttvals = [datahist.Integral(),bkgqcd.Integral(),tthist.Integral(),sthist.Integral()]
				sigdat=sqrt(datahist.GetEntries())
				sigbkg=bkgqcd.Integral()
				sigttbar=sqrt(tthist.GetEntries())
				sigst=sthist.GetEntries()

				relerrnum=sqrt(sigdat*sigdat+sigbkg*sigbkg+sigst*sigst)/(datahist.Integral()-bkgqcd.Integral()-sthist.Integral())
				relerrden=sigttbar/tthist.GetEntries()
				#print "VERY BASIC ERRORS","dat",sigdat,"tt",relerrden*tthist.Integral(),"bkg",bkgqcd.Integral()

				tttnormsimple=(datahist.Integral()-bkgqcd.Integral()-sthist.Integral())/tthist.Integral()
				print "FAKING TTSYST",avettsfunc

				print tttnormsimple*sqrt(relerrnum*relerrnum+relerrden*relerrden),avettsfunc
				errsimple=sqrt((tttnormsimple*sqrt(relerrnum*relerrnum+relerrden*relerrden+avettsfunc*avettsfunc))**2)
				
				#print "tot",errsimple

			
			isig=0
			plottedsigs = {}
			bttp=[]
			zh=[]
			reso=10

			if options.dogcvlq:
				for it in xrange(reso+1):
					for jt in xrange(reso+1):
						if (it+jt<=reso+1):
							bttp.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
			else:
				bttp=[[0.5,0.5]]
			if options.dogczh:
				for it in xrange(reso+1):
					for jt in xrange(reso+1):
						if (it+jt<=reso+1):
							zh.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
			else:
				zh=[[0.5,0.5]]
			if options.anatype=="tHb" or options.anatype=="tZb":
					#print "Summing Sigs"
					if options.anatype=="tHb" or options.anatype=="tZb":

						for sigh in sorted(sighs):
							#print "Adding ",sigh,sighs[sigh].Integral()
							isZt=(sigh.split("_")[3])=="Zt"
							isHt=(sigh.split("_")[3])=="Ht"

							if isHt:
								Htname= sigh
								Ztname= sigh.replace("Ht","Zt")
								replnameHtTp = sigh.replace("BpT","TpB").replace("Bp","Tp")
								replnameHtBp = sigh.replace("TpB","BpT").replace("Tp","Bp")
								replnameZtTp = replnameHtTp.replace("Ht","Zt")
								replnameZtBp = replnameHtBp.replace("Ht","Zt")

								#print "Ht",sighs[sigh].Integral(),"Zt",sighs[Ztname].Integral()
								#print "comp ",replnameBp,replnameTp,sigh,sigh==replnameBp,sigh==replnameTp
								if replnameHtBp==sigh:
									for vlqc in bttp:
										for zhc in zh:

											resxsigHBp = copy.deepcopy(sighs[replnameHtBp])
											resxsigZBp = copy.deepcopy(sighs[replnameZtBp])
											resxsigHTp = copy.deepcopy(sighs[replnameHtTp])
											resxsigZTp = copy.deepcopy(sighs[replnameZtTp])

											resxsigHBp.Scale(vlqc[0]*zhc[0]/0.25)
											resxsigZBp.Scale(vlqc[0]*zhc[1]/0.25)
											resxsigHTp.Scale(vlqc[1]*zhc[0]/0.25)
											resxsigZTp.Scale(vlqc[1]*zhc[1]/0.25)

											summedsig = copy.deepcopy(resxsigHBp)
											summedsig.Add(resxsigZBp)
											summedsig.Add(resxsigHTp)
											summedsig.Add(resxsigZTp)

											#print summedsig.Integral()
											
											curhname = sigh.split("_")[0]+sigh.split("_")[1]+sigh.split("_")[2]
											if sigh.split("_")[-1] in ["up","down"]:
												curhname+="__"+sigh.split("__")[-2]+"__"+sigh.split("_")[-1]
											
											tempn=nobject+"__"+curhname
											curcomb="_B"+str(vlqc[0])+"T"+str(vlqc[1])+"H"+str(zhc[0])+"Z"+str(zhc[1])+"_"
											curcomb=curcomb.replace(".","p")
											filtnm=tempn.split("__")[1].replace("WpToBpT","WptoqVLQ").replace("Bp","VLQ")[:14]
											newsetname=filtnm[:10]+curcomb+filtnm[10:14]
											nametowrite = tempn.replace(tempn.split("__")[1],newsetname)
											sighssum[nametowrite]=summedsig
											sighssum[nametowrite].SetName(nametowrite)
											if writelim:
												limithistos[nametowrite]=sighssum[nametowrite]
												#print "NAME",sighssum[nametowrite].GetName()
											if curcomb=="_B0p5T0p5H0p5Z0p5_":
												#print "Found",sigh
												summedsig.SetLineColor(sigcolors[isig])
												summedsig.SetLineStyle(2)
												summedsig.SetLineWidth(2)

												if not (sigh.split("__")[-1] in ["up","down"]):
													wpmass = (sigh.split("_")[1])[2:6]


													lumi = constdict["lumi"]





													nev_xsec = constdict["dataconst"][replnameHtBp]
													#print "resxsigHBp",wpmass,100.*float(resxsigHBp.GetEntries())/nev_xsec[0]
													#print "weight",resxsigHBp.Integral()/float(resxsigHBp.GetEntries()),lumi*nev_xsec[1]*0.5/nev_xsec[0]
													#print "resxsigHBp",wpmass,100.*float(resxsigHBp.Integral())/(lumi*nev_xsec[1]*0.5),nev_xsec[1]
													#nevweighted=float(nev_xsec[0])
													if vv[0]=="C":
														if not (wpmass+"Ht" in allsigtoteff):
															allsigtoteff[wpmass+"Ht"]=lumi*nev_xsec[1]*0.5
															allsigneff[wpmass+"Ht"]=resxsigHBp.Integral()
														else :
															allsigtoteff[wpmass+"Ht"]+=lumi*nev_xsec[1]*0.5
															allsigneff[wpmass+"Ht"]+=resxsigHBp.Integral()
								

														nev_xsec = constdict["dataconst"][replnameZtBp]
														#print "resxsigZBp",wpmass,100.*float(resxsigZBp.GetEntries())/nev_xsec[0]
														#print "resxsigZBp",wpmass,100.*float(resxsigZBp.Integral())/(lumi*nev_xsec[1]*0.5),nev_xsec[1]
														#nevweighted=float(nev_xsec[0])
														if not (wpmass+"Zt" in allsigtoteff):
															allsigtoteff[wpmass+"Zt"]=lumi*nev_xsec[1]*0.5
															allsigneff[wpmass+"Zt"]=resxsigZBp.Integral()
														else :
															allsigtoteff[wpmass+"Zt"]+=lumi*nev_xsec[1]*0.5
															allsigneff[wpmass+"Zt"]+=resxsigZBp.Integral()


														nev_xsec = constdict["dataconst"][replnameHtTp]
														#print "resxsigHTp",wpmass,100.*float(resxsigHTp.GetEntries())/nev_xsec[0]
														#print "resxsigHTp",wpmass,100.*float(resxsigHTp.Integral())/(lumi*nev_xsec[1]*0.5),nev_xsec[1]
														#nevweighted=float(nev_xsec[0])
														allsigtoteff[wpmass+"Ht"]+=lumi*nev_xsec[1]*0.5
														allsigneff[wpmass+"Ht"]+=resxsigHTp.Integral()


														nev_xsec = constdict["dataconst"][replnameZtTp]
														#print "resxsigZTp",wpmass,100.*float(resxsigZTp.GetEntries())/nev_xsec[0]
														#print "resxsigZTp",wpmass,100.*float(resxsigZTp.Integral())/(lumi*nev_xsec[1]*0.5),nev_xsec[1]
														#nevweighted=float(nev_xsec[0])
														allsigtoteff[wpmass+"Zt"]+=lumi*nev_xsec[1]*0.5
														allsigneff[wpmass+"Zt"]+=resxsigZTp.Integral()



														#print "allsigneff",allsigneff												
														#print "allsigtoteff",allsigtoteff

														#print wpmass
													if wpmass in wpfilter:
														#print "plot"
														summedsig.Draw("samehist")
														plottedsigs[wpmass] = copy.deepcopy(summedsig)
														isig += 1
														#print "curname" ,curname,"sigh",sigh
														if sigh in sumhists[curname+"__"+vv[0]]:
															sumhists[curname+"__"+vv[0]][sigh].Add(summedsig)
														else:
															sumhists[curname+"__"+vv[0]][sigh]=summedsig
								#print "sigh",sigh
								#print "summedint",summedsig.Integral()
							
					#print sighs


			else:
				for sigh in sighs:

					sighs[sigh].SetLineColor(sigcolors[isig])
					sighs[sigh].SetLineWidth(2)
					sighs[sigh].SetLineStyle(2)
					#sighs[sigh].Scale(1./100.)
					sighs[sigh].Draw("samehist")
					isig+=1

			totalH = st1.GetStack().Last().Clone("totalH")
			#print "Bkg fracs"
			#print "QCD",bkgqcd.Integral(),100*(bkgqcd.Integral()/totalH.Integral()),"%"
			#print "WJets",bkgwj.Integral(),100*(bkgwj.Integral()/totalH.Integral()),"%"
			#print "ttbar",tthist.Integral(),100*(tthist.Integral()/totalH.Integral()),"%"
			#if options.anatype=="Pho":
			#	print "Gammajet",gjetshist.Integral(),100*(gjetshist.Integral()/totalH.Integral()),"%"
			#print "total:",totalH.Integral()
			#print "Data:",datahist.Integral()
			#hackerton
			ttnorms=[[ttbarnormcorr[1],ttbarnormcorr[1],ttbarnormcorr[0]]]
			
			totalHuperruncorr = copy.deepcopy(totalH)
			totalHdownerruncorr  = copy.deepcopy(totalH)

			qcduperruncorr = copy.deepcopy(totalH)
			qcddownerruncorr  = copy.deepcopy(totalH)

			totalHup = copy.deepcopy(totalH)
			totalHdown = copy.deepcopy(totalH)
			for bkgbin in xrange(totalHup.GetNbinsX()+1):
				#print
				upuncs = []
				downuncs = []


				upuncs.append(max(bkghistup.GetBinContent(bkgbin),bkghistdown.GetBinContent(bkgbin))-bkghist.GetBinContent(bkgbin))
				downuncs.append(min(bkghistup.GetBinContent(bkgbin),bkghistdown.GetBinContent(bkgbin))-bkghist.GetBinContent(bkgbin))
				#if not qcdmcbkg:
				if not qcdmcbkg:
					upuncstt = []
					downuncstt = []

					upuncstt.append(max(bkghistttup.GetBinContent(bkgbin),bkghistttdown.GetBinContent(bkgbin))-bkghist.GetBinContent(bkgbin))
					downuncstt.append(min(bkghistttup.GetBinContent(bkgbin),bkghistttdown.GetBinContent(bkgbin))-bkghist.GetBinContent(bkgbin))

					qcduperruncorr.SetBinContent(bkgbin,abs(upuncs[-1])*abs(upuncs[-1])+abs(upuncstt[-1])*abs(upuncstt[-1]))
					qcddownerruncorr.SetBinContent(bkgbin,abs(downuncs[-1])*abs(downuncs[-1])+abs(downuncstt[-1])*abs(downuncstt[-1]))

					upuncs.append(upuncstt[-1])
					downuncs.append(downuncstt[-1])

					for unc in tthistuncs:
						#print unc,"ttint",tthistuncs[unc][0].Integral(),tthistuncs[unc][1].Integral()
						upuncs.append(tthistuncs[unc][1].GetBinContent(bkgbin)-tthist.GetBinContent(bkgbin))
						downuncs.append(tthistuncs[unc][0].GetBinContent(bkgbin)-tthist.GetBinContent(bkgbin))
					for ttnorm in ttnorms:
						upuncs.append(ttnorm[1]*tthist.GetBinContent(bkgbin)*(1.0/ttnorm[2]))
						downuncs.append(-1.0*ttnorm[0]*tthist.GetBinContent(bkgbin)*(1.0/ttnorm[2]))

					upuncs.append(tthist.GetBinError(bkgbin))
					downuncs.append(-1.0*tthist.GetBinError(bkgbin))
					if withST:

						for unc in sthistuncs:

							upuncs.append(sthistuncs[unc][1].GetBinContent(bkgbin)-sthist.GetBinContent(bkgbin))
							downuncs.append(sthistuncs[unc][0].GetBinContent(bkgbin)-sthist.GetBinContent(bkgbin))
							#print unc,(upuncs[-1]-upuncs[-2])*0.5/max([sthist.GetBinContent(bkgbin),0.00001])
						upuncs.append(sthist.GetBinError(bkgbin))
						downuncs.append(-1.0*sthist.GetBinError(bkgbin))
				else:
	
					qcduperruncorr.SetBinContent(bkgbin,abs(upuncs[-1])*abs(upuncs[-1]))
					qcddownerruncorr.SetBinContent(bkgbin,abs(downuncs[-1])*abs(downuncs[-1]))

				#should be done earlier
				#upuncs.append(bkghist.GetBinError(bkgbin))
				#downuncs.append(-1.0*bkghist.GetBinError(bkgbin))
				fullup=0.0
				fulldown=0.0
				#print "newbin",bkgbin
				for un in xrange(len(upuncs)):
					#print "diffs",upuncs[un],downuncs[un]
					modup=max(0.0,upuncs[un],downuncs[un])
					moddown=min(0.0,upuncs[un],downuncs[un])
					#print "modup modown",modup,moddown
					fullup+=modup*modup
					fulldown+=moddown*moddown
				#print "cont",totalH.GetBinContent(bkgbin)
				totalHup.SetBinContent(bkgbin,totalH.GetBinContent(bkgbin)+sqrt(fullup)) 
				totalHdown.SetBinContent(bkgbin,totalH.GetBinContent(bkgbin)-sqrt(fulldown)) 
		
				totalHuperruncorr.SetBinContent(bkgbin,fullup)
				totalHdownerruncorr.SetBinContent(bkgbin,fulldown)
				
			totalHup.SetLineStyle(2)
			totalHdown.SetLineStyle(2)
			totalHup.SetFillColor(0)
			totalHdown.SetFillColor(0)


			yvmin = array('d')
			yvmax = array('d')
			xv = array('d')

			totbins = totalHup.GetNbinsX()
			for xbin in range(0,totbins+1):
				xv.append(totalHup.GetBinLowEdge(xbin))	
				xv.append(totalHup.GetBinLowEdge(xbin)+totalHup.GetBinWidth(xbin))	

				yvmax.append(totalHup.GetBinContent(xbin))
				yvmax.append(totalHup.GetBinContent(xbin))
				yvmin.append(totalHdown.GetBinContent(xbin))
				yvmin.append(totalHdown.GetBinContent(xbin))



			totpoints = len(xv)
		   	grshade = TGraph(2*totpoints);
			for xpoint in range(0,totpoints):
		     		grshade.SetPoint(xpoint,xv[xpoint],yvmax[xpoint])
		      		grshade.SetPoint(totpoints+xpoint,xv[totpoints-xpoint-1],yvmin[totpoints-xpoint-1])


			#totalHup.Draw("histsame")
			#totalHdown.Draw("histsame")

			grshade.Draw("f")
		   	grshade.SetFillStyle(3013);
		   	grshade.SetFillColor(1);

			if "data" in sumhists[curname+"__"+vv[0]]:
				sumhists[curname+"__"+vv[0]]["data"].Add(datahist)
				#sumhists[curname+"__"+vv[0]]["bkgup"].Add(totalHup)
				#sumhists[curname+"__"+vv[0]]["bkgdown"].Add(totalHdown)
				sumhists[curname+"__"+vv[0]]["qcd"].Add(bkgqcd)
				sumhists[curname+"__"+vv[0]]["tt"].Add(tthist)
				if withST:
					sumhists[curname+"__"+vv[0]]["st"].Add(sthist)
				
				sumhists[curname+"__"+vv[0]]["sqerrup"].Add(totalHuperruncorr)
				sumhists[curname+"__"+vv[0]]["sqerrdown"].Add(totalHdownerruncorr)
				sumhists[curname+"__"+vv[0]]["sqqcderrup"].Add(qcduperruncorr)
				sumhists[curname+"__"+vv[0]]["sqqcderrdown"].Add(qcddownerruncorr)
		
			else:
				sumhists[curname+"__"+vv[0]]["data"]=copy.deepcopy(datahist)
				#sumhists[curname+"__"+vv[0]]["bkgup"]=copy.deepcopy(totalHup)
				#sumhists[curname+"__"+vv[0]]["bkgdown"]=copy.deepcopy(totalHdown)
				sumhists[curname+"__"+vv[0]]["qcd"]=copy.deepcopy(bkgqcd)
				sumhists[curname+"__"+vv[0]]["tt"]=copy.deepcopy(tthist)
				if withST:
					sumhists[curname+"__"+vv[0]]["st"]=copy.deepcopy(sthist)

				sumhists[curname+"__"+vv[0]]["sqerrup"]=copy.deepcopy(totalHuperruncorr)
				sumhists[curname+"__"+vv[0]]["sqerrdown"]=copy.deepcopy(totalHdownerruncorr)
				sumhists[curname+"__"+vv[0]]["sqqcderrup"]=copy.deepcopy(qcduperruncorr)
				sumhists[curname+"__"+vv[0]]["sqqcderrdown"]=copy.deepcopy(qcddownerruncorr)
	
			leg = TLegend(0.60, 0.5, 0.84, 0.84)
			leg.SetFillColor(0)
			leg.SetBorderSize(0)
			leg.AddEntry( datahist, 'Data', 'PE')
			leg.AddEntry( bkgqcd, 'Data driven QCD', 'F')
			leg.AddEntry( tthist, 't#bar{t} Monte Carlo', 'F')
			if withST:
				leg.AddEntry( sthist, 'single-t Monte Carlo', 'F')
			leg.AddEntry( totalHup, '1#sigma background uncertainty', 'l')
			leg.AddEntry( grshade, '1#sigma background uncertainty', 'F')
			if wjetscorr!="None":
				leg.AddEntry( bkgwj, 'W+jets->QQ fraction', 'F')				
			for plotsig in sorted(plottedsigs):
				leg.AddEntry(plottedsigs[plotsig],"Wp at "+plotsig+"GeV","l")
			leg.Draw()
			prelim = TLatex()
			prelim.SetNDC()
			if not cutopt:
				prelim.DrawLatex( 0.2, 0.91, "Region: "+regiontoname[vv[0]] )
			c2.Update()
			sub.cd()

			pull = NanoF.Make_Pull_plot( datahist,totalH,totalHup,totalHdown )

			pull.SetFillColor(ROOT.kBlue)
			if var=="mass":
				xaxist = "M_{"+obj+"} [GeV]"
			elif var=="pt":
				xaxist = obj+" candidate p_{T} [GeV]"
			elif var=="eta":
				xaxist = obj+" candidate #eta"
			elif var=="msoftdropdef":
				xaxist = "top candidate softdrop mass [GeV]"
			else:
				xaxist = var+"("+obj+")"
			pull.SetTitle(';'+xaxist+';(Data-Bkg)/#sigma')
			pull.SetStats(0)


			pull.GetYaxis().SetRangeUser(-2.9,2.9)
			pull.GetXaxis().SetLabelSize(0.05)
			pull.GetYaxis().SetLabelSize(0.05)


			LS = .13

			pull.GetYaxis().SetTitleOffset(0.4)
			pull.GetXaxis().SetTitleOffset(0.9)
			pull.SetStats(0)
			    

			pull.GetYaxis().SetLabelSize(LS)
			pull.GetYaxis().SetTitleSize(LS)
			pull.GetYaxis().SetNdivisions(306)
			pull.GetXaxis().SetLabelSize(LS)
			pull.GetXaxis().SetTitleSize(LS)
			if crange!=None:
				pull.GetXaxis().SetRangeUser(crange[0],crange[1])
			if not blindington:
				pull.Draw("hist")
			elif not vv[0]=="C":
				pull.Draw("hist")
			else:
				pull.Scale(0)
				pull.Draw("hist")

			if crange!=None:
				Fbinval = crange[0]
				Lbinval = crange[1]
			else:
				Fbinval = datahist.GetXaxis().GetBinLowEdge(1)
				Lbin=datahist.GetNbinsX()+1
				Lbinval = datahist.GetXaxis().GetBinLowEdge(Lbin)

			#print Fbinval,"to",Lbinval

			line2=ROOT.TLine(Fbinval,0.0,Lbinval,0.0)
			line2.SetLineColor(0)
			line1=ROOT.TLine(Fbinval,0.0,Lbinval,0.0)
			line1.SetLineStyle(2)
			#print "Lowhigh"
			#print Fbinval,Lbinval
			#print crange
			line2.Draw()
			line1.Draw()
			if options.set=="JetHT":
				if era=="2016":
					per=1
				if era=="2017":
					per=2
				if era=="2018":
					per=3

				ROOT.insertlogo( main, per, 11 )
			if not sumomly:
				st1.SetMinimum(0.00001)
				if setstring=="JetHT":
					if not options.skipplots:
						c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__'+setstring+extex+era+'.root', 'root')
						c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__'+setstring+extex+era+'.pdf', 'pdf')
						c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__'+setstring+extex+era+'.png', 'png')
				st1.SetMinimum(0.01)
				st1.SetMaximum(max(st1.GetMaximum(),datahist.GetMaximum())*30)	
				main.SetLogy()
				main.RedrawAxis()
				c2.Update()
				if setstring=="JetHT":
					if not options.skipplots:
						c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__semilog__'+setstring+extex+era+'.root', 'root')
						c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__semilog__'+setstring+extex+era+'.pdf', 'pdf')
						c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__semilog__'+setstring+extex+era+'.png', 'png')

	#print "Writing limit histos"

	output = ROOT.TFile("limitsetting/theta/"+prestr+"_ForLimits__"+(options.era).replace(",","_")+genstr+".root","recreate")
	output.cd()
	nparts=10
	Bparr = []
	Tparr = []
	#for ll in limithistos:
	#	print ll
	for histon in limithistos:
		
		histo=limithistos[histon]
		#print "limithistos",histo.GetName()
		#print histo.GetName().split("__")[0].split("_")[2]
		if histo.GetName().split("__")[-1]=="DATA" and histo.GetName().split("__")[0].split("_")[2]=="C":
			#print "DATA"
			for xbin in range(0,totbins+1):
				print limithistos[histon].GetBinContent(xbin)
				if limithistos[histon].GetBinContent(xbin)<0.001:
					print "badbin"
		limithistos[histon].SetName(histo.GetName().replace("__up","__plus").replace("__down","__minus"))

		#limithistos[histon]
		#print limithistos[histon].GetName()
		#if (options.anatype=="tHb" or options.anatype=="tZb"):
		#	print limithistos[histon].GetName()
			#if histon.find("WpToBpT")!=-1:
			#	histonTp=histon.replace("BpT","TpB").replace("Bp","Tp")
				#print histonTp,histon
			#	try :
			#		histoTp=limithistos[histonTp]
			#	except:
			#		print "histo not found",histonTp
			#		continue
			#	histosum = copy.deepcopy(histo)
			#	histosum.Add(histoTp)
			#	#histosum.SetName(histon.replace("WpToBpT","WptoqVLQ").replace("Bp","VLQ"))
				#print "histon",histon
			#	charinid=histon.find("WpToBpT")
			#	newsetname=histon.split("__")[1].replace("WpToBpT","WptoqVLQ").replace("Bp","VLQ")[:14]
			#	histosum.SetName(histosum.GetName().replace(histon.split("__")[1],newsetname))
			#	histosum.SetTitle(histosum.GetName())
			#	histosum.Write()
			#elif histon.find("WpToTpB")!=-1:	
			#	pass
			#else:
			#	histo.SetTitle(histo.GetName())
			#	histo.Write()
		histo.SetTitle(histo.GetName())
		ZeroHist(histo)
		histo.Write()

	#print Tparr
	#print Bparr


	'''
	sys.exit()
	if (options.anatype=="tHb" or options.anatype=="tZb"):

		for ii in range(0,nparts+1):
			for jj in range(0,nparts+1):
				if ii==0 and jj==0:
					continue
				scalefacBp = float(jj)/(float(nparts)/2.0)
				scalefacTp = float(ii)/(float(nparts)/2.0)
				Tparr[ii].Add(Bparr[jj])
				if jj==1:
					#print Tparr[ii].GetName()
					sindex = (Tparr[ii].GetName()).find("Nar")
					#print sindex
					massstr= ((Tparr[ii].GetName())[sindex-4:sindex]).replace("p","")
					prestr = Tparr[ii].GetName().split("__")[0]
				Tparr[ii].SetName(prestr+"__"+("WptoVLQ_VLQ"+str(scalefacTp)+str(scalefacBp)).replace(".",""))
				Tparr[ii].SetTitle(Tparr[ii].GetName())
				print Tparr[ii].GetName()
				Tparr[ii].Write()
	output.Write()
	output.Close()
	'''



c3 = TCanvas('c3', '', 700, 600)

sumhistsunb={}
regfarray=[]
if options.postfit:
	datafiles=[]
	toplotr = ["C","K","H","F"]
	for reg in toplotr:
		plotrstr=""
		if reg!="C":
			plotrstr="_"+reg+"_"
		if reg!="C":
			combineglobs=glob.glob("/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/fitDiagnosticscentralWp*"+plotrstr+"datsys.txt.root")
		else:
			combineglobs=glob.glob("/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/fitDiagnosticscentralWp*0datsys.txt.root")
		print  "combineglobs",combineglobs
		regfarray.append([])
		regfarray[-1]={}
		for cg in combineglobs:
			substr = cg.split("/")[-1]
			sind = substr.find("Wp")
			eind = substr.find(plotrstr+"datsys")
			#print reg
			#if reg!="C":
			#	eind -= 3
			#print eind-sind
			substr=substr[sind:eind]
			#print plotrstr+"datsys",substr
			regfarray[-1][substr]=TFile(cg,"open")
		combinefile=regfarray[-1][substr]
		#print "combineglobs",combineglobs
		fold="shapes_fit_b/"
		#fold="shapes_prefit/"
		anastr=""
		if options.anatype=="tZb":
			anastr="TZB"
		if options.anatype=="tHb":
			anastr="THB"
		for era in eras:
			settofind="JetHT__Run"+era
			datafiles.append(TFile(rootfolder+prestr+"Ana"+era+"__"+settofind+".root","open"))
			if "mass__"+anastr+"__"+reg in sumhistsunb:
					sumhistsunb["mass__"+anastr+"__"+reg]["qcd"].Add(combinefile.Get(fold+options.anatype+era+"/qcd"))
					if withST:
						sumhistsunb["mass__"+anastr+"__"+reg]["st"].Add(combinefile.Get(fold+options.anatype+era+"/st"))
					sumhistsunb["mass__"+anastr+"__"+reg]["tt"].Add(combinefile.Get(fold+options.anatype+era+"/ttbar"))
					sumhistsunb["mass__"+anastr+"__"+reg]["data"].Add(datafiles[-1].Get("mass__"+anastr+"__"+reg))
					sumhistsunb["mass__"+anastr+"__"+reg]["total"].Add(combinefile.Get(fold+options.anatype+era+"/total"))
					for cf in regfarray[-1]:		
						sumhistsunb["mass__"+anastr+"__"+reg][cf].Add(regfarray[-1][cf].Get("shapes_prefit/"+options.anatype+era+"/"+cf))
			else:
					sumhistsunb["mass__"+anastr+"__"+reg]={}
					sumhistsunb["mass__"+anastr+"__"+reg]["qcd"]= combinefile.Get(fold+options.anatype+era+"/qcd")
					if withST:
						sumhistsunb["mass__"+anastr+"__"+reg]["st"]= combinefile.Get(fold+options.anatype+era+"/st")
					sumhistsunb["mass__"+anastr+"__"+reg]["tt"]= combinefile.Get(fold+options.anatype+era+"/ttbar")
					sumhistsunb["mass__"+anastr+"__"+reg]["data"]= datafiles[-1].Get("mass__"+anastr+"__"+reg)
					sumhistsunb["mass__"+anastr+"__"+reg]["total"]= combinefile.Get(fold+options.anatype+era+"/total")
					for cf in regfarray[-1]:			
						sumhistsunb["mass__"+anastr+"__"+reg][cf]=regfarray[-1][cf].Get("shapes_prefit/"+options.anatype+era+"/"+cf)
			print "mass__"+anastr+"__"+reg,sumhistsunb["mass__"+anastr+"__"+reg]["data"].Integral()

		sumhists["mass__"+anastr+"__"+reg]={}
		sumhists["mass__"+anastr+"__"+reg]["data"] = sumhistsunb["mass__"+anastr+"__"+reg]["data"]
		sumhists["mass__"+anastr+"__"+reg]["data"] = sumhistsunb["mass__"+anastr+"__"+reg]["data"].Rebin(len(bins2)-1,sumhistsunb["mass__"+anastr+"__"+reg]["data"].GetName()+"TEMP",bins2)
		print "mass__"+anastr+"__"+reg,sumhists["mass__"+anastr+"__"+reg]["data"].Integral()

	for ss in sumhistsunb:
		for hh in sumhistsunb[ss]:
			sumhists[ss][hh]=copy.deepcopy(sumhists[ss]["data"])
			if hh=="data":
				continue
			#print hh,sumhists[ss][hh].Integral()
		
			for bb in xrange(sumhists[ss][hh].GetNbinsX()+1):
				sumhists[ss][hh].SetBinContent(bb,sumhistsunb[ss][hh].GetBinContent(bb))
				#sumhists[ss][hh].SetBinError(bb,sumhistsunb[ss][hh].GetBinError(bb))
				#sumhists[ss][hh].SetBinErrorLow(bb,sumhistsunb[ss][hh].GetBinErrorLow(bb))
			#print hh,sumhists[ss][hh].Integral()


else:

	print "allsigneff",allsigneff
	print "allsigtoteff",allsigtoteff


	for asig in sorted(allsigneff):
		print asig,allsigneff[asig]/allsigtoteff[asig]*100.
	print options.era,"ttttvals",ttvals
	print options.era,"ttnormsimple",tttnormsimple,errsimple



if len(eras)==1:
	sys.exit()

for sumhist in sumhists:
	curhset = sumhists[sumhist]
	print sumhist,curhset,curhset["data"].Integral()
	

	main = ROOT.TPad("main", "main", 0, 0.3, 1, 1)
	sub = ROOT.TPad("sub", "sub", 0, 0, 1, 0.3)

	main.SetLeftMargin(0.16)
	main.SetRightMargin(0.05)
	main.SetTopMargin(0.11)
	main.SetBottomMargin(0.0)

	sub.SetLeftMargin(0.16)
	sub.SetRightMargin(0.05)
	sub.SetTopMargin(0)
	sub.SetBottomMargin(0.3)
	c3.cd()
	main.Draw()
	sub.Draw()

	main.cd()

	st1= ROOT.THStack("st1", "st1")
	curhset["qcd"].SetFillColor(ROOT.kYellow)
	curhset["tt"].SetFillColor(ROOT.kRed)
	curhset["tt"].SetStats(0)
	if withST:
		curhset["st"].SetFillColor(ROOT.kMagenta)
	curhset["data"].SetMarkerStyle(20)	
	curhset["data"].SetLineColor(1)
	var = sumhist.split("__")[0]
	crange=None
	obj = sumhist.split("__")[1]
	reg  = sumhist.split("__")[2]
	if var=="mass":
			if len(obj)==3:
				crange=[1000.0,8000.0]
			if len(obj)==2:
				crange=[200.0,6000.0]
	elif var=="pt":
			if obj=="B":
				crange=[200.0,2500.0]
			else:
				crange=[450.0,2500.0]
	elif var=="eta":
			crange=[-2.4,2.4]
	elif var=="msoftdropdef":
			crange=[120.0,300.0]
			

	if var=="msoftdropdef":
		st1.Add(curhset["qcd"])
		if withST:
			st1.Add(curhset["st"])
		st1.Add(curhset["tt"])
	else:
		st1.Add(curhset["tt"])
		if withST:
			st1.Add(curhset["st"])
		st1.Add(curhset["qcd"])
	print "reg",reg,"obj",obj,"var",var
	if options.postfit:
		xaxist = "M_{"+obj+"} [GeV]"
	if setstring!="QCD":
		st1.SetMaximum(max(st1.GetMaximum(),curhset["data"].GetMaximum())*1.4)	
		st1.SetTitle(';'+xaxist+';Events/Bin')
		st1.Draw("hist")
		st1.GetYaxis().SetLabelSize(.05)
		st1.GetYaxis().SetTitleSize(.05)
		st1.GetYaxis().SetTitleOffset(1.4)
		totalH = st1.GetStack().Last().Clone("totalH")
		if crange!=None:
			st1.GetXaxis().SetRangeUser(crange[0],crange[1])
	else:
		totalH=curhset["qcd"]
		qcdl=copy.deepcopy(curhset["qcd"])
		qcdl.SetFillColor(0)
		qcdl.SetMaximum(max(qcdl.GetMaximum(),curhset["data"].GetMaximum())*2.4)	
		qcdl.SetTitle(';'+xaxist+';Events/Bin')
		qcdl.GetYaxis().SetLabelSize(.05)
		qcdl.GetYaxis().SetTitleSize(.05)
		if crange!=None:
			qcdl.GetXaxis().SetRangeUser(crange[0],crange[1])
		qcdl.Draw("hist")

	if not blindington:
		curhset["data"].Draw("same")
	elif not reg=="C":
		curhset["data"].Draw("same")
	else:
		print "not drawing",reg+'__'+var

	if options.postfit:	
		bkgup= copy.deepcopy(curhset["total"])
		bkgdown= copy.deepcopy(curhset["total"])
		bkgup.Scale(0.0)
		bkgdown.Scale(0.0)
		for bb in xrange(curhset["total"].GetNbinsX()+1):
			bkgdown.SetBinContent(bb,curhset["total"].GetBinContent(bb)-sumhistsunb[sumhist]["total"].GetBinErrorLow(bb))
			bkgup.SetBinContent(bb,curhset["total"].GetBinContent(bb)+sumhistsunb[sumhist]["total"].GetBinErrorUp(bb))
		print sumhist,sumhists["mass__"+anastr+"__"+reg]["data"].Integral()
	else:
		errup= copy.deepcopy(curhset["sqerrup"])
		errdown= copy.deepcopy(curhset["sqerrdown"])
		qcderrup= copy.deepcopy(curhset["sqqcderrup"])
		qcderrdown= copy.deepcopy(curhset["sqqcderrdown"])
		for bkgbin in xrange(curhset["sqerrup"].GetNbinsX()+1):
			errup.SetBinContent(bkgbin,sqrt(curhset["sqerrup"].GetBinContent(bkgbin)))
			errdown.SetBinContent(bkgbin,sqrt(curhset["sqerrdown"].GetBinContent(bkgbin)))
			qcderrup.SetBinContent(bkgbin,sqrt(curhset["sqqcderrup"].GetBinContent(bkgbin)))
			qcderrdown.SetBinContent(bkgbin,sqrt(curhset["sqqcderrdown"].GetBinContent(bkgbin)))
		if setstring!="QCD":
			bkgup= copy.deepcopy(totalH)
			bkgdown= copy.deepcopy(totalH)
			bkgup.Add(errup)
			bkgdown.Add(errdown,-1.0)

		else:
			bkgup= copy.deepcopy(curhset["qcd"])
			bkgdown= copy.deepcopy(curhset["qcd"])
			bkgup.Add(qcderrup)
			bkgdown.Add(qcderrdown,-1.0)

		bkgup.SetLineStyle(2)
		bkgdown.SetLineStyle(2)
		bkgup.SetFillColor(0)
		bkgdown.SetFillColor(0)




	yvmin = array('d')
	yvmax = array('d')
	xv = array('d')

	totbins = bkgup.GetNbinsX()
	for xbin in range(0,totbins+1):
		xv.append(bkgup.GetBinLowEdge(xbin))	
		xv.append(bkgup.GetBinLowEdge(xbin)+bkgup.GetBinWidth(xbin))	

		yvmax.append(bkgup.GetBinContent(xbin))
		yvmax.append(bkgup.GetBinContent(xbin))
		yvmin.append(bkgdown.GetBinContent(xbin))
		yvmin.append(bkgdown.GetBinContent(xbin))




	totpoints = len(xv)
	grshade = TGraph(2*totpoints);
	for xpoint in range(0,totpoints):
		     	grshade.SetPoint(xpoint,xv[xpoint],yvmax[xpoint])
		      	grshade.SetPoint(totpoints+xpoint,xv[totpoints-xpoint-1],yvmin[totpoints-xpoint-1])


	grshade.Draw("f")
  	grshade.SetFillStyle(3013)
	grshade.SetFillColor(1)

	leg = TLegend(0.55, 0.5, 0.84, 0.84)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	if setstring!="QCD":
		leg.AddEntry( curhset["data"], 'Data', 'P')
		leg.AddEntry( curhset["qcd"], 'Data driven QCD', 'F')
		leg.AddEntry( curhset["tt"], 't#bar{t} Monte Carlo', 'F')
		if withST:
			leg.AddEntry( curhset["st"], 'single-t Monte Carlo', 'F')
		leg.AddEntry( grshade, '1#sigma background uncertainty', 'F')


		print curhset
		isig=0
		for ch in curhset:
			if ch.find("Wp")!=-1:
				curwpm=""
				if options.postfit:
					if not (ch in ["Wp2000","Wp3000","Wp4000"]):
						continue
					curwpm=ch.replace("Wp","")
				else:
					curwpm=ch.split("_")[1].replace("Wp","").replace("Nar","")

				if setstring!="QCD":
					
					curhset[ch].Draw("samehist")

					curhset[ch].SetLineColor(sigcolors[isig])
					curhset[ch].SetLineWidth(2)
					curhset[ch].SetLineStyle(2)
					leg.AddEntry( curhset[ch], 'Signal at '+curwpm+' GeV', 'l')
					isig+=1
			

	else:
		leg.AddEntry( curhset["data"], 'QCD MC selection', 'P')
		leg.AddEntry( qcdl, 'QCD background estimate', 'l')
		leg.AddEntry( grshade, '1#sigma background uncertainty', 'F')

	leg.Draw()
	prelim = TLatex()
	prelim.SetNDC()
	prelim.DrawLatex( 0.2, 0.91, "Region: "+regiontoname[reg] )




	c3.Update()
	sub.cd()

	pull = NanoF.Make_Pull_plot( curhset["data"],totalH,bkgup,bkgdown )

	pull.SetFillColor(ROOT.kBlue)
	if var=="mass":
				xaxist = "M_{"+obj+"} [GeV]"

	elif var=="pt":
				xaxist = obj+" candidate p_{T} [GeV]"
	elif var=="eta":
				xaxist = obj+" candidate #eta"
	elif var=="msoftdropdef":
				xaxist = "top candidate softdrop mass [GeV]"
	else:
				xaxist = var+"("+obj+")"
	pull.SetTitle(';'+xaxist+';(Data-Bkg)/#sigma')
	pull.SetStats(0)

	pull.GetYaxis().SetRangeUser(-2.9,2.9)
	pull.GetXaxis().SetLabelSize(0.05)
	pull.GetYaxis().SetLabelSize(0.05)


	LS = .13

	pull.GetYaxis().SetTitleOffset(0.4)
	pull.GetXaxis().SetTitleOffset(0.9)
	pull.SetStats(0)
			    

	pull.GetYaxis().SetLabelSize(LS)
	pull.GetYaxis().SetTitleSize(LS)
	pull.GetYaxis().SetNdivisions(306)
	pull.GetXaxis().SetLabelSize(LS)
	pull.GetXaxis().SetTitleSize(LS)






	if crange!=None:
		pull.GetXaxis().SetRangeUser(crange[0],crange[1])

	if not blindington:
		pull.Draw("hist")
	elif not reg=="C":
		pull.Draw("hist")
	else:
		pull.Scale(0)
		pull.GetYaxis().SetRangeUser(-2.9,2.9)
		pull.Draw("hist")

		print "not drawing",reg+'__'+var
	if crange!=None:
		Fbinval = crange[0]
		Lbinval = crange[1]
	else:
		Fbinval = pull.GetXaxis().GetBinLowEdge(1)
		Lbin=pull.GetNbinsX()+1
		Lbinval = pull.GetXaxis().GetBinLowEdge(Lbin)


	line2=ROOT.TLine(Fbinval,0.0,Lbinval,0.0)
	line2.SetLineColor(0)
	line1=ROOT.TLine(Fbinval,0.0,Lbinval,0.0)
	line1.SetLineStyle(2)

	line2.Draw()
	line1.Draw()
	if options.set=="JetHT":
		per=3
		if ("2017" in eras) and ("2018" in eras):
			per=4
		if ("2016" in eras) and ("2017" in eras) and ("2018" in eras):
			per=5
		ROOT.insertlogo( main, per, 11 )


	st1.SetMinimum(0.00001)

	if setstring!="QCD":	
		st1.SetMinimum(0.00001)
	else:	
		qcdl.SetMinimum(0.00001)

	if not options.skipplots:
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__'+setstring+extex+pftex+sumera+'.root', 'root')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__'+setstring+extex+pftex+sumera+'.pdf', 'pdf')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__'+setstring+extex+pftex+sumera+'.png', 'png')
		


	if setstring!="QCD":
		st1.SetMinimum(0.1)
		st1.SetMaximum(max(st1.GetMaximum(),curhset["data"].GetMaximum())*30)	

	else:	
		qcdl.SetMinimum(0.1)
		qcdl.SetMaximum(max(st1.GetMaximum(),curhset["data"].GetMaximum())*30)

	main.SetLogy()
	main.RedrawAxis()
	c3.Update()
	if not options.skipplots:
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__semilog__'+setstring+extex+pftex+sumera+'.root', 'root')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__semilog__'+setstring+extex+pftex+sumera+'.pdf', 'pdf')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__semilog__'+setstring+extex+pftex+sumera+'.png', 'png')


print "Completed..."																										

