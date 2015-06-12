import ROOT
import sys
from treeFunctions import *
from SignalScan import isSignal
ROOT.gSystem.Load("libTreeObjects.so")
ROOT.TH1.SetDefaultSumw2()




# reading scale Histos
# this was a test wether a scalfactor depending on jets.size() would improve the method, it failed
"""
TFileJetScale = ROOT.TFile("TFileJetScale.root")
GTJetMultiRatioSim = TFileJetScale.Get("SimGTMulti")
GLJetMultiRatioSim = TFileJetScale.Get("SimGLMulti")
"""




"""
this program aims to find weights for GammaLoose (GL) to predict their
fakerate (faking GammaTight GT)
The Controll region to find these weights are all events with Met<100 (no possible signal)

To be able to varify the method it is used on simulated data.
(QCD and GJet samples)
"""


Styles.tdrStyle() # set Style for 1D histos
Canvas1D = ROOT.TCanvas ("canvas1D", "canvas1D")


Styles.tdrStyle() # set Style for 1D histos
ROOT.gStyle.SetOptLogy(0)
Canvas1DNLog = ROOT.TCanvas ("canvas1DNLog", "canvas1D")

Styles.tdrStyle2D() # set style for 2D histos
#ROOT.gStyle.SetPalette(1)
Canvas1 = ROOT.TCanvas ("canvas1", "canvas1")

plotvar="Met" # set plotvar Backround only uses it to set axis Titles
BreakFill = 0 # if set to 1 the loop will break after 10000 Entries
PrintMaps = 0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "#gamma_{tight}/#gamma_{loose}"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar

path ="/user/eicker/08/"
IDVersion =".08_tree.root" #Version of the trees
homePath="~/plotting/MultiJetBackground/"


TFileBackground = ROOT.TFile(homePath+"TFileBackgroundPtJetMulti.root", "recreate")

if len(sys.argv)>1:
	if len(sys.argv)==2:
		print "found "+str(len(sys.argv)-1)+" arguments"
		if sys.argv[1]=="0" or sys.argv[1]=="1":
			BreakFill=int(sys.argv[1])
			print "set Breakfill = "+sys.argv[1]
		else:
			sys.exit("Wrong argument given! BreakFill can be set to 0 or 1") 
	else:
		sys.exit("too many arguments given! Expected 1 or none")




print "plotting against "+plotvar
print "Programm is:"
if BreakFill:
	print "breaking loops after 10000 entries"
else:
	print "looping over all entries"
if PrintMaps:
	print "printing maps with names, files, entries ..."
else:
	print "not printing maps"

Title[1]="E_{T}^{miss}(GeV)"


# maps used to mesure weight and define TFiles
# the order in which plots are stacked and generated is set in Names
# weight for data has to bet set to 1 later!
Names=["TTJets_V03", "TTGamma_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
N = {}
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':0.2571, 'WGamma_50_130_V03':1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':0.074, 'ZGamma_V02':123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204., 'PhotonA_V04':1.,  'SinglePhotonB_V04':1., 'SinglePhotonC_V04':1., 'PhotonParkedD_V10':1.}
Lsim = {}
FileList = {}


for name in Names:
	print "filling maps for "+path+name+IDVersion
	FileList[name]=ROOT.TFile(path+name+IDVersion) # fill map with TFiles
	GenHist = FileList[name].Get("nGen") # get Hist with entry information
	N[name] = GenHist.GetEntries() # get entries and fill them in the map
	Lsim[name]=N[name]/sigma[name] # fill map with luminosity (data Lsim is set to Lint)

if PrintMaps:
	print "########### Names ############"
	print Names
	print "########### N ################"
	print N
	print "########### sigma ############"
	print sigma
	print "########### Lsim #############"
	print Lsim
	print "########### Filelist #########"
	print FileList


L = ROOT.TLegend(.6,.75,.9,.9)

nBinsJet = 13 # set number of Bins in Ht for 2D Plots
nBinsPt = 15 # set number of Bins in Pt for 2D Plots
PtMin = 175
PtMax = 1900
JetMin = 0
JetMax = 13

