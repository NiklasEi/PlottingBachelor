import ROOT
import sys
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
ROOT.TH1.SetDefaultSumw2()
#e=2.7182818284590452353602874713526624977572470937




# reading scale Histos
# this was a test wether a scalfactor depending on jets.size() would improve the method, it failed
"""
TFileJetScale = ROOT.TFile("TFileJetScale.root")
GTJetMultiRatioSim = TFileJetScale.Get("SimGTMulti")
GLJetMultiRatioSim = TFileJetScale.Get("SimGLMulti")
"""



# change status to recreate if you change keys in .Write() otherwise "update"
TFileBackground = ROOT.TFile("TFileBackground.root", "recreate")

"""
this program aims to find weights for GammaLoose (GL) to predict their
fakerate (faking GammaTight GT)
The Controll region to find these weights are all events with Met<100 (no possible signal)

To be able to varify the method it is used on simulated data.
(QCD and GJet samples)
"""


simulated = ROOT.TChain("myTree")
data = ROOT.TChain("myTree")

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

nBinsHt = 35 # set number of Bins in Ht for 2D Plots
nBinsPt = 30 # set number of Bins in Pt for 2D Plots
PtMin = 175
PtMax = 1000
HtMin = 0
HtMax = 1900

"""
									Histograms for Data
"""
#Hist for GT objects binned in Ht and PhotonPt* in controll region
HistDataHtPtGT = ROOT.TH2F( "DataHtPtGT", "DataHtPtGT", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtGT.SetTitle(Title[0]+" #gamma_{tight}, E_{T}^{miss}<100")
HistDataHtPtGT.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGT.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt* in controll region
HistDataHtPtGL = ROOT.TH2F( "DataHtPtGL", "DataHtPtGL", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtGL.SetTitle(Title[0]+" #gamma_{loose}, E_{T}^{miss}<100")
HistDataHtPtGL.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGL.GetYaxis().SetTitle("Ht")

#Hist for GT objects binned in Ht and PhotonPt* in signal region
HistDataHtPtGTSignal = ROOT.TH2F( "DataHtPtGTSignal", "DataHtPtGTSignal", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtGTSignal.SetTitle(Title[0]+" #gamma_{tight}, E_{T}^{miss}>100")
HistDataHtPtGTSignal.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGTSignal.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt* in signal region
HistDataHtPtGLSignal = ROOT.TH2F( "DataHtPtGLSignal", "DataHtPtGLSignal", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtGLSignal.SetTitle(Title[0]+" #gamma_{loose}, E_{T}^{miss}>100")
HistDataHtPtGLSignal.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGLSignal.GetYaxis().SetTitle("Ht")

#Hist for weight binned like HistDataHtPtGT and HistDataHtPtGL. Weight is GT/GL in every bin
HistDataHtPtWeight = ROOT.TH2F( "DataHtPtWeight", "DataHtPtWeight", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtWeight.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtWeight.GetYaxis().SetTitle("Ht")
HistDataHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose}")

#Error on weight
HistDataHtPtWeightError = ROOT.TH2F( "DataHtPtWeightError", "DataHtPtWeightError", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtWeightError.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtWeightError.GetYaxis().SetTitle("Ht")
HistDataHtPtWeightError.SetTitle(Title[0]+" #sigma_{w_{i}}/w_{i}")

#Events with weight==0 (bevor set to mean)
HistDataHtPtWeightZeroEvents = ROOT.TH2F( "DataHtPtWeightZeroEvents", "DataHtPtWeightZeroEvents", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
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
HistDataBackgroundPredictionMet = ROOT.TH1F( "DataBackgroundPredictionMet", "DataBackgroundPredictionMet", 30, 0, 900 )
HistDataBackgroundPredictionMet.SetTitle(Title[0])
HistDataBackgroundPredictionMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistDataBackgroundPredictionMet.GetYaxis().SetTitle("Events")

# Background prediction for data estimated with weights plottet with Ht
HistDataBackgroundPredictionHt = ROOT.TH1F( "DataBackgroundPredictionHt", "DataBackgroundPredictionHt", 50, 0, 1400 )
HistDataBackgroundPredictionHt.SetTitle(Title[0])
HistDataBackgroundPredictionHt.GetXaxis().SetTitle("Ht(GeV)")
HistDataBackgroundPredictionHt.GetYaxis().SetTitle("Events")

# Background prediction for data estimated with weights plottet with Pt*
HistDataBackgroundPredictionPtStar = ROOT.TH1F( "DataBackgroundPredictionPtStar", "DataBackgroundPredictionPtStar", 50, 0, 1400 )
HistDataBackgroundPredictionPtStar.SetTitle(Title[0])
HistDataBackgroundPredictionPtStar.GetXaxis().SetTitle("P_{T}*(GeV)")
HistDataBackgroundPredictionPtStar.GetYaxis().SetTitle("Events")

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
HistSimHtPtGT = ROOT.TH2F( "SimHtPtGT", "SimHtPtGT", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGT.SetTitle(Title[0]+" #gamma_{tight} simulated data, E_{T}^{miss}<100")
HistSimHtPtGT.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGT.GetYaxis().SetTitle("Ht")

#hist for GL binned in pt ht with weights in controll region
HistSimHtPtGL = ROOT.TH2F( "SimHtPtGL", "SimHtPtGL", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGL.SetTitle(Title[0]+" #gamma_{loose} simulated data, E_{T}^{miss}<100")
HistSimHtPtGL.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGL.GetYaxis().SetTitle("Ht")

#Hist for GT objects binned in Ht and PhotonPt* in signal region
HistSimHtPtGTSignal = ROOT.TH2F( "SimHtPtGTSignal", "SimHtPtGTSignal", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGTSignal.SetTitle(Title[0]+" #gamma_{tight}, E_{T}^{miss}>100")
HistSimHtPtGTSignal.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGTSignal.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt* in signal region
HistSimHtPtGLSignal = ROOT.TH2F( "SimHtPtGLSignal", "SimHtPtGLSignal", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGLSignal.SetTitle(Title[0]+" #gamma_{loose}, E_{T}^{miss}>100")
HistSimHtPtGLSignal.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGLSignal.GetYaxis().SetTitle("Ht")

#hist for data weight (gt/gl)
HistSimHtPtWeight = ROOT.TH2F( "SimHtPtWeight", "SimHtPtWeight", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtWeight.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeight.GetYaxis().SetTitle("Ht")
HistSimHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose} simulated data")

#weight error 
HistSimHtPtWeightError = ROOT.TH2F( "SimHtPtWeightError", "SimHtPtWeightError", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtWeightError.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeightError.GetYaxis().SetTitle("Ht")
HistSimHtPtWeightError.SetTitle(Title[0]+" #sigma_{w_{i}}/w_{i}")

#Events with weight==0 (bevor set to mean)
HistSimHtPtWeightZeroEvents = ROOT.TH2F( "SimHtPtWeightZeroEvents", "SimHtPtWeightZeroEvents", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
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
HistSimBackgroundPredictionMet = ROOT.TH1F( "SimBackgroundPredictionMet", "SimBackgroundPredictionMet", 30, 0, 900)
HistSimBackgroundPredictionMet.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPredictionMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundPredictionMet.GetYaxis().SetTitle("Events")

HistSimBackgroundMet = ROOT.TH1F( "SimBackgroundMet", "SimBackgroundMet", 30, 0, 900)
HistSimBackgroundMet.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundMet.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundMet.GetYaxis().SetTitle("Events")

# Background no weights
HistSimBackgroundMetNW = ROOT.TH1F( "SimBackgroundMetNW", "SimBackgroundMetNW", 30, 0, 900)
HistSimBackgroundMetNW.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundMetNW.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundMetNW.GetYaxis().SetTitle("Events")

# prediction and Background against Ht
HistSimBackgroundPredictionHt = ROOT.TH1F( "SimBackgroundPredictionHt", "SimBackgroundPredictionHt", 50, 0, 1400)
HistSimBackgroundPredictionHt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPredictionHt.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundPredictionHt.GetYaxis().SetTitle("Events")

HistSimBackgroundHt = ROOT.TH1F( "SimBackgroundHt", "SimBackgroundHt", 50, 0, 1400)
HistSimBackgroundHt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundHt.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundHt.GetYaxis().SetTitle("Events")

# Background no weight
HistSimBackgroundHtNW = ROOT.TH1F( "SimBackgroundHtNW", "SimBackgroundHtNW", 50, 0, 1400)
HistSimBackgroundHtNW.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundHtNW.GetXaxis().SetTitle("Ht(GeV)")
HistSimBackgroundHtNW.GetYaxis().SetTitle("Events")

# prediction and Background against PhotonPt
HistSimBackgroundPredictionPhotonPt = ROOT.TH1F( "SimBackgroundPredictionPhotonPt", "SimBackgroundPredictionPhotonPt", 50, 0, 1400)
HistSimBackgroundPredictionPhotonPt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPredictionPhotonPt.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundPredictionPhotonPt.GetYaxis().SetTitle("Events")

HistSimBackgroundPhotonPt = ROOT.TH1F( "SimBackgroundPhotonPt", "SimBackgroundPhotonPt", 50, 0, 1400)
HistSimBackgroundPhotonPt.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPhotonPt.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundPhotonPt.GetYaxis().SetTitle("Events")

# Background no weight
HistSimBackgroundPhotonPtNW = ROOT.TH1F( "SimBackgroundPhotonPtNW", "SimBackgroundPhotonPtNW", 50, 0, 1400)
HistSimBackgroundPhotonPtNW.SetTitle(Title[0]+" Comparison for QCD and GJet samples")
HistSimBackgroundPhotonPtNW.GetXaxis().SetTitle("P_{T}*(GeV)")
HistSimBackgroundPhotonPtNW.GetYaxis().SetTitle("Events")

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
			continue # filter for controll region
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
		else:# if only gt OR gl exist both possibilities are checked
			UsePhoton=1
			UseJetphoton=1
		if event.photons.size()>0 and UsePhoton==1:
			if status=="sim":
				HistSimGTMulti.Fill(event.cleanjets.size(), weight*event.weight)	
				HistSimIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso, weight*event.weight )
			elif status=="data":
				HistDataGTMulti.Fill(event.cleanjets.size())
				HistIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso)
			if event.photons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGT.Fill(event.photons[0].pt, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGT.Fill(event.photons[0].pt, event.ht)
			else:
				if status=="sim":
					HistSimHtPtGT.Fill(event.photons[0].ptMJet, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGT.Fill(event.photons[0].ptMJet, event.ht)
			
		if event.jetphotons.size()>0 and UseJetphoton==1:
			if status=="sim":
				HistSimGLMulti.Fill(event.cleanjets.size(), weight*event.weight)	
				HistSimIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso, weight*event.weight )
			if status=="data":
				HistDataGLMulti.Fill(event.cleanjets.size())
				HistIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso)
			if event.jetphotons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGL.Fill(event.jetphotons[0].pt, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGL.Fill(event.jetphotons[0].pt, event.ht)
			else:
				if status=="sim":
					HistSimHtPtGL.Fill(event.jetphotons[0].ptMJet, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGL.Fill(event.jetphotons[0].ptMJet, event.ht)


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

HistDataHtPtGT.Draw("colz")
HistDataHtPtGT.Write()
ROOT.gPad.SaveAs(homePath+"Data/GTHtPtData.pdf")

HistSimHtPtGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLHtPtSim.pdf")
HistSimHtPtGL.Write()

HistSimHtPtGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTHtPtSim.pdf")
HistSimHtPtGT.Write()


BinsCount=0		
countData=0
countSim=0
print "****************** setting 2D-Bincontents ************************"

HistDataHtPtGT.Divide(HistDataHtPtGL)
HistSimHtPtGT.Divide(HistSimHtPtGL)
countWeightsSim=0.
meanWeightSim=0.
countWeightsData=0.
meanWeightData=0.
for ht in range(1, nBinsHt+1): # Bin numbers start at 1 first bin (1,1)
	for pt in range(1, nBinsPt+1):
		BinsCount+=1
		if ht>=pt:
			countWeightsSim+=1.
			countWeightsData+=1.
		if HistSimHtPtGT.GetBinContent(pt, ht)!=0:
			#countWeightsSim+=1.
			meanWeightSim+=HistSimHtPtGT.GetBinContent(pt, ht)
			HistSimHtPtWeightError.SetBinContent(pt, ht, (float(HistSimHtPtGT.GetBinError(pt, ht))/float(HistSimHtPtGT.GetBinContent(pt, ht)))) # relative Error on w(i)
		elif HistSimHtPtGT.GetBinContent(pt, ht)==0:
			HistSimHtPtWeightError.SetBinContent(pt, ht, 0) # relative Error on w(i)

		if HistDataHtPtGT.GetBinContent(pt, ht)!=0:
			#countWeightsData+=1.
			meanWeightData+=HistDataHtPtGT.GetBinContent(pt, ht)
			HistDataHtPtWeightError.SetBinContent(pt, ht, (float(HistDataHtPtGT.GetBinError(pt, ht))/float(HistDataHtPtGT.GetBinContent(pt, ht))))
		elif HistDataHtPtGT.GetBinContent(pt, ht)==0:
			HistDataHtPtWeightError.SetBinContent(pt, ht, 0)

		HistSimHtPtWeight.SetBinContent(pt, ht, HistSimHtPtGT.GetBinContent(pt, ht))
		HistDataHtPtWeight.SetBinContent(pt, ht, HistDataHtPtGT.GetBinContent(pt, ht))
meanWeightSim=(float(meanWeightSim)/float(countWeightsSim)) # calculate meanweight for empty Bins for simulation
meanWeightData=(float(meanWeightData)/float(countWeightsData)) # same for data
print str(BinsCount)+" of "+str(nBinsHt*nBinsPt)+" Bins were looped over"
print "Mean weight for Simulation is "+str(meanWeightSim)
print "Mean weight for data is "+str(meanWeightData)
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
		if event.met<100:
			continue
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
		if event.jetphotons.size()>0 and UseJetphoton==1:
			if event.jetphotons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGLSignal.Fill(event.jetphotons[0].pt, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGLSignal.Fill(event.jetphotons[0].pt, event.ht)
				pt, nothing = divmod(event.jetphotons[0].pt, (float(PtMax-PtMin)/float(nBinsPt)))  # evaluate ht-pt bin event is in
			else:
				if status=="sim":
					HistSimHtPtGLSignal.Fill(event.jetphotons[0].ptMJet, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGLSignal.Fill(event.jetphotons[0].ptMJet, event.ht)
				pt, nothing = divmod(event.jetphotons[0].ptMJet, (float(PtMax-PtMin)/float(nBinsPt)))
			ht, nothing = divmod(event.ht, (float(HtMax-HtMin)/float(nBinsHt)))
			pt = int(pt)+1 # bin numbers start at 1
			ht = int(ht)+1
			if status=="sim":
				#weightJet = GLJetMultiRatioSim.GetBinContent(event.jets.size()+1)
				HistSimGLMultiSignal.Fill(event.cleanjets.size(), weight*event.weight)
				weightGTGL = HistSimHtPtWeight.GetBinContent(pt, ht)
				if name == "QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
					if weightGTGL==0.:
						weightGTGL=meanWeightSim
						if event.jetphotons[0].ptMJet==0.:
							HistSimHtPtWeightZeroEvents.Fill(event.jetphotons[0].pt, event.ht, weight*event.weight)
							MeanPtForMeanWeightEventsSim+=event.jetphotons[0].pt
						else:
							MeanPtForMeanWeightEventsSim+=event.jetphotons[0].ptMJet
							HistSimHtPtWeightZeroEvents.Fill(event.jetphotons[0].ptMJet, event.ht, weight*event.weight)
						MeanHtForMeanWeightEventsSim+=event.ht
						countMeanWeightSim+=1
						
						countFilledWeightBinsSim=0
						meanWeightTempSim=0.
						for pttemp in range(pt-1, pt+2):
							for httemp in range(ht-1, ht+2):
								if HistSimHtPtWeight.GetBinContent(pttemp, httemp)!=0:
									countFilledWeightBinsSim+=1
									meanWeightTempSim+=HistSimHtPtWeight.GetBinContent(pttemp, httemp)
						if countFilledWeightBinsSim>3:
							weightGTGL=(float(meanWeightTempSim)/float(countFilledWeightBinsSim))
							countTestNewMeanWeightSim+=1
					HistSimBackgroundPredictionMet.Fill(event.met, weight*event.weight*weightGTGL)
					HistSimBackgroundMetNW.Fill(event.met, weight*event.weight)
					HistSimBackgroundPredictionHt.Fill(event.ht, weight*event.weight*weightGTGL)
					HistSimBackgroundHtNW.Fill(event.ht, weight*event.weight)
					if event.jetphotons[0].ptMJet==0.:
						HistSimBackgroundPredictionPhotonPt.Fill(event.jetphotons[0].pt, weight*event.weight*weightGTGL)
						HistSimBackgroundPhotonPtNW.Fill(event.jetphotons[0].pt, weight*event.weight)
					else:
						HistSimBackgroundPredictionPhotonPt.Fill(event.jetphotons[0].ptMJet, weight*event.weight*weightGTGL)
						HistSimBackgroundPhotonPtNW.Fill(event.jetphotons[0].ptMJet, weight*event.weight)
			if status=="data":
				HistDataGLMultiSignal.Fill(event.cleanjets.size())
				weightGTGL = HistDataHtPtWeight.GetBinContent(pt, ht)
				if weightGTGL ==0.:
					countMeanWeightData+=1
					weightGTGL=meanWeightData
					if event.jetphotons[0].ptMJet==0:
						HistDataHtPtWeightZeroEvents.Fill(event.jetphotons[0].pt, event.ht)
						MeanPtForMeanWeightEventsData+=event.jetphotons[0].pt
					else:
						MeanPtForMeanWeightEventsData+=event.jetphotons[0].ptMJet
						HistDataHtPtWeightZeroEvents.Fill(event.jetphotons[0].ptMJet, event.ht)
					MeanHtForMeanWeightEventsData+=event.ht
				HistDataBackgroundPredictionMet.Fill(event.met, weightGTGL)
				HistDataBackgroundPredictionHt.Fill(event.ht, weightGTGL)
				if event.jetphotons[0].ptMJet==0.:
					HistDataBackgroundPredictionPtStar.Fill(event.jetphotons[0].pt, weightGTGL)
				else:
					HistDataBackgroundPredictionPtStar.Fill(event.jetphotons[0].ptMJet, weightGTGL)
		if event.photons.size()>0 and UsePhoton==1:
			if status=="sim":
				HistSimGTMultiSignal.Fill(event.cleanjets.size(), weight*event.weight)
			if status=="data":
				HistDataGTMultiSignal.Fill(event.cleanjets.size(), weight*event.weight)
			if event.photons[0].ptMJet==0:
				if status=="sim":
					HistSimHtPtGTSignal.Fill(event.photons[0].pt, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGTSignal.Fill(event.photons[0].pt, event.ht)
			else:
				if status=="sim":
					HistSimHtPtGTSignal.Fill(event.photons[0].ptMJet, event.ht, weight*event.weight)
				if status=="data":
					HistDataHtPtGTSignal.Fill(event.photons[0].ptMJet, event.ht)
			if name == "QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
				HistSimBackgroundMet.Fill(event.met, weight*event.weight)
				HistSimBackgroundHt.Fill(event.ht, weight*event.weight)
				if event.photons[0].ptMJet==0:
					HistSimBackgroundPhotonPt.Fill(event.photons[0].pt, weight*event.weight)
				else:
					HistSimBackgroundPhotonPt.Fill(event.photons[0].ptMJet, weight*event.weight)

	print "******************************************************************"
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
print "calculate the ratios of Gt(control)/Gt(signal) and Gl(control)/Gl(signal) ratios should be equal"
print "Simulation: "+str(float(HistSimHtPtGT.Integral())/float(HistSimHtPtGTSignal.Integral()))+" and "+str(float(HistSimHtPtGL.Integral())/float(HistSimHtPtGLSignal.Integral()))
print "Data: "+str(float(HistDataHtPtGT.Integral())/float(HistDataHtPtGTSignal.Integral()))+" and "+str(float(HistDataHtPtGL.Integral())/float(HistDataHtPtGLSignal.Integral()))
TFileBackground.cd()

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
HistDataGTMulti.SetTitle("#gamma_{tight} in signal and controll region")
HistDataGTMulti.Draw()
HistDataGTMultiSignal.Draw("same")
LMultiGT.AddEntry(HistDataGTMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "f")
LMultiGT.AddEntry(HistDataGTMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGT.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGtControllAndSignal.pdf")

LMultiGL = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGLMulti.Integral())
HistDataGLMulti.Scale(norm)
norm = 1./float(HistDataGLMultiSignal.Integral())
HistDataGLMultiSignal.Scale(norm)
HistDataGLMulti.SetLineColor(2)
HistDataGLMulti.SetTitle("#gamma_{loose} in signal and controll region")
HistDataGLMulti.Draw()
HistDataGLMultiSignal.Draw("same")
LMultiGL.AddEntry(HistDataGLMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "f")
LMultiGL.AddEntry(HistDataGLMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGL.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGlControllAndSignal.pdf")

LMultiGLGTSignal = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGTMultiSignal.Integral())
HistDataGTMultiSignal.Scale(norm)
norm = 1./float(HistDataGLMultiSignal.Integral())
HistDataGLMultiSignal.Scale(norm)
HistDataGTMultiSignal.SetLineColor(2)
HistDataGTMultiSignal.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in signal region")
HistDataGTMultiSignal.Draw()
HistDataGLMultiSignal.Draw("same")
LMultiGLGTSignal.AddEntry(HistDataGTMultiSignal, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGLGTSignal.AddEntry(HistDataGLMultiSignal, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGLGTSignal.Draw()
ROOT.gPad.SaveAs(homePath+"Data/JetMultiGlGtSignal.pdf")

LMultiGLGTControl = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistDataGTMulti.Integral())
HistDataGTMulti.Scale(norm)
norm = 1./float(HistDataGLMulti.Integral())
HistDataGLMulti.Scale(norm)
HistDataGTMulti.SetLineColor(2)
HistDataGTMulti.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in control region")
HistDataGTMulti.Draw()
HistDataGLMulti.Draw("same")
LMultiGLGTControl.AddEntry(HistDataGTMulti, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}<100GeV", "f")
LMultiGLGTControl.AddEntry(HistDataGLMulti, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}<100GeV", "f")
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
HistDataBackgroundPredictionMet.Draw("Ehist")
HistSimBackgroundMet.Draw("samePEX0")
LMetData.AddEntry(HistDataBackgroundPredictionMet, "Predicion for #gamma_{tight} out of data", "f")
LMetData.AddEntry(HistSimBackgroundMet, "#gamma_{tight} QCD+GJets", "ep")
LMetData.Draw()
ROOT.gPad.SaveAs(homePath+"Data/ComparisonDataMet.pdf")
HistDataBackgroundPredictionMet.Write()
HistSimBackgroundMet.Write()

LHtData = ROOT.TLegend(.6,.75,.9,.9)
HistDataBackgroundPredictionHt.SetMarkerSize(0)
HistDataBackgroundPredictionHt.Draw("Ehist")
HistSimBackgroundHt.Draw("samePEX0")
LHtData.AddEntry(HistDataBackgroundPredictionHt, "Predicion for #gamma_{tight} out of data", "f")
LHtData.AddEntry(HistSimBackgroundHt, "#gamma_{tight} QCD+GJets", "ep")
LHtData.Draw()
ROOT.gPad.SaveAs(homePath+"Data/ComparisonDataHt.pdf")
HistDataBackgroundPredictionHt.Write()
HistSimBackgroundHt.Write()

LPtData = ROOT.TLegend(.6,.75,.9,.9)
HistDataBackgroundPredictionPtStar.SetMarkerSize(0)
HistDataBackgroundPredictionPtStar.Draw("Ehist")
HistSimBackgroundPhotonPt.Draw("samePEX0")
LPtData.AddEntry(HistDataBackgroundPredictionPtStar, "Predicion for #gamma_{tight} out of data", "f")
LPtData.AddEntry(HistSimBackgroundPhotonPt, "#gamma_{tight} QCD+GJets", "ep")
LPtData.Draw()
ROOT.gPad.SaveAs(homePath+"Data/ComparisonDataPt.pdf")
HistDataBackgroundPredictionPtStar.Write()
HistSimBackgroundPhotonPt.Write()

# SIM Plots

#comparison plots sim
Canvas1D.cd() # for 1D histos
LMet = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundMetNW.SetLineColor(2)
HistSimBackgroundMetNW.SetMarkerSize(0)
HistSimBackgroundPredictionMet.SetMarkerSize(0)
HistSimBackgroundPredictionMet.SetMinimum( 0.01 )
HistSimBackgroundPredictionMet.SetMaximum( 100000000 )
HistSimBackgroundMet.SetMinimum( 0.01 )
HistSimBackgroundMet.SetMaximum( 100000000 )
HistSimBackgroundMetNW.SetMinimum( 0.01 )
HistSimBackgroundMetNW.SetMaximum( 100000000 )
HistSimBackgroundPredictionMet.Draw("Ehist")
HistSimBackgroundMet.Draw("samePEX0")
HistSimBackgroundMetNW.Draw("sameEhist")
LMet.AddEntry(HistSimBackgroundPredictionMet, "Predicion for #gamma_{tight}", "f")
LMet.AddEntry(HistSimBackgroundMetNW, "#gamma_{loose}", "f")
LMet.AddEntry(HistSimBackgroundMet, "#gamma_{tight}", "ep")
LMet.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimMet.pdf")
HistSimBackgroundPredictionMet.Write()
HistSimBackgroundMet.Write()

LHt = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundHtNW.SetLineColor(2)
HistSimBackgroundHtNW.SetMarkerSize(0)
HistSimBackgroundPredictionHt.SetMarkerSize(0)
HistSimBackgroundPredictionHt.SetMinimum( 0.01 )
HistSimBackgroundPredictionHt.SetMaximum( 100000000 )
HistSimBackgroundHt.SetMinimum( 0.01 )
HistSimBackgroundHt.SetMaximum( 100000000 )
HistSimBackgroundHtNW.SetMinimum( 0.01 )
HistSimBackgroundHtNW.SetMaximum( 100000000 )
HistSimBackgroundPredictionHt.Draw("Ehist")
HistSimBackgroundHt.Draw("samePEX0")
HistSimBackgroundHtNW.Draw("sameEhist")
LHt.AddEntry(HistSimBackgroundPredictionHt, "Predicion for #gamma_{tight}", "f")
LHt.AddEntry(HistSimBackgroundHtNW, "#gamma_{loose}", "f")
LHt.AddEntry(HistSimBackgroundHt, "#gamma_{tight}", "ep")
LHt.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimHt.pdf")
HistSimBackgroundPredictionHt.Write()
HistSimBackgroundHt.Write()

LPhotonPt = ROOT.TLegend(.6,.75,.9,.9)
HistSimBackgroundPhotonPtNW.SetLineColor(2)
HistSimBackgroundPhotonPtNW.SetMarkerSize(0)
HistSimBackgroundPredictionPhotonPt.SetMarkerSize(0)
HistSimBackgroundPredictionPhotonPt.SetMinimum( 0.01 )
HistSimBackgroundPredictionPhotonPt.SetMaximum( 100000000 )
HistSimBackgroundPhotonPt.SetMinimum( 0.01 )
HistSimBackgroundPhotonPt.SetMaximum( 100000000 )
HistSimBackgroundPhotonPtNW.SetMinimum( 0.01 )
HistSimBackgroundPhotonPtNW.SetMaximum( 100000000 )
HistSimBackgroundPredictionPhotonPt.Draw("Ehist")
HistSimBackgroundPhotonPt.Draw("samePEX0")
HistSimBackgroundPhotonPtNW.Draw("sameEhist")
LPhotonPt.AddEntry(HistSimBackgroundPredictionPhotonPt, "Predicion for #gamma_{tight}", "f")
LPhotonPt.AddEntry(HistSimBackgroundPhotonPtNW, "#gamma_{loose}", "f")
LPhotonPt.AddEntry(HistSimBackgroundPhotonPt, "#gamma_{tight}", "ep")
LPhotonPt.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSimPt.pdf")
HistSimBackgroundPredictionPhotonPt.Write()
HistSimBackgroundPhotonPt.Write()


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
HistSimGTMulti.SetTitle("#gamma_{tight} in signal and controll region")
HistSimGTMulti.Draw()
HistSimGTMultiSignal.Draw("same")
LMultiGTSim.AddEntry(HistSimGTMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "f")
LMultiGTSim.AddEntry(HistSimGTMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGTSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGtControllAndSignal.pdf")

LMultiGLSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGLMulti.Integral())
HistSimGLMulti.Scale(norm)
norm = 1./float(HistSimGLMultiSignal.Integral())
HistSimGLMultiSignal.Scale(norm)
HistSimGLMulti.SetLineColor(2)
HistSimGLMulti.SetTitle("#gamma_{loose} in signal and controll region")
HistSimGLMulti.Draw()
HistSimGLMultiSignal.Draw("same")
LMultiGLSim.AddEntry(HistSimGLMulti, "normalized Jet multiplicity for E_{T}^{miss}<100GeV", "f")
LMultiGLSim.AddEntry(HistSimGLMultiSignal, "normalized Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGLSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGlControllAndSignal.pdf")

LMultiGLGTSignalSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGTMultiSignal.Integral())
HistSimGTMultiSignal.Scale(norm)
norm = 1./float(HistSimGLMultiSignal.Integral())
HistSimGLMultiSignal.Scale(norm)
HistSimGTMultiSignal.SetLineColor(2)
HistSimGTMultiSignal.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in signal region")
HistSimGTMultiSignal.Draw()
HistSimGLMultiSignal.Draw("same")
LMultiGLGTSignalSim.AddEntry(HistSimGTMultiSignal, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGLGTSignalSim.AddEntry(HistSimGLMultiSignal, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}>100GeV", "f")
LMultiGLGTSignalSim.Draw()
ROOT.gPad.SaveAs(homePath+"Sim/JetMultiGlGtSignal.pdf")

LMultiGLGTControlSim = ROOT.TLegend(.6,.75,.9,.9)
norm = 1./float(HistSimGTMulti.Integral())
HistSimGTMulti.Scale(norm)
norm = 1./float(HistSimGLMulti.Integral())
HistSimGLMulti.Scale(norm)
HistSimGTMulti.SetLineColor(2)
HistSimGLMulti.SetLineColor(1)
HistSimGTMulti.SetTitle("Jet Multi for #gamma_{loose} and #gamma_{tight} in control region")
HistSimGTMulti.Draw()
HistSimGLMulti.Draw("same")
LMultiGLGTControlSim.AddEntry(HistSimGTMulti, "normalized #gamma_{tight} Jet multiplicity for E_{T}^{miss}<100GeV", "f")
LMultiGLGTControlSim.AddEntry(HistSimGLMulti, "normalized #gamma_{loose} Jet multiplicity for E_{T}^{miss}<100GeV", "f")
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
