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
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 1 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 2 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 3 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 4 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 5 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 6 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 7 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 8 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 9 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 10 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 11 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 12 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 13 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 14 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 15 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 16 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 17 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 18 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 19 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 20 -t 20  --Ana -e 2017 -S Run2017  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j 1 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j 2 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j 3 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j 4 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j 5 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8 -j 6 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j 1 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j 2 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j 3 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j 4 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j 5 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8 -j 6 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j 1 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j 2 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j 3 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j 4 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j 5 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8 -j 6 -t 6  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2017    --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 2  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 2 -t 2  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 2 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 3 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 4 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 5 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 6 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 7 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 8 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 9 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 10 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 11 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 12 -t 12  --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
