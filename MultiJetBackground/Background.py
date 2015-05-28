import ROOT
import sys
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
ROOT.TH1.SetDefaultSumw2()
e=2.7182818284590452353602874713526624977572470937


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

Styles.tdrStyle2D() # set style for 2D histos
#ROOT.gStyle.SetPalette(1)
Canvas1 = ROOT.TCanvas ("canvas1", "canvas1")

# possible Variables:
# Met Ht PhotonPt
plotvar="Met" # set plotvar
BreakFill = 0 # if set to 1 the loop will break after 10000 Entries
PrintMaps = 0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "#gamma_{tight}/#gamma_{loose}"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/06/"
IDVersion =".06_tree.root" #Version of the trees
homePath="~/plotting/MultiJetBackground/"


if len(sys.argv)>1:
	if len(sys.argv)==2:
		print "found argument: "+sys.argv[1]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt":
			plotvar=sys.argv[1]
			print "set plotvar = "+sys.argv[1]
	if len(sys.argv)==3:
		print "found arguments: "+sys.argv[1]+" and "+sys.argv[2]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt":
			plotvar=sys.argv[1]
			BreakFill=int(sys.argv[2])
			print "set plotvar = "+sys.argv[1]+" and BreakFill was set to "+sys.argv[2]
	elif:
		print "too many arguments!"




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




if plotvar == "PhotonPt":
	Title[1]="PhotonPt(GeV)"
	MinMax = [30,145,1900,0.01,1000000]
elif plotvar == "Met":
	Title[1]="E_{T}^{miss}(GeV)"
	MinMax = [15,0,800,0.01,1000000]
elif plotvar == "Ht":
	Title[1]="Ht(GeV)"
	MinMax = [25,0,1800,0.1,100000000]
else:
	print "no binning information!"



# maps used to mesure weight and define TFiles
# the order in which plots are stacked and generated is set in Names
# weight for data has to bet set to 1 later!
Names=["TTJets_V03", "TTGamma_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
N = {}
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':0.2571, 'WGamma_50_130_V03':1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':0.074, 'ZGamma_V02':123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204., 'PhotonA_V04':1.,  'SinglePhotonB_V04':1., 'SinglePhotonC_V04':1., 'PhotonParkedD_V10':1.}
Lsim = {}
FileList = {}


for name in Names:
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

nBinsHt = 50 # set number of Bins in Ht for 2D Plots
nBinsPt = 40 # set number of Bins in Pt for 2D Plots
PtMin = 100
PtMax = 800
HtMin = 0
HtMax = 1600

