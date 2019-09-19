
#from DataFormats.FWLite import Events, Handle
from array import array
import subprocess, math, copy, random, time, logging, sys, os, glob, numpy, itertools
import NanoAODskim_Data	
from NanoAODskim_Data import *
#random.seed(8574931)
from math import sqrt
import ROOT 
from ROOT import TLorentzVector,TH1F,TH2F,TTree,TFile,gROOT,TCanvas,TGraph,TMultiGraph,TLegend,gROOT,TTreeReader,TLatex
from optparse import OptionParser
class NanoAODskim_Functions:
	def __init__(self,anatype="Pho",era="2017",versionstring="v8"):
		self.anatype=anatype
		self.truncval = 300
		self.era = era
		self.versionstring = versionstring
		self.trigstopass=[]
		if self.era=="2017" or self.era=="2018":
			self.ptrigs = ["HLT_PFHT780"]
			self.strigs = ["HLT_PFHT1050","HLT_PFJet500","HLT_PFJet550","HLT_AK8PFJet500","HLT_AK8PFJet550"]
			self.etrigs = ["HLT_AK8PFJet400_TrimMass30","HLT_AK8PFJet420_TrimMass30","HLT_AK8PFHT800_TrimMass50","HLT_AK8PFHT850_TrimMass50","HLT_AK8PFHT900_TrimMass50","HLT_DiPFJetAve500"]

		if self.era=="2016":
			print "UPDATE 2016 TRIGS"
			self.ptrigs = []
			self.strigs = ["HLT_PFHT900","HLT_PFJet450"]
			self.etrigs = []
		self.LoadConstants  = NanoAODskim_Data(era).LoadConstants
		#for ll in self.LoadConstants['dataconst']:
		#	print ll,self.LoadConstants['dataconst'][ll])
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
					'btagHbb__H':{'L':[-1.0,0.0],'M':[0.0,0.6],'M1':[0.6,0.8],'T':[0.8,1.0],'F':[-1.0,1.0]},
					'msoftdrop__H':{'L':[10.0,30.0],'M':[105.0,150.0],'M1':[105.0,150.0],'T':[105.0,150.0],'F':[150.0,220.0]},
					'iMDtop__H':{'L':[0.0,1.0],'M':[0.0,1.0],'M1':[0.0,1.0],'T':[0.0,1.0],'F':[0.9,1.0]},
					'iMDtop__T':{'L':[0.0,0.6],'M':[0.6,0.9],'M1':[0.6,0.9],'T':[0.9,1.0]},
					'msoftdrop__T':{'L':[30.0,65.0],'M':[150.0,220.0],'M1':[150.0,220.0],'T':[150.0,220.0]},
					'btagDeepFlavB__B':{'L':[-1.0,0.0494],'M':[-1.0,0.0494],'M1':[0.0494,1.0],'T':[0.0494,1.0]},
					'pt__B':{'L':200.0,'M':200.0,'M1':200.0,'T':200.0},
					'ptAK8':{'L':450.0,'M':450.0,'M1':450.0,'T':450.0},
					} 
			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.0494],'M':[-1.0,0.0494],'M1':[0.0494,1.0],'T':[0.0494,1.0]}
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
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['L'],
								'pt__B':cutranges['pt__B']['L'],
								'ptAK8':cutranges['ptAK8']['T'],
								},

						'FTR':		{	
								'btagHbb__H':cutranges['btagHbb__H']['F'],
								'msoftdrop__H':cutranges['msoftdrop__H']['F'],
								'iMDtop__H':cutranges['iMDtop__H']['F'],
								'iMDtop__T':cutranges['iMDtop__T']['L'],
								'msoftdrop__T':cutranges['msoftdrop__T']['L'],
								'btagDeepFlavB__B':cutranges['btagDeepFlavB__B']['T'],
								'pt__B':cutranges['pt__B']['T'],
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
					'msoftdrop__T':{'L':[30.0,65.0],'M':[150.0,220.0],'M1':[150.0,220.0],'T':[150.0,220.0]},
					'btagDeepFlavB__B':{'L':[-1.0,0.0494],'M':[-1.0,0.0494],'M1':[0.0494,1.0],'T':[0.0494,1.0]},
					'pt__B':{'L':200.0,'M':200.0,'M1':200.0,'T':200.0},
					'ptAK8':{'L':450.0,'M':450.0,'M1':450.0,'T':450.0},
					} 
			if self.era=="2016":
				cutranges['btagDeepFlavB__B']={'L':[-1.0,0.0494],'M':[-1.0,0.0494],'M1':[0.0494,1.0],'T':[0.0494,1.0]}
				cutranges['tau21__Z']={'L':[0.6,1.0],'M':[0.6,1.0],'M1':[0.4,0.6],'T':[0.0,0.4]}
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


		self.branchestokeepevent = 	[
						"event",
						"run",
						"luminosityBlock"
						]

		self.branchestokeepevent+=self.strigs+self.etrigs+self.ptrigs

		self.branchestokeep=	{
					"CustomAK8Puppi":
						[
						"pt",
						"eta",
						"phi",
						"mass",
						"iMDPho",
						"iMDWW",
						"iMDtop",
						"iW",
						"iMDW",
						"iMDtop",
						"msoftdrop",
						"tau1",
						"tau2",
						"tau3",
						"tau4",
						"btagHbb"
						],
					"Jet":
						[
						"pt",
						"eta",
						"phi",
						"mass",
						"btagDeepFlavB"
						],
					"Muon":
						[
						"pt",
						"eta",
						"phi",
						"mass",
						"highPtId",
						"mvaId"
						],
					"Electron":
						[
						"pt",
						"eta",
						"phi",
						"mass",
						"mvaFall17V2Iso_WP90",
						"mvaFall17V2noIso_WP90"
						]


							
					}
		if anatype=="Pho":
			self.branchestokeep['Photon']=	[
							"pt",
							"eta",
							"phi",
							"mass",
							'pfRelIso03_all',
							'electronVeto',
							'pixelSeed',
							'mvaID_WP80',
							'mvaID_WP90',
							]
					
		#if anatype=="tHb":
		#	self.branchestokeep["Jet"] =	[
		#					"pt",
		#					"eta",
		#					"phi",
		#					"mass",
		#					"btagDeepFlavB"
		#					]
							

	def loadfiles(self,setname="QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",folder="/eos/cms/store/user/knash",redir="eoscms.cern.ch",search=""):
		ntry=0
		files = []
		#print setname,folder,redir
		versionstring=self.versionstring
		#cmsxrootd.fnal.gov
		setnametowrite=setname.replace("/","_").replace("*","")
		#print setname,folder,redir,setnametowrite
		while len(files)==0:
				#print redir

				tempfname="tempfiles"+setnametowrite+self.era+".txt"
				spcall = "eos root://"+redir+" find  "+folder+"/"+setname+" > "+tempfname 
				#print spcall
				#subprocess.call( ["eos root://cmseos.fnal.gov find  /eos/uscms/"+folder+"/"+setname], shell=True )
				subprocess.call( [spcall], shell=True )
				files = []
				
				with open(tempfname) as ftemp:
					filestemp = ftemp.read().splitlines()
					for curfile in filestemp:
						#print curfile
						#print curfile,versionstring,curfile.find(versionstring)
						if curfile.find(".root")!=-1 and curfile.find(versionstring)!=-1 and curfile.find("NanoSlimNtuples")!=-1 and curfile.find("failed")==-1 and curfile.find(search)!=-1:
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
						histos[region]["msoftdrop__"+label+"__"+region] =  TH1F("msoftdrop__"+label+"__"+region,	"msoftdrop__"+label+"__"+region,		250, 0.,500. )
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
					histos[region]["ht__"+label+"__"+region] =  TH1F("htval__"+label+"__"+region,	"htval__"+label+"__"+region,		300, 1000.0,5000.0 )
					histos[region]["htval__"+label+"__"+region] =  TH1F("ht__"+label+"__"+region,	"ht__"+label+"__"+region,		300, 1000.0,5000.0 )
					histos[region]["deltapt__"+label+"__"+region] =  TH1F("deltapt__"+label+"__"+region,	"deltapt__"+label+"__"+region,		250, -500.,500.0 )
					histos[region]["deta__"+label+"__"+region] =  TH1F("deta__"+label+"__"+region,	"deta__"+label+"__"+region,		100, 0.,5.0 )
					histos[region]["dy__"+label+"__"+region] =  TH1F("dy__"+label+"__"+region,	"dy__"+label+"__"+region,		30, 0.,3.0 )
					histos[region]["dyhighm__"+label+"__"+region] =  TH1F("dyhighm__"+label+"__"+region,	"dyhighm__"+label+"__"+region,		30, 0.,3.0 )
					if self.anatype=="Pho":
							histos[region]["iMDW__"+label[1]+"__iMDPho__"+label[0]+"__"+region] =  TH2F("iMDW__"+label[1]+"__iMDPho__"+label[0]+"__"+region,	"iMDW__"+label[1]+"__iMDPho__"+label[0]+"__"+region,		40, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDPho__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDPho__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDPho__"+label[0]+"__"+region,		250, 0.,500.,100, 0.,1. )
					if self.anatype=="WW":
							histos[region]["iMDW__"+label[1]+"__iMDWW__"+label[0]+"__"+region] =  TH2F("iMDW__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"iMDW__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		40, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDWW__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		250, 0.,500.,100, 0.,1. )
							histos[region]["njets__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("njets__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"njets__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		15,-0.5, 14.5,100, 0.,1. )
							histos[region]["htval__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("htval__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"htval__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		250, 0.,2500.,100, 0.,1. )
							histos[region]["njetsrem__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("njetsrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"njetsrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		15,-0.5, 14.5,100, 0.,1. )
							histos[region]["htvalrem__"+label+"__iMDWW__"+label[0]+"__"+region] =  TH2F("htvalrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,	"htvalrem__"+label[1]+"__iMDWW__"+label[0]+"__"+region,		250, 0.,2500.,100, 0.,1. )

					if self.anatype=="Zprime":
							histos[region]["iMDtop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("iMDtop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"iMDtop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )

					if self.anatype=="Bstar":
							histos[region]["tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		250, 0.,500.,100, 0.,1. )
				if len(label)>2:
					if self.anatype=="tHb":
							histos[region]["btagHbb__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("btagHbb__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"btagHbb__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, -1.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		250, 0.,500.,100, 0.,1. )

					if self.anatype=="tZb":
							histos[region]["tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"tau21__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		100, 0.,1.,100, 0.,1. )
							histos[region]["msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region] =  TH2F("msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,	"msoftdrop__"+label[1]+"__iMDtop__"+label[0]+"__"+region,		250, 0.,500.,100, 0.,1. )

				if not isAK4:				
					histos[region]["pt__"+label+"__aeta__"+label+"__"+region] =  TH2F("pt__"+label+"__aeta__"+label+"__"+region,	"pt__"+label+"__aeta__"+label+"__"+region,		350, 400.,3900.,24, 0.0,2.4 )
				else:				
					histos[region]["pt__"+label+"__aeta__"+label+"__"+region] =  TH2F("pt__"+label+"__aeta__"+label+"__"+region,	"pt__"+label+"__aeta__"+label+"__"+region,		350, 0.,3500.,24, 0.0,2.4 )


		for region in regions:
			for histo in histos[region]:
				histos[region][histo].Sumw2()
		return histos


	def makeinv(self,cands,lab):
		invcand={}

		ilab=0
		for ll in lab:
			if ilab==0:
				invcand["TLV"] = copy.deepcopy(cands[ll]["TLV"])
			else:
				invcand["TLV"]+=cands[ll]["TLV"]
			ilab+=1


		invcand["pt"] = invcand["TLV"].Perp()
		invcand["eta"] = invcand["TLV"].Eta()
		invcand["aeta"] = abs(invcand["TLV"].Eta())
		invcand["phi"] = invcand["TLV"].Phi()
		invcand["mass"] = invcand["TLV"].M()
		invcand["p"] = invcand["TLV"].P()
		if ilab==2:
			invcand["dR"] = cands[lab[0]]["TLV"].DeltaR(cands[lab[1]]["TLV"])
			invcand["deltapt"] = cands[lab[0]]["TLV"].Perp() - cands[lab[1]]["TLV"].Perp()
			invcand["ht"] = cands[lab[0]]["TLV"].Perp() + cands[lab[1]]["TLV"].Perp()
			invcand["deta"] = cands[lab[0]]["TLV"].Eta() - cands[lab[1]]["TLV"].Eta()
			invcand["dphi"] = cands[lab[0]]["TLV"].DeltaPhi(cands[lab[1]]["TLV"])
			invcand["dy"] = abs(cands[lab[0]]["TLV"].Rapidity()-cands[lab[1]]["TLV"].Rapidity())
			invcand["dyhighm"] = -1.0


			if invcand["mass"]>2000:
				invcand["dyhighm"] = abs(cands[lab[0]]["TLV"].Rapidity()-cands[lab[1]]["TLV"].Rapidity())
		return invcand
	def histosfill(self,histos,cands,region='C',weight=1.0,hfilter=[]):
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
			if len(idval)>4:
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
			if curcuts["iMDW__W"][0]<ak8jet["iMDW"]<=curcuts["iMDW__W"][1] :
				if curcuts["msoftdrop__W"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__W"][1]:
					return True
				
		if obj=="H":
			if curcuts["btagHbb__H"][0]<ak8jet["btagHbb"]<=curcuts["btagHbb__H"][1] and (curcuts["msoftdrop__H"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__H"][1]):
				

				if "iMDtop__H" in curcuts:
					if curcuts["iMDtop__H"][0]<ak8jet["iMDtop"]<=curcuts["iMDtop__H"][1]:
						return True
				else:			
					return True
		if obj=="Z":
			if curcuts["tau21__Z"][0]<ak8jet["tau21"]<=curcuts["tau21__Z"][1] and (curcuts["msoftdrop__Z"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__Z"][1]):
				return True
		if obj=="T":
			if (curcuts["iMDtop__T"][0]<ak8jet["iMDtop"]<=curcuts["iMDtop__T"][1]) and (curcuts["msoftdrop__T"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__T"][1]):
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
			if (curcuts["iMDtop__A"][0]<ak8jet["iMDtop"]<=curcuts["iMDtop__A"][1]) and (curcuts["msoftdrop__A"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__A"][1]):
					return True
		if obj=="B":
			if curcuts["btagDeepFlavB__B"][0]<ak8jet["btagDeepFlavB"]<=curcuts["btagDeepFlavB__B"][1]:
					return True
		if obj=="P":
			if ((curcuts["iMDPho__P"][0]<ak8jet["iMDPho"]<=curcuts["iMDPho__P"][1]) and (curcuts["msoftdrop__P"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__P"][1])):
				if curcuts["msoftdrop__P"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__P"][1]:
				#if not ( (curcuts["Inv_iMDW__P"][0]<ak8jet["iMDW"]<curcuts["Inv_iMDW__P"][1])):		
					return True
		if obj=="F":
			if ((curcuts["iMDWW__F"][0]<ak8jet["iMDWW"]<=curcuts["iMDWW__F"][1]) and (curcuts["msoftdrop__F"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__F"][1])):
				#if not ( (curcuts["Inv_iMDW__F"][0]<ak8jet["iMDW"]<curcuts["Inv_iMDW__F"][1])):
				if curcuts["msoftdrop__F"][0]<ak8jet["msoftdrop"]<=curcuts["msoftdrop__F"][1]:		
					return True
		return False
	def ttreeinit(self,curttree,runver=""):
		branchestokeepevent=copy.copy(self.branchestokeepevent)
		self.trigstopass=self.strigs+self.etrigs
		if runver=="2017B":
			for curt in self.etrigs:
				branchestokeepevent.remove(curt)
				self.trigstopass.remove(curt)
		if runver=="2017C":
			branchestokeepevent.remove("HLT_DiPFJetAve500")
			self.trigstopass.remove("HLT_DiPFJetAve500")
		branchestokeep=self.branchestokeep
		intlist = ["pdgId","cutBasedV1Bitmap"]

		boollist = ["electronVeto","pixelSeed","mvaID_WP80","mvaID_WP90","mvaId","highPtId","mvaFall17V2Iso_WP90","mvaFall17V2noIso_WP90"]

		branchdir = {}
		for branchclass  in branchestokeep:
			branchdir[branchclass]=[array('i',[0]),{}]
			curttree.SetBranchAddress("n"+branchclass,branchdir[branchclass][0])

			for branchsubclass in branchestokeep[branchclass]:

				if branchsubclass in intlist:
					#print branchsubclass,"I"
					branchdir[branchclass][1][branchsubclass]=array('i',[0]*self.truncval)
				elif branchsubclass in boollist:
					#print branchsubclass,"I"
					branchdir[branchclass][1][branchsubclass]=array('b',[0]*self.truncval)
				else:
					branchdir[branchclass][1][branchsubclass]=array('f',[0.]*self.truncval)
				curttree.SetBranchAddress(branchclass+"_"+branchsubclass, branchdir[branchclass][1][branchsubclass])
		for branchclass in branchestokeepevent:
			if branchclass.find("HLT")!=-1:
				branchdir[branchclass]=array('b',[0])
			else:
				branchdir[branchclass]=array('i',[0])
			curttree.SetBranchAddress(branchclass, branchdir[branchclass])
		return branchdir

	def eventinit(self,branchdir):
		#print "in init"
		curdictval = {}	
		for bb in branchdir:
			#print bb
			if type(branchdir[bb])==type(array('i')):
				curdictval[bb]=branchdir[bb][0]

			else:
				
				curdictval[bb]={} 
				for val in branchdir[bb][1]:
					curdictval[bb][val]=[]
				#print branchdir[bb][0][0]

				tval=self.truncval
				maxnum = min(tval,branchdir[bb][0][0])

				if branchdir[bb][0][0]>=tval:
					logging.warning("Truncating branch of length %s" % branchdir[bb][0][0])
				for i in xrange(maxnum):
					
					for bnames in branchdir[bb][1]:
						curdictval[bb][bnames].append(branchdir[bb][1][bnames][i])
						
		random.seed(curdictval['event'])
		
		return curdictval
	def TriggerPass(self,curdictval,prescale=False):
		#for ctrig in self.trigstopass:
		#	print ctrig,curdictval[ctrig]
		if prescale:
			curtrigs = copy.copy(self.ptrigs)
		else:
			curtrigs = copy.copy(self.trigstopass)
		for ctrig in curtrigs:
			#print ctrig,curdictval[ctrig]
			try: 
				if curdictval[ctrig]==1:
					#print "PASS!"
					return True
			except:
				print "Missing trigger",ctrig

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


			

	def strf(self, x):
		return '%.0f' % x









