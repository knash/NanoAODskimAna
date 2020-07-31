#! /usr/bin/env python
import os
import copy
from math import *

from optparse import OptionParser
parser = OptionParser()


parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
		  default	=	'Mu',
		  dest		=	'anatype',
		  help		=	'')
parser.add_option('-w', '--plot', metavar='F', type='string', action='store',
                  default	=	'both',
                  dest		=	'plot',
                  help		=	'pass or fail')

parser.add_option('-e', '--era', metavar='F', type='string', action='store',
		  default	=	'2017',
		  dest		=	'era',
		  help		=	'2016,2017, or 2018')

parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')



parser.add_option('-p', '--pt', metavar='F', type='string', action='store',
                  default	=	'ALL',
                  dest		=	'pt',
                  help		=	'')



parser.add_option('-d', '--disc', metavar='F', type='string', action='store',
                  default	=	'0.9',
                  dest		=	'disc',
                  help		=	'')



parser.add_option('-v', '--ver', metavar='F', type='string', action='store',
                  default	=	'',
                  dest		=	'ver',
                  help		=	'')

parser.add_option('--bsum', metavar='F', action='store_true',
		  default=False,
		  dest='bsum',
		  help='bsum')


(options, args) = parser.parse_args()

import ROOT
import array
import glob
import sys
from array import *
from ROOT import *

gROOT.LoadMacro("insertlogo.C+")


if options.era=="2016":
	per=1
if options.era=="2017":
	per=2
if options.era=="2018":
	per=3

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True



title = ';M_{SD} (GeV);Counts'

string = ""

ROOT.gROOT.Macro("rootlogon.C")

cnnstr = "_CNN"+(options.disc).replace(".","p")
ptstr ="_Pt"+(options.pt)

if options.pt=="ALL":
	ptfiles = glob.glob("ThetaFile_ttfit_"+options.anatype+options.era+"_*"+cnnstr+".root")
	print ptfiles
	ptstrings = []
	for curptstring in ptfiles:
		ptstrings.append(curptstring.replace("ThetaFile_ttfit_"+options.anatype+options.era+"_","").replace(cnnstr+".root",""))
else:
	ptstrings = [ptstr]
print ptstrings
SFdict = {}
SFdictbmerge = {}
verstr=options.ver

