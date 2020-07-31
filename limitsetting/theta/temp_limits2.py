# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT

def histogram_filter(hname):
 
    if "q2" in hname:
	return False
    if "btag" in hname:
	return False
    return True

TT_SF_global=1.0
def build_allhad_model(TT_SF_local=1.0,ltype="Mu"):
    files = ["ThetaFile_ttfit_Mu2018_Pt500to600_CNN0p9.root"]

    #HACKY! I HATE MYSELF
    files[0]=files[0].replace("Ele",ltype).replace("Mu",ltype)

    thefile=ROOT.TFile(files[0])

    #tempfile=ROOT.TFile('ThetaFile_TEMP.root','recreate')

    model = build_model_from_rootfile(files, histogram_filter,include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.set_signal_processes('TT_sig')
    print dir(model)
    evs = {}
    for pr in model.processes:

	if not (pr in evs):
		evs[pr] = {}
    	for ob in model.observables:
		name1 = ob+"__"+pr 
		evs[pr][ob] = thefile.Get(name1).Integral()
    print "evs",evs
    TT_SF=TT_SF_global
    #print "scale pass by",TT_SF
    #TT_SF_local*=TT_SF_global

    evs["TT_sig"]["mtop_"+ltype+"pass"]*=1.0/TT_SF

    factor = (evs["TT_sig"]["mtop_"+ltype+"fail"]+evs["TT_sig"]["mtop_"+ltype+"pass"]*TT_SF-evs["TT_sig"]["mtop_"+ltype+"pass"])/evs["TT_sig"]["mtop_"+ltype+"fail"]
    evs["TT_sig"]["mtop_"+ltype+"fail"]*=factor


    #factor_global = (evs["TT_sig"]["mtop_"+ltype+"fail"]+evs["TT_sig"]["mtop_"+ltype+"pass"]*TT_SF-evs["TT_sig"]["mtop_"+ltype+"pass"])/evs["TT_sig"]["mtop_"+ltype+"fail"]
    #model.scale_predictions(1.0/TT_SF,"TT_sig","mtop_"+ltype+"pass")
    #model.scale_predictions(factor,"TT_sig","mtop_"+ltype+"fail")
    for ob in model.observables:
    	for pr in model.processes:

		ptype=pr

		#if pr=="QCD" or pr=="WJetsToLNu":
		#	ptype="bkg"
		if pr.find("TT")!=-1 :
			ptype="TT"
    			model.add_lognormal_uncertainty(ptype+'_rate', math.log(1.5), pr,ob)
		if pr=="QCD" or pr=="WJetsToLNu" or pr=="TT" : 
    			model.add_lognormal_uncertainty('bkg_mistag', math.log(1.5), pr,ob)

		print pr,"type",ptype
		#if pr=="st":
		#	continue
		#print ob,pr,"scalename:", ptype

		if False:
			tnorm = 0.0
			#print evs[pr]
			for key in evs[pr]:
				tnorm += evs[pr][key]
			
			#normval = 1.0*(1.0-evs[pr][ob]/(tnorm))
			

			#print pr,ob,normval
			if ob=="mtop_"+ltype+"fail":

				

				#factor = (tnorm-(evs[pr]["mtop_"+ltype+"pass"]/TT_SF))/evs[pr][ob]
				#factor = (evs[pr][ob]+(evs[pr]["mtop_"+ltype+"pass"]*TT_SF)-evs[pr]["mtop_"+ltype+"pass"])/evs[pr][ob]
				#print "scale fail by",factor


				normval = 1.0*(evs[pr]["mtop_"+ltype+"pass"]/tnorm)
				print normval		
	    			model.add_lognormal_uncertainty(pr+'_tag', -normval, pr,ob)
			if ob=="mtop_"+ltype+"pass":
				normval = 1.0*(evs[pr]["mtop_"+ltype+"fail"]/tnorm)
				print normval		
	    			model.add_lognormal_uncertainty(pr+'_tag', normval, pr,ob)
    return model




#SFstring = "SFemu",str(TT_SF).replace(".","p")


deltaSF = 99999.0
cursf = 1.0
ncount=0
model = build_allhad_model(cursf,"Mu")
modelele = build_allhad_model(cursf,"Ele")

model.combine(modelele)
for p in model.distribution.get_parameters():
	    d = model.distribution.get_distribution(p)
	    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
		model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
		print "dist",p
		if p.find("_tag")!=-1:#  or p=="TT_rate" or  p=="bkg_mistag":
			print "float"
			model.distribution.set_distribution(p, typ = "gauss",mean = 0.0,width = inf, range = [-7.,7.])






posttext = "ThetaFile_ttfit_Mu2018_Pt500to600_CNN0p9.root".replace("ThetaFile_ttfit_PSET_default","").replace(".root","").replace("Mu","").replace("Ele","")



signal_process_groups = {'TT_sig': ['TT_sig']}
myopts = Options()
myopts.set('minimizer', 'strategy', 'robust')
myopts.set('minimizer', 'minuit_tolerance_factor', '50')


parVals = mle(model, input = 'data', n=1, signal_process_groups = signal_process_groups,signal_prior='fix:1.0',options=myopts)
print "-"*20
print parVals
print "-"*20
parameter_values = {}
for p in model.get_parameters(['TT_sig']):
	    #print p
	    parameter_values[p] = parVals['TT_sig'][p][0][0]
#print  parameter_values
histos = evaluate_prediction(model, parameter_values, include_signal = True)


write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst'+posttext+'.root')


parameter_values_AB = {}
for p in model.get_parameters(['TT_sig']):

    if p=="beta_signal":
    	parameter_values_AB[p] = 1.0
    elif  p=="TT_sig_tag":
    	parameter_values_AB[p] = 0.0
    else:
    	parameter_values_AB[p] = parVals['TT_sig'][p][0][0]
#print  parameter_values_AB
histos = evaluate_prediction(model, parameter_values_AB, include_signal = True)
write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-AB'+posttext+'.root')






parameter_values1 = {}
for p in model.get_parameters(['TT_sig']):
    parameter_values1[p] = parVals['TT_sig'][p][0][0]+parVals['TT_sig'][p][0][1]
histos1 = evaluate_prediction(model, parameter_values1, include_signal = True)
write_histograms_to_rootfile(histos1, 'histos-CNN-mleup_syst'+posttext+'.root')
print "post fit full up: ",parameter_values1


parameter_values2 = {}
for p in model.get_parameters(['TT_sig']):
    parameter_values2[p] = parVals['TT_sig'][p][0][0]-parVals['TT_sig'][p][0][1]
histos2 = evaluate_prediction(model, parameter_values2, include_signal = True)
write_histograms_to_rootfile(histos2, 'histos-CNN-mledown_syst'+posttext+'.root')
print
print "Up"
for ip in model.get_parameters(['TT_sig']):
	parameter_values_up = {}
	for jp in model.get_parameters(['TT_sig']):
	    if jp==ip:
	    	parameter_values_up[jp] = parVals['TT_sig'][jp][0][0]+parVals['TT_sig'][jp][0][1]
	    else:
	    	parameter_values_up[jp] = parVals['TT_sig'][jp][0][0]
	print ip
	print parameter_values_up
	histos_up = evaluate_prediction(model, parameter_values_up, include_signal = True)
	write_histograms_to_rootfile(histos_up, 'postfithistos/histos-CNN-'+ip+'up_syst'+posttext+'.root')
print
print "Down"
for ip in model.get_parameters(['TT_sig']):
	parameter_values_down = {}
	for jp in model.get_parameters(['TT_sig']):
	    if jp==ip:
	    	parameter_values_down[jp] = parVals['TT_sig'][jp][0][0]-parVals['TT_sig'][jp][0][1]
	    else:
	    	parameter_values_down[jp] = parVals['TT_sig'][jp][0][0]
	print ip
	print parameter_values_down
	histos_down = evaluate_prediction(model, parameter_values_down, include_signal = True)
	write_histograms_to_rootfile(histos_down, 'postfithistos/histos-CNN-'+ip+'down_syst'+posttext+'.root')




#for p in model.distribution.get_parameters():s
 #   d = model.distribution.get_distribution(p)
  #  if p=="TT_sig_tag":
#	print "lock"
#	model.distribution.set_distribution(p, typ = "gauss",mean = 0.0,width = 0.00000000001, range = [-7.,7.])



#parValspre = mle(model, input = 'data', n=1, signal_process_groups = signal_process_groups,signal_prior='fix:1.0',options=myopts)
#print "Fit result: "
#for ppp in parValspre['TT_sig']: 
#	print ppp,"pre",parValspre['TT_sig'][ppp],"post",parVals['TT_sig'][ppp]
#print "--"
#print "Scale",parValspre['TT_sig']["TT_sig_tag"]
#print "--"



parameter_values_pre = {}
for p in model.get_parameters(['TT_sig']):

    if p=="beta_signal":
    	parameter_values_pre[p] = 1.0
    else:
    	parameter_values_pre[p] = 0.0
print  parameter_values_pre
histos = evaluate_prediction(model, parameter_values_pre, include_signal = True)
write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-pre'+posttext+'.root')


parameter_values_ON = {}
for p in model.get_parameters(['TT_sig']):

    if p=="beta_signal":
    	parameter_values_ON[p] = 1.0
    elif  p!="TT_sig_tag":
    	parameter_values_ON[p] = 0.0
    else:
    	parameter_values_ON[p] = parVals['TT_sig'][p][0][0]
print  parameter_values_ON
histos = evaluate_prediction(model, parameter_values_ON, include_signal = True)
write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-ON'+posttext+'.root')




print
print "Up"
for ip in model.get_parameters(['TT_sig']):
	parameter_values_up = {}
	for jp in model.get_parameters(['TT_sig']):
	    if jp==ip:
	    	parameter_values_up[jp] = parVals['TT_sig'][jp][0][0]+parVals['TT_sig'][jp][0][1]
	    elif jp=="beta_signal":
	    	parameter_values_up[jp] = 1.0
    	    elif jp=="TT_sig_tag":
    		parameter_values_up[jp] = 0.0
	    else:
	    	parameter_values_up[jp] = parVals['TT_sig'][jp][0][0]
	print ip
	print parameter_values_up
	histos_up = evaluate_prediction(model, parameter_values_up, include_signal = True)
	write_histograms_to_rootfile(histos_up, 'prefithistos/histos-CNN-'+ip+'up_syst'+posttext+'.root')
print
print "Down"
for ip in model.get_parameters(['TT_sig']):
	parameter_values_down = {}
	for jp in model.get_parameters(['TT_sig']):
		
	    if jp==ip:
	    	parameter_values_down[jp] = parVals['TT_sig'][jp][0][0]-parVals['TT_sig'][jp][0][1]
	    elif jp=="beta_signal":
	    	parameter_values_down[jp] = 1.0
    	    elif jp=="TT_sig_tag":
    		parameter_values_down[jp] = 0.0
	    else:
	    	parameter_values_down[jp] = parVals['TT_sig'][jp][0][0]
	print ip
	print parameter_values_down
	histos_down = evaluate_prediction(model, parameter_values_down, include_signal = True)
	write_histograms_to_rootfile(histos_down, 'prefithistos/histos-CNN-'+ip+'down_syst'+posttext+'.root')




model_summary(model)
report.write_html('htmlout')

