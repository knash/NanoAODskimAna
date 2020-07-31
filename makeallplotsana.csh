python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016  --normcorr --batch &
#python NanoAODskim_Plotter.py -a tHb -e 2016  --normcorr --batch &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2016  --normcorr --batch --withST &
#python NanoAODskim_Plotter.py -a tZb -e 2016  --normcorr --batch --withST &

python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2017  --normcorr --batch &
#python NanoAODskim_Plotter.py -a tHb -e 2017  --normcorr --batch &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2017  --normcorr --batch --withST &
#python NanoAODskim_Plotter.py -a tZb -e 2017  --normcorr --batch --withST &

python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2018  --normcorr --batch &
#python NanoAODskim_Plotter.py -a tHb -e 2018  --normcorr --batch &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2018  --normcorr --batch --withST &
#python NanoAODskim_Plotter.py -a tZb -e 2018  --normcorr --batch --withST &

python NanoAODskim_Plotter.py -a tHb -e 2016,2017,2018 --batch --qcdmcbkg &
python NanoAODskim_Plotter.py -a tZb -e 2016,2017,2018 --batch --withST --qcdmcbkg &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016,2017,2018 --batch &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2016,2017,2018 --batch --withST &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016,2017,2018  --normcorr --batch &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2016,2017,2018  --normcorr --batch --withST &








python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016   --batch --onlyttnorm --withST  &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2017   --batch --onlyttnorm --withST  &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2018   --batch --onlyttnorm --withST  &









python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016   --batch  --withST  &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2017   --batch  --withST  &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2018   --batch  --withST  &

python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016  --normcorr --batch --skipplots --onlylim -S high &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2016  --normcorr --batch --skipplots --onlylim -S high &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2017  --normcorr --batch --skipplots --onlylim -S high &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2017  --normcorr --batch --skipplots --onlylim -S high &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2018  --normcorr --batch --skipplots --onlylim -S high &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2018  --normcorr --batch --skipplots --onlylim -S high &

python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2016  --normcorr --batch --skipplots --onlylim -S low &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2016  --normcorr --batch --skipplots --onlylim -S low &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2017  --normcorr --batch --skipplots --onlylim -S low &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2017  --normcorr --batch --skipplots --onlylim -S low &
python NanoAODskim_Plotter.py -a tHb -s JetHT -e 2018  --normcorr --batch --skipplots --onlylim -S low &
python NanoAODskim_Plotter.py -a tZb -s JetHT -e 2018  --normcorr --batch --skipplots --onlylim -S low &
