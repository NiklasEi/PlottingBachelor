import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
ROOT.TH1.SetDefaultSumw2()
e=2.7182818284590452353602874713526624977572470937

simulated = ROOT.TChain("myTree")
data = ROOT.TChain("myTree")

# possible Variables:
# Met Ht PhotonPt
plotvar="Met" # set plotvar
LoopData = 0 # if set to 1 program will loop over simulation AND Data
BreakFill = 1 # if set to 1 the loop will break after 10000 Entries
PrintMaps = 0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "Events"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/V05/"

print "Programm is:"
if LoopData:
	"looping over real data"
else:
	"not looping over real data"
if BreakFill:
	"breaking loops after 10000 entries"
else:
	"not breaking loops after 10000 entries"
if PrintMaps:
	"printing maps with names, files, entries ..."
else:
	"not printing maps"




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


IDVersion =".05_tree.root" #Version of the trees

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

# Data Trees are added to a chain and then looped over in one loop
weight=1#set weight=1 for real data
#Data

for name in Names:
	if name =="PhotonA_V04" or name =="SinglePhotonB_V04" or name =="SinglePhotonC_V04" or name =="PhotonParkedD_V10":
		# filter data names
		print "******************************************************************"
		data.Add(path+name+IDVersion+"/myTree")#Add Trees to TChain
		print "Added "+name+IDVersion+"/myTree  to chain"

print "******************************************************************"

HistData = ROOT.TH1F( "data", "data", MinMax[0], MinMax[1], MinMax[2] ) #				Hist for real data
HistFakeData = ROOT.TH1F( "fakes", "fakes", MinMax[0], MinMax[1], MinMax[2] )# 			Hist for fakes from data

HistSimData = ROOT.TH1F( "simData", "simData", MinMax[0], MinMax[1], MinMax[2] ) #		Hist for simulated data
HistSimGen = ROOT.TH1F( "simulated", "simulated", MinMax[0], MinMax[1], MinMax[2] )#	Hist for REAL fakes (matched genElectron) from simData
HistSimFake = ROOT.TH1F( "simFake", "simFake", MinMax[0], MinMax[1], MinMax[2] )#		Hist for fakes from simulation with the weight method
if LoopData:
	print "********************      datachain     **************************"
	eweight=0. # weight for elektrons faking photons
	stop=0
	for event in data: # loop over datachain
		if stop==10000 and BreakFill:
			break
		stop+=1
		if event.photons.size()>0:
			if plotvar=="PhotonPt":
				HistData.Fill( event.photons[0].pt, weight )
			elif plotvar=="Ht":
				HistData.Fill( event.ht, weight )
			elif plotvar=="Met":
				HistData.Fill( event.met, weight )
		if event.electrons.size()>0:
			eweight = (1.-(1.-0.00194)*(1.-pow((event.electrons[0].pt/14.1)+1.,-4.9))*(1.-0.14*pow(e,(-0.296*event.nTracksPV)))*(1.-0.000315*event.nVertex))
			if plotvar=="PhotonPt":
				HistFakeData.Fill( event.electrons[0].pt, eweight )
			elif plotvar=="Ht":
				HistFakeData.Fill( event.ht, eweight )
			elif plotvar=="Met":
				HistFakeData.Fill( event.met, eweight )
	print "******************************************************************"
	print "looped over real data"
else:
	print "don't loop over real data"
HistoTTJetsGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoTTGammaGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoWJetsGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoWGammaGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoZGammaGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoQCDGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoGJetsGen = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )

HistoTTJetsFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoTTGammaFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoWJetsFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoWGammaFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoZGammaFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoQCDFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )
HistoGJetsFake = ROOT.TH1F( "", "", MinMax[0], MinMax[1], MinMax[2] )