"""
									Histograms for Data
"""
#Hist for GT objects binned in Ht and PhotonPt* in controll region
HistDataHtPtGT = ROOT.TH2F( "DataHtPtGT", "DataHtPtGT", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistDataHtPtGT.SetTitle(Title[0]+" #gamma_{tight}, E_{T}^{miss}<100")
HistDataHtPtGT.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGT.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt* in controll region
HistDataHtPtGL = ROOT.TH2F( "DataHtPtGL", "DataHtPtGL", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistDataHtPtGL.SetTitle(Title[0]+" #gamma_{loose}, E_{T}^{miss}<100")
HistDataHtPtGL.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGL.GetYaxis().SetTitle("Ht")

#Hist for GT objects binned in Ht and PhotonPt* in signal region
HistDataHtPtGTSignal = ROOT.TH2F( "DataHtPtGTSignal", "DataHtPtGTSignal", nBinsPt, PtMin, PtMax, nBinsJet, JetMin, JetMax)
HistDataHtPtGTSignal.SetTitle(Title[0]+" #gamma_{tight}, E_{T}^{miss}>100")
HistDataHtPtGTSignal.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGTSignal.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt* in signal region
HistDataHtPtGLSignal = ROOT.TH2F( "DataHtPtGLSignal", "DataHtPtGLSignal", nBinsPt, PtMin, PtMax, nBinsJet, JetMin, JetMax)
HistDataHtPtGLSignal.SetTitle(Title[0]+" #gamma_{loose}, E_{T}^{miss}>100")
HistDataHtPtGLSignal.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGLSignal.GetYaxis().SetTitle("Ht")

#Hist for weight binned like HistDataHtPtGT and HistDataHtPtGL. Weight is GT/GL in every bin
HistDataHtPtWeight = ROOT.TH2F( "DataHtPtWeight", "DataHtPtWeight", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistDataHtPtWeight.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtWeight.GetYaxis().SetTitle("Ht")
HistDataHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose}")

#Error on weight
HistDataHtPtWeightError = ROOT.TH2F( "DataHtPtWeightError", "DataHtPtWeightError", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistDataHtPtWeightError.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtWeightError.GetYaxis().SetTitle("Ht")
HistDataHtPtWeightError.SetTitle(Title[0]+" #sigma_{w_{i}}/w_{i}")

#Events with weight==0 (bevor set to mean)
HistDataHtPtWeightZeroEvents = ROOT.TH2F( "DataHtPtWeightZeroEvents", "DataHtPtWeightZeroEvents", nBinsPt, PtMin, PtMax, nBinsJet, JetMin, JetMax)
HistDataHtPtWeightZeroEvents.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtWeightZeroEvents.GetYaxis().SetTitle("Ht")
HistDataHtPtWeightZeroEvents.SetTitle(Title[0]+" Events with w_{i}=0")

#to see the isolation criteria of gt and gl  
HistIsoGT = ROOT.TH2F( "DataIsoGT", "DataIsoGT", 100, 0, 30, 100, 0, 40)
HistIsoGT.SetTitle(Title[0]+" #gamma_{tight}")
HistIsoGT.GetXaxis().SetTitle("I_{#pm}")
HistIsoGT.GetYaxis().SetTitle("I_{0}")

HistIsoGL = ROOT.TH2F( "DataIsoGL", "DataIsoGL", 100, 0, 30, 100, 0, 40)
HistIsoGL.SetTitle(Title[0]+" #gamma_{loose}")
HistIsoGL.GetXaxis().SetTitle("I_{#pm}")
HistIsoGL.GetYaxis().SetTitle("I_{0}")

# Background prediction for data estimated with weights plottet with met
HistDataBackgroundPredictionMet = ROOT.TH1F( "DataBackgroundPredictionMet", "DataBackgroundPredictionMet", 18, 0, 900 )
HistDataBackgroundPredictionMet.SetTitle(Title[0])
HistDataBackgroundPredictionMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistDataBackgroundPredictionMet.GetYaxis().SetTitle("Events")

HistDataBackgroundPredictionMetSys = HistDataBackgroundPredictionMet.Clone("HistDataBackgroundPredictionMetSys")

# Background prediction for data estimated with weights plottet with Ht
HistDataBackgroundPredictionHt = ROOT.TH1F( "DataBackgroundPredictionHt", "DataBackgroundPredictionHt", 25, 0, 1800 )
HistDataBackgroundPredictionHt.SetTitle(Title[0])
HistDataBackgroundPredictionHt.GetXaxis().SetTitle("Ht(GeV)")
HistDataBackgroundPredictionHt.GetYaxis().SetTitle("Events")

HistDataBackgroundPredictionHtSys = HistDataBackgroundPredictionHt.Clone("HistDataBackgroundPredictionHtSys")

# Background prediction for data estimated with weights plottet with Pt*
HistDataBackgroundPredictionPtStar = ROOT.TH1F( "DataBackgroundPredictionPtStar", "DataBackgroundPredictionPtStar", 30, 145, 1900 )
HistDataBackgroundPredictionPtStar.SetTitle(Title[0])
HistDataBackgroundPredictionPtStar.GetXaxis().SetTitle("P_{T}*(GeV)")
HistDataBackgroundPredictionPtStar.GetYaxis().SetTitle("Events")

HistDataBackgroundPredictionPtStarSys = HistDataBackgroundPredictionPtStar.Clone("HistDataBackgroundPredictionPtStarSys")

# Background prediction for data estimated with weights plottet with met in control region
HistDataBackgroundCPredictionMet = ROOT.TH1F( "DataBackgroundCPredictionMet", "DataBackgroundCPredictionMet", 18, 0, 900 )
HistDataBackgroundCPredictionMet.SetTitle(Title[0]+", E_{T}^{miss}<100")
HistDataBackgroundCPredictionMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistDataBackgroundCPredictionMet.GetYaxis().SetTitle("Events")

HistDataBackgroundCPredictionMetSys = HistDataBackgroundCPredictionMet.Clone("HistDataBackgroundCPredictionMetSys")

# Background prediction for data estimated with weights plottet with Ht in control region
HistDataBackgroundCPredictionHt = ROOT.TH1F( "DataBackgroundCPredictionHt", "DataBackgroundCPredictionHt", 25, 0, 1800 )
HistDataBackgroundCPredictionHt.SetTitle(Title[0]+", E_{T}^{miss}<100")
HistDataBackgroundCPredictionHt.GetXaxis().SetTitle("Ht(GeV)")
HistDataBackgroundCPredictionHt.GetYaxis().SetTitle("Events")

HistDataBackgroundCPredictionHtSys = HistDataBackgroundCPredictionHt.Clone("HistDataBackgroundCPredictionHtSys")

# Background prediction for data estimated with weights plottet with Pt* in control region
HistDataBackgroundCPredictionPtStar = ROOT.TH1F( "DataBackgroundCPredictionPtStar", "DataBackgroundCPredictionPtStar", 30, 145, 1900 )
HistDataBackgroundCPredictionPtStar.SetTitle(Title[0]+", E_{T}^{miss}<100")
HistDataBackgroundCPredictionPtStar.GetXaxis().SetTitle("P_{T}*(GeV)")
HistDataBackgroundCPredictionPtStar.GetYaxis().SetTitle("Events")

HistDataBackgroundCPredictionPtStarSys = HistDataBackgroundCPredictionPtStar.Clone("HistDataBackgroundCPredictionPtStarSys")

# GT Jet multi for data in controll region 
HistDataGTMulti = ROOT.TH1F("DataGTMulti", "DataGTMulti", 12, -0.5, 11.5)
HistDataGTMulti.SetTitle(Title[0]+"E_{T}^{miss}(GeV)<100GeV")
HistDataGTMulti.GetXaxis().SetTitle("Jets in #gamma_{tight} event")
HistDataGTMulti.GetYaxis().SetTitle("Events")

# GL Jet multi for data in controll region
HistDataGLMulti = ROOT.TH1F("DataGLMulti", "DataGLMulti", 12, -0.5, 11.5)
HistDataGLMulti.SetTitle(Title[0]+"E_{T}^{miss}(GeV)<100GeV")
HistDataGLMulti.GetXaxis().SetTitle("Jets in #gamma_{loose} event")
HistDataGLMulti.GetYaxis().SetTitle("Events")

# GT Jet multi for data in signal region 
HistDataGTMultiSignal = ROOT.TH1F("DataGTMultiSignal", "DataGTMultiSignal", 12, -0.5, 11.5)
HistDataGTMultiSignal.SetTitle(Title[0]+"E_{T}^{miss}(GeV)>100GeV")
HistDataGTMultiSignal.GetXaxis().SetTitle("Jets in #gamma_{tight} event")
HistDataGTMultiSignal.GetYaxis().SetTitle("Events")

# GL Jet multi for data in signal region
HistDataGLMultiSignal = ROOT.TH1F("DataGLMultiSignal", "DataGLMultiSignal", 12, -0.5, 11.5)
HistDataGLMultiSignal.SetTitle(Title[0]+"E_{T}^{miss}(GeV)>100GeV")
HistDataGLMultiSignal.GetXaxis().SetTitle("Jets in #gamma_{loose} event")
HistDataGLMultiSignal.GetYaxis().SetTitle("Events")

HistDataGTGL = ROOT.TH1F( "DataGTGL", "DataGTGL", 10, 0, 100 )

GTData = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
GLData = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]

"""
								Histograms for simulation
"""


#hist for GT binned in pt ht with weights in controll region
HistSimHtPtGT = ROOT.TH2F( "SimHtPtGT", "SimHtPtGT", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistSimHtPtGT.SetTitle(Title[0]+" #gamma_{tight} simulated data, E_{T}^{miss}<100")
HistSimHtPtGT.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGT.GetYaxis().SetTitle("Ht")

#hist for GL binned in pt ht with weights in controll region
HistSimHtPtGL = ROOT.TH2F( "SimHtPtGL", "SimHtPtGL", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistSimHtPtGL.SetTitle(Title[0]+" #gamma_{loose} simulated data, E_{T}^{miss}<100")
HistSimHtPtGL.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGL.GetYaxis().SetTitle("Ht")

#Hist for GT objects binned in Ht and PhotonPt* in signal region
HistSimHtPtGTSignal = ROOT.TH2F( "SimHtPtGTSignal", "SimHtPtGTSignal", nBinsPt, PtMin, PtMax, nBinsJet, JetMin, JetMax)
HistSimHtPtGTSignal.SetTitle(Title[0]+" #gamma_{tight}, E_{T}^{miss}>100")
HistSimHtPtGTSignal.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGTSignal.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt* in signal region
HistSimHtPtGLSignal = ROOT.TH2F( "SimHtPtGLSignal", "SimHtPtGLSignal", nBinsPt, PtMin, PtMax, nBinsJet, JetMin, JetMax)
HistSimHtPtGLSignal.SetTitle(Title[0]+" #gamma_{loose}, E_{T}^{miss}>100")
HistSimHtPtGLSignal.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGLSignal.GetYaxis().SetTitle("Ht")

#hist for weight (gt/gl)
HistSimHtPtWeight = ROOT.TH2F( "SimHtPtWeight", "SimHtPtWeight", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistSimHtPtWeight.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeight.GetYaxis().SetTitle("Ht")
HistSimHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose} simulated data")

#weight error 
HistSimHtPtWeightError = ROOT.TH2F( "SimHtPtWeightError", "SimHtPtWeightError", nBinsPt, PtMin, PtMax, nBinsJet , JetMin, JetMax)
HistSimHtPtWeightError.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeightError.GetYaxis().SetTitle("Ht")
HistSimHtPtWeightError.SetTitle(Title[0]+" #sigma_{w_{i}}/w_{i}")

#Events with weight==0 (bevor set to mean)
HistSimHtPtWeightZeroEvents = ROOT.TH2F( "SimHtPtWeightZeroEvents", "SimHtPtWeightZeroEvents", nBinsPt, PtMin, PtMax, nBinsJet, JetMin, JetMax)
HistSimHtPtWeightZeroEvents.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeightZeroEvents.GetYaxis().SetTitle("Ht")
HistSimHtPtWeightZeroEvents.SetTitle(Title[0]+" Events with w_{i}=0")

HistSimIsoGT = ROOT.TH2F( "SimIsoGT", "SimIsoGT", 100, 0, 30, 100, 0, 40)
HistSimIsoGT.SetTitle(Title[0]+" #gamma_{tight} simulated data")
HistSimIsoGT.GetXaxis().SetTitle("I_{0}")
HistSimIsoGT.GetYaxis().SetTitle("I_{#pm}")

HistSimIsoGL = ROOT.TH2F( "SimIsoGL", "SimIsoGL", 100, 0, 30, 100, 0, 40)
HistSimIsoGL.SetTitle(Title[0]+" #gamma_{loose} simulated data")
HistSimIsoGL.GetXaxis().SetTitle("I_{0}")
HistSimIsoGL.GetYaxis().SetTitle("I_{#pm}")

# prediction and Background against Met
HistSimBackgroundPredictionMet = ROOT.TH1F( "SimBackgroundPredictionMet", "SimBackgroundPredictionMet", 18, 0, 900)
HistSimBackgroundPredictionMet.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPredictionMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundPredictionMet.GetYaxis().SetTitle("Events")

HistSimBackgroundPredictionMetSys = HistSimBackgroundPredictionMet.Clone("HistSimBackgroundPredictionMetSys")

HistSimBackgroundMet = ROOT.TH1F( "SimBackgroundMet", "SimBackgroundMet", 18, 0, 900)
HistSimBackgroundMet.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundMet.GetYaxis().SetTitle("Events")

# Background no weights
HistSimBackgroundMetNW = ROOT.TH1F( "SimBackgroundMetNW", "SimBackgroundMetNW", 18, 0, 900)
HistSimBackgroundMetNW.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundMetNW.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundMetNW.GetYaxis().SetTitle("Events")

# prediction and Background against Ht
HistSimBackgroundPredictionHt = ROOT.TH1F( "SimBackgroundPredictionHt", "SimBackgroundPredictionHt", 25, 0, 1800)
HistSimBackgroundPredictionHt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPredictionHt.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundPredictionHt.GetYaxis().SetTitle("Events")

HistSimBackgroundPredictionHtSys = HistSimBackgroundPredictionHt.Clone("HistSimBackgroundPredictionHtSys")

HistSimBackgroundHt = ROOT.TH1F( "SimBackgroundHt", "SimBackgroundHt", 25, 0, 1800)
HistSimBackgroundHt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundHt.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundHt.GetYaxis().SetTitle("Events")

# Background no weight
HistSimBackgroundHtNW = ROOT.TH1F( "SimBackgroundHtNW", "SimBackgroundHtNW", 25, 0, 1800)
HistSimBackgroundHtNW.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundHtNW.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundHtNW.GetYaxis().SetTitle("Events")

# prediction and Background against PhotonPt
HistSimBackgroundPredictionPhotonPt = ROOT.TH1F( "SimBackgroundPredictionPhotonPt", "SimBackgroundPredictionPhotonPt", 30, 145, 1900)
HistSimBackgroundPredictionPhotonPt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPredictionPhotonPt.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundPredictionPhotonPt.GetYaxis().SetTitle("Events")

HistSimBackgroundPredictionPhotonPtSys = HistSimBackgroundPredictionPhotonPt.Clone("HistSimBackgroundPredictionPhotonPtSys")

HistSimBackgroundPhotonPt = ROOT.TH1F( "SimBackgroundPhotonPt", "SimBackgroundPhotonPt", 30, 145, 1900)
HistSimBackgroundPhotonPt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPhotonPt.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundPhotonPt.GetYaxis().SetTitle("Events")

# Background no weight
HistSimBackgroundPhotonPtNW = ROOT.TH1F( "SimBackgroundPhotonPtNW", "SimBackgroundPhotonPtNW", 30, 145, 1900)
HistSimBackgroundPhotonPtNW.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPhotonPtNW.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundPhotonPtNW.GetYaxis().SetTitle("Events")

# prediction and Background against Met in control region
HistSimBackgroundCPredictionMet = ROOT.TH1F( "SimBackgroundCPredictionMet", "SimBackgroundCPredictionMet", 18, 0, 900)
HistSimBackgroundCPredictionMet.SetTitle(Title[0]+" Comparison for QCD and GJet samples, E_{T}^{miss}<100")
HistSimBackgroundCPredictionMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundCPredictionMet.GetYaxis().SetTitle("Events")

HistSimBackgroundCPredictionMetSys = HistSimBackgroundCPredictionMet.Clone("HistSimBackgroundCPredictionMetSys")

HistSimBackgroundCMet = ROOT.TH1F( "SimBackgroundCMet", "SimBackgroundCMet", 18, 0, 900)
HistSimBackgroundCMet.SetTitle(Title[0]+" Comparison for QCD and GJet samples, E_{T}^{miss}<100")
HistSimBackgroundCMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundCMet.GetYaxis().SetTitle("Events")

HistSimBackgroundCPredictionMetNW = ROOT.TH1F( "SimBackgroundCPredictionMetNW", "SimBackgroundCPredictionMetNW", 18, 0, 900)

# prediction and Background against Ht in control region
HistSimBackgroundCPredictionHt = ROOT.TH1F( "SimBackgroundCPredictionHt", "SimBackgroundCPredictionHt", 25, 0, 1800)
HistSimBackgroundCPredictionHt.SetTitle(Title[0]+" Comparison for QCD and GJet samples, E_{T}^{miss}<100")
HistSimBackgroundCPredictionHt.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundCPredictionHt.GetYaxis().SetTitle("Events")

HistSimBackgroundCPredictionHtSys = HistSimBackgroundCPredictionHt.Clone("HistSimBackgroundCPredictionHtSys")

HistSimBackgroundCHt = ROOT.TH1F( "SimBackgroundCHt", "SimBackgroundCHt", 25, 0, 1800)
HistSimBackgroundCHt.SetTitle(Title[0]+" Comparison for QCD and GJet samples, E_{T}^{miss}<100")
HistSimBackgroundCHt.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundCHt.GetYaxis().SetTitle("Events")

# prediction and Background against PhotonPt in control region
HistSimBackgroundCPredictionPhotonPt = ROOT.TH1F( "SimBackgroundCPredictionPhotonPt", "SimBackgroundCPredictionPhotonPt", 30, 145, 1900)
HistSimBackgroundCPredictionPhotonPt.SetTitle(Title[0]+" Comparison for QCD and GJet samples, E_{T}^{miss}<100")
HistSimBackgroundCPredictionPhotonPt.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundCPredictionPhotonPt.GetYaxis().SetTitle("Events")

HistSimBackgroundCPredictionPhotonPtSys = HistSimBackgroundCPredictionPhotonPt.Clone("HistSimBackgroundCPredictionPhotonPtSys")

HistSimBackgroundCPhotonPt = ROOT.TH1F( "SimBackgroundCPhotonPt", "SimBackgroundCPhotonPt", 30, 145, 1900)
HistSimBackgroundCPhotonPt.SetTitle(Title[0]+" Comparison for QCD and GJet samples, E_{T}^{miss}<100")
HistSimBackgroundCPhotonPt.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundCPhotonPt.GetYaxis().SetTitle("Events")

# GT Jet multi for simulated data in controll region 
HistSimGTMulti = ROOT.TH1F("SimGTMulti", "SimGTMulti", 12, -0.5, 11.5)
HistSimGTMulti.SetTitle(Title[0]+" simulated, E_{T}^{miss}(GeV)<100")
HistSimGTMulti.GetXaxis().SetTitle("Jets in #gamma_{tight} event")
HistSimGTMulti.GetYaxis().SetTitle("Events")

# GL Jet multi for simulated data in controll region 
HistSimGLMulti = ROOT.TH1F("SimGLMulti", "SimGLMulti", 12, -0.5, 11.5)
HistSimGLMulti.SetTitle(Title[0]+" simulated, E_{T}^{miss}(GeV)<100")
HistSimGLMulti.GetXaxis().SetTitle("Jets in #gamma_{loose} event")
HistSimGLMulti.GetYaxis().SetTitle("Events")

# GT Jet multi for simulated data in signal region 
HistSimGTMultiSignal = ROOT.TH1F("SimGTMultiSignal", "SimGTMultiSignal", 12, -0.5, 11.5)
HistSimGTMultiSignal.SetTitle(Title[0]+" simulated, E_{T}^{miss}(GeV)>100")
HistSimGTMultiSignal.GetXaxis().SetTitle("Jets in #gamma_{tight} event")
HistSimGTMultiSignal.GetYaxis().SetTitle("Events")

# GL Jet multi for simulated data in signal region 
HistSimGLMultiSignal = ROOT.TH1F("SimGLMultiSignal", "SimGLMultiSignal", 12, -0.5, 11.5)
HistSimGLMultiSignal.SetTitle(Title[0]+" simulated, E_{T}^{miss}(GeV)>100")
HistSimGLMultiSignal.GetXaxis().SetTitle("Jets in #gamma_{loose} event")
HistSimGLMultiSignal.GetYaxis().SetTitle("Events")

HistSimGTGL = ROOT.TH1F( "SimGTGL", "SimGTGL", 10, 0, 100 )

GTSim = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
GLSim = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]


GT = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
GL = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]

print "************** looping over controll region **********************"

for name in Names:
	#if name!="QCD_500_1000_V03" and name!="PhotonA_V04":
	#	continue
	print "******************************************************************"
	print "looping over: "+path+name+IDVersion
	stop=0
	status = "default"
	if name == "ZGammaNuNu_V03":
		print "skipping ZGammaNuNu"
		print "******************************************************************"
		continue
	if name =="PhotonA_V04" or name =="SinglePhotonB_V04" or name =="SinglePhotonC_V04" or name =="PhotonParkedD_V10":
		print "idetified real data"
		status = "data"
		print "status set to "+status
	else:
		if name != "QCD_250_500_V03" and name!="QCD_100_250_V09" and name!="QCD_500_1000_V03" and name!="QCD_1000_inf_V03" and name!="GJets_100_200_V09" and name!="GJets_200_400_V03" and name!="GJets_400_inf_V03" and name!="GJets_40_100_V09":
			print "not QCD or GJets"
			print "skipping..."
			print "******************************************************************"
			continue
		print "identified simulated data"
		status = "sim"
		print "status set to "+status
	tree = FileList[name].Get("myTree")#Inputtree
	if status=="data":
		weight=1
	elif status=="sim":
		weight = Lint/Lsim[name]
	else:
		print "no valid status found... exiting"
		break
	print "weight is "+str(weight)
	GT = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
	GL = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
	for event in tree:
		if status=="data" and event.weight!=1:
			print "data found with event.weight!=1 check treeWriter (wrong weights for data!)"
		if BreakFill:
			stop+=1
			if stop==10000:
				print "breaking loop..."
				break
		if event.met > 100:
			continue # filter for control region
		GtCount=0 # reset number of GT and GL in the event
		GlCount=0
		if event.photons.size()>0:
			GtCount=1

		if event.jetphotons.size()>0:
			GlCount=1
		
		if event.met < 10:#						for HistSimGTGL and HistDataGTGL
			GT[0] += weight*event.weight*GtCount
			GL[0] += weight*event.weight*GlCount
		elif event.met < 20:
			GT[1] += weight*event.weight*GtCount
			GL[1] += weight*event.weight*GlCount
		elif event.met < 30:
			GT[2] += weight*event.weight*GtCount
			GL[2] += weight*event.weight*GlCount
		elif event.met < 40:
			GT[3] += weight*event.weight*GtCount
			GL[3] += weight*event.weight*GlCount
		elif event.met < 50:
			GT[4] += weight*event.weight*GtCount
			GL[4] += weight*event.weight*GlCount
		elif event.met < 60:
			GT[5] += weight*event.weight*GtCount
			GL[5] += weight*event.weight*GlCount
		elif event.met < 70:
			GT[6] += weight*event.weight*GtCount
			GL[6] += weight*event.weight*GlCount
		elif event.met < 80:
			GT[7] += weight*event.weight*GtCount
			GL[7] += weight*event.weight*GlCount
		elif event.met < 90:
			GT[8] += weight*event.weight*GtCount
			GL[8] += weight*event.weight*GlCount
		elif event.met <= 100:
			GT[9] += weight*event.weight*GtCount
			GL[9] += weight*event.weight*GlCount
		else:
			print "something went wrong here! Too much met for controll region"
			break
		"""
		UseJetphoton=0
		UsePhoton=0
		if event.photons.size()>0 and event.jetphotons.size()>0: # if an event has gt and gl use the one with highest pt* and ignore the rest
			if event.photons[0].ptMJet==0 and event.jetphotons[0].ptMJet==0:
				if (event.photons[0].pt-event.jetphotons[0].pt)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1
			elif event.photons[0].ptMJet==0:
				if (event.photons[0].pt-event.jetphotons[0].ptMJet)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1
			elif event.jetphotons[0].ptMJet==0:
				if (event.photons[0].ptMJet-event.jetphotons[0].pt)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1
			else:
				if (event.photons[0].ptMJet-event.jetphotons[0].ptMJet)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1	
			
			print "event with : gt pt = "+str(event.photons[0].pt)+" gt ptMJet = "+str(event.photons[0].ptMJet)	
			print "event with : gl pt = "+str(event.jetphotons[0].pt)+" gl ptMJet = "+str(event.jetphotons[0].ptMJet)	
			print "stati: UsePhoton = "+str(UsePhoton)+" and UseJetphoton = "+str(UseJetphoton)	
			print
				
		else:# if only gt OR gl exist both possibilities are checked
			UsePhoton=1
			UseJetphoton=1
		"""
		if isSignal(event)=="GT":
			if status=="sim":
				HistSimGTMulti.Fill(event.cleanjets.size(), weight*event.weight)	
				HistSimIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso, weight*event.weight )
			elif status=="data":
				HistDataGTMulti.Fill(event.cleanjets.size())
				HistIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso)
			if event.photons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGT.Fill(event.photons[0].pt, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGT.Fill(event.photons[0].pt, event.cleanjets.size())
			else:
				if status=="sim":
					HistSimHtPtGT.Fill(event.photons[0].ptMJet, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGT.Fill(event.photons[0].ptMJet, event.cleanjets.size())
			
		if isSignal(event)=="GL":
			if status=="sim":
				HistSimGLMulti.Fill(event.cleanjets.size(), weight*event.weight)	
				HistSimIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso, weight*event.weight )
			if status=="data":
				HistDataGLMulti.Fill(event.cleanjets.size())
				HistIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso)
			if event.jetphotons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGL.Fill(event.jetphotons[0].pt, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGL.Fill(event.jetphotons[0].pt, event.cleanjets.size())
			else:
				if status=="sim":
					HistSimHtPtGL.Fill(event.jetphotons[0].ptMJet, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGL.Fill(event.jetphotons[0].ptMJet, event.cleanjets.size())


	if status=="data":
		i=0
		for i,g in enumerate(GTData):
			GTData[i] += GT[i]
			GLData[i] += GL[i]
	if status=="sim":
		i=0
		for i,g in enumerate(GTSim):
			GTSim[i] += GT[i]
			GLSim[i] += GL[i]
		
	print "******************************************************************"

print "*********** finished looping over controll region ****************"
print "******************************************************************"


TFileBackground.cd()#				print and save to TFile here
Canvas1.cd()#						GT histos will be overwritten by TH1.Divide

HistDataHtPtGL.Draw("colz")
HistDataHtPtGL.Write()
ROOT.gPad.SaveAs(homePath+"Data/GLHtPtData.pdf")
countDataGLControlRegion = HistDataHtPtGL.GetEntries()
if HistDataHtPtGL.Integral()!=HistDataHtPtGL.GetEntries():
	print "something went wrong here, weights for data should be 1!"

HistDataHtPtGT.Draw("colz")
HistDataHtPtGT.Write()
ROOT.gPad.SaveAs(homePath+"Data/GTHtPtData.pdf")
countDataGTControlRegion = HistDataHtPtGT.GetEntries()

HistSimHtPtGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLHtPtSim.pdf")
HistSimHtPtGL.Write()
countSimGLControlRegion = HistSimHtPtGL.Integral()

HistSimHtPtGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTHtPtSim.pdf")
HistSimHtPtGT.Write()
countSimGTControlRegion = HistSimHtPtGT.Integral()
#print str(HistSimHtPtGT.Integral())+" != "+str(HistSimHtPtGT.GetEntries())

print "GT(controll)/GL(controll) use it for meanweight!"
print "Sim: Gt(control) = "+str(countSimGTControlRegion)+"    Gl(control) = "+str(countSimGLControlRegion)
print "Data: Gt(control) = "+str(countDataGTControlRegion)+"    Gl(control) = "+str(countDataGLControlRegion)
print "Sim: "+str(countSimGTControlRegion/countSimGLControlRegion)
print "Data: "+str(float(countDataGTControlRegion)/float(countDataGLControlRegion))

meanWeightSim = countSimGTControlRegion/countSimGLControlRegion
meanWeightData = float(countDataGTControlRegion)/float(countDataGLControlRegion)

BinsCount=0	
print "****************** setting 2D-Bincontents ************************"

HistDataHtPtGT.Divide(HistDataHtPtGL)
HistSimHtPtGT.Divide(HistSimHtPtGL)
countWeightsSim=0.
countWeightsData=0.
for pt in range(1, nBinsPt+1):# Bin numbers start at 1 first bin (1,1)
	for jet in range(1, nBinsJet+1):
		BinsCount+=1
		if HistSimHtPtGT.GetBinContent(pt, jet)!=0:
			countWeightsSim+=1.
			HistSimHtPtWeightError.SetBinContent(pt, jet, (float(HistSimHtPtGT.GetBinError(pt, jet))/float(HistSimHtPtGT.GetBinContent(pt, jet)))) # relative Error on w(i)
		elif HistSimHtPtGT.GetBinContent(pt, jet)==0:
			HistSimHtPtWeightError.SetBinContent(pt, jet, 0) # relative Error on w(i)

		if HistDataHtPtGT.GetBinContent(pt, jet)!=0:
			countWeightsData+=1.
			HistDataHtPtWeightError.SetBinContent(pt, jet, (float(HistDataHtPtGT.GetBinError(pt, jet))/float(HistDataHtPtGT.GetBinContent(pt, jet))))
		elif HistDataHtPtGT.GetBinContent(pt, jet)==0:
			HistDataHtPtWeightError.SetBinContent(pt, jet, 0)
		HistSimHtPtWeight.SetBinContent(pt, jet, HistSimHtPtGT.GetBinContent(pt, jet))
		HistDataHtPtWeight.SetBinContent(pt, jet, HistDataHtPtGT.GetBinContent(pt, jet))

print str(BinsCount)+" of "+str(nBinsPt*nBinsJet)+" Bins were looped over"
print "Mean weight for Simulation is "+str(meanWeightSim)+" compare to "+str(HistSimHtPtWeight.GetMean())
print "Mean weight for data is "+str(meanWeightData)+" compare to "+str(HistDataHtPtWeight.GetMean())
print "*************** finished setting Bincontents *********************"
print "******************************************************************"

# calculating ration gt/gl in met bins in controll region for sim and data
# fill in 1D histo (set error = 0)
print "Data: GT, then GL"
print GTData
print GLData
print "******************************************************************"
print "Sim: GT, then GL"
print GTSim
print GLSim

print "****************** setting 1D-Bincontents ************************"
i =0
for i,g in enumerate(GT):
	GLData[i] = float(GLData[i])
	GTData[i] = float(GTData[i])
	GLSim[i] = float(GLSim[i])
	GTSim[i] = float(GTSim[i])
	if GLData[i] == 0.:
		GLData[i]=1.
		print "no loose photon in met bin!! set 0 to 1 INVALID PLOTS!" # should only pop up while BreakFill==1
	if GLSim[i]==0.:
		GLSim[i]=1.
		print "no loose photon in met bin!! set 0 to 1 INVALID PLOTS!"
	weightData = GTData[i]/GLData[i]
	weightSim = GTSim[i]/GLSim[i]
	HistDataGTGL.Fill(5+i*10, weightData)
	HistDataGTGL.SetBinError(i+1, 0.)
	HistSimGTGL.Fill(5+i*10, weightSim)
	HistSimGTGL.SetBinError(i+1, 0.)



print "******************************************************************"
print "***************** filling comparison Plots ***********************"

countTestNewMeanWeightSim=0
countFilledWeightBinsSim=0
meanWeightTempSim=0.
countMeanWeightSim=0
MeanPtForMeanWeightEventsSim=0.
MeanHtForMeanWeightEventsSim=0.

countMeanWeightData=0
MeanPtForMeanWeightEventsData=0.
MeanHtForMeanWeightEventsData=0.


for name in Names:
	#if name!="QCD_500_1000_V03" and name!="PhotonA_V04":
	#	continue
	print "******************************************************************"
	print "looping over: "+path+name+IDVersion
	stop=0
	status = "default"
	if name == "ZGammaNuNu_V03":
		print "skipping ZGammaNuNu"
		print "******************************************************************"
		continue
	if name =="PhotonA_V04" or name =="SinglePhotonB_V04" or name =="SinglePhotonC_V04" or name =="PhotonParkedD_V10":
		print "idetified real data"
		status = "data"
		print "status set to "+status
	else:
		if name != "QCD_250_500_V03" and name!="QCD_100_250_V09" and name!="QCD_500_1000_V03" and name!="QCD_1000_inf_V03" and name!="GJets_100_200_V09" and name!="GJets_200_400_V03" and name!="GJets_400_inf_V03" and name!="GJets_40_100_V09":
			print "not QCD or GJets"
			print "skipping..."
			print "******************************************************************"
			continue
		print "identified simulated data"
		status = "sim"
		print "status set to "+status
	tree = FileList[name].Get("myTree")#Inputtree
	if status=="data":
		weight=1
	elif status=="sim":
		weight = Lint/Lsim[name]
	else:
		print "no valid status found... exiting"
		break
	print "weight is "+str(weight)
	for event in tree:
		if BreakFill:
			stop += 1
			if stop ==10000:
				print "breaking loop..."
				break
		UsePhoton=0
		UseJetphoton=0

		if event.met<100: #need these events to get prediction plots for the controll area at the end: "continue"
			"""
			if event.photons.size()>0 and event.jetphotons.size()>0: # if an event has gt and gl use the one with highest pt* and ignore the rest
				if event.photons[0].ptMJet==0 and event.jetphotons[0].ptMJet==0:
					if (event.photons[0].pt-event.jetphotons[0].pt)>0.:
						UsePhoton=1
					else:
						UseJetphoton=1
				elif event.photons[0].ptMJet==0:
					if (event.photons[0].pt-event.jetphotons[0].ptMJet)>0.:
						UsePhoton=1
					else:
						UseJetphoton=1
				elif event.jetphotons[0].ptMJet==0:
					if (event.photons[0].ptMJet-event.jetphotons[0].pt)>0.:
						UsePhoton=1
					else:
						UseJetphoton=1
				else:
					if (event.photons[0].ptMJet-event.jetphotons[0].ptMJet)>0.:
						UsePhoton=1
					else:
						UseJetphoton=1				
			else:# if only gt OR gl exist both possibilities are checked
				UsePhoton=1
				UseJetphoton=1
			"""
			if isSignal(event)=="GL":

				if status=="sim":
					

					if event.jetphotons[0].ptMJet==0:
						Bin = HistSimHtPtWeight.FindFixBin(event.jetphotons[0].pt, event.cleanjets.size())
						weightGTGL = HistSimHtPtWeight.GetBinContent(Bin)
					else:
						Bin = HistSimHtPtWeight.FindFixBin(event.jetphotons[0].ptMJet, event.cleanjets.size())
						weightGTGL = HistSimHtPtWeight.GetBinContent(Bin)


					if status=="sim":#name == "QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
						if weightGTGL <=0.1:
							weightGTGL=meanWeightSim
							HistSimHtPtWeightError.SetBinContent(Bin, 1.)
							"""
							#calculate meanweight arround the empty bin
							#if there are more then 3 filled bins arround use this weight
							for pttemp in range(pt-1, pt+2):
								for httemp in range(jet-1, jet+2):
									if HistSimHtPtWeight.GetBinContent(pttemp, httemp)!=0:
										countFilledWeightBinsSim+=1
										meanWeightTempSim+=HistSimHtPtWeight.GetBinContent(pttemp, httemp)
							if countFilledWeightBinsSim>3:
								weightGTGL=(float(meanWeightTempSim)/float(countFilledWeightBinsSim))
							"""	
						HistSimBackgroundCPredictionMet.Fill(event.met, weight*event.weight*weightGTGL)
						HistSimBackgroundCPredictionMetSys.Fill(event.met, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
						HistSimBackgroundCPredictionMetNW.Fill(event.met, weight*event.weight)
						HistSimBackgroundCPredictionHt.Fill(event.ht, weight*event.weight*weightGTGL)
						HistSimBackgroundCPredictionHtSys.Fill(event.ht, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
						if event.jetphotons[0].ptMJet==0.:
							HistSimBackgroundCPredictionPhotonPt.Fill(event.jetphotons[0].pt, weight*event.weight*weightGTGL)
							HistSimBackgroundCPredictionPhotonPtSys.Fill(event.jetphotons[0].pt, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
						else:
							HistSimBackgroundCPredictionPhotonPt.Fill(event.jetphotons[0].ptMJet, weight*event.weight*weightGTGL)
							HistSimBackgroundCPredictionPhotonPtSys.Fill(event.jetphotons[0].ptMJet, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
				if status=="data":

					if event.jetphotons[0].ptMJet==0:
						Bin = HistDataHtPtWeight.FindFixBin(event.jetphotons[0].pt, event.cleanjets.size())
						weightGTGL = HistDataHtPtWeight.GetBinContent(Bin)
					else:
						Bin = HistDataHtPtWeight.FindFixBin(event.jetphotons[0].ptMJet, event.cleanjets.size())
						weightGTGL = HistDataHtPtWeight.GetBinContent(Bin)

					if weightGTGL <=0.1:
						weightGTGL=meanWeightData
						HistDataHtPtWeightError.SetBinContent(Bin, 1.)
					HistDataBackgroundCPredictionMet.Fill(event.met, weightGTGL)
					HistDataBackgroundCPredictionMetSys.Fill(event.met, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
					HistDataBackgroundCPredictionHt.Fill(event.ht, weightGTGL)
					HistDataBackgroundCPredictionHtSys.Fill(event.ht, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
					if event.jetphotons[0].ptMJet==0.:
						HistDataBackgroundCPredictionPtStar.Fill(event.jetphotons[0].pt, weightGTGL)
						HistDataBackgroundCPredictionPtStarSys.Fill(event.jetphotons[0].pt, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
					else:
						HistDataBackgroundCPredictionPtStar.Fill(event.jetphotons[0].ptMJet, weightGTGL)
						HistDataBackgroundCPredictionPtStarSys.Fill(event.jetphotons[0].ptMJet, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
			if isSignal(event)=="GT":
				if status=="sim":#name == "QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
					HistSimBackgroundCMet.Fill(event.met, weight*event.weight)
					HistSimBackgroundCHt.Fill(event.ht, weight*event.weight)
					if event.photons[0].ptMJet==0:
						HistSimBackgroundCPhotonPt.Fill(event.photons[0].pt, weight*event.weight)
					else:
						HistSimBackgroundCPhotonPt.Fill(event.photons[0].ptMJet, weight*event.weight)

			continue
		if event.met<100: # double checking...
			print "that should not be happening    ### trollolo ###"
			continue
		"""
		if event.photons.size()>0 and event.jetphotons.size()>0: # if an event has gt and gl use the one with highest pt* and ignore the rest
			if event.photons[0].ptMJet==0 and event.jetphotons[0].ptMJet==0:
				if (event.photons[0].pt-event.jetphotons[0].pt)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1
			elif event.photons[0].ptMJet==0:
				if (event.photons[0].pt-event.jetphotons[0].ptMJet)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1
			elif event.jetphotons[0].ptMJet==0:
				if (event.photons[0].ptMJet-event.jetphotons[0].pt)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1
			else:
				if (event.photons[0].ptMJet-event.jetphotons[0].ptMJet)>0.:
					UsePhoton=1
				else:
					UseJetphoton=1				
		else:# if only gt OR gl exist both possibilities are checked
			UsePhoton=1
			UseJetphoton=1
		"""
		if isSignal(event)=="GL":
			if event.jetphotons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGLSignal.Fill(event.jetphotons[0].pt, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGLSignal.Fill(event.jetphotons[0].pt, event.cleanjets.size())
			else:
				if status=="sim":
					HistSimHtPtGLSignal.Fill(event.jetphotons[0].ptMJet, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGLSignal.Fill(event.jetphotons[0].ptMJet, event.cleanjets.size())

			if status=="sim":
				
				if event.jetphotons[0].ptMJet==0:
					Bin = HistSimHtPtWeight.FindFixBin(event.jetphotons[0].pt, event.cleanjets.size())
					weightGTGL = HistSimHtPtWeight.GetBinContent(Bin)
				else:
					Bin = HistSimHtPtWeight.FindFixBin(event.jetphotons[0].ptMJet, event.cleanjets.size())
					weightGTGL = HistSimHtPtWeight.GetBinContent(Bin)

				HistSimGLMultiSignal.Fill(event.cleanjets.size(), weight*event.weight)
				if status=="sim":#name == "QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
					if weightGTGL <=0.1:
						weightGTGL=meanWeightSim
						HistSimHtPtWeightError.SetBinContent(Bin, 1.)
						if event.jetphotons[0].ptMJet==0.:
							HistSimHtPtWeightZeroEvents.Fill(event.jetphotons[0].pt, event.cleanjets.size(), weight*event.weight)
							MeanPtForMeanWeightEventsSim+=event.jetphotons[0].pt
						else:
							MeanPtForMeanWeightEventsSim+=event.jetphotons[0].ptMJet
							HistSimHtPtWeightZeroEvents.Fill(event.jetphotons[0].ptMJet, event.cleanjets.size(), weight*event.weight)
						MeanHtForMeanWeightEventsSim+=event.ht
						countMeanWeightSim+=1
						
						"""
						countFilledWeightBinsSim=0
						meanWeightTempSim=0.
						for pttemp in range(pt-1, pt+2):
							for jettemp in range(jet-1, jet+2):
								if HistSimHtPtWeight.GetBinContent(pttemp, jettemp)!=0:
									countFilledWeightBinsSim+=1
									meanWeightTempSim+=HistSimHtPtWeight.GetBinContent(pttemp, jettemp)
						if countFilledWeightBinsSim>3:
							weightGTGL=(float(meanWeightTempSim)/float(countFilledWeightBinsSim))
							countTestNewMeanWeightSim+=1
						"""
					HistSimBackgroundPredictionMet.Fill(event.met, weight*event.weight*weightGTGL)
					HistSimBackgroundPredictionMetSys.Fill(event.met, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
					HistSimBackgroundMetNW.Fill(event.met, weight*event.weight)
					HistSimBackgroundPredictionHt.Fill(event.ht, weight*event.weight*weightGTGL)
					HistSimBackgroundPredictionHtSys.Fill(event.ht, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
					HistSimBackgroundHtNW.Fill(event.ht, weight*event.weight)
					if event.jetphotons[0].ptMJet==0.:
						HistSimBackgroundPredictionPhotonPt.Fill(event.jetphotons[0].pt, weight*event.weight*weightGTGL)
						HistSimBackgroundPredictionPhotonPtSys.Fill(event.jetphotons[0].pt, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
						HistSimBackgroundPhotonPtNW.Fill(event.jetphotons[0].pt, weight*event.weight)
					else:
						HistSimBackgroundPredictionPhotonPt.Fill(event.jetphotons[0].ptMJet, weight*event.weight*weightGTGL)
						HistSimBackgroundPredictionPhotonPtSys.Fill(event.jetphotons[0].ptMJet, weight*event.weight*weightGTGL*HistSimHtPtWeightError.GetBinContent(Bin))
						HistSimBackgroundPhotonPtNW.Fill(event.jetphotons[0].ptMJet, weight*event.weight)
			if status=="data":

				if event.jetphotons[0].ptMJet==0:
					Bin = HistDataHtPtWeight.FindFixBin(event.jetphotons[0].pt, event.cleanjets.size())
					weightGTGL = HistDataHtPtWeight.GetBinContent(Bin)
				else:
					Bin = HistDataHtPtWeight.FindFixBin(event.jetphotons[0].ptMJet, event.cleanjets.size())
					weightGTGL = HistDataHtPtWeight.GetBinContent(Bin)
				HistDataGLMultiSignal.Fill(event.cleanjets.size())
				if weightGTGL <=0.1:
					countMeanWeightData+=1
					weightGTGL=meanWeightData
					HistDataHtPtWeightError.SetBinContent(Bin, 1.)
					if event.jetphotons[0].ptMJet==0:
						HistDataHtPtWeightZeroEvents.Fill(event.jetphotons[0].pt, event.cleanjets.size())
						MeanPtForMeanWeightEventsData+=event.jetphotons[0].pt
					else:
						MeanPtForMeanWeightEventsData+=event.jetphotons[0].ptMJet
						HistDataHtPtWeightZeroEvents.Fill(event.jetphotons[0].ptMJet, event.cleanjets.size())
					MeanHtForMeanWeightEventsData+=event.ht
				HistDataBackgroundPredictionMet.Fill(event.met, weightGTGL)
				HistDataBackgroundPredictionMetSys.Fill(event.met, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
				HistDataBackgroundPredictionHt.Fill(event.ht, weightGTGL)
				HistDataBackgroundPredictionHtSys.Fill(event.ht, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
				if event.jetphotons[0].ptMJet==0.:
					HistDataBackgroundPredictionPtStar.Fill(event.jetphotons[0].pt, weightGTGL)
					HistDataBackgroundPredictionPtStarSys.Fill(event.jetphotons[0].pt, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
				else:
					HistDataBackgroundPredictionPtStar.Fill(event.jetphotons[0].ptMJet, weightGTGL)
					HistDataBackgroundPredictionPtStarSys.Fill(event.jetphotons[0].ptMJet, weightGTGL*HistDataHtPtWeightError.GetBinContent(Bin))
		if isSignal(event)=="GT":
			if status=="sim":
				HistSimGTMultiSignal.Fill(event.cleanjets.size(), weight*event.weight)
			if status=="data":
				HistDataGTMultiSignal.Fill(event.cleanjets.size(), weight*event.weight)
			if event.photons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGTSignal.Fill(event.photons[0].pt, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGTSignal.Fill(event.photons[0].pt, event.cleanjets.size())
			else:
				if status=="sim":
					HistSimHtPtGTSignal.Fill(event.photons[0].ptMJet, event.cleanjets.size(), weight*event.weight)
				if status=="data":
					HistDataHtPtGTSignal.Fill(event.photons[0].ptMJet, event.cleanjets.size())
			if status=="sim":#name == "QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
				HistSimBackgroundMet.Fill(event.met, weight*event.weight)
				HistSimBackgroundHt.Fill(event.ht, weight*event.weight)
				if event.photons[0].ptMJet==0:
					HistSimBackgroundPhotonPt.Fill(event.photons[0].pt, weight*event.weight)
				else:
					HistSimBackgroundPhotonPt.Fill(event.photons[0].ptMJet, weight*event.weight)

	print "******************************************************************"
print "Sim: Gt(signal) = "+str(HistSimHtPtGTSignal.Integral())+"     Gl(signal) = "+str(HistSimHtPtGLSignal.Integral())
print "Data: Gt(signal) = "+str(HistDataHtPtGTSignal.Integral())+"     Gl(signal) = "+str(HistDataHtPtGLSignal.Integral())
if countMeanWeightSim>0:
	MeanHtForMeanWeightEventsSim=MeanHtForMeanWeightEventsSim/float(countMeanWeightSim)
	MeanPtForMeanWeightEventsSim=MeanPtForMeanWeightEventsSim/float(countMeanWeightSim)
if countMeanWeightData>0:
	MeanHtForMeanWeightEventsData=MeanHtForMeanWeightEventsData/float(countMeanWeightData)
	MeanPtForMeanWeightEventsData=MeanPtForMeanWeightEventsData/float(countMeanWeightData)
print "Simulation: Mean weight had to be used "+str(countMeanWeightSim)+" times because messured weight was zero (only QCD and GJet)"
print "it was used for events with mean values of ht = "+str(MeanHtForMeanWeightEventsSim)+" and Pt* = "+str(MeanPtForMeanWeightEventsSim)
print str(countTestNewMeanWeightSim)+" out of these events now have new meanweight"
print "Data: Mean weight had to be used "+str(countMeanWeightData)+" times because messured weight was zero"
print "it was used for events with mean values of ht = "+str(MeanHtForMeanWeightEventsData)+" and Pt* = "+str(MeanPtForMeanWeightEventsData)
print "******************************************************************"
print "calculate the ratios of Gt(control)/Gl(control) and Gt(signal)/Gl(signal)"
print "Simulation: "+str(float(HistSimHtPtGT.Integral())/float(HistSimHtPtGL.Integral()))+" and "+str(float(HistSimHtPtGTSignal.Integral())/float(HistSimHtPtGLSignal.Integral()))
print "Data: "+str(float(HistDataHtPtGT.Integral())/float(HistDataHtPtGL.Integral()))+" and "+str(float(HistDataHtPtGTSignal.Integral())/float(HistDataHtPtGLSignal.Integral()))

print "******************************************************************"
print "getting systematic errors on prediction now..."
# Bins for HistSimBackgroundCPrediction*Sys :18, 25 ,30 (met,ht.pt)
for i in range(1, 19):
	BinError = HistSimBackgroundCPredictionMetSys.GetBinContent(i)
	HistSimBackgroundCPredictionMetSys.SetBinError(i, BinError)
	BinContent = HistSimBackgroundCPredictionMet.GetBinContent(i)
	HistSimBackgroundCPredictionMetSys.SetBinContent(i, BinContent)
HistSimBackgroundCPredictionMetSys.SetMinimum(1)
HistSimBackgroundCPredictionMetSys.SetMaximum(10000000)

for i in range(1, 26):
	BinError = HistSimBackgroundCPredictionHtSys.GetBinContent(i)
	HistSimBackgroundCPredictionHtSys.SetBinError(i, BinError)
	BinContent = HistSimBackgroundCPredictionHt.GetBinContent(i)
	HistSimBackgroundCPredictionHtSys.SetBinContent(i, BinContent)
HistSimBackgroundCPredictionHtSys.SetMinimum(10)
HistSimBackgroundCPredictionHtSys.SetMaximum(1000000)

for i in range(1, 31):
	BinError = HistSimBackgroundCPredictionPhotonPtSys.GetBinContent(i)
	HistSimBackgroundCPredictionPhotonPtSys.SetBinError(i, BinError)
	BinContent = HistSimBackgroundCPredictionPhotonPt.GetBinContent(i)
	HistSimBackgroundCPredictionPhotonPtSys.SetBinContent(i, BinContent)
HistSimBackgroundCPredictionPhotonPtSys.SetMinimum(0.01)
HistSimBackgroundCPredictionPhotonPtSys.SetMaximum(10000000)
	

# Bins for HistSimBackgroundPrediction*Sys :18, 25 ,30 (met,ht.pt)
for i in range(1, 19):
	BinError = HistSimBackgroundPredictionMetSys.GetBinContent(i)
	HistSimBackgroundPredictionMetSys.SetBinError(i, BinError)
	BinContent = HistSimBackgroundPredictionMet.GetBinContent(i)
	HistSimBackgroundPredictionMetSys.SetBinContent(i, BinContent)
HistSimBackgroundPredictionMetSys.SetMinimum(0.01)
HistSimBackgroundPredictionMetSys.SetMaximum(100000)

for i in range(1, 26):
	BinError = HistSimBackgroundPredictionHtSys.GetBinContent(i)
	HistSimBackgroundPredictionHtSys.SetBinError(i, BinError)
	BinContent = HistSimBackgroundPredictionHt.GetBinContent(i)
	HistSimBackgroundPredictionHtSys.SetBinContent(i, BinContent)
HistSimBackgroundPredictionHtSys.SetMinimum(0.1)
HistSimBackgroundPredictionHtSys.SetMaximum(100000)

for i in range(1, 31):
	BinError = HistSimBackgroundPredictionPhotonPtSys.GetBinContent(i)
	HistSimBackgroundPredictionPhotonPtSys.SetBinError(i, BinError)
	BinContent = HistSimBackgroundPredictionPhotonPt.GetBinContent(i)
	HistSimBackgroundPredictionPhotonPtSys.SetBinContent(i, BinContent)
HistSimBackgroundPredictionPhotonPtSys.SetMinimum(0.001)
HistSimBackgroundPredictionPhotonPtSys.SetMaximum(100000)
	
# Bins for HistDataBackgroundCPrediction*Sys :18, 25 ,30 (met,ht.pt)
for i in range(1, 19):
	BinError = HistDataBackgroundCPredictionMetSys.GetBinContent(i)
	HistDataBackgroundCPredictionMetSys.SetBinError(i, BinError)
	BinContent = HistDataBackgroundCPredictionMet.GetBinContent(i)
	HistDataBackgroundCPredictionMetSys.SetBinContent(i, BinContent)
HistDataBackgroundCPredictionMetSys.SetMinimum(1)
HistDataBackgroundCPredictionMetSys.SetMaximum(10000000)

for i in range(1, 26):
	BinError = HistDataBackgroundCPredictionHtSys.GetBinContent(i)
	HistDataBackgroundCPredictionHtSys.SetBinError(i, BinError)
	BinContent = HistDataBackgroundCPredictionHt.GetBinContent(i)
	HistDataBackgroundCPredictionHtSys.SetBinContent(i, BinContent)
HistDataBackgroundCPredictionHtSys.SetMinimum(10)
HistDataBackgroundCPredictionHtSys.SetMaximum(1000000)

for i in range(1, 31):
	BinError = HistDataBackgroundCPredictionPtStarSys.GetBinContent(i)
	HistDataBackgroundCPredictionPtStarSys.SetBinError(i, BinError)
	BinContent = HistDataBackgroundCPredictionPtStar.GetBinContent(i)
	HistDataBackgroundCPredictionPtStarSys.SetBinContent(i, BinContent)
HistDataBackgroundCPredictionPtStarSys.SetMinimum(0.01)
HistDataBackgroundCPredictionPtStarSys.SetMaximum(10000000)
	
# Bins for HistDataBackgroundPrediction*Sys :18, 25 ,30 (met,ht.pt)
for i in range(1, 19):
	BinError = HistDataBackgroundPredictionMetSys.GetBinContent(i)
	HistDataBackgroundPredictionMetSys.SetBinError(i, BinError)
	BinContent = HistDataBackgroundPredictionMet.GetBinContent(i)
	HistDataBackgroundPredictionMetSys.SetBinContent(i, BinContent)
HistDataBackgroundPredictionMetSys.SetMinimum(0.01)
HistDataBackgroundPredictionMetSys.SetMaximum(100000)

for i in range(1, 26):
	BinError = HistDataBackgroundPredictionHtSys.GetBinContent(i)
	HistDataBackgroundPredictionHtSys.SetBinError(i, BinError)
	BinContent = HistDataBackgroundPredictionHt.GetBinContent(i)
	HistDataBackgroundPredictionHtSys.SetBinContent(i, BinContent)
HistDataBackgroundPredictionHtSys.SetMinimum(0.1)
HistDataBackgroundPredictionHtSys.SetMaximum(100000)

for i in range(1, 31):
	BinError = HistDataBackgroundPredictionPtStarSys.GetBinContent(i)
	HistDataBackgroundPredictionPtStarSys.SetBinError(i, BinError)
	BinContent = HistDataBackgroundPredictionPtStar.GetBinContent(i)
	HistDataBackgroundPredictionPtStarSys.SetBinContent(i, BinContent)
HistDataBackgroundPredictionPtStarSys.SetMinimum(0.001)
HistDataBackgroundPredictionPtStarSys.SetMaximum(100000)

	



print "******************************************************************"
print "printing pdfs and saving histogramms to a TFile"





TFileBackground.cd()


HistDataBackgroundCPredictionPtStarSys.Write("HistDataBackgroundCPredictionPtStarSys")
HistDataBackgroundCPredictionHtSys.Write("HistDataBackgroundCPredictionHtSys")
HistDataBackgroundCPredictionMetSys.Write("HistDataBackgroundCPredictionMetSys")

HistDataBackgroundCPredictionPtStar.Write("HistDataBackgroundCPredictionPtStar")
HistDataBackgroundCPredictionHt.Write("HistDataBackgroundCPredictionHt")
HistDataBackgroundCPredictionMet.Write("HistDataBackgroundCPredictionMet")

ROOT.gStyle.SetOptLogz(0)
Canvas2 = ROOT.TCanvas ("canvas2", "canvas2") # Canvas2 for weight and weightError plots (no logscale for z axis)


HistDataHtPtWeight.Draw("colz")
HistDataHtPtWeight.Write()
ROOT.gPad.SaveAs(homePath+"Data/GtGlRatioHtPtData.pdf")

HistDataHtPtWeight.SetMaximum(5)
HistDataHtPtWeight.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Data/GtGlRatioHtPtDataZoom.pdf")

HistDataHtPtWeightError.Draw("colz")
HistDataHtPtWeightError.Write()
ROOT.gPad.SaveAs(homePath+"Data/GtGlRatioErrorHtPtData.pdf")


Styles.tdrStyle2D()
Canvas1.cd()

HistDataHtPtWeightZeroEvents.Draw("colz")
HistDataHtPtWeightZeroEvents.Write()
ROOT.gPad.SaveAs(homePath+"Data/WeightZeroEventsData.pdf")

HistDataHtPtGTSignal.Draw("colz")
HistDataHtPtGTSignal.Write()
ROOT.gPad.SaveAs(homePath+"Data/GTHtPtDataSignal.pdf")

HistDataHtPtGLSignal.Draw("colz")
HistDataHtPtGLSignal.Write()
ROOT.gPad.SaveAs(homePath+"Data/GLHtPtDataSignal.pdf")

HistIsoGT.Draw("colz")
HistIsoGT.Write()
ROOT.gPad.SaveAs(homePath+"Data/GTIsoData.pdf")

HistIsoGL.Draw("colz")
HistIsoGL.Write()
ROOT.gPad.SaveAs(homePath+"Data/GLIsoData.pdf")

Canvas1D.cd()
HistDataGTMulti.Draw()
HistDataGTMulti.Write()
ROOT.gPad.SaveAs(homePath+"Data/DataGTMulti.pdf")

HistDataGLMulti.Draw()
HistDataGLMulti.Write()
ROOT.gPad.SaveAs(homePath+"Data/DataGLMulti.pdf")

HistDataGTMultiSignal.Draw()
HistDataGTMultiSignal.Write()
ROOT.gPad.SaveAs(homePath+"Data/DataGTMultiSignal.pdf")

HistDataGLMultiSignal.Draw()
HistDataGLMultiSignal.Write()
ROOT.gPad.SaveAs(homePath+"Data/DataGLMultiSignal.pdf")

Canvas1DNLog.cd() # 1D no Log y
# histograms for comparison of jetmultiplicity in controll and signal region

LMultiGT = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGTMulti.Integral())
HistDataGTMulti.Scale(norm)
norm = 1./float(HistDataGTMultiSignal.Integral())
HistDataGTMultiSignal.Scale(norm)
HistDataGTMulti.SetLineColor(2)
HistDataGTMulti.SetMarkerColor(2)
HistDataGTMulti.SetTitle("#gamma_{tight} in signal and controll region")
HistDataGTMulti.Draw()
HistDataGTMultiSignal.Draw("same")
LMultiGT.AddEntry(HistDataGTMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGT.AddEntry(HistDataGTMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGT.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGtControllAndSignal.pdf")

LMultiGL = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGLMulti.Integral())
HistDataGLMulti.Scale(norm)
norm = 1./float(HistDataGLMultiSignal.Integral())
HistDataGLMultiSignal.Scale(norm)
HistDataGLMulti.SetLineColor(2)
HistDataGLMulti.SetMarkerColor(2)
HistDataGLMulti.SetTitle("#gamma_{loose} in signal and controll region")
HistDataGLMulti.Draw()
HistDataGLMultiSignal.Draw("same")
LMultiGL.AddEntry(HistDataGLMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGL.AddEntry(HistDataGLMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGL.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGlControllAndSignal.pdf")

LMultiGLGTSignal = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGTMultiSignal.Integral())
HistDataGTMultiSignal.Scale(norm)
norm = 1./float(HistDataGLMultiSignal.Integral())
HistDataGLMultiSignal.Scale(norm)
HistDataGTMultiSignal.SetLineColor(2)
HistDataGTMultiSignal.SetMarkerColor(2)
HistDataGTMultiSignal.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in signal region")
HistDataGTMultiSignal.Draw()
HistDataGLMultiSignal.Draw("same")
LMultiGLGTSignal.AddEntry(HistDataGTMultiSignal, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGLGTSignal.AddEntry(HistDataGLMultiSignal, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGLGTSignal.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGlGtSignal.pdf")

LMultiGLGTControl = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGTMulti.Integral())
HistDataGTMulti.Scale(norm)
norm = 1./float(HistDataGLMulti.Integral())
HistDataGLMulti.Scale(norm)
HistDataGTMulti.SetLineColor(2)
HistDataGTMulti.SetMarkerColor(2)
HistDataGLMulti.SetLineColor(1)
HistDataGLMulti.SetMarkerColor(1)
HistDataGTMulti.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in control region")
HistDataGTMulti.Draw()
HistDataGLMulti.Draw("same")
LMultiGLGTControl.AddEntry(HistDataGTMulti, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGLGTControl.AddEntry(HistDataGLMulti, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGLGTControl.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGlGtControl.pdf")



Canvas1.cd()

HistDataGTGL.SetTitle(Title[0])
HistDataGTGL.GetXaxis().SetTitle(Title[1])
HistDataGTGL.GetYaxis().SetTitle(Title[2])
HistDataGTGL.GetXaxis().SetTitleOffset(1)
HistDataGTGL.GetYaxis().SetTitleOffset(1.2)

HistDataGTGL.Draw("PE")
ROOT.gPad.SaveAs(homePath+"Data/GtGlRatioMetData.pdf")
HistDataGTGL.Write()

Canvas1D.cd() # for 1D histos
# comparison plots data (compare prediction with QCD and GJet sim.)
LMetData = ROOT.TLegend(.6,.75,.9,.9)
HistDataBackgroundPredictionMet.SetMarkerSize(0)
HistDataBackgroundPredictionMetSys.SetMarkerSize(0)
HistDataBackgroundPredictionMetSys.SetFillColor(4)
HistDataBackgroundPredictionMetSys.SetFillStyle(3254)
HistDataBackgroundPredictionMetSys.Draw("E2")
HistDataBackgroundPredictionMet.Draw("same Ehist")
HistSimBackgroundMet.Draw("same PEX0")
LMetData.AddEntry(HistDataBackgroundPredictionMet, "Predicion for #gamma_{tight}", "l")
LMetData.AddEntry(HistSimBackgroundMet, "#gamma_{tight} QCD+GJets", "ep")
LMetData.AddEntry(HistDataBackgroundPredictionMetSys, "#sigma_{sys}", "f")
LMetData.Draw()
ROOT.gPad.SaveAs(homePath+"Data/ComparisonDataMet.pdf")
HistDataBackgroundPredictionMet.Write()
HistSimBackgroundMet.Write()
HistDataBackgroundPredictionMetSys.Write("HistDataBackgroundPredictionMetSys")

LHtData = ROOT.TLegend(.6,.75,.9,.9)
HistDataBackgroundPredictionHt.SetMarkerSize(0)
HistDataBackgroundPredictionHtSys.SetMarkerSize(0)
HistDataBackgroundPredictionHtSys.SetFillColor(4)
HistDataBackgroundPredictionHtSys.SetFillStyle(3254)
HistDataBackgroundPredictionHtSys.Draw("E2")
HistDataBackgroundPredictionHt.Draw("same Ehist")
HistSimBackgroundHt.Draw("samePEX0")
LHtData.AddEntry(HistDataBackgroundPredictionHt, "Predicion for #gamma_{tight}", "f")
LHtData.AddEntry(HistSimBackgroundHt, "#gamma_{tight} QCD+GJets", "ep")
LHtData.AddEntry(HistDataBackgroundPredictionHtSys, "#sigma_{sys}", "f")
LHtData.Draw()
ROOT.gPad.SaveAs(homePath+"Data/ComparisonDataHt.pdf")
HistDataBackgroundPredictionHt.Write()
HistSimBackgroundHt.Write()
HistDataBackgroundPredictionHtSys.Write("HistDataBackgroundPredictionHtSys")

LPtData = ROOT.TLegend(.6,.75,.9,.9)
HistDataBackgroundPredictionPtStar.SetMarkerSize(0)
HistDataBackgroundPredictionPtStarSys.SetMarkerSize(0)
HistDataBackgroundPredictionPtStarSys.SetFillColor(4)
HistDataBackgroundPredictionPtStarSys.SetFillStyle(3254)
HistDataBackgroundPredictionPtStarSys.Draw("E2")
HistDataBackgroundPredictionPtStar.Draw("same Ehist")
HistSimBackgroundPhotonPt.Draw("same PEX0")
LPtData.AddEntry(HistDataBackgroundPredictionPtStar, "Predicion for #gamma_{tight}", "f")
LPtData.AddEntry(HistSimBackgroundPhotonPt, "#gamma_{tight} QCD+GJets", "ep")
LPtData.AddEntry(HistDataBackgroundPredictionPtStarSys, "#sigma_{sys}", "f")
LPtData.Draw()
ROOT.gPad.SaveAs(homePath+"Data/ComparisonDataPt.pdf")
HistDataBackgroundPredictionPtStar.Write()
HistSimBackgroundPhotonPt.Write()
HistDataBackgroundPredictionPtStarSys.Write("HistDataBackgroundPredictionPtStarSys")

# SIM Plots

#comparison plots sim
Canvas1D.cd() # for 1D histos
LMet = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundMetNW.SetLineColor(2)
HistSimBackgroundMetNW.SetMarkerSize(0)
HistSimBackgroundPredictionMet.SetMarkerSize(0)
HistSimBackgroundPredictionMetSys.SetMarkerSize(0)
HistSimBackgroundPredictionMet.SetMinimum( 0.01 )
HistSimBackgroundPredictionMet.SetMaximum( 100000000 )
HistSimBackgroundMet.SetMinimum( 0.01 )
HistSimBackgroundMet.SetMaximum( 100000000 )
HistSimBackgroundMetNW.SetMinimum( 0.01 )
HistSimBackgroundMetNW.SetMaximum( 100000000 )
HistSimBackgroundPredictionMetSys.SetFillColor(4)
HistSimBackgroundPredictionMetSys.SetFillStyle(3254)
HistSimBackgroundPredictionMetSys.Draw("E2")
HistSimBackgroundPredictionMet.Draw("same Ehist")
HistSimBackgroundMetNW.Draw("same Ehist")
HistSimBackgroundMet.Draw("same PEX0")
LMet.AddEntry(HistSimBackgroundPredictionMet, "Predicion for #gamma_{tight}", "l")
LMet.AddEntry(HistSimBackgroundMetNW, "#gamma_{loose}", "l")
LMet.AddEntry(HistSimBackgroundMet, "#gamma_{tight}", "ep")
LMet.AddEntry(HistSimBackgroundPredictionMetSys, "#sigma_{sys}", "f")
LMet.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimMet.pdf")
HistSimBackgroundPredictionMet.Write()
HistSimBackgroundMet.Write()
HistSimBackgroundPredictionMetSys.Write("HistSimBackgroundPredictionMetSys")

LHt = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundHtNW.SetLineColor(2)
HistSimBackgroundHtNW.SetMarkerSize(0)
HistSimBackgroundPredictionHt.SetMarkerSize(0)
HistSimBackgroundPredictionHtSys.SetMarkerSize(0)
HistSimBackgroundPredictionHt.SetMinimum( 0.01 )
HistSimBackgroundPredictionHt.SetMaximum( 100000000 )
HistSimBackgroundHt.SetMinimum( 0.01 )
HistSimBackgroundHt.SetMaximum( 100000000 )
HistSimBackgroundHtNW.SetMinimum( 0.01 )
HistSimBackgroundHtNW.SetMaximum( 100000000 )
HistSimBackgroundPredictionHtSys.SetFillColor(4)
HistSimBackgroundPredictionHtSys.SetFillStyle(3254)
HistSimBackgroundPredictionHtSys.Draw("E2")
HistSimBackgroundPredictionHt.Draw("same Ehist")
HistSimBackgroundHtNW.Draw("sameEhist")
HistSimBackgroundHt.Draw("samePEX0")
LHt.AddEntry(HistSimBackgroundPredictionHt, "Predicion for #gamma_{tight}", "l")
LHt.AddEntry(HistSimBackgroundHtNW, "#gamma_{loose}", "l")
LHt.AddEntry(HistSimBackgroundHt, "#gamma_{tight}", "ep")
LHt.AddEntry(HistSimBackgroundPredictionHtSys, "#sigma_{sys}", "f")
LHt.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimHt.pdf")
HistSimBackgroundPredictionHt.Write()
HistSimBackgroundHt.Write()
HistSimBackgroundPredictionHtSys.Write("HistSimBackgroundPredictionHtSys")

LPhotonPt = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundPhotonPtNW.SetLineColor(2)
HistSimBackgroundPhotonPtNW.SetMarkerSize(0)
HistSimBackgroundPredictionPhotonPtSys.SetMarkerSize(0)
HistSimBackgroundPredictionPhotonPt.SetMarkerSize(0)
HistSimBackgroundPredictionPhotonPt.SetMinimum( 0.01 )
HistSimBackgroundPredictionPhotonPt.SetMaximum( 100000000 )
HistSimBackgroundPhotonPt.SetMinimum( 0.01 )
HistSimBackgroundPhotonPt.SetMaximum( 100000000 )
HistSimBackgroundPhotonPtNW.SetMinimum( 0.01 )
HistSimBackgroundPhotonPtNW.SetMaximum( 100000000 )
HistSimBackgroundPredictionPhotonPtSys.SetFillColor(4)
HistSimBackgroundPredictionPhotonPtSys.SetFillStyle(3254)
HistSimBackgroundPredictionPhotonPtSys.Draw("E2")
HistSimBackgroundPredictionPhotonPt.Draw("same Ehist")
HistSimBackgroundPhotonPtNW.Draw("sameEhist")
HistSimBackgroundPhotonPt.Draw("samePEX0")
LPhotonPt.AddEntry(HistSimBackgroundPredictionPhotonPt, "Predicion for #gamma_{tight}", "l")
LPhotonPt.AddEntry(HistSimBackgroundPhotonPtNW, "#gamma_{loose}", "l")
LPhotonPt.AddEntry(HistSimBackgroundPhotonPt, "#gamma_{tight}", "ep")
LPhotonPt.AddEntry(HistSimBackgroundPredictionPhotonPtSys, "#sigma_{sys}", "f")
LPhotonPt.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimPt.pdf")
HistSimBackgroundPredictionPhotonPt.Write()
HistSimBackgroundPhotonPt.Write()
HistSimBackgroundPredictionPhotonPtSys.Write("HistSimBackgroundPredictionPhotonPtSys")

#comparison plots sim in controll region
Canvas1D.cd() # for 1D histos
LMetC = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundCPredictionMetNW.SetLineColor(2)
HistSimBackgroundCPredictionMetNW.SetMarkerSize(0)
HistSimBackgroundCPredictionMetSys.SetMarkerSize(0)
HistSimBackgroundCPredictionMet.SetMarkerSize(0)
HistSimBackgroundCPredictionMet.SetMinimum( 0.01 )
HistSimBackgroundCPredictionMet.SetMaximum( 100000000 )
HistSimBackgroundCMet.SetMinimum( 0.01 )
HistSimBackgroundCMet.SetMaximum( 100000000 )
HistSimBackgroundCPredictionMetSys.SetFillColor(4)
HistSimBackgroundCPredictionMetSys.SetFillStyle(3254)
HistSimBackgroundCPredictionMetSys.Draw("E2")
HistSimBackgroundCPredictionMet.Draw("same Ehist")
HistSimBackgroundCPredictionMetNW.Draw("same hist")
HistSimBackgroundCMet.Draw("same PEX0")
LMetC.AddEntry(HistSimBackgroundCPredictionMet, "Predicion for #gamma_{tight}", "l")
LMetC.AddEntry(HistSimBackgroundCMet, "#gamma_{tight}", "ep")
LMetC.AddEntry(HistSimBackgroundCPredictionMetSys, "#sigma_{sys}", "f")
LMetC.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimMetControllRegion.pdf")
HistSimBackgroundCPredictionMet.Write()
HistSimBackgroundCMet.Write()
HistSimBackgroundCPredictionMetSys.Write("HistSimBackgroundCPredictionMetSys")

LHtC = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundCPredictionHtSys.SetMarkerSize(0)
HistSimBackgroundCPredictionHt.SetMarkerSize(0)
HistSimBackgroundCPredictionHt.SetMinimum( 0.01 )
HistSimBackgroundCPredictionHt.SetMaximum( 100000000 )
HistSimBackgroundCHt.SetMinimum( 0.01 )
HistSimBackgroundCHt.SetMaximum( 100000000 )
HistSimBackgroundCPredictionHtSys.SetFillColor(4)
HistSimBackgroundCPredictionHtSys.SetFillStyle(3254)
HistSimBackgroundCPredictionHtSys.Draw("E2")
HistSimBackgroundCPredictionHt.Draw("same Ehist")
HistSimBackgroundCHt.Draw("same PEX0")
LHtC.AddEntry(HistSimBackgroundCPredictionHt, "Predicion for #gamma_{tight}", "l")
LHtC.AddEntry(HistSimBackgroundCHt, "#gamma_{tight}", "ep")
LHtC.AddEntry(HistSimBackgroundCPredictionHtSys, "#sigma_{sys}", "f")
LHtC.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimHtControllRegion.pdf")
HistSimBackgroundCPredictionHt.Write()
HistSimBackgroundCHt.Write()
HistSimBackgroundCPredictionHtSys.Write("HistSimBackgroundCPredictionHtSys")

LPhotonPtC = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundCPredictionPhotonPtSys.SetMarkerSize(0)
HistSimBackgroundCPredictionPhotonPt.SetMarkerSize(0)
HistSimBackgroundCPredictionPhotonPt.SetMinimum( 0.01 )
HistSimBackgroundCPredictionPhotonPt.SetMaximum( 100000000 )
HistSimBackgroundCPhotonPt.SetMinimum( 0.01 )
HistSimBackgroundCPhotonPt.SetMaximum( 100000000 )
HistSimBackgroundCPredictionPhotonPtSys.SetFillColor(4)
HistSimBackgroundCPredictionPhotonPtSys.SetFillStyle(3254)
HistSimBackgroundCPredictionPhotonPtSys.Draw("E2")
HistSimBackgroundCPredictionPhotonPt.Draw("same Ehist")
HistSimBackgroundCPhotonPt.Draw("same PEX0")
LPhotonPtC.AddEntry(HistSimBackgroundCPredictionPhotonPt, "Predicion for #gamma_{tight}", "l")
LPhotonPtC.AddEntry(HistSimBackgroundCPhotonPt, "#gamma_{tight}", "ep")
LPhotonPtC.AddEntry(HistSimBackgroundCPredictionPhotonPtSys, "#sigma_{sys}", "f")
LPhotonPtC.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimPtControllRegion.pdf")
HistSimBackgroundCPredictionPhotonPt.Write()
HistSimBackgroundCPhotonPt.Write()
HistSimBackgroundCPredictionPhotonPtSys.Write("HistSimBackgroundCPredictionPhotonPtSys")


HistSimGTMulti.Draw()
HistSimGTMulti.Write()
ROOT.gPad.SaveAs(homePath+"Sim/SimGTMulti.pdf")

HistSimGLMulti.Draw()
HistSimGLMulti.Write()
ROOT.gPad.SaveAs(homePath+"Sim/SimGLMulti.pdf")

HistSimGTMultiSignal.Draw()
HistSimGTMultiSignal.Write()
ROOT.gPad.SaveAs(homePath+"Sim/SimGTMultiSignal.pdf")

HistSimGLMultiSignal.Draw()
HistSimGLMultiSignal.Write()
ROOT.gPad.SaveAs(homePath+"Sim/SimGLMultiSignal.pdf")

Canvas1DNLog.cd() # 1D no Log y
# histograms for comparison of jetmultiplicity in controll and signal region

LMultiGTSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGTMulti.Integral())
HistSimGTMulti.Scale(norm)
norm = 1./float(HistSimGTMultiSignal.Integral())
HistSimGTMultiSignal.Scale(norm)
HistSimGTMulti.SetLineColor(2)
HistSimGTMulti.SetMarkerColor(2)
HistSimGTMulti.SetTitle("#gamma_{tight} in signal and controll region")
HistSimGTMulti.Draw()
HistSimGTMultiSignal.Draw("same")
LMultiGTSim.AddEntry(HistSimGTMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGTSim.AddEntry(HistSimGTMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGTSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGtControllAndSignal.pdf")

LMultiGLSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGLMulti.Integral())
HistSimGLMulti.Scale(norm)
norm = 1./float(HistSimGLMultiSignal.Integral())
HistSimGLMultiSignal.Scale(norm)
HistSimGLMulti.SetLineColor(2)
HistSimGLMulti.SetMarkerColor(2)
HistSimGLMulti.SetTitle("#gamma_{loose} in signal and controll region")
HistSimGLMulti.Draw()
HistSimGLMultiSignal.Draw("same")
LMultiGLSim.AddEntry(HistSimGLMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGLSim.AddEntry(HistSimGLMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGLSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGlControllAndSignal.pdf")

LMultiGLGTSignalSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGTMultiSignal.Integral())
HistSimGTMultiSignal.Scale(norm)
norm = 1./float(HistSimGLMultiSignal.Integral())
HistSimGLMultiSignal.Scale(norm)
HistSimGTMultiSignal.SetLineColor(2)
HistSimGTMultiSignal.SetMarkerColor(2)
HistSimGTMultiSignal.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in signal region")
HistSimGTMultiSignal.Draw()
HistSimGLMultiSignal.Draw("same")
LMultiGLGTSignalSim.AddEntry(HistSimGTMultiSignal, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGLGTSignalSim.AddEntry(HistSimGLMultiSignal, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}>100GeV", "lep")
LMultiGLGTSignalSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGlGtSignal.pdf")

LMultiGLGTControlSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGTMulti.Integral())
HistSimGTMulti.Scale(norm)
norm = 1./float(HistSimGLMulti.Integral())
HistSimGLMulti.Scale(norm)
HistSimGTMulti.SetLineColor(2)
HistSimGLMulti.SetLineColor(1)
HistSimGTMulti.SetMarkerColor(2)
HistSimGLMulti.SetMarkerColor(1)
HistSimGTMulti.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in control region")
HistSimGLMulti.Draw()
HistSimGTMulti.Draw("same")
LMultiGLGTControlSim.AddEntry(HistSimGTMulti, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGLGTControlSim.AddEntry(HistSimGLMulti, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}<100GeV", "lep")
LMultiGLGTControlSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGlGtControl.pdf")


Canvas2.cd() # no log axis for z
HistSimHtPtWeightError.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioErrorHtPtSim.pdf")
HistSimHtPtWeightError.Write()

HistSimHtPtWeight.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioHtPtSim.pdf")
HistSimHtPtWeight.Write()

HistSimHtPtWeight.SetMaximum(5)
HistSimHtPtWeight.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioHtPtSimZoom.pdf")

Canvas1.cd()

HistSimHtPtGTSignal.Draw("colz")
HistSimHtPtGTSignal.Write()
ROOT.gPad.SaveAs(homePath+"Sim/GTHtPtSimSignal.pdf")

HistSimHtPtGLSignal.Draw("colz")
HistSimHtPtGLSignal.Write()
ROOT.gPad.SaveAs(homePath+"Sim/GLHtPtSimSignal.pdf")

HistSimHtPtWeightZeroEvents.Draw("colz")
HistSimHtPtWeightZeroEvents.Write()
ROOT.gPad.SaveAs(homePath+"Sim/WeightZeroEventsSim.pdf")

HistSimIsoGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTIsoSim.pdf")
HistSimIsoGT.Write()

HistSimIsoGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLIsoSim.pdf")
HistSimIsoGL.Write()

HistSimGTGL.SetTitle(Title[0])
HistSimGTGL.GetXaxis().SetTitle(Title[1])
HistSimGTGL.GetYaxis().SetTitle(Title[2])
HistSimGTGL.GetXaxis().SetTitleOffset(1)
HistSimGTGL.GetYaxis().SetTitleOffset(1.2)

HistSimGTGL.Draw("PE")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioMetSim.pdf")
HistSimGTGL.Write()
