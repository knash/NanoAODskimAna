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
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 1 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 2 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 3 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 4 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 5 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 6 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 7 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 8 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 9 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 10 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 11 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 12 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 13 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 14 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 15 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 16 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 17 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 18 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 19 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 20 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 21 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 22 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 23 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 24 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 25 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 26 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 27 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 28 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 29 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  JetHT -j 30 -t 30  --Bkg -e 2018 -S Run2018  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 1 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 2 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 3 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 4 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 5 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 6 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 7 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 1 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 2 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 3 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 4 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 5 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 6 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 7 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 1 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 2 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 3 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 4 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 5 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 6 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 7 -t 7  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2018   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 2  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 2 -t 2  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 1 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 2 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 3 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 4 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 5 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 6 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 7 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 8 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 9 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 10 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 11 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 12 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 13 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 14 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a Bstar -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 15 -t 15  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2018 --condor

