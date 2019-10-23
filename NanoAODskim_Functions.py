#from DataFormats.FWLite import Events, Handle
from array import array
import subprocess, math, copy, random, time, logging, sys, os, glob, numpy, itertools
import NanoAODskim_Data	
from NanoAODskim_Data import *
#random.seed(8574931)
from math import sqrt
import ROOT 

sys.path.insert(0,os.getcwd()+'/tardir')
sys.path.insert(0,os.getcwd()+'/CMSSW_10_2_9/src')
from ROOT import TLorentzVector,TH1F,TH2F,TTree,TFile,gROOT,TCanvas,TGraph,TMultiGraph,TLegend,gROOT,TTreeReader,TLatex

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetSmearer import jetSmearer

class objecttype:
	def __init__(self,name):
		self.pt = None
		self.eta = None
		self.phi = None
		self.mass = None
		self.p4 = TLorentzVector()

		if name=="CustomAK8Puppi":	
			self.iMDPho= None
			self.iMDWW= None
			self.iMDtop= None
			self.iW= None
			self.iMDW= None
			self.iMDtop= None
			self.msoftdrop= None
			self.tau1= None
			self.tau2= None
			self.tau21= None
			self.btagHbb= None
			self.rawFactor= None
			self.area= None
		if name=="Jet":	
			self.btagDeepFlavB= None
			self.rawFactor= None
			self.area= None
		if name=="GenPart":
			self.pdgId= None
			self.statusFlags= None	
		if name=="Muon":	
			self.tightId= None
		if name=="Electron":	
			self.mvaFall17V2Iso_WP90= None
			self.mvaFall17V2noIso_WP90= None

	def setp4(self):
		self.p4.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)
class invobj:
	def __init__(self,ovec):
		invcand={}

		ilab=0
		for ll in ovec:
			if ilab==0:
				self.p4 = copy.deepcopy(ll.p4)
			else:
				self.p4 += ll.p4
			ilab+=1


		self.pt = self.p4.Perp()
		self.eta = self.p4.Eta()
		self.aeta = abs(self.p4.Eta())
		self.phi = self.p4.Phi()
		self.mass = self.p4.M()
		self.p = self.p4.P()
		if ilab>1:
			self.dR = ovec[0].p4.DeltaR(ovec[1].p4)
			self.deltapt = ovec[0].p4.Perp() - ovec[1].p4.Perp()
			self.ht = ovec[0].p4.Perp() + ovec[1].p4.Perp()
			self.deta = ovec[0].p4.Eta() - ovec[1].p4.Eta()
			self.dphi = ovec[0].p4.DeltaPhi(ovec[1].p4)
			self.dy = abs(ovec[0].p4.Rapidity()-ovec[1].p4.Rapidity())
			self.dyhighm = -1.0
			if self.mass>2000:
				self.dyhighm = abs(ovec[0].p4.Rapidity()-ovec[1].p4.Rapidity())
		self.njets = 0
		self.htval=0.0
		self.njetsrem=0
		self.htvalrem=0.0
		self.idval= 0

