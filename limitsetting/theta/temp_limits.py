# -*- coding: utf-8 -*-
import scipy.interpolate
import sys
import subprocess
import ROOT
#from ROOT import *
sys.path.append('../../')
import NanoAODskim_Data	
from NanoAODskim_Data import *
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True



class hfilt:
	def __init__(self,regs,coupstr):
		self.regs=regs
		self.coupstr=coupstr
	def histogram_filter(self,hname):
	    #if 'ttag' in hname: return False
	    #if 'htag' in hname: return False

	    for rr in self.regs:
		searchl = "_"+rr+"_"
		if searchl in hname:
		    	if "WptoqVLQWp" in hname:
				if not (self.coupstr in hname):
					return False

			return True
	    return False

class hrn:
	def __init__(self,coupstr,corr):
		self.coupstr=coupstr
		self.corr=corr
	def histogram_rename(self,hname):


	    hname=hname.replace(self.coupstr,"")
	    for ccorr in self.corr:
		    if ccorr != None:
			    for iyr in ["2016","2017","2018"]:
					hname=hname.replace(ccorr+iyr,ccorr)
	    #print hname
	    return hname



def makenuisanceplot(parlist,parVal):
   c1 = TCanvas('c1', 'NP', 1200, 700)
   c1.Divide(1,2)
   NPplot = ROOT.TH1F("NPplot",     "nuisanceplot",     	  	len(parVal.keys())-2, -0.5, len(parVal.keys())-1.5 )
   S95low  = TLine(-0.5,-2,len(parVal.keys())-1.5,-2)
   S95high = TLine(-0.5,2,len(parVal.keys())-1.5,2)
   zero = TLine(-0.5,0,len(parVal.keys())-1.5,0)
   zeroblank = TLine(-0.5,0,len(parVal.keys())-1.5,0)
   S68low = TLine(-0.5,-1,len(parVal.keys())-1.5,-1)
   S68high = TLine(-0.5,1,len(parVal.keys())-1.5,1)
   Pull = ROOT.TH1F("Pull",     "pullplot",     	  	len(parVal.keys())-2, -0.5, len(parVal.keys())-1.5 )
   i=0
   nuisances = []
   for par in parVal.keys():
	if par in parlist:
		continue
	nuisances.append(par)
   #nuisances = ['','pile','pdf','modm','modtb','jer','q2','lumi','st_TW_xsec','ttbar_xsec','Fit','btag','pdf','Alt','lumi','trig','jes','ttag','AK8btag']
   #procs = [['ttbar','st','qcd'],['ttbar'],['ttbar'],['qcd'],['qcd'],['ttbar'],['ttbar'],['st'],['ttbar'],['qcd'],['ttbar'],['ttbar'],['qcd'],['ttbar','st'],['ttbar'],['ttbar'],['ttbar','st'],['ttbar']]
   hrange = (100, -3.0, 3.0)
   histogram_specs = {}
   
   for nu in nuisances:

	if nu=='':
		nudev=['']

	else:
		nudev=['up','down']

	for n in nudev:		
		parameter_values = {}
   		for p in model.get_parameters(['WptoqVLQWp2000']):
			if p==nu:
				if n=='up':
   					parameter_values[p] = parVal[p][0][0]+parVal[p][0][1]
				if n=='down':
   					parameter_values[p] = parVal[p][0][0]-parVal[p][0][1]
			else:
   				parameter_values[p] = parVal[p][0][0]
   		histos = evaluate_prediction(model, parameter_values)
   		write_histograms_to_rootfile(histos, 'plots/histos-mle'+nu+n+'.root')
   for par in nuisances:
	print par 
	i+=1
	NPplot.GetXaxis().SetBinLabel(i, par)
	print parVal[par][0][0]
	print parVal[par][0][1]
	NPplot.SetBinContent(i, parVal[par][0][0])
	NPplot.SetBinError(i, parVal[par][0][1])
        Pull.GetXaxis().SetBinLabel(i, par)
        Pull.SetBinContent(i, parVal[par][0][0]/abs(parVal[par][0][1]))


	Pull.SetTitle(';Nuisance Parameter;Pull')
	Pull.SetStats(0)
	Pull.SetLineColor(1)


	NPplot.SetTitle(';Nuisance Parameter;\sigma')
	NPplot.SetStats(0)
	NPplot.SetLineColor(1)
	NPplot.SetMarkerStyle(21)

	LS=.10
	LS1 = 0.09
	NPplot.GetXaxis().SetTitleOffset(1.2)
	NPplot.GetXaxis().SetLabelSize(LS)
	NPplot.GetXaxis().SetTitleSize(LS1)

	S95low.SetLineWidth(4)
	S95high.SetLineWidth(4)
	S68low.SetLineWidth(4)
	S68high.SetLineWidth(4)
	S95low.SetLineColor(5)
	S95high.SetLineColor(5)
	S68low.SetLineColor(3)
	S68high.SetLineColor(3)
	zeroblank.SetLineColor(0)
	zero.SetLineColor(1)
	zero.SetLineStyle(2)
	zero.SetLineWidth(1)
	NPplot.GetXaxis().SetTickLength(0.0)

	NPplot.GetYaxis().SetRangeUser(-4,4)
	NPplot.GetYaxis().SetTitleOffset(0.4)

	Pull.GetXaxis().SetTickLength(0.0)

	Pull.GetYaxis().SetRangeUser(-1,1)
	Pull.GetYaxis().SetTitleOffset(0.4)


	c1.cd(1)
	gPad.SetLeftMargin(0.06)
	gPad.SetRightMargin(0.08)
	gPad.SetBottomMargin(0.31)
	NPplot.Draw()
	S95low.Draw()
	S95high.Draw()
	S68low.Draw()
	S68high.Draw()
	zero.Draw()
	NPplot.Draw("same")
        prelim = ROOT.TLatex()
        prelim.SetTextFont(42)
        prelim.SetNDC()
	prelim.DrawLatex( 0.15, 0.91, "#scale[1.0]{CMS Preliminary #sqrt{s} = 13 TeV}" )
	gPad.RedrawAxis()
	c1.cd(2)
	Pull.GetXaxis().SetTitleOffset(1.1)
	Pull.GetXaxis().SetLabelSize(LS)
	Pull.GetXaxis().SetTitleSize(LS1)
	gPad.SetLeftMargin(0.06)
	gPad.SetRightMargin(0.08)
	gPad.SetBottomMargin(0.3)
	Pull.SetFillColor(4)
	Pull.Draw('hist')
	zeroblank.Draw()
	zero.Draw()
	histogram_specs[par] = hrange
   c1.Update()

   c1.Print('plots/nuisance2000.root', 'root')
   c1.Print('plots/nuisance2000.pdf', 'pdf')

   return c1

