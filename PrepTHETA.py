import os
import array
import glob
import math
import ROOT
import copy
import sys
#from ROOT import *
from array import *
from optparse import OptionParser
#For specific objects
import NanoAODskim_Functions
from NanoAODskim_Functions import *

def projectCNNfromTH3(hist3dFF,CNNsel=[0.0,0.9,1.0],ptsel=[400.,1400.],masselpass=[60.0,220.],masselfail=[0.0,220.]):
	hist3dpass=copy.deepcopy(hist3dFF)
	hist3dfail=copy.deepcopy(hist3dFF)

	CNNbinsfail = [hist3dFF.GetYaxis().FindBin(CNNsel[0]),hist3dFF.GetYaxis().FindBin(CNNsel[1])]
	CNNbinspass = [hist3dFF.GetYaxis().FindBin(CNNsel[1]),hist3dFF.GetYaxis().FindBin(CNNsel[2])]

	#print "FBcont",hist3dFF.GetYaxis().GetBinCenter(CNNbinsfail[0]),hist3dFF.GetYaxis().GetBinCenter(CNNbinsfail[1])
	#print "PBcont",hist3dFF.GetYaxis().GetBinCenter(CNNbinspass[0]),hist3dFF.GetYaxis().GetBinCenter(CNNbinspass[1])
	ptbins = [hist3dFF.GetZaxis().FindBin(ptsel[0]),hist3dFF.GetZaxis().FindBin(ptsel[1])]

	hist3dpass.GetXaxis().SetRangeUser(masselpass[0],masselpass[1])
	hist1dpass = hist3dpass.ProjectionX(hist3dpass.GetName()+"pass",CNNbinspass[0],CNNbinspass[1],ptbins[0],ptbins[1],"e")

	hist3dfail.GetXaxis().SetRangeUser(masselfail[0],masselfail[1])	
	hist1dfail = hist3dfail.ProjectionX(hist3dfail.GetName()+"fail",CNNbinsfail[0],CNNbinsfail[1],ptbins[0],ptbins[1],"e")

	return hist1dpass,hist1dfail



parser = OptionParser()
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
		  default	=	'Mu',
		  dest		=	'anatype',
		  help		=	'')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
		  default	=	'2017',
		  dest		=	'era',
		  help		=	'2016,2017, or 2018')

parser.add_option('-d', '--disc', metavar='F', type='string', action='store',
                  default	=	'0.9',
                  dest		=	'disc',
                  help		=	'')



parser.add_option('-p', '--pt', metavar='F', type='string', action='store',
                  default	=	'400to500',
                  dest		=	'pt',
                  help		=	'')

parser.add_option('--bsum', metavar='F', action='store_true',
		  default=False,
		  dest='bsum',
		  help='bsum')



parser.add_option('-f', '--sfval', metavar='F', type='string', action='store',
                  default	=	'1.0',
                  dest		=	'sfval',
                  help		=	'')


(options, args) = parser.parse_args()
NanoF = NanoAODskim_Functions(options.anatype,options.era)
print options.pt
ptbounds = (options.pt).split('to')
ptbounds = [float(ptbounds[0]),float(ptbounds[1])]
print ptbounds

discval = float(options.disc)

fsets = ["QCD","TT","WJetsToLNu"]
if options.anatype=="Mu":
	fsets.append("SingleMuon")
if options.anatype=="Ele":
	if options.era=="2018":
		fsets.append("EGamma")
	else:
		fsets.append("SingleElectron")
addstrsf=""
if options.sfval!="1.0":
	addstrsf+="_SF"+(options.sfval).replace(".","p")

addstrsf+="_Pt"+(options.pt)
addstrsf+="_CNN"+(options.disc).replace(".","p")
	
rebinval = 2
output = TFile("limitsetting/theta/ThetaFile_ttfit_"+options.anatype+options.era+addstrsf+".root","recreate")


CNNsel=[0.0,discval,1.0]
ptsel=[ptbounds[0],ptbounds[1]]
#etasel=[0.,2.4]
mrangefail = [10.,260.0]
mrangepass = [60.0,260.0]

