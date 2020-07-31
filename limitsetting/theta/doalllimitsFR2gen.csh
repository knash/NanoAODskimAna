source setuptheta.csh
rm -rf analysis
cp analysis_FR2_limits_genv.py  temp_limits.py
python run_theta.py --file=temp_limits.py