print "******************************************************************"		
print "**********************    simulation    **************************"
stop=0
for name in Names: # loop over names
	if name == "ZGammaNuNu_V03":
		print "skipping ZGammaNuNu"
		continue
	print "******************************************************************"
	if name =="PhotonA_V04" or name =="SinglePhotonB_V04" or name =="SinglePhotonC_V04" or name =="PhotonParkedD_V10":
		print "skipping real Data"
		print "******************************************************************"
		continue # filter simulated data
	print "looping over: "+path+name+IDVersion

	if name == "TTJets_V03":
		HistSimGenTemp = HistoTTJetsGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoTTJetsFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoTTJetsGen and HistoTTJetsFake"
	if name == "TTGamma_V03":
		HistSimGenTemp = HistoTTGammaGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoTTGammaFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoTTGammaGen and HistoTTGammaFake"
	if name == "WGamma_130_inf_V03" or name == "WGamma_50_130_V03":
		HistSimGenTemp = HistoWGammaGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoWGammaFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoWGammaGen and HistoWGammaFake"
	if name == "WJets_250_300_V03" or name == "WJets_300_400_V03" or name == "WJets_400_inf_V03":
		HistSimGenTemp = HistoWJetsGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoWJetsFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoWJetsGen and HistoWJetsFake"
	if name == "ZGamma_V02":
		HistSimGenTemp = HistoZGammaGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoZGammaFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoZGammaGen and HistoZGammaFake"
	if name == "QCD_250_500_V03" or name == "QCD_100_250_V09" or name == "QCD_500_1000_V03" or name == "QCD_1000_inf_V03":
		HistSimGenTemp = HistoQCDGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoQCDFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoQCDGen and HistoQCDFake"
	if name == "GJets_100_200_V09" or name == "GJets_200_400_V03" or name == "GJets_400_inf_V03" or name == "GJets_40_100_V09":
		HistSimGenTemp = HistoGJetsGen.Clone( "HistSimGenTemp" )
		HistSimFakeTemp = HistoGJetsFake.Clone( "HistSimFakeTemp" )
		print "filling in clone of HistoGJetsGen and HistoGJetsFake"

	tree = FileList[name].Get("myTree")#Inputtree
	weight = Lint/Lsim[name]
	print "weight is "+str(weight)
	for event in tree:
		if stop==10000 and BreakFill:
			break
		stop+=1
		if event.photons.size()>0:
			if plotvar=="PhotonPt":
				HistSimData.Fill( event.photons[0].pt, weight*event.weight )
			elif plotvar=="Ht":
				HistSimData.Fill( event.ht, weight*event.weight )
			elif plotvar=="Met":
				HistSimData.Fill( event.met, weight*event.weight )
			if event.photons[0].genElectron:
				if plotvar=="PhotonPt":
					HistSimGen.Fill( event.photons[0].pt, weight*event.weight )
					HistSimGenTemp.Fill( event.photons[0].pt, weight*event.weight )
				elif plotvar=="Ht":
					HistSimGen.Fill( event.ht, weight*event.weight )
					HistSimGenTemp.Fill( event.ht, weight*event.weight )
				elif plotvar=="Met":
					HistSimGen.Fill( event.met, weight*event.weight )
					HistSimGenTemp.Fill( event.met, weight*event.weight )
		if event.electrons.size()>0:
			eweight = 1 - (1 - 0.00623) * (1 - pow(event.electrons[0].pt / 4.2 + 1,-2.9)) * (1 - 0.29 * pow(e,-0.335 * event.nTracksPV)) * (1 - 0.000223 * event.nVertex)
			if plotvar=="PhotonPt":
				HistSimFake.Fill( event.electrons[0].pt, eweight*event.weight )
				HistSimFakeTemp.Fill( event.electrons[0].pt, eweight*event.weight*weight )
			elif plotvar=="Ht":
				HistSimFake.Fill( event.ht, eweight*event.weight*weight )
				HistSimFakeTemp.Fill( event.ht, eweight*event.weight*weight )
			elif plotvar=="Met":
				HistSimFake.Fill( event.met, eweight*event.weight*weight )
				HistSimFakeTemp.Fill( event.met, eweight*event.weight*weight )

	if name == "TTJets_V03":
		HistoTTJetsGen = HistSimGenTemp.Clone( "HistoTTJetsGen" )
		HistoTTJetsFake = HistSimFakeTemp.Clone( "HistoTTJetsFake" )
	if name == "TTGamma_V03":
		HistoTTGammaGen = HistSimGenTemp.Clone( "HistoTTGammaGen" )
		HistoTTGammaFake = HistSimFakeTemp.Clone( "HistoTTGammaFake" )
	if name == "WGamma_130_inf_V03" or name == "WGamma_50_130_V03":
		HistoWGammaGen = HistSimGenTemp.Clone( "HistoWGammaGen" )
		HistoWGammaFake = HistSimFakeTemp.Clone( "HistoWGammaFake" )
	if name == "WJets_250_300_V03" or name == "WJets_300_400_V03" or name == "WJets_400_inf_V03":
		HistoWJetsGen = HistSimGenTemp.Clone( "HistoWJetsGen" )
		HistoWJetsFake = HistSimFakeTemp.Clone( "HistoWJetsFake" )
	if name == "ZGamma_V02":
		HistoZGammaGen = HistSimGenTemp.Clone( "HistoZGammaGen" )
		HistoZGammaFake = HistSimFakeTemp.Clone( "HistoZGammaFake" )
	if name == "QCD_250_500_V03" or name == "QCD_100_250_V09" or name == "QCD_500_1000_V03" or name == "QCD_1000_inf_V03":
		HistoQCDGen = HistSimGenTemp.Clone( "HistoQCDGen" )
		HistoQCDFake = HistSimFakeTemp.Clone( "HistoQCDFake" )
	if name == "GJets_100_200_V09" or name == "GJets_200_400_V03" or name == "GJets_400_inf_V03" or name == "GJets_40_100_V09":
		HistoGJetsGen = HistSimGenTemp.Clone( "HistoGJetsGen" )
		HistoGJetsFake = HistSimFakeTemp.Clone( "HistoGJetsFake" )

	print "******************************************************************"

