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


(options, args) = parser.parse_args()

regiontoname=	{
		"C":"Signal",
		"K":"Loose t",
		"H":"Loose V",
		"F":"Validation",
		"FT":"ttbar measurement",
		}


rootfolder=options.rootfolder+"/"
setname = options.set
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True
extex=""
if options.normcorr:
	extex="__ttnorm"

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
for era in eras:
	sumera+=era
	setname =options.set
	NanoF = NanoAODskim_Functions(options.anatype,era)
	labels = NanoF.labels 
	candl = NanoF.candl
	probl = NanoF.probl
	wjetscorr=options.wjets

	uncs=["pu","trig","q2","btag","jes","jer"]
	corruncs=["pu","q2"]
	uncorruncs=["trig","btag","jes","jer"]
	if "H" in labels:
		uncs.append("htag")
	#if "Z" in labels:
	#	uncs.append("wtag")
	uncnames=["mass","pt","eta"]
	prestr="NanoAODskim_"+optstr+options.anatype
	if options.wjets!="None":
		extex+="__WJ"+wjetscorr
	if isdata:
		datafile=TFile(rootfolder+prestr+"Ana"+era+"__JetHT.root","open")
	else:
		datafile=TFile(rootfolder+prestr+"Ana"+era+"__QCD.root","open")
	QCDfile=TFile(rootfolder+prestr+"Ana"+era+"__QCD.root","open")
	ttfile=TFile(rootfolder+prestr+"Ana"+era+"__TT.root","open")

	if options.anatype=="Pho":
		gjetsfile=TFile(rootfolder+prestr+"Ana"+era+"__GJets.root","open")
	if wjetscorr!="None":
		wjetsfile=TFile(rootfolder+prestr+"Ana"+era+"__WJets.root","open")
	sigfiles=[]
	sigyearforplotting=era
	if options.anatype=="Pho":
		sigfiles=glob.glob(rootfolder+prestr+"Ana"+era+"__WkkToRWToTri_*.root")
	if options.anatype=="WW":
		sigfiles=glob.glob(rootfolder+prestr+"Ana"+era+"__WkkToWRadionToWWW_M*.root")
	genmatrix = NanoF.genmatrix
	#print genmatrix
	#if cutopt:
	#	genmatrix=[[3000, [1700, 2000, 2300]]]
	genindex=1
	if options.anatype=="tZb":
		sigfiles=[]
		for gg in genmatrix:
			#print gg
			wpm=gg[0]
			if wpm==5500 or  wpm==5000 or wpm==2500:
				continue
			vlqm=gg[1][genindex]
			#print wpm,vlqm
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToBpT_Wp"+str(wpm)+"Nar_Bp"+str(vlqm)+"Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToTpB_Wp"+str(wpm)+"Nar_Tp"+str(vlqm)+"Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")

	if options.anatype=="tHb":
		sigfiles=[]
		for gg in genmatrix:
			#print gg
			wpm=gg[0]
			if wpm==5500 or  wpm==5000 or wpm==2500:
				continue
			vlqm=gg[1][genindex]
			#print wpm,vlqm
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToBpT_Wp"+str(wpm)+"Nar_Bp"+str(vlqm)+"Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
			sigfiles.append(rootfolder+prestr+"Ana"+sigyearforplotting+"__WpToTpB_Wp"+str(wpm)+"Nar_Tp"+str(vlqm)+"Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")

	if qcdmcbkg:
		qcdfile=TFile(rootfolder+prestr+"Ana"+era+"__QCD.root","open")

	sigfs = {}

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
	for sigf in sigfiles:
		sigfs[sigf.split("__")[1].replace(".root","")]=TFile(sigf,"open")
	histonames=[]
	rebins=[]
	invmnames =[]

	constdict = NanoF.LoadConstants
	#print constdict
	ttbarnormcorr=constdict['ttrenorm']
	#print ttbarnormcorr
	for lab in labels:

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
				histonames.append("msoftdrop__"+lab)
				rebins.append(rebinsd)
	limithistos = {}


	blindington = False
	if options.set=="JetHT":
		blindington = True

	vers = [["C","D"],["F","G"],["K","L"],["H","I"]]
	if cutopt:
		vers = [['C'],['CFH1'],['CFH2'],['CFH3'],['CFT1'],['CFT2'],['CFT3'],['CFB1'],['CFB2'],['HFH1'],['HFH2'],['HFH3'],['KFT1'],['KFT2'],['KFT3']]

	#if options.anatype=="tHb" or options.anatype=="tZb":
		#vers.append(["N","O"])
	if options.anatype=="tHb" and not cutopt:
		vers.append(["FT","FTR"])
	tttnormsimple=None
	errsimple=None

	ttvals=None
	limsetregions=["C","K","H"]
	if cutopt:
		limsetregions=['C','CFH1','CFH2','CFH3','CFT1','CFT2','CFT3','CFB1','CFB2','HFH1','HFH2','HFH3','KFT1','KFT2','KFT3']
	for vv in vers:
		for ihn in xrange(len(histonames)):

			curname = histonames[ihn]
			if not (curname+"__"+vv[0] in sumhists):
				sumhists[curname+"__"+vv[0]]={}
			writelim=False
			#print vv[0],limsetregions,vv[0] in limsetregions
			if (curname in invmnames) and (vv[0] in limsetregions):
				writelim=True
			sighs = {}

			datahist = datafile.Get(curname+"__"+vv[0])
			#print curname+"__"+vv[0]
			#print datahist.GetName()
			nobject = datahist.GetName().split("__")[0]+"_"+datahist.GetName().split("__")[1]
			nobject+="_"+vv[0]+"_"+options.era
			#print datafile
			#print curname+"__"+vv[0]
			datahist.Rebin(rebins[ihn])
			#print datafile,curname+"__"+vv[1]+"_0"
			if qcdmcbkg:
				bkghist = qcdfile.Get(curname+"__"+vv[0])
			else:
				bkghist = datafile.Get(curname+"__"+vv[1]+"_0")
				bkghist.Add(datafile.Get(curname+"__"+vv[1]+"_1"))

			if isdata and (not qcdmcbkg):

				bkgtosubtract = [ttfile]
				if options.anatype=="Pho":
					bkgtosubtract.append(gjetsfile)
				if wjetscorr=="MC" and wjetscorr!="None":
					bkgtosubtract.append(wjetsfile)
				print curname+"__"+vv[1]
				for bkgs in bkgtosubtract:
					print bkgs
					temphist = bkgs.Get(curname+"__"+vv[1])
					#print bkghist.Integral(),"M",temphist.Integral()
					bkghist.Add(temphist,-1)
			bkghist.Rebin(rebins[ihn])
			#QCD==wjets+qcd!!
			if wjetscorr!="None":
				wjetshist = wjetsfile.Get(curname+"__"+vv[0])

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
			tthist.Rebin(rebins[ihn])
			tthistuncs = {}
			bkghist.SetMaximum(max(bkghist.GetMaximum(),datahist.GetMaximum())*1.4)
			obj=curname.split("__")[1]
			var=curname.split("__")[0]
			#print  var,uncnames
			if var in uncnames:
				for unc in uncs:
					#print unc,curname+"__"+vv[0]+"__"+unc+"__down",curname+"__"+vv[0]+"__"+unc+"__up"
					tthistuncs[unc]=[ttfile.Get(curname+"__"+vv[0]+"__"+unc+"__down"),ttfile.Get(curname+"__"+vv[0]+"__"+unc+"__up")]
					if writelim:
						appstr=""
						if unc in uncorruncs:
							appstr=options.era

						tthistuncs[unc][0].SetName(nobject+"__ttbar__"+unc+appstr+"__down")
						limithistos[tthistuncs[unc][0].GetName()] = tthistuncs[unc][0]

						tthistuncs[unc][1].SetName(nobject+"__ttbar__"+unc+appstr+"__up")
						limithistos[tthistuncs[unc][1].GetName()]=tthistuncs[unc][1]
					tthistuncs[unc][0].Rebin(rebins[ihn])
					tthistuncs[unc][1].Rebin(rebins[ihn])

			if options.anatype=="Pho":
				gjetshist = gjetsfile.Get(curname+"__"+vv[0])

			for sigf in sigfiles:
				#print sigf
				sindex = sigf.split("__")[1].replace(".root","")
				sighs[sindex]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0])
				if var in uncnames:
					for unc in uncs:
						appstr=""
						if unc in uncorruncs:
							appstr=options.era
						#print curname+"__"+vv[0]+"__"+unc+"__down"
						sighs[sindex+"__"+unc+appstr+"__down"]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0]+"__"+unc+"__down")
						sighs[sindex+"__"+unc+appstr+"__up"]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0]+"__"+unc+"__up")
						sighs[sindex+"__"+unc+appstr+"__down"].SetName(curname+"__"+vv[0]+"__"+unc+appstr+"__down")
						sighs[sindex+"__"+unc+appstr+"__up"].SetName(curname+"__"+vv[0]+"__"+unc+appstr+"__up")
		
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
			if qcdmcbkg:
				errhist.Scale(0.1)
				errhistcorr.Scale(0.1)
			else:
				for xbin in xrange(errhist.GetNbinsX()+1):
					cont=0.0
					contcorr=0.0
					fullcont = 0.0
					for lbin in xrange(2):
						for ybin in xrange(nbins+1):
							#print "bbin"+str(ybin)+"__"+candl+"__"+curname+"__D__err_"+str(lbin)
							bbinhistserr = copy.deepcopy(datafile.Get("bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]+"__err_"+str(lbin)))
							bbinhistscont = copy.deepcopy(datafile.Get("bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]))
							#print "bbin"+str(ybin)+"__"+candl+"__"+curname+"__"+vv[1]+"__err_"+str(lbin)
							bbinhistserr.RebinY(rebins[ihn])
							bbinhistscont.RebinY(rebins[ihn])

							errpoint = bbinhistserr.GetYaxis().GetBinCenter(xbin)
							for errbin in xrange(bbinhistserr.GetNbinsX()+1):
								cont += bbinhistserr.GetBinContent(errbin,xbin)*bbinhistserr.GetBinContent(errbin,xbin)
								contcorr += bbinhistserr.GetBinContent(errbin,xbin)
								#print 		
								#print ybin		
								#print errhist.GetBinCenter(xbin),bbinhistserr.GetBinContent(errbin,xbin)
								#print errhist.GetBinCenter(xbin),contcorr
							for errbin1 in xrange(bbinhistscont.GetNbinsX()+1):
								fullcont += bbinhistscont.GetBinContent(errbin1,xbin)
								#print			
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
					conthist.SetBinContent(xbin,fullcont)
					#print errhist.GetXaxis().GetBinCenter(xbin),errpoint
					if errhist.GetXaxis().GetBinCenter(xbin)!=errpoint:
						logging.error("Inconsistent Binning "+str(errhist.GetXaxis().GetBinCenter(xbin))+" "+str(errpoint))
					
				#print "5"
				#print conthist.Integral()
				#print bkghist.Integral()



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
				bkghistup.SetName(nobject+"__qcd__bkg__up")
				bkghistdown.SetName(nobject+"__qcd__bkg__down")



				#limithistos.append(datahist)
				limithistos[tthist.GetName()]=tthist
				if options.anatype=="Pho":
					limithistos[gjetshist.GetName()]=gjetshist
				#limithistos.append(wjetshist)
				limithistos[bkghist.GetName()]=bkghist
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
						if options.anatype=="tHb" or options.anatype=="tZb":
							#print sigh,sighs[sigh].GetName()
							curhname = sigh.split("_")[0]+sigh.split("_")[1]+sigh.split("_")[2]
							
							#print curhname,sigh
							if sigh.split("_")[-1] in ["up","down"]:
								curhname+="__"+sigh.split("__")[-2]+"__"+sigh.split("_")[-1]
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
			#print datahist.Integral(),bkghist.Integral(),bkghistup.Integral(),bkghistdown.Integral()
			
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
				bkghist.SetMinimum(0.01)
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
			if var=="msoftdrop":
				st1.Add(bkgqcd)
				st1.Add(tthist)
				if wjetscorr!="None":
					st1.Add(bkgwj)


			else:
				st1.Add(tthist)
				if wjetscorr!="None":
					st1.Add(bkgwj)

				st1.Add(bkgqcd)

			st1.SetMaximum(max(st1.GetMaximum(),datahist.GetMaximum())*1.4)	
			st1.SetTitle(';'+xaxist+';Events/Bin')

		

			st1.Draw("hist")

			crange=None
			if var=="mass":
				if len(obj)==3:
					crange=[900.0,7000.0]
				if len(obj)==2:
					crange=[900.0,7000.0]
			elif var=="pt":
				if obj=="B":
					crange=[200.0,2500.0]
				else:
					crange=[450.0,2500.0]
			elif var=="eta":
				crange=[-2.4,2.4]
			elif var=="msoftdrop":
				crange=[120.0,300.0]
			if crange!=None:
				st1.GetXaxis().SetRangeUser(crange[0],crange[1])
			

			#if not isdata:
			#	if options.anatype=="Pho":
			#		datahist.Add(gjetshist)
			#	datahist.Add(tthist)
			#	if wjetscorr!="None":
			#		datahist.Add(wjetshist)
			if not blindington:
				datahist.Draw("same")

			elif not vv[0]=="C":
				datahist.Draw("same")
			if vv[0]=="FT" and isdata and var=="msoftdrop":
				ttvals = [datahist.Integral(),bkgqcd.Integral(),tthist.Integral()]
				sigdat=sqrt(datahist.GetEntries())
				sigbkg=bkgqcd.Integral()
				sigttbar=sqrt(tthist.GetEntries())

				relerrnum=sqrt(sigdat*sigdat+sigbkg*sigbkg)/(datahist.Integral()-bkgqcd.Integral())
				relerrden=sigttbar/tthist.GetEntries()
				#print "VERY BASIC ERRORS","dat",sigdat,"tt",relerrden*tthist.Integral(),"bkg",bkgqcd.Integral()

				tttnormsimple=(datahist.Integral()-bkgqcd.Integral())/tthist.Integral()
				errsimple=tttnormsimple*sqrt(relerrnum*relerrnum+relerrden*relerrden)

				#print "tot",errsimple

			sigcolors = [1,2,3,4,5,6,7,8,9,10]
			isig=0
			if options.anatype=="tHb" or options.anatype=="tZb":
					#print "Summing Sigs"
					nsigs = 0
					if options.anatype=="tHb" or options.anatype=="tZb":

						for sigh in sighs:
							#print "Adding ",sigh,sighs[sigh].Integral()
							replnameBp = sigh.replace("BpT","TpB").replace("Bp","Tp")
							replnameTp = sigh.replace("TpB","BpT").replace("Tp","Bp")
							#print "comp ",replnameBp,replnameTp,sigh,sigh==replnameBp,sigh==replnameTp
							if replnameBp==sigh:
								summedsig = copy.deepcopy(sighs[sigh])
								#print "pradd",summedsig.Integral()
								summedsig.Add(sighs[replnameTp])
								#print "postadd",summedsig.Integral()
								summedsig.SetLineColor(sigcolors[isig+2])
								summedsig.Draw("samehist")

								if sigh in sumhists[curname+"__"+vv[0]]:
									sumhists[curname+"__"+vv[0]][sigh].Add(summedsig)
								else:
									sumhists[curname+"__"+vv[0]][sigh]=summedsig
							#print "sigh",sigh
							#print "summedint",summedsig.Integral()
							nsigs += 1
					#print sighs


			else:
				for sigh in sighs:
					#print sigh
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
				upuncs = []
				downuncs = []

				upuncs.append(bkghistup.GetBinContent(bkgbin)-bkghist.GetBinContent(bkgbin))
				downuncs.append(bkghistdown.GetBinContent(bkgbin)-bkghist.GetBinContent(bkgbin))

		
				qcduperruncorr.SetBinContent(bkgbin,abs(upuncs[-1])*abs(upuncs[-1]))
				qcddownerruncorr.SetBinContent(bkgbin,abs(downuncs[-1])*abs(downuncs[-1]))

				for unc in tthistuncs:
					#print unc,"ttint",tthistuncs[unc][0].Integral(),tthistuncs[unc][1].Integral()
					upuncs.append(tthistuncs[unc][1].GetBinContent(bkgbin)-tthist.GetBinContent(bkgbin))
					downuncs.append(tthistuncs[unc][0].GetBinContent(bkgbin)-tthist.GetBinContent(bkgbin))
				for ttnorm in ttnorms:
					upuncs.append(ttnorm[1]*tthist.GetBinContent(bkgbin)*(1.0/ttnorm[2]))
					downuncs.append(-1.0*ttnorm[0]*tthist.GetBinContent(bkgbin)*(1.0/ttnorm[2]))
				upuncs.append(tthist.GetBinError(bkgbin))
				downuncs.append(-1.0*tthist.GetBinError(bkgbin))
				#print "upuncs",upuncs
				#print "downuncs",downuncs
				fullup=0.0
				fulldown=0.0
				#print "newbin",bkgbin
				for un in xrange(len(upuncs)):
					#print "diffs",upuncs[un],downuncs[un]
					modup=max(0.0,upuncs[un],downuncs[un])
					moddown=min(0.0,upuncs[un],downuncs[un])
					#print "up/down",modup,moddown	
					fullup+=modup*modup
					fulldown+=moddown*moddown
				totalHup.SetBinContent(bkgbin,totalH.GetBinContent(bkgbin)+sqrt(fullup)) 
				totalHdown.SetBinContent(bkgbin,totalH.GetBinContent(bkgbin)-sqrt(fulldown)) 
		
				totalHuperruncorr.SetBinContent(bkgbin,fullup)
				totalHdownerruncorr.SetBinContent(bkgbin,fulldown)
				
			totalHup.SetLineStyle(2)
			totalHdown.SetLineStyle(2)
			totalHup.SetFillColor(0)
			totalHdown.SetFillColor(0)

			totalHup.Draw("histsame")
			totalHdown.Draw("histsame")


			if "data" in sumhists[curname+"__"+vv[0]]:
				sumhists[curname+"__"+vv[0]]["data"].Add(datahist)
				#sumhists[curname+"__"+vv[0]]["bkgup"].Add(totalHup)
				#sumhists[curname+"__"+vv[0]]["bkgdown"].Add(totalHdown)
				sumhists[curname+"__"+vv[0]]["qcd"].Add(bkgqcd)
				sumhists[curname+"__"+vv[0]]["tt"].Add(tthist)
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
			leg.AddEntry( totalHup, '1#sigma background uncertainty', 'l')
			if wjetscorr!="None":
				leg.AddEntry( bkgwj, 'W+jets->QQ fraction', 'F')				
			for sigh in sighs:
					#print sigh
				leg.AddEntry(sighs[sigh],"Signal")

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
			elif var=="msoftdrop":
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
				st1.SetMinimum(0.1)
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
	output = ROOT.TFile("limitsetting/theta/"+prestr+"_ForLimits__"+options.era+".root","recreate")
	output.cd()
	nparts=10
	Bparr = []
	Tparr = []
	#for ll in limithistos:
	#	print ll
	for histon in limithistos:
		histo=limithistos[histon]

		if (options.anatype=="tHb" or options.anatype=="tZb"):
			 
			if histon.find("WpToBpT")!=-1:
				histonTp=histon.replace("BpT","TpB").replace("Bp","Tp")
				#print histonTp,histon
				try :
					histoTp=limithistos[histonTp]
				except:
					print "histo not found",histonTp
					continue
				histosum = copy.deepcopy(histo)
				histosum.Add(histoTp)
				#histosum.SetName(histon.replace("WpToBpT","WptoqVLQ").replace("Bp","VLQ"))
				#print "histon",histon
				charinid=histon.find("WpToBpT")
				newsetname=histon.split("__")[1].replace("WpToBpT","WptoqVLQ").replace("Bp","VLQ")[:14]
				histosum.SetName(histosum.GetName().replace(histon.split("__")[1],newsetname))
				histosum.SetTitle(histosum.GetName())
				histosum.Write()
			elif histon.find("WpToTpB")!=-1:	
				pass
			else:
				histo.SetTitle(histo.GetName())
				histo.Write()
		else:
			histo.SetTitle(histo.GetName())
			histo.Write()

	#print Tparr
	#print Bparr

	print "ttttvals",ttvals
	print "ttnormsimple",tttnormsimple,errsimple
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
if len(eras)==1:
	sys.exit()
c3 = TCanvas('c3', '', 700, 600)



for sumhist in sumhists:
	print
	curhset = sumhists[sumhist]

	

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

	var = sumhist.split("__")[0]
	crange=None
	obj = sumhist.split("__")[1]
	reg  = sumhist.split("__")[2]
	if var=="mass":
			if len(obj)==3:
				crange=[900.0,7000.0]
			if len(obj)==2:
				crange=[900.0,7000.0]
	elif var=="pt":
			if obj=="B":
				crange=[200.0,2500.0]
			else:
				crange=[450.0,2500.0]
	elif var=="eta":
			crange=[-2.4,2.4]
	elif var=="msoftdrop":
			crange=[120.0,300.0]
			
	if var=="msoftdrop":
		st1.Add(curhset["qcd"])
		st1.Add(curhset["tt"])
	else:
		st1.Add(curhset["tt"])
		st1.Add(curhset["qcd"])
	print "reg",reg,"obj",obj,"var",var


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
	bkgup.Draw("samehist")
	bkgdown.Draw("samehist")
	leg = TLegend(0.55, 0.5, 0.84, 0.84)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	if setstring!="QCD":
		leg.AddEntry( curhset["data"], 'Data', 'P')
		leg.AddEntry( curhset["qcd"], 'Data driven QCD', 'F')
		leg.AddEntry( curhset["tt"], 't#bar{t} Monte Carlo', 'F')
		leg.AddEntry( bkgup, '1#sigma background uncertainty', 'l')


		print curhset
		for ch in curhset:
			if ch.find("WpTo")!=-1:
				if setstring!="QCD":
					curhset[ch].Draw("samehist")
					leg.AddEntry( curhset[ch], 'Signal', 'l')

	else:
		leg.AddEntry( curhset["data"], 'QCD MC selection', 'P')
		leg.AddEntry( qcdl, 'QCD background estimate', 'l')
		leg.AddEntry( bkgup, '1#sigma background uncertainty', 'l')

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
	elif var=="msoftdrop":
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
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__'+setstring+extex+sumera+'.root', 'root')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__'+setstring+extex+sumera+'.pdf', 'pdf')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__'+setstring+extex+sumera+'.png', 'png')
		


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
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__semilog__'+setstring+extex+sumera+'.root', 'root')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__semilog__'+setstring+extex+sumera+'.pdf', 'pdf')
		c3.Print('plots/'+options.anatype+'__'+reg+'__'+var+'__'+obj+'__semilog__'+setstring+extex+sumera+'.png', 'png')


print "Completed..."																										

