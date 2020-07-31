

import array, math, ROOT
ROOT.gROOT.LoadMacro("insertlogo.C+")
def Inter(g1,g2):
	xaxisrange = g1.GetXaxis().GetXmax()-g1.GetXaxis().GetXmin()
	xaxismin = g1.GetXaxis().GetXmin()
	inters = []
	for x in range(0,10000):
		xpoint = xaxismin + (float(x)/1000.0)*xaxisrange
		xpoint1 = xaxismin + (float(x+1)/1000.0)*xaxisrange
		Pr1 = g1.Eval(xpoint)
		Pr2 = g2.Eval(xpoint)
		Po1 = g1.Eval(xpoint1)
		Po2 = g2.Eval(xpoint1)
		if (Pr1-Pr2)*(Po1-Po2)<0:
			inters.append(0.5*(xpoint+xpoint1))
		
	return inters
			
def strf( x ):
	return '%.3f' % x

def strf1( x ):
	return '%.0f' % x
	

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileExp', metavar='H', type='string', action='store',
                  default='limits_shape_exp.txt',
                  dest='inputFileExp',
                  help='Expected limits from theta')

parser.add_option('--inputFileObs', metavar='H', type='string', action='store',
                  default='limits_shape_obs.txt',
                  dest='inputFileObs',
                  help='Observed limits from theta')

parser.add_option('--outputName', metavar='D', type='string', action='store',
                  default='comb',
                  dest='outputName',
                  help='Directory to plot')

parser.add_option('--title', metavar='D', type='string', action='store',
                  default='narrow',
                  dest='title',
                  help='Titles to use, options are narrow, wide, kkg')

parser.add_option('--showNarrowTheory', action='store_true',
                  default=False,
                  dest='showNarrowTheory',
                  help='Show theory prediction for 1% width')

parser.add_option('--showWideTheory', action='store_true',
                  default=False,
                  dest='showWideTheory',
                  help='Show theory prediction for 3% width')

parser.add_option('--showKKGTheory', action='store_true',
                  default=False,
                  dest='showKKGTheory',
                  help='Show theory prediction for KK Gluon')

parser.add_option('--useLog', metavar='L', action='store_true',
                  default=False,
                  dest='useLog',
                  help='use log y-axis')

parser.add_option('--scale', metavar='T', action='store_true',
                  default=False,
                  dest='scale',
                  help='scale')

parser.add_option('--blind', metavar='T', action='store_true',
                  default=False,
                  dest='blind',
                  help='blind')

parser.add_option('-R', '--region', metavar='F', type='string', action='store',
                  default	=	'center',
                  dest		=	'region',
                  help		=	'sigscale')


(options, args) = parser.parse_args()

argv = []

import NanoAODskim_Functions	
from NanoAODskim_Functions import *
print options.inputFileObs
gROOT.Macro("rootlogon.C")
#VLQbuddy = {'1500':'1000','2000':'1300','2500':'1500','3000':'1800'}
VLQbuddy = {}
#Outf   =   open("pdfw.csv", "r")
#Outfr = Outf.read()
#Outspl = Outfr.split('\n')
#csunc = {}
#for outl in Outspl:
#	tempoutspl = outl.split(',')
#	if len(tempoutspl)<3:
#		continue 
#	tempoutspl = outl.split(',')
#	string = tempoutspl[0].replace("THBWp","").replace("Tp","").replace("Bp","")
#	csunc[string+"__PDF__plus"]=float(tempoutspl[1])
#	csunc[string+"__PDF__minus"]=float(tempoutspl[2])

#print "extracted pdf uncertatainty:   "+str(csunc)
#WprimeConvo = (1.0)*(0.25)*(0.50)
NanoAODskimData= NanoAODskim_Data("COMB")
sigxsecdict=NanoAODskimData.sigxsecdict
sigbrdict=NanoAODskimData.sigbrdict
genmatrix=NanoAODskimData.genmatrix
print sigxsecdict
print sigbrdict

sigxsecdictinterp=NanoAODskimData.sigxsecdictinterp
sigbrdictinterp=NanoAODskimData.sigbrdictinterp

#if options.region=='low':
#	mindex=0
#if options.region=='center':
#	mindex=1
#if options.region=='high':
#	mindex=2




gROOT.Macro("rootlogon.C")

