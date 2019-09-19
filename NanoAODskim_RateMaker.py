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
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')
(options, args) = parser.parse_args()

setname = options.set
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True

NanoF = NanoAODskim_Functions(options.anatype)
candl = NanoF.candl
probl = NanoF.probl

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True

output = ROOT.TFile("NanoAODskim_RateMaker__"+options.anatype+options.era+"__"+options.set+".root","recreate")
numregions = ["B","E","J"]
if (options.anatype=="tHb" or options.anatype=="tZb"):
	numregions.append("M")
for num in numregions:
	Denregion ="A"
	if num=="M":
		Denregion ="Z"
	exstr = num
	if num=="B":
		exstr = ""
	inputfile = TFile('rootfiles/NanoAODskim_'+options.anatype+'Bkg'+options.era+'__'+options.set+'.root','open')
	Numrstr = 'pt__'+candl+'__aeta__'+candl+'__'+num
	Denrstr = 'pt__'+candl+'__aeta__'+candl+'__'+Denregion
	indexrat = inputfile.Get('index__'+candl+'__'+num)
	masshist = inputfile.Get('mass__'+candl+'__'+num)
	indexD = inputfile.Get('index__'+candl+'__'+Denregion)
	indexrat.Divide(indexD)



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
		threshvals = [0.00001,0.04,0.04,0.04,0.05,0.08,0.1]
		biasval=60000.0
	if options.anatype=="Zprime":
		rebinval = 4
		threshvals = [0.00001,0.04,0.04,0.04,0.05,0.08,0.1]
		biasval=60000.0
	if options.anatype=="tHb":
		rebinval = 8
		if isdata:
			threshvals = [0.00001,0.1,0.2,0.3]
			biasval=70000.0
		else:
			threshvals = [0.00001,0.1,0.2,0.3]
			biasval=70000.0
	if options.anatype=="tZb":
		rebinval = 8
		if isdata:
			threshvals = [0.00001,0.1,0.2,0.3]
			biasval=70000.0
		else:
			threshvals = [0.00001,0.1,0.2,0.3]
			biasval=70000.0
	indexrat.Scale(2.0/indexrat.Integral())
	binh = []
	binhweighted = []


	histosnum = {}
	histosnum["0"]=inputfile.Get(Numrstr+"_0")
	histosnum["1"]=inputfile.Get(Numrstr+"_1")
	histosnum["sum"]=inputfile.Get(Numrstr)
	histosnum["0"].RebinY(rebinval)
	histosnum["1"].RebinY(rebinval)
	histosnum["sum"].RebinY(rebinval)


	histosden = {}
	histosden["0"]=inputfile.Get(Denrstr+"_0")
	histosden["1"]=inputfile.Get(Denrstr+"_1")
	histosden["sum"]=inputfile.Get(Denrstr)
	histosden["0"].RebinY(rebinval)
	histosden["1"].RebinY(rebinval)
	histosden["sum"].RebinY(rebinval)


	if isdata:
		
		bkgtosubtract = ["TT","WJets"]
		if options.anatype=="Pho":
			bkgtosubtract.append("GJets")
		for bkgs in bkgtosubtract:

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

			print "subfrac"
			print bkgs,histosnumbkg["sum"].Integral()/histosnum["sum"].Integral()
			print bkgs,histosdenbkg["sum"].Integral()/histosden["sum"].Integral()

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
			print ybin,"curn",curn.Integral()
			print ybin,"curd",curd.Integral()
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
					if err[0]/curint<(threshvals[ybin]+float(dxbias)/biasval):


						if curn.Integral(xbin,curn.GetNbinsX()+1)==0:
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
			print "h",hemis,"ybin",ybin,"nbins",len(bins)-1

			curnr= curn.Rebin(len(bins)-1,"curnr",bins)
			curdr= curd.Rebin(len(bins)-1,"curdr",bins)
			hemarr.append([copy.deepcopy(curnr),copy.deepcopy(curdr)])
		print
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
	maxes= []
	for bbb in binh:
		maxes.append(bbb.GetMaximum())
	maxmaxes = max(maxes)
	for bbb in binh:
		bbb.Write(exstr+"ratebin__"+str(ibbb))
		if ibbb>0:
			canv.cd(ibbb)
			bbb.SetStats(0)
			bbb.GetYaxis().SetRangeUser(0.0,max(maxes)*1.5)
			bbb.SetTitle(";p_{T};")
			bbb.Draw()

		ibbb+=1
	canvw1 = TCanvas(exstr+"ratew1",exstr+"ratew1",800,1000)
	canvw1.Divide(2,3)
	canvw2 = TCanvas(exstr+"ratew2",exstr+"ratew2",800,1000)
	canvw2.Divide(2,3)
	ibbb=0
	for bbb in binhweighted:
		
		bbb[0].Write(exstr+"ratebin__"+str(ibbb)+"__0")
		bbb[1].Write(exstr+"ratebin__"+str(ibbb)+"__1")
		print bbb
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
	rate.Write(exstr+"rate")
	masshist.Write(exstr+"masshist")

	indexrat.Write(exstr+"indexrat")
	#pbins = array('d',[400,420,440,460,480,500,520,540,560,580,620,660,700,740,780,820,900,1000,1100,1200,1300,1400,1500,1700,1900,2100,2400,2800,3300,3900])
	#Nump = inputfile.Get('p__P__B')
	#Denp = inputfile.Get('p__P__A')
	#Numpr= Nump.Rebin(len(pbins)-1,"Numpr",pbins)
	#Denpr= Denp.Rebin(len(pbins)-1,"Denpr",pbins)

	#ratep = copy.deepcopy(Numpr)
	#ratep.Divide(Denpr)
	#ratep.Write("ratep")
output.Write()
output.Close()
print "Completed..."


