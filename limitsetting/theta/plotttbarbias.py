#! /usr/bin/env python
import os
import copy
from math import *

from optparse import OptionParser

import ROOT
import array
import glob
import sys
from array import *
from ROOT import *
import numpy as np



gROOT.LoadMacro("insertlogo.C+")
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

x=[]
y=[]
yup=[]
ydown=[]
normy=1.0
for iter in xrange(21):
	xval=0.80+float(iter)*0.02
	striter=str(xval).replace(".","p")
	print striter
	if striter=="1p0":
		striter=""

	File = ROOT.TFile("plots/topSF_2018"+striter+".root")
	sfplot= File.Get("SF")
	sfplot.Fit("pol0","Q")
	fitter = TVirtualFitter.GetFitter()
	yval=fitter.GetParameter(0)

	sfplotup= File.Get("SFup")
	sfplotup.Fit("pol0","Q")
	fitter = TVirtualFitter.GetFitter()
	yvalup=fitter.GetParameter(0)

	sfplotdown= File.Get("SFdown")
	sfplotdown.Fit("pol0","Q")
	fitter = TVirtualFitter.GetFitter()
	yvaldown=fitter.GetParameter(0)

	print xval,yval,yvalup,yvaldown
	if striter=="":
		normy=yval
	x.append(xval)
	y.append(yval)
	yup.append(yvalup)
	ydown.append(yvaldown)

for iy in xrange(len(y)):
	y[iy]/=normy
	yup[iy]/=normy
	ydown[iy]/=normy
	print y[iy],normy

xarr= array("d",x)
yarr= array("d",y)

yarrup= array("d",yup)

yarrdown= array("d",ydown)

gr = TGraph(len(xarr),xarr,yarr)
grup = TGraph(len(xarr),xarr,yarrup)
grdown = TGraph(len(xarr),xarr,yarrdown)

mg =TMultiGraph()
c = TCanvas('c', 'c', 800, 800)
grup.SetLineColor(3)
grdown.SetLineColor(3)
mg.Add(gr)
mg.Add(grup)
mg.Add(grdown)

mg.Draw("AC")
c.Print('plots/biasgraph.pdf', 'pdf')
c.Print('plots/biasgraph.root', 'root')

gr.Fit("pol1")





