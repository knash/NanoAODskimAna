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
if options.era=="2016":
	mcfile=TFile("PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/pileup_profile_Summer16.root")
	datafile=TFile("PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/PileupData_GoldenJSON_Full2016.root")
if options.era=="2017":
	mcfile=TFile("PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileup2017.root")
	datafile=TFile("PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/puData2017_withVar.root")
if options.era=="2018":
	mcfile=TFile("PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/mcPileup2018.root")
	datafile=TFile("PhysicsTools/NanoAODTools/python/postprocessing/data/pileup/puData2018_withVar.root")



mchist = mcfile.Get("pu_mc")
mchist.Scale(1.0/mchist.Integral())
pileuphist = datafile.Get("pileup")
pileuphist.Scale(1.0/pileuphist.Integral())
pileup_plushist = datafile.Get("pileup_plus")
pileup_plushist.Scale(1.0/pileup_plushist.Integral())
pileup_minushist = datafile.Get("pileup_minus")
pileup_minushist.Scale(1.0/pileup_minushist.Integral())


output = ROOT.TFile("NanoAODskim_PUMaker__"+options.era+".root","recreate")

purwnom=copy.copy(pileuphist)
purwnom.Divide(mchist)

purwup=copy.copy(pileup_plushist)
purwup.Divide(mchist)

purwdown=copy.copy(pileup_minushist)
purwdown.Divide(mchist)

output.cd()

purwnom.Write("purwnom")
purwup.Write("purwup")
purwdown.Write("purwdown")
output.Write()
output.Close()
print "Completed..."


