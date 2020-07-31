

python limit_plot_shape.py --inputFileExp=limitsetting/theta/expckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018_B0p5T0p5H0p5Z0p5_Nonelow.txt  --inputFileObs=limitsetting/theta/obsckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018_B0p5T0p5H0p5Z0p5_Nonelow.txt --scale --useLog -R low --outputName=AllHadronic
python limit_plot_shape.py --inputFileExp=limitsetting/theta/expckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018_B0p5T0p5H0p5Z0p5_Nonehigh.txt --inputFileObs=limitsetting/theta/obsckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018_B0p5T0p5H0p5Z0p5_Nonehigh.txt --scale --useLog -R high --outputName=AllHadronic
python limit_plot_shape.py --inputFileExp=limitsetting/theta/expckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018_B0p5T0p5H0p5Z0p5_Nonecentral.txt --inputFileObs=limitsetting/theta/obsckhcomptHb2016tHb2017tHb2018tZb2016tZb2017tZb2018_B0p5T0p5H0p5Z0p5_Nonecentral.txt --scale --useLog -R center --outputName=AllHadronic



python limit_plot_shape.py --inputFileExp=/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/combinelimslow.txt  --inputFileObs=/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/combinelimsobslow.txt --scale --useLog -R low --outputName=AllHadronicCombine
python limit_plot_shape.py --inputFileExp=/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/combinelimshigh.txt --inputFileObs=/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/combinelimsobshigh.txt --scale --useLog -R high --outputName=AllHadronicCombine
python limit_plot_shape.py --inputFileExp=/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/combinelimscentral.txt --inputFileObs=/afs/cern.ch/work/k/knash/NanoAODskim/NanoAODskim_Analyzer/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/combinelimsobscentral.txt --scale --useLog -R center --outputName=AllHadronicCombine



