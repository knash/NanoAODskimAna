python NanoAODskim_Generic.py -a tHb -s ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff 
python NanoAODskim_Generic.py -a tHb -s ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff 
python NanoAODskim_Generic.py -a tHb -s ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff 
python NanoAODskim_Generic.py -a tHb -s ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff 

python NanoAODskim_Generic.py -a tZb -s ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff --skipskim
python NanoAODskim_Generic.py -a tZb -s ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff --skipskim
python NanoAODskim_Generic.py -a tZb -s ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff --skipskim
python NanoAODskim_Generic.py -a tZb -s ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 --Ana -e 2017 -f /eos/cms/store/group/phys_b2g/knash -v _v10 -S NanoSlimNtuples2017 --genwoff --skipskim
