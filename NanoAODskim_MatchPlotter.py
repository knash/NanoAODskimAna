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

parser.add_option('--dogcvlq', metavar='F', action='store_true',
		  default=False,
		  dest='dogcvlq',
		  help='dogcvlq')

parser.add_option('--dogczh', metavar='F', action='store_true',
		  default=False,
		  dest='dogczh',
		  help='dogczh')
(options, args) = parser.parse_args()

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

c2 = TCanvas('c2', '', 700, 600)

eras=(options.era).split(",")


ROOT.gROOT.LoadMacro("insertlogo.C+")

rebins=	{
	"pt":4,
	"eta":1,
	"DR":1,
	}
if options.anatype=="tHb":

	plottingtons=	[
			"pt__t__all",
			"pt__H__all",
			"pt__b__all",
			"eta__t__all",
			"eta__H__all",
			"eta__b__all",
			"DR__bt__all",
			"DR__Hb__all",
			"DR__Ht__all"
			]
if options.anatype=="tZb":

	plottingtons=	[
			"pt__t__all",
			"pt__Z__all",
			"pt__b__all",
			"eta__t__all",
			"eta__Z__all",
			"eta__b__all",
			"DR__bt__all",
			"DR__Zb__all",
			"DR__Zt__all"
			]
for era in eras:
	colarr=[1,2,3,4,5,6,7]

	setname =options.set
	NanoF = NanoAODskim_Functions(options.anatype,era)
	labels = NanoF.labels 
	candl = NanoF.candl
	probl = NanoF.probl

	wpmasses=["2000","3000","4500"]
	sigfiles={}
	for wpmass in wpmasses:
		print wpmass

		sigfiles[wpmass]=glob.glob("NanoAODskimMatch_"+options.anatype+"Ana"+era+"__WpTo*_Wp"+wpmass+"*.root")
	print sigfiles


	for plot in plottingtons:
		var = plot.split("__")[0]
		rval = rebins[var]
		c2 = TCanvas('c2', '', 700, 600)
		allf=[]
		summedsigs=[]
		nsig=0

		leg1 = TLegend(0.15, 0.55, 0.6, 0.84)
		leg1.SetFillColor(0)
		leg1.SetBorderSize(0)
		for sigf in sigfiles:

			summedsigs.append(None)

			for VLQ in xrange(len(sigfiles[sigf])):
				allf.append(TFile(sigfiles[sigf][VLQ]))
				
				if summedsigs[-1]==None:
					summedsigs[-1]=allf[-1].Get(plot)
				else:
					summedsigs[-1].Add(allf[-1].Get(plot))
			#print sigfiles[sigf],VLQ, plot,summedsigs[-1].Integral()
			summedsigs[-1].Rebin(rval)
			summedsigs[-1].Scale(1.0/summedsigs[-1].Integral())
			summedsigs[-1].SetLineColor(colarr[nsig])


			
			leg1.AddEntry( summedsigs[-1], 'W\' at '+sigf+'GeV', 'L')
			if nsig==0:

				summedsigs[-1].SetStats(0)
				summedsigs[-1].SetMaximum(summedsigs[-1].GetMaximum()*1.9)
				summedsigs[-1].SetTitle(";"+plot+";Fraction")
				summedsigs[-1].Draw("hist")
			else:
				summedsigs[-1].Draw("samehist")
			nsig+=1
		leg1.Draw()
		c2.Print('plots/Match'+options.anatype+'__'+plot+'.root', 'root')
		c2.Print('plots/Match'+options.anatype+'__'+plot+'.pdf', 'pdf')
		c2.Print('plots/Match'+options.anatype+'__'+plot+'.png', 'png')
														