"""
									Histograms for Data
"""
#Hist for GT objects binned in Ht and PhotonPt*
HistDataHtPtGT = ROOT.TH2F( "dataHtPtGT", "dataHtPtGT", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtGT.SetTitle(Title[0]+" #gamma_{tight}")
HistDataHtPtGT.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGT.GetYaxis().SetTitle("Ht")

#Hist for GL objects binned in Ht and PhotonPt*
HistDataHtPtGL = ROOT.TH2F( "dataHtPtGL", "dataHtPtGL", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtGL.SetTitle(Title[0]+" #gamma_{loose}")
HistDataHtPtGL.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtGL.GetYaxis().SetTitle("Ht")

#Hist for weight binned like HistDataHtPtGT and HistDataHtPtGL. Weight is GT/GL in every bin
HistDataHtPtWeight = ROOT.TH2F( "dataHtPtWeight", "dataHtPtWeight", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistDataHtPtWeight.GetXaxis().SetTitle("P_{T}*")
HistDataHtPtWeight.GetYaxis().SetTitle("Ht")
HistDataHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose}")

#for 
HistIsoGT = ROOT.TH2F( "IsoGT", "IsoGT", 100, 0, 30, 100, 0, 40)
HistIsoGT.SetTitle(Title[0]+" #gamma_{tight}")
HistIsoGT.GetXaxis().SetTitle("I_{#pm}")
HistIsoGT.GetYaxis().SetTitle("I_{0}")

HistIsoGL = ROOT.TH2F( "IsoGL", "IsoGL", 100, 0, 30, 100, 0, 40)
HistIsoGL.SetTitle(Title[0]+" #gamma_{loose}")
HistIsoGL.GetXaxis().SetTitle("I_{#pm}")
HistIsoGL.GetYaxis().SetTitle("I_{0}")


HistDataPrediction = ROOT.TH1F( "DataPrediction", "DataPrediction", 30, 0, 900 )
HistDataPrediction.SetTitle(Title[0])
HistDataPrediction.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistDataPrediction.GetYaxis().SetTitle("Events")

HistDataGTGL = ROOT.TH1F( "data", "data", 10, 0, 100 )

GTData = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
GLData = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]

"""
								Histograms for simulation
"""


#hist for GT binned in pt ht with weights
HistSimHtPtGT = ROOT.TH2F( "SimHtPtGT", "SimHtPtGT", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGT.SetTitle(Title[0]+" #gamma_{tight} simulated data")
HistSimHtPtGT.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGT.GetYaxis().SetTitle("Ht")

#hist for GL binned in pt ht with weights
HistSimHtPtGL = ROOT.TH2F( "SimHtPtGL", "SimHtPtGL", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGL.SetTitle(Title[0]+" #gamma_{loose} simulated data")
HistSimHtPtGL.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGL.GetYaxis().SetTitle("Ht")

HistSimHtPtWeight = ROOT.TH2F( "simHtPtWeight", "simHtPtWeight", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtWeight.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeight.GetYaxis().SetTitle("Ht")
HistSimHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose} simulated data")

HistSimHtPtWeightError = ROOT.TH2F( "simHtPtWeightError", "simHtPtWeightError", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtWeightError.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtWeightError.GetYaxis().SetTitle("Ht")
HistSimHtPtWeightError.SetTitle(Title[0]+" #sigma_{w} (stat) ")

HistSimIsoGT = ROOT.TH2F( "simIsoGT", "simIsoGT", 100, 0, 30, 100, 0, 40)
HistSimIsoGT.SetTitle(Title[0]+" #gamma_{tight} simulated data")
HistSimIsoGT.GetXaxis().SetTitle("I_{0}")
HistSimIsoGT.GetYaxis().SetTitle("I_{#pm}")

HistSimIsoGL = ROOT.TH2F( "simIsoGL", "simIsoGL", 100, 0, 30, 100, 0, 40)
HistSimIsoGL.SetTitle(Title[0]+" #gamma_{loose} simulated data")
HistSimIsoGL.GetXaxis().SetTitle("I_{0}")
HistSimIsoGL.GetYaxis().SetTitle("I_{#pm}")

#hist for GT binned in pt ht no weights (to calculate sigma(stat))
HistSimHtPtGTNoWeights = ROOT.TH2F( "SimHtPtGTNoWeights", "SimHtPtGTNoWeights", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGTNoWeights.SetTitle(Title[0]+" #gamma_{tight} simulated data (no weights applied)")
HistSimHtPtGTNoWeights.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGTNoWeights.GetYaxis().SetTitle("Ht")

#hist for GL binned in pt ht no weights (to calculate sigma(stat))
HistSimHtPtGLNoWeights = ROOT.TH2F( "SimHtPtGLNoWeights", "SimHtPtGLNoWeights", nBinsPt, PtMin, PtMax, nBinsHt, HtMin, HtMax)
HistSimHtPtGLNoWeights.SetTitle(Title[0]+" #gamma_{loose} simulated data (no weights applied)")
HistSimHtPtGLNoWeights.GetXaxis().SetTitle("P_{T}*")
HistSimHtPtGLNoWeights.GetYaxis().SetTitle("Ht")

HistSimBackgroundPrediction = ROOT.TH1F( "SimBackgroundPrediction", "SimBackgroundPrediction", 30, 0, 900)
HistSimBackgroundPrediction.SetTitle(Title[0])
HistSimBackgroundPrediction.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackgroundPrediction.GetYaxis().SetTitle("Events")

HistSimBackground = ROOT.TH1F( "SimBackground", "SimBackground", 30, 0, 900)
HistSimBackground.SetTitle(Title[0])
HistSimBackground.GetXaxis().SetTitle("E_{T}^{miss}(GeV)")
HistSimBackground.GetYaxis().SetTitle("Events")

HistSimGTGL = ROOT.TH1F( "Sim", "Sim", 10, 0, 100 )


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
	for event in tree:
		if status=="data" and event.weight!=1:
			print "data found with event.weight!=1 change program (wrong weights for data)"
		if BreakFill:
			stop+=1
			if stop==10000:
				break
		if event.met > 100:
			continue # filter for controll region
		GtCount=0 # reset number of GT and GL in the event
		GlCount=0
		if event.photons.size()>0:
			GtCount=1

		if event.jetphotons.size()>0:
			GlCount=1
		
		if event.met < 10:
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
		elif event.met < 100:
			GT[9] += weight*event.weight*GtCount
			GL[9] += weight*event.weight*GlCount
		if event.photons.size()>0:
			if event.photons[0].ptMJet==0:
				HistSimHtPtGT.Fill(event.photons[0].pt, event.ht, weight*event.weight)
				HistSimHtPtGTNoWeights.Fill(event.photons[0].pt, event.ht)
			else:
				HistSimHtPtGT.Fill(event.photons[0].ptMJet, event.ht, weight*event.weight)
				HistSimHtPtGTNoWeights.Fill(event.photons[0].ptMJet, event.ht)
			HistSimIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso, weight*event.weight )
			
		if event.jetphotons.size()>0:
			if event.jetphotons[0].ptMJet==0:
				HistSimHtPtGL.Fill(event.jetphotons[0].pt, event.ht, weight*event.weight)
				HistSimHtPtGLNoWeights.Fill(event.jetphotons[0].pt, event.ht)
			else:
				HistSimHtPtGL.Fill(event.jetphotons[0].ptMJet, event.ht, weight*event.weight)	
				HistSimHtPtGLNoWeights.Fill(event.jetphotons[0].ptMJet, event.ht)			
			HistSimIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso, weight*event.weight )

	print "******************************************************************"








stop = 0
for event in data:
	if BreakFill:
		stop += 1
		if stop ==100:
			break
	if event.met > 100:
		continue
	GtCount=0
	GlCount=0
	if event.photons.size()>0:
		GtCount=1

	if event.jetphotons.size()>0:
		GlCount=1

	if event.met < 10:
		GT[0] += GtCount
		GL[0] += GlCount
	elif event.met < 20:
		GT[1] += GtCount
		GL[1] += GlCount
	elif event.met < 30:
		GT[2] += GtCount
		GL[2] += GlCount
	elif event.met < 40:
		GT[3] += GtCount
		GL[3] += GlCount
	elif event.met < 50:
		GT[4] += GtCount
		GL[4] += GlCount
	elif event.met < 60:
		GT[5] += GtCount
		GL[5] += GlCount
	elif event.met < 70:
		GT[6] += GtCount
		GL[6] += GlCount
	elif event.met < 80:
		GT[7] += GtCount
		GL[7] += GlCount
	elif event.met < 90:
		GT[8] += GtCount
		GL[8] += GlCount
	elif event.met < 100:
		GT[9] += GtCount
		GL[9] += GlCount
	if event.photons.size()>0:
		if event.photons[0].ptMJet==0:
			HistDataHtPtGT.Fill(event.photons[0].pt, event.ht)
		else:
			HistDataHtPtGT.Fill(event.photons[0].ptMJet, event.ht)			
		HistIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso)
	if event.jetphotons.size()>0:
		if event.jetphotons[0].ptMJet==0:
			HistDataHtPtGL.Fill(event.jetphotons[0].pt, event.ht)
		else:
			HistDataHtPtGL.Fill(event.jetphotons[0].ptMJet, event.ht)		
		HistIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso)

		
print "******************** finished looping data ***********************"
print "******************************************************************"

BinsCount=0		
count=0
print "****************** setting 2D-Bincontents ************************"
for ht in range(0, nBinsHt):
	for pt in range(0, nBinsPt):
		BinsCount+=1
		GLBin = HistDataHtPtGL.GetBinContent(pt, ht)
		GTBin = HistDataHtPtGT.GetBinContent(pt, ht)
		GTBin = float(GTBin)
		if GLBin ==0:
			HistDataHtPtWeight.SetBinContent(pt, ht, 0)
			count+=1
		else:
			HistDataHtPtWeight.SetBinContent(pt, ht, GTBin/GLBin)
		"""
		if HistDataHtPtWeight.GetBinContent(pt, ht)>50:
			print "Bin Nr. "+str(pt)+"/"+str(ht)+" hat wert: "+str(HistDataHtPtWeight.GetBinContent(pt, ht))+" bei GL = "+str(GLBin)+" und GT = "+str(GTBin)+" Bin set zu 1 "
			HistDataHtPtWeight.SetBinContent(pt, ht, 1)
		"""
print str(count)+" out of "+str(nBinsHt*nBinsPt)+" Bins had to be set to zero because GLBin was empty"
print str(BinsCount)+" Bins were looped over"
print "*************** finished setting Bincontents *********************"
print "******************************************************************"
print "***************** filling comparison Plots ***********************"

stop=0
for event in data:
	if BreakFill:
		stop += 1
		if stop ==100:
			break
	if event.met < 100:
		continue
	if event.jetphotons.size()==0:
		continue
	if event.jetphotons[0].ptMJet==0:
		pt, nothing = divmod(event.jetphotons[0].pt, ((PtMax-PtMin)/nBinsPt))
	else:
		pt, nothing = divmod(event.jetphotons[0].ptMJet, ((PtMax-PtMin)/nBinsPt))
	ht, nothing = divmod(event.ht, ((HtMax-HtMin)/nBinsHt))
	pt = int(pt)
	ht = int(ht)	
	weightGTGL = HistDataHtPtWeight.GetBinContent(pt, ht)
	HistDataPrediction.Fill(event.met, weightGTGL)




print "******************************************************************"

TFileBackground.cd()

HistDataHtPtGL.Draw("colz")
HistDataHtPtGL.Write()
ROOT.gPad.SaveAs(homePath+"Data/GLHtPtData.pdf")

HistDataHtPtGT.Draw("colz")
HistDataHtPtGT.Write()
ROOT.gPad.SaveAs(homePath+"Data/GTHtPtData.pdf")

ROOT.gStyle.SetOptLogz(0)
HistDataHtPtWeight.SetMaximum(5)
Canvas2 = ROOT.TCanvas ("canvas2", "canvas2")
HistDataHtPtWeight.Draw("colz")
HistDataHtPtWeight.Write()
ROOT.gPad.SaveAs(homePath+"Data/GtGlRatioHtPtData.pdf")
Styles.tdrStyle2D()
Canvas1.cd()

HistIsoGT.Draw("colz")
HistIsoGT.Write()
ROOT.gPad.SaveAs(homePath+"Data/GTIsoData.pdf")

HistIsoGL.Draw("colz")
HistIsoGL.Write()
ROOT.gPad.SaveAs(homePath+"Data/GLIsoData.pdf")

print "******************************************************************"
print GT
print GL
i =0
for i,g in enumerate(GT):
	if GL[i] == 0:
		GL[i]=1
		print "no loose photon in met bin!! set 0 to 1 INVALID PLOTS!"
	weight = GT[i]/GL[i]
	print str(weight)+" bei i= "+str(i)
	HistDataGTGL.Fill(5+i*10, weight)
	HistDataGTGL.SetBinError(i+1, 0.000001)
	GL[i]=0.
	GT[i]=0.

HistDataGTGL.SetTitle(Title[0])
HistDataGTGL.GetXaxis().SetTitle(Title[1])
HistDataGTGL.GetYaxis().SetTitle(Title[2])
HistDataGTGL.GetXaxis().SetTitleOffset(1)
HistDataGTGL.GetYaxis().SetTitleOffset(1.2)

HistDataGTGL.Draw("PE")
ROOT.gPad.SaveAs(homePath+"Data/GtGlRatioMetData.pdf")

print "*********************** simulated data ***************************"







count=0
print "****************** setting 2D-Bincontents ************************"
for ht in range(0, nBinsHt):
	for pt in range(0, nBinsPt):
		GLBin = HistSimHtPtGL.GetBinContent(pt, ht)
		GTBin = HistSimHtPtGT.GetBinContent(pt, ht)
		GTBin = float(GTBin)
		if GLBin ==0.:
			HistSimHtPtWeight.SetBinContent(pt, ht, 0.)
			count+=1
		else:
			HistSimHtPtWeight.SetBinContent(pt, ht, GTBin/GLBin)
			HistSimHtPtWeightError.SetBinContent(pt, ht, HistSimHtPtWeight.GetBinError(pt, ht))
		"""
		if HistSimHtPtWeight.GetBinContent(pt, ht)>50:
			print "Bin Nr. "+str(pt)+"/"+str(ht)+" hat wert: "+str(HistSimHtPtWeight.GetBinContent(pt, ht))+" bei GL = "+str(GLBin)+" und GT = "+str(GTBin)+" Bin set zu 1 "
			HistSimHtPtWeight.SetBinContent(pt, ht, 1)
		"""
print str(count)+" out of "+str(nBinsHt*nBinsPt)+" Bins had to be set to zero because GLBin was empty"
print "*************** finished setting Bincontents *********************"


for name in Names:
	print "******************************************************************"
	stop=0
	if name == "ZGammaNuNu_V03":
		print "skipping ZGammaNuNu"
		print "******************************************************************"
		continue
	if name =="PhotonA_V04" or name =="SinglePhotonB_V04" or name =="SinglePhotonC_V04" or name =="PhotonParkedD_V10":
		print "skipping real Data"
		print "******************************************************************"
		continue # filter for simulated data
	if name=="QCD_250_500_V03" or name=="QCD_100_250_V09" or name=="QCD_500_1000_V03" or name=="QCD_1000_inf_V03" or name=="GJets_100_200_V09" or name=="GJets_200_400_V03" or name=="GJets_400_inf_V03" or name=="GJets_40_100_V09":
		print "looping over: "+path+name+IDVersion
		tree = FileList[name].Get("myTree")#Inputtree
		weight = Lint/Lsim[name]
		print "weight is "+str(weight)
		for event in tree:
#			if event.met<100:
#				continue
			if event.jetphotons.size()>0:
				if event.jetphotons[0].ptMJet==0:
					pt, nothing = divmod(event.jetphotons[0].pt, ((PtMax-PtMin)/nBinsPt))
				else:
					pt, nothing = divmod(event.jetphotons[0].ptMJet, ((PtMax-PtMin)/nBinsPt))
				ht, nothing = divmod(event.ht, ((HtMax-HtMin)/nBinsHt))
				pt = int(pt)
				ht = int(ht)
			
				weightGTGL = HistSimHtPtWeight.GetBinContent(pt, ht)
				HistSimBackgroundPrediction.Fill(event.met, weight*event.weight*weightGTGL)
			if event.photons.size()>0:
				HistSimBackground.Fill(event.met, weight*event.weight)
TFileBackground.cd()
Canvas1D.cd()
HistSimBackgroundPrediction.SetMinimum( 0.01 )
HistSimBackgroundPrediction.SetMaximum( 100000000 )
HistSimBackground.SetMinimum( 0.01 )
HistSimBackground.SetMaximum( 100000000)
HistSimBackgroundPrediction.Draw("Ehist")
HistSimBackground.Draw("samePEX0")
ROOT.gPad.SaveAs(homePath+"Sim/"+"ComparisonSim.pdf")
HistSimBackgroundPrediction.Write()
HistSimBackground.Write()
Canvas1.cd()

HistSimHtPtGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLHtPtSim.pdf")
HistSimHtPtGL.Write()

HistSimHtPtGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTHtPtSim.pdf")
HistSimHtPtGT.Write()

Canvas2.cd()
HistSimHtPtWeightError.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioErrorHtPtSim.pdf")
HistSimHtPtWeightError.Write()

HistSimHtPtWeight.SetMaximum(5)
HistSimHtPtWeight.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioHtPtSim.pdf")
HistSimHtPtWeight.Write()
Canvas1.cd()

HistSimIsoGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTIsoSim.pdf")
HistSimIsoGT.Write()

HistSimIsoGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLIsoSim.pdf")
HistSimIsoGL.Write()


print GT
print GL
i =0
for i,g in enumerate(GT):
	if GL[i] == 0:
		GL[i]=1
		print "no loose photon in met bin!! set 0 to 1 INVALID PLOTS!"
	weight = GT[i]/GL[i]
	print str(weight)+" bei i= "+str(i)
	HistSimGTGL.Fill(5+i*10, weight)
	HistSimGTGL.SetBinError(i+1, 0.000001)
	GL[i]=0
	GT[i]=0


HistSimGTGL.SetTitle(Title[0])
HistSimGTGL.GetXaxis().SetTitle(Title[1])
HistSimGTGL.GetYaxis().SetTitle(Title[2])
HistSimGTGL.GetXaxis().SetTitleOffset(1)
HistSimGTGL.GetYaxis().SetTitleOffset(1.2)

HistSimGTGL.Draw("PE")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioMetSim.pdf")
HistSimGTGL.Write()
