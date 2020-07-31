# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT

def histogram_filter_partial(hname):
 
    if "q2" in hname:
	return False
    if "tptrw" in hname:
	return False
    if "btag" in hname:
	return False
    if "semi_tag" in hname:
	return False

    #if "bmerge_tag" in hname:
	#return False
    return True

def histogram_filter_all(hname):
    if "semi_tag" in hname:
	return False
    return True

def histogram_filter_sigonly(hname):
    if "q2" in hname:
	return False
    if ('TT_sig' in hname) or ('TT_bmerge' in hname):
	return True
    if (("minus" in hname) or ("plus" in hname)):
	return False
    if "semi_tag" in hname:
	return False
    return True

def histogram_filter_nosyst(hname):
 

    if (("minus" in hname) or ("plus" in hname)) and (not "_tag" in hname):
	return False
    if "semi_tag" in hname:
	return False
    return True


def histogram_filter_none(hname):
 
    if (("minus" in hname) or ("plus" in hname)):
	return False
    return True

TT_SF_global=1.0
sigstr=""
unc1=False 
unc2=False
unc3=True 
unc4=False 
#bsum=True
def build_allhad_model(TT_SF_local=1.0,ltype="Mu",cfile=""):
    files = [cfile]
    print "cfile",cfile
    exstr=cfile[cfile.find("Pt"):cfile.find(".root")]+"_"
    #HACKY! I HATE MYSELF
    files[0]=files[0].replace("Ele",ltype).replace("Mu",ltype)

    thefile=ROOT.TFile(files[0])



    #model = build_model_from_rootfile(files, histogram_filter_all,include_mc_uncertainties=True)

    if unc1:
    	model = build_model_from_rootfile(files, histogram_filter_sigonly,include_mc_uncertainties=True)
    elif unc2:
    	model = build_model_from_rootfile(files, histogram_filter_nosyst,include_mc_uncertainties=True)
    elif unc3:
    	model = build_model_from_rootfile(files, histogram_filter_partial,include_mc_uncertainties=True)
    elif unc4:
    	model = build_model_from_rootfile(files, histogram_filter_none,include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    print dir(model)
    evs = {}
    for pr in model.processes:
	print pr
	if not (pr in evs):
		evs[pr] = {}
    	for ob in model.observables:
		name1 = ob+"__"+pr 
		evs[pr][ob] = thefile.Get(name1).Integral()
 		for par in model.distribution.get_parameters():
	
			try:
				print "par",par,thefile.Get(name1+"__"+par+"__minus").Integral()-evs[pr][ob],thefile.Get(name1+"__"+par+"__plus").Integral()-evs[pr][ob]
				
			except:
				print "none"
    TT_SF=TT_SF_local
    if not unc4:
	    evs['TT_sig']["mtop_"+exstr+ltype+"pass"]*=1.0/TT_SF

	    factor = (evs['TT_sig']["mtop_"+exstr+ltype+"fail"]+evs['TT_sig']["mtop_"+exstr+ltype+"pass"]*TT_SF-evs['TT_sig']["mtop_"+exstr+ltype+"pass"])/evs['TT_sig']["mtop_"+exstr+ltype+"fail"]
	    evs['TT_sig']["mtop_"+exstr+ltype+"fail"]*=factor

	    print "factors",factor,TT_SF

	    model.scale_predictions(1.0/TT_SF,'TT_sig',"mtop_"+exstr+ltype+"pass")
	    model.scale_predictions(factor,'TT_sig',"mtop_"+exstr+ltype+"fail")
    #model.scale_predictions((evs["QCD"]["mtop_"+exstr+ltype+"pass"]+evs["WJetsToLNu"]["mtop_"+exstr+ltype+"pass"])/evs["WJetsToLNu"]["mtop_"+exstr+ltype+"pass"],"WJetsToLNu","mtop_"+exstr+ltype+"pass")
    #model.scale_predictions((evs["QCD"]["mtop_"+exstr+ltype+"fail"]+evs["WJetsToLNu"]["mtop_"+exstr+ltype+"fail"])/evs["WJetsToLNu"]["mtop_"+exstr+ltype+"fail"],"WJetsToLNu","mtop_"+exstr+ltype+"fail") 
    #model.scale_predictions(0.0,"QCD","*")
    floatnum=1.2
    for ob in model.observables:
	print ob
	lepst=""
	if ob.find("Ele")!=-1:
		lepst="Ele"
	if ob.find("Mu")!=-1:
		lepst="Mu"
	ptstr=ob[ob.find("Pt"):ob.find("_CNN")]
	passf=ob[-4:]
	if ob.find("Mu")!=-1:
		lepst="Mu"
    	for pr in model.processes:
	
		ptype=pr
   	 	if unc1 or unc3:
			if pr=="QCD" or pr=="WJetsToLNu" or pr=="TT": 
				ptype="bkg"
	    			model.add_lognormal_uncertainty(ptype+'_rate'+exstr+lepst, math.log(floatnum), pr,ob)
			if pr in ["TT_semi"]:
	    			model.add_lognormal_uncertainty(pr+'_rate'+exstr+lepst, math.log(floatnum), pr,ob)
   	 	if unc2:
			if pr=="QCD" or pr=="WJetsToLNu" or pr=="TT": 
				ptype="bkg"
	    			model.add_lognormal_uncertainty(ptype+'_rate'+exstr+lepst, math.log(floatnum), pr,ob)
			if pr in ["TT_semi"]:
	    			model.add_lognormal_uncertainty(pr+'_rate'+ob, math.log(floatnum), pr,ob)
   	 	if unc4:
			if pr=="QCD" or pr=="WJetsToLNu" or pr=="TT": 
				ptype="bkg"
	    			model.add_lognormal_uncertainty(ptype+'_rate'+ptstr+passf, math.log(floatnum), pr,ob)
			else:
				model.add_lognormal_uncertainty(pr+'_rate'+ptstr+passf, math.log(floatnum), pr,ob)
   	 	if unc1:
			if pr.find("TT")!=-1  :
				ptype="TT"
    				model.add_lognormal_uncertainty(ptype+'_rate'+exstr+lepst, math.log(floatnum), pr,ob)
		elif unc2:
			if pr.find("TT")!=-1 and pr!="TT" and pr!="TT_semi" :
				ptype="TT"
    				model.add_lognormal_uncertainty(pr+'_rate'+exstr+lepst, math.log(floatnum), pr,ob)
		elif unc3:
			if pr.find("TT")!=-1 and pr!="TT" and pr!="TT_semi" :
				ptype="TT"
    				model.add_lognormal_uncertainty(pr+'_rate'+exstr+lepst, math.log(floatnum), pr,ob)


    return model




#SFstring = "SFemu",str(TT_SF).replace(".","p")


deltaSF = 99999.0
cursfs = [0.8,0.82,0.84,0.86,0.88,0.9,0.92,0.94,0.96,0.98,1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14,1.16,1.18,1.2]
cursfs = [1.0]
ncount=0

ptsels="RFILE".split(",")
for cursf in  cursfs:
		
	models=[]
	for iff,ff in enumerate(ptsels):
		#print ff
		models.append(build_allhad_model(cursf,"Mu","ThetaFile_ttfit_Mu"+ff+".root"))
		models.append(build_allhad_model(cursf,"Ele","ThetaFile_ttfit_Ele"+ff+".root"))
	for iff,ff in enumerate(models):
		if iff==0:
			model=models[iff]
		else:
			model.combine(models[iff])
	for p in model.distribution.get_parameters():
		    d = model.distribution.get_distribution(p)
		    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
			model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
			print "dist",p
			#if p.find("_tag")!=-1:
			if p.find("_tag")!=-1 or p.find("_rate")!=-1:
				print "float"
				model.distribution.set_distribution(p, typ = "gauss",mean = 0.0,width = inf, range = [-10.,10.])





	posttext = "ALL"

	if str(cursf)!="1.0":
		posttext+=str(cursf).replace(".","p")

	signal_process_groups = {sigstr: [sigstr]}
	myopts = Options()
	myopts.set('minimizer', 'strategy', 'robust')
	myopts.set('minimizer', 'minuit_tolerance_factor', '40')
	myopts.set('minimizer', 'mcmc_iterations', '100000')

	print "running",cursf
	#parVals = mle(model, input = 'data', n=20, signal_process_groups = signal_process_groups,signal_prior='fix:1.0',options=myopts)






	#ngroups=4
	#obl=[]
        #for ib,ob in enumerate(sorted(model.observables)):
	#	print ib,ob,ib%ngroups
	#	obl.append(ob)
	#	if len(obl)==ngroups:
	#		print obl
	#		copym=copy.deepcopy(model)
	#		copym.restrict_to_observables(obl)
	#		parVals = mle(copym, input = 'data', n=1, with_error = True, signal_process_groups = {'': []},chi2=True,options=myopts)
	#		print parVals
	parVals = mle(model, input = 'data', n=1, with_error = True, signal_process_groups = {'': []},chi2=True,options=myopts)




	#parVals = bayesian_posterior_model_prediction(model, input = 'data', n=20, signal_process_groups={'': []}, options=myopts)
	#print pl_interval(model, input = 'data', n=1,cls = [cl_1sigma] ,signal_process_groups = {'': []}, options=myopts,parameter = 'TT_sig_tag_Pt575to650_CNN0p9')	
	print "-"*20
	print parVals
	print "-"*20
	parameter_values = {}
	for p in model.get_parameters([]):
		    #print p
		    parameter_values[p] = parVals[sigstr][p][0][0]
	print  parameter_values
	histos = evaluate_prediction(model, parameter_values, include_signal = True)
	print "dirh",dir(histos)

	write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst'+posttext+'.root')


	parameter_values_AB = {}
	for p in model.get_parameters([]):
	    #print p
	    if p=="beta_signal":
	    	parameter_values_AB[p] = 1.0
	    elif  p.find("TT_sig_tag")!=-1:
	    	parameter_values_AB[p] = 0.0
	    else:
	    	parameter_values_AB[p] = parVals[sigstr][p][0][0]
	#print  parameter_values_AB
	histos = evaluate_prediction(model, parameter_values_AB, include_signal = True)
	write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-AB'+posttext+'.root')




	parameter_values1 = {}
	for p in model.get_parameters([]):
	    parameter_values1[p] = parVals[sigstr][p][0][0]+parVals[sigstr][p][0][1]
	histos1 = evaluate_prediction(model, parameter_values1, include_signal = True)
	write_histograms_to_rootfile(histos1, 'histos-CNN-mleup_syst'+posttext+'.root')
	#print "post fit full up: ",parameter_values1


	parameter_values2 = {}
	for p in model.get_parameters([]):
	    parameter_values2[p] = parVals[sigstr][p][0][0]-parVals[sigstr][p][0][1]
	histos2 = evaluate_prediction(model, parameter_values2, include_signal = True)
	write_histograms_to_rootfile(histos2, 'histos-CNN-mledown_syst'+posttext+'.root')
	#print
	#print "Up"
	for ip in model.get_parameters([]):
		parameter_values_up = {}
		for jp in model.get_parameters([]):
		    if jp==ip:
		    	parameter_values_up[jp] = parVals[sigstr][jp][0][0]+parVals[sigstr][jp][0][1]
		    else:
		    	parameter_values_up[jp] = parVals[sigstr][jp][0][0]
		#print ip
		#print parameter_values_up
		histos_up = evaluate_prediction(model, parameter_values_up, include_signal = True)
		write_histograms_to_rootfile(histos_up, 'postfithistos/histos-CNN-'+ip+'up_syst'+posttext+'.root')
	#print
	#print "Down"
	for ip in model.get_parameters([]):
		parameter_values_down = {}
		for jp in model.get_parameters([]):
		    if jp==ip:
		    	parameter_values_down[jp] = parVals[sigstr][jp][0][0]-parVals[sigstr][jp][0][1]
		    else:
		    	parameter_values_down[jp] = parVals[sigstr][jp][0][0]
		#print ip
		#print parameter_values_down
		histos_down = evaluate_prediction(model, parameter_values_down, include_signal = True)
		write_histograms_to_rootfile(histos_down, 'postfithistos/histos-CNN-'+ip+'down_syst'+posttext+'.root')




	#for p in model.distribution.get_parameters():s
	 #   d = model.distribution.get_distribution(p)
	  #  if p=="TT_sig_tag":
	#	print "lock"
	#	model.distribution.set_distribution(p, typ = "gauss",mean = 0.0,width = 0.00000000001, range = [-7.,7.])



	#parValspre = mle(model, input = 'data', n=1, signal_process_groups = signal_process_groups,signal_prior='fix:1.0',options=myopts)
	#print "Fit result: "
	#for ppp in parValspre[sigstr]: 
	#	print ppp,"pre",parValspre[sigstr][ppp],"post",parVals[sigstr][ppp]
	#print "--"
	#print "Scale",parValspre[sigstr]["TT_sig_tag"]
	#print "--"



	parameter_values_pre = {}
	for p in model.get_parameters([]):

	    if p=="beta_signal":
	    	parameter_values_pre[p] = 1.0
	    else:
	    	parameter_values_pre[p] = 0.0
	#print  parameter_values_pre
	histos = evaluate_prediction(model, parameter_values_pre, include_signal = True)
	write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-pre'+posttext+'.root')


	parameter_values_ON = {}
	for p in model.get_parameters([]):

	    if p=="beta_signal":
	    	parameter_values_ON[p] = 1.0
	    elif  p.find("TT_sig_tag")!=-1:
	    	parameter_values_ON[p] = 0.0
	    else:
	    	parameter_values_ON[p] = parVals[sigstr][p][0][0]
	#print  parameter_values_ON
	histos = evaluate_prediction(model, parameter_values_ON, include_signal = True)
	write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-ON'+posttext+'.root')




	print
	print "Up"
	for ip in model.get_parameters([]):
		parameter_values_up = {}
		for jp in model.get_parameters([]):
		    if jp==ip:
		    	parameter_values_up[jp] = parVals[sigstr][jp][0][0]+parVals[sigstr][jp][0][1]
		    elif jp=="beta_signal":
		    	parameter_values_up[jp] = 1.0
	    	    elif jp.find("TT_sig_tag")!=-1:
	    		parameter_values_up[jp] = 0.0
		    else:
		    	parameter_values_up[jp] = parVals[sigstr][jp][0][0]
		#print ip
		#print parameter_values_up
		histos_up = evaluate_prediction(model, parameter_values_up, include_signal = True)
		write_histograms_to_rootfile(histos_up, 'prefithistos/histos-CNN-'+ip+'up_syst'+posttext+'.root')
	print
	print "Down"
	for ip in model.get_parameters([]):
		parameter_values_down = {}
		for jp in model.get_parameters([]):
			
		    if jp==ip:
		    	parameter_values_down[jp] = parVals[sigstr][jp][0][0]-parVals[sigstr][jp][0][1]
		    elif jp=="beta_signal":
		    	parameter_values_down[jp] = 1.0
	    	    elif jp.find("TT_sig_tag")!=-1:
	    		parameter_values_down[jp] = 0.0
		    else:
		    	parameter_values_down[jp] = parVals[sigstr][jp][0][0]
		#print ip
		#print parameter_values_down
		histos_down = evaluate_prediction(model, parameter_values_down, include_signal = True)
		write_histograms_to_rootfile(histos_down, 'prefithistos/histos-CNN-'+ip+'down_syst'+posttext+'.root')



	parameter_values_AB = {}

	for p in model.get_parameters([]):
	    #print p
	    if p=="beta_signal":
	    	parameter_values_AB[p] = 1.0
	    elif  p.find("TT_bmerge_tag")!=-1:
		#print "bmerge"
	    	parameter_values_AB[p] = 0.0
	    else:
	    	parameter_values_AB[p] = parVals[sigstr][p][0][0]
	#print  parameter_values_AB
	histos = evaluate_prediction(model, parameter_values_AB, include_signal = True)
	write_histograms_to_rootfile(histos, 'histos-CNN-mle_syst-AB'+posttext+'_bmerge.root')

model_summary(model)
report.write_html('htmlout')