class NanoAODskim_Functions:
	def __init__(self,anatype="Pho",era="2017",versionstring="v8",settype="TT",condor=False):
		di=""
		if condor:
			di="tardir/"
		self.isdata=False
		if settype=="JetHT":
			self.isdata=True
		#print settype,self.isdata
		self.anatype=anatype
		self.truncval = 300
		self.era = era
		self.versionstring = versionstring

		self.nanotype = "NanoSlimNtuples"
		self.trigstopass=[]
        	self.rnd = ROOT.TRandom3(12345)

		
		NanoAODskimData= NanoAODskim_Data(era)
		self.LoadConstants=NanoAODskimData.LoadConstants
		self.allsignamesHT=NanoAODskimData.allsignamesHT
		self.allsignamesZT=NanoAODskimData.allsignamesZT

		self.btagdict=NanoAODskimData.btagdict
		#for ll in self.LoadConstants['dataconst']:
		#	print ll,self.LoadConstants['dataconst'][ll])
		if not self.isdata:
			self.jmeCorrections = createJMECorrector((not self.isdata), self.era, "B", "Total", True, "AK8PFPuppi", False)
			smearmc = self.jmeCorrections().jetSmearer
			self.params_sf_and_uncertainty = ROOT.PyJetParametersWrapper()
			self.jer = ROOT.PyJetResolutionWrapper(os.path.join(smearmc.jerInputFilePath, smearmc.jerInputFileName))
			self.jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(smearmc.jerInputFilePath, smearmc.jerUncertaintyInputFileName))
	       		self.params_resolution = ROOT.PyJetParametersWrapper()

			self.jmeCorrectionsak4 = createJMECorrector((not self.isdata), self.era, "B", "Total", True, "AK4PFchs", True)
			smearmcak4 = self.jmeCorrectionsak4().jetSmearer
			self.params_sf_and_uncertaintyak4 = ROOT.PyJetParametersWrapper()
			self.jerak4 = ROOT.PyJetResolutionWrapper(os.path.join(smearmcak4.jerInputFilePath, smearmcak4.jerInputFileName))
			self.jerSF_and_Uncertaintyak4 = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(smearmcak4.jerInputFilePath, smearmcak4.jerUncertaintyInputFileName))
	       		self.params_resolutionak4 = ROOT.PyJetParametersWrapper()
			#self.jetSmearer = self.jmeCorrections.jetSmearer
			pufile=TFile(di+"NanoAODskim_PUMaker__"+self.era+".root","open")

			self.puhists =	{
					"sf":copy.deepcopy(pufile.Get("purwnom")),
					"down":copy.deepcopy(pufile.Get("purwdown")),
					"up":copy.deepcopy(pufile.Get("purwup"))
					}
	
			self.trighist2ds = []
			self.trighists=[]
			self.trigprobs=[]
			if self.era=="2016":
				trigfiles=[]
				trigfiles.append(TFile(di+"NanoAODskim_TrigMaker__2016__Run2016BtoG.root","open"))
				trigfiles.append(TFile(di+"NanoAODskim_TrigMaker__2016__Run2016H.root","open"))
				self.trighist2ds.append(copy.deepcopy(trigfiles[0].Get("trighisthtmass")))
				self.trighists.append(copy.deepcopy(trigfiles[0].Get("trighistht")))
				self.trigprobs.append(8.7/35.9)
				self.trighist2ds.append(copy.deepcopy(trigfiles[1].Get("trighisthtmass")))
				self.trighists.append(copy.deepcopy(trigfiles[1].Get("trighistht")))	
				self.trigprobs.append(0.0)

			if self.era=="2017":
				
				trigfiles=[]
				trigfiles.append(TFile(di+"NanoAODskim_TrigMaker__2017__Run2017CtoF.root","open"))
				trigfiles.append(TFile(di+"NanoAODskim_TrigMaker__2017__Run2017B.root","open"))
				self.trighist2ds.append(copy.deepcopy(trigfiles[0].Get("trighisthtmass")))
				self.trighists.append(copy.deepcopy(trigfiles[0].Get("trighistht")))	
				self.trigprobs.append(3.93/41.8)
				self.trighist2ds.append(copy.deepcopy(trigfiles[1].Get("trighisthtmass")))
				self.trighists.append(copy.deepcopy(trigfiles[1].Get("trighistht")))		
				self.trigprobs.append(0.0)

			if self.era=="2018":
				trigfiles=[]
				trigfiles.append(TFile(di+"NanoAODskim_TrigMaker__2018__Run2018AtoD.root","open"))
				self.trighist2ds.append(copy.deepcopy(trigfiles[0].Get("trighisthtmass")))
				self.trighists.append(copy.deepcopy(trigfiles[0].Get("trighistht")))		
				self.trigprobs.append(0.0)
			
		if anatype=="Pho":
			self.labels = ["W","P","PW"]
			self.ak8labels = ["W","P"]
			self.ak4labels = []
			self.candl = "P"
			self.probl = "W"
			cutranges = 	{
					'iMDW__W':{'L':[0.2,0.5],'M':[0.5,0.8],'M1':[0.8,0.9],'T':[0.9,1.0]},
					'msoftdrop__W':{'L':[65.0,105.0],'M':[65.0,105.0],'M1':[65.0,105.0],'T':[65.0,105.0]},
					'iMDPho__P':{'L':[0.0,0.5],'M':[0.5,0.75],'M1':[0.75,0.85],'T':[0.85,1.0]},
					'msoftdrop__P':{'L':[105.0,float("inf")],'M':[105.0,float("inf")],'M1':[105.0,float("inf")],'T':[105.0,float("inf")]},
					'ptAK8':{'L':500.0,'M':500.0,'M1':500.0,'T':500.0},
					}
			self.LoadCuts =  	{
						'A':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDPho__P':cutranges['iMDPho__P']['L'],
								'msoftdrop__P':cutranges['msoftdrop__P']['L'],
								},
						'B':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDPho__P':cutranges['iMDPho__P']['T'],
								'msoftdrop__P':cutranges['msoftdrop__P']['T'],
								},
						'C':	 	{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDPho__P':cutranges['iMDPho__P']['T'],
								'msoftdrop__P':cutranges['msoftdrop__P']['T'],
								},
						'D':		{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDPho__P':cutranges['iMDPho__P']['L'],
								'msoftdrop__P':cutranges['msoftdrop__P']['L'],
								},

						'E':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDPho__P':cutranges['iMDPho__P']['M'],
								'msoftdrop__P':cutranges['msoftdrop__P']['M'],
								},
						'F':	 	{	
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDPho__P':cutranges['iMDPho__P']['M'],
								'msoftdrop__P':cutranges['msoftdrop__P']['M'],
								},
						'G':		{	
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDPho__P':cutranges['iMDPho__P']['L'],
								'msoftdrop__P':cutranges['msoftdrop__P']['L'],
								},

						'H':	 	{	
								'iMDW__W':cutranges['iMDW__W']['M1'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M1'],
								'iMDPho__P':cutranges['iMDPho__P']['T'],
								'msoftdrop__P':cutranges['msoftdrop__P']['T'],
								},
						'I':		{	
								'iMDW__W':cutranges['iMDW__W']['M1'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M1'],
								'iMDPho__P':cutranges['iMDPho__P']['L'],
								'msoftdrop__P':cutranges['msoftdrop__P']['L'],
								},


						'J':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDPho__P':cutranges['iMDPho__P']['M1'],
								'msoftdrop__P':cutranges['msoftdrop__P']['M1'],
								},
						'K':	 	{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDPho__P':cutranges['iMDPho__P']['M1'],
								'msoftdrop__P':cutranges['msoftdrop__P']['M1'],
								},
						'L':		{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDPho__P':cutranges['iMDPho__P']['L'],
								'msoftdrop__P':cutranges['msoftdrop__P']['L'],
								},



				
				
						'NM1PiMDPho':	 {	
								'iMDW__W':[0.9,1.0],
								'msoftdrop__W':[65.0,105.0],
								'iMDPho__P':[0.0,1.0],
								'msoftdrop__P':[105.0,float("inf")],
								},
						'NM1Pmsoftdrop':{	
								'iMDW__W':[0.9,1.0],
								'msoftdrop__W':[65.0,105.0],
								'iMDPho__P':[0.85,1.0],
								'msoftdrop__P':[0.0,float("inf")],
								},
						'NM1WiW':	 {	
								'iMDW__W':[0.0,1.0],
								'msoftdrop__W':[65.0,105.0],
								'iMDPho__P':[0.85,1.0],
								'msoftdrop__P':[105.0,float("inf")],
								},

						'NM1Wmsoftdrop':{	
								'iMDW__W':[0.9,1.0],
								'msoftdrop__W':[0.0,float("inf")],
								'iMDPho__P':[0.85,1.0],
								'msoftdrop__P':[105.0,float("inf")],
								},

						'All':	  	{	
								'iMDW__W':[0.0,1.0],
								'msoftdrop__W':[0.0,float("inf")],
								'iMDPho__P':[0.0,1.0],
								'msoftdrop__P':[0.0,float("inf")],
								},

						}

		elif anatype=="WW":
			self.labels = ["W","F","FW"]
			self.ak8labels = ["W","F"]
			self.ak4labels = []
			self.candl = "F"
			self.probl = "W"
			cutranges = 	{
					'iMDW__W':{'L':[0.2,0.4],'M':[0.4,0.6],'M1':[0.6,0.9],'T':[0.9,1.0]},
					'msoftdrop__W':{'L':[65.0,105.0],'M':[65.0,105.0],'M1':[65.0,105.0],'T':[65.0,105.0]},
					'iMDWW__F':{'L':[0.0,0.3],'M':[0.3,0.5],'M1':[0.5,0.8],'T':[0.8,1.0]},
					'msoftdrop__F':{'L':[105.0,float("inf")],'M':[105.0,float("inf")],'M1':[105.0,float("inf")],'T':[105.0,float("inf")]},
					'ptAK8':{'L':500.0,'M':500.0,'M1':500.0,'T':500.0},
					}

			self.LoadCuts =  	{
						'A':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDWW__F':cutranges['iMDWW__F']['L'],
								'msoftdrop__F':cutranges['msoftdrop__F']['L'],
								},
						'B':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDWW__F':cutranges['iMDWW__F']['T'],
								'msoftdrop__F':cutranges['msoftdrop__F']['T'],
								},
						'C':	 	{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDWW__F':cutranges['iMDWW__F']['T'],
								'msoftdrop__F':cutranges['msoftdrop__F']['T'],
								},
						'D':		{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDWW__F':cutranges['iMDWW__F']['L'],
								'msoftdrop__F':cutranges['msoftdrop__F']['L'],
								},

						'E':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDWW__F':cutranges['iMDWW__F']['M'],
								'msoftdrop__F':cutranges['msoftdrop__F']['M'],
								},
						'F':	 	{	
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDWW__F':cutranges['iMDWW__F']['M'],
								'msoftdrop__F':cutranges['msoftdrop__F']['M'],
								},
						'G':		{	
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDWW__F':cutranges['iMDWW__F']['L'],
								'msoftdrop__F':cutranges['msoftdrop__F']['L'],
								},

						'H':	 	{	
								'iMDW__W':cutranges['iMDW__W']['M1'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M1'],
								'iMDWW__F':cutranges['iMDWW__F']['T'],
								'msoftdrop__F':cutranges['msoftdrop__F']['T'],
								},
						'I':		{	
								'iMDW__W':cutranges['iMDW__W']['M1'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M1'],
								'iMDWW__F':cutranges['iMDWW__F']['L'],
								'msoftdrop__F':cutranges['msoftdrop__F']['L'],
								},


						'J':		{	
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDWW__F':cutranges['iMDWW__F']['M1'],
								'msoftdrop__F':cutranges['msoftdrop__F']['M1'],
								},
						'K':	 	{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDWW__F':cutranges['iMDWW__F']['M1'],
								'msoftdrop__F':cutranges['msoftdrop__F']['M1'],
								},
						'L':		{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDWW__F':cutranges['iMDWW__F']['L'],
								'msoftdrop__F':cutranges['msoftdrop__F']['L'],
								},





						'NM1FiMDWW':	  	{	
								'iMDW__W':[0.9,1.0],
								'msoftdrop__W':[65.0,105.0],
								'iMDWW__F':[0.0,1.0],
								'msoftdrop__F':[105.0,float("inf")],
								},
						'NM1Fmsoftdrop':	  	{	
								'iMDW__W':[0.9,1.0],
								'msoftdrop__W':[65.0,105.0],
								'iMDWW__F':[0.8,1.0],
								'msoftdrop__F':[0.0,float("inf")],
								},
						'NM1WiW':	 	{	
								'iMDW__W':[0.0,1.0],
								'msoftdrop__W':[65.0,105.0],
								'iMDWW__F':[0.8,1.0],
								'msoftdrop__F':[105.0,float("inf")],
								},
						'NM1Wmsoftdrop':	 	{	
								'iMDW__W':[0.9,1.0],
								'msoftdrop__W':[0.0,float("inf")],
								'iMDWW__F':[0.8,1.0],
								'msoftdrop__F':[105.0,float("inf")],
								},


						'NM2FmsoftdropiMDWW':	  	{	
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDWW__F':[0.0,1.0],
								'msoftdrop__F':[0.0,float("inf")],
								},
						
						'NM2WmsoftdropiMDW':	 	{	
								'iMDW__W':[0.0,1.0],
								'msoftdrop__W':[0.0,float("inf")],
								'iMDWW__F':cutranges['iMDWW__F']['T'],
								'msoftdrop__F':cutranges['msoftdrop__F']['T'],
								},


						'All':	  	{	
								'iMDW__W':[0.0,1.0],
								'msoftdrop__W':[0.0,float("inf")],
								'iMDWW__F':[0.0,1.0],
								'msoftdrop__F':[0.0,float("inf")],
								},

						}



		


		

		elif anatype=="tHb":
			self.labels = ["H","T","B","THB","TH","BH","BT"]
			self.ak8labels = ["H","T"]
			self.ak4labels = ["B"]
			self.candl = "T"
			self.probl = "H"

			cutranges = 	{
					'btagHbb__H':{'L':[-1.0,0.0],'M':[0.0,0.3],'M1':[0.3,0.6],'T':[0.6,1.0],'F':[-1.0,1.0]},
					'msoftdrop__H':{'L':[10.0,30.0],'M':[105.0,140.0],'M1':[105.0,140.0],'T':[105.0,140.0],'F':[130.0,250.0]},
					'iMDtop__H':{'L':[0.0,0.95],'M':[0.0,0.95],'M1':[0.0,0.95],'T':[0.0,0.95],'F':[0.9,1.0]},
					'iMDtop__T':{'L':[0.0,0.6],'M':[0.6,0.9],'M1':[0.6,0.9],'T':[0.9,1.0]},
					'msoftdrop__T':{'L':[30.0,65.0],'M':[140.0,220.0],'M1':[140.0,220.0],'T':[140.0,220.0]},
					'btagDeepFlavB__B':{'L':[-1.0,0.0521],'M':[-1.0,0.0521],'M1':[0.0521,1.0],'T':[0.0521,1.0],'F':[-1.0,0.0521]},
					'pt__B':{'L':200.0,'M':200.0,'M1':200.0,'T':200.0,'F':50.0},
					'ptAK8':{'L':450.0,'M':450.0,'M1':450.0,'T':450.0},
					} 
			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.0614],'M':[-1.0,0.0614],'M1':[0.0614,1.0],'T':[0.0614,1.0],'F':[-1.0,0.0614]}
			if self.era=="2018":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.0494],'M':[-1.0,0.0494],'M1':[0.0494,1.0],'T':[0.0494,1.0],'F':[-1.0,0.0494]}

			self.LoadCuts =  	{



						'A':		{	
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'B':		{	
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'C':	 	{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'D':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},

						'E':		{	
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'F':	 	{	
								'btagHbb__H':cutranges['btagHbb__H']['M'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'G':		{	
								'btagHbb__H':cutranges['btagHbb__H']['M'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'H':	 	{	
								'btagHbb__H':cutranges['btagHbb__H']['M1'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M1'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'I':		{	
								'btagHbb__H':cutranges['btagHbb__H']['M1'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M1'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'J':		{	
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M1'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M1'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'K':	 	{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['M1'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M1'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'L':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},

						'M':		{	
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'N':	 	{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'O':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},



						'Z':		{	
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'FT':		{	
								'btagHbb__H':cutranges['btagHbb__H']['F'],
								'msoftdrop__H':cutranges['msoftdrop__H']['F'],
								'iMDtop__H':cutranges['iMDtop__H']['F'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['F'],
								'pt__B':cutranges['pt__B']['F'],
								'ptAK8':cutranges['ptAK8']['T'],
								},

						'FTR':		{	
								'btagHbb__H':cutranges['btagHbb__H']['F'],
								'msoftdrop__H':cutranges['msoftdrop__H']['F'],
								'iMDtop__H':cutranges['iMDtop__H']['F'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['F'],
								'pt__B':cutranges['pt__B']['F'],
								'ptAK8':cutranges['ptAK8']['T'],
								},

						'NM1Tmsoftdrop':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1TiMDtop':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1HbtagHbb':		{	
								'btagHbb__H':[-1.0,1.0],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1Hmsoftdrop':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1BbtagDeepFlavB':		{	
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'All':		{	
								'btagHbb__H':[-1.0,1.0],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__T':[0.0,1.0],
								'msoftdrop__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						}

		elif anatype=="tZb":
			self.labels = ["Z","T","B","TZB","TZ","BZ","BT"]
			self.ak8labels = ["Z","T"]
			self.ak4labels = ["B"]
			self.candl = "T"
			self.probl = "Z"

			cutranges = 	{
					'tau21__Z':{'L':[0.6,1.0],'M':[0.6,1.0],'M1':[0.45,0.6],'T':[0.0,0.45]},
					'msoftdrop__Z':{'L':[10.0,30.0],'M':[65.0,105.0],'M1':[65.0,105.0],'T':[65.0,105.0]},
					'iMDtop__T':{'L':[0.0,0.6],'M':[0.6,0.9],'M1':[0.6,0.9],'T':[0.9,1.0]},
					'msoftdrop__T':{'L':[30.0,65.0],'M':[140.0,220.0],'M1':[140.0,220.0],'T':[140.0,220.0]},
					'btagDeepFlavB__B':{'L':[-1.0,0.0521],'M':[-1.0,0.0521],'M1':[0.0521,1.0],'T':[0.0521,1.0],'F':[-1.0,0.0521]},
					'pt__B':{'L':200.0,'M':200.0,'M1':200.0,'T':200.0},
					'ptAK8':{'L':450.0,'M':450.0,'M1':450.0,'T':450.0},
					} 
			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.0614],'M':[-1.0,0.0614],'M1':[0.0614,1.0],'T':[0.0614,1.0],'F':[-1.0,0.0614]}
				cutranges['tau21__Z']={'L':[0.6,1.0],'M':[0.6,1.0],'M1':[0.4,0.6],'T':[0.0,0.4]}
			if self.era=="2018":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.0494],'M':[-1.0,0.0494],'M1':[0.0494,1.0],'T':[0.0494,1.0],'F':[-1.0,0.0494]}
			self.LoadCuts =  	{



						'A':		{	
								'tau21__Z':cutranges['tau21__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'B':		{	
								'tau21__Z':cutranges['tau21__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'C':	 	{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'D':		{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},

						'E':		{	
								'tau21__Z':cutranges['tau21__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'F':	 	{	
								'tau21__Z':cutranges['tau21__Z']['M'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'G':		{	
								'tau21__Z':cutranges['tau21__Z']['M'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'H':	 	{	
								'tau21__Z':cutranges['tau21__Z']['M1'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M1'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'I':		{	
								'tau21__Z':cutranges['tau21__Z']['M1'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M1'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'J':		{	
								'tau21__Z':cutranges['tau21__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M1'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M1'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'K':	 	{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['M1'],
								'msoftdrop__T':cutranges['msoftdrop__T']['M1'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'L':		{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'M':		{	
								'tau21__Z':cutranges['tau21__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'N':	 	{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'O':		{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'Z':		{	
								'tau21__Z':cutranges['tau21__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},


						'NM1Tmsoftdrop':{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1TiMDtop':{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1Ztau21':		{	
								'tau21__Z':[-1.0,1.0],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1Zmsoftdrop':		{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'NM1BbtagDeepFlavB':{	
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdrop__T':cutranges['msoftdrop__T']['T'],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						'All':		{	
								'tau21__Z':[-1.0,1.0],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__T':[0.0,1.0],
								'msoftdrop__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8':cutranges['ptAK8']['T'],
								},
						}

	def setruntrigs(self,runver):
		print "runver",runver

		if self.era=="2017" or self.era=="2018":
			self.ptrigs = ["HLT_PFHT780"]
			self.strigs = ["HLT_PFHT1050","HLT_PFJet500","HLT_PFJet550","HLT_AK8PFJet500","HLT_AK8PFJet550"]
			self.etrigs = ["HLT_AK8PFJet400_TrimMass30","HLT_AK8PFJet420_TrimMass30","HLT_AK8PFHT800_TrimMass50","HLT_AK8PFHT850_TrimMass50","HLT_AK8PFHT900_TrimMass50"]
			self.mutrigs = ["HLT_IsoMu27","HLT_IsoMu24_eta2p1","HLT_Mu50"]
		if self.era=="2016":
			self.ptrigs = ["HLT_PFHT650"]
			self.strigs = ["HLT_PFHT900","HLT_PFHT800","HLT_PFJet450","HLT_PFJet500","HLT_AK8PFJet450","HLT_AK8PFJet500"]
			self.etrigs = ["HLT_AK8PFHT700_TrimR0p1PT0p03Mass50","HLT_AK8PFHT650_TrimR0p1PT0p03Mass50","HLT_AK8PFJet360_TrimMass30"]	
			self.mutrigs = ["HLT_IsoMu27","HLT_IsoMu22_eta2p1","HLT_Mu50"]
		if runver=="Run2017B":
			self.etrigs = []
		if runver=="Run2016H":
			self.strigs = ["HLT_PFHT900","HLT_PFJet450","HLT_PFJet500","HLT_AK8PFJet450","HLT_AK8PFJet500"]

		
	def loadfiles(self,setname="QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",folder="/eos/cms/store/user/knash",redir="eoscms.cern.ch",search=""):
		ntry=0
		files = []
		#print setname,folder,redir
		versionstring=self.versionstring
		nanotype=self.nanotype
		#cmsxrootd.fnal.gov
		setnametowrite=setname.replace("/","_").replace("*","")
		#print setname,folder,redir,setnametowrite
		while len(files)==0:
				#print redir

				tempfname="tempfiles"+setnametowrite+self.era+".txt"
				spcall = "eos root://"+redir+" find  "+folder+"/"+setname+" > "+tempfname 
				print spcall
				#subprocess.call( ["eos root://cmseos.fnal.gov find  /eos/uscms/"+folder+"/"+setname], shell=True )
				subprocess.call( [spcall], shell=True )
				files = []
				
				with open(tempfname) as ftemp:
					filestemp = ftemp.read().splitlines()
					for curfile in filestemp:
						#print curfile
						#print curfile,versionstring,curfile.find(versionstring),search,curfile.find(search)
						
						if curfile.find(".root")!=-1 and curfile.find(versionstring)!=-1 and curfile.find(nanotype)!=-1 and curfile.find("failed")==-1 and curfile.find(search)!=-1:
							#files.append(curfile)
							if redir=="eoscms.cern.ch":
								files.append(curfile.replace("/eos/cms/","root://"+redir+":///"))
							else:
								files.append(curfile.replace("/eos/uscms/","root://"+redir+":///"))
							#print files[-1]
						#else:
						#	print "skipppp"
				subprocess.call( ["rm "+tempfname], shell=True )
				if len(files) != len(set(files)):
					logging.error("Duplicate Files")
				files = list(set(files))
				
				#files = eos find 
				if len(files)==0:
					ntry+=1
					logging.error("No Files Found For "+setname)
					time.sleep(2)

				if ntry>10:
					logging.error("Too Many Tries")
					sys.exit()
		return files
	def initcorr(self,filename):
		print filename
		index = filename.find("JetHT/Run")
		#super hacky parsing, assume RunXXXXY for year,run
		year,run=str(filename[index+9:index+13]),str(filename[index+13:index+14])
		print year,run
		print dir(createJMECorrector((not self.isdata), year, run, "Total", True, "AK8PFPuppi", True))
		print createJMECorrector((not self.isdata), year, run, "Total", True, "AK8PFPuppi", True)
		self.jmeCorrections = createJMECorrector((not self.isdata), year, run, "Total", True, "AK8PFPuppi", True)
		
	def histosmatchinit(self,labels,regions=['C']):
		histos = {}
		for region in regions:
			histos[region] = {}
			for label in labels:
				histos[region]["tau21__"+label+"__"+region] =  TH1F("tau21__"+label+"__"+region,	"tau21__"+label+"__"+region,		10000, 0.,1.01 )
				histos[region]["iMDW__"+label+"__"+region] =  TH1F("iMDW__"+label+"__"+region,	"iMDW__"+label+"__"+region,		10000, 0.,1. )		
				histos[region]["tau41__"+label+"__"+region] =  TH1F("tau41__"+label+"__"+region,	"tau41__"+label+"__"+region,		10000, 0.,1.01 )		
				histos[region]["iMDWW__"+label+"__"+region] =  TH1F("iMDWW__"+label+"__"+region,	"iMDWW__"+label+"__"+region,		10000, 0.,1.01 )		
		return histos



	def expandgeneric(self,ev,name,maxlen=-1,ptcut=30.0):

		nobj = int(getattr(ev, "n"+name))
		if maxlen>0:
			nobj = min(nobj,maxlen)
		objvec = []
		#print name	
		for iobj in xrange(nobj):
			curpt=float(getattr(ev, name+"_pt")[iobj])
			#if name=="GenPart":
			#	print curpt
			if curpt<ptcut:
				continue
			objvec.append(objecttype(name))

			objvec[-1].pt = float(curpt)
			objvec[-1].eta = float(getattr(ev, name+"_eta")[iobj])
			objvec[-1].phi = float(getattr(ev, name+"_phi")[iobj])
			objvec[-1].mass = float(getattr(ev, name+"_mass")[iobj])
			if name=="CustomAK8Puppi":	
				objvec[-1].iMDPho=float(getattr(ev, name+"_iMDPho")[iobj])
				objvec[-1].iMDWW=float(getattr(ev, name+"_iMDWW")[iobj])
				objvec[-1].iMDtop=float(getattr(ev, name+"_iMDtop")[iobj])
				objvec[-1].iW=float(getattr(ev, name+"_iW")[iobj])
				objvec[-1].iMDW=float(getattr(ev, name+"_iMDW")[iobj])
				objvec[-1].iMDtop=float(getattr(ev, name+"_iMDtop")[iobj])
				objvec[-1].msoftdrop=float(getattr(ev, name+"_msoftdrop")[iobj])
				objvec[-1].tau1=float(getattr(ev, name+"_tau1")[iobj])
				objvec[-1].tau2=float(getattr(ev, name+"_tau2")[iobj])
				if objvec[-1].tau1>0.0:
					objvec[-1].tau21=objvec[-1].tau2/objvec[-1].tau1
				else:
					objvec[-1].tau21=1.0
				objvec[-1].btagHbb=float(getattr(ev, name+"_btagHbb")[iobj])
				objvec[-1].rawFactor=float(getattr(ev, name+"_rawFactor")[iobj])
				objvec[-1].area=float(getattr(ev, name+"_area")[iobj])
			if name=="Jet":	
				objvec[-1].btagDeepFlavB=float(getattr(ev, name+"_btagDeepFlavB")[iobj])
				objvec[-1].rawFactor=float(getattr(ev, name+"_rawFactor")[iobj])
				objvec[-1].area=float(getattr(ev, name+"_area")[iobj])
			if name=="Muon":	
				#print getattr(ev, name+"_highPtId")[iobj]
				#print float(getattr(ev, name+"_highPtId")[iobj])
				#objvec[-1].mediumId=bool(getattr(ev, name+"_mediumId")[iobj])
				objvec[-1].tightId=bool(getattr(ev, name+"_tightId")[iobj])
				#print "MEDID",objvec[-1].mediumId
				#objvec[-1].mvaId=getattr(ev, name+"_mvaId")[iobj]
			if name=="Electron":	
				objvec[-1].mvaFall17V2Iso_WP90=int(getattr(ev, name+"_mvaFall17V2Iso_WP90")[iobj])
				objvec[-1].mvaFall17V2noIso_WP90=int(getattr(ev, name+"_mvaFall17V2noIso_WP90")[iobj])
			if name=="GenPart":	
				objvec[-1].pdgId=int(getattr(ev, name+"_pdgId")[iobj])
				objvec[-1].statusFlags=int(getattr(ev, name+"_statusFlags")[iobj])	
			#objvec[-1].p4.SetPtEtaPhiM(objvec[-1].pt,objvec[-1].eta,objvec[-1].phi,objvec[-1].mass)
			objvec[-1].setp4()
		return objvec

	def weightshistosinit(self,weightstoplot,regions=['C']):
		weightshistos = {}		
		for region in regions:
			weightshistos[region]={}
			for curweight in weightstoplot:
				if curweight=="genweightsf":
					curaxlims = [20000,-500.,500.]
				else:
					curaxlims = [100,-2.,2.]
				#print curweight+"__"+region
				#print curweight+"__"+region
				weightshistos[region][curweight]=TH1F(curweight+"__"+region,	"curweight"+"__"+region,		curaxlims[0], curaxlims[1],curaxlims[2])

			for whisto in weightshistos[region]:
				weightshistos[region][whisto].Sumw2()
		
		return weightshistos
	def histosinit(self,labels,regions=['C']):
		histos = {}
		AK4labs=["B"]
		for region in regions:
			#print region
			histos[region] = {}
			for label in labels:
				isAK4=False
				if label in AK4labs:
					isAK4=True
				if isAK4:
					histos[region]["p__"+label+"__"+region] =  TH1F("p__"+label+"__"+region,	"p__"+label+"__"+region,		350, 0.,3500. )
					histos[region]["pt__"+label+"__"+region] =  TH1F("pt__"+label+"__"+region,	"pt__"+label+"__"+region,		350, 0.,3500. )

				else:
					histos[region]["p__"+label+"__"+region] =  TH1F("p__"+label+"__"+region,	"p__"+label+"__"+region,		350, 400.,3900. )
					histos[region]["pt__"+label+"__"+region] =  TH1F("pt__"+label+"__"+region,	"pt__"+label+"__"+region,		350, 400.,3900. )
				histos[region]["eta__"+label+"__"+region] =  TH1F("eta__"+label+"__"+region,	"eta__"+label+"__"+region,		60, -3.0,3.0 )
				histos[region]["phi__"+label+"__"+region] =  TH1F("phi__"+label+"__"+region,	"phi__"+label+"__"+region,		80, -4.0,4.0)

				if len(label)>1:
					histos[region]["mass__"+label+"__"+region] =  TH1F("mass__"+label+"__"+region,	"mass__"+label+"__"+region,		800, 0.,8000. )

				if len(label)==1:
					histos[region]["mass__"+label+"__"+region] =  TH1F("mass__"+label+"__"+region,	"mass__"+label+"__"+region,		250, 0.,500.  )
					histos[region]["index__"+label+"__"+region] =  TH1F("index__"+label+"__"+region,	"index__"+label+"__"+region,		4, -.5,3.5  )
					if not isAK4:				
						histos[region]["msoftdrop__"+label+"__"+region] =  TH1F("msoftdrop__"+label+"__"+region,	"msoftdrop__"+label+"__"+region,		240, 0.,480. )
						if self.anatype=="Pho":
							histos[region]["Piso__"+label+"__"+region] =  TH1F("Piso__"+label+"__"+region,	"Piso__"+label+"__"+region,	5000, -1.0,1.0 )
							histos[region]["PelectronVeto__"+label+"__"+region] =  TH1F("PelectronVeto__"+label+"__"+region,	"PelectronVeto__"+label+"__"+region,	3, -1.5,1.5 )
							histos[region]["PpixelSeed__"+label+"__"+region] =  TH1F("PpixelSeed__"+label+"__"+region,	"PpixelSeed__"+label+"__"+region,	3, -1.5,1.5 )
							histos[region]["PmvaID_WP80__"+label+"__"+region] =  TH1F("PmvaID_WP80__"+label+"__"+region,	"PmvaID_WP80__"+label+"__"+region,	3, -1.5,1.5 )
							histos[region]["PmvaID_WP90__"+label+"__"+region] =  TH1F("PmvaID_WP90__"+label+"__"+region,	"PmvaID_WP90__"+label+"__"+region,	3, -1.5,1.5 )

	

							#histos[region]["Pisoch__"+label+"__"+region] =  TH1F("Pisoch__"+label+"__"+region,	"Pisoch__"+label+"__"+region,	5000, -1.0,1.0 )
							#histos[region]["Pbm__"+label+"__"+region] =  TH1F("Pbm__"+label+"__"+region,	"Pbm__"+label+"__"+region,		40, 0.,20. )
							#histos[region]["DRP__"+label+"__"+region] =  TH1F("DRP__"+label+"__"+region,	"DRP__"+label+"__"+region,		80, 0.,7. )
							histos[region]["iMDW__"+label+"__"+region] =  TH1F("iMDW__"+label+"__"+region,	"iMDW__"+label+"__"+region,		40, 0.,1. )
							histos[region]["iMDPho__"+label+"__"+region] =  TH1F("iMDPho__"+label+"__"+region,	"iMDPho__"+label+"__"+region,		5000, 0.,1. )
						if self.anatype=="WW":
							histos[region]["iMDW__"+label+"__"+region] =  TH1F("iMDW__"+label+"__"+region,	"iMDW__"+label+"__"+region,		40, 0.,1. )
							histos[region]["iMDWW__"+label+"__"+region] =  TH1F("iMDWW__"+label+"__"+region,	"iMDWW__"+label+"__"+region,		5000, 0.,1. )

						if self.anatype=="Zprime":
							histos[region]["iMDtop__"+label+"__"+region] =  TH1F("iMDtop__"+label+"__"+region,	"iMDtop__"+label+"__"+region,		5000, 0.,1. )
						if self.anatype=="Bstar":
							histos[region]["tau21__"+label+"__"+region] =  TH1F("tau21__"+label+"__"+region,	"tau21__"+label+"__"+region,		40, 0.,1. )
							histos[region]["iMDtop__"+label+"__"+region] =  TH1F("iMDtop__"+label+"__"+region,	"iMDtop__"+label+"__"+region,		5000, 0.,1. )
						if self.anatype=="tHb":
							histos[region]["iMDtop__"+label+"__"+region] =  TH1F("iMDtop__"+label+"__"+region,	"iMDtop__"+label+"__"+region,		5000, 0.,1. )
							histos[region]["btagHbb__"+label+"__"+region] =  TH1F("btagHbb__"+label+"__"+region,	"btagHbb__"+label+"__"+region,		100, -1.,1. )
						if self.anatype=="tZb":
							histos[region]["iMDtop__"+label+"__"+region] =  TH1F("iMDtop__"+label+"__"+region,	"iMDtop__"+label+"__"+region,		5000, 0.,1. )
							histos[region]["tau21__"+label+"__"+region] =  TH1F("tau21__"+label+"__"+region,	"tau21__"+label+"__"+region,		100, 0.,1. )
					else:
						histos[region]["btagDeepFlavB__"+label+"__"+region] =  TH1F("btagDeepFlavB__"+label+"__"+region,	"btagDeepFlavB__"+label+"__"+region,		100, 0.,1. )
	
				if len(label)==2:
					histos[region]["dphi__"+label+"__"+region] =  TH1F("dphi__"+label+"__"+region,	"dphi__"+label+"__"+region,		60, -4.0,4.0 )
					histos[region]["dR__"+label+"__"+region] =  TH1F("dR__"+label+"__"+region,	"dR__"+label+"__"+region,		100, 0.0,10.0 )
					histos[region]["ht__"+label+"__"+region] =  TH1F("ht__"+label+"__"+region,	"ht__"+label+"__"+region,		300, 1000.0,5000.0 )
					histos[region]["htval__"+label+"__"+region] =  TH1F("htval__"+label+"__"+region,	"htval__"+label+"__"+region,		300, 1000.0,5000.0 )
					histos[region]["deltapt__"+label+"__"+region] =  TH1F("deltapt__"+label+"__"+region,	"deltapt__"+label+"__"+region,		250, -500.,500.0 )
					histos[region]["deta__"+label+"__"+region] =  TH1F("deta__"+label+"__"+region,	"deta__"+label+"__"+region,		100, 0.,5.0 )
					histos[region]["dy__"+label+"__"+region] =  TH1F("dy__"+label+"__"+region,	"dy__"+label+"__"+region,		30, 0.,3.0 )
					histos[region]["dyhighm__"+label+"__"+region] =  TH1F("dyhighm__"+label+"__"+region,	"dyhighm__"+label+"__"+region,		30, 0.,3.0 )
					if self.anatype=="Pho":
							histos[region]["iMDW__"+label[1]+"__iMDPho__"+label[0]+"__"+region] =  TH2F("iMDW__"+label[1]+"__iMDPho__"+label[0]+"__"+region,	"iMDW__"+label[1]+"__iMDPho__"+label[0]+"__"+region,		40, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDPho__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDPho__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDPho__"+label[0]+"__"+region,		240, 0.,480.,100, 0.,1. )
					if self.anatype=="WW":
							histos[region]["iMDW__"+label[1]+"__iMDWW__"+label[0]+"__"+region] =  TH2F("iMDW__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"iMDW__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		40, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDWW__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		240, 0.,480.,100, 0.,1. )
							histos[region]["njets__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("njets__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"njets__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		15,-0.5, 14.5,100, 0.,1. )
							histos[region]["htval__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("htval__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"htval__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		250, 0.,2500.,100, 0.,1. )
							histos[region]["njetsrem__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("njetsrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"njetsrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		15,-0.5, 14.5,100, 0.,1. )
							histos[region]["htvalrem__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("htvalrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"htvalrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		250, 0.,2500.,100, 0.,1. )

					if self.anatype=="Zprime":
							histos[region]["iMDtop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("iMDtop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"iMDtop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )

					if self.anatype=="Bstar":
							histos[region]["tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		240, 0.,480.,100, 0.,1. )
				if len(label)>2:
					if self.anatype=="tHb":
							histos[region]["btagHbb__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("btagHbb__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"btagHbb__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, -1.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		240, 0.,480.,100, 0.,1. )

					if self.anatype=="tZb":
							histos[region]["tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		240, 0.,480.,100, 0.,1. )

				if not isAK4:				
					histos[region]["pt__"+label+"__aeta__"+label+"__"+region] =  TH2F("pt__"+label+"__aeta__"+label+"__"+region,	"pt__"+label+"__aeta__"+label+"__"+region,		350, 400.,3900.,24, 0.0,2.4 )
				else:				
					histos[region]["pt__"+label+"__aeta__"+label+"__"+region] =  TH2F("pt__"+label+"__aeta__"+label+"__"+region,	"pt__"+label+"__aeta__"+label+"__"+region,		350, 0.,3500.,24, 0.0,2.4 )


		for region in regions:
			for histo in histos[region]:
				histos[region][histo].Sumw2()
		return histos


	def makeinv(self,cands,lab):

		return invcand
	def weightshistosfill(self,weightshistos,weightdict,region):
		if not (region in weightshistos):
			return
		for whisto in weightdict[region]:
			for vari in weightdict[region][whisto]:
				if (whisto+vari) in weightshistos[region]:
					weightshistos[region][whisto+vari].Fill(weightdict[region][whisto][vari])
				
	def histosfill(self,histos,cands,region='C',weight=1.0,hfilter=[]):
		if not (region in histos):
			return
		for histo in histos[region]:
			
			keep=False
			if hfilter==[]:
				keep=True
			for hf in hfilter:
				if histo.find(hf)!=-1:
					keep=True
			if not keep:
				continue 
			#print region,histo
			
			idval = histo.split("__")
			#print idval
			if isinstance(histos[region][histo], TH2F):
				#print "2D",idval[0],idval[1],idval[2],idval[3]
				if cands[idval[1]]!=None and cands[idval[3]]!=None:
					if cands[idval[1]][idval[0]]!=None and cands[idval[3]][idval[2]]!=None:
						#print "filling",histo,cands[idval[1]][idval[0]],cands[idval[3]][idval[2]]
						histos[region][histo].Fill(cands[idval[1]][idval[0]],cands[idval[3]][idval[2]],weight)
			else:
				if cands[idval[1]]!=None:
					#print idval[1],idval[0]
					if cands[idval[1]][idval[0]]!=None:
						#print "filling",histo,cands[idval[1]][idval[0]]
						histos[region][histo].Fill(cands[idval[1]][idval[0]],weight)
		
	def overlapcheck(self,histos,cands,region,matchmatrix):
		for histo in histos[region]:
			if [region,histo] in matchmatrix:
				logging.error("Multiple histogram fills")
				sys.exit()
			else:
				matchmatrix.append([region,histo])
	def tagjet(self,ak8jet,obj,region='C'):
		curcuts = self.LoadCuts[region] 
		defaultcuts = self.LoadCuts['C'] 

		if obj=="W":
			#if region=="C":
			#	if curcuts["msoftdrop__W"][0]<ak8jet["msoftdrop"]<curcuts["msoftdrop__W"][1]:
			#		print region,ak8jet["iMDW"],ak8jet["iMDW"],ak8jet["msoftdrop"]
			if curcuts["iMDW__W"][0]<ak8jet.iMDW<=curcuts["iMDW__W"][1] :
				if curcuts["msoftdrop__W"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__W"][1]:
					return True
				
		if obj=="H":
			if curcuts["btagHbb__H"][0]<ak8jet.btagHbb<=curcuts["btagHbb__H"][1] and (curcuts["msoftdrop__H"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__H"][1]):
				

				if "iMDtop__H" in curcuts:
					if curcuts["iMDtop__H"][0]<ak8jet.iMDtop<=curcuts["iMDtop__H"][1]:
						return True
				else:			
					return True
		if obj=="Z":
			if curcuts["tau21__Z"][0]<ak8jet.tau21<=curcuts["tau21__Z"][1] and (curcuts["msoftdrop__Z"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__Z"][1]):
				return True
		if obj=="T":
			if (curcuts["iMDtop__T"][0]<ak8jet.iMDtop<=curcuts["iMDtop__T"][1]) and (curcuts["msoftdrop__T"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__T"][1]):
					return True	
				#if self.anatype=="tHb":
				#	if not (curcuts["_btagHbb__T"][0]<ak8jet["btagHbb"]<=curcuts["Inv_btagHbb__T"][1] and (curcuts["Inv_msoftdrop__T"][0]<ak8jet["msoftdrop"]<=curcuts["Inv_msoftdrop__T"][1])):
				#		return True
				#elif self.anatype=="Bstar":
				#	#if not( curcuts["Inv_tau21__T"][0]<ak8jet["tau21"]<curcuts["Inv_tau21__T"][1] and (curcuts["Inv_msoftdrop__T"][0]<ak8jet["msoftdrop"]<curcuts["Inv_msoftdrop__T"][1])):		
				#	return True
				#else:
				#	return True



		if obj=="A":
			if (curcuts["iMDtop__A"][0]<ak8jet.iMDtop<=curcuts["iMDtop__A"][1]) and (curcuts["msoftdrop__A"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__A"][1]):
					return True
		if obj=="B":
			if curcuts["btagDeepFlavB__B"][0]<ak8jet.btagDeepFlavB<=curcuts["btagDeepFlavB__B"][1]:
					return True
		if obj=="P":
			if ((curcuts["iMDPho__P"][0]<ak8jet.iMDPho<=curcuts["iMDPho__P"][1]) and (curcuts["msoftdrop__P"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__P"][1])):
				if curcuts["msoftdrop__P"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__P"][1]:
				#if not ( (curcuts["Inv_iMDW__P"][0]<ak8jet["iMDW"]<curcuts["Inv_iMDW__P"][1])):		
					return True
		if obj=="F":
			if ((curcuts["iMDWW__F"][0]<ak8jet.iMDWW<=curcuts["iMDWW__F"][1]) and (curcuts["msoftdrop__F"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__F"][1])):
				#if not ( (curcuts["Inv_iMDW__F"][0]<ak8jet["iMDW"]<curcuts["Inv_iMDW__F"][1])):
				if curcuts["msoftdrop__F"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__F"][1]:		
					return True
		return False
	
	
	def TriggerPass(self,curdictval,prescale=False):
		#print "intp"  
		for ctrig in curdictval:
			#print ctrig,curdictval[ctrig]
			try: 
				if curdictval[ctrig]==1:
					#print "PASS!"
					return True
			except:
				print "Missing trigger",ctrig
		#print "FAIL!"
		return False 

	def disambiguate(self,tags,jets):
		cands = {"W":None, "P":None}
		intersection = list(set(tags["W"]) & set(tags["P"]))
		print tags 
		print intersection
		if len(tags["W"])>=2 and len(tags["P"])>=2:
			#print "randomizing"
			randomar =  [0,1]
			random.shuffle(randomar)
			#print "returning W",randomar[0]
			#print "returning P",randomar[1]
			cands["W"]=jets[randomar[0]]
			cands["P"]=jets[randomar[1]]
			
		else:
			for tag in tags:
				if len(tags[tag])==2:
					#print "removing", intersection[0]
					tags[tag].remove(intersection[0])
			#print "returning W",tags["W"][0]
			#print "returning P",tags["P"][0]
			cands["W"]= jets[tags["W"][0]]
			cands["P"]= jets[tags["P"][0]]
		return cands
		
	def getPUPPIweight(self,puppipt,puppieta ):
		puppifile=TFile('puppiCorr.root','open')
  		puppisd_corrGEN      = puppifile.Get("puppiJECcorr_gen")
  		puppisd_corrRECO_cen = puppifile.Get("puppiJECcorr_reco_0eta1v3")
  		puppisd_corrRECO_for = puppifile.Get("puppiJECcorr_reco_1v3eta2v5")


  		genCorr  = 1.
  		recoCorr = 1.
  		totalWeight = 1.
        
  		genCorr =  puppisd_corrGEN.Eval( puppipt )
  		if abs(puppieta)  <= 1.3 :
    			recoCorr = puppisd_corrRECO_cen.Eval( puppipt )
  
  		else:
    			recoCorr = puppisd_corrRECO_for.Eval( puppipt )
  
  
  		totalWeight = genCorr * recoCorr;

  		return totalWeight;

	def physobjinit(self,lvdict,num=10):
		
		tlvs = []
		otherb = []
		for cname in lvdict:
			#if not (cname in ["pt","eta","phi","mass"]):
			#print cname
			otherb.append(cname)
		for lv in xrange(min(len(lvdict["pt"]),num)):
			#print lv
			
			tlvs.append({})
			tlvs[-1]["TLV"] = TLorentzVector()
			tlvs[-1]["TLV"].SetPtEtaPhiM(lvdict["pt"][lv],lvdict["eta"][lv],lvdict["phi"][lv],lvdict["mass"][lv])
			tlvs[-1]["p"] = tlvs[-1]["TLV"].P()
			tlvs[-1]["aeta"] = abs(tlvs[-1]["TLV"].Eta())

			#print "tob"
			for oth in otherb:
				#print "tob",lvdict[oth][lv]
				tlvs[-1][oth] = lvdict[oth][lv]
			#print "done"
		#print "ret"
		return tlvs

	def Make_Pull_plot( self,DATA,BKG,BKGUP,BKGDOWN ):
		pull = DATA.Clone("pull")

		pull
		pull.Add(BKG,-1)
		sigma = 0.0
		FScont = 0.0
		BKGcont = 0.0
		normval=1.0
		if DATA.GetEntries()!=0:
			normval = DATA.Integral()/float(DATA.GetEntries())
		for ibin in range(1,pull.GetNbinsX()+1):
			FScont = DATA.GetBinContent(ibin)
			BKGcont = BKG.GetBinContent(ibin)
			if FScont>=BKGcont:
				FSerr = DATA.GetBinErrorLow(ibin)
				BKGerr = abs(BKGUP.GetBinContent(ibin)-BKG.GetBinContent(ibin))
			if FScont<BKGcont:
				FSerr = DATA.GetBinErrorUp(ibin)
				BKGerr = abs(BKGDOWN.GetBinContent(ibin)-BKG.GetBinContent(ibin))
			if FScont == 0.0:
				FSerr=1.84*normval
	
			sigma = sqrt(FSerr*FSerr + BKGerr*BKGerr)

			if FScont == 0.0 and BKGcont == 0.0 :
				pull.SetBinContent(ibin, 0.0 )
			else:
				if sigma != 0 :
					pullcont = (pull.GetBinContent(ibin))/sigma
					pull.SetBinContent(ibin, pullcont)
				else :
					pull.SetBinContent(ibin, 0.0 )



		return pull


	def jersmear(self,jets, genjets,rho,jind,jtype="ak8"):
	
		pairs = matchObjectCollection(jets, genjets)
		if jtype=="ak8":
			params_sf_and_uncertainty = self.params_sf_and_uncertainty
			params_resolution = self.params_resolution
			jerSF_and_Uncertainty = self.jerSF_and_Uncertainty
			jer = self.jer
		if jtype=="ak4":
			params_sf_and_uncertainty = self.params_sf_and_uncertaintyak4
			params_resolution = self.params_resolutionak4
			jerSF_and_Uncertainty = self.jerSF_and_Uncertaintyak4
			jer = self.jerak4
		#print pairs
		for ak8j in jets:
			#temporary, for some reason low pt stuff throws an error.  has a small effect on ht
			
            		params_sf_and_uncertainty.setJetEta(ak8j.eta)
			curSF = jerSF_and_Uncertainty.getScaleFactor(params_sf_and_uncertainty, jind)

			#CHECK THIS!!!!
			smearFactor=1.0
			genJet=pairs[ak8j]
			params_resolution.setJetPt(ak8j.pt)
			params_resolution.setJetEta(ak8j.eta)
			params_resolution.setRho(rho)
		  	jet_pt_resolution = jer.getResolution(params_resolution)
			dostoc=False
			if genJet==None:
				dostoc=True
			if not dostoc:
				dPt = ak8j.pt - genJet.pt
				if abs(dPt)>3.0*ak8j.pt*jet_pt_resolution:
					dostoc=True
			if not dostoc:
				#print "ptreco",ak8j.pt,"ptgen",genJet.pt
				
				smearFactor = 1. + (curSF - 1.)*dPt/ak8j.pt
				#print "smear",smearFactor,"dPt",dPt,"curSF",curSF
				
			else:
		  		jerrand = self.rnd.Gaus(0,jet_pt_resolution)
				if curSF>1.:
		      			smearFactor = 1. + jerrand * math.sqrt(curSF**2 - 1.)
			if (smearFactor*ak8j.pt) < 1.e-2:
				smearFactor = 1.e-2
			#ak8jorigpt = ak8j.pt
			ak8j.pt = ak8j.pt*smearFactor
			#if ak8j.pt<0.0:
			#	print "bloop2",ak8j.pt,ak8jorigpt,smearFactor
			ak8j.setp4()

	def pdfweight(self,pdfweights):

		avew=sum(pdfweights)/len(pdfweights)
		#print "np",len(pdfweights),"avew",avew
		pdw=0
		# check rms math 
		for pp in pdfweights:
			pdw+=(pp-avew)*(pp-avew)
		#curttree.Draw("LHEPdfWeight>>pdavehist","","goff")
		#print "pdw2",pdw
		pdw = sqrt(pdw)
		#print "pdw",pdw
		return {"sf":1.0,"down":1.0-pdw,"up":1.0+pdw}
	def q2weight(self,q2weights):
		upweight = max(q2weights)
		downweight = min(q2weights)
		#upweight = max(0.0,upweight)
		#downweight = max(0.0,downweight)
		return {"sf":1.0,"down":downweight,"up":upweight}
	#PLACEHOLDER
	def toptagsf(self,ak8jet,cut):
		if cut=="T":
			return {"sf":1.0,"down":1.1,"up":0.9}
		else:
			return {"sf":1.0,"down":1.0,"up":1.0}
	def htagsf(self,ak8jet,cut,settype="Signal"):
		if settype=="Signal":
			if self.era=="2016":
				sf=	[350.0,850.0,1.01,0.06,0.10]
					
			if self.era=="2017":
				sf=	[350.0,840.0,0.9,0.08,0.04]
					
			if self.era=="2018":
				sf=	[350.0,850.0,0.89,0.06,0.04]
		#USE 2017 TTBAR FOR ALL!!
		elif settype=="TT":
			if self.era=="2016":
				sf=	[430.0,float("inf"),0.902,0.083,0.081]
					
			if self.era=="2017":
				sf=	[430.0,float("inf"),0.902,0.083,0.081]
					
			if self.era=="2018":
				sf=	[430.0,float("inf"),0.902,0.083,0.081]
		else:
			return {"sf":1.0,"down":1.0,"up":1.0}
		if cut=="T":
			if sf[0]<ak8jet.pt<sf[1]:
				return {"sf":sf[2],"down":sf[2]-sf[4],"up":sf[2]+sf[3]}
			else:
				#RETURN 2XUNC, CHECK!!
				return {"sf":sf[2],"down":sf[2]-2.0*sf[4],"up":sf[2]+2.0*sf[3]}
		else:
			return {"sf":1.0,"down":1.0,"up":1.0}
	def btagsf(self,ak4jet,cut):
		ak4pt = ak4jet.pt
		if cut=="T":
			
			bsfdict={"sf":1.0,"down":1.0,"up":1.0}
			for bsf in bsfdict:
				for prange in (self.btagdict)[bsf]:
					if prange[0]<ak4pt<prange[1]:
						bsfdict[bsf]=prange[2].Eval(ak4pt)
					if (prange[1]<ak4pt) and (prange==(self.btagdict)[bsf][-1]):
						bsfdict[bsf]=2.0*prange[2].Eval(prange[1])
			
			
			
			return bsfdict
		else:
			return {"sf":1.0,"down":1.0,"up":1.0}
	def wtagsf(self,ak8jet,cut):

		if cut=="T":
			if self.era=="2016":
				sf=[0.980,0.027]
					
			if self.era=="2017":
				sf=[0.97,0.06]
					
			if self.era=="2018":
				sf=[1.10,0.12]
			return {"sf":sf[0],"down":sf[0]-sf[1],"up":sf[0]+sf[1]}
		else:
			return {"sf":1.0,"down":1.0,"up":1.0}
	def puweight(self,ntrueint):

		pudict={"sf":1.0,"down":1.0,"up":1.0}

		cbin= (self.puhists["sf"]).FindBin(ntrueint)
		pudict["sf"] = min(5.0,(self.puhists["sf"]).GetBinContent(cbin))
		pudict["down"] = min(5.0,(self.puhists["down"]).GetBinContent(cbin))
		pudict["up"] = min(5.0,(self.puhists["up"]).GetBinContent(cbin))
		#print ntrueint,pudict
		return pudict
	def triggerweight(self,ht,msd=0.0):
		#print "trigw",ht,msd
		trigdict={}
		#print "maxes",self.maxtright,self.maxtrigmass
		maxtright=1500.0
		maxtrigmass=120.0
		trigrand=random.random()
		#print "trigrand",trigrand
		histotype="2D"
		trhisto=None
		for it in xrange(len(self.trigprobs)):
			#print it,trigrand,self.trigprobs[it]
			if trigrand>self.trigprobs[it]:
		
				if self.era=="2017" and it==1:
					trhisto=self.trighists[it]
					histotype="1D"
					#print "using 1D"
					
				else:
					trhisto=self.trighist2ds[it]	
				break
		if trhisto==None:
			print "Trig ERROR!"
			return {"sf":1.0,"down":1.0,"up":1.0}
		if histotype=="1D":
			if ht > maxtright:
				trigdict= {"sf":1.0,"down":1.0,"up":1.0}
			else:
				htbin = trhisto.FindBin(ht)
				weight = trhisto.GetBinContent(htbin)
				toterr=0.5*abs(1.0-weight)
				trigdict= {"sf":weight,"down":max(weight-toterr,0.0),"up":min(weight+toterr,1.0)}
		else:		
			if (ht > maxtright) or (msd > maxtrigmass):
				trigdict= {"sf":1.0,"down":1.0,"up":1.0}
		
			else:
				htbin = trhisto.GetXaxis().FindBin(ht)
				msdbin = trhisto.GetYaxis().FindBin(msd)
				weight = trhisto.GetBinContent(htbin,msdbin)
				toterr=0.5*abs(1.0-weight)
				trigdict= {"sf":weight,"down":max(weight-toterr,0.0),"up":min(weight+toterr,1.0)}
		#print trigdict
		return trigdict
		
	def candtodict(self,cands):
		dictver = {}
		for cand in cands:
			dictver[cand]={}
			#print cand
			#print cands[cand],type(cands[cand])
			dictver[cand]["pt"] = cands[cand].pt
			dictver[cand]["eta"] = cands[cand].eta
			dictver[cand]["phi"] = cands[cand].phi
			dictver[cand]["mass"] = cands[cand].mass
			dictver[cand]["aeta"] = abs(cands[cand].eta)


			if len(cand)==1:
				dictver[cand]["p"] = cands[cand].p4.P()
				dictver[cand]["index"] = cands[cand].index
				if cand in self.ak8labels:
					dictver[cand]["iMDPho"] = cands[cand].iMDPho
					dictver[cand]["iMDWW"] = cands[cand].iMDWW
					dictver[cand]["iMDtop"] = cands[cand].iMDtop
					dictver[cand]["iW"] = cands[cand].iW
					dictver[cand]["iMDW"] = cands[cand].iMDW
					dictver[cand]["iMDtop"] = cands[cand].iMDtop
					dictver[cand]["msoftdrop"] = cands[cand].msoftdrop
					dictver[cand]["tau1"] = cands[cand].tau1
					dictver[cand]["tau2"] = cands[cand].tau2
					#dictver[cand]["tau3"] = cands[cand].tau3
					#dictver[cand]["tau4"] = cands[cand].tau4
					dictver[cand]["tau21"] = cands[cand].tau21
					dictver[cand]["btagHbb"] = cands[cand].btagHbb
				else:
					dictver[cand]["btagDeepFlavB"] = cands[cand].btagDeepFlavB

			else:

				dictver[cand]["p"] = cands[cand].p4.P()
				dictver[cand]["deltapt"] = cands[cand].deltapt
				dictver[cand]["deta"] = cands[cand].deta
				dictver[cand]["dphi"] = cands[cand].dphi
				dictver[cand]["ht"] = cands[cand].ht
				dictver[cand]["htval"] = cands[cand].htval
				dictver[cand]["dR"] = cands[cand].dR
				dictver[cand]["dy"] = cands[cand].dy
				dictver[cand]["dyhighm"] = cands[cand].dyhighm
		return dictver

	def tptrw(self,geninfo):
		TPT = None
		ATPT = None
		tptsf= {"sf":1.0,"down":1.0,"up":1.0}
		igens=0
		#print len(geninfo)
		for gg in geninfo:
			igens+=1
			if gg.statusFlags!=10497:
				continue
			if (gg.pdgId==6) and TPT==None:
				TPT = gg.pt
			if (gg.pdgId==-6) and ATPT==None:
				ATPT = gg.pt
			if TPT!=None and ATPT!=None:
				
				#print "foundem ",TPT,ATPT
				#print
				#print math.exp(0.0615-0.0005*TPT),math.exp(0.0615-0.0005*ATPT)
				sfval= math.exp(0.0615-0.0005*TPT)*math.exp(0.0615-0.0005*ATPT)
				abserror = 1.0-sfval
				#print sfval,abserror
				tptsf["sf"] = sfval
				tptsf["down"] = 1.0
				tptsf["up"] = max((1.0-2.0*abserror),0.0)
				break

		if tptsf["sf"]==1.0:
			print "1.0",geninfo
		#print tptsf
		return tptsf	



def setfilter(setstring):
	filtername=None
	if (setstring).find('JetHT')!=-1:
		filtername="JetHT"
	if (setstring).find('QCD')!=-1:
		filtername="QCD"
	if ((setstring).find('TTTo')!=-1) or ((setstring).find('TT_Mtt')!=-1):
		filtername="TT"
	if (setstring).find('WJetsToQQ')!=-1:
		filtername="WJets"
	if (setstring).find('WpTo')!=-1:
		filtername="Signal"
	return filtername 

def strf(x):
	return '%.0f' % x



