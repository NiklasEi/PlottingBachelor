import ROOT
import sys
from treeFunctions import *
from SignalScan import isSignal
ROOT.gSystem.Load("libTreeObjects.so")
ROOT.TH1.SetDefaultSumw2()
e=2.7182818284590452353602874713526624977572470937

"""
to estimate photonfakes comming from electrons, a formula is used f = f(nVertex, nTracksPV, electron.pt)
to varify the method it is used on simulated data
"""

data = ROOT.TChain("myTree") # chain for data


# possible Variables:
# Met Ht PhotonPt
plotvar="PhotonPt" # set plotvar
LoopData = 0 # if set to 1 program will loop over simulation AND Data
BreakFill = 0 # if set to 1 the loop will break after 10000 Entries
PrintMaps = 0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "Events"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/10/"
IDVersion =".10_tree.root" #Version of the trees
homePath="~/plotting/Elektrons/"



if len(sys.argv)>1:
	if len(sys.argv)==2:
		print "found argument: "+sys.argv[1]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt":
			plotvar=sys.argv[1]
			print "set plotvar = "+sys.argv[1]
			sys.exit("need an argument for creating the TFile!")
	if len(sys.argv)==3:
		print "found arguments: "+sys.argv[1]+" and "+sys.argv[2]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt":
			plotvar=sys.argv[1]
			BreakFill=int(sys.argv[2])
			print "set plotvar = "+sys.argv[1]+" and BreakFill was set to "+sys.argv[2]
			sys.exit("need an argument for creating the TFile!")
	if len(sys.argv)==4:
		print "found arguments: "+sys.argv[1]+" and "+sys.argv[2]+" and "+sys.argv[3]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt":
			plotvar=sys.argv[1]
			BreakFill=int(sys.argv[2])
			print "creating TFile with "+sys.argv[3]
			print "set plotvar = "+sys.argv[1]+" and BreakFill was set to "+sys.argv[2]
else:
	sys.exit("need an argument for creating the TFile!")
		

if sys.argv[3]=="recreate":
	TFileEfake = ROOT.TFile(homePath+"TFileEfake.root", "recreate") # TFile to save histos
elif sys.argv[3]=="update":
	TFileEfake = ROOT.TFile(homePath+"TFileEfake.root", "update") # TFile to save histos
else:
	sys.exit("need a valid argument for creating the TFile!")

print "plotting against "+plotvar
print "Programm is:"
if LoopData:
	print "looping over real data"
else:
	print "not looping over real data"
if BreakFill:
	print "breaking loops after 10000 entries"
else:
	print "not breaking loops after 10000 entries"
if PrintMaps:
	print "printing maps with names, files, entries ..."
else:
	print "not printing maps"




if plotvar == "PhotonPt":
	Title[1]="PhotonPt(GeV)"
	MinMax = [30,145,1900,0.01,1000000]
elif plotvar == "Met":
	Title[1]="E_{T}^{miss}(GeV)"
	MinMax = [18,0,900,0.01,1000000]
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
	print "weight is "+str(weight)
	for event in data: # loop over datachain
		if stop==10000 and BreakFill:
			print "breaking loop..."
			break
		stop+=1
		if isSignal(event)=="GT":
			if plotvar=="PhotonPt":
				HistData.Fill( event.photons[0].pt, weight )
			elif plotvar=="Ht":
				HistData.Fill( event.ht, weight )
			elif plotvar=="Met":
				HistData.Fill( event.met, weight )
		elif isSignal(event)=="e":
			eweight = (1.-(1.-0.00194)*(1.-pow((event.electrons[0].pt/14.1)+1.,-4.9))*(1.-0.14*pow(e,(-0.296*event.nTracksPV)))*(1.-0.000315*event.nVertex))
			if plotvar=="PhotonPt":
				HistFakeData.Fill( event.electrons[0].pt, eweight )
			elif plotvar=="Ht":
				HistFakeData.Fill( event.ht, eweight )
			elif plotvar=="Met":
				HistFakeData.Fill( event.met, eweight )
		elif isSignal( event )!="GL":
			print isSignal( event )
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



