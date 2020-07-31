
#! /usr/bin/env python
import os
import copy
from math import *
import sys
sys.path.append('../../')
import NanoAODskim_Data	
from NanoAODskim_Data import *
from optparse import OptionParser
parser = OptionParser()


parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
		  default	=	'tHb,tZb',
		  dest		=	'anatype',
		  help		=	'')


parser.add_option('-e', '--era', metavar='F', type='string', action='store',
		  default	=	'2016,2017,2018',
		  dest		=	'era',
		  help		=	'2016,2017, or 2018')

parser.add_option('-S', '--sr', metavar='F', type='string', action='store',
		  default	=	'C',
		  dest		=	'sr',
		  help		=	'')

parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

parser.add_option('-p', '--pt', metavar='F', type='string', action='store',
                  default	=	'ALL',
                  dest		=	'pt',
                  help		=	'')


parser.add_option('--blind', metavar='T', action='store_true',
                  default=False,
                  dest='blind',
                  help='blind')

parser.add_option('-d', '--disc', metavar='F', type='string', action='store',
                  default	=	'0.9',
                  dest		=	'disc',
                  help		=	'')



parser.add_option('-v', '--ver', metavar='F', type='string', action='store',
                  default	=	'',
                  dest		=	'ver',
                  help		=	'')

parser.add_option('-x', '--start', metavar='F', type='string', action='store',
		  default	=	'0',
		  dest		=	'start',
		  help		=	'')
parser.add_option('-y', '--end', metavar='F', type='string', action='store',
		  default	=	'999999',
		  dest		=	'end',
		  help		=	'')


parser.add_option('--bsum', metavar='F', action='store_true',
		  default=False,
		  dest='bsum',
		  help='bsum')

parser.add_option('--dogcvlq', metavar='F', action='store_true',
		  default=False,
		  dest='dogcvlq',
		  help='dogcvlq')

parser.add_option('--dogczh', metavar='F', action='store_true',
		  default=False,
		  dest='dogczh',
		  help='dogczh')

(options, args) = parser.parse_args()
import ROOT
import array
import glob
import sys
from array import *
from ROOT import *

srname=""
if options.sr!="C":
	srname="_"+options.sr+"_"

limrange=[int(options.start),int(options.end)]

sigts=["central","high","low"]
fold="combine/HiggsAnalysis/CombinedLimit/"
systtemp={}
for era in options.era.split(","):
	systtemp['jes'+era]='-'
	systtemp['jer'+era]='-'
	systtemp['jms'+era]='-'
	systtemp['jmr'+era]='-'
	systtemp['btag'+era]='-'
	systtemp['bmistag'+era]='-'
	systtemp['htag'+era]='-'
	systtemp['hmistag'+era]='-'
	systtemp['pu'+era]='-'
	systtemp['wtag'+era]='-'
	systtemp['extrap'+era]='-'
	systtemp['ttag'+era]='-'
	systtemp['trig'+era]='-'
	systtemp['bkg'+era+"tHb"]='-'
	systtemp['bkg'+era+"tZb"]='-'
	systtemp['tt'+era+"tHb"]='-'
	systtemp['tt'+era+"tZb"]='-'
	systtemp['ps'+era]='-'
	systtemp['q2'+era]='-'


sigs=	[ 
	"Wp1500",
	"Wp2000",
	"Wp2500",
	"Wp3000",
	"Wp3500",
	"Wp4000",
	"Wp4500",
	"Wp5000"
	]
ptonum=	{
	"ttbar":"1",
	"qcd":"2",
	"st":"3"
	}
reso=10
bttp=[]
zh=[]
genstr=""

zeroonly = False

if options.dogcvlq:
	genstr="genvlq"
	for it in xrange(reso+1):
		for jt in xrange(reso+1):
			if zeroonly:
				if it>0 and jt>0:
					continue
			if (it+jt<=reso+1):
				bttp.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
else:
	bttp=[[0.5,0.5]]


if options.dogczh:
	genstr="genzc"
	for it in xrange(reso+1):
		for jt in xrange(reso+1):
			if zeroonly:
				if it>0 and jt>0:
					continue
			if (it+jt<=reso+1):
				zh.append([max(0.0001,float(it)/float(reso)),max(0.0001,float(jt)/float(reso))])
else:
	zh=[[0.5,0.5]]
NanoFs={}
NanoFs["2016"]=NanoAODskim_Data("2016")
NanoFs["2017"]=NanoAODskim_Data("2017")
NanoFs["2018"]=NanoAODskim_Data("2018")

