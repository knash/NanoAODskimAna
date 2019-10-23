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
parser.add_option('--normcorr', metavar='F', action='store_true',
                  default=False,
                  dest='normcorr',
                  help='normcorr')
parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()

regiontoname=	{
		"C":"Signal",
		"K":"Loose t",
		"H":"Loose H",
		"F":"Validation",
		"FT":"ttbar measurement",
		}


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


eras=(options.era).split(",")

for era in eras:
	setname =options.set
	NanoF = NanoAODskim_Functions(options.anatype,era)
	labels = NanoF.labels 
	candl = NanoF.candl
	probl = NanoF.probl
	wjetscorr=options.wjets

	uncs=["pu","trig","q2","btag","jes","jer"]
	if "H" in labels:
		uncs.append("htag")
	#if "Z" in labels:
	#	uncs.append("wtag")
	uncnames=["mass","pt","eta"]

	if options.wjets!="None":
		extex+="__WJ"+wjetscorr
	if isdata:
		datafile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__JetHT.root","open")
	else:
		datafile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__QCD.root","open")
	QCDfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__QCD.root","open")
	ttfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__TT.root","open")

	if options.anatype=="Pho":
		gjetsfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__GJets.root","open")
	if wjetscorr!="None":
		wjetsfile=TFile("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__WJets.root","open")
	sigfiles=[]
	sigyearforplotting="2017"
	if era=="2016": 
		sigyearforplotting="2016"
	if options.anatype=="Pho":
		sigfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__WkkToRWToTri_*.root")
	if options.anatype=="WW":
		sigfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+era+"__WkkToWRadionToWWW_M*.root")
	if options.anatype=="tZb":
		sigfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+sigyearforplotting+"__WpToBpT_Wp3000Nar_Bp2000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")
		sigfiles+=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+sigyearforplotting+"__WpToTpB_Wp3000Nar_Tp2000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8.root")

	if options.anatype=="tHb":
		sigfiles=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+sigyearforplotting+"__WpToBpT_Wp3000Nar_Bp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")
		sigfiles+=glob.glob("rootfiles/NanoAODskim_"+options.anatype+"Ana"+sigyearforplotting+"__WpToTpB_Wp3000Nar_Tp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8.root")



	sigfs = {}

	nbins=6
	rebininv=10
	rebinob=5
	rebinsd=5
	if options.anatype=="tHb" or options.anatype=="tZb" or options.anatype=="Pho" :
		nbins=2
		rebininv=25
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
	print ttbarnormcorr
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
	limithistos = []

	ROOT.gROOT.LoadMacro("insertlogo.C+")
	blindington = False
	if options.set=="JetHT":
		blindington = True
	vers = [["C","D"],["F","G"],["K","L"],["H","I"]]
	#if options.anatype=="tHb" or options.anatype=="tZb":
		#vers.append(["N","O"])
	if options.anatype=="tHb":
		vers.append(["FT","FTR"])
	tttnormsimple=None
	errsimple=None

	ttvals=None

	for vv in vers:
		for ihn in xrange(len(histonames)):
			curname = histonames[ihn]
			sighs = {}

			datahist = datafile.Get(curname+"__"+vv[0])
			print datafile
			print curname+"__"+vv[0]
			datahist.Rebin(rebins[ihn])
			#print datafile,curname+"__"+vv[1]+"_0"
			bkghist = datafile.Get(curname+"__"+vv[1]+"_0")
			bkghist.Add(datafile.Get(curname+"__"+vv[1]+"_1"))

			if isdata:

				bkgtosubtract = [ttfile]
				if options.anatype=="Pho":
					bkgtosubtract.append(gjetsfile)
				if wjetscorr=="MC" and wjetscorr!="None":
					bkgtosubtract.append(wjetsfile)
				for bkgs in bkgtosubtract:
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
			print  var,uncnames
			if var in uncnames:
				for unc in uncs:
					print unc,curname+"__"+vv[0]+"__"+unc+"__down",curname+"__"+vv[0]+"__"+unc+"__up"
					tthistuncs[unc]=[ttfile.Get(curname+"__"+vv[0]+"__"+unc+"__down"),ttfile.Get(curname+"__"+vv[0]+"__"+unc+"__up")]
					tthistuncs[unc][0].Rebin(rebins[ihn])
					tthistuncs[unc][1].Rebin(rebins[ihn])

			if options.anatype=="Pho":
				gjetshist = gjetsfile.Get(curname+"__"+vv[0])

			for sigf in sigfiles:
				print sigf
				sindex = sigf.split("__")[1].replace(".root","")
				sighs[sindex]=sigfs[sigf.split("__")[1].replace(".root","")].Get(curname+"__"+vv[0])


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
				#sighs[sigh].Scale(0.64)
				sighs[sigh].Rebin(rebins[ihn])
				if options.anatype=="tHb" or options.anatype=="tZb":
					print "RESCALE ALL SIG BY",rescale
					print sighs[sigh].Integral()			
					sighs[sigh].Scale(rescale)
					print sighs[sigh].Integral()	
			#print "4"

			bbinhistsup = []
			errhist = copy.deepcopy(bkghist)
			errhistcorr = copy.deepcopy(bkghist)
			conthist = copy.deepcopy(bkghist)


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






			if curname in invmnames and vv[0]=="C":
				nobject = datahist.GetName().split("__")[0]+"_"+datahist.GetName().split("__")[1]
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
				limithistos.append(tthist)
				if options.anatype=="Pho":
					limithistos.append(gjetshist)
				#limithistos.append(wjetshist)
				limithistos.append(bkghist)
				limithistos.append(bkghistup)
				limithistos.append(bkghistdown)
				for sigh in sighs:
						#print sigh
						if options.anatype=="Pho":
							if sigh == "WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2":
								sighs[sigh].SetName(nobject+"__M3000")
								sighs[sigh].SetTitle(sighs[sigh].GetName())
								limithistos.append(sighs[sigh])
						if options.anatype=="WW":
							#print sigh
							#print sigh.split("-")
							#print (sigh.split("-")[0]).split("_")
							curhname = (sigh.split("-")[0]).split("_")[1]
							sighs[sigh].SetName(nobject+"__"+curhname)
							limithistos.append(sighs[sigh])
						if options.anatype=="tHb" or options.anatype=="tZb":
							#print "sigh",sigh
							curhname = sigh.split("_")[0]+sigh.split("_")[1]+sigh.split("_")[2]
							sighs[sigh].SetName(nobject+"__"+curhname)
							limithistos.append(sighs[sigh])


			c1 = TCanvas('c1', '', 700, 600)
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

			datahist.SetMarkerStyle(21)	
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
			leg1.AddEntry( datahist, 'Data', 'P')
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

			setstring=options.set
			if setstring=="QCD":
				c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__'+setstring+era+'.root', 'root')
				c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__'+setstring+era+'.pdf', 'pdf')
				c1.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__bkgonly__'+setstring+era+'.png', 'png')
			bkghist.SetMinimum(0.01)
			main.SetLogy()
			bkghist.SetMaximum(bkghist.GetMaximum()*100)			
			main.RedrawAxis()
			c1.Update()
			if setstring=="QCD":
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
				print"CORRECTING QCD",bkghist.Integral()
				bkghist.Scale(wjcorr)
				print"CORRECTING QCD",bkghist.Integral()
				bkghistup.Scale(wjcorr)
				bkghistdown.Scale(wjcorr)
			c2 = TCanvas('c2', '', 700, 600)
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
					crange=[1000.0,7000.0]
				if len(obj)==2:
					crange=[1000.0,7000.0]
			elif var=="pt":
				if obj=="B":
					crange=[200.0,2500.0]
				else:
					crange=[450.0,2500.0]
			elif var=="eta":
				crange=[-2.4,2.4]
			elif var=="msoftdrop":
				crange=[100.0,280.0]
			if crange!=None:
				st1.GetXaxis().SetRangeUser(crange[0],crange[1])
			

			if not isdata:
				if options.anatype=="Pho":
					datahist.Add(gjetshist)
				datahist.Add(tthist)
				if wjetscorr!="None":
					datahist.Add(wjetshist)
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
				print "VERY BASIC ERRORS","dat",sigdat,"tt",relerrden*tthist.Integral(),"bkg",bkgqcd.Integral()

				tttnormsimple=(datahist.Integral()-bkgqcd.Integral())/tthist.Integral()
				errsimple=tttnormsimple*sqrt(relerrnum*relerrnum+relerrden*relerrden)

				print "tot",errsimple

			sigcolors = [1,2,3,4,5,6,7,8,9,10]
			isig=0
			if options.anatype=="tHb" or options.anatype=="tZb":
					#print "Summing Sigs"
					nsigs = 0
					if options.anatype=="tHb" or options.anatype=="tZb":

						for sigh in sighs:
							print "Adding ",sigh,sighs[sigh].Integral()
							replnameBp = sigh.replace("BpT","TpB").replace("Bp","Tp")
							replnameTp = sigh.replace("TpB","BpT").replace("Tp","Bp")
							#print "comp ",replnameBp,replnameTp,sigh,sigh==replnameBp,sigh==replnameTp
							if replnameBp==sigh:
								summedsig = copy.deepcopy(sighs[sigh])
								print "pradd",summedsig.Integral()
								summedsig.Add(sighs[replnameTp])
								print "postadd",summedsig.Integral()
								summedsig.SetLineColor(sigcolors[isig+2])
								summedsig.Draw("samehist")
				
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
			totalHup = copy.deepcopy(totalH)
			totalHdown = copy.deepcopy(totalH)
			for bkgbin in xrange(totalHup.GetNbinsX()+1):
				upuncs = []
				downuncs = []

				upuncs.append(bkghistup.GetBinContent(bkgbin)-bkghist.GetBinContent(bkgbin))
				downuncs.append(bkghistdown.GetBinContent(bkgbin)-bkghist.GetBinContent(bkgbin))
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

			totalHup.SetLineStyle(2)
			totalHdown.SetLineStyle(2)
			totalHup.SetFillColor(0)
			totalHdown.SetFillColor(0)

			totalHup.Draw("histsame")
			totalHdown.Draw("histsame")
			leg = TLegend(0.60, 0.55, 0.84, 0.84)
			leg.SetFillColor(0)
			leg.SetBorderSize(0)
			leg.AddEntry( datahist, 'Data', 'P')
			leg.AddEntry( bkgqcd, 'Data driven QCD', 'F')
			leg.AddEntry( tthist, 't#bar{t} Monte Carlo', 'F')
			if wjetscorr!="None":
				leg.AddEntry( bkgwj, 'W+jets->QQ fraction', 'F')

			leg.Draw()
			prelim = TLatex()
			prelim.SetNDC()
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
				xaxist = obj+" candidate softdrop mass [GeV]"
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


			if setstring=="JetHT":
				c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__'+setstring+extex+era+'.root', 'root')
				c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__'+setstring+extex+era+'.pdf', 'pdf')
				c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__'+setstring+extex+era+'.png', 'png')
			st1.SetMinimum(0.1)
			st1.SetMaximum(max(st1.GetMaximum(),datahist.GetMaximum())*30)	
			main.SetLogy()
			main.RedrawAxis()
			c2.Update()
			if setstring=="JetHT":
				c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__semilog__'+setstring+extex+era+'.root', 'root')
				c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__semilog__'+setstring+extex+era+'.pdf', 'pdf')
				c2.Print('plots/'+options.anatype+'__'+vv[0]+'__'+curname+'__semilog__'+setstring+extex+era+'.png', 'png')

	print "Writing limit histos"
	output = ROOT.TFile("limitsetting/theta/NanoAODskim_ForLimits__"+options.anatype+".root","recreate")
	output.cd()
	nparts=10
	Bparr = []
	Tparr = []
	for histo in limithistos:
		histo.SetTitle(histo.GetName())
		if (options.anatype=="tHb" or options.anatype=="tZb"):
			 


			#print histo.GetName()
			if histo.GetName().find("WpToBpT")!=-1:
				
				for ii in range(0,nparts+1):
					scalefacBp = float(ii)/(float(nparts)/2.0)
					Bparr.append(copy.deepcopy(histo))
					Bparr[-1].Scale(scalefacBp)
			elif histo.GetName().find("WpToTpB")!=-1:	
				
				for ii in range(0,nparts+1):
					scalefacTp = float(ii)/(float(nparts)/2.0)
					Tparr.append(copy.deepcopy(histo))
					Tparr[-1].Scale(scalefacTp)
			else:
				histo.Write()
		else:
			histo.Write()
		print histo.GetName(),histo.GetTitle()
	#print Tparr
	#print Bparr

	print "ttttvals",ttvals
	print "ttnormsimple",tttnormsimple,errsimple

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

print "Completed..."																										

