import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
e=2.7182818284590452353602874713526624977572470937

simulated = ROOT.TChain("myTree")
data = ROOT.TChain("myTree")

# possible Variables:
# Met Ht PhotonPt
plotvar="Met" # set plotvar
BreakFill=0 # if set to 1 the loop will break after 10000 Entries
PrintMaps=0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "Events"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/V04/"

if plotvar == "PhotonPt":
	Title[1]="PhotonPt(GeV)"
	MinMax = [30,100,1900,0.01,1000000]
elif plotvar == "Met":
	Title[1]="E_{T}^{miss}(GeV)"
	MinMax = [15,0,800,0.01,1000000]
elif plotvar == "Ht":
	Title[1]="Ht(GeV)"
	MinMax = [25,0,1800,0.1,100000000]
else:
	print "no binning information!"


IDVersion =".04_tree.root" #Version of the trees

# maps used to mesure weight and define TFiles
# the order in which plots are stacked and generated is set in Names
# weight for data has to bet set to 1 later!
Names=["TTJets_V03", "TTGamma_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
#N = {'TTGamma_V03':1719954., 'TTJets_V03':6923652., 'WGamma_130_inf_V03':471458., 'WGamma_50_130_V03':1135698., 'WJets_250_300_V03':4940990., 'WJets_300_400_V03':5141023., 'WJets_400_inf_V03':2871847., 'ZGammaNuNu_V03':489474., 'ZGamma_V02':6321549., 'GJets_100_200_V09':9612703., 'GJets_200_400_V03':57627140., 'GJets_400_inf_V03':42391680., 'GJets_40_100_V09':19857930., 'QCD_250_500_V03':26109530., 'QCD_100_250_V09':50129520., 'QCD_500_1000_V03':29599290., 'QCD_1000_inf_V03':13843860., "PhotonA_V04":Lint, "SinglePhotonB_V04":Lint, "SinglePhotonC_V04":Lint, "PhotonParkedD_V10":Lint }
N = {}
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':0.2571, 'WGamma_50_130_V03':1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':0.074, 'ZGamma_V02':123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204., 'PhotonA_V04':1.,  'SinglePhotonB_V04':1., 'SinglePhotonC_V04':1., 'PhotonParkedD_V10':1.}
Lsim = {}
FileList = {}


for name in Names:
	if name == "QCD_1000_inf_V03":
		continue
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

	
L = ROOT.TLegend(.6,.8,.9,.9)

# Data Trees are added to a chain and then looped over in one loop
weight=1#set weight=1 for real data
#Data

for name in Names:
	if name !="PhotonA_V04" and name !="SinglePhotonB_V04" and name !="SinglePhotonC_V04" and name !="PhotonParkedD_V10":
		continue # filter data names
	print "******************************************************************"
	data.Add(path+name+IDVersion+"/myTree")#Add Trees to TChain
	print "Added "+name+IDVersion+"/myTree  to chain"
	print "weight is "+str(weight)

print "******************************************************************"

HistData = ROOT.TH1F( "data", "data", MinMax[0], MinMax[1], MinMax[2] ) #				Hist for real data
HistFakeData = ROOT.TH1F( "fakes", "fakes", MinMax[0], MinMax[1], MinMax[2] )# 			Hist for fakes from data

HistSimData = ROOT.TH1F( "simData", "simData", MinMax[0], MinMax[1], MinMax[2] ) #		Hist for simulated data
HistSimulated = ROOT.TH1F( "simulated", "simulated", MinMax[0], MinMax[1], MinMax[2] )#	Hist for REAL fakes (matched genElectron) from simData
HistSimFake = ROOT.TH1F( "simFake", "simFake", MinMax[0], MinMax[1], MinMax[2] )#		Hist for fakes from simulation with the weight method

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
print "**********************    simulation    **************************"
stop=0
for name in Names: # loop over names
	print "******************************************************************"
	if name =="PhotonA_V04" or name =="SinglePhotonB_V04" or name =="SinglePhotonC_V04" or name =="PhotonParkedD_V10" or name =="QCD_1000_inf_V03":
		continue # filter simulated data
	print "looping over: "+path+name+IDVersion		
	tree = FileList[name].Get("myTree")#Inputtree
	weight = Lint/Lsim[name]
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
					HistSimulated.Fill( event.photons[0].pt, weight*event.weight )
				elif plotvar=="Ht":
					HistSimulated.Fill( event.ht, weight*event.weight )
				elif plotvar=="Met":
					HistSimulated.Fill( event.met, weight*event.weight )
		if event.electrons.size()>0:
			eweight = 1 - (1 - 0.00623) * (1 - pow(event.electrons[0].pt / 4.2 + 1,-2.9)) * (1 - 0.29 * pow(e,-0.335 * event.nTracksPV)) * (1 - 0.000223 * event.nVertex)
			if plotvar=="PhotonPt":
				HistSimFake.Fill( event.electrons[0].pt, eweight*event.weight )
			elif plotvar=="Ht":
				HistSimFake.Fill( event.ht, eweight*event.weight )
			elif plotvar=="Met":
				HistSimFake.Fill( event.met, eweight*event.weight )
	print "******************************************************************"
HistFakeData.SetLineColor(3)
HistFakeData.SetLineWidth(1)
HistFakeData.SetMarkerSize(0)

HistFakeDataClone = HistFakeData.Clone("HistFakeDataClone")
for i in range(0, MinMax[0]):
	HistFakeDataClone.SetBinError(i,0.11*HistFakeDataClone.GetBinContent(i))

HistFakeData.SetTitle(Title[0])
HistFakeData.GetXaxis().SetTitle(Title[1])
HistFakeData.GetYaxis().SetTitle(Title[2])
HistFakeData.GetXaxis().SetTitleOffset(1)
HistFakeData.GetYaxis().SetTitleOffset(1)

L.AddEntry(HistSimulated, "Direct simulation", "lep")
L.AddEntry(HistFakeData, "Prediction", "f")

HistFakeDataClone.SetFillColor(4)
HistFakeDataClone.SetLineColor(4)
HistFakeDataClone.SetFillStyle(3005)

HistSimulated.SetLineWidth(1)

HistFakeData.Draw("Ehist")
HistFakeDataClone.Draw("sameE2")
HistSimulated.Draw("samePEX0")
L.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
ROOT.gPad.SaveAs("EFakes.pdf")

