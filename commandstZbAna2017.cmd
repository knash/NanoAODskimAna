# -*- sh -*- # for font lock mode
# variable definitions
- env = export SCRAM_ARCH=slc7_amd64_gcc700; eval `scramv1 project CMSSW CMSSW_10_2_9` ; cp -r tardir/PhysicsTools CMSSW_10_2_9/src ; cd CMSSW_10_2_9/src ; eval `scram b` ;eval `scramv1 runtime -sh`; eval `scram b` ; cd -
- tag = 
- output = outputFile=
- tagmode = none
- tarfile = /afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_9/src/tarball.tgz
- untardir = tardir
- copycommand = cp

# Sections listed
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tZb -s  WpToBpT_Wp3500Nar_Bp2700Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v v8,v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tZb -s  WpToBpT_Wp5500Nar_Bp3300Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v v8,v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tZb -s  WpToTpB_Wp5500Nar_Tp4000Nar_Zt_TuneCP5_13TeV-madgraphMLM-pythia8  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v v8,v10 --condor

