import NanoAODskim_Functions	
from NanoAODskim_Functions import *

from optparse import OptionParser
import subprocess,os,sys
ROOT.gROOT.LoadMacro("insertlogo.C+")
parser = OptionParser()
parser.add_option('--dogcvlq', metavar='F', action='store_true',
		  default=False,
		  dest='dogcvlq',
		  help='dogcvlq')

parser.add_option('--dogczh', metavar='F', action='store_true',
		  default=False,
		  dest='dogczh',
		  help='dogczh')

parser.add_option('--obs', metavar='F', action='store_true',
		  default=False,
		  dest='obs',
		  help='obs')
(options, args) = parser.parse_args()

regiontoname=	{
		"C":"C, Signal",
		"K":"K, Loose t",
		"H":"H, Loose V",
		"F":"F, Validation",
		"FT":"ttbar measurement",
		}

genstr=""
if options.dogczh:
	genstr+="genzc"
if options.dogcvlq:
	genstr+="genvlq"


alim=[1.5,3.9]

bttp=[]
zh=[]																								
reso=10
if options.dogcvlq:
				for it in xrange(reso+1):
					for jt in xrange(reso+1):
						if (it+jt<=reso+1):
							bttp.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
else:
				bttp=[[0.5,0.5]]
if options.dogczh:
				for it in xrange(reso+1):
					for jt in xrange(reso+1):
						if (it+jt<=reso+1):
							zh.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
else:
				zh=[[0.5,0.5]]


lim2d=TH2F("lim2d"+genstr,	"lim2d"+genstr,		reso+1, -0.05,1.05,reso+1, -0.05,1.05 )
minval=1.0

xyval=[]
tystr="exp"
pltxt="Expected"
if options.obs:
	tystr="obs"
	pltxt="Observed"
for vlqc in bttp:
	for zhc in zh:
		print float(vlqc[0])+float(vlqc[1])
		print float(zhc[0])+float(zhc[1])
		if float(vlqc[0])+float(vlqc[1])>1.05:
			continue
		if float(zhc[0])+float(zhc[1])>1.05:
			continue
		xyval.append([])
		if options.dogczh:
			xyval[-1].append([zhc[0],zhc[1]])
		if options.dogcvlq:
			xyval[-1].append([vlqc[0],vlqc[1]])
		curcomb="_B"+str(vlqc[0])+"T"+str(vlqc[1])+"H"+str(zhc[0])+"Z"+str(zhc[1])+"_"
		curcomb=curcomb.replace(".","p")
		curtxt=tystr+"ckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018"+curcomb+"Nonecentral.txt"

		
		if not os.path.exists("limitsetting/theta/"+curtxt):
			
			print "notxt","limitsetting/theta/"+curtxt
			xyval[-1].append(minval)
			continue 
		sigstrpre=999
		masspre=999	
		interf=False
		with open("limitsetting/theta/"+curtxt,'r') as txtf:     
     			for line in txtf.readlines()[1:]:
        		 	linepl = line.split()
				mass = float(linepl[0])
				sigstr = float(linepl[1])
				print mass,sigstr
				if ((sigstr>1) and (sigstrpre<1)):
					m=(sigstr-sigstrpre)/(mass-masspre)
					ll=(1.0-sigstrpre)/m
					interp =masspre+ll 
					print "inter!",interp
					xyval[-1].append(interp/1000.)
					interf=True
					break
				sigstrpre=sigstr
				masspre=mass
			if not interf:
				xyval[-1].append(minval)
print xyval
for xyv in xyval:
	lim2d.Fill(xyv[0][0],xyv[0][1],xyv[1])
canv= TCanvas("canv","canv",1000,900)
lim2d.GetZaxis().SetRangeUser(alim[0],alim[1])
if options.dogcvlq:
	lim2d.SetTitle(";F(VLQ=B);F(VLQ=T);W' exclusion mass [TeV]")

