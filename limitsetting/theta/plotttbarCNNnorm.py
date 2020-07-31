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
	norms = {}
	normspre = {}
	normsup = {}
	normsdown = {}
	normspreup = {}
	normspredown = {}

	totnevmc = 0.0
	
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
		pre_data = File.Get("mtop_Mu"+passf+"__DATA")
		pre_TT = File.Get("mtop_Mu"+passf+"__TT")
		pre_TT_sig = File.Get("mtop_Mu"+passf+"__TT_sig")
		totnevmc+=pre_TT_sig.GetEntries()
		pre_TT_semi = File.Get("mtop_Mu"+passf+"__TT_semi")
		pre_TT_bmerge = File.Get("mtop_Mu"+passf+"__TT_bmerge")
		#pre_st = File.Get("mtop_"+passf+"__st")
		pre_WJetsToLNu = File.Get("mtop_Mu"+passf+"__WJetsToLNu")
		pre_QCD = File.Get("mtop_Mu"+passf+"__QCD")

		pre_data.Add(FileEle.Get("mtop_Ele"+passf+"__DATA"))
		pre_TT.Add(FileEle.Get("mtop_Ele"+passf+"__TT"))
		pre_TT_sig.Add(FileEle.Get("mtop_Ele"+passf+"__TT_sig"))
		totnevmc+=pre_TT_sig.GetEntries()
		pre_TT_semi.Add(FileEle.Get("mtop_Ele"+passf+"__TT_semi"))
		pre_TT_bmerge.Add(FileEle.Get("mtop_Ele"+passf+"__TT_bmerge"))
		#pre_st = FileEle.Get("mtop_"+passf+"__st")
		pre_WJetsToLNu.Add(FileEle.Get("mtop_Ele"+passf+"__WJetsToLNu"))
		pre_QCD.Add(FileEle.Get("mtop_Ele"+passf+"__QCD"))

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

		pr1File = ROOT.TFile("histos-CNN-mle_syst-pre"+extrstr+curptrange+cnnstr+".root")
		pr1_TT_sig = pr1File.Get("mtop_"+passf+"__TT_sig")
	


		PoFile = ROOT.TFile("histos-CNN-mle_syst"+extrstr+curptrange+cnnstr+".root")
		post_TT = PoFile.Get("mtop_Mu"+passf+"__TT")
		post_TT_sig = PoFile.Get("mtop_Mu"+passf+"__TT_sig")
		post_TT_semi = PoFile.Get("mtop_Mu"+passf+"__TT_semi")
		post_TT_bmerge = PoFile.Get("mtop_Mu"+passf+"__TT_bmerge")
		#post_st = PoFile.Get("mtop_"+passf+"__st")
		post_WJetsToLNu = PoFile.Get("mtop_Mu"+passf+"__WJetsToLNu")
		post_QCD = PoFile.Get("mtop_Mu"+passf+"__QCD")


		post_TT.Add(PoFile.Get("mtop_Ele"+passf+"__TT"))
		post_TT_sig.Add(PoFile.Get("mtop_Ele"+passf+"__TT_sig"))
		post_TT_semi.Add(PoFile.Get("mtop_Ele"+passf+"__TT_semi"))
		post_TT_bmerge.Add(PoFile.Get("mtop_Ele"+passf+"__TT_bmerge"))
		#post_st = PoFile.Get("mtop_"+passf+"__st")
		post_WJetsToLNu.Add(PoFile.Get("mtop_Ele"+passf+"__WJetsToLNu"))
		post_QCD.Add(PoFile.Get("mtop_Ele"+passf+"__QCD"))



		ABFile = ROOT.TFile("histos-CNN-mle_syst-AB"+extrstr+curptrange+cnnstr+".root")
		AB_TT_sig = ABFile.Get("mtop_Mu"+passf+"__TT_sig")
		AB_TT_sig.Add(ABFile.Get("mtop_Ele"+passf+"__TT_sig"))
	    	uncstot=['jer','jes','tptrw']

		totalbkgunc = copy.copy(post_TT).Scale(0.)
		TTbkgunc = copy.copy(post_TT).Scale(0.)


		print "SFfromparam",post_TT_sig.Integral()/AB_TT_sig.Integral()
		intbins=(post_TT_sig.FindBin(mrange[0]),post_TT_sig.FindBin(mrange[1]))

		norms[passf] = post_TT_sig.Integral(*intbins)
		normspre[passf] = AB_TT_sig.Integral(*intbins)
		normsup[passf] = {}
		normsdown[passf] = {}
		normspreup[passf] = {}
		normspredown[passf] = {}

		for curunc in uncstot:
			tempfile_up = ROOT.TFile("postfithistos/histos-CNN-"+curunc+"up_syst"+extrstr+curptrange+cnnstr+".root")
			tempfile_down = ROOT.TFile("postfithistos/histos-CNN-"+curunc+"down_syst"+extrstr+curptrange+cnnstr+".root")

			post_TT_up = tempfile_up.Get("mtop_Mu"+passf+"__TT")
			post_TT_sig_up = tempfile_up.Get("mtop_Mu"+passf+"__TT_sig")
			post_TT_semi_up = tempfile_up.Get("mtop_Mu"+passf+"__TT_semi")
			post_TT_bmerge_up = tempfile_up.Get("mtop_Mu"+passf+"__TT_bmerge")
			#post_st_up = tempfile_up.Get("mtop_"+passf+"__st")
			post_WJetsToLNu_up = tempfile_up.Get("mtop_Mu"+passf+"__WJetsToLNu")
			post_QCD_up = tempfile_up.Get("mtop_Mu"+passf+"__QCD")

			post_TT_up.Add(tempfile_up.Get("mtop_Ele"+passf+"__TT"))
			post_TT_sig_up.Add(tempfile_up.Get("mtop_Ele"+passf+"__TT_sig"))
			post_TT_semi_up.Add(tempfile_up.Get("mtop_Ele"+passf+"__TT_semi"))
			post_TT_bmerge_up.Add(tempfile_up.Get("mtop_Ele"+passf+"__TT_bmerge"))
			#post_st_up = tempfile_up.Get("mtop_"+passf+"__st"))
			post_WJetsToLNu_up.Add(tempfile_up.Get("mtop_Ele"+passf+"__WJetsToLNu"))
			post_QCD_up.Add(tempfile_up.Get("mtop_Ele"+passf+"__QCD"))




			post_TT_down = tempfile_down.Get("mtop_Mu"+passf+"__TT")
			post_TT_sig_down = tempfile_down.Get("mtop_Mu"+passf+"__TT_sig")
			post_TT_semi_down = tempfile_down.Get("mtop_Mu"+passf+"__TT_semi")
			post_TT_bmerge_down = tempfile_down.Get("mtop_Mu"+passf+"__TT_bmerge")
			#post_st_down = tempfile_down.Get("mtop_Mu"+passf+"__st")
			post_WJetsToLNu_down = tempfile_down.Get("mtop_Mu"+passf+"__WJetsToLNu")
			post_QCD_down = tempfile_down.Get("mtop_Mu"+passf+"__QCD")

			post_TT_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__TT"))
			post_TT_sig_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__TT_sig"))
			post_TT_semi_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__TT_semi"))
			post_TT_bmerge_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__TT_bmerge"))
			#post_st_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__st"))
			post_WJetsToLNu_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__WJetsToLNu"))
			post_QCD_down.Add(tempfile_down.Get("mtop_Ele"+passf+"__QCD"))


			normsup[passf][curunc] = post_TT_sig_up.Integral(*intbins)
			normsdown[passf][curunc] = post_TT_sig_down.Integral(*intbins)


			tempfile_up_pre = ROOT.TFile("prefithistos/histos-CNN-"+curunc+"up_syst"+extrstr+curptrange+cnnstr+".root")
			tempfile_down_pre = ROOT.TFile("prefithistos/histos-CNN-"+curunc+"down_syst"+extrstr+curptrange+cnnstr+".root")

			pre_TT_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__TT")
			pre_TT_sig_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__TT_sig")
			pre_TT_semi_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__TT_semi")
			pre_TT_bmerge_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__TT_bmerge")
			#pre_st_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__st")
			pre_WJetsToLNu_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__WJetsToLNu")
			pre_QCD_up = tempfile_up_pre.Get("mtop_Mu"+passf+"__QCD")


			pre_TT_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__TT"))
			pre_TT_sig_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__TT_sig"))
			pre_TT_semi_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__TT_semi"))
			pre_TT_bmerge_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__TT_bmerge"))
			#pre_st_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__st"))
			pre_WJetsToLNu_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__WJetsToLNu"))
			pre_QCD_up.Add(tempfile_up_pre.Get("mtop_Ele"+passf+"__QCD"))




			pre_TT_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__TT")
			pre_TT_sig_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__TT_sig")
			pre_TT_semi_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__TT_semi")
			pre_TT_bmerge_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__TT_bmerge")
			#pre_st_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__st")
			pre_WJetsToLNu_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__WJetsToLNu")
			pre_QCD_down = tempfile_down_pre.Get("mtop_Mu"+passf+"__QCD")



			pre_TT_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__TT"))
			pre_TT_sig_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__TT_sig"))
			pre_TT_semi_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__TT_semi"))
			pre_TT_bmerge_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__TT_bmerge"))
			#pre_st_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__st"))
			pre_WJetsToLNu_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__WJetsToLNu"))
			pre_QCD_down.Add(tempfile_down_pre.Get("mtop_Ele"+passf+"__QCD"))


			normspreup[passf][curunc] = pre_TT_sig_up.Integral(*intbins)
			normspredown[passf][curunc] = pre_TT_sig_down.Integral(*intbins)
			print normspreup[passf][curunc]
			print normspredown[passf][curunc]








			#for xbin in range(0,TTbkgunc.GetXaxis().GetNbins()+1)
			#	prebkgunc=TTbkgunc.GetBinContent(xbin)
			#	curunc_up=post_TT_sig_up.GetBinContent(xbin)
			#	curunc_down=post_TT_sig_down.GetBinContent(xbin)
			#	curuncsymave = 0.5*abs(curunc_up-curunc_down)


		post_TT.SetFillColor(ROOT.kRed+3)
		post_TT_semi.SetFillColor(ROOT.kRed+2)
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
		leg.AddEntry( post_TT_bmerge, 't#bar{t} (bq)q', 'F')
		leg.AddEntry( post_TT_sig, 't#bar{t} (bqq)', 'F')


		leg1.AddEntry( pre_data, 'Data', 'P')
		leg1.AddEntry( post_QCD, 'QCD', 'F')
		leg1.AddEntry( post_WJetsToLNu, 'W+Jets', 'F')
		#leg.AddEntry( post_st, 'Single top', 'F')
		leg1.AddEntry( post_TT, 't#bar{t} unmerged', 'F')
		leg1.AddEntry( post_TT_semi, 't#bar{t} b(qq)', 'F')
		leg1.AddEntry( post_TT_bmerge, 't#bar{t} (bq)q', 'F')
		leg1.AddEntry( post_TT_sig, 't#bar{t} (bqq)', 'F')

		st1.Add(post_QCD)
		st1.Add(post_WJetsToLNu)
		st1.Add(post_TT)
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
			st1.SetMaximum(pre_data.GetMaximum() * 1.5)
			leg1.Draw()



		prelim = TLatex()
		prelim.SetNDC()
		prelim.DrawLatex( 0.1, 0.91, "#scale[0.8]{Post Fitting "+passf+"   "+curptrange+"}" )
		ROOT.insertlogo( c1, per, 11 )

		c1.Update()

		c1.Print('plots/TTfitCNN'+passf+extrstr+curptrange+cnnstr+options.era+'.root', 'root')
		c1.Print('plots/TTfitCNN'+passf+extrstr+curptrange+cnnstr+options.era+'.pdf', 'pdf')


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
		pre_TT_bmerge.SetFillColor(ROOT.kRed+1)
		pre_TT_sig.SetFillColor(ROOT.kRed)
		pre_WJetsToLNu.SetFillColor(ROOT.kGreen)
		#pre_st.SetFillColor(ROOT.kBlue)
		pre_QCD.SetFillColor(ROOT.kYellow)



		st2.Add(pre_QCD)
		st2.Add(pre_WJetsToLNu)
		st2.Add(pre_TT)
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
			st2.SetMaximum(pre_data.GetMaximum() * 1.5)
			leg1.Draw()

		prelim = TLatex()
		prelim.SetNDC()
		#prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 13 TeV, 35 fb^{-1}  Pre Fitting "+passf+"}" )
		prelim.DrawLatex( 0.1, 0.91, "#scale[0.8]{Pre Fitting "+passf+"   "+curptrange+"}" )

		ROOT.insertlogo( c2, per, 11 )
		c2.Update()
		c2.Print('plots/TTprefitCNN'+passf+extrstr+curptrange+cnnstr+options.era+'.root', 'root')
		c2.Print('plots/TTprefitCNN'+passf+extrstr+curptrange+cnnstr+options.era+'.pdf', 'pdf')
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
	postfit_ttup_file = ROOT.TFile("postfithistos/histos-CNN-TT_sig_tagup_syst"+extrstr+curptrange+cnnstr+".root")
	postfit_ttup_hist = postfit_ttup_file.Get("mtop_Mupass__TT_sig")
	postfit_ttup_hist.Add(postfit_ttup_file.Get("mtop_Elepass__TT_sig"))
	postfit_ttup = postfit_ttup_hist.Integral(*intbins)
	postfit_ttdown_file = ROOT.TFile("postfithistos/histos-CNN-TT_sig_tagdown_syst"+extrstr+curptrange+cnnstr+".root")
	postfit_ttdown_hist = postfit_ttdown_file.Get("mtop_Mupass__TT_sig")
	postfit_ttdown_hist.Add(postfit_ttdown_file.Get("mtop_Elepass__TT_sig"))
	postfit_ttdown = postfit_ttdown_hist.Integral(*intbins)

	#statunc = 0.5*(postfit_ttup-postfit_ttdown)/norms["pass"]


	print "totalMCcounts = ",totnevmc 

	print "Eff MC"
	effmc = (normspre["pass"]/(normspre["pass"]+normspre["fail"]))
	statuncmc = sqrt((effmc*(1.0-effmc))/(totnevmc))
	print effmc,"+/-",statuncmc
	print "Eff DATA"
	effdata =  (norms["pass"]/(norms["pass"]+norms["fail"]))



	print "up",postfit_ttup,"down",postfit_ttdown,"nom",norms["pass"]
	effupdata = postfit_ttup/(norms["pass"]+norms["fail"])
	effdowndata = postfit_ttdown/(norms["pass"]+norms["fail"])

	statuncdata = 0.5*(effupdata-effdowndata)



	print effdata,"+/-",statuncdata
	print "Scale factor"
	SFfinal= effdata/effmc
	#norms["pass"]/normspre["pass"]
	print effdata/effmc,SFfinal
	totstat=SFfinal*sqrt( (statuncmc/effmc)*(statuncmc/effmc) + (statuncdata/effdata)*(statuncdata/effdata) )
	print "---"
	print curptrange
	print "---"
	print SFfinal,"+/-",totstat,"+/-",totuncsys
	print "---"
	SFdict["_"+curptrange]=[SFfinal,totstat,totuncsys]
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

print SFdict
print bins
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
ptSFhistupfull.Draw('hist')
ptSFhistupstat.Draw('histsame')
ptSFhistdownstat.Draw('histsame')
ptSFhistdownfull.Draw('histsame')
ptSFhist.Draw('esame')
cleanline1.Draw('histsame')
cleanline2.Draw('histsame')





csf.RedrawAxis()
csf.Print('plots/ptSFhist'+options.era+'.root', 'root')
csf.Print('plots/ptSFhist'+options.era+'.pdf', 'pdf')


