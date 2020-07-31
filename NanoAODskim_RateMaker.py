from optparse import OptionParser
import subprocess,os,sys

import NanoAODskim_Functions	
from NanoAODskim_Functions import *

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'QCD',
                  dest		=	'set',
                  help		=	'data or ttbar')
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')
parser.add_option('--normcorr', metavar='F', action='store_true',
                  default=False,
                  dest='normcorr',
                  help='normcorr')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')
(options, args) = parser.parse_args()
ROOT.gROOT.LoadMacro("insertlogo.C+")
setname = options.set
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True
NanoF = NanoAODskim_Functions(options.anatype,options.era)
candl = NanoF.candl
probl = NanoF.probl

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True
settofind=options.set
if settofind=="JetHT":
	settofind="JetHT__Run"+options.era
output = ROOT.TFile("NanoAODskim_RateMaker__"+options.anatype+options.era+"__"+options.set+".root","recreate")
numregions = ["B","E","J","ZB"]
if (options.anatype=="tHb" or options.anatype=="tZb"):
	numregions.append("M")
constdict = NanoF.LoadConstants
ttbarnormcorr=constdict['ttrenorm']
ttscales=[["",1.0]]
if isdata:
	ttscales=[["down",1.0-ttbarnormcorr[1]/ttbarnormcorr[0]],["",1.0],["up",1.0+ttbarnormcorr[1]/ttbarnormcorr[0]]]
isc=0