alllimc=0
for vlqc in bttp:
	for zhc in zh:	
		alllimc+=1
print "bttp",bttp
print "zhc",zh
print "TOT",alllimc

limcount=-1

filedict={}

for vlqc in bttp:
	for zhc in zh:	
		limcount+=1
		print "limcount,limrange",limcount,limrange
		print "vlq,zh",options.dogcvlq,options.dogczh
		if not (limcount>=limrange[0] and limcount<limrange[1]):
			continue
		replsig="toqVLQWpB"+str(vlqc[0]).replace(".","p")+"T"+str(vlqc[1]).replace(".","p")+"H"+str(zhc[0]).replace(".","p")+"Z"+str(zhc[1]).replace(".","p")
		extexgen=""
		if ( options.dogczh) or (options.dogcvlq):
			extexgen=replsig
		#print "replsig",replsig
		#print "extexgen",extexgen
		for sigt in sigts:
			for sig in sigs:

				coFile = ROOT.TFile(fold+"NanoAODskim_Combine__"+sigt+sig+srname+extexgen+".root","RECREATE")
				header= '''
imax 6
jmax *
kmax *
---------------
shapes * * NanoAODskim_Combine__'''+sigt+sig+srname+extexgen+'''.root $CHANNEL/$PROCESS $CHANNEL/$PROCESS_$SYSTEMATIC
---------------
bin    \t\t\t\ttHb2016	tZb2016	tHb2017	tZb2017	tHb2018	tZb2018
observation\t\t\t-1	-1	-1	-1	-1	-1
---------------
'''
				chdict={}

				for anat in options.anatype.split(","):
					for era in options.era.split(","):
						#print "newerr",anat,era,sig,sigt
						foname=anat+era
						#print "foname",foname
						coFile.mkdir(foname)
						fname="NanoAODskim_"+anat+"_ForLimits__"+era+sigt+genstr+".root"
						if not (fname in filedict):
							filedict[fname]=ROOT.TFile(fname)
						#print "fname",fname
						thFile = filedict[fname]
					
						prdict={}
						#print "sloop"
						for hist in thFile.GetListOfKeys():

							thFile.cd()
							hname= hist.GetName()
							hnamespl=hname.split("__")
							if hnamespl[0].split("_")[2]!=options.sr:
								continue
							if hnamespl[1].split("_")[0]=="WptoqVLQWp":

								brstr=hnamespl[1].split("_")[1]
								#print brstr,replsig
								if "toqVLQWp"+brstr!=replsig:
									continue
								#print "match"
						
						 	hobj = hist.ReadObj()

							#print hname



							#print hnamespl[0].split("_")[2]
							#print hnamespl[0].split("_")[2],options.sr
							#print  hnamespl[0].split("_")[2]

							#print "pass"
							cname=""
							#print  "AAA"
							#print  hnamespl,hnamespl[1],hnamespl[1].split("_")[0]


							rname=hnamespl[1].replace("_","").replace(replsig,"").replace("DATA","data_obs")
							#print "RNAME"
							#print hnamespl
							#print rname
							#print rname,sig
							if (rname in sigs) and (rname!=sig):
								continue
							if not (rname in prdict):
								prdict[rname] =	copy.deepcopy(systtemp)

							#print "hnamespl",hnamespl
							for ihn,hn in enumerate(hnamespl):
								#print ihn,hn
								if ihn==0:
									continue
								if ihn >1 and ihn!=3:
									cname+="_"
								if ihn==1:
									cname+=rname
								if ihn==2:
									cname+=hn
									#print "hnamespl",hnamespl[2],prdict[rname]
									if (hnamespl[2] in prdict[rname]):
										#print hnamespl[1],hnamespl[2],foname
										prdict[rname][hnamespl[2]] = '1'					
								if ihn==3:
									cname+=hn.replace("plus","Up").replace("minus","Down")
									#print hn,cname

							#print hname
							#print cname
							coFile.cd()
							coFile.cd(foname)
							hobj.SetLineColor(1)
							hobj.SetMarkerColor(1)
							hobj.SetLineStyle(1)
							hobj.SetFillColor(0)
							hobj.SetMaximum()

							cobj=copy.deepcopy(hobj)

							#print cname
							cobj.SetTitle(cname)
							cobj.SetName(cname)
							cobj.Write(cname)


							if cname=="qcd" and options.sr=="C" and (options.blind) :
								cobj1=copy.deepcopy(hobj)
								cobj1.Scale(0.0)
								cobj1.SetTitle("data_obs")
								cobj1.SetName("data_obs")
								cobj1.Write("data_obs")
						#print "prdict",prdict
								
						chdict[foname]=prdict

						coFile.cd("../")
						#print "dloop"
							
				coFile.Write()
				coFile.Close()

				binstr = "bin\t\t\t" 
				pstr = "process\t\t\t" 
				pstr1 = "process\t\t\t" 
				rate = "rate\t\t\t" 
				lumis16="lumi2016\t\tlnN"
				lumis17="lumi2017\t\tlnN"
				lumis18="lumi2018\t\tlnN"
				ttclos16="ttclos2016\t\tlnN"
				ttclos17="ttclos2017\t\tlnN"
				ttclos18="ttclos2018\t\tlnN"
				mcs = "* autoMCStats \t0 \t0 \t1" 
				uncstrs={}
				for unc in sorted(systtemp):

					if len(unc)<8:
						uncstrs[unc]=unc+"\t\t\tshape"
					else:
						uncstrs[unc]=unc+"\t\tshape"
					
				#print "chdict",chdict
				for ckey in  sorted(chdict):
					for pkey in  sorted(chdict[ckey]):

						if pkey=="st" and ckey[0:3]=="tHb":
							print "CKEY!!",pkey,ckey[0:3]
							continue
		    				if pkey=="data_obs":
								continue
						binstr+="\t"+ckey
						pstr+=" \t"+pkey
						#print pkey,sigs
						if pkey in sigs:
							pstr1+=" \t0"
						else:
							pstr1+=" \t"+ptonum[pkey]

						#mcs+=" \t1"
						clum16="-"
					       	clum17="-"
						clum18="-"

						if ckey.find("2016")!=-1:
							clum16="1.023"
						if ckey.find("2017")!=-1:
					       		clum17="1.025"
						if ckey.find("2018")!=-1:
							clum18="1.023"

						if not pkey in ["qcd","ttbar"]:
							lumis16+="\t"+clum16
							lumis17+="\t"+clum17
							lumis18+="\t"+clum18
						else:
							lumis16+=" \t-"
							lumis17+=" \t-"
							lumis18+=" \t-"



						cttclos16="-"
						cttclos17="-"
						cttclos18="-"
						curera=""
						if ckey.find("2016")!=-1:
							curera="2016"
						if ckey.find("2017")!=-1:
							curera="2017"
						if ckey.find("2018")!=-1:
							curera="2018"
						NanoF = NanoFs[curera]
						constdict = NanoF.LoadConstants
						ttbarnormcorr=constdict['ttrenorm']
						ttclos=1.0+ttbarnormcorr[1]/ttbarnormcorr[0]

						if curera=="2016":
							cttclos16=str(ttclos)
						if curera=="2017":
							cttclos17=str(ttclos)
						if curera=="2018":
							cttclos18=str(ttclos)
						#print cttclos16,cttclos17,cttclos18
					
						if pkey == "ttbar":
							ttclos16+="\t"+cttclos16
							ttclos17+="\t"+cttclos17
							ttclos18+="\t"+cttclos18
						else:
							ttclos16+=" \t-"
							ttclos17+=" \t-"
							ttclos18+=" \t-"


						rate+=" \t-1"
						#print ckey,pkey
						for unc in sorted(systtemp):
							#print unc
							if unc in chdict[ckey][pkey]:

								uncstrs[unc]+=" \t"+chdict[ckey][pkey][unc]
								#print chdict[ckey][pkey][unc]
								#print uncstrs[unc]


				#print "-"*20
				#print sigt
				#print "-"*20
				sysf = open(fold+sigt+sig+srname+extexgen+"datsys.txt","w") 			
				#print binstr
				#print pstr
				#print str(pstr1)
				#print rate 
				#print lumis16
				#print lumis17
				#print lumis18
				#print ttclos16
				#print ttclos17
				#print ttclos18
				#for unc in sorted(uncstrs):
				#	print uncstrs[unc]
				#print mcs

				sysf.write(header)
				sysf.write(binstr+"\n")
				sysf.write(pstr+"\n")
				sysf.write(pstr1+"\n")
				sysf.write(rate+"\n")
				sysf.write(lumis16+"\n")
				sysf.write(lumis17+"\n")
				sysf.write(lumis18+"\n")
				sysf.write(ttclos16+"\n")
				sysf.write(ttclos17+"\n")
				sysf.write(ttclos18+"\n")
				for unc in sorted(uncstrs):
					#print unc
					sysf.write(uncstrs[unc]+"\n")
				sysf.write(mcs+"\n")



