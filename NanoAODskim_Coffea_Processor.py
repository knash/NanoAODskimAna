import NanoAODskim_Functions_coffea	
from NanoAODskim_Functions_coffea import *
import time
import NanoAODskim_Coffea_Processor
from coffea import hist
from coffea.analysis_objects import JaggedCandidateArray
import coffea.processor as processor
from awkward import JaggedArray
import numpy as np
class THBproc(processor.ProcessorABC):
	def __init__(self):
		dataset_axis = hist.Cat("dataset", "Primary dataset")
		mass_axis = hist.Bin("mass", r"$m_{\mu\mu}$ [GeV]", 600, 0.25, 300)
		pt_axis = hist.Bin("pt", r"$p_{T,\mu}$ [GeV]", 3000, 0.0, 3000)

		self._accumulator = processor.dict_accumulator({
			'pt_AK8': hist.Hist("Counts", dataset_axis, pt_axis)
		})

	@property
	def accumulator(self):
		return self._accumulator

	def process(self, df):
		output = self.accumulator.identity()
		dataset = df['dataset']



		CustomAK8Puppis = JaggedCandidateArray.candidatesfromcounts(
			df['nCustomAK8Puppi'],
			pt=df['CustomAK8Puppi_pt'],
			eta=df['CustomAK8Puppi_eta'],
			phi=df['CustomAK8Puppi_phi'],
			mass=df['CustomAK8Puppi_mass'],
			tau1=df['CustomAK8Puppi_tau1'],
			tau2=df['CustomAK8Puppi_tau2'],
			tau3=df['CustomAK8Puppi_tau3'],
			tau4=df['CustomAK8Puppi_tau4'],
			iMDPho=df['CustomAK8Puppi_iMDPho'],
			iMDWW=df['CustomAK8Puppi_iMDWW'],
			iMDtop=df['CustomAK8Puppi_iMDtop'],
			msoftdrop=df['CustomAK8Puppi_msoftdrop'],
			btagHbb=df['CustomAK8Puppi_btagHbb']
			)
		Jets = JaggedCandidateArray.candidatesfromcounts(
			df['nJet'],
			pt=df['Jet_pt'],
			eta=df['Jet_eta'],
			phi=df['Jet_phi'],
			mass=df['Jet_mass'],
			btagDeepFlavB=df['Jet_btagDeepFlavB']
			)
		Muons = JaggedCandidateArray.candidatesfromcounts(
			df['nMuon'],
			pt=df['Muon_pt'],
			eta=df['Muon_eta'],
			phi=df['Muon_phi'],
			mass=df['Muon_mass'],
			highPtId=df['Muon_highPtId'],
			mvaId=df['Muon_mvaId']
			)
		Electrons = JaggedCandidateArray.candidatesfromcounts(
			df['nElectron'],
			pt=df['Electron_pt'],
			eta=df['Electron_eta'],
			phi=df['Electron_phi'],
			mass=df['Electron_mass'],
			mvaFall17V2Iso_WP90=df['Electron_mvaFall17V2Iso_WP90'],
			mvaFall17V2noIso_WP90=df['Electron_mvaFall17V2noIso_WP90']
			)
		Trigs = JaggedCandidateArray.candidatesfromcounts(
			HLT_PFHT780 = ['HLT_PFHT780'],
			HLT_PFHT1050 = ['HLT_PFHT1050'],
			HLT_PFJet500 = ['HLT_PFJet500'],
			HLT_PFJet550 = ['HLT_PFJet550'],
			HLT_AK8PFJet500 = ['HLT_AK8PFJet500'],
			HLT_AK8PFJet550 = ['HLT_AK8PFJet550'],
			HLT_AK8PFJet400_TrimMass30 = ['HLT_AK8PFJet400_TrimMass30'],
			HLT_AK8PFJet420_TrimMass30 = ['HLT_AK8PFJet420_TrimMass30'],
			HLT_AK8PFHT800_TrimMass50 = ['HLT_AK8PFHT800_TrimMass50'],
			HLT_AK8PFHT850_TrimMass50 = ['HLT_AK8PFHT850_TrimMass50'],
			HLT_AK8PFHT900_TrimMass50 = ['HLT_AK8PFHT900_TrimMass50'],
			HLT_DiPFJetAve500 = ['HLT_DiPFJetAve500']
			)


		muId = Muons.pt>70.0 and ((Muons.mvaId > 1) or (Muons.highPtId > 1))
		nomuonscut = (Muons[muId].counts == 0)

		elId = Electrons.pt>70.0 and ((Electrons.mvaFall17V2Iso_WP90>0) or (Electrons.mvaFall17V2noIso_WP90>0))
		noelectronscut = (Electrons[elId].counts == 0)
		CustomAK8Puppi = CustomAK8Puppis[muId and elId]
		output['pt_AK8'].fill(dataset=dataset,pt=CustomAK8Puppi.pt)
		return output

	def postprocess(self, accumulator):
		return accumulator