if options.dogczh:
	lim2d.SetTitle(";BR(VLQ->Hq);BR(VLQ->Zq);W' exclusion mass [TeV]")

LS=0.04
lim2d.GetYaxis().SetLabelSize(LS)
lim2d.GetYaxis().SetTitleSize(LS)
lim2d.GetZaxis().SetLabelSize(LS)
lim2d.GetZaxis().SetTitleSize(LS)
lim2d.GetZaxis().SetTitleOffset(1.4)
lim2d.GetXaxis().SetLabelSize(LS)
lim2d.GetXaxis().SetTitleSize(LS)
canv.SetLeftMargin(0.13)
canv.SetRightMargin(0.17)
canv.SetTopMargin(0.1)
canv.SetBottomMargin(0.1)
lim2d.SetContour(200)
lim2d.SetStats(0)

TPT = ROOT.TPaveText(.67, .83, .77, .88,"NDC")
TPT.AddText(pltxt)   
TPT.SetFillColor(0)
TPT.SetBorderSize(0)
TPT.SetTextAlign(12)

TPT1 = ROOT.TPaveText(.62, .78, .82, .83,"NDC")
TPT1.AddText("Medium VLQ mass")   
TPT1.SetFillColor(0)
TPT1.SetBorderSize(0)
TPT1.SetTextAlign(12)

lim2d.Draw("colz")
TPT.Draw()
TPT1.Draw()
ROOT.insertlogo( canv, 5, 10)
canv.RedrawAxis()
canv.Print('plots/lim2d'+tystr+genstr+'.root', 'root')
canv.Print('plots/lim2d'+tystr+genstr+'.pdf', 'pdf')
canv.Print('plots/lim2d'+tystr+genstr+'.png', 'png')
		

interpreso=100
lim2dinterp=TH2F("lim2dinterp"+genstr,	"lim2dinterp"+genstr,		interpreso+1, 0.0,1.0,interpreso+1, 0.0,1.0 )
for xbin in xrange(lim2dinterp.GetNbinsX()+1):
	for ybin in xrange(lim2dinterp.GetNbinsY()+1):
		limx=lim2dinterp.GetXaxis().GetBinCenter(xbin)
		limy=lim2dinterp.GetYaxis().GetBinCenter(ybin)
		binx=lim2d.GetXaxis().FindBin(limx)
		biny=lim2d.GetYaxis().FindBin(limy)
		curbinc=lim2d.GetBinContent(binx,biny)
		#print limx,limy
		#print curbinc
		if (limx+limy)>1 or curbinc<1.0:
			continue

		lim2dinterp.SetBinContent(xbin,ybin,lim2d.Interpolate(limx,limy))
lim2dinterp.GetZaxis().SetRangeUser(alim[0],alim[1])
if options.dogcvlq:
	lim2dinterp.SetTitle(";B;T;W' exclusion mass [TeV]")

if options.dogczh:
	lim2dinterp.SetTitle(";BR(VLQ->Hq);BR(VLQ->Zq);W' exclusion mass [TeV]")

LS=0.04
lim2dinterp.GetYaxis().SetLabelSize(LS)
lim2dinterp.GetYaxis().SetTitleSize(LS)
lim2dinterp.GetZaxis().SetLabelSize(LS)
lim2dinterp.GetZaxis().SetTitleSize(LS)
lim2dinterp.GetZaxis().SetTitleOffset(1.4)
lim2dinterp.GetXaxis().SetLabelSize(LS)
lim2dinterp.GetXaxis().SetTitleSize(LS)

lim2dinterp.SetContour(200)
lim2dinterp.SetStats(0)
lim2dinterp.Draw("colz")
canv.Print('plots/lim2dinterp'+tystr+genstr+'.root', 'root')
canv.Print('plots/lim2dinterp'+tystr+genstr+'.pdf', 'pdf')
canv.Print('plots/lim2dinterp'+tystr+genstr+'.png', 'png')
		




