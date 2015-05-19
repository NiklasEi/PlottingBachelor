import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")

stack = ROOT.THStack("stack", "simulated back ground")
data = ROOT.TChain("myTree")

# possible Variables:
# Met Ht PhotonPt
plotvar="Met" # set plotvar
BreakFill=1 # if set to 1 the loop will break after 10000 Entries
PrintMaps=0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}", plotvar, "Events"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/V05/"


print "Programm is:"
if BreakFill:
	print "breaking loops after 10000 entries and saving *Break.pdf files"
else:
	print "not breaking loops after 10000 entries and saving 'main pdfs'"
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


IDVersion =".05_tree.root" #Version of the trees

# maps used to mesure weight and define TFiles
# the order in which plots are stacked and generated is set in Names
# N for data is set to LumData and sigam for data is 1 => weight=1
Names=["TTJets_V03", "TTGamma_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
#N = {'TTGamma_V03':1719954., 'TTJets_V03':6923652., 'WGamma_130_inf_V03':471458., 'WGamma_50_130_V03':1135698., 'WJets_250_300_V03':4940990., 'WJets_300_400_V03':5141023., 'WJets_400_inf_V03':2871847., 'ZGammaNuNu_V03':489474., 'ZGamma_V02':6321549., 'GJets_100_200_V09':9612703., 'GJets_200_400_V03':57627140., 'GJets_400_inf_V03':42391680., 'GJets_40_100_V09':19857930., 'QCD_250_500_V03':26109530., 'QCD_100_250_V09':50129520., 'QCD_500_1000_V03':29599290., 'QCD_1000_inf_V03':13843860., "PhotonA_V04":Lint, "SinglePhotonB_V04":Lint, "SinglePhotonC_V04":Lint, "PhotonParkedD_V10":Lint }
N = {}
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':0.2571, 'WGamma_50_130_V03':1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':0.074, 'ZGamma_V02':123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204., 'PhotonA_V04':1.,  'SinglePhotonB_V04':1., 'SinglePhotonC_V04':1., 'PhotonParkedD_V10':1.}
Lsim = {}
FileList = {}


for name in Names:
	FileList[name]=ROOT.TFile(path+name+IDVersion) # fill map with TFiles
	GenHist = FileList[name].Get("nGen")
	N[name] = GenHist.GetEntries()
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

	
L = ROOT.TLegend(.6,.6,.9,.9)


i=0#counting variable
for variable in Names:
	print "******************************************************************"
	tree = FileList[variable].Get("myTree")#Inputtree
	weight = Lint/Lsim[variable]
	#testHis=createHistoFromTree(tree, "met", str(weight), 25, 0., 500. )
	testHis = ROOT.TH1F( variable, variable, MinMax[0], MinMax[1], MinMax[2]  )
	testHis.SetLineWidth(1)
	stop=0
	for event in tree:
		if stop==10000 and BreakFill:
			break
		stop+=1	
		if event.photons.size() ==0:
			continue
		if plotvar=="PhotonPt":
			testHis.Fill( event.photons[0].pt, weight*event.weight )
		elif plotvar=="Ht":
			testHis.Fill( event.ht, weight*event.weight )
		elif plotvar=="Met":
			testHis.Fill( event.met, weight*event.weight )
	
	if i<2:# select TT
		if i==1:
			testHis.SetFillColor(ROOT.kRed)
			testHis.SetLineColor(ROOT.kRed)
			L.AddEntry(testHis, "TTGamma", "f")
			print "identified TTGamma"
		if i==0:
			testHis.SetFillColor(ROOT.kYellow)
			testHis.SetLineColor(ROOT.kYellow)
			L.AddEntry(testHis, "TTJets", "f")
			print "identified TTJets"
	elif i<9:# select Z/W
		if i==2 or i==3:
			testHis.SetFillColor(ROOT.kBlue)
			testHis.SetLineColor(ROOT.kBlue)
			if i==3:
				L.AddEntry(testHis, "WGamma", "f")
			print "identified WGamma"
		elif i==4 or i==5 or i==6:
			testHis.SetFillColor(ROOT.kCyan-2)
			testHis.SetLineColor(ROOT.kCyan-2)
			if i==6:
				L.AddEntry(testHis, "WJets", "f")
			print "identified WJets"
		elif i==7:
			i+=1
			continue
			testHis.SetFillColor(ROOT.kRed+2)
			testHis.SetLineColor(ROOT.kRed+2)
			L.AddEntry(testHis, "ZGammaNuNu", "f")
			print "identified ZGammaNuNu"
		elif i==8:
			testHis.SetFillColor(ROOT.kGreen+3)
			testHis.SetLineColor(ROOT.kGreen+3)
			L.AddEntry(testHis, "ZGamma", "f")
			print "identified ZGamma"
	elif i<13:#GJets
		testHis.SetFillColor(ROOT.kGreen)
		testHis.SetLineColor(ROOT.kGreen)
		if i==12:
			L.AddEntry(testHis, "Multijet", "f")
		print "identified QCD and marked Green"
	elif i<17:#QCD
		testHis.SetFillColor(ROOT.kRed+3)
		testHis.SetLineColor(ROOT.kRed+3)
		if i==16:
			L.AddEntry(testHis, "GJets", "f")
		print "identified GJets and marked Yellow"
	elif i<21:#Data
		break

	testHis.Draw()
	
	if not BreakFill:
		ROOT.gPad.SaveAs(plotvar+"/"+variable+plotvar+".pdf")
	
	if BreakFill:
		ROOT.gPad.SaveAs(plotvar+"/"+variable+plotvar+"Break.pdf")
		
	i+=1
	stack.Add(testHis)
	print 'weight is '+str(weight)+' times weight from event'
	print "Integral is: "+str(testHis.Integral())
	print "Added "+variable+IDVersion
	print "******************************************************************"

