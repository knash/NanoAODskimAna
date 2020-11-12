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
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 2  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 2 -t 2  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 2 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 3 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 4 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 5 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 6 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 7 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 8 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 9 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 10 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 11 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 12 -t 12  --Bkg -e 2017 -f /eos/cms/store/group/phys_b2g/knash   -v _v10  -S NanoSlimNtuples2017 --condor

