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
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 1 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 2 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 3 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 4 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 5 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 6 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 7 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 8 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 9 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 10 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 11 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 12 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 13 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 14 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 15 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 16 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 17 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 18 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 19 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 20 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 21 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 22 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 23 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 24 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 25 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 26 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 27 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 28 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 29 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 30 -t 30  --Bkg -e 2016 -S Run2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 1 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 2 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 3 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 4 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 5 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 1 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 2 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 3 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 4 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 5 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 1 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 2 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 3 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 4 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 -j 5 -t 5  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash -S NanoSlimNtuples2016   --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 1  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 1  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 1 -t 2  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 2 -t 2  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 1 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 2 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 3 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 4 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 5 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 6 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 7 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 8 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 9 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8 -j 10 -t 10  --Bkg -e 2016 -f /eos/cms/store/group/phys_b2g/knash   -S NanoSlimNtuples2016 --condor

