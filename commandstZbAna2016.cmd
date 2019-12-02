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

