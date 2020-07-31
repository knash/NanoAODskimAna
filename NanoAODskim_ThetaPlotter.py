import NanoAODskim_Functions	
from NanoAODskim_Functions import *

from optparse import OptionParser
import subprocess,os,sys

parser = OptionParser()

parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('-e', '--era', metavar='F', type='string', action='store',
                  default	=	'2017',
                  dest		=	'era',
                  help		=	'2016,2017, or 2018')



(options, args) = parser.parse_args()
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

regiontoname=	{
		"C":"C, Signal",
		"K":"K, Medium t",
		"H":"H, Medium V",
		"F":"F, Validation",
		"ZC":"Low mass t",
		"FT":"ttbar measurement",
		}

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

uncdict={}

print eras
for era in eras:

	infile=TFile("limitsetting/theta/NanoAODskim_"+options.anatype+"_ForLimits__"+era+"central.root","open")	
	print dir(infile)
	histodict={}
	for ff in infile.GetListOfKeys():
		curhist = ff.ReadObj()
		parsed = curhist.GetName().split("__")
		if not (parsed[0]+parsed[1]) in histodict:
			histodict[parsed[0]+parsed[1]]={}
		if len(parsed)==2:
			histodict[parsed[0]+parsed[1]][""]=curhist
		if len(parsed)>2:
			if not parsed[-2] in histodict[parsed[0]+parsed[1]]:
				histodict[parsed[0]+parsed[1]][parsed[-2]]=[None,None]
			if parsed[-1]=="plus":
				histodict[parsed[0]+parsed[1]][parsed[-2]][0]=curhist
			if parsed[-1]=="minus":
				histodict[parsed[0]+parsed[1]][parsed[-2]][1]=curhist


	for hk in histodict:
		print hk
		nom=histodict[hk][""]
		for key in histodict[hk]:
			if key=="":
				continue
			
			c2.cd()
			histodict[hk][key][0].SetLineColor(2)
			histodict[hk][key][1].SetLineColor(3)
			histodict[hk][key][0].SetFillColor(0)
			histodict[hk][key][1].SetFillColor(0)
			histodict[hk][key][0].SetLineStyle(1)
			histodict[hk][key][1].SetLineStyle(1)
			histodict[hk][key][0].SetLineWidth(2)
			histodict[hk][key][1].SetLineWidth(2)
			leg = TLegend(0.55, 0.5, 0.84, 0.84)
			leg.SetFillColor(0)
			leg.SetBorderSize(0)
			nom.SetMaximum(1.2*max(histodict[hk][key][0].GetMaximum(),histodict[hk][key][1].GetMaximum()))	
			nom.SetTitle(';M_{'+options.anatype+'};Events/Bin')	
			nom.SetStats(0)			
			nom.SetLineColor(1)
			nom.SetFillColor(0)


			nom.SetLineStyle(1)
			nom.SetLineWidth(2)

			nom.Draw("hist")
			histodict[hk][key][0].Draw("histsame")
			histodict[hk][key][1].Draw("histsame")
			nom.Draw("histsame")
			leg.Draw()
			
			if hk.split("_")[2]=="C" and (hk.split("_")[-1] in ["3000","2017ttbar","2017qcd","2017st"]):
				uncdict[hk+key]=0.5*abs(histodict[hk][key][1].Integral()-histodict[hk][key][0].Integral())/nom.Integral()
			leg.AddEntry( nom, 'nominal', 'l')
			leg.AddEntry( histodict[hk][key][0], key+' up', 'l')
			leg.AddEntry( histodict[hk][key][1], key+' down', 'l')
			prelim = TLatex()
			prelim.SetNDC()
			prelim.DrawLatex( 0.2, 0.91, "Region: "+regiontoname[hk.split("_")[2]] )
			c2.Print('plots/unc'+options.anatype+'__'+era+'__'+hk+key+'.root', 'root')
			c2.Print('plots/unc'+options.anatype+'__'+era+'__'+hk+key+'.pdf', 'pdf')
			c2.Print('plots/unc'+options.anatype+'__'+era+'__'+hk+key+'.png', 'png')
		
for uu in uncdict:
	print uu,uncdict[uu]*100,"%"

print "Completed..."																										