Histos = [[HistoTTJetsGen, HistoTTJetsFake], [HistoTTGammaGen, HistoTTGammaFake], [HistoWJetsGen, HistoWJetsFake], [HistoWGammaGen, HistoWGammaFake], [HistoZGammaGen, HistoZGammaFake], [HistoQCDGen, HistoQCDFake], [HistoGJetsGen, HistoGJetsFake]]
#Fake = [HistoTTJetsFake, HistoTTGammaFake, HistoWJetsFake, HistoWGammaFake, HistoZGammaFake, HistoQCDFake, HistoGJetsFake]


for i,hist in enumerate(Histos):
	if i==0:
		TempTitle="TTJets"
	if i==1:
		TempTitle="TTGamma"
	if i==2:
		TempTitle="WJets"
	if i==3:
		TempTitle="WGamma"
	if i==4:
		TempTitle="ZGamma"
	if i==5:
		TempTitle="Multijet"
	if i==6:
		TempTitle="GJets"

	print TempTitle+" "+str(hist[0])+" und "+str(hist[1])

	hist[1].SetLineColor(2)
	hist[1].SetLineWidth(1)
	hist[0].SetLineWidth(1)
	hist[1].SetMarkerSize(0)
	hist[1].SetTitle(Title[0]+" "+TempTitle)
	hist[1].GetXaxis().SetTitle(Title[1])
	hist[1].GetYaxis().SetTitle(Title[2])
	hist[1].GetXaxis().SetTitleOffset(1)
	hist[1].GetYaxis().SetTitleOffset(1)

	TempClone = hist[1].Clone("TempClone")
	for i in range(0, MinMax[0]):
		TempClone.SetBinError(i,0.11*TempClone.GetBinContent(i))

	TempClone.SetFillColor(4)
	TempClone.SetLineColor(4)
	TempClone.SetFillStyle(3004)

	hist[1].Draw("Ehist")
	hist[0].Draw("samePEX0")
	TempClone.Draw("sameE2")


	LTemp = ROOT.TLegend(.6,.75,.9,.9)
	LTemp.AddEntry(hist[0], "Direct simulation", "ep")
	LTemp.AddEntry(hist[1], "Prediction", "f")	
	LTemp.AddEntry(TempClone, "systematic Error", "f")
	LTemp.Draw()

	ROOT.gPad.Update()
	ROOT.gPad.RedrawAxis()
	ROOT.gPad.SaveAs(TempTitle+"EFakes.pdf")	



HistSimFake.SetLineColor(2)
HistSimFake.SetLineWidth(1)
HistSimFake.SetMarkerSize(0)

HistSimFakeClone = HistSimFake.Clone("HistSimFakeClone")
for i in range(0, MinMax[0]):
	HistSimFakeClone.SetBinError(i,0.11*HistSimFakeClone.GetBinContent(i))

HistSimFake.SetTitle(Title[0])
HistSimFake.GetXaxis().SetTitle(Title[1])
HistSimFake.GetYaxis().SetTitle(Title[2])
HistSimFake.GetXaxis().SetTitleOffset(1)
HistSimFake.GetYaxis().SetTitleOffset(1)

L.AddEntry(HistSimGen, "Direct simulation", "ep")
L.AddEntry(HistSimFake, "Prediction", "f")
L.AddEntry(HistSimFakeClone, "systematic Error", "f")

HistSimFakeClone.SetFillColor(4)
HistSimFakeClone.SetLineColor(4)
HistSimFakeClone.SetFillStyle(3004)

HistSimGen.SetLineWidth(1)

HistSimFake.Draw("Ehist")
HistSimFakeClone.Draw("sameE2")
HistSimFakeClone.Draw("same")
HistSimGen.Draw("samePEX0")
L.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
ROOT.gPad.SaveAs("EFakes.pdf")

