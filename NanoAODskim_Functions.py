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
from ROOT import TLorentzVector,TH1F,TH2F,TH3F,TTree,TFile,gROOT,TCanvas,TGraph,TMultiGraph,TLegend,gROOT,TTreeReader,TLatex

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection, matchObjectCollectionMultiple
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetSmearer import jetSmearer

class ObjectType:
	def __init__(self,name):
		self.pt = None
		self.eta = None
		self.phi = None
		self.mass = None
		self.p4 = TLorentzVector()
		self.shift = 1.0
		self.mshift = 1.0
		self.umass = None
		self.upt = None 

		self.name = name
		if name=="CustomAK8Puppi":
			self.jetId= None
			self.iMDPho= None
			self.iMDWW= None
			self.iMDtop= None
			self.iW= None
			self.iMDW= None
			self.iMDtop= None
			self.msoftdrop= None
			self.msoftdropdef= None
			self.umsoftdrop = None 
			self.tau1= None
			self.tau2= None
			self.tau21= None
			self.btagHbb= None
			self.rawFactor= None
			self.area= None
			self.subJetIdx1= None
			self.subJetIdx2= None
		if name=="CustomAK8PuppiSubJet":
			self.rawFactor= None
			self.area= None
		if name=="Jet":
			self.jetId= None
			self.btagDeepFlavB= None
			self.btagCSVV2= None
			self.rawFactor= None
			self.area= None
	
		if name=="GenPart":
			self.pdgId= None
			self.statusFlags= None
			self.genPartIdxMother= None

		if name=="GenJet":
			self.hadronFlavour= None
		if name=="Muon":
			self.tightId= None
			self.pfIsoId= None
			self.mediumId= None
			self.mvaId= None
			self.miniPFRelIso_all= None

		if name=="Electron":
			self.mvaFall17V2Iso_WP90= None
			self.mvaFall17V2noIso_WP90= None
			self.mvaFall17V2Iso_WP80= None
			self.mvaFall17V2noIso_WP80= None

	def setp4(self):
		self.p4.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)

	def setfromp4(self,p4):
		self.p4=p4
		#print self.pt,self.p4.Perp()
		self.pt=self.p4.Perp()
		self.eta=self.p4.Eta()
		self.phi=self.p4.Phi()
		self.mass=self.p4.M()
	def setshift(self,shift):
		#print self.pt,self.mass,shift
		self.shift*=shift
		self.mass=self.umass*self.shift
		self.pt=self.upt*self.shift
		#print self.pt,self.mass,shift

		self.setp4()
	def setmshift(self,mshift):
		self.mshift*=mshift
		self.msoftdrop=self.umsoftdrop*self.mshift
	def reset(self):

		#print "pt upt",self.pt,self.upt
		if self.name=="CustomAK8Puppi":
			#print self.msoftdrop,self.umsoftdrop
			#self.msoftdrop=self.umsoftdrop
			self.mshift=1.0
			self.setmshift(1.0)
		#self.pt=self.upt
		#self.mass=self.umass
		self.shift=1.0
		self.setshift(1.0)
		self.setp4()
class InvObj:
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
			if self.mass>2000.:
				self.dyhighm = abs(ovec[0].p4.Rapidity()-ovec[1].p4.Rapidity())
		self.njets = 0
		self.htval=0.0
		self.njetsrem=0
		self.htvalrem=0.0
		self.idval= 0