#binsfail = [0.,5.,10.,15.,20.,25.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,160.,180.,200.,220.,240.,260.]
#binspass = [60.,70.,80.,90.,100.,110.,120.,140.,160.,180.,200.,220.]
#binspass=array('d',binspass)
#binsfail=array('d',binsfail)

Numfile = ROOT.TFile("rootfiles/NanoAODskim_semilep_"+options.anatype+"Ana"+options.era+"__"+fsets[-1]+".root")
Denfile = ROOT.TFile("rootfiles/NanoAODskim_semilep_"+options.anatype+"Ana"+options.era+"__"+fsets[1]+".root")

ratn=Numfile.Get("PV_npvs_pre")
ratd=Denfile.Get("PV_npvs_pre")

ratn.Scale(1.0/ratn.Integral())
ratd.Scale(1.0/ratd.Integral())

ratn.Divide(ratd)



outputp = TFile("PUF_"+options.anatype+options.era+".root","recreate")
ratn.Write("pvrat")
outputp.Write()
outputp.Close()
output.cd()
sfval = float(options.sfval)
for fset in fsets:   
    writeset = fset
    if fset in ["SingleMuon","SingleElectron","EGamma"]:
		writeset="DATA"

    uncsfortheta  = ['']
    if not writeset in ["DATA"]:
    	uncsfortheta.extend(['__jer__plus','__jer__minus','__jes__plus','__jes__minus','__btag__plus','__btag__minus'])
    if fset=="TT":
	uncsfortheta.extend(['__tptrw__plus','__tptrw__minus','__q2__plus','__q2__minus'])	
    for unc in uncsfortheta:




	uncstr=unc.replace("plus","up").replace("minus","down")
	unctowrite = unc

	curfile = ROOT.TFile("rootfiles/NanoAODskim_semilep_"+options.anatype+"Ana"+options.era+"__"+fset+".root")

	if fset=="TT":
		passfailhist3d = curfile.Get("msoftdropdef__T__iMDtop__T__pt__T__Cm4"+uncstr)
	else:
		passfailhist3d = curfile.Get("msoftdropdef__T__iMDtop__T__pt__T__C"+uncstr)
	passhisto,failhisto = projectCNNfromTH3(passfailhist3d,CNNsel,ptsel,mrangepass,mrangefail)


	failhisto.Rebin(rebinval)
	passhisto.Rebin(rebinval)

	
	#failhisto = failhisto.Rebin(len(binsfail)-1,"failhisto",binsfail)
	#passhisto = passhisto.Rebin(len(binspass)-1,"passhisto",binspass)

	if fset=="TT":

		passfailhist3d_sig = curfile.Get("msoftdropdef__T__iMDtop__T__pt__T__Cm1"+uncstr)
		passhisto_sig,failhisto_sig = projectCNNfromTH3(passfailhist3d_sig,CNNsel,ptsel,mrangepass,mrangefail)
		

		failhisto_sig.Rebin(rebinval)
		passhisto_sig.Rebin(rebinval)

		#passfac = sfval
		#failfac = (failhisto_sig.Integral()+passhisto_sig.Integral()-sfval*passhisto_sig.Integral())/failhisto_sig.Integral()
		#passhisto_sig.Scale(passfac)
		#failhisto_sig.Scale(failfac)



		#failhisto_sig = failhisto_sig.Rebin(len(binsfail)-1,"failhisto_sig",binsfail)
		#passhisto_sig = passhisto_sig.Rebin(len(binspass)-1,"passhisto_sig",binspass)


		passfailhist3d_semi = curfile.Get("msoftdropdef__T__iMDtop__T__pt__T__Cm3"+uncstr)
		passhisto_semi,failhisto_semi = projectCNNfromTH3(passfailhist3d_semi,CNNsel,ptsel,mrangepass,mrangefail)
		

		failhisto_semi.Rebin(rebinval)
		passhisto_semi.Rebin(rebinval)


		#failhisto_semi = failhisto_semi.Rebin(len(binsfail)-1,"failhisto_semi",binsfail)
		#passhisto_semi = passhisto_semi.Rebin(len(binspass)-1,"passhisto_semi",binspass)


		passfailhist3d_bmerge = curfile.Get("msoftdropdef__T__iMDtop__T__pt__T__Cm2"+uncstr)
		passhisto_bmerge,failhisto_bmerge = projectCNNfromTH3(passfailhist3d_bmerge,CNNsel,ptsel,mrangepass,mrangefail)
		
		failhisto_bmerge.Rebin(rebinval)
		passhisto_bmerge.Rebin(rebinval)

		#failhisto_bmerge = failhisto_bmerge.Rebin(len(binsfail)-1,"failhisto_bmerge",binsfail)
		#passhisto_bmerge = passhisto_bmerge.Rebin(len(binspass)-1,"passhisto_bmerge",binspass)


		output.cd()



		failhisto_bmerge.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge"+unctowrite)
		failhisto_bmerge.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge"+unctowrite)

	
		passhisto_bmerge.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge"+unctowrite)
		passhisto_bmerge.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge"+unctowrite)
		if not options.bsum:
			failhisto_bmerge.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge"+unctowrite)
			passhisto_bmerge.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge"+unctowrite)



		failhisto_sig.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig"+unctowrite)
		failhisto_sig.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig"+unctowrite)

	
		passhisto_sig.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig"+unctowrite)
		passhisto_sig.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig"+unctowrite)


		if options.bsum:
			failhisto_sig.Add(failhisto_bmerge)
			passhisto_sig.Add(passhisto_bmerge)


		print 
		print "SIG EFF"
		print uncstr,passhisto_sig.Integral(),failhisto_sig.Integral(),passhisto_sig.Integral()/(failhisto_sig.Integral()+passhisto_sig.Integral())
		print 

		failhisto_sig.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig"+unctowrite)
		passhisto_sig.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig"+unctowrite)


		if unctowrite=='':


			effscale = 0.15

			passhisto_sig_up = copy.copy(passhisto_sig)
			failhisto_sig_up = copy.copy(failhisto_sig)

			passhisto_sig_down = copy.copy(passhisto_sig)
			failhisto_sig_down = copy.copy(failhisto_sig)

			failhisto_sig_up.Scale(1.0-(effscale)*passhisto_sig.Integral()/(failhisto_sig.Integral()+passhisto_sig.Integral()))
			passhisto_sig_up.Scale(1.0+(effscale)*failhisto_sig.Integral()/(failhisto_sig.Integral()+passhisto_sig.Integral()))

			failhisto_sig_down.Scale(1.0-(-effscale)*passhisto_sig.Integral()/(failhisto_sig.Integral()+passhisto_sig.Integral()))
			passhisto_sig_down.Scale(1.0+(-effscale)*failhisto_sig.Integral()/(failhisto_sig.Integral()+passhisto_sig.Integral()))
			

			passhisto_bmerge_up = copy.copy(passhisto_bmerge)
			failhisto_bmerge_up = copy.copy(failhisto_bmerge)

			passhisto_bmerge_down = copy.copy(passhisto_bmerge)
			failhisto_bmerge_down = copy.copy(failhisto_bmerge)

			failhisto_bmerge_up.Scale(1.0-(effscale)*passhisto_bmerge.Integral()/(failhisto_bmerge.Integral()+passhisto_bmerge.Integral()))
			passhisto_bmerge_up.Scale(1.0+(effscale)*failhisto_bmerge.Integral()/(failhisto_bmerge.Integral()+passhisto_bmerge.Integral()))

			failhisto_bmerge_down.Scale(1.0-(-effscale)*passhisto_bmerge.Integral()/(failhisto_bmerge.Integral()+passhisto_bmerge.Integral()))
			passhisto_bmerge_down.Scale(1.0+(-effscale)*failhisto_bmerge.Integral()/(failhisto_bmerge.Integral()+passhisto_bmerge.Integral()))
			
			print "inttest",failhisto_bmerge_down.Integral() + passhisto_bmerge_down.Integral()
			print "inttest",failhisto_bmerge_up.Integral() + passhisto_bmerge_up.Integral()



			passhisto_bmerge_up.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__plus")
			passhisto_bmerge_up.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__plus")


			failhisto_bmerge_up.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__plus")
			failhisto_bmerge_up.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__plus")



			passhisto_bmerge_down.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__minus")
			passhisto_bmerge_down.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__minus")



			failhisto_bmerge_down.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__minus")
			failhisto_bmerge_down.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__minus")

			if not options.bsum:
				passhisto_bmerge_up.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__plus")
				failhisto_bmerge_up.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__plus")
				passhisto_bmerge_down.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__minus")
				failhisto_bmerge_down.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_bmerge__TT_bmerge_tag"+addstrsf+"__minus")

			passhisto_sig_up.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__plus")
			passhisto_sig_up.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__plus")


			failhisto_sig_up.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__plus")
			failhisto_sig_up.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__plus")


			failhisto_sig_down.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__minus")
			failhisto_sig_down.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__minus")


			passhisto_sig_down.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__minus")
			passhisto_sig_down.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__minus")



			passhisto_sig_up.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__plus")
			failhisto_sig_up.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__plus")
			failhisto_sig_down.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__minus")
			passhisto_sig_down.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig__TT_sig_tag"+addstrsf+"__minus")



			passhisto_semi_up = copy.copy(passhisto_semi)
			failhisto_semi_up = copy.copy(failhisto_semi)

			passhisto_semi_down = copy.copy(passhisto_semi)
			failhisto_semi_down = copy.copy(failhisto_semi)

			failhisto_semi_up.Scale(1.0-(effscale)*passhisto_semi.Integral()/(failhisto_semi.Integral()+passhisto_semi.Integral()))
			passhisto_semi_up.Scale(1.0+(effscale)*failhisto_semi.Integral()/(failhisto_semi.Integral()+passhisto_semi.Integral()))

			failhisto_semi_down.Scale(1.0-(-effscale)*passhisto_semi.Integral()/(failhisto_semi.Integral()+passhisto_semi.Integral()))
			passhisto_semi_down.Scale(1.0+(-effscale)*failhisto_semi.Integral()/(failhisto_semi.Integral()+passhisto_semi.Integral()))
			
			print "inttest",failhisto_semi_down.Integral() + passhisto_semi_down.Integral()
			print "inttest",failhisto_semi_up.Integral() + passhisto_semi_up.Integral()



			passhisto_semi_up.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__plus")
			passhisto_semi_up.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__plus")
			passhisto_semi_up.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__plus")

			failhisto_semi_up.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__plus")
			failhisto_semi_up.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__plus")
			failhisto_semi_up.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__plus")

			failhisto_semi_down.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__minus")
			failhisto_semi_down.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__minus")
			failhisto_semi_down.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__minus")

			passhisto_semi_down.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__minus")
			passhisto_semi_down.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__minus")
			passhisto_semi_down.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi__TT_semi_tag"+addstrsf+"__minus")
			





		failhisto_semi.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi"+unctowrite)
		failhisto_semi.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi"+unctowrite)
		failhisto_semi.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_semi"+unctowrite)
	
		passhisto_semi.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi"+unctowrite)
		passhisto_semi.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi"+unctowrite)
		passhisto_semi.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_semi"+unctowrite)


		failhisto_sig.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+"_sig"+unctowrite)
		passhisto_sig.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+"_sig"+unctowrite)


	output.cd()



	

	failhisto.SetName("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+unctowrite)
	failhisto.SetTitle("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+unctowrite)
	failhisto.Write("mtop"+addstrsf+"_"+options.anatype+"fail__"+writeset+unctowrite)

	passhisto.SetName("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+unctowrite)
	passhisto.SetTitle("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+unctowrite)
	passhisto.Write("mtop"+addstrsf+"_"+options.anatype+"pass__"+writeset+unctowrite)

	print "write " +writeset+unctowrite
print "writing",output
output.cd()
output.Write()
output.ls()
output.Close()
print "Done!"
sys.exit



