import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
#ROOT.TH1.SetDefaultSumw2()
e=2.7182818284590452353602874713526624977572470937

simulated = ROOT.TChain("myTree")
data = ROOT.TChain("myTree")

# possible Variables:
# Met Ht PhotonPt
plotvar="Met" # set plotvar
BreakFill = 0 # if set to 1 the loop will break after 10000 Entries
PrintMaps = 0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "#gamma_{tight}/#gamma_{loose}"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/V05/"
IDVersion =".05_tree.root" #Version of the trees

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


HistDataGTGL = ROOT.TH1F( "data", "data", 10, 0, 100 )
GT = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
GL = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
print "************************* looping data ***************************"
stop = 0
for event in data:
	if BreakFill:
		stop += 1
		if stop ==100:
			break
	if event.met > 100:
		continue
	if event.met < 10:
		GT[0] += event.photons.size()
		GL[0] += event.jetphotons.size()
	elif event.met < 20:
		GT[1] += event.photons.size()
		GL[1] += event.jetphotons.size()
	elif event.met < 30:
		GT[2] += event.photons.size()
		GL[2] += event.jetphotons.size()
	elif event.met < 40:
		GT[3] += event.photons.size()
		GL[3] += event.jetphotons.size()
	elif event.met < 50:
		GT[4] += event.photons.size()
		GL[4] += event.jetphotons.size()
	elif event.met < 60:
		GT[5] += event.photons.size()
		GL[5] += event.jetphotons.size()
	elif event.met < 70:
		GT[6] += event.photons.size()
		GL[6] += event.jetphotons.size()
	elif event.met < 80:
		GT[7] += event.photons.size()
		GL[7] += event.jetphotons.size()
	elif event.met < 90:
		GT[8] += event.photons.size()
		GL[8] += event.jetphotons.size()
	elif event.met < 100:
		GT[9] += event.photons.size()
		GL[9] += event.jetphotons.size()

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
	HistDataGTGL.SetBinError(i, 0.000001)
	GL[i]=0.
	GT[i]=0.

HistDataGTGL.SetTitle(Title[0])
HistDataGTGL.GetXaxis().SetTitle(Title[1])
HistDataGTGL.GetYaxis().SetTitle(Title[2])
HistDataGTGL.GetXaxis().SetTitleOffset(1)
HistDataGTGL.GetYaxis().SetTitleOffset(1.2)

HistDataGTGL.Draw("PE")
ROOT.gPad.SaveAs("GtGlRatioData.pdf")

print "*********************** simulated data ***************************"

print GT
print GL

HistSimGTGL = ROOT.TH1F( "Sim", "Sim", 10, 0, 100 )

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
	print "looping over: "+path+name+IDVersion
	tree = FileList[name].Get("myTree")#Inputtree
	weight = Lint/Lsim[name]
	print "weight is "+str(weight)
	for event in tree:
		if stop==10000 and BreakFill:
			break
		stop+=1	
		if event.met > 100:
			continue
		if event.met < 10:
			GT[0] += event.photons.size()*weight*event.weight
			GL[0] += event.jetphotons.size()*weight*event.weight
		elif event.met < 20:
			GT[1] += event.photons.size()*weight*event.weight
			GL[1] += event.jetphotons.size()*weight*event.weight
		elif event.met < 30:
			GT[2] += event.photons.size()*weight*event.weight
			GL[2] += event.jetphotons.size()*weight*event.weight
		elif event.met < 40:
			GT[3] += event.photons.size()*weight*event.weight
			GL[3] += event.jetphotons.size()*weight*event.weight
		elif event.met < 50:
			GT[4] += event.photons.size()*weight*event.weight
			GL[4] += event.jetphotons.size()*weight*event.weight
		elif event.met < 60:
			GT[5] += event.photons.size()*weight*event.weight
			GL[5] += event.jetphotons.size()*weight*event.weight
		elif event.met < 70:
			GT[6] += event.photons.size()*weight*event.weight
			GL[6] += event.jetphotons.size()*weight*event.weight
		elif event.met < 80:
			GT[7] += event.photons.size()*weight*event.weight
			GL[7] += event.jetphotons.size()*weight*event.weight
		elif event.met < 90:
			GT[8] += event.photons.size()*weight*event.weight
			GL[8] += event.jetphotons.size()*weight*event.weight
		elif event.met < 100:
			GT[9] += event.photons.size()*weight*event.weight
			GL[9] += event.jetphotons.size()*weight*event.weight
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
	HistSimGTGL.Fill(5+i*10, weight)
	HistSimGTGL.SetBinError(i, 0.000001)
	GL[i]=0
	GT[i]=0


HistSimGTGL.SetTitle(Title[0])
HistSimGTGL.GetXaxis().SetTitle(Title[1])
HistSimGTGL.GetYaxis().SetTitle(Title[2])
HistSimGTGL.GetXaxis().SetTitleOffset(1)
HistSimGTGL.GetYaxis().SetTitleOffset(1.2)

HistSimGTGL.Draw("PE")
ROOT.gPad.SaveAs("GtGlRatioSim.pdf")