# Data Trees are added to a chain and then looped over in one loop
weight=1#set weight=1 for real data
#Data
i=0
for name in Names:
	if i<17:
		i+=1
		continue
	print "******************************************************************"
	data.Add(path+name+IDVersion+"/myTree")#Add Trees to TChain
	print "Added "+name+IDVersion+"/myTree  to chain"
	print "weight is "+str(weight)

print "******************************************************************"
testHis = ROOT.TH1F( "data", "data", MinMax[0], MinMax[1], MinMax[2] )
stop=0

for event in data:
	if stop==10000 and BreakFill:
		break
	stop+=1
	if event.photons.size() ==0:
		continue
	if plotvar=="PhotonPt":
		testHis.Fill( event.photons[0].pt, weight )
	elif plotvar=="Ht":
		testHis.Fill( event.ht, weight )
	elif plotvar=="Met":
		testHis.Fill( event.met, weight )

L.AddEntry(testHis, "Data", "lep")
testHis.SetFillStyle(0)
testHis.SetLineColor(ROOT.kBlack)
testHis.SetLineWidth(2)
testHis.SetMarkerStyle(20)

testHis.Draw()

if not BreakFill:
	ROOT.gPad.SaveAs(plotvar+"/"+"ChainedData"+plotvar+".pdf")

if BreakFill:
	ROOT.gPad.SaveAs(plotvar+"/"+"ChainedData"+plotvar+"Break.pdf")	

print "Integral is: "+str(testHis.Integral())
print "Data is plotted"
print "******************************************************************"
stack.Draw()

if not BreakFill:
	ROOT.gPad.SaveAs(plotvar+"/"+"Background"+plotvar+".pdf")

if BreakFill:
	ROOT.gPad.SaveAs(plotvar+"/"+"Background"+plotvar+"Break.pdf")
	
stack.SetTitle(Title[0])
stack.GetXaxis().SetTitle(Title[1])
stack.GetYaxis().SetTitle(Title[2])
stack.GetXaxis().SetTitleOffset(1)
stack.GetYaxis().SetTitleOffset(1)

stack.Draw("")
stack.SetMinimum( MinMax[3] )
stack.SetMaximum( MinMax[4] )
testHis.SetMinimum( MinMax[3] )
testHis.SetMaximum( MinMax[4] )
testHis.Draw("samePE")
L.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()

if not BreakFill:
	ROOT.gPad.SaveAs("Stack"+plotvar+".pdf")
	
if BreakFill:
	ROOT.gPad.SaveAs("Stack"+plotvar+"Break.pdf")