for num in numregions:
	for tts in ttscales:
		Denregion ="A"
		if num=="M":
			Denregion ="Z"
		exstr = num
		if num=="B":
			exstr = ""
		inputfile = TFile('rootfiles/NanoAODskim_'+options.anatype+'Bkg'+options.era+'__'+settofind+'.root','open')
		Numrstr = 'pt__'+candl+'__aeta__'+candl+'__'+num
		Denrstr = 'pt__'+candl+'__aeta__'+candl+'__'+Denregion

		indexrat = inputfile.Get('index__'+candl+'__'+num)

		masshist = inputfile.Get('mass__'+candl+'__'+num)
		indexD = inputfile.Get('index__'+candl+'__'+Denregion)

		indexrat.Divide(indexD)
		print num,'index__'+candl+'__'+Denregion,indexrat.Integral()


		if options.anatype=="Pho":
			rebinval = 8
			if isdata:
				threshvals = [0.00001,0.25,0.25,0.5]#,0.45,0.45,0.6]
				biasval=60000.0
			else:
				threshvals = [0.00001,0.25,0.25,0.5]#,0.45,0.45,0.6]
				biasval=60000.0
		if options.anatype=="WW":
			rebinval = 4
			if isdata:
				threshvals = [0.00001,0.07,0.07,0.1,0.1,0.15,0.3]
				biasval=60000.0
			else:
				threshvals = [0.00001,0.07,0.07,0.1,0.1,0.15,0.3]
				biasval=60000.0

		if options.anatype=="Bstar":
			rebinval = 4
			if isdata:
				threshvals = [0.00001,0.07,0.07,0.1,0.1,0.15,0.3]
				biasval=60000.0
			else:
				threshvals = [0.00001,0.07,0.07,0.1,0.1,0.15,0.3]
				biasval=60000.0

		if options.anatype=="Zprime":
			rebinval = 4
			threshvals = [0.00001,0.04,0.04,0.04,0.05,0.08,0.1]
			biasval=60000.0
		if options.anatype=="tHb":
			rebinval = 12
			if isdata:
				threshvals = [0.00001,0.10,0.2,0.3]
				biasval=50000.0
			else:
				threshvals = [0.00001,0.10,0.2,0.3]
				biasval=50000.0

		if options.anatype=="tZb":
			rebinval = 12
			#higher, more bins
			if isdata:
				threshvals = [0.00001,0.07,0.12,0.2]
				#lower, more bins
				biasval=12000.0
			else:
				threshvals = [0.00001,0.07,0.12,0.2]
				biasval=12000.0
		if indexrat.Integral()>0.0:
			indexrat.Scale(2.0/indexrat.Integral())
		else:
			print "Empty region",'index__'+candl+'__'+num
			continue
		binh = []
		binhweighted = []


		histosnum = {}
		histosnum["0"]=inputfile.Get(Numrstr+"_0")
		histosnum["1"]=inputfile.Get(Numrstr+"_1")
		histosnum["sum"]=inputfile.Get(Numrstr)
		histosnum["0"].RebinY(rebinval)
		histosnum["1"].RebinY(rebinval)
		histosnum["sum"].RebinY(rebinval)
		print "Netabins",histosnum["sum"].GetNbinsY()


		histosden = {}
		histosden["0"]=inputfile.Get(Denrstr+"_0")
		histosden["1"]=inputfile.Get(Denrstr+"_1")
		histosden["sum"]=inputfile.Get(Denrstr)
		histosden["0"].RebinY(rebinval)
		histosden["1"].RebinY(rebinval)
		histosden["sum"].RebinY(rebinval)


		if isdata:
			
			bkgtosubtract = ["TT","ST"]
			if options.anatype=="Pho":
				bkgtosubtract.append("GJets")
			if options.anatype=="WW":
				bkgtosubtract.append("WJets")

			for bkgs in bkgtosubtract:
				#print 'rootfiles/NanoAODskim_'+options.anatype+'Bkg'+options.era+'__'+bkgs+'.root'
				curfile = TFile('rootfiles/NanoAODskim_'+options.anatype+'Bkg'+options.era+'__'+bkgs+'.root','open')

				histosnumbkg = {}
				histosnumbkg["0"] = curfile.Get(Numrstr+"_0")
				histosnumbkg["1"] = curfile.Get(Numrstr+"_1")
				histosnumbkg["sum"] = curfile.Get(Numrstr)
				histosnumbkg["0"].RebinY(rebinval)
				histosnumbkg["1"].RebinY(rebinval)
				histosnumbkg["sum"].RebinY(rebinval)

				histosdenbkg = {}
				histosdenbkg["0"] = curfile.Get(Denrstr+"_0")
				histosdenbkg["1"] = curfile.Get(Denrstr+"_1")
				histosdenbkg["sum"] = curfile.Get(Denrstr)
				histosdenbkg["0"].RebinY(rebinval)
				histosdenbkg["1"].RebinY(rebinval)
				histosdenbkg["sum"].RebinY(rebinval)

				print bkgs
				if options.normcorr and bkgs=="TT":
					print "normcorr",ttbarnormcorr
					histosnumbkg["0"].Scale(ttbarnormcorr[0])
					histosnumbkg["1"].Scale(ttbarnormcorr[0])
					histosnumbkg["sum"].Scale(ttbarnormcorr[0])

					histosdenbkg["0"].Scale(ttbarnormcorr[0])
					histosdenbkg["1"].Scale(ttbarnormcorr[0])
					histosdenbkg["sum"].Scale(ttbarnormcorr[0])

					histosnumbkg["0"].Scale(tts[1])
					histosnumbkg["1"].Scale(tts[1])
					histosnumbkg["sum"].Scale(tts[1])

					histosdenbkg["0"].Scale(tts[1])
					histosdenbkg["1"].Scale(tts[1])
					histosdenbkg["sum"].Scale(tts[1])


					print "subfrac",num,tts
					print bkgs,"-- Num:",histosnumbkg["sum"].Integral(),histosnum["sum"].Integral(),",","Den:",histosdenbkg["sum"].Integral(),histosden["sum"].Integral()
					print bkgs,"-- Num:",histosnumbkg["sum"].Integral()/histosnum["sum"].Integral(),",","Den:",histosdenbkg["sum"].Integral()/histosden["sum"].Integral()



				histosnum["0"].Add(histosnumbkg["0"],-1)
				histosnum["1"].Add(histosnumbkg["1"],-1)
				histosnum["sum"].Add(histosnumbkg["sum"],-1)



				histosden["0"].Add(histosdenbkg["0"],-1)
				histosden["1"].Add(histosdenbkg["1"],-1)
				histosden["sum"].Add(histosdenbkg["sum"],-1)


		for ybin in xrange(histosnum["0"].GetNbinsY()+1):
			hemarr = []
			for hemis in ["0","1","sum"]:
				Numr = histosnum[hemis]
				Denr = histosden[hemis]


				curn = Numr.ProjectionX("curn",ybin,ybin,"e")
				curd = Denr.ProjectionX("curd",ybin,ybin,"e")
				#print ybin,"curn",curn.Integral()
				#print ybin,"curd",curd.Integral()
				bins = array('d',[400.])
				curn.Integral()
				lastval = 0
				for xbin in range(1,curn.GetNbinsX()+1):
					err = array('d',[0.])
					errd = array('d',[0.])
					startbin=curn.FindBin(bins[-1])
					curint = curn.IntegralAndError(startbin,xbin,err)
					curintd = curd.IntegralAndError(startbin,xbin,errd)

					if curint>0 and curintd>0:
						#print err[0]/curint
						dxbias=(curn.GetBinLowEdge(xbin) + curn.GetBinWidth(xbin)-startbin)
						if (err[0]/curint<(threshvals[ybin]+float(dxbias)/biasval)):


							if curn.Integral(xbin+1,curn.GetNbinsX()+1)<=0:
								binval=3900.
								bins.append(3900.)
								break
							bins.append(curn.GetBinLowEdge(xbin) + curn.GetBinWidth(xbin))
							lastval=(curint/curintd)
							binval = min(3900.,curn.GetBinLowEdge(xbin) + curn.GetBinWidth(xbin))
					#if curint>0 and curintd>0: 
					#	if abs((curint/curintd)-lastval)>0:
					#		comberr = (curint/curintd)*sqrt((err[0]/curint)*(err[0]/curint) + (errd[0]/curintd)*(errd[0]/curintd))
							#print comberr,abs((curint/curintd)-lastval)
					#		if len(bins)>1 and comberr/abs((curint/curintd)-lastval)<0.2:
					#			bins.append(curn.GetBinLowEdge(xbin) + curn.GetBinWidth(xbin))
					#			lastval=(curint/curintd)
					#			binval = min(3900.,curn.GetBinLowEdge(xbin) + curn.GetBinWidth(xbin))
				if bins[-1]!=3900.:
					bins.append(3900.)
				#print "h",hemis,"ybin",ybin,bins	
				#print "h",hemis,"ybin",ybin,"nbins",len(bins)-1
				if (options.anatype=="tHb" or options.anatype=="tZb") and num in ["B","E","ZB"]:
					print "REBIN",options.anatype	
					if num=="B":
						bins = array('d',[400.0,500.0,600.0,700.0,3900.])
					else:
						bins = array('d',[400.0,500.0,600.0,700.0,800.0,1000.0,3900.])
				curnr= curn.Rebin(len(bins)-1,"curnr",bins)
				curdr= curd.Rebin(len(bins)-1,"curdr",bins)
				hemarr.append([copy.deepcopy(curnr),copy.deepcopy(curdr)])
			#print
			sumnum = copy.deepcopy(hemarr[2][0])
			sumden = copy.deepcopy(hemarr[2][1])
			currate = copy.deepcopy(sumnum)
			currate.Divide(sumden)

			sumnum1 = copy.deepcopy(hemarr[0][0])
			sumden1 = copy.deepcopy(hemarr[0][1])
			currate1 = copy.deepcopy(sumnum1)
			currate1.Divide(sumden1)

			sumnum2 = copy.deepcopy(hemarr[1][0])
			sumden2 = copy.deepcopy(hemarr[1][1])
			currate2 = copy.deepcopy(sumnum2)
			currate2.Divide(sumden2)



			binhweighted.append([currate1,currate2])
			binh.append(currate)
		rate = copy.deepcopy(Numr)
		rate.Divide(Denr)

		output.cd()
		ibbb=0
		canv = TCanvas(exstr+"rateh",exstr+"rateh",800,1000)
		canv.Divide(2,3)
		if options.set=="JetHT":
			if options.era=="2016":
				per=1
			if options.era=="2017":
				per=2
			if options.era=="2018":
				per=3

				

		maxes= []
		for bbb in binh:
			maxes.append(bbb.GetMaximum())
		maxmaxes = max(maxes)
		ttstr=""
		if tts[0]!="":
			ttstr="__"+tts[0]
		for bbb in binh:
			bbb.Write(exstr+"ratebin__"+str(ibbb)+ttstr)
			if ibbb>0:

				canv.cd(ibbb)
				bbb.SetStats(0)

				bbb.GetYaxis().SetRangeUser(0.0,max(maxes)*1.5)
				bbb.SetTitle(";p_{T} (GeV);TF(p_{T},#eta)")

				bbb.Draw()
				canvcur = TCanvas(exstr+"rateh_ebin"+str(ibbb),exstr+"rateh_ebin"+str(ibbb),700,600)
				canvcur.cd()
				canvcur.SetLeftMargin(0.16)
				canvcur.SetRightMargin(0.05)
				canvcur.SetTopMargin(0.11)
				bbb.SetMaximum(bbb.GetMaximum()*1.4)
				bbb.SetMinimum(0.0)
				bbb.Draw()
				if options.set=="JetHT":
					ROOT.insertlogo( canvcur, per, 11 )

				canvcur.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin'+ttstr+'_ebin'+str(ibbb)+'.root', 'root')
				canvcur.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin'+ttstr+'_ebin'+str(ibbb)+'.pdf', 'pdf')
				canvcur.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin'+ttstr+'_ebin'+str(ibbb)+'.png', 'png')


			ibbb+=1


		canv.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin'+ttstr+'.root', 'root')
		canv.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin'+ttstr+'.pdf', 'pdf')
		canv.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin'+ttstr+'.png', 'png')


		canvw1 = TCanvas(exstr+"ratew1",exstr+"ratew1",800,1000)
		canvw1.Divide(2,3)
		canvw2 = TCanvas(exstr+"ratew2",exstr+"ratew2",800,1000)
		canvw2.Divide(2,3)
		ibbb=0
		for bbb in binhweighted:
			
			bbb[0].Write(exstr+"ratebin__"+str(ibbb)+"__0"+ttstr)
			bbb[1].Write(exstr+"ratebin__"+str(ibbb)+"__1"+ttstr)
			#print bbb
			if ibbb>0:
				canvw1.cd(ibbb)
				#print "T0"
				bbb[0].SetStats(0)
				bbb[0].GetYaxis().SetRangeUser(0.0,max(maxes)*1.5)
				bbb[0].SetTitle(";p_{T};")
				bbb[0].Draw()
				#print bbb[0].GetMean()
				canvw2.cd(ibbb)
				#print "T1"
				bbb[1].SetStats(0)
				bbb[1].GetYaxis().SetRangeUser(0.0,max(maxes)*1.5)
				bbb[1].SetTitle(";p_{T};")
				bbb[1].Draw()
				#print bbb[1].GetMean()
			ibbb+=1

		canvw1.Update()
		canvw2.Update()

		canvw1.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin__0'+ttstr+'.root', 'root')
		canvw1.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin__0'+ttstr+'.pdf', 'pdf')
		canvw1.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin__0'+ttstr+'.png', 'png')
		canvw2.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin__1'+ttstr+'.root', 'root')
		canvw2.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin__1'+ttstr+'.pdf', 'pdf')
		canvw2.Print('plots/'+exstr+options.anatype+options.era+'__'+options.set+'ratebin__1'+ttstr+'.png', 'png')
		rate.Write(exstr+"rate"+ttstr)

	masshist.Write(exstr+"masshist")
	indexrat.Write(exstr+"indexrat")
output.Write()
output.Close()
print "Completed..."


