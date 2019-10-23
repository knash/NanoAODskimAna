eval `scramv1 project CMSSW CMSSW_10_2_9`
cp -r tardir/PhysicsTools ../CMSSW_10_2_9/src
cd CMSSW_10_2_9/src
ls
eval `scram b`
eval `scramv1 runtime -sh`
eval `cmsenv`
cd ../../
ls /
pwd
