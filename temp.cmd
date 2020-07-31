# -*- sh -*- # for font lock mode
# variable definitions
- env = export SCRAM_ARCH=slc7_amd64_gcc820; eval `scramv1 project CMSSW CMSSW_11_0_0_pre10_ROOT618` ; cp -r tardir/PhysicsTools CMSSW_11_0_0_pre10_ROOT618/src ; cd CMSSW_11_0_0_pre10_ROOT618/src ; eval `scram b` ;eval `scramv1 runtime -sh`; eval `scram b` ; cd -
- tag = 
- output = outputFile=
- tagmode = none
- tarfile = /afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_11_0_0_pre10_ROOT618/src/tarball.tgz
- untardir = tardir
- copycommand = cp

# Sections listed
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  NanoAODskim_tHbAna2017__JetHT__Run2017__ -j 4 -t 13  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  NanoAODskim_tHbAna2017__JetHT__Run2017__ -j 5 -t 13  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tZb -s  NanoAODskim_tZbAna2016__TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8__ -j 4 -t 5  --Ana -e 2016 -f /eos/cms/store/group/phys_b2g/knash  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tZb -s  NanoAODskim_tZbAna2016__JetHT__Run2016__ -j 9 -t 10  --Ana -e 2016 -f /eos/cms/store/group/phys_b2g/knash  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  NanoAODskim_tHbAna2016__TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8__ -j 4 -t 5  --Ana -e 2016 -f /eos/cms/store/group/phys_b2g/knash  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  NanoAODskim_tHbAna2016__TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8__ -j 1 -t 2  --Ana -e 2016 -f /eos/cms/store/group/phys_b2g/knash  --condor