def build_allhad_model(signaltype="tHb",year="2017",regs=[["C"]],coups=[0.5,0.5],corr=[None],sign="central",genstr=""):
    optname="optimizer_"
    optname=""

    zhc=coups[0]
    vlqc=coups[1]

    NanoF = NanoAODskim_Data(year)
    constdict = NanoF.LoadConstants
    ttbarnormcorr=constdict['ttrenorm']

    coupstr="_B"+str(vlqc[0])+"T"+str(vlqc[1])+"H"+str(zhc[0])+"Z"+str(zhc[1])+"_"
    coupstr=coupstr.replace(".","p")
    frn = hrn(coupstr,corr)
    flec = hfilt(regs,coupstr)
    files = ["NanoAODskim_"+optname+signaltype+"_ForLimits__"+year+sign+genstr+".root"]
    histogram_filter=flec.histogram_filter
    histogram_rename=frn.histogram_rename
    model = build_model_from_rootfile(files, histogram_filter,  histogram_rename, include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    #print 'WptoqVLQWp'+coupstr

    model.set_signal_processes('WptoqVLQWp*')
    #print "Observables"
    #for oo in model.get_observables():
	#print oo

    #print "Processes"
    for p in model.processes:
	print p
       	if (p=='qcd'): 
		print p,"continue"
       		#model.add_lognormal_uncertainty('nonclosure', math.log(1.12), p)
		continue
       	if (p=='ttbar'): 
		print p,ttbarnormcorr[1],ttbarnormcorr[0]
		ttclos=1.0+ttbarnormcorr[1]/ttbarnormcorr[0]
       		model.add_lognormal_uncertainty('tt', math.log(ttclos), p)
		continue
	if year=="2017":
       		model.add_lognormal_uncertainty('lumi'+year, math.log(1.025), p)
	else:
       		model.add_lognormal_uncertainty('lumi'+year, math.log(1.023), p)
       	#if p=='ttbar':
	#	print "ttbar unc"
    	#	model.add_asymmetric_lognormal_uncertainty('ttbar_xsec',math.log(1.048),math.log(1.055), p)

    return model

def limits_allhad(model,genstr=""):
   myopts = Options()
   #myopts.set('minimizer', 'strategy', 'robust')
   myopts.set('minimizer', 'minuit_tolerance_factor', '1000')
   myopts.set('minimizer', 'strategy', 'newton_vanilla')

   #if genstr!="":
   #	myopts.set('minimizer', 'minuit_tolerance_factor', '10000')
   #	myopts.set('minimizer', 'strategy', 'newton_vanilla')

   print "TEST"
   exp,obs = asymptotic_cls_limits(model,use_data=True,options = myopts,n=5)



   Nbin=0
   for obsbl in model.get_observables():
   	Nbin+=model.get_data_histogram(obsbl).get_nbins()
   myopts1 = Options()
   myopts1.set('minimizer', 'minuit_tolerance_factor', '100')
   #myopts1.set('minimizer', 'strategy', 'robust')
   myopts1.set('minimizer', 'strategy', 'newton_vanilla')

   #parVals = mle(model, input = 'data', n=1, with_error = True,chi2=True,options=myopts1)
   #print parVals
   #print discovery(model,spid="WptoqVLQWp1500")
   #parVals = mle(model, input = 'data', n=1, with_error = True, signal_process_groups = {'': []},chi2=True,options=myopts1)
   #parVals = mle(model, input = 'toys:0', n=1, with_error = True, signal_process_groups = {'': []},chi2=True,options=myopts1)

   chi2=-1
   #for pp in parVals:
	#for pp1 in parVals[pp]:
	#	if pp1=="__chi2":
	#		chi2=parVals[pp][pp1][0]/Nbin
	#		print pp1,Nbin, parVals[pp][pp1][0]/Nbin
	#	print pp,pp1,parVals[pp][pp1][0]
   return [exp,obs],chi2

regs=[['C']]
#regs=[['C'],['K'],['H'],['C','K','H']]
#regs=[['F'],['K'],['H']]
#regs=[['H']]

#SRs=[["tHb2016"],["tHb2017"],["tHb2018"],["tZb2016"],["tZb2017"],["tZb2018"],["tHb2016","tHb2017","tHb2018","tZb2016","tZb2017","tZb2018"]]
#SRs=[["tHb2016"],["tHb2017"],["tHb2018"],["tHb2016","tHb2017","tHb2018"]]
#SRs=[["tZb2016"],["tZb2017"],["tZb2018"],["tZb2016","tZb2017","tZb2018"]]
SRs=[["tHb2016","tHb2017","tHb2018","tZb2016","tZb2017","tZb2018"]]
#SRs=[["tHb2016","tHb2017","tHb2018"],["tZb2016","tZb2017","tZb2018"]]

#SRs=[["tHb2017","tZb2017"]]

bttp=[]
zh=[]
reso=10
dogcvlq=False
dogczh=False
genstr=""
if dogcvlq:
	genstr="genvlq"
	for it in xrange(reso+1):
		for jt in xrange(reso+1):
			if (it+jt<=reso+1):
				bttp.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
else:
	bttp=[[0.5,0.5]]
if dogczh:
	genstr="genzc"
	for it in xrange(reso+1):
		for jt in xrange(reso+1):
			if (it+jt<=reso+1):
				zh.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
else:
	zh=[[0.5,0.5]]



#SRs=[["tHb2017","tZb2017"]]
#SRs=[["tHb2016","tHb2017","tHb2018","tZb2016","tZb2017","tZb2018"]]
#SRs=[["tHb2016","tHb2017","tHb2018","tZb2016","tZb2017","tZb2018"]]

rootstr="Bench_FullRun2LimTZBplusTHBCOMP"
rootstr="ckhcomp"
tc = ROOT.TCanvas("tc","tc",700,600)
tc.Draw()
tcnorm = ROOT.TCanvas("tcnorm","tcnorm",700,600)
tcnorm.Draw()
grarray=[]
grarraylow=[]
grarrayhigh=[]
grnormarray=[]
grnormarraylow=[]
grnormarrayhigh=[]
mg=ROOT.TMultiGraph()
mgnorm=ROOT.TMultiGraph()

leg = ROOT.TLegend(0.20, 0.55, 0.54, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)
#corrs=[[None],['jms'],['jmr'],['jes'],['jer'],['btag'],['wtag'],['htag'],['jms','jmr','jes','jer','btag','wtag','htag']]
corrs=[[None]]
#signs=["central","low","high"]
signs=["central"]
allchis=[]

print zh
print bttp
#zh = [[0.5, 0.5]]
#bttp = [[0.0001, 0.2]]
for sign in signs:
	for corr in corrs:
		for vlqc in bttp:
			for zhc in zh:
				for sr in SRs:
					for rr in regs:

						srstr=""
						for srr1 in sr:
							for srr2 in srr1:
								srstr+=str(srr2)
						#corrstr="None"
						if len(corr)==1:
								corrstr=str(corr[0])
						else:
								corrstr="All"
		    				coupstr="_B"+str(vlqc[0])+"T"+str(vlqc[1])+"H"+str(zhc[0])+"Z"+str(zhc[1])+"_"
		    				coupstr=coupstr.replace(".","p")
						txtname='exp'+rootstr+srstr+coupstr+corrstr+sign+'.txt'
						txtnameobs='obs'+rootstr+srstr+coupstr+corrstr+sign+'.txt'

						if os.path.exists(txtname) and genstr!="":
							print "alreadyran"
							continue 
    						#subprocess.call( ["rm -rf analysis/*.cfg"], shell=True )
						print rr,sr,zhc,vlqc,corr
						models={}
						for sr1 in sr:
							anat=str(sr1[:3])
							yr=str(sr1[3:])
							print anat,yr
							models[sr1]=build_allhad_model(anat,yr,rr,[zhc,vlqc],corr,sign,genstr)

						nmodel = 0
						for mmm in models:
							print mmm
							if nmodel==0:
								model=models[mmm]
							else:
								model.combine(models[mmm])
							nmodel += 1
						#for p in model.distribution.get_parameters():
						#    d = model.distribution.get_distribution(p)
						#    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
						#	model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
						#model_summary(model, True, True, True)
						print "zhc,vlqc",zhc,vlqc
						lim=limits_allhad(model,genstr)
						#try:
						#	lim=limits_allhad(model,genstr)
						#except:
						#	print "FAIL"
						#	continue 
						print lim[0]
				   		lim[0][0].write_txt(txtname)
						print "lim[0][1]",lim[0][1]
						if lim[0][1]!=None:
				   			lim[0][1].write_txt(txtnameobs)
						del models

						continue

						chi2=lim[1]
						print "chi2",rr,chi2
						allchis.append([sr+rr,chi2])
						#try:
						#	lim=limits_allhad(model)
						#	print lim[0]
				   		#	lim[0].write_txt(txtname)
						#except:

						#	print "FAIL!"
						#	continue
						yarr = array.array('d',lim[0][0].y)
						yarrnorm = array.array('d',lim[0][0].y)
						lowerr,higherr = lim[0][0].bands
						lowerrnorm,higherrnorm = lim[0][0].bands
						#print lowerr
						#print higherr
						yarrerrlow = array.array('d',lowerr[0])
						yarrerrhigh = array.array('d',lowerr[1])
						#print yarrerrlow
						#print yarrerrhigh

						yarrerrlownorm = array.array('d',lowerrnorm[0])
						yarrerrhighnorm = array.array('d',lowerrnorm[1])


						yarrerrnorm = array.array('d',lim[0][0].y)
						xarr = array.array('d',lim[0][0].x)
						if len(grarray)==0:
							yarrinit=copy.deepcopy(yarr)
							xarrinit=copy.deepcopy(xarr)
						for yy in xrange(len(yarr)):
							yarrnorm[yy]/=yarrinit[yy]
							yarrerrlownorm[yy]/=yarrinit[yy]
							yarrerrhighnorm[yy]/=yarrinit[yy]
						print xarr,yarr
						grarray.append(ROOT.TGraph(len(xarr),xarr,yarr))
						grarraylow.append(ROOT.TGraph(len(xarr),xarr,yarrerrlow))
						grarrayhigh.append(ROOT.TGraph(len(xarr),xarr,yarrerrhigh))
						tc.cd()
						colo= (len(grarray))%9+1
						grarray[-1].SetMarkerColor(colo)
						grarray[-1].SetLineWidth(2)
						grarray[-1].SetLineColor(colo)
						grarray[-1].SetMarkerStyle(5)

						grarraylow[-1].SetLineStyle(2)
						grarraylow[-1].SetLineWidth(2)
						grarraylow[-1].SetLineColor(colo)
						#grarraylow[-1].SetMarkerStyle(5)

						grarrayhigh[-1].SetLineStyle(2)
						grarrayhigh[-1].SetLineWidth(2)
						grarrayhigh[-1].SetLineColor(colo)
						#grarrayhigh[-1].SetMarkerStyle(5)

						grnormarray.append(ROOT.TGraph(len(xarr),xarr,yarrnorm))
						grnormarraylow.append(ROOT.TGraph(len(xarr),xarr,yarrerrlownorm))
						grnormarrayhigh.append(ROOT.TGraph(len(xarr),xarr,yarrerrhighnorm))

						tcnorm.cd()
						grnormarray[-1].SetMarkerColor(colo)
						grnormarray[-1].SetLineColor(colo)
						grnormarray[-1].SetLineWidth(2)
						grnormarray[-1].SetMarkerStyle(5)
						#leg.AddEntry( grarray[-1], str(rr)+" - "+str(sr), 'PL')
						#leg.AddEntry( grarray[-1], corrstr, 'PL')
						leg.AddEntry( grarray[-1], str(rr), 'PL')
						mg.Add(grarray[-1])
						mg.Add(grarraylow[-1])
						mg.Add(grarrayhigh[-1])
						mgnorm.Add(grnormarray[-1])
						mgnorm.Add(grnormarraylow[-1])
						mgnorm.Add(grnormarrayhigh[-1])
			
						tc.Update()
						#print lim[0].split("\n")[1:]

print "Done"

tc.cd()
mg.Draw("ALP")
mg.GetYaxis().SetRangeUser(min(yarr)*0.1,max(yarr)*100.0)
mg.GetXaxis().SetRangeUser(min(xarr)*0.9,max(xarr)*1.5)
tc.SetLogy()
tc.Update()
leg.Draw()
tc.Print("limcomp"+rootstr+".root","root")
tc.Print("../../plots/limcomp"+rootstr+".pdf","pdf")



tcnorm.cd()
mgnorm.Draw("ALP")
mgnorm.GetYaxis().SetRangeUser(min(yarrnorm)*0.7,max(yarrnorm)*40.0)
mgnorm.GetXaxis().SetRangeUser(min(xarr)*0.9,max(xarr)*1.5)
tcnorm.SetLogy()
tcnorm.Update()
leg.Draw()
tcnorm.Print("limcompnorm"+rootstr+".root","root")
tc.Print("../../plots/limcompnorm"+rootstr+".pdf","pdf")

print allchis

