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
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 1 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 2 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 3 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 4 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 5 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 6 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 7 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 8 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 9 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 10 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 11 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 12 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 13 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 14 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 15 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 16 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 17 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 18 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 19 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 20 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 21 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 22 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 23 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 24 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 25 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 26 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 27 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 28 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 29 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 30 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 31 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 32 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 33 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 34 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 35 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 36 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 37 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 38 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 39 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 40 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 41 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 42 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 43 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 44 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 45 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 46 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 47 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 48 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 49 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 50 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 51 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 52 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 53 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 54 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 55 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 56 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 57 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 58 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 59 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 60 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 61 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 62 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 63 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 64 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 65 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 66 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 67 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 68 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 69 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 70 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 71 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 72 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 73 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 74 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 75 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 76 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 77 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 78 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 79 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 80 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 81 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 82 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 83 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 84 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 85 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 86 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 87 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 88 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 89 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 90 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 91 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 92 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 93 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 94 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 95 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 96 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 97 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 98 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 99 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 100 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 101 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 102 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 103 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 104 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 105 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 106 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 107 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 108 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 109 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 110 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 111 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 112 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 113 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 114 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 115 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 116 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 117 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 118 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 119 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 120 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 121 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 122 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 123 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 124 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 125 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 126 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 127 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 128 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 129 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 130 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 131 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 132 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 133 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 134 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 135 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 136 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 137 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 138 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 139 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  JetHT -j 140 -t 140  --Bkg -e 2018 -S Run2018 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp1500Nar_Bp800Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp1500Nar_Tp800Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp1500Nar_Bp1000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp1500Nar_Tp1000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp1500Nar_Bp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp1500Nar_Tp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp2000Nar_Bp1000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp2000Nar_Tp1000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp2000Nar_Bp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp2000Nar_Tp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp2000Nar_Bp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp2000Nar_Tp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp2500Nar_Bp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp2500Nar_Tp1300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp2500Nar_Bp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp2500Nar_Tp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp2500Nar_Bp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp2500Nar_Tp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3000Nar_Bp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3000Nar_Tp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3000Nar_Bp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3000Nar_Tp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3000Nar_Bp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3000Nar_Tp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3500Nar_Bp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3500Nar_Tp1700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3500Nar_Bp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3500Nar_Tp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3500Nar_Bp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3500Nar_Tp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3500Nar_Bp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3500Nar_Tp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp3500Nar_Bp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp3500Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4000Nar_Bp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4000Nar_Tp2000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4000Nar_Bp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4000Nar_Tp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4000Nar_Bp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4000Nar_Tp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4000Nar_Bp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4000Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4000Nar_Bp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4000Nar_Tp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4500Nar_Bp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4500Nar_Tp2300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4500Nar_Bp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4500Nar_Tp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4500Nar_Bp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4500Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4500Nar_Bp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4500Nar_Tp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp4500Nar_Bp3700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp4500Nar_Tp3700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5000Nar_Bp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5000Nar_Tp2700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5000Nar_Bp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5000Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5000Nar_Bp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5000Nar_Tp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5000Nar_Bp3700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5000Nar_Tp3700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5000Nar_Bp4000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5000Nar_Tp4000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5500Nar_Bp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5500Nar_Tp3000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5500Nar_Bp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5500Nar_Tp3300Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5500Nar_Bp3700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5500Nar_Tp3700Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5500Nar_Bp4000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5500Nar_Tp4000Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToBpT_Wp5500Nar_Bp4400Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  WpToTpB_Wp5500Nar_Tp4400Nar_Ht_TuneCP5_13TeV-madgraphMLM-pythia8  --Bkg -e 2018 -S RunIIFall17MiniAODv2 -f /eos/cms/store/group/phys_b2g/knash --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 1 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 2 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 3 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 4 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 5 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 6 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 7 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 8 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 9 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 10 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 11 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 12 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 13 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 14 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 15 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 16 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 17 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 18 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 19 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 20 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 21 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 22 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 23 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 24 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 25 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 26 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 27 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 28 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 29 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 30 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 31 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 32 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 33 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 34 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 35 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 36 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 37 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 38 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 39 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8 -j 40 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 1 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 2 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 3 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 4 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 5 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 6 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 7 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 8 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 9 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 10 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 11 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 12 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 13 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 14 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 15 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 16 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 17 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 18 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 19 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 20 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 21 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 22 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 23 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 24 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 25 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 26 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 27 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 28 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 29 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 30 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 31 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 32 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 33 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 34 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 35 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 36 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 37 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 38 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 39 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8 -j 40 -t 40  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 1 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 2 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 3 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 4 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 5 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 6 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 7 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 8 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 9 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 10 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 11 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 12 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 13 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 14 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 15 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 16 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 17 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 18 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 19 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 20 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 21 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 22 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 23 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 24 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 25 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 26 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 27 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 28 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 29 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8 -j 30 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD  --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 1 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 2 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 3 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 4 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 5 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 6 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 7 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 8 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 9 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8 -j 10 -t 10  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 1 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 2 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 3 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 4 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 5 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 6 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 7 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 8 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 9 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 10 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 11 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 12 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 13 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 14 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 15 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 16 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 17 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 18 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 19 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 20 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 21 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 22 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 23 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 24 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 25 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 26 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 27 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 28 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 29 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor
output_$(JID)        python ./tardir/NanoAODskim_Generic.py -a tHb -s  TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8 -j 30 -t 30  --Bkg -e 2018 -f /eos/cms/store/group/phys_b2g/knash -S RunIIAutumn18MiniAOD -v v10 --condor

