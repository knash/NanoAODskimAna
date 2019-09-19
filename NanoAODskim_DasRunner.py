import NanoAODskim_Functions	
from NanoAODskim_Functions import *



allsets = 	[
		"BstarToTW_private_M-1200_LH_TuneCP5_13TeV-madgraph-pythia8/knash-MINIAODSIM-57e6cb033643cfa6c372ff41c8f6b812/USER",
		"BstarToTW_private_M-2000_LH_TuneCP5_13TeV-madgraph-pythia8/knash-MINIAODSIM-57e6cb033643cfa6c372ff41c8f6b812/USER",
		"BstarToTW_private_M-2800_LH_TuneCP5_13TeV-madgraph-pythia8/knash-MINIAODSIM-57e6cb033643cfa6c372ff41c8f6b812/USER",
		"WkkToRWToTri_Wkk3000R100_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2/knash-MINIAODSIM-57e6cb033643cfa6c372ff41c8f6b812/USER",
		"WkkToRWToTri_Wkk3000R200_ZA_private_TuneCP5_13TeV-madgraph-pythia8_v2/knash-MINIAODSIM-57e6cb033643cfa6c372ff41c8f6b812/USER"
		]
allsetsglobal = [
		"QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM",
		"QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM",
		"QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM",
		"TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM",
		"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM",
		]
commands = []

for cset in allsets:
	commands.append('dasgoclient --query="summary dataset=/'+cset+' instance=prod/phys03"') 
for cset in allsetsglobal:
	commands.append('dasgoclient --query="summary dataset=/'+cset+'"') 

for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )


