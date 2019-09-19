import NanoAODskim_Functions	
from NanoAODskim_Functions import *

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'QCD',
                  dest		=	'set',
                  help		=	'data or ttbar')
parser.add_option('-a', '--anatype', metavar='F', type='string', action='store',
                  default	=	'Pho',
                  dest		=	'anatype',
                  help		=	'Pho or tHb')
parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True

print "Options Summary..."
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""


setname =options.set
NanoF = NanoAODskim_Functions(options.anatype)
labels = NanoF.labels 
candl = NanoF.candl
probl = NanoF.probl


datafile=TFile("rootfiles/NanoAODskim_Match__QCD.root","open")
sigfile=TFile("rootfiles/NanoAODskim_Match__SIG.root","open")

qcd_iMDWWF = datafile.Get("iMDWW__F__Allcumint")
qcd_iWW = datafile.Get("iW__W__Allcumint")

qcd_tau21W = datafile.Get("tau21__W__Allcumint")
qcd_tau41F = datafile.Get("tau41__F__Allcumint")

sig_iMDWWF = sigfile.Get("iMDWW__F__Allcumint")
sig_iWW = sigfile.Get("iW__W__Allcumint")

sig_tau21W = sigfile.Get("tau21__W__Allcumint")
sig_tau41F = sigfile.Get("tau41__F__Allcumint")

qcd_iMDWWF.Scale(1.0/qcd_iMDWWF.GetMaximum())
qcd_iWW.Scale(1.0/qcd_iWW.GetMaximum())

qcd_tau21W.Scale(1.0/qcd_tau21W.GetMaximum())
qcd_tau41F.Scale(1.0/qcd_tau41F.GetMaximum())

sig_iMDWWF.Scale(1.0/sig_iMDWWF.GetMaximum())
sig_iWW.Scale(1.0/sig_iWW.GetMaximum())

sig_tau21W.Scale(1.0/sig_tau21W.GetMaximum())
sig_tau41F.Scale(1.0/sig_tau41F.GetMaximum())



ROCW = [array('d'),array('d')]
ROCWW = [array('d'),array('d')]
ROCtau21 = [array('d'),array('d')]
ROCtau41 = [array('d'),array('d')]


for xbin in xrange(0,qcd_iWW.GetNbinsX()-1):
	ROCW[0].append(sig_iWW[xbin])
	ROCW[1].append(qcd_iWW[xbin])
	ROCWW[0].append(sig_iMDWWF[xbin])
	ROCWW[1].append(qcd_iMDWWF[xbin])
	ROCtau41[0].append(sig_tau41F[xbin])
	ROCtau41[1].append(qcd_tau41F[xbin])
	ROCtau21[0].append(sig_tau21W[xbin])
	ROCtau21[1].append(qcd_tau21W[xbin])

#for roc in ROCW:
#	for r in roc :
#		print r
grW = TGraph( len(ROCW[0])+1, ROCW[0], ROCW[1] )
grW.SetLineColor(2)
grW.SetMarkerColor(2)
grW.SetMarkerStyle(20)
grWW = TGraph( len(ROCWW[0])+1, ROCWW[0], ROCWW[1] )
grWW.SetLineColor(2)
grWW.SetMarkerColor(2)
grWW.SetMarkerStyle(20)
grtau41 = TGraph( len(ROCtau41[0])+1, ROCtau41[0], ROCtau41[1] )
grtau21 = TGraph( len(ROCtau21[0])+1, ROCtau21[0], ROCtau21[1] )
grtau41.SetMarkerStyle(20)
grtau21.SetMarkerStyle(20)

c2 = TCanvas('c2', '', 700, 600)
mg = TMultiGraph();
mg.Add(grW)
mg.Add(grtau21)
mg.Draw("Ap");
c2.SetLogy()
c2.RedrawAxis()
c2.Update()
c2.Print('plots/MatchW_semilog__'+options.anatype+'.root', 'root')
c2.Print('plots/MatchW_semilog__'+options.anatype+'.pdf', 'pdf')
c2.Print('plots/MatchW_semilog__'+options.anatype+'.png', 'png')

c3 = TCanvas('c3', '', 700, 600)
mg = TMultiGraph();
mg.Add(grWW)
mg.Add(grtau41)
mg.Draw("Ap");
c3.SetLogy()
c3.RedrawAxis()
c3.Update()
c3.Print('plots/MatchWW_semilog__'+options.anatype+'.root', 'root')
c3.Print('plots/MatchWW_semilog__'+options.anatype+'.pdf', 'pdf')
c3.Print('plots/MatchWW_semilog__'+options.anatype+'.png', 'png')




print "Completed..."																										