firnarr=[]
firnarr1=[]
for curptrange in ptstrings:

	File = ROOT.TFile("ThetaFile_ttfit_Mu"+options.era+"_"+curptrange+cnnstr+".root")
	FileEle = ROOT.TFile("ThetaFile_ttfit_Ele"+options.era+"_"+curptrange+cnnstr+".root")

	if options.plot!='both':
		passfs = [options.plot]
	else:
		passfs = ['fail','pass']
		fituncs = {}
		systuncs = {}



	mrangefail = [0.0,260.0]
	mrangepass = [140.0,220.0]
	#mrangepass = [0.0,260.0]
	norms = {}
	normspre = {}
	normspreorig = {}
	normsup = {}
	normsdown = {}
	normspreup = {}
	normspredown = {}

	normsbmerge = {}
	normsprebmerge = {}
	normspreorigbmerge = {}
	normsupbmerge = {}
	normsdownbmerge = {}
	normspreupbmerge = {}
	normspredownbmerge = {}

	totnevmc = 0.0
	totnevmcbmerge = 0.0
	
	for passf in passfs:
		if passf=='fail':
			xaxisrange = [0.,220.]
			mrange = mrangefail
		else:
			xaxisrange = [60.,220.]
			mrange = mrangepass

		st1= ROOT.THStack("st1", "st1")
		st2= ROOT.THStack("st2", "st2")

		leg = TLegend(0.2, 0.4, 0.45, 0.7)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)

		leg1 = TLegend(0.55, 0.5, 0.84, 0.84)
		leg1.SetFillColor(0)
		leg1.SetBorderSize(0)




		c1 = TCanvas('c1'+passf, 'c1', 800, 600)
		c2 = TCanvas('c2'+passf, 'c2', 800, 600)
		pre_data = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__DATA")
		pre_TT = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT")
		pre_TT_sig = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
		pre_TT_semi = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_semi")
		if not options.bsum:
			pre_TT_bmerge = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
		#pre_st = File.Get("mtop_"+passf+"__st")
		pre_WJetsToLNu = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__WJetsToLNu")
		pre_QCD = File.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__QCD")

		pre_data.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__DATA"))
		pre_TT.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"))
		pre_TT_sig.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
		pre_TT_semi.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_semi"))
		if not options.bsum:
			pre_TT_bmerge.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
		#pre_st = FileEle.Get("mtop_"+passf+"__st")
		pre_WJetsToLNu.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__WJetsToLNu"))
		pre_QCD.Add(FileEle.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__QCD"))

		totnevmc+=pre_TT_sig.GetEntries()
		if not options.bsum:
			totnevmcbmerge+=pre_TT_bmerge.GetEntries()
		#NormFile = ROOT.TFile("histos-CNN-TTrate_syst"+curptrange+cnnstr+".root")
		#post_norm_TT = NormFile.Get("mtop_"+passf+"__TT")
		#post_norm_TT_sig = NormFile.Get("mtop_"+passf+"__TT_sig")
		#post_norm_TT_semi = NormFile.Get("mtop_"+passf+"__TT_semi")
		#post_norm_TT_bmerge = NormFile.Get("mtop_"+passf+"__TT_bmerge")
		#post_norm_st = NormFile.Get("mtop_"+passf+"__st")
		#post_norm_WJetsToLNu = NormFile.Get("mtop_"+passf+"__WJetsToLNu")
		#post_norm_QCD = NormFile.Get("mtop_"+passf+"__QCD")

		#TagFile = ROOT.TFile("histos-CNN-TTtag_syst"+curptrange+cnnstr+".root")
		#post_tag_TT = TagFile.Get("mtop_"+passf+"__TT")
		#post_tag_TT_sig = TagFile.Get("mtop_"+passf+"__TT_sig")
		#post_tag_TT_semi = TagFile.Get("mtop_"+passf+"__TT_semi")
		#post_tag_TT_bmerge = TagFile.Get("mtop_"+passf+"__TT_bmerge")
		#post_tag_st = TagFile.Get("mtop_"+passf+"__st")
		#post_tag_WJetsToLNu = TagFile.Get("mtop_"+passf+"__WJetsToLNu")
		#post_tag_QCD = TagFile.Get("mtop_"+passf+"__QCD")


		extrstr="ThetaFile_ttfit_"+options.era+"_"

		pr1File = ROOT.TFile("histos-CNN-mle_syst-preALL"+verstr+".root")
		pr1_TT_sig = pr1File.Get("mtop_"+passf+"__TT_sig")
	


		PoFile = ROOT.TFile("histos-CNN-mle_systALL"+verstr+".root")
		post_TT = PoFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT")
		post_TT_sig = PoFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
		post_TT_semi = PoFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_semi")
		if not options.bsum:
			post_TT_bmerge = PoFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
		#post_st = PoFile.Get("mtop_"+passf+"__st")
		post_WJetsToLNu = PoFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__WJetsToLNu")
		post_QCD = PoFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__QCD")


		post_TT.Add(PoFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"))
		post_TT_sig.Add(PoFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
		post_TT_semi.Add(PoFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_semi"))
		if not options.bsum:
			post_TT_bmerge.Add(PoFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
		#post_st = PoFile.Get("mtop_"+passf+"__st")
		post_WJetsToLNu.Add(PoFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__WJetsToLNu"))
		post_QCD.Add(PoFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__QCD"))


		
		ABFile = ROOT.TFile("histos-CNN-mle_syst-ABALL"+verstr+".root")
		AB_TT_sig = ABFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
		AB_TT_sig.Add(ABFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))

		if not options.bsum:
			ABFilebmerge = ROOT.TFile("histos-CNN-mle_syst-ABALL"+verstr+"_bmerge.root")
			AB_TT_bmerge = ABFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
			AB_TT_bmerge.Add(ABFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))

		#ABFile = ROOT.TFile("histos-CNN-mle_syst-preALL"+verstr+".root")
		#AB_TT_sig = ABFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
		#AB_TT_sig.Add(ABFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))


		#ABFilebmerge = ROOT.TFile("histos-CNN-mle_syst-preALL"+verstr+".root")
		#AB_TT_bmerge = ABFile.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
		#AB_TT_bmerge.Add(ABFile.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))

	    	uncstot=['jer','jes']
	    	#uncstot=['jer','jes','btag','tptrw']
	    	#uncstot=[]

		totalbkgunc = copy.copy(post_TT).Scale(0.)
		TTbkgunc = copy.copy(post_TT).Scale(0.)


		print "SFfromparam",post_TT_sig.Integral()/AB_TT_sig.Integral()
		intbins=(post_TT_sig.FindBin(mrange[0]),post_TT_sig.FindBin(mrange[1])-1)
		print "TrueRange",post_TT_sig.GetBinLowEdge(intbins[0]),post_TT_sig.GetBinLowEdge(intbins[1])+post_TT_sig.GetBinWidth(intbins[1])
		for rrr in xrange(post_TT_sig.GetNbinsX()+1):
			print post_TT_sig.GetBinContent(rrr),post_TT_sig.GetBinLowEdge(rrr),post_TT_sig.GetBinLowEdge(rrr)+post_TT_sig.GetBinWidth(rrr)
		print  post_TT_sig.Integral(*intbins)
		norms[passf] = post_TT_sig.Integral(*intbins)
		normspre[passf] = AB_TT_sig.Integral(*intbins)
		normspreorig[passf] = pre_TT_sig.Integral(*intbins)
		normsup[passf] = {}
		normsdown[passf] = {}
		normspreup[passf] = {}
		normspredown[passf] = {}

		if not options.bsum:
			normsbmerge[passf] = post_TT_bmerge.Integral(*intbins)
			normsprebmerge[passf] = AB_TT_bmerge.Integral(*intbins)
			normspreorigbmerge[passf] = pre_TT_bmerge.Integral(*intbins)
			normsupbmerge[passf] = {}
			normsdownbmerge[passf] = {}
			normspreupbmerge[passf] = {}
			normspredownbmerge[passf] = {}
		for curunc in uncstot:
			tempfile_up = ROOT.TFile("postfithistos/histos-CNN-"+curunc+"up_systALL"+verstr+".root")
			tempfile_down = ROOT.TFile("postfithistos/histos-CNN-"+curunc+"down_systALL"+verstr+".root")

			post_TT_up = tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT")
			post_TT_sig_up = tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
			post_TT_semi_up = tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_semi")
			if not options.bsum:
				post_TT_bmerge_up = tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
			#post_st_up = tempfile_up.Get("mtop_"+passf+"__st")
			post_WJetsToLNu_up = tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__WJetsToLNu")
			post_QCD_up = tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__QCD")
			print  post_TT_up,"mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"
			print "postfithistos/histos-CNN-"+curunc+"up_systALL"+verstr+".root"
			post_TT_up.Add(tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"))
			post_TT_sig_up.Add(tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
			post_TT_semi_up.Add(tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_semi"))
			if not options.bsum:
				post_TT_bmerge_up.Add(tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
			#post_st_up = tempfile_up.Get("mtop_"+passf+"__st"))
			post_WJetsToLNu_up.Add(tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__WJetsToLNu"))
			post_QCD_up.Add(tempfile_up.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__QCD"))




			post_TT_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT")
			post_TT_sig_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
			post_TT_semi_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_semi")
			if not options.bsum:
				post_TT_bmerge_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
			#post_st_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__st")
			post_WJetsToLNu_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__WJetsToLNu")
			post_QCD_down = tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__QCD")

			post_TT_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"))
			post_TT_sig_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
			post_TT_semi_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_semi"))
			if not options.bsum:
				post_TT_bmerge_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
			#post_st_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__st"))
			post_WJetsToLNu_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__WJetsToLNu"))
			post_QCD_down.Add(tempfile_down.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__QCD"))


			normsup[passf][curunc] = post_TT_sig_up.Integral(*intbins)
			normsdown[passf][curunc] = post_TT_sig_down.Integral(*intbins)
			if not options.bsum:
				normsupbmerge[passf][curunc] = post_TT_bmerge_up.Integral(*intbins)
				normsdownbmerge[passf][curunc] = post_TT_bmerge_down.Integral(*intbins)


			tempfile_up_pre = ROOT.TFile("prefithistos/histos-CNN-"+curunc+"up_systALL"+verstr+".root")
			tempfile_down_pre = ROOT.TFile("prefithistos/histos-CNN-"+curunc+"down_systALL"+verstr+".root")

			pre_TT_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT")
			pre_TT_sig_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
			pre_TT_semi_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_semi")
			if not options.bsum:
				pre_TT_bmerge_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
			#pre_st_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__st")
			pre_WJetsToLNu_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__WJetsToLNu")
			pre_QCD_up = tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__QCD")


			pre_TT_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"))
			pre_TT_sig_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
			pre_TT_semi_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_semi"))
			if not options.bsum:
				pre_TT_bmerge_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
			#pre_st_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__st"))
			pre_WJetsToLNu_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__WJetsToLNu"))
			pre_QCD_up.Add(tempfile_up_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__QCD"))




			pre_TT_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT")
			pre_TT_sig_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
			pre_TT_semi_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_semi")
			if not options.bsum:
				pre_TT_bmerge_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
			#pre_st_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__st")
			pre_WJetsToLNu_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__WJetsToLNu")
			pre_QCD_down = tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__QCD")



			pre_TT_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT"))
			pre_TT_sig_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
			pre_TT_semi_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_semi"))
			if not options.bsum:
				pre_TT_bmerge_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
			#pre_st_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__st"))
			pre_WJetsToLNu_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__WJetsToLNu"))
			pre_QCD_down.Add(tempfile_down_pre.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__QCD"))


			normspreup[passf][curunc] = pre_TT_sig_up.Integral(*intbins)
			normspredown[passf][curunc] = pre_TT_sig_down.Integral(*intbins)
			if not options.bsum:
				normspreupbmerge[passf][curunc] = pre_TT_bmerge_up.Integral(*intbins)
				normspredownbmerge[passf][curunc] = pre_TT_bmerge_down.Integral(*intbins)


			print normspreup[passf][curunc]
			print normspredown[passf][curunc]

			#for xbin in range(0,TTbkgunc.GetXaxis().GetNbins()+1)
			#	prebkgunc=TTbkgunc.GetBinContent(xbin)
			#	curunc_up=post_TT_sig_up.GetBinContent(xbin)
			#	curunc_down=post_TT_sig_down.GetBinContent(xbin)
			#	curuncsymave = 0.5*abs(curunc_up-curunc_down)


		post_TT.SetFillColor(ROOT.kRed+3)
		post_TT_semi.SetFillColor(ROOT.kRed+2)
		if not options.bsum:
			post_TT_bmerge.SetFillColor(ROOT.kRed+1)
		post_TT_sig.SetFillColor(ROOT.kRed)

		post_WJetsToLNu.SetFillColor(ROOT.kGreen)
		#post_st.SetFillColor(ROOT.kBlue)
		post_QCD.SetFillColor(ROOT.kYellow)
		pre_data.SetLineColor(1)
		pre_data.SetMarkerColor(1)
		pre_data.SetMarkerStyle(20)
		pre_data.SetMarkerSize(0.7)

		leg.AddEntry( pre_data, 'Data', 'P')
		leg.AddEntry( post_QCD, 'QCD', 'F')
		leg.AddEntry( post_WJetsToLNu, 'W+Jets', 'F')
		#leg.AddEntry( post_st, 'Single top', 'F')
		leg.AddEntry( post_TT, 't#bar{t} unmerged', 'F')
		leg.AddEntry( post_TT_semi, 't#bar{t} b(qq)', 'F')
		if not options.bsum:
			leg.AddEntry( post_TT_bmerge, 't#bar{t} (bq)q', 'F')
			leg.AddEntry( post_TT_sig, 't#bar{t} (bqq)', 'F')
		else:
			leg.AddEntry( post_TT_sig, 't#bar{t} (bqq)+(bq)q', 'F')

		leg1.AddEntry( pre_data, 'Data', 'P')
		leg1.AddEntry( post_QCD, 'QCD', 'F')
		leg1.AddEntry( post_WJetsToLNu, 'W+Jets', 'F')
		#leg.AddEntry( post_st, 'Single top', 'F')
		leg1.AddEntry( post_TT, 't#bar{t} unmerged', 'F')
		leg1.AddEntry( post_TT_semi, 't#bar{t} b(qq)', 'F')
		if not options.bsum:
			leg1.AddEntry( post_TT_bmerge, 't#bar{t} (bq)q', 'F')
			leg1.AddEntry( post_TT_sig, 't#bar{t} (bqq)', 'F')
		else:
			leg1.AddEntry( post_TT_sig, 't#bar{t} (bqq)+(bq)q', 'F')
		st1.Add(post_QCD)
		st1.Add(post_WJetsToLNu)
		st1.Add(post_TT)
		if not options.bsum:
			st1.Add(post_TT_bmerge)
		#st1.Add(post_st)
		st1.Add(post_TT_semi)
		st1.Add(post_TT_sig)


		c1.cd()
		st1.SetMinimum(0.1)
		st1.SetTitle(title)
		st1.Draw("hist")
		st1.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])
		gPad.SetLeftMargin(0.12)
		st1.GetYaxis().SetTitleOffset(0.98)
		pre_data.Draw("samep")
		if passf=="pass":
			st1.SetMaximum(pre_data.GetMaximum() * 2.5)
			leg.Draw()
		if passf=="fail":
			st1.SetMaximum(pre_data.GetMaximum() * 2.5)
			leg1.Draw()



		prelim = TLatex()
		prelim.SetNDC()
		prelim.DrawLatex( 0.1, 0.91, "#scale[0.8]{Post Fitting "+passf+"   "+curptrange+"}" )
		ROOT.insertlogo( c1, per, 11 )

		c1.Update()

		c1.Print('plots/TTfitCNN'+passf+extrstr+curptrange+cnnstr+options.era+verstr+'.root', 'root')
		c1.Print('plots/TTfitCNN'+passf+extrstr+curptrange+cnnstr+options.era+verstr+'.pdf', 'pdf')


		#print "pre fit "
		#print "TT",pre_TT.Integral(*intbins)
		#print "TT_bmerge",pre_TT_bmerge.Integral(*intbins)
		#print "TT_semi",pre_TT_semi.Integral(*intbins)
		#print "TT_sig",pre_TT_sig.Integral(*intbins)


		#print "normal"
		#print "TT",post_norm_TT.Integral(*intbins),post_norm_TT.Integral(*intbins)/pre_TT.Integral(*intbins)
		#print "TT_semi",post_norm_TT_bmerge.Integral(*intbins),post_norm_TT_bmerge.Integral(*intbins)/pre_TT_bmerge.Integral(*intbins)
		#print "TT_semi",post_norm_TT_semi.Integral(*intbins),post_norm_TT_semi.Integral(*intbins)/pre_TT_semi.Integral(*intbins)
		#print "TT_sig",post_norm_TT_sig.Integral(*intbins),post_norm_TT_sig.Integral(*intbins)/pre_TT_sig.Integral(*intbins)

		#print "WJetsToLNu",post_norm_WJetsToLNu.Integral(*intbins)/pre_WJetsToLNu.Integral(*intbins)
		#print "QCD",post_norm_QCD.Integral(*intbins)/pre_QCD.Integral(*intbins)

		#print "scale factors"
		#print "TT",post_tag_TT.Integral(*intbins),post_tag_TT.Integral(*intbins)/pre_TT.Integral(*intbins)
		#print "TT_bmerge",post_tag_TT_bmerge.Integral(*intbins),post_tag_TT_bmerge.Integral(*intbins)/pre_TT_bmerge.Integral(*intbins)
		#print "TT_semi",post_tag_TT_semi.Integral(*intbins),post_tag_TT_semi.Integral(*intbins)/pre_TT_semi.Integral(*intbins)
		#print "TT_sig",post_tag_TT_sig.Integral(*intbins),post_tag_TT_sig.Integral(*intbins)/pre_TT_sig.Integral(*intbins)




		pre_TT.SetFillColor(ROOT.kRed+3)
		pre_TT_semi.SetFillColor(ROOT.kRed+2)
		if not options.bsum:
			pre_TT_bmerge.SetFillColor(ROOT.kRed+1)
		pre_TT_sig.SetFillColor(ROOT.kRed)
		pre_WJetsToLNu.SetFillColor(ROOT.kGreen)
		#pre_st.SetFillColor(ROOT.kBlue)
		pre_QCD.SetFillColor(ROOT.kYellow)



		st2.Add(pre_QCD)
		st2.Add(pre_WJetsToLNu)
		st2.Add(pre_TT)
		if not options.bsum:
			st2.Add(pre_TT_bmerge)
		#st2.Add(pre_st)
		st2.Add(pre_TT_semi)
		st2.Add(pre_TT_sig)


		c2.cd()

		st2.SetMinimum(0.1)
		st2.SetTitle(title)
		st2.Draw("hist")
		st2.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])
		gPad.SetLeftMargin(0.12)
		st2.GetYaxis().SetTitleOffset(0.98)
		pre_data.Draw("samep")
		if passf=="pass":
			st2.SetMaximum(pre_data.GetMaximum() * 2.5)
			leg.Draw()
		if passf=="fail":
			st2.SetMaximum(pre_data.GetMaximum() * 2.5)
			leg1.Draw()

		prelim = TLatex()
		prelim.SetNDC()
		#prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 13 TeV, 35 fb^{-1}  Pre Fitting "+passf+"}" )
		prelim.DrawLatex( 0.1, 0.91, "#scale[0.8]{Pre Fitting "+passf+"   "+curptrange+"}" )

		ROOT.insertlogo( c2, per, 11 )
		c2.Update()
		c2.Print('plots/TTprefitCNN'+passf+extrstr+curptrange+cnnstr+options.era+verstr+'.root', 'root')
		c2.Print('plots/TTprefitCNN'+passf+extrstr+curptrange+cnnstr+options.era+verstr+'.pdf', 'pdf')
	print "normspre"
	for nnn in  normspre:
		print  nnn,normspre[nnn]
	print "norms"
	for nnn in  norms:
		print  nnn,norms[nnn]
	print "normsup"
	for nnn in  normsup:
		print  nnn,normsup[nnn]
	print "normsdown"
	for nnn in  normsdown:
		print  nnn,normsdown[nnn]
	print "normspreup"
	for nnn in  normspreup:
		print  nnn,normspreup[nnn]
	print "normspredown"
	for nnn in  normspredown:
		print  nnn,normspredown[nnn]


	sqtotuncsys = 0.0

	for nnn in  normspreup["pass"]:
		print "----------"
		print nnn
		print normsup["pass"][nnn],normsup["fail"][nnn],normspreup["pass"][nnn],normspreup["fail"][nnn]
		print normsdown["pass"][nnn],normsdown["fail"][nnn],normspredown["pass"][nnn],normspredown["fail"][nnn]
		uncup = (normsup["pass"][nnn]/(normsup["pass"][nnn]+normsup["fail"][nnn]))/(normspreup["pass"][nnn]/(normspreup["pass"][nnn]+normspreup["fail"][nnn]))
		uncdown = (normsdown["pass"][nnn]/(normsdown["pass"][nnn]+normsdown["fail"][nnn]))/(normspredown["pass"][nnn]/(normspredown["pass"][nnn]+normspredown["fail"][nnn]))
		aveunc = 0.5*(uncup-uncdown)

		print "SFup: ",uncup
		print "SFdown: ",uncdown
		sqtotuncsys+=aveunc*aveunc
	totuncsys = sqrt(sqtotuncsys)
	postfit_ttup_file = ROOT.TFile("postfithistos/histos-CNN-TT_sig_tag_"+curptrange+cnnstr+"up_systALL"+verstr+".root")
	postfit_ttup_hist = postfit_ttup_file.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
	print postfit_ttup_file,"mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"
	postfit_ttup_hist.Add(postfit_ttup_file.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
	postfit_ttup = postfit_ttup_hist.Integral(*intbins)
	postfit_ttdown_file = ROOT.TFile("postfithistos/histos-CNN-TT_sig_tag_"+curptrange+cnnstr+"down_systALL"+verstr+".root")
	postfit_ttdown_hist = postfit_ttdown_file.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_sig")
	postfit_ttdown_hist.Add(postfit_ttdown_file.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_sig"))
	postfit_ttdown = postfit_ttdown_hist.Integral(*intbins)





	#statunc = 0.5*(postfit_ttup-postfit_ttdown)/norms["pass"]


	print "totalMCcounts = ",totnevmc 

	print "Eff MC"
	#print normspre["pass"],normspre["fail"]
	#print "ORIG",normspreorig["pass"],normspreorig["fail"]
	effmc = (normspre["pass"]/(normspre["pass"]+normspre["fail"]))
	statuncmc = sqrt((effmc*(1.0-effmc))/(totnevmc))
	print effmc,"+/-",statuncmc
	#print "ORIG",normspreorig["pass"]/(normspreorig["pass"]+normspreorig["fail"])
	print "Eff DATA"

	effdata =  (norms["pass"]/(norms["pass"]+norms["fail"]))

	print "mc eff comps",effmc,normspreorig["pass"]/(normspreorig["pass"]+normspreorig["fail"])
	print "norm,normpre",norms["pass"]+norms["fail"],normspre["pass"]+normspre["fail"]
	firnarr.append((norms["pass"]+norms["fail"])/(normspre["pass"]+normspre["fail"]))
	firnarr1.append((norms["pass"]+norms["fail"])/(normspreorig["pass"]+normspreorig["fail"]))

	print "up",postfit_ttup,"down",postfit_ttdown,"nom",norms["pass"]
	effupdata = postfit_ttup/(norms["pass"]+norms["fail"])
	effdowndata = postfit_ttdown/(norms["pass"]+norms["fail"])
	
	statuncdata = 0.5*(effupdata-effdowndata)



	print effdata,"+/-",statuncdata
	print "Scale factor"
	SFfinal= effdata/effmc
	#norms["pass"]/normspre["pass"]
	print "sf comps",effdata/effmc,norms["pass"]/normspre["pass"]
	totstat=SFfinal*sqrt( (statuncmc/effmc)*(statuncmc/effmc) + (statuncdata/effdata)*(statuncdata/effdata) )
	print "---"
	print curptrange
	print "---"
	print SFfinal,"+/-",totstat,"+/-",totuncsys
	print "---"
	SFdict["_"+curptrange]=[SFfinal,totstat,totuncsys]


	if not options.bsum:
		print ""
		print "BMERGE"
		print ""

		sqtotuncsysbmerge = 0.0

		for nnn in  normspreupbmerge["pass"]:
			uncup = (normsupbmerge["pass"][nnn]/(normsupbmerge["pass"][nnn]+normsupbmerge["fail"][nnn]))/(normspreupbmerge["pass"][nnn]/(normspreupbmerge["pass"][nnn]+normspreupbmerge["fail"][nnn]))
			uncdown = (normsdownbmerge["pass"][nnn]/(normsdownbmerge["pass"][nnn]+normsdownbmerge["fail"][nnn]))/(normspredownbmerge["pass"][nnn]/(normspredownbmerge["pass"][nnn]+normspredownbmerge["fail"][nnn]))
			aveunc = 0.5*(uncup-uncdown)
			sqtotuncsysbmerge+=aveunc*aveunc
		totuncsysbmerge = sqrt(sqtotuncsysbmerge)
		postfit_ttup_filebmerge = ROOT.TFile("postfithistos/histos-CNN-TT_bmerge_tag_"+curptrange+cnnstr+"up_systALL"+verstr+".root")
		postfit_ttup_histbmerge = postfit_ttup_filebmerge.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
		postfit_ttup_histbmerge.Add(postfit_ttup_filebmerge.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
		postfit_ttupbmerge = postfit_ttup_histbmerge.Integral(*intbins)
		postfit_ttdown_filebmerge = ROOT.TFile("postfithistos/histos-CNN-TT_bmerge_tag_"+curptrange+cnnstr+"down_systALL"+verstr+".root")
		postfit_ttdown_histbmerge = postfit_ttdown_filebmerge.Get("mtop_"+curptrange+cnnstr+"_Mu"+passf+"__TT_bmerge")
		postfit_ttdown_histbmerge.Add(postfit_ttdown_filebmerge.Get("mtop_"+curptrange+cnnstr+"_Ele"+passf+"__TT_bmerge"))
		postfit_ttdownbmerge = postfit_ttdown_histbmerge.Integral(*intbins)

		effmcbmerge = (normsprebmerge["pass"]/(normsprebmerge["pass"]+normsprebmerge["fail"]))
		statuncmcbmerge = sqrt((effmcbmerge*(1.0-effmcbmerge))/(totnevmcbmerge))

		effdatabmerge =  (normsbmerge["pass"]/(normsbmerge["pass"]+normsbmerge["fail"]))
		effupdatabmerge = postfit_ttupbmerge/(normsbmerge["pass"]+normsbmerge["fail"])
		effdowndatabmerge = postfit_ttdownbmerge/(normsbmerge["pass"]+normsbmerge["fail"])

		statuncdatabmerge = 0.5*(effupdatabmerge-effdowndatabmerge)


		SFfinalbmerge= effdatabmerge/effmcbmerge
		totstatbmerge=SFfinalbmerge*sqrt( (statuncmcbmerge/effmcbmerge)*(statuncmcbmerge/effmcbmerge) + (statuncdatabmerge/effdatabmerge)*(statuncdatabmerge/effdatabmerge) )

		SFdictbmerge["_"+curptrange]=[SFfinalbmerge,totstatbmerge,totuncsysbmerge]










if not options.bsum:

	print ""
	print "BMERGE SF"
	print SFdictbmerge
	print ""


print ""
print "SF"
print SFdict
print ""


ptSFhist =  TH1F("ptSFhist","",50, 400., 1400.)
bins = []
ptrangearr = []
for ptrangestr in SFdict:
	print ptrangestr.replace("_Pt","").split("to")
	ptrangearr.append(ptrangestr.replace("_Pt","").split("to"))
	print ptrangearr
	ptrangearr[-1] = [float(ptrangearr[-1][0]),float(ptrangearr[-1][1])]
	bins.append(ptrangearr[-1][0])
	bins.append(ptrangearr[-1][1])
bins = list(set(bins))
bins = sorted(bins)
bins=array('d',bins)


ptSFhist = ptSFhist.Rebin(len(bins)-1,"ptSFhist",bins)
ptSFhistupstat = copy.copy(ptSFhist)
ptSFhistdownstat = copy.copy(ptSFhist)
ptSFhistupfull = copy.copy(ptSFhist)
ptSFhistdownfull = copy.copy(ptSFhist)
cleanline1 = copy.copy(ptSFhist)
cleanline2 = copy.copy(ptSFhist)
for ibin in range(1,ptSFhist.GetXaxis().GetNbins()+1):
	lowbin = ptSFhist.GetBinLowEdge(ibin)
	upbin = lowbin + ptSFhist.GetBinWidth(ibin) 
	print lowbin,upbin
	print '_Pt'+str(int(lowbin))+'to'+str(int(upbin))
	cont = SFdict['_Pt'+str(int(lowbin))+'to'+str(int(upbin))][0]
	stat = SFdict['_Pt'+str(int(lowbin))+'to'+str(int(upbin))][1]
	syst = SFdict['_Pt'+str(int(lowbin))+'to'+str(int(upbin))][2]
	fullunc = sqrt(stat*stat+syst*syst)
	ptSFhist.SetBinContent(ibin,cont)
	ptSFhist.SetBinError(ibin,0.0000000001)
	ptSFhistupstat.SetBinContent(ibin,cont+stat)
	ptSFhistdownstat.SetBinContent(ibin,cont-stat)
	ptSFhistupfull.SetBinContent(ibin,cont+fullunc)
	ptSFhistdownfull.SetBinContent(ibin,cont-fullunc)
	if ibin%2==0:
		cleanline1.SetBinContent(ibin,cont-fullunc)
		cleanline2.SetBinContent(ibin,cont+fullunc)
	else:
		cleanline1.SetBinContent(ibin,cont+fullunc)
		cleanline2.SetBinContent(ibin,cont-fullunc)

csf = TCanvas('csf', 'csf', 800, 600)



ptSFhistupfull.GetYaxis().SetRangeUser(0.7,1.6)
ptSFhistupfull.SetFillColor(kOrange+1)
ptSFhistupstat.SetFillColor(kOrange)
ptSFhistdownstat.SetFillColor(kOrange+1)

ptSFhistupfull.SetLineColor(0)
ptSFhistdownfull.SetLineColor(0)
ptSFhistupstat.SetLineColor(kOrange+1)
ptSFhistdownstat.SetLineColor(kOrange+1)
cleanline1.SetLineColor(0)
cleanline2.SetLineColor(0)

ptSFhistupfull.SetLineWidth(0)
ptSFhistdownfull.SetLineWidth(0)
ptSFhistupstat.SetLineWidth(0)
ptSFhistdownstat.SetLineWidth(0)
cleanline1.SetLineWidth(0)
cleanline2.SetLineWidth(0)

ptSFhist.SetLineColor(1)
ptSFhist.SetLineWidth(2)
ptSFhist.SetLineStyle(2)

color  = TColor(9999,1., 1., 1.)
ptSFhistdownfull.SetFillColor(9999)

ptSFhistupfull.SetStats(0)
ptSFhistupfull.SetTitle(";p_{T};SF")
gPad.SetLeftMargin(0.12)
ptSFhistupfull.GetYaxis().SetTitleOffset(0.98)
ptSFhistupfull.GetYaxis().SetRangeUser(0.7,1.3)
ptSFhistupfull.GetXaxis().SetRangeUser(500,1400)
ptSFhistupfull.Draw('hist')
ptSFhistupstat.Draw('histsame')
ptSFhistdownstat.Draw('histsame')
ptSFhistdownfull.Draw('histsame')
ptSFhist.Draw('esame')
cleanline1.Draw('histsame')
cleanline2.Draw('histsame')





csf.RedrawAxis()
csf.Print('plots/ptSFhist'+options.era+verstr+'.root', 'root')
csf.Print('plots/ptSFhist'+options.era+verstr+'.pdf', 'pdf')
outputp1 = TFile("plots/topSF_"+options.era+verstr+".root","recreate")
ptSFhist.Write("SF")
ptSFhistupfull.Write("SFup")
ptSFhistdownfull.Write("SFdown")
outputp1.Close()
if verstr=="":
	outputp = TFile("../../topSF_"+options.era+verstr+".root","recreate")
	outputp.cd()
	ptSFhist.Write("SF")
	ptSFhistupfull.Write("SFup")
	ptSFhistdownfull.Write("SFdown")
	outputp.Close()

print "firnarr",firnarr
#print "firnarr1",firnarr1