Histos = [[HistoTTJetsGen, HistoTTJetsFake], [HistoTTGammaGen, HistoTTGammaFake], [HistoWJetsGen, HistoWJetsFake], [HistoWGammaGen, HistoWGammaFake], [HistoZGammaGen, HistoZGammaFake], [HistoQCDGen, HistoQCDFake], [HistoGJetsGen, HistoGJetsFake]]


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

	if name == "TTJets_V03": # method has to work here TTJets is EW
		i=0
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])
	if name == "TTGamma_V03":
		i=1
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])
	if name == "WJets_250_300_V03" or name == "WJets_300_400_V03" or name == "WJets_400_inf_V03": # same for WJets (EW)
		i=2
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])
	if name == "WGamma_130_inf_V03" or name == "WGamma_50_130_V03":
		i=3
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])
	if name == "ZGamma_V02":
		i=4
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])
	if name == "QCD_250_500_V03" or name == "QCD_100_250_V09" or name == "QCD_500_1000_V03" or name == "QCD_1000_inf_V03":
		i=5
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])
	if name == "GJets_100_200_V09" or name == "GJets_200_400_V03" or name == "GJets_400_inf_V03" or name == "GJets_40_100_V09":
		i=6
		print "filling in "+str(Histos[i][0])+" und "+str(Histos[i][1])

	tree = FileList[name].Get("myTree")#Inputtree
	weight = Lint/Lsim[name]
	print "weight is "+str(weight)
	stop=0
	for event in tree:
		if stop==10000 and BreakFill:
			print "breaking loop..."
			break
		stop+=1
		if isSignal(event)=="GT":
			if plotvar=="PhotonPt":
				HistSimData.Fill( event.photons[0].pt, weight*event.weight )
			elif plotvar=="Ht":
				HistSimData.Fill( event.ht, weight*event.weight )
			elif plotvar=="Met":
				HistSimData.Fill( event.met, weight*event.weight )

				
			if event.photons[0].genElectron:
				if plotvar=="PhotonPt":
					HistSimGen.Fill( event.photons[0].pt, weight*event.weight )
					Histos[i][0].Fill( event.photons[0].pt, weight*event.weight )
				elif plotvar=="Ht":
					HistSimGen.Fill( event.ht, weight*event.weight )
					Histos[i][0].Fill( event.ht, weight*event.weight )
				elif plotvar=="Met":
					HistSimGen.Fill( event.met, weight*event.weight )
					Histos[i][0].Fill( event.met, weight*event.weight )
		elif isSignal(event)=="e":
			eweight = 1 - (1 - 0.00623) * (1 - pow(event.electrons[0].pt / 4.2 + 1,-2.9)) * (1 - 0.29 * pow(e,-0.335 * event.nTracksPV)) * (1 - 0.000223 * event.nVertex)
			if plotvar=="PhotonPt":
				HistSimFake.Fill( event.electrons[0].pt, eweight*event.weight*weight )
				Histos[i][1].Fill( event.electrons[0].pt, eweight*event.weight*weight )
			elif plotvar=="Ht":
				HistSimFake.Fill( event.ht, eweight*event.weight*weight )
				Histos[i][1].Fill( event.ht, eweight*event.weight*weight )
			elif plotvar=="Met":
				HistSimFake.Fill( event.met, eweight*event.weight*weight )
				Histos[i][1].Fill( event.met, eweight*event.weight*weight )
		elif isSignal(event)!="GL":
			print isSignal(event)

	print "******************************************************************"


TFileEfake.cd()
i = 0
i = int(i)
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
	for i2 in range(1, MinMax[0]+1):
		TempClone.SetBinError(i2,0.11*TempClone.GetBinContent(i2))

	TempClone.SetFillColor(4)
	TempClone.SetLineColor(4)
	TempClone.SetFillStyle(3254)

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
	ROOT.gPad.SaveAs(homePath+plotvar+"/"+TempTitle+plotvar+"EFakes.pdf")
	print "i = "+str(i)
	Histos[i][1].Write("Sim"+plotvar+TempTitle+"Fake")	
	Histos[i][0].Write("Sim"+plotvar+TempTitle+"Gen")	


HistSimFake.SetLineColor(2)
HistSimFake.SetLineWidth(1)
HistSimFake.SetMarkerSize(0)

HistSimFakeClone = HistSimFake.Clone("HistSimFakeClone")
for i in range(1, MinMax[0]+1):
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
HistSimFakeClone.SetFillStyle(3254)

HistSimGen.SetLineWidth(1)

HistSimFakeClone.Draw("E2")
HistSimFake.Draw("same Ehist")
HistSimGen.Draw("same PEX0")
L.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
ROOT.gPad.SaveAs(homePath+plotvar+"/"+plotvar+"EFakes.pdf")
HistSimGen.Write(plotvar+"SimGen")
HistSimFake.Write(plotvar+"SimFake")
HistSimFakeClone.Write(plotvar+"SimFakeSys")


HistFakeDataClone = HistFakeData.Clone("HistFakeDataClone")
for i in range(1, MinMax[0]+1):
	HistFakeDataClone.SetBinError(i,0.11*HistFakeDataClone.GetBinContent(i))

HistFakeData.Write(plotvar+"DataFake")
HistFakeDataClone.Write(plotvar+"DataFakeSys")