def make_smooth_graph(h2,h3):
    h2 = TGraph(h2)
    h3 = TGraph(h3)
    npoints = h3.GetN()
    h3.Set(2*npoints+2)
    for b in range(npoints+2):
        x1, y1 = (ROOT.Double(), ROOT.Double())
        if b == 0:
            h3.GetPoint(npoints-1, x1, y1)
        elif b == 1:
            h2.GetPoint(npoints-b, x1, y1)
        else:
            h2.GetPoint(npoints-b+1, x1, y1)
        h3.SetPoint(npoints+b, x1, y1)
    return h3

if __name__ == "__main__":
    ROOT.gROOT.Macro("rootlogon.C")
    TPT = ROOT.TPaveText(.20, .63, .43, .7,"NDC")
    TPT1 = ROOT.TPaveText(.20, .57, .43, .63 ,"NDC")


    if options.region=="low":
    	TPT.AddText("Low VLQ mass")
    	TPT1.AddText("m_{VLQ} ~ 1/2m_{W'}")
    if options.region=="center":
    	TPT.AddText("Medium VLQ mass")
    	TPT1.AddText("m_{VLQ} ~ 2/3m_{W'}")
    if options.region=="high":
    	TPT.AddText("High VLQ mass")
    	TPT1.AddText("m_{VLQ} ~ 3/4m_{W'}")

    pdfarray=["pdfuncs2016.txt","pdfuncs2017.txt","pdfuncs2018.txt"]
    

    TPT.SetFillColor(0)
    TPT.SetBorderSize(0)
    TPT.SetTextAlign(12)


    TPT1.SetFillColor(0)
    TPT1.SetBorderSize(0)
    TPT1.SetTextAlign(12)



    #masses = [1500,2000,2500,3000,3500,4000,4500,5000] 
    masses = [1500,2000,2500,3000,3500,4000,4500,5000] 
    intermasses = [1500,1600,1700,1800,1900,2000,2500,2600,2700,2800,2900,3000,3100,3200,3300,3400,3500,3600,3700,3800,3900,4000,4100,4200,4300,4400,4500,4600,4700,4800,4900] 

    x_mass = array('d')
    y_limit = array('d')
    y_mclimit  = array('d')
    y_mclimitlow68 = array('d')
    y_mclimitup68 = array('d')
    y_mclimitup95 = array('d')
    y_mclimitlow95 = array('d')
    


    VLQbuddy={}
    for sigsets in genmatrix:
		awpmass = sigsets[0]
		centindex=(int(len(sigsets[1])/2))
		if options.region=='low':
			centindex-=1
		if options.region=='high':
			centindex+=1
		vlqmass = sigsets[1][centindex]
		VLQbuddy[str(awpmass)]=str(vlqmass)



    print "VLQbuddy",VLQbuddy


    pdfdict={}
    for p in pdfarray:
	with open(p, "r") as pdff: 
		readl=pdff.readlines()
		found=False
		for ll in readl:

			curl = ll.split(",")[0]
			curlwp=curl.split("_")[1][2:6].replace("N","")
			curlvlq=curl.split("_")[2][2:6].replace("N","")

			valdown=float(ll.split(",")[1].replace("\n",""))
			valup=float(ll.split(",")[2].replace("\n",""))

			print curlwp+curlvlq,valdown,valup
			if valdown>0.6 or valup>0.6:
				print "badval"
				continue
			if not (curlwp+curlvlq in pdfdict):
				pdfdict[curlwp+curlvlq]=[[valdown],[valup]]
			else:
				pdfdict[curlwp+curlvlq][0].append(valdown)
				pdfdict[curlwp+curlvlq][1].append(valup)
    #print pdfdict
	
    logScale = options.useLog
    print options.inputFileExp
    print options.inputFileObs
    f1 = file(options.inputFileExp, "r").readlines()
    if (not options.blind) :
    	f2 = file(options.inputFileObs, "r").readlines()

    # i = 0
    expvals = []
    for line in f1[1:]:

        data = map(float,line.split())
        x_mass.append( data[0]/1000.0  )    # mass
	wpm=line.split()[0]
	curxsec=sigxsecdict[wpm]
	vlq = VLQbuddy[wpm]
	curbr=(sigbrdict[wpm+vlq]["Tp"]+sigbrdict[wpm+vlq]["Bp"])


        
        #print data
        # data is an array along the line, has 8 entries

        #y_limit.append( data[1] )
	rt_xsec=1.0
    	if (options.scale) :
		rt_xsec = curbr*curxsec
	y_mclimit.append( data[1]*rt_xsec )
	#print data[1]*rt_xsec
	y_mclimitlow95.append( data[2]*rt_xsec )
	y_mclimitup95.append( data[3]*rt_xsec )
	y_mclimitlow68.append( data[4]*rt_xsec )
	y_mclimitup68.append( data[5]*rt_xsec )
	
    print "y_mclimit",y_mclimit
    # i = 0
    if (not options.blind) :
	    for line in f2[1:]:

		data = map(float,line.split())
		wpm=line.split()[0]
		curxsec=sigxsecdict[wpm]
		vlq = VLQbuddy[wpm]
		curbr=(sigbrdict[wpm+vlq]["Tp"]+sigbrdict[wpm+vlq]["Bp"])

		#print data[1]*rt_xsec
		rt_xsec=1.0
	    	if (options.scale) :
			rt_xsec = curbr*curxsec

		y_limit.append( data[1]*rt_xsec )
		print data[1]*rt_xsec 
    print "y_limit",y_limit	 

    cv = TCanvas("cv", "cv",900, 700)
    #cv = TCanvas("cv", "cv")
    if logScale:
        cv.SetLogy(True)
    cv.SetLeftMargin(.18)
    cv.SetBottomMargin(.18)   

    if (not options.blind) : 
	    g_limit = TGraph(len(x_mass), x_mass, y_limit)	

	    g_limit.SetTitle("")
	    g_limit.SetMarkerStyle(0)
	    g_limit.SetMarkerColor(1)
	    g_limit.SetLineColor(1)
	    g_limit.SetLineWidth(3)
	    g_limit.SetMarkerSize(0.5) #0.5

	    g_limit.GetXaxis().SetTitle("M_{W'_{R}} (TeV)")
	    g_limit.GetYaxis().SetTitle("Upper Limit #sigma_{W'_{R}} #times B(W'_{R}#rightarrowtb) [pb]")

	    g_limit.Draw("alp")
	    g_limit.GetYaxis().SetRangeUser(0., 80.)
	    g_limit.GetXaxis().SetRangeUser(1.0, 2.9)
	    if logScale:
		g_limit.SetMinimum(1.0e-4) #0.005
		g_limit.SetMaximum(4000.) #10000
	    else:
		# g_limit.SetMaximum(80.)
		g_limit.SetMaximum(0.5)#20.)

	    g_limit.Draw("al")		#uncomm later
	    
    g_mclimit = TGraph(len(x_mass), x_mass, y_mclimit)
    g_mclimit.SetTitle("")
    g_mclimit.SetMarkerStyle(21)
    g_mclimit.SetMarkerColor(1)
    g_mclimit.SetLineColor(1)
    g_mclimit.SetLineStyle(2)
    g_mclimit.SetLineWidth(3)
    g_mclimit.SetMarkerSize(0.)
    g_mclimit.GetXaxis().SetTitle("m_{W'} (TeV)")
    g_mclimit.GetYaxis().SetTitle("#sigma_{W'} #times #bf{#it{#Beta}}( W'#rightarrow (Tb,tB)) (pb)")
    #g_mclimit.GetYaxis().SetTitle("Upper Limit #sigma_{W'} #times #bf{#it{#Beta}}( W' #rightarrow (Tb,tB) #rightarrow tHb) (pb)")

    g_mclimit.GetYaxis().SetTitleSize(0.05)
    g_mclimit.GetYaxis().SetTitleOffset(1.2)

    g_mclimit.GetXaxis().SetTitleSize(0.05)
    g_mclimit.GetXaxis().SetTitleOffset(1.2)
    g_mclimit.Draw("al")
    g_mclimit.GetYaxis().SetRangeUser(0., 80.)
    if logScale:
		g_mclimit.SetMinimum(5.0e-4) #0.005
		g_mclimit.SetMaximum(300.) #10000
    else:
		# g_limit.SetMaximum(80.)
		g_mclimit.SetMaximum(0.5)#20.)


    g_mcplus = TGraph(len(x_mass), x_mass, y_mclimitup68)
    g_mcminus = TGraph(len(x_mass), x_mass, y_mclimitlow68)
    
    g_mc2plus = TGraph(len(x_mass), x_mass, y_mclimitup95)
    g_mc2minus = TGraph(len(x_mass), x_mass, y_mclimitlow95)

    graphWPv = ROOT.TGraph()
    graphWPupv = ROOT.TGraph()
    graphWPdownv = ROOT.TGraph()

    q = 0
    print "Theory lines"
    sigstr = []
    xbr=[]
    for wpmass in masses:
	wpm=str(wpmass)
	curxsec=sigxsecdict[wpm]
	vlq = VLQbuddy[wpm]
	curbr=(sigbrdict[wpm+vlq]["Tp"]+sigbrdict[wpm+vlq]["Bp"])
	pdarr=pdfdict[wpm+vlq]
	pdavedown = sum(pdarr[0])/len(pdarr[0])
	pdaveup = sum(pdarr[1])/len(pdarr[1])
	print wpm,curbr,curxsec,pdaveup,pdavedown
	#print pdarr[0],pdarr[1]
	rt_xsec = curbr*curxsec
	
	sigstr.append(rt_xsec)
	xbr.append([wpmass,vlq,rt_xsec])
    	graphWPv.SetPoint(q,    wpmass/1000. ,    rt_xsec   )
    	graphWPupv.SetPoint(q,    wpmass/1000. ,    rt_xsec*(1.+pdaveup)   )
    	graphWPdownv.SetPoint(q,    wpmass/1000. ,    rt_xsec*(1.-pdavedown)   )
	q+=1

    if options.region=='low':
		mindex=0
    if options.region=='center':
		mindex=1
    if options.region=='high':
		mindex=2
    q = 0
    graphWP = ROOT.TGraph()
    graphWP.SetTitle("")
    graphWP.SetMarkerStyle(23)
    graphWP.SetMarkerColor(4)
    graphWP.SetLineColor(4)
    graphWP.SetLineWidth(2)
    graphWP.SetMarkerSize(0.5)

    graphWPup = ROOT.TGraph()
    graphWPup.SetTitle("")
    graphWPup.SetMarkerStyle(23)
    graphWPup.SetMarkerColor(4)
    graphWPup.SetLineColor(4)
    graphWPup.SetLineWidth(1)
    graphWPup.SetLineStyle(2)
    graphWPup.SetMarkerSize(0.5)

    graphWPdown = ROOT.TGraph()
    graphWPdown.SetTitle("")
    graphWPdown.SetMarkerStyle(23)
    graphWPdown.SetMarkerColor(4)
    graphWPdown.SetLineColor(4)
    graphWPdown.SetLineWidth(1)
    graphWPdown.SetLineStyle(2)
    graphWPdown.SetMarkerSize(0.5)

    curbr=0.
    for wpmass in intermasses:
	#print wpmass
	#print sigxsecdictinterp
	curxsec = sigxsecdictinterp[str(wpmass)]
	#print sigxsecdictinterp,str(wpmass),sigxsecdictinterp[str(wpmass)]
	fvls=[]

	for xx in sigbrdictinterp:
		#print xx
		if xx[0:4]==str(wpmass):
			fvls.append(int(xx[4:]))
    	fvls=sorted(fvls)
	#print fvls
	dstr=str(wpmass)+str(fvls[mindex])
	#print dstr,sigbrdictinterp[dstr]
	#if sigbrdictinterp[dstr]=={}:
	#	rt_xsec=curbr*curxsec
	#	graphWPinterp.SetPoint(q,    wpmass/1000. ,    rt_xsec   )
	#	print "skipping"
	#	continue
		
	curbr=sigbrdictinterp[dstr]["Tp"]+sigbrdictinterp[dstr]["Bp"]
	


	pdaveup=abs(graphWPupv.Eval(wpmass/1000.)-graphWPv.Eval(wpmass/1000.))
	pdavedown=abs(graphWPv.Eval(wpmass/1000.)-graphWPdownv.Eval(wpmass/1000.))
	#print wpmass,rt_xsec,pdaveup

	#xsec fit breaks for high mass "low"
	if options.region=='low' and (wpmass/1000.)>3.:
		if not (wpmass in masses):
			continue
		else:
			rt_xsec = graphWPv.Eval(wpmass/1000.)
	else:
		rt_xsec = curbr*curxsec
	print wpmass/1000.,curbr,curxsec,pdaveup,pdavedown
	print wpmass/1000.,dstr,rt_xsec

    	graphWP.SetPoint(q,    wpmass/1000. ,    rt_xsec   )
    	graphWPup.SetPoint(q,    wpmass/1000. ,    rt_xsec+pdaveup   )
    	graphWPdown.SetPoint(q,    wpmass/1000. ,    rt_xsec-pdavedown   )

    	#graphWPinterp.SetPoint(q,    wpmass/1000. ,    rt_xsec   )
	q+=1



    q=0
    #for im in xrange(35):
	#wpmass=1500+im*100
	#wpmasstev= float(wpmass)/1000.
	#rt_xsec=graphWPinterp.Eval(wpmasstev)
	#pdaveup=abs(graphWPupv.Eval(wpmasstev)-graphWPv.Eval(wpmasstev))
	#pdavedown=abs(graphWPv.Eval(wpmasstev)-graphWPdownv.Eval(wpmasstev))
	#print wpmass,rt_xsec,pdaveup
    	#graphWP.SetPoint(q,    wpmasstev ,    rt_xsec   )
    	#graphWPup.SetPoint(q,    wpmasstev ,    rt_xsec*(1.+pdaveup)   )
    	#graphWPdown.SetPoint(q,    wpmasstev ,    rt_xsec*(1.-pdavedown)   )

	#print  graphWPinterp.Eval(wpmasstev),graphWP.Eval(wpmasstev)
    	#q+=1

    #graphWPinterp.SetLineWidth(3)
    #graphWPinterp.SetLineColor(2)
    graphWP.SetLineWidth(3)
    graphWP.SetLineColor(4 )


    g_error95 = make_smooth_graph(g_mc2minus, g_mc2plus)
    g_error95.SetFillColor(ROOT.kOrange)
    g_error95.SetLineColor(0)
    g_error95.Draw("lf")
    g_error95.Draw("lf")
    
    g_error = make_smooth_graph(g_mcminus, g_mcplus)
    g_error.SetFillColor( ROOT.kGreen+1)
    g_error.SetLineColor(0)
    g_error.Draw("lf")
    g_error.Draw("lf")
   

 

    g_mclimit.Draw("l")
    graphWP.Draw("l")
    graphWPup.Draw("l")
    graphWPdown.Draw("l")
    if (not options.blind) :
    	g_limit.Draw("p l same")
    #graphWPinterp.Draw("l")
	
    legLabel = ""
    if logScale:
	  legend = TLegend(0.47, 0.45, 0.86, 0.84, legLabel)
    else:
	  legend = TLegend(0.47, 0.35, 0.86, 0.75, legLabel)
    if (not options.blind):
    	legend.AddEntry(g_limit, "Observed limit (95% CL)","l")
    legend.AddEntry(g_mclimit, "Expected limit (95% CL)","l")
    legend.AddEntry(g_error, "68% expected", "f")
    legend.AddEntry(g_error95, "95% expected", "f")

    legend.AddEntry(graphWP, "W' signal", "l")
    legend.AddEntry(graphWPup, "#splitline{W' signal}{PDF+scale uncertainty}", "l")   



    if (not options.blind):
	g_limit.GetYaxis().SetTitleOffset(1.4)


    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    
    text1 = ROOT.TLatex()
    text1.SetNDC()
    text1.SetTextFont(42)
    
    text11 = ROOT.TLatex()
    text11.SetTextFont(42)
    text11.SetNDC()

    label = "temp"
  
    text2 = ROOT.TLatex(3.570061, 23.08044, label)
    text2.SetNDC()
    text2.SetTextAlign(13)
    text2.SetX(0.4) #0.32
    text2.SetY(0.8) #0.87
    #text2.SetW(0.5)
    text2.SetTextFont(42)

    ROOT.insertlogo( cv, 5, 11 )	
    legend.Draw("same")



    postpend = options.outputName
    if logScale:
        postpend = postpend + "_log"
    if options.blind :
        postpend = postpend + "_blind"
    TPT.Draw()
    TPT1.Draw()	
    cv.RedrawAxis()

    print "name is limits_theta_"+postpend+options.region
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".pdf")
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".gif")
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".png")
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".root")
    if (not options.blind) :
	    obs = Inter(g_limit,graphWP)
	    exp = Inter(g_mclimit,graphWP)


	    print "intersections:"
	    print "Observed"
	    for i in range(0,len(obs)): 
	    	print str(obs[i]) 
	    print "Experimental"
	    for i in range(0,len(exp)): 
	    	print str(exp[i]) 


print xbr





