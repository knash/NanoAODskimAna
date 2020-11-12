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
parser.add_option('-r', '--run', metavar='F', type='string', action='store',
                  default	=	'NONE',
                  dest		=	'run',
                  help		=	'')
(options, args) = parser.parse_args()
ROOT.gROOT.LoadMacro("insertlogo.C+")
setname = options.set
isdata=False
if (setname).find('JetHT')!=-1:
	isdata=True
NanoF = NanoAODskim_Functions(options.anatype,options.era)
candl = NanoF.candl
probl = NanoF.probl
runstr="Run"+options.era+options.run
if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True



output = ROOT.TFile("NanoAODskim_TrigMaker__"+options.era+"__"+runstr+".root","recreate")
inputfile = TFile('rootfiles_trig/NanoAODskim_Trig'+options.era+'__'+runstr+'.root','open')
hthistpost=inputfile.Get("postHT")
hthistpre=inputfile.Get("preHT")
hthistpost.Rebin(2)
hthistpre.Rebin(2)
trighistht=copy.copy(hthistpost)
trighistht.Divide(hthistpre)


htmasshistpost=inputfile.Get("postHTmass")
htmasshistpre=inputfile.Get("preHTmass")
copyhtmasshistpost=copy.deepcopy(htmasshistpost)
copyhtmasshistpre=copy.deepcopy(htmasshistpre)
copyhtmasshistpost.GetYaxis().SetRangeUser(65.0,1000.0)
copyhtmasshistpre.GetYaxis().SetRangeUser(65.0,1000.0)
htmasshistpost.Rebin2D(2,2)
htmasshistpre.Rebin2D(2,2)
trighisthtmass=copy.copy(htmasshistpost)
trighisthtmass.Divide(htmasshistpre)
output.cd()
trighistht.Write("trighistht")
trighisthtmass.Write("trighisthtmass")

output.Write()
output.Close()
c3 = TCanvas('c3', '', 700, 600)
c3.SetLeftMargin(0.16)
c3.SetRightMargin(0.16)
c3.SetTopMargin(0.11)
c3.SetBottomMargin(0.1)



trighisthtmass.SetStats(0)
trighisthtmass.SetTitle(';H_{T}(GeV);m_{softdrop}(GeV)')
trighisthtmass.GetYaxis().SetLabelSize(.05)
trighisthtmass.GetYaxis().SetTitleSize(.05)
trighisthtmass.GetYaxis().SetTitleOffset(1.4)



trighisthtmass.Draw("colz")
if options.era=="2016":
	per=1
if options.era=="2017":
	per=2
if options.era=="2018":
	per=3

ROOT.insertlogo( c3, per, 11 )

prelim = TLatex()
prelim.SetNDC()
prelim.DrawLatex( 0.2, 0.91, runstr )

c3.Print('plots/trigplot2D_ht_msd_'+runstr+'__'+options.era+'.root', 'root')
c3.Print('plots/trigplot2D_ht_msd_'+runstr+'__'+options.era+'.pdf', 'pdf')
c3.Print('plots/trigplot2D_ht_msd_'+runstr+'__'+options.era+'.png', 'png')

c2 = TCanvas('c2', '', 700, 600)
c2.SetLeftMargin(0.16)
c2.SetRightMargin(0.1)
c2.SetTopMargin(0.11)
c2.SetBottomMargin(0.1)

cuttrighisthtpost=copyhtmasshistpost.ProjectionX()
cuttrighisthtpre=copyhtmasshistpre.ProjectionX()
cuttrighistht=copy.copy(cuttrighisthtpost)
cuttrighistht.Divide(cuttrighisthtpre)


cuttrighistht.GetXaxis().SetRangeUser(500.,2000.)
cuttrighistht.GetYaxis().SetRangeUser(0.85,1.0)
cuttrighistht.SetStats(0)
cuttrighistht.SetTitle(';H_{T}(GeV);Efficiency')
cuttrighistht.GetYaxis().SetLabelSize(.05)
cuttrighistht.GetYaxis().SetTitleSize(.05)
cuttrighistht.GetYaxis().SetTitleOffset(1.4)
cuttrighistht.Draw("hist")

ROOT.insertlogo( c2, per, 11 )

prelim = TLatex()
prelim.SetNDC()
prelim.DrawLatex( 0.2, 0.91, runstr )

c2.Print('plots/trigplot1D_ht_'+runstr+'__'+options.era+'.root', 'root')
c2.Print('plots/trigplot1D_ht_'+runstr+'__'+options.era+'.pdf', 'pdf')
c2.Print('plots/trigplot1D_ht_'+runstr+'__'+options.era+'.png', 'png')



print "Completed..."


