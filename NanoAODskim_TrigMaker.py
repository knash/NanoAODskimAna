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
htmasshistpost.Rebin2D(2,2)
htmasshistpre.Rebin2D(2,2)
trighisthtmass=copy.copy(htmasshistpost)
trighisthtmass.Divide(htmasshistpre)
output.cd()
trighistht.Write("trighistht")
trighisthtmass.Write("trighisthtmass")
output.Write()
output.Close()
print "Completed..."