class NanoAODskim_Functions:
	def __init__(self,anatype="Pho",era="2017",versionstring=["v8"],settype="TT",condor=False):
		di=""
		if condor:
			di="tardir/"
		self.isdata=False
		if settype in ["JetHT","SingleMuon","SingleElectron","EGamma"]:
			self.isdata=True
		print settype,self.isdata
		self.anatype=anatype
		self.truncval = 300
		self.era = era
		self.versionstring = versionstring
		self.masssmearlims=[0.6,1.5]

		self.nanotype = "NanoSlimNtuples"
		self.trigstopass=[]
        	self.rnd1 = ROOT.TRandom3(12345)
        	self.rnd2 = ROOT.TRandom3(12345)

		NanoAODskimData= NanoAODskim_Data(era,condor=condor)
		self.LoadConstants=NanoAODskimData.LoadConstants
		self.allsignamesHT=NanoAODskimData.allsignamesHT
		self.allsignamesZT=NanoAODskimData.allsignamesZT
		self.genmatrix=NanoAODskimData.genmatrix
		self.runver=NanoAODskimData.runver
		self.topSFhists = NanoAODskimData.topSFhists
		if anatype in ["Mu","Ele"]:
			self.btagdict=NanoAODskimData.btagdictDFlav
			self.bmistagdict=NanoAODskimData.bmistagdictDFlav
		else:
			self.btagdict=NanoAODskimData.btagdictDFlav
			self.bmistagdict=NanoAODskimData.bmistagdictDFlav

		
		#for ll in self.LoadConstants['dataconst']:
		#	print ll,self.LoadConstants['dataconst'][ll])
		self.puppifile = ROOT.TFile.Open(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/puppiCorr.root")
  		self.puppisd_corrGEN      = self.puppifile.Get("puppiJECcorr_gen")
  		self.puppisd_corrRECO_cen = self.puppifile.Get("puppiJECcorr_reco_0eta1v3")
  		self.puppisd_corrRECO_for = self.puppifile.Get("puppiJECcorr_reco_1v3eta2v5")
		self.jmeCorrections = {}
		self.jmeCorrectionsak4 = {}
		self.jmeCorrectionsak4puppi = {}
		self.recal = {}
		self.recalak4 = {}
		self.recalak4puppi = {}

		if self.era=="2016":
			periods = 	{ 'B','C','D','E','F','G','H'}
		if self.era=="2017":
			periods = 	{ 'B','C','D','E','F'}
		if self.era=="2018":
			periods = 	{ 'A','B','C','D'}
 


		if (not self.isdata):
			self.jmeCorrections["All"]=createJMECorrector((not self.isdata), self.era, "B", "Total", True, "AK8PFPuppi", False)()
			self.jmeCorrectionsak4["All"]=createJMECorrector((not self.isdata), self.era, "B", "Total", True, "AK4PFchs", True)()
			self.jmeCorrectionsak4puppi["All"]=createJMECorrector((not self.isdata), self.era, "B", "Total", True, "AK4PFPuppi", True)()
			self.recal["All"]=self.jmeCorrections["All"].jetReCalibrator
			self.recalak4["All"] = self.jmeCorrectionsak4["All"].jetReCalibrator
			self.recalak4puppi["All"] = self.jmeCorrectionsak4puppi["All"].jetReCalibrator
		else:
			for period in periods:
				self.jmeCorrections[period]=createJMECorrector((not self.isdata), self.era, period, "Total", True, "AK8PFPuppi", False)()
				self.jmeCorrectionsak4[period]=createJMECorrector((not self.isdata), self.era, period, "Total", True, "AK4PFchs", True)()
				self.jmeCorrectionsak4puppi[period]=createJMECorrector((not self.isdata), self.era, period, "Total", True, "AK4PFPuppi", True)()
				self.recal[period]=self.jmeCorrections[period].jetReCalibrator
				self.recalak4[period] = self.jmeCorrectionsak4[period].jetReCalibrator
				self.recalak4puppi[period] = self.jmeCorrectionsak4puppi[period].jetReCalibrator

		self.tteff=	{
			"tau21":0.68,
			"iMDtop":0.52,
			"btagHbb":0.14
			}

		if not self.isdata:

			smearmc = self.jmeCorrections["All"].jetSmearer
			self.params_sf_and_uncertainty = ROOT.PyJetParametersWrapper()
			self.jer = ROOT.PyJetResolutionWrapper(os.path.join(smearmc.jerInputFilePath, smearmc.jerInputFileName))
			self.jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(smearmc.jerInputFilePath, smearmc.jerUncertaintyInputFileName))
	       		self.params_resolution = ROOT.PyJetParametersWrapper()


			smearmcak4 = self.jmeCorrectionsak4["All"].jetSmearer
			self.params_sf_and_uncertaintyak4 = ROOT.PyJetParametersWrapper()
			self.jerak4 = ROOT.PyJetResolutionWrapper(os.path.join(smearmcak4.jerInputFilePath, smearmcak4.jerInputFileName))
			self.jerSF_and_Uncertaintyak4 = ROOT.PyJetResolutionScaleFactorWrapper(os.path.join(smearmcak4.jerInputFilePath, smearmcak4.jerUncertaintyInputFileName))
	       		self.params_resolutionak4 = ROOT.PyJetParametersWrapper()
			#self.jetSmearer = self.jmeCorrections.jetSmearer



			self.enlist=[0,2,1]
        		self.jet_m_sf_and_uncertainty = dict( zip( self.enlist, smearmc.jmr_vals ) )
			self.jms_vals = self.jmeCorrections["All"].jmsVals
			#print "SMEAR",smearmc.jmr_vals 
			#print "SMEAR",smearmc.jmr_vals 
			#print "SMEAR",smearmc.jmr_vals 
				
			self.puppiJMRFile = ROOT.TFile.Open(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/puppiSoftdropResol.root")
			self.puppisd_resolution_cen = self.puppiJMRFile.Get("massResolution_0eta1v3")
			self.puppisd_resolution_for = self.puppiJMRFile.Get("massResolution_1v3eta2v5")

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



		if anatype in ["Mu","Ele"]:
			self.labels = ["T","B"]
			self.ak8labels = ["T"]
			self.ak4labels = ["B"]
			self.candl = "T"
			self.probl = "B"

			cutranges = 	{
					'iMDtop__T':{'L':[0.0,0.9],'T':[0.9,1.0]},
					'msoftdropdef__T':{'L':[0.0,float("inf")],'T':[140.0,220.0]},
					'btagDeepFlavB__B':{'T':[0.3033,1.0]},
					'pt__B':{'T':100.0},
					'ptAK8__T':{'L':400.0,'T':400.0},
					}
			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'T':[0.3093,1.0]}
			if self.era=="2018":
				cutranges['btagDeepFlavB__B']={'T':[0.2770,1.0]}

					

			self.LoadCuts =  	{
						'C':	 	{
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'pt__B':cutranges['pt__B']['T']
								},
						
						'CP':	 	{
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'pt__B':cutranges['pt__B']['T']
								},
						
						'CF':	 	{
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'pt__B':cutranges['pt__B']['T']
								}


						}




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



		if anatype=="Bstar":
			self.labels = ["W","T","TW"]
			self.ak8labels = ["W","T"]
			self.ak4labels = []
			self.candl = "T"
			self.probl = "W"
			cutranges = 	{
					'iMDW__W':{'L':[0.0,0.5],'M':[0.5,0.9],'T':[0.9,1.0]},

					'msoftdrop__W':{'L':[5.0,30.0],'M':[65.0,105.0],'T':[65.0,105.0]},
					'iMDtop__T':{'L':[0.0,0.5],'M':[0.5,0.9],'T':[0.9,1.0]},
					'msoftdropdef__T':{'L':[30.0,65.0],'M':[140.0,220.0],'T':[140.0,220.0]},
					'ptAK8__T':{'L':500.0,'M':500.0,'T':500.0},
					'ptAK8__W':{'L':500.0,'M':500.0,'T':500.0},
					}
			self.LoadCuts =  	{
						'A':		{
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},
						'B':		{
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},
						'C':	 	{
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},
						'D':		{
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},

						'E':	 	{
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},


						'F':	 	{
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},
						'G':		{
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},




						'H':	 	{
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},
						'I':		{
								'iMDW__W':cutranges['iMDW__W']['M'],
								'msoftdrop__W':cutranges['msoftdrop__W']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},


						'J':		{
								'iMDW__W':cutranges['iMDW__W']['L'],
								'msoftdrop__W':cutranges['msoftdrop__W']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},

						'K':	 	{
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},
						'L':		{
								'iMDW__W':cutranges['iMDW__W']['T'],
								'msoftdrop__W':cutranges['msoftdrop__W']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
								},



						'All':	  	{
								'iMDW__W':[0.0,1.0],
								'msoftdrop__W':[0.0,float("inf")],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__W':cutranges['ptAK8__W']['T'],
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
					'btagHbb__H':{'L':[-1.0,0.0],'M':[0.0,0.6],'T':[0.6,1.0],'F':[-1.0,1.0],'C1':[0.3,1.0],'C2':[0.8,1.0],'C3':[0.9,1.0]},
					'msoftdrop__H':{'L':[5.0,30.0],'M':[105.0,140.0],'T':[105.0,140.0],'F':[130.0,250.0]},
					#'msoftdrop__H':{'L':[10.0,30.0],'M':[65.0,140.0],'T':[65.0,140.0],'F':[130.0,250.0]},
					'iMDtop__H':{'L':[0.0,0.95],'M':[0.0,0.95],'T':[0.0,0.95],'F':[0.9,1.0],'C1':[0.0,0.90],'C2':[0.0,0.99]},
					'iMDtop__T':{'L':[0.0,0.3],'M':[0.3,0.9],'T':[0.9,1.0],'BT':[0.9,1.0],'C1':[0.8,1.0],'C2':[0.85,1.0],'C3':[0.95,1.0]},
					'msoftdropdef__T':{'L':[30.0,65.0],'M':[140.0,220.0],'T':[140.0,220.0],'BT':[65.0,105.0]},
					'btagDeepFlavB__B':{'L':[-1.0,0.3033],'M':[0.3033,1.0],'T':[0.3033,1.0],'F':[-1.0,0.3033],'C1':[0.0521,1.0],'C2':[0.7489,1.0]},
					'pt__B':{'L':200.0,'M':200.0,'T':200.0,'F':100.0},
					'ptAK8__T':{'L':400.0,'M':400.0,'T':400.0,'F':400.0},
					'ptAK8__H':{'L':400.0,'M':400.0,'T':400.0,'F':400.0},
					}
			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.3093],'M':[0.3093,1.0],'T':[0.3093,1.0],'F':[-1.0,0.3093],'C1':[0.0614,1.0],'C2':[0.7221,1.0]}
			if self.era=="2018":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.2770],'M':[0.2770,1.0],'T':[0.2770,1.0],'F':[-1.0,0.2770],'C1':[0.0494,1.0],'C2':[0.7264,1.0]}

			self.LoadCuts =  	{



						'A':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'B':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'ZB':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['BT'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['BT'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'C':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'ZC':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['BT'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['BT'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'D':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'ZD':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},

						'CH':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								'maxvlq__THB':[1500.0,float("inf")],
								},
						'DH':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								'maxvlq__THB':[1500.0,float("inf")],
								},

						'CL':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								'maxvlq__THB':[0.0,1500.],
								},
						'DL':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								'maxvlq__THB':[0.0,1500.],
								},


						'E':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'F':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['M'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M'],
								'iMDtop__H':cutranges['iMDtop__H']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'G':		{
								'btagHbb__H':cutranges['btagHbb__H']['M'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M'],
								'iMDtop__H':cutranges['iMDtop__H']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},


						'H':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['M'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M'],
								'iMDtop__H':cutranges['iMDtop__H']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'I':		{
								'btagHbb__H':cutranges['btagHbb__H']['M'],
								'msoftdrop__H':cutranges['msoftdrop__H']['M'],
								'iMDtop__H':cutranges['iMDtop__H']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},


						'J':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'K':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'L':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},

						'M':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'N':	 	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'O':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},



						'Z':		{
								'btagHbb__H':cutranges['btagHbb__H']['L'],
								'msoftdrop__H':cutranges['msoftdrop__H']['L'],
								'iMDtop__H':cutranges['iMDtop__H']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},


						'FT':		{
								'btagHbb__H':cutranges['btagHbb__H']['F'],
								'msoftdropdef__H':cutranges['msoftdrop__H']['F'],
								'iMDtop__H':cutranges['iMDtop__H']['F'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['F'],
								'pt__B':cutranges['pt__B']['F'],
								'ptAK8__T':cutranges['ptAK8__T']['F'],
								'ptAK8__H':cutranges['ptAK8__H']['F'],
								},

						'FTR':		{
								'btagHbb__H':cutranges['btagHbb__H']['F'],
								'msoftdropdef__H':cutranges['msoftdrop__H']['F'],
								'iMDtop__H':cutranges['iMDtop__H']['F'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['F'],
								'pt__B':cutranges['pt__B']['F'],
								'ptAK8__T':cutranges['ptAK8__T']['F'],
								'ptAK8__H':cutranges['ptAK8__H']['F'],
								},

						'NM1Tmsoftdropdef':		{
								'btagHbb__H':[-1.0,1.0],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__H':[0.0,1.0],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'NM1TiMDtop':		{
								'btagHbb__H':[-1.0,1.0],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__H':[0.0,1.0],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'NM1HbtagHbb':		{
								'btagHbb__H':[-1.0,1.0],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'NM1Hmsoftdrop':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'NM1BbtagDeepFlavB':		{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__H':cutranges['iMDtop__H']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'NM2bt':	{
								'btagHbb__H':cutranges['btagHbb__H']['T'],
								'msoftdrop__H':cutranges['msoftdrop__H']['T'],
								'iMDtop__H':[0.0,1.0],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},
						'All':		{
								'btagHbb__H':[-1.0,1.0],
								'msoftdrop__H':[0.0,float("inf")],
								'iMDtop__H':[0.0,float("inf")],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__H':cutranges['ptAK8__H']['T'],
								},


						}
			self.LoadCuts['DFM'] =  copy.deepcopy(self.LoadCuts['D'])

			self.LoadCuts['CFD'] =  copy.deepcopy(self.LoadCuts['C'])

			self.LoadCuts['CFH1'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFH1']['btagHbb__H']=cutranges['btagHbb__H']['C1']

			self.LoadCuts['CFH2'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFH2']['btagHbb__H']=cutranges['btagHbb__H']['C2']

			self.LoadCuts['CFH3'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFH3']['btagHbb__H']=cutranges['btagHbb__H']['C3']

			self.LoadCuts['CFT1'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFT1']['iMDtop__T']=cutranges['iMDtop__T']['C1']

			self.LoadCuts['CFT2'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFT2']['iMDtop__T']=cutranges['iMDtop__T']['C2']

			self.LoadCuts['CFT3'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFT3']['iMDtop__T']=cutranges['iMDtop__T']['C3']

			self.LoadCuts['CFB1'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFB1']['btagDeepFlavB__B']=cutranges['btagDeepFlavB__B']['C1']

			self.LoadCuts['CFB2'] =  copy.deepcopy(self.LoadCuts['C'])
			self.LoadCuts['CFB2']['btagDeepFlavB__B']=cutranges['btagDeepFlavB__B']['C2']


			self.LoadCuts['HFD'] =  copy.deepcopy(self.LoadCuts['H'])

			self.LoadCuts['HFH1'] =  copy.deepcopy(self.LoadCuts['CFH1'])
			self.LoadCuts['HFH1']['btagHbb__H']=[0.2,cutranges['btagHbb__H']['C1'][0]]

			self.LoadCuts['HFH2'] =  copy.deepcopy(self.LoadCuts['CFH2'])
			self.LoadCuts['HFH2']['btagHbb__H']=[0.3,cutranges['btagHbb__H']['C2'][0]]

			self.LoadCuts['HFH3'] =  copy.deepcopy(self.LoadCuts['CFH3'])
			self.LoadCuts['HFH3']['btagHbb__H']=[0.3,cutranges['btagHbb__H']['C3'][0]]

			self.LoadCuts['KFD'] =  copy.deepcopy(self.LoadCuts['K'])

			self.LoadCuts['KFT1'] =  copy.deepcopy(self.LoadCuts['CFT1'])
			self.LoadCuts['KFT1']['iMDtop__T']=[0.6,cutranges['iMDtop__T']['C1'][0]]

			self.LoadCuts['KFT2'] =  copy.deepcopy(self.LoadCuts['CFT2'])
			self.LoadCuts['KFT2']['iMDtop__T']=[0.6,cutranges['iMDtop__T']['C2'][0]]

			self.LoadCuts['KFT3'] =  copy.deepcopy(self.LoadCuts['CFT3'])
			self.LoadCuts['KFT3']['iMDtop__T']=[0.6,cutranges['iMDtop__T']['C3'][0]]





		elif anatype=="tZb":
			self.labels = ["Z","T","B","TZB","TZ","BZ","BT"]
			self.ak8labels = ["Z","T"]
			self.ak4labels = ["B"]
			self.candl = "T"
			self.probl = "Z"

			cutranges = 	{
					#'btagHbb__Z':{'L':[-1.0,0.6],'M':[-1.0,0.6],'T':[-1.0,0.6]},
					'btagHbb__Z':{'L':[-1.0,1.0],'M':[-1.0,1.0],'T':[-1.0,1.0]},
					'tau21__Z':{'L':[0.6,1.0],'M':[0.45,0.6],'T':[0.0,0.45]},
					'msoftdrop__Z':{'L':[5.0,30.0],'M':[65.0,105.0],'T':[65.0,105.0]},
					'iMDtop__Z':{'L':[0.0,1.0],'M':[0.0,1.0],'T':[0.0,1.0],'C1':[0.0,0.90],'C2':[0.0,0.99]},
					#'msoftdrop__Z':{'L':[10.0,30.0],'M':[65.0,140.0],'T':[65.0,140.0]},
					'iMDtop__T':{'L':[0.0,0.3],'M':[0.3,0.9],'T':[0.9,1.0],'BT':[0.9,1.0],'C1':[0.8,1.0],'C2':[0.85,1.0],'C3':[0.95,1.0]},
					'msoftdropdef__T':{'L':[30.0,65.0],'M':[140.0,220.0],'T':[140.0,220.0],'BT':[105.0,140.0]},
					'btagDeepFlavB__B':{'L':[-1.0,0.3033],'M':[0.3033,1.0],'T':[0.3033,1.0],'F':[-1.0,0.3033],'C1':[0.0521,1.0],'C2':[0.7489,1.0]},
					'pt__B':{'L':200.0,'M':200.0,'T':200.0,'F':100.0},
					'ptAK8__T':{'L':400.0,'M':400.0,'T':400.0},
					'ptAK8__Z':{'L':400.0,'M':400.0,'T':400.0},
					}

			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.3093],'M':[0.3093,1.0],'T':[0.3093,1.0],'F':[-1.0,0.3093],'C1':[0.0614,1.0],'C2':[0.7221,1.0]}
				cutranges['tau21__Z']={'L':[0.6,1.0],'M':[0.4,0.6],'T':[0.0,0.4]}
			if self.era=="2018":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.2770],'M':[0.2770,1.0],'T':[0.2770,1.0],'F':[-1.0,0.2770],'C1':[0.0494,1.0],'C2':[0.7264,1.0]}
			self.LoadCuts =  	{


						'A':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'B':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},

						'ZB':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['BT'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['BT'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},



						'C':	 	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},


						'ZC':	 	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['BT'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['BT'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},

						'D':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},

						'ZD':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},









						'CH':	 	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								'maxvlq__TZB':[1500.0,float("inf")],
								},
						'DH':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								'maxvlq__TZB':[1500.0,float("inf")],
								},








						'CL':	 	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								'maxvlq__TZB':[0.0,1500.0],
								},
						'DL':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								'maxvlq__TZB':[0.0,1500.0],
								},









						'E':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'F':	 	{
								'tau21__Z':cutranges['tau21__Z']['M'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['M'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M'],
								'iMDtop__Z':cutranges['iMDtop__Z']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'G':		{
								'tau21__Z':cutranges['tau21__Z']['M'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['M'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M'],
								'iMDtop__Z':cutranges['iMDtop__Z']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},


						'H':	 	{
								'tau21__Z':cutranges['tau21__Z']['M'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['M'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M'],
								'iMDtop__Z':cutranges['iMDtop__Z']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'I':		{
								'tau21__Z':cutranges['tau21__Z']['M'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['M'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['M'],
								'iMDtop__Z':cutranges['iMDtop__Z']['M'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},


						'J':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'K':	 	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['M'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['M'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'L':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},


						'M':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'N':	 	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'O':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},


						'Z':		{
								'tau21__Z':cutranges['tau21__Z']['L'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['L'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['L'],
								'iMDtop__Z':cutranges['iMDtop__Z']['L'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},


						'NM1Tmsoftdropdef':{
								'tau21__Z':[-1.0,1.0],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__Z':[0.0,1.0],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'NM1TiMDtop':{
								'tau21__Z':[-1.0,1.0],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__Z':[0.0,1.0],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':cutranges['msoftdropdef__T']['T'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'NM1Ztau21':		{
								'tau21__Z':[-1.0,1.0],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'NM1Zmsoftdrop':		{
								'tau21__Z':cutranges['tau21__Z']['T'],
								#'btagHbb__Z':cutranges['btagHbb__Z']['T'],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'NM1BbtagDeepFlavB':{
								'tau21__Z':[-1.0,1.0],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],
								'iMDtop__T':cutranges['iMDtop__T']['T'],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},





						'NM2bt':	{
								'tau21__Z':cutranges['tau21__Z']['T'],
								'msoftdrop__Z':cutranges['msoftdrop__Z']['T'],
								'iMDtop__Z':cutranges['iMDtop__Z']['T'],								'tau21__Z':cutranges['tau21__Z']['T'],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						'All':		{
								'tau21__Z':[-1.0,1.0],
								#'btagHbb__Z':[-1.0,1.0],
								'msoftdrop__Z':[0.0,float("inf")],
								'iMDtop__Z':[0.0,1.0],
								'iMDtop__T':[0.0,1.0],
								'msoftdropdef__T':[0.0,float("inf")],
								'btagDeepFlavB__B':[-2.0,2.0],
								'pt__B':cutranges['pt__B']['T'],
								'ptAK8__T':cutranges['ptAK8__T']['T'],
								'ptAK8__Z':cutranges['ptAK8__Z']['T'],
								},
						}
			self.LoadCuts['DFM'] =  copy.deepcopy(self.LoadCuts['D'])

	def SetRunTrigs(self,runver):


		if self.era=="2017":
			self.eletrigs=["HLT_Ele35_WPTight_Gsf","HLT_Ele32_WPTight_Gsf_L1DoubleEG","HLT_Ele115_CaloIdVT_GsfTrkIdT","HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165","HLT_Photon200"]
			self.mutrigs = ["HLT_IsoMu27","HLT_Mu50"]
		if self.era=="2018":
			self.eletrigs=["HLT_Ele32_WPTight_Gsf","HLT_Ele115_CaloIdVT_GsfTrkIdT","HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165"]
			self.mutrigs = ["HLT_IsoMu24","HLT_Mu50"]
		if self.era=="2017" or self.era=="2018":



			self.ptrigs = ["HLT_PFHT780"]
			self.strigs = ["HLT_PFHT1050","HLT_PFJet500","HLT_PFJet550","HLT_AK8PFJet500","HLT_AK8PFJet550"]
			self.etrigs = ["HLT_AK8PFJet400_TrimMass30","HLT_AK8PFJet420_TrimMass30","HLT_AK8PFHT800_TrimMass50","HLT_AK8PFHT850_TrimMass50","HLT_AK8PFHT900_TrimMass50"]

		if self.era=="2016":
			self.eletrigs=["HLT_Ele27_WPTight_Gsf","HLT_Ele115_CaloIdVT_GsfTrkIdT","HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165","HLT_Photon175"]
			self.mutrigs = ["HLT_IsoTkMu24","HLT_IsoMu24","HLT_Mu50","HLT_TkMu50"]

			self.ptrigs = ["HLT_PFHT650"]
			self.strigs = ["HLT_PFHT900","HLT_PFHT800","HLT_PFJet450","HLT_PFJet500","HLT_AK8PFJet450","HLT_AK8PFJet500"]
			self.etrigs = ["HLT_AK8PFHT700_TrimR0p1PT0p03Mass50","HLT_AK8PFHT650_TrimR0p1PT0p03Mass50","HLT_AK8PFJet360_TrimMass30"]

		if runver=="Run2017B":
			self.etrigs = []
			self.eletrigs = ["HLT_Ele35_WPTight_Gsf","HLT_Photon200"]
		if runver=="Run2016H":
			self.strigs = ["HLT_PFHT900","HLT_PFJet450","HLT_PFJet500","HLT_AK8PFJet450","HLT_AK8PFJet500"]
		if runver=="NONE":
			self.ptrigs = []
			self.strigs = []
			self.etrigs = []

	def LoadFiles(self,setname="QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",folder="/eos/cms/store/user/knash",redir="eoscms.cern.ch",search="",rdf=False):


		files = []

		#Miniaod version string 
		rvsearch = self.runver
		'''
		print self.ovrvec
		if setname in self.ovrvec:
			print setname
			if self.era=="2016":	
				rvsearch="RunIIFall17MiniAOD"
			if self.era=="2017":	
				rvsearch="RunIIAutumn18MiniAOD"
			if self.era=="2018":	
				rvsearch="RunIIFall17MiniAOD"

		print rvsearch
		'''
		#Nanoaodskim version string 
		versionstring=self.versionstring

		#Another search string
		nanotype=self.nanotype

		setnametowrite=setname.replace("/","_").replace("*","")

		ntry=0
		while len(files)==0:

				#Find all possible files in eos and save in txt
				tempfname="tempfiles"+setnametowrite+self.era+".txt"
				spcall = "eos root://"+redir+" find  "+folder+"/"+setname+" > "+tempfname
				print spcall
				subprocess.call( [spcall], shell=True )
				files = []

				#Loop through files and filter only the ones we want
				with open(tempfname) as ftemp:
					filestemp = ftemp.read().splitlines()
					verfs={}
					for curfile in filestemp:
						verfind=False
						#Some sets can be one of a few versions -- check double counting 

						for vv in versionstring:
							#print curfile,vv
							if curfile.find(vv)!=-1:
								verfind=True

						#For finding nano or roodataframe (not sure if still used...)
						if not rdf:
							#print curfile
							#print curfile.find(".root")!=-1 , verfind , curfile.find(nanotype)!=-1 , curfile.find("failed")==-1 , curfile.find(search)!=-1
							fileBool=curfile.find(".root")!=-1 and verfind and curfile.find(nanotype)!=-1 and curfile.find("failed")==-1 and curfile.find(search)!=-1
							if not self.isdata:
								fileBool = fileBool and curfile.find(rvsearch)!=-1 
						else:
							fileBool=curfile.find(".root")!=-1 and curfile.find("failed")==-1 and curfile.find(search)!=-1 and curfile.find("_"+self.era+"__")!=-1
						#print curfile,versionstring
						#print curfile.find(".root")!=-1 , verfind , curfile.find(nanotype)!=-1 , curfile.find("failed")==-1 , curfile.find(search)!=-1,curfile.find(rvsearch)
						if fileBool:
							#access w/xrootd
							for vv in versionstring:
								if curfile.find(vv)!=-1:
									#print vv
									if not (vv in verfs):
										verfs[vv]=0
									verfs[vv]+=1
							if redir=="eoscms.cern.ch":
								files.append(curfile.replace("/eos/cms/","root://"+redir+":///"))
							else:
								files.append(curfile.replace("/eos/uscms/","root://"+redir+":///"))
					if len(verfs)>1:
						
						logging.error("MULTIVERSION!")
						print files
				subprocess.call( ["rm "+tempfname], shell=True )

				#Eliminate double counting (should not happen)
				if len(files) != len(set(files)):
					logging.error("Duplicate Files")
				files = list(set(files))

				if len(files)==0:
					ntry+=1
					logging.error("No Files Found For "+setname)
					time.sleep(2)

				if ntry>10:
					logging.error("Too Many Tries")
					sys.exit()

		#Return alphabetically sorted files 
		files.sort()
		return files


	def InitCorr(self,filename):
		print filename
		index = filename.find("JetHT/Run")
		#super hacky parsing, assume RunXXXXY for year,run
		year,run=str(filename[index+9:index+13]),str(filename[index+13:index+14])
		print year,run
		print dir(createJMECorrector((not self.isdata), year, run, "Total", True, "AK8PFPuppi", True))
		print createJMECorrector((not self.isdata), year, run, "Total", True, "AK8PFPuppi", True)
		self.jmeCorrections = createJMECorrector((not self.isdata), year, run, "Total", True, "AK8PFPuppi", True)

	def HistosMatchInit(self,labels,regions=['C']):
		histos = {}
		for region in regions:
			histos[region] = {}
			for label in labels:
				histos[region]["tau21__"+label+"__"+region] =  TH1F("tau21__"+label+"__"+region,	"tau21__"+label+"__"+region,		10000, 0.,1.01 )
				histos[region]["iMDW__"+label+"__"+region] =  TH1F("iMDW__"+label+"__"+region,	"iMDW__"+label+"__"+region,		10000, 0.,1. )
				histos[region]["tau41__"+label+"__"+region] =  TH1F("tau41__"+label+"__"+region,	"tau41__"+label+"__"+region,		10000, 0.,1.01 )
				histos[region]["iMDWW__"+label+"__"+region] =  TH1F("iMDWW__"+label+"__"+region,	"iMDWW__"+label+"__"+region,		10000, 0.,1.01 )
		return histos




	def ExpandGeneric(self,ev,name,maxlen=-1,ptcut=30.0):

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
			objvec.append(ObjectType(name))

			objvec[-1].pt = float(curpt)
			objvec[-1].upt = float(curpt)
			objvec[-1].eta = float(getattr(ev, name+"_eta")[iobj])
			objvec[-1].phi = float(getattr(ev, name+"_phi")[iobj])
			objvec[-1].mass = float(getattr(ev, name+"_mass")[iobj])
			objvec[-1].umass = float(getattr(ev, name+"_mass")[iobj])
			if name=="CustomAK8Puppi":
				objvec[-1].jetId=int(getattr(ev, name+"_jetId")[iobj])
				objvec[-1].iMDPho=float(getattr(ev, name+"_iMDPho")[iobj])
				objvec[-1].iMDWW=float(getattr(ev, name+"_iMDWW")[iobj])
				objvec[-1].iMDtop=float(getattr(ev, name+"_iMDtop")[iobj])
				objvec[-1].iW=float(getattr(ev, name+"_iW")[iobj])
				objvec[-1].iMDW=float(getattr(ev, name+"_iMDW")[iobj])
				objvec[-1].iMDtop=float(getattr(ev, name+"_iMDtop")[iobj])
				objvec[-1].msoftdrop=float(getattr(ev, name+"_msoftdrop")[iobj])
				objvec[-1].msoftdropdef=float(getattr(ev, name+"_msoftdrop")[iobj])
				objvec[-1].umsoftdrop=float(getattr(ev, name+"_msoftdrop")[iobj])
				objvec[-1].tau1=float(getattr(ev, name+"_tau1")[iobj])
				objvec[-1].tau2=float(getattr(ev, name+"_tau2")[iobj])
				if objvec[-1].tau1>0.0:
					objvec[-1].tau21=objvec[-1].tau2/objvec[-1].tau1
				else:
					objvec[-1].tau21=1.0
				objvec[-1].btagHbb=float(getattr(ev, name+"_btagHbb")[iobj])
				objvec[-1].rawFactor=float(getattr(ev, name+"_rawFactor")[iobj])
				objvec[-1].area=float(getattr(ev, name+"_area")[iobj])
				objvec[-1].subJetIdx1=int(getattr(ev, name+"_subJetIdx1")[iobj])
				objvec[-1].subJetIdx2=int(getattr(ev, name+"_subJetIdx2")[iobj])
			if name=="CustomAK8PuppiSubJet":
				objvec[-1].rawFactor=float(getattr(ev, name+"_rawFactor")[iobj])
				objvec[-1].area=float(getattr(ev, name+"_area")[iobj])

			if name=="Jet":
				objvec[-1].jetId=int(getattr(ev, name+"_jetId")[iobj])
				objvec[-1].btagDeepFlavB=float(getattr(ev, name+"_btagDeepFlavB")[iobj])
				objvec[-1].btagCSVV2=float(getattr(ev, name+"_btagCSVV2")[iobj])
				objvec[-1].rawFactor=float(getattr(ev, name+"_rawFactor")[iobj])
				objvec[-1].area=float(getattr(ev, name+"_area")[iobj])
				#print objvec[-1].jetId
			if name=="Muon":
				#print getattr(ev, name+"_highPtId")[iobj]
				#print float(getattr(ev, name+"_highPtId")[iobj])
				#objvec[-1].mediumId=bool(getattr(ev, name+"_mediumId")[iobj])
				objvec[-1].tightId=bool(getattr(ev, name+"_tightId")[iobj])
				objvec[-1].pfIsoId=ord(getattr(ev, name+"_pfIsoId")[iobj])
				objvec[-1].mediumId=bool(getattr(ev, name+"_mediumId")[iobj])
				objvec[-1].miniPFRelIso_all=float(getattr(ev, name+"_miniPFRelIso_all")[iobj])
				#print "MEDID",objvec[-1].mediumId
				#objvec[-1].mvaId=getattr(ev, name+"_mvaId")[iobj]
			if name=="Electron":
				objvec[-1].mvaFall17V2Iso_WP90=int(getattr(ev, name+"_mvaFall17V2Iso_WP90")[iobj])
				objvec[-1].mvaFall17V2noIso_WP90=int(getattr(ev, name+"_mvaFall17V2noIso_WP90")[iobj])
				objvec[-1].mvaFall17V2Iso_WP80=int(getattr(ev, name+"_mvaFall17V2Iso_WP80")[iobj])
				objvec[-1].mvaFall17V2noIso_WP80=int(getattr(ev, name+"_mvaFall17V2noIso_WP80")[iobj])
			if name=="GenPart":
				objvec[-1].pdgId=int(getattr(ev, name+"_pdgId")[iobj])
				objvec[-1].statusFlags=int(getattr(ev, name+"_statusFlags")[iobj])
				objvec[-1].genPartIdxMother=int(getattr(ev, name+"_genPartIdxMother")[iobj])
			if name=="GenJet":
				objvec[-1].hadronFlavour=int(ord(getattr(ev, name+"_hadronFlavour")[iobj]))

			#objvec[-1].p4.SetPtEtaPhiM(objvec[-1].pt,objvec[-1].eta,objvec[-1].phi,objvec[-1].mass)
			objvec[-1].setp4()
		return objvec

	def WeightsHistosInit(self,weightstoplot,regions=['C']):
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
	def HistosInit(self,labels,regions=['C']):
		histos = {}
		#hacky
		AK4labs=["B"]
		for region in regions:
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

				#Single-Object Labels
				if len(label)==1:
					histos[region]["mass__"+label+"__"+region] =  TH1F("mass__"+label+"__"+region,	"mass__"+label+"__"+region,		250, 0.,500.  )
					histos[region]["index__"+label+"__"+region] =  TH1F("index__"+label+"__"+region,	"index__"+label+"__"+region,		4, -.5,3.5  )
					if not isAK4:
						histos[region]["msoftdrop__"+label+"__"+region] =  TH1F("msoftdrop__"+label+"__"+region,	"msoftdrop__"+label+"__"+region,		240, 0.,480. )
						histos[region]["msoftdropdef__"+label+"__"+region] =  TH1F("msoftdropdef__"+label+"__"+region,	"msoftdrop__"+label+"__"+region,		240, 0.,480. )
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
						if self.anatype in ["Mu","Ele"]:
							histos[region]["msoftdropdef__"+label+"__iMDtop__"+label+"__pt__"+label+"__"+region] =  TH3F("msoftdropdef__"+label+"__iMDtop__"+label+"__pt__"+label+"__"+region,"msoftdropdef__"+label+"__iMDtop__"+label+"__pt__"+label+"__"+region,60, 0, 300.,200, 0, 1.,75, 400., 1900.)
						if self.anatype=="tHb":
							histos[region]["iMDtop__"+label+"__"+region] =  TH1F("iMDtop__"+label+"__"+region,	"iMDtop__"+label+"__"+region,		5000, 0.,1. )
							histos[region]["btagHbb__"+label+"__"+region] =  TH1F("btagHbb__"+label+"__"+region,	"btagHbb__"+label+"__"+region,		100, -1.,1. )
						if self.anatype=="tZb":
							histos[region]["iMDtop__"+label+"__"+region] =  TH1F("iMDtop__"+label+"__"+region,	"iMDtop__"+label+"__"+region,		5000, 0.,1. )
							histos[region]["tau21__"+label+"__"+region] =  TH1F("tau21__"+label+"__"+region,	"tau21__"+label+"__"+region,		100, 0.,1. )
					else:
						histos[region]["btagDeepFlavB__"+label+"__"+region] =  TH1F("btagDeepFlavB__"+label+"__"+region,	"btagDeepFlavB__"+label+"__"+region,		100, 0.,1. )

				#Multi-Object Labels
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
							histos[region]["aeta__"+label[1]+"__aeta__"+label[0]+"__"+region] =  TH2F("aeta__"+label[1]+"__aeta__"+label[0]+"__"+region,	"aeta__"+label[1]+"__aeta__"+label[0]+"__"+region,		24, 0.0,2.4,24, 0.0,2.4 )
							#histos[region]["mass__"+label+"__"+region] =  TH1F("mass__"+label+"__"+region,	"mass__"+label+"__"+region,		800, 0.,8000. )
					if self.anatype=="tZb":
							histos[region]["tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		240, 0.,480.,100, 0.,1. )
							histos[region]["aeta__"+label[1]+"__aeta__"+label[0]+"__"+region] =  TH2F("aeta__"+label[1]+"__aeta__"+label[0]+"__"+region,	"aeta__"+label[1]+"__aeta__"+label[0]+"__"+region,		24, 0.0,2.4,24, 0.0,2.4 )
							#histos[region]["mass__"+label+"__"+region] =  TH1F("mass__"+label+"__"+region,	"mass__"+label+"__"+region,		800, 0.,8000. )

				if not isAK4:
					histos[region]["pt__"+label+"__aeta__"+label+"__"+region] =  TH2F("pt__"+label+"__aeta__"+label+"__"+region,	"pt__"+label+"__aeta__"+label+"__"+region,		350, 400.,3900.,24, 0.0,2.4 )
				else:
					histos[region]["pt__"+label+"__aeta__"+label+"__"+region] =  TH2F("pt__"+label+"__aeta__"+label+"__"+region,	"pt__"+label+"__aeta__"+label+"__"+region,		350, 0.,3500.,24, 0.0,2.4 )


		for region in regions:
			for histo in histos[region]:
				histos[region][histo].Sumw2()
		return histos


	def WeightsHistosFill(self,weightshistos,weightdict,region):
		if not (region in weightshistos):
			return
		for whisto in weightdict[region]:
			for vari in weightdict[region][whisto]:
				if (whisto+vari) in weightshistos[region]:
					weightshistos[region][whisto+vari].Fill(weightdict[region][whisto][vari])

	def HistosFill(self,histos,cands,region='C',weight=1.0,hfilter=[]):
		#print "rr",region
		#print histos
		#print region
		#print histos
			
		#print region,histos[region]
		if not (region in histos):
			return
		for histo in histos[region]:
			#if region=="C":
			#	print histo
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
			if isinstance(histos[region][histo], TH3F):
				#print cands[idval[1]] , cands[idval[3]] , cands[idval[5]]
				if cands[idval[1]]!=None and cands[idval[3]]!=None and cands[idval[5]]!=None:
					if cands[idval[1]][idval[0]]!=None and cands[idval[3]][idval[2]]!=None and cands[idval[5]][idval[4]]!=None:
						#print "filling",histo,cands[idval[1]][idval[0]],cands[idval[3]][idval[2]],cands[idval[5]][idval[4]]
						histos[region][histo].Fill(cands[idval[1]][idval[0]],cands[idval[3]][idval[2]],cands[idval[5]][idval[4]],weight)
			elif isinstance(histos[region][histo], TH2F):
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

	def OverlapCheck(self,histos,cands,region,matchmatrix):
		for histo in histos[region]:
			if [region,histo] in matchmatrix:
				logging.error("Multiple histogram fills")
				sys.exit()
			else:
				matchmatrix.append([region,histo])
	def TagJet(self,ak8jet,obj,region='C'):
		#print "Jetid",ak8jet.jetId
		if ak8jet.jetId<2:
			return False
		curcuts = self.LoadCuts[region]

		if obj=="W":
			#if region=="C":
			#	if curcuts["msoftdrop__W"][0]<ak8jet["msoftdrop"]<curcuts["msoftdrop__W"][1]:
			#		print region,ak8jet["iMDW"],ak8jet["iMDW"],ak8jet["msoftdrop"]
			if curcuts["iMDW__W"][0]<ak8jet.iMDW<=curcuts["iMDW__W"][1] :
				if curcuts["msoftdrop__W"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__W"][1]:
					return True

		if obj=="H":
			if "msoftdropdef__H" in curcuts:
				sdbool=(curcuts["msoftdropdef__H"][0]<ak8jet.msoftdropdef<=curcuts["msoftdropdef__H"][1])
			else:
				sdbool=(curcuts["msoftdrop__H"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__H"][1])
			if curcuts["btagHbb__H"][0]<ak8jet.btagHbb<=curcuts["btagHbb__H"][1] and sdbool:
				if "iMDtop__H" in curcuts:
					if curcuts["iMDtop__H"][0]<ak8jet.iMDtop<=curcuts["iMDtop__H"][1]:
						return True
				else:
					return True
		if obj=="Z":
			if curcuts["tau21__Z"][0]<ak8jet.tau21<=curcuts["tau21__Z"][1] and (curcuts["msoftdrop__Z"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__Z"][1]):
				#if "btagHbb__Z" in curcuts:
				#	if curcuts["btagHbb__Z"][0]<ak8jet.btagHbb<=curcuts["btagHbb__Z"][1]:
				#		return True
				#else:
				#	return True

				if "iMDtop__Z" in curcuts:
					if curcuts["iMDtop__Z"][0]<ak8jet.iMDtop<=curcuts["iMDtop__Z"][1]:
						return True
				else:
					return True


		if obj=="T":
			if (curcuts["iMDtop__T"][0]<ak8jet.iMDtop<=curcuts["iMDtop__T"][1]) and (curcuts["msoftdropdef__T"][0]<ak8jet.msoftdropdef<=curcuts["msoftdropdef__T"][1]):
					return True
				#if self.anatype=="tHb":
				#	if not (curcuts["_btagHbb__T"][0]<ak8jet["btagHbb"]<=curcuts["Inv_btagHbb__T"][1] and (curcuts["Inv_msoftdropdef__T"][0]<ak8jet["msoftdrop"]<=curcuts["Inv_msoftdropdef__T"][1])):
				#		return True
				#elif self.anatype=="Bstar":
				#	#if not( curcuts["Inv_tau21__T"][0]<ak8jet["tau21"]<curcuts["Inv_tau21__T"][1] and (curcuts["Inv_msoftdropdef__T"][0]<ak8jet["msoftdrop"]<curcuts["Inv_msoftdropdef__T"][1])):
				#	return True
				#else:
				#	return True



		if obj=="A":
			if (curcuts["iMDtop__A"][0]<ak8jet.iMDtop<=curcuts["iMDtop__A"][1]) and (curcuts["msoftdrop__A"][0]<ak8jet.msoftdrop<=curcuts["msoftdrop__A"][1]):
					return True
		if obj=="B":
			if "btagDeepFlavB__B" in curcuts:
				if curcuts["btagDeepFlavB__B"][0]<ak8jet.btagDeepFlavB<=curcuts["btagDeepFlavB__B"][1]:
					return True
			if "btagCSVV2__B" in curcuts:
				if curcuts["btagCSVV2__B"][0]<ak8jet.btagCSVV2<=curcuts["btagCSVV2__B"][1]:
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

	#Does the event pass MET filters
	def FilterPass(self,ev):
		efiltarr=[] 

		efiltarr.append(int(getattr(ev, "Flag_goodVertices")))
		efiltarr.append(int(getattr(ev, "Flag_globalSuperTightHalo2016Filter")))
		efiltarr.append(int(getattr(ev, "Flag_HBHENoiseFilter")))
		efiltarr.append(int(getattr(ev, "Flag_HBHENoiseIsoFilter")))
		efiltarr.append(int(getattr(ev, "Flag_EcalDeadCellTriggerPrimitiveFilter")))
		efiltarr.append(int(getattr(ev, "Flag_BadPFMuonFilter")))
		if self.isdata:
			efiltarr.append(int(getattr(ev, "Flag_eeBadScFilter")))
		for ef in efiltarr:
			if ef==0:
				#print efiltarr
				return False

		if int(getattr(ev, "PV_npvsGood"))<1:
			print "NPV FAIL!"
			return False
		#print "True"


		return True

	#Apply Puppi SD mass correction 
	def CorrectSdMass(self,jets,subJets ):

  		genCorr  = 1.
  		recoCorr = 1.
  		totalWeight = 1.
		jets_msoftdrop_raw=[]
		jets_msoftdrop_nom=[]
		jets_groomed_corr_PUPPI=[]
		for ijet,jet in enumerate(jets):
			jets_msoftdrop_raw.append(jet.msoftdrop)
			jets_msoftdrop_nom.append(jet.msoftdrop)
			inds=[jet.subJetIdx1,jet.subJetIdx2]
			if len(subJets)<=inds[0] or len(subJets)<=inds[1]:
				continue
		    	if inds[0]>=0 and inds[1]>=0 :
		        	groomedP4 = subJets[inds[0]].p4*(1 - subJets[inds[0]].rawFactor) + subJets[inds[1]].p4*(1 - subJets[inds[1]].rawFactor)
		        	groomedP4corr = subJets[inds[0]].p4*(1 - subJets[inds[0]].rawFactor) + subJets[inds[1]].p4*(1 - subJets[inds[1]].rawFactor)
		    	else : groomedP4 = None

		    	if groomedP4 != None:
				jets_msoftdrop_raw[ijet] = groomedP4.M()
		    	puppisd_genCorr = self.puppisd_corrGEN.Eval(jet.pt)
		    	if abs(jet.eta) <= 1.3: puppisd_recoCorr = self.puppisd_corrRECO_cen.Eval(jet.pt)
		    	else: puppisd_recoCorr = self.puppisd_corrRECO_for.Eval(jet.pt)

		    	puppisd_total = puppisd_genCorr * puppisd_recoCorr
		    	if groomedP4 != None:
		    		groomedP4.SetPtEtaPhiM(groomedP4.Perp(), groomedP4.Eta(), groomedP4.Phi(), groomedP4.M()*puppisd_total)

		    	jets_groomed_corr_PUPPI.append(puppisd_total)
			if groomedP4 != None :
		    		jets_msoftdrop_nom[ijet] = groomedP4.M()
		return jets_msoftdrop_raw,jets_msoftdrop_nom
	def CorrectSdMassdef(self,jets,subJets ):

		jets_msoftdropdef_nom=[]
	
		for ijet,jet in enumerate(jets):
			jets_msoftdropdef_nom.append(jet.msoftdropdef)
			#print "msd1",jets_msoftdropdef_nom[-1]
			inds=[jet.subJetIdx1,jet.subJetIdx2]
			if len(subJets)<=inds[0] or len(subJets)<=inds[1]:
				continue

		    	if inds[0]>=0 and inds[1]>=0 :
		        	groomedP4corr = subJets[inds[0]].p4+subJets[inds[1]].p4
		    	else : 
				continue
		    	jets_msoftdropdef_nom[ijet] = groomedP4corr.M()
			#print "msd2",jets_msoftdropdef_nom[-1]
		
		return jets_msoftdropdef_nom



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



	def JerSmearstoc(self,jets,rho,jind,jtype="ak8"):
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

		for ak8j in jets:
            		params_sf_and_uncertainty.setJetEta(ak8j.eta)
            		params_sf_and_uncertainty.setJetPt(ak8j.pt) 
			curSF = jerSF_and_Uncertainty.getScaleFactor(params_sf_and_uncertainty, jind)

			#CHECK THIS!!!!
			smearFactor=1.0

			params_resolution.setJetPt(ak8j.pt)
			params_resolution.setJetEta(ak8j.eta)
			params_resolution.setRho(rho)
		  	jet_pt_resolution = jer.getResolution(params_resolution)
			dostoc=False

			jerrand = self.rnd1.Gaus(0,jet_pt_resolution)
			if curSF>1.:
		      		smearFactor = 1. + jerrand * math.sqrt(curSF**2 - 1.)
			if (smearFactor*ak8j.pt) < 1.e-2:
				smearFactor = 1.e-2
			#ak8j.pt = ak8j.pt*smearFactor
			#ak8j.shift = ak8j.shift*smearFactor
			#ak8j.setp4()
			ak8j.setshift(smearFactor)
		return



	def JerSmear(self,jets, genjets,rho,jind,jtype="ak8"):

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

		for ak8j in jets:
            		params_sf_and_uncertainty.setJetEta(ak8j.eta)
            		params_sf_and_uncertainty.setJetPt(ak8j.pt) 
			curSF = jerSF_and_Uncertainty.getScaleFactor(params_sf_and_uncertainty, jind)

			#CHECK THIS!!!!
			smearFactor=1.0

			params_resolution.setJetPt(ak8j.pt)
			params_resolution.setJetEta(ak8j.eta)
			params_resolution.setRho(rho)
		  	jet_pt_resolution = jer.getResolution(params_resolution)
			dostoc=False

			genJet=pairs[ak8j]
			if genJet==None:
				dostoc=True
			if not dostoc:
				dPt = ak8j.pt - genJet.pt
				if abs(dPt)>3.0*ak8j.pt*jet_pt_resolution:
					dostoc=True
			if not dostoc:
				smearFactor = 1. + (curSF - 1.)*dPt/ak8j.pt
			else:
		  		jerrand = self.rnd1.Gaus(0,jet_pt_resolution)
				if curSF>1.:
		      			smearFactor = 1. + jerrand * math.sqrt(curSF**2 - 1.)
			if (smearFactor*ak8j.pt) < 1.e-2:
				smearFactor = 1.e-2
			#ak8j.pt = ak8j.pt*smearFactor
			#ak8j.shift = ak8j.shift*smearFactor
			#ak8j.setp4()
			ak8j.setshift(smearFactor)


	def JesScaleHEM(self,jet):
		hemlumi=0.65
		hemrand=random.random()
		if hemrand>hemlumi:
			return 1.0
		else:
			if (-1.57<jet.phi<-0.87):
				if (-2.5<jet.eta<-1.3):
					return 0.8 
				if (-3.0<jet.eta<-2.5):
					return 0.65
		return 1.0


	def HEMskip(self,jet,run):
		if not self.isdata:
			hemlumi=0.65
			hemrand=random.random()
			if hemrand>hemlumi:
				return False
		else:
			if run<319077:
				return False
		if (-1.57<jet.phi<-0.87):
			if (-2.5<jet.eta<-1.3):
				#print jet,jet.phi,jet.eta,"HEMSKiPlow"
				return True
			if (-3.0<jet.eta<-2.5):
				#print jet,jet.phi,jet.eta,"HEMSKiPhigh"
				return True
		return False


	def JmsScale(self,jets,central_or_shift):
		jmsv=self.jms_vals
		for jet in jets:
			#jet.msoftdrop = jet.msoftdrop*jmsv[central_or_shift]
			jet.setmshift(jmsv[central_or_shift])

	def JmrSmear(self,jets,central_or_shift):
		for jet in jets:
			#Set to W res for now
			jet_m_resolution=10./80.
		  	rand = self.rnd2.Gaus(0,jet_m_resolution)
		    	if self.jet_m_sf_and_uncertainty[central_or_shift] > 1.:
		      		smearFactor = rand * math.sqrt(self.jet_m_sf_and_uncertainty[central_or_shift]**2 - 1.)
		    	else:
		      		smearFactor = 0.
		    	curfac=1.0+smearFactor
			savefac=curfac
	
			#Get rid of extreme outliers 
			#CHECK THIS!!!!
			curfac=min(curfac,self.masssmearlims[1])
			curfac=max(curfac,self.masssmearlims[0])

			if savefac!=curfac:
				print "lim",curfac
			
			#jet.msoftdrop = jet.msoftdrop*max(curfac,0.0)
			jet.setmshift(max(curfac,0.0))

	#Calculate PDF RMS
	def PdfWeight(self,pdfweights):
		avew=sum(pdfweights)/len(pdfweights)
		pdw=0
		for pp in pdfweights:
			pdw+=(pp-avew)*(pp-avew)
		pdw = sqrt(pdw/len(pdfweights))
                #print pdw
		return {"sf":1.0,"down":1.0-pdw,"up":1.0+pdw}

	#Really annoying hessian pdfs
	def PdfWeightHessian(self,pdfweights,opdf):
		#print "HESSIAN"
		avew=sum(pdfweights)/len(pdfweights)
		#print len(pdfweights)
		pdw=0
		origw=opdf
		#print origw,avew
		for ip in xrange(0,len(pdfweights)):
			
			curp=pdfweights[ip]
			pdw+=(curp-origw)*(curp-origw)

		pdwsq = sqrt(pdw)/(origw)
                #print "pdw",pdwsq
		#print len(pdfweights)
		#rare buggy events
   		pdwsq=min(5.0,pdwsq)
		return {"sf":1.0,"down":1.0-pdwsq,"up":1.0+pdwsq}

	#Calculate Q2 Envelope
	def Q2Weight(self,q2weights):

		upweight = max(q2weights)
		downweight = min(q2weights)
		return {"sf":1.0,"down":downweight,"up":upweight}

	#Calculate PS Envelope
	def PSWeight(self,psweights):
		#print
		#for ip,pp in enumerate(psweights):
		#	print ip,pp
		fullweight = list(psweights)+[psweights[0]*psweights[1],psweights[2]*psweights[3],psweights[2]*psweights[1],psweights[0]*psweights[3]]
		#print fullweight
		upweight = max(fullweight)
		downweight = min(fullweight)

		
		#print upweight,downweight

		return {"sf":1.0,"down":downweight,"up":upweight}


	def TopTagSf(self,ak8jet,cut):
		topSFhists = self.topSFhists

		#print topSFhists[0].GetMean(0),topSFhists[0].GetMean(1),topSFhists[0].GetMean(2)

		ptbin=topSFhists[0].FindBin(ak8jet.pt)
		nbins=topSFhists[0].GetNbinsX() 
		upedge=topSFhists[0].GetBinLowEdge(nbins) +  topSFhists[0].GetBinWidth(nbins)
		if ak8jet.pt>upedge:
			ptbin=nbins
		cont=topSFhists[0].GetBinContent(ptbin)
		upunc=topSFhists[2].GetBinContent(ptbin)-cont
		downunc=topSFhists[1].GetBinContent(ptbin)-cont
		if cut=="T":

			rdict = {"sf":cont,"down":cont+downunc,"up":cont+upunc}
			#if ak8jet.pt<upedge:
			#	rdict = {"sf":cont,"down":cont+downunc,"up":cont+upunc}
			#else:
			#	rdict = {"sf":cont,"down":cont+2.0*downunc,"up":cont+2.0*upunc}
			return rdict
		else:

			sfval=(1.0-cont*self.tteff["tau21"])/(1.0-self.tteff["tau21"])
			sfvald=(1.0-(cont+downunc)*self.tteff["tau21"])/(1.0-self.tteff["tau21"])
			sfvalu=(1.0-(cont+upunc)*self.tteff["tau21"])/(1.0-self.tteff["tau21"])
			return {"sf":sfval,"down":sfvald,"up":sfvalu}

			#return {"sf":1.0,"down":1.0,"up":1.0}
	#Higgs SF calc
	def HTagSf(self,ak8jet,cut,settype="H"):
		ismistag=False
		#print settype
		#print ak8jet,cut,settype
		if settype=="H":
			#print "isH"
			if self.era=="2016":
				sf=	[350.0,850.0,1.01,0.06,0.10]
			if self.era=="2017":
				sf=	[350.0,840.0,0.9,0.08,0.04]
			if self.era=="2018":
				sf=	[350.0,850.0,0.89,0.06,0.04]
			#print "H",sf
		#USE 2017 TTBAR FOR ALL!!
		elif settype=="T":
			ismistag=True
			#print "isT"
			if ak8jet.pt>430.:
				if self.era=="2016":
					sf=	[430.0,float("inf"),0.902,0.083,0.081]

				if self.era=="2017":
					sf=	[430.0,float("inf"),0.902,0.083,0.081]

				if self.era=="2018":
					sf=	[430.0,float("inf"),0.902,0.083,0.081]
			elif ak8jet.pt>350.:

				if self.era=="2016":
					sf=	[350.0,430.,0.967,0.057,0.056]

				if self.era=="2017":
					sf=	[350.0,430.,0.967,0.057,0.056]

				if self.era=="2018":
					sf=	[350.0,430.,0.967,0.057,0.056]




		else:
			return {"sf":1.0,"down":1.0,"up":1.0},{"sf":1.0,"down":1.0,"up":1.0}


		if cut=="T":
			if sf[0]<ak8jet.pt<sf[1]:
				if ismistag:
					return {"sf":1.0,"down":1.0,"up":1.0},{"sf":sf[2],"down":sf[2]-sf[4],"up":sf[2]+sf[3]}
				else:
					return {"sf":sf[2],"down":sf[2]-sf[4],"up":sf[2]+sf[3]},{"sf":1.0,"down":1.0,"up":1.0}
			else:
				#RETURN 2XUNC, CHECK!!
				if ismistag:
					return {"sf":1.0,"down":1.0,"up":1.0},{"sf":sf[2],"down":sf[2]-2.0*sf[4],"up":sf[2]+2.0*sf[3]}
				else:
					return {"sf":sf[2],"down":sf[2]-2.0*sf[4],"up":sf[2]+2.0*sf[3]},{"sf":1.0,"down":1.0,"up":1.0}
		else:

			if ismistag:
				sfval=(1.0-sf[2]*self.tteff["btagHbb"])/(1.0-self.tteff["btagHbb"])
				sfvald=(1.0-(sf[2]-sf[4])*self.tteff["btagHbb"])/(1.0-self.tteff["btagHbb"])
				sfvalu=(1.0-(sf[2]+sf[3])*self.tteff["btagHbb"])/(1.0-self.tteff["btagHbb"])
				return {"sf":1.0,"down":1.0,"up":1.0},{"sf":sfval,"down":sfvald,"up":sfvalu}
			else:
				return {"sf":1.0,"down":1.0,"up":1.0},{"sf":1.0,"down":1.0,"up":1.0}

	#B SF calc (just ev weight)
	def BTagSf(self,ak4jet,cut,hadfl):
		ak4pt = ak4jet.pt
		ismistag=False

		if hadfl==None:
			return {"sf":1.0,"down":1.0,"up":1.0},{"sf":1.0,"down":1.0,"up":1.0}
		if cut=="T":
			#print hadfl

				
			if abs(hadfl) in [4,5]:
				sfdict=self.btagdict
			else:
				ismistag=True
				sfdict=self.bmistagdict
			bsfdict={"sf":1.0,"down":1.0,"up":1.0}
			for bsf in ["sf","down","up"]:
				for prange in (sfdict)[bsf]:

					if prange[0]<ak4pt<prange[1]:
						bsfdict[bsf]=prange[2].Eval(ak4pt)
					if (prange[1]<ak4pt) and (prange==(sfdict)[bsf][-1]):
						
						if bsf=="sf":
							bsfdict[bsf]=prange[2].Eval(prange[1])
						else:


							tempsf=bsfdict["sf"]
							bsfdict[bsf]=tempsf+2.0*(prange[2].Eval(prange[1])-tempsf)
							#print "oout",bsfdict

			#print ismistag,bsfdict
			#print hadfl,ismistag,cut,bsfdict
			if ismistag:
				return {"sf":1.0,"down":1.0,"up":1.0},bsfdict
			else:
				return bsfdict,{"sf":1.0,"down":1.0,"up":1.0}
		else:
			return {"sf":1.0,"down":1.0,"up":1.0},{"sf":1.0,"down":1.0,"up":1.0}


	#W SF calc
	def WTagSf(self,ak8jet,cut):


		if self.era=="2016":
				sf=[1.00,0.06]

		if self.era=="2017":
				if ak8jet.pt>350.0:
					sf=[0.97,0.13]
				else:
					sf=[0.97,0.09]
				#sf=[0.97,0.06]

		if self.era=="2018":
				#sf=[0.980,0.13]
				sf=[0.980,0.027]
		if cut=="T":
			return {"sf":sf[0],"down":sf[0]-sf[1],"up":sf[0]+sf[1]}
		else:
			sfval=(1.0-sf[0]*self.tteff["tau21"])/(1.0-self.tteff["tau21"])
			sfvald=(1.0-(sf[0]-sf[1])*self.tteff["tau21"])/(1.0-self.tteff["tau21"])
			sfvalu=(1.0-(sf[0]+sf[1])*self.tteff["tau21"])/(1.0-self.tteff["tau21"])
			return {"sf":sfval,"down":sfvald,"up":sfvalu}

	#W SF extrapolation
	def Extrap(self,ak8jet,cut):
		if cut=="T":
			if (self.era=="2017") and ak8jet.pt<600.0:
				return {"sf":1.0,"down":1.0,"up":1.0}
			uval=(4.1/100.0)*math.log(ak8jet.pt/200.0)
			return {"sf":1.0,"down":1.0-uval,"up":1.0+uval}

		else:
			return {"sf":1.0,"down":1.0,"up":1.0}


	def PuWeight(self,ntrueint):

		pudict={"sf":1.0,"down":1.0,"up":1.0}

		cbin= (self.puhists["sf"]).FindBin(ntrueint)

		#CHECK!!! max??
		pudict["sf"] = min(5.0,(self.puhists["sf"]).GetBinContent(cbin))
		pudict["down"] = min(5.0,(self.puhists["down"]).GetBinContent(cbin))
		pudict["up"] = min(5.0,(self.puhists["up"]).GetBinContent(cbin))

		return pudict
	def TriggerWeight(self,ht,msd=0.0):
		trigdict={}

		maxtright=1500.0
		maxtrightwithm=1100.0
		maxtrigmass=120.0

		trigrand=random.random()
		histotype="2D"
		trhisto=None

		#Select era from probability
		for it in xrange(len(self.trigprobs)):
			if trigrand>self.trigprobs[it]:
				if self.era=="2017" and it==1:
					trhisto=self.trighists[it]
					histotype="1D"
				else:
					trhisto=self.trighist2ds[it]
				break
		if trhisto==None:
			print "Trig ERROR!"
			return {"sf":1.0,"down":1.0,"up":1.0}

		#1D if no trimmedmass trigger
		if histotype=="1D":
			if ht > maxtright:
				trigdict= {"sf":1.0,"down":1.0,"up":1.0}
			else:
				htbin = trhisto.FindBin(ht)
				weight = trhisto.GetBinContent(htbin)
				toterr=0.5*abs(1.0-weight)
				trigdict= {"sf":weight,"down":max(weight-toterr,0.0),"up":min(weight+toterr,1.0)}
		else:
			if ((ht > maxtrightwithm) and (msd > maxtrigmass)) or (ht > maxtright):
				trigdict= {"sf":1.0,"down":1.0,"up":1.0}

			else:
				htbin = trhisto.GetXaxis().FindBin(ht)
				msdbin = trhisto.GetYaxis().FindBin(msd)
				weight = trhisto.GetBinContent(htbin,msdbin)
				toterr=0.5*abs(1.0-weight)
				trigdict= {"sf":weight,"down":max(weight-toterr,0.0),"up":min(weight+toterr,1.0)}

		if trigdict["sf"]<0.0001:
			logging.error("Zero Weight Trig "+str(ht)+","+str(msd))
			trigdict= {"sf":1.0,"down":1.0,"up":1.0}
		return trigdict

	def CandToDict(self,cands):
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
					dictver[cand]["msoftdropdef"] = cands[cand].msoftdropdef
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

	def RegionMap(self,regionint,regionmap):
		outr=[]
		#regionmap=["A","B","E","J","C","K","H","F","D","L","I","G"]

		for rr in xrange(len(regionmap)):
			bitv = 1<<rr
			truthv=(bitv&regionint)>>rr
			if(truthv):outr.append(regionmap[rr])
		return outr

	def Tptrw(self,geninfo):
		TPT = None
		ATPT = None
		tptsf= {"sf":1.0,"down":1.0,"up":1.0}
		for gg in geninfo:
			if gg.statusFlags!=10497:
				continue
			if (gg.pdgId==6) and TPT==None:
				TPT = min(gg.pt,400.0)
			if (gg.pdgId==-6) and ATPT==None:
				ATPT = min(gg.pt,400.0)
			if TPT!=None and ATPT!=None:
				sfval= sqrt(math.exp(0.0615-0.0005*TPT)*math.exp(0.0615-0.0005*ATPT))
				abserror = 0.5*(1.0-sfval)
				tptsf["sf"] = sfval
				tptsf["down"] = sfval+abserror
				tptsf["up"] = max((sfval-abserror),0.0)
				break

		if tptsf["sf"]==1.0:
			print "tptsf 1.0",geninfo
		return tptsf

	def GenTruth(self,geninfo):
		truthdict={}
		nump=0
		for gg in geninfo:
			if (abs(gg.pdgId)==6) and (not "t" in truthdict):
				truthdict["t"]= gg
			if (abs(gg.pdgId)==25) and (not "H" in truthdict):
				truthdict["H"]= gg
				
			if (abs(gg.pdgId)==23) and (not "Z" in truthdict):
				truthdict["Z"]= gg
			if (abs(gg.pdgId)==5) and (not "b" in truthdict):
				if abs(geninfo[gg.genPartIdxMother].pdgId)>100:
					truthdict["b"]=	gg
			nump+=1
			#if len(truthdict)==3:
			#	break
		return truthdict
	def GenMatchAK8(self,ak8jet,geninfo):
		
		gmatch=None
		for gg in geninfo:
		
			#print abs(gg.pdgId),geninfo[gg.genPartIdxMother].pdgId

			if ((abs(gg.pdgId)==24) and (abs(geninfo[gg.genPartIdxMother].pdgId)==6)):
				gdr = (ak8jet.p4).DeltaR(gg.p4)

				if gdr<0.8:
					gmatch= "T" 
					#print "gdr",gdr
		

			if (abs(gg.pdgId)==25):
				gdr = (ak8jet.p4).DeltaR(gg.p4)
				if gdr<0.8:
					#print gdr
					#give H priority
					gmatch= "H" 
					return gmatch 
		return gmatch
	def GenMatchB(self,ak8jet,geninfo):
		
		gmatch=None
		ng=0
		print 
		for gg in geninfo:
			nind=gg.genPartIdxMother
			curg=geninfo[nind]
			print gg.pdgId,curg.pdgId,nind
			if (abs(gg.pdgId)==5):
				gdr = (ak8jet.p4).DeltaR(gg.p4)
				if gdr<0.4:
					print "B"
					gmatch= "B" 
					curg=copy.deepcopy(gg)
					print "FOUND!"
					print "FOUND!"
			if ng>15:
				continue
			ng+=1


		return gmatch
	def GenMatchAK4(self,ak4jet,genjet):
		for gg in genjet:
			gdr = (ak4jet.p4).DeltaR(gg.p4)
			if gdr<0.4:
				return gg.hadronFlavour
		
	def STFilt(self,genpart):

		gps=[]
		for gg in genpart:
			nind=gg.genPartIdxMother
			if nind==-1:
				gps.append(copy.deepcopy(gg))
			#print
			if len(gps)==2:
				#Ftop=False
				#Fb=False
				#FW=False
				#for gg1 in genpart:
				#		if gg1.genPartIdxMother==0 and abs(gg1.pdgId)==6:
				#			Ftop=True
							#print "TOP"
				#		if gg1.genPartIdxMother==0 and abs(gg1.pdgId)==5:
				#			Fb=True
							#print "B"
				#		if gg1.genPartIdxMother==0 and abs(gg1.pdgId)==24:
				#			FW=True
							#print "W"
					


						#print gg1.pdgId,genpart[gg1.genPartIdxMother].pdgId,gg1.genPartIdxMother

				#print gps[0].pdgId,gps[1].pdgId
				if (abs(gps[0].pdgId)== 5 and abs(gps[1].pdgId) == 21) or (abs(gps[1].pdgId)== 5 and abs(gps[0].pdgId) == 21):
				#	print "pass"
				#	if Ftop and Fb and FW:
				#		print "TTev"
					#for gg1 in genpart:
					#	print gg1.pdgIdgg1.genPartIdxMother
					return True
				else:

				#	print "fail"
				#	if Ftop and Fb and FW:
				#		print "TTev"
					return False
		return True	

	def GenMatchForSF(self,ak8jet,geninfo):
		matchval=1
		ig=0
		dprods=[]
		for gg in geninfo:

			gdr = (ak8jet.p4).DeltaR(gg.p4)

		 
			if gdr<0.8:
				#print gg.pdgId,abs(geninfo[gg.genPartIdxMother].pdgId)
				if (abs(geninfo[gg.genPartIdxMother].pdgId) in [24,6]) and abs(gg.pdgId)!=24 and abs(gg.pdgId)!=6:
					#print "fromW"
					dprods.append(gg.pdgId)
			ig+=1
		nq=0
		nb=0
		for dp in dprods:
			if 0<abs(dp)<5:
				nq+=1
			if abs(dp)==5:
				nb+=1
		if nb>0 and nq>1:
			matchval=1
		if nb>0 and nq==1:
			matchval=2
		if nb==0 and nq>1:
			matchval=3
		if nb==0 and nq<=1:
			matchval=4

		return matchval

	def MakeWNu(self,metpt,metphi,muon,bjet):
		Lmuon=muon.p4
		Lbjet=bjet.p4
		nucand=TLorentzVector()
		nucand.SetPtEtaPhiM(metpt,0.0,metphi,0.0)
		dphi=Lmuon.DeltaPhi(nucand)
		cosdphi=math.cos(dphi)
		ptl=Lmuon.Perp()
		pzl=Lmuon.Pz()
		ptnu=nucand.Perp()
		Enl=Lmuon.Energy()
		MW=80.2
		MTOP=172.5
		muval=(MW*MW)/2.0 + ptl*ptnu*cosdphi
		val1 = ((muval*pzl)/(ptl*ptl))
		insqrtval = (muval*pzl*muval*pzl)/(ptl*ptl*ptl*ptl)- ((Enl*ptnu*Enl*ptnu)-(muval*muval))/(ptl*ptl)
		if insqrtval<0:
			pznu = val1
		else:
			val2 = sqrt(insqrtval)
			if (val1-val2)<0:
				pznu=val1+val2
			else:
				pznu=[val1+val2,val1-val2]
			
		#print str(type(pznu))
		if str(type(pznu))=="<type 'list'>":
			#print "islist"
			nulvs_0 = TLorentzVector()
			nulvs_1 = TLorentzVector()
			nulvs_0.SetPxPyPzE(nucand.Px(),nucand.Py(),pznu[0],sqrt(nucand.Px()*nucand.Px()+nucand.Py()*nucand.Py()+pznu[0]*pznu[0]))
			nulvs_1.SetPxPyPzE(nucand.Px(),nucand.Py(),pznu[1],sqrt(nucand.Px()*nucand.Px()+nucand.Py()*nucand.Py()+pznu[1]*pznu[1]))
			#print "numass",	nulvs_0.M(),nulvs_1.M()			
			testtmasses = [(nulvs_0+Lmuon+Lbjet).M(),(nulvs_1+Lmuon+Lbjet).M()]
			#print testtmasses
			if abs(testtmasses[0]-MTOP)<abs(testtmasses[1]-MTOP):
				pznu=pznu[0]
				#print "0"
			else:
				pznu=pznu[1]
				#print "1"



		reconu = TLorentzVector()
		reconu.SetPxPyPzE(nucand.Px(),nucand.Py(),pznu,sqrt(nucand.Px()*nucand.Px()+nucand.Py()*nucand.Py()+pznu*pznu))
		recoW = (reconu+Lmuon)
		return reconu,recoW

def SetFilter(setstring):
	print setstring
	filtername=None
	if (setstring).find('JetHT')!=-1:
		filtername="JetHT"
	if (setstring).find('QCD')!=-1:
		filtername="QCD"
	if ((setstring).find('TTTo')!=-1) or ((setstring).find('TT_Mtt')!=-1):
		filtername="TT"
	if ((setstring).find('ST_tW')!=-1):
		filtername="ST"
	if (setstring).find('WJetsToQQ')!=-1:
		filtername="WJets"
	if (setstring).find('WpTo')!=-1:
		filtername="Signal"
	if (setstring).find('SingleMuon')!=-1:
		filtername="SingleMuon"
	if (setstring).find('EGamma')!=-1:
		filtername="SingleElectron"
	if (setstring).find('SingleElectron')!=-1:
		filtername="SingleElectron"
	return filtername

def ZeroHist(phist):
	for xbin in xrange(phist.GetNbinsX()+1):
		if phist.GetBinContent(xbin)<0.0:
			#print phist.GetBinContent(xbin)
			phist.SetBinContent(xbin,0.0)


def strf(x , nsf=3 ):
		if x==0:
			return "0"
		ndigs = int(math.log10(10.*float(x)))
		newnsf =nsf
		if ndigs<newnsf:
			dps = "."+str(min(newnsf,abs(ndigs-newnsf)))+"f"
			return '%{0}'.format(dps) % x
		else:
			return '%.0f' % x








