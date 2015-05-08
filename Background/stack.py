import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
stack = ROOT.THStack("stack", "simulated back ground:x:y")

# possible Variables:
# Met Ht PhotonPt
plotvar="PhotonPt" # set plotvar
BreakFill=1 # if set to 1 the loop will break after 10000 Entries
Lint = 13771. # luminosity of the data


IDVersion =".03_tree.root" #Version of the trees

# maps used to mesure weight and define TFiles
# the order in which plots are stacked and generated is set in Names
# N for data is set to LumData and sigam for data is 1 => weight=1
Names=["TTGamma_V03", "TTJets_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
N = {'TTGamma_V03':1719954., 'TTJets_V03':6923652., 'WGamma_130_inf_V03':471458., 'WGamma_50_130_V03':1135698., 'WJets_250_300_V03':4940990., 'WJets_300_400_V03':5141023., 'WJets_400_inf_V03':2871847., 'ZGammaNuNu_V03':489474., 'ZGamma_V02':6321549., 'GJets_100_200_V09':9612703., 'GJets_200_400_V03':57627140., 'GJets_400_inf_V03':42391680., 'GJets_40_100_V09':19857930., 'QCD_250_500_V03':26109530., 'QCD_100_250_V09':50129520., 'QCD_500_1000_V03':29599290., 'QCD_1000_inf_V03':13843860., "PhotonA_V04":Lint, "SinglePhotonB_V04":Lint, "SinglePhotonC_V04":Lint, "PhotonParkedD_V10":Lint }
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':0.2571, 'WGamma_50_130_V03':1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':0.074, 'ZGamma_V02':123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204., 'PhotonA_V04':1.,  'SinglePhotonB_V04':1., 'SinglePhotonC_V04':1., 'PhotonParkedD_V10':1.}
Lsim = {}
FileList = {}


for name in Names:
	Lsim[name]=N[name]/sigma[name] # fill map with luminosity (data Lsim is set to Lint)
	FileList[name]=ROOT.TFile("/user/eicker/"+name+IDVersion) # fill map with TFiles

print Lsim
	
L = ROOT.TLegend(.6,.6,.9,.9)


i=0#counting variable
for variable in Names:
	print "******************************************************************"
	tree = FileList[variable].Get("myTree")#Inputtree
	weight = Lint/Lsim[variable]
	#testHis=createHistoFromTree(tree, "met", str(weight), 25, 0., 500. )
	testHis = ROOT.TH1F( variable, variable, 30, 0, 2000 )
	stop=0
	for event in tree:
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
	
	if i<2:# select TT
		testHis.SetMarkerColor(ROOT.kBlue)
		testHis.SetFillColor(ROOT.kBlue)
		testHis.SetLineColor(ROOT.kBlue)
		testHis.SetLineWidth(1)
		if i==1:
			L.AddEntry(testHis, "TTJets", "f")
		if i==0:
			testHis.SetFillColor(ROOT.kBlue-6)
			testHis.SetLineColor(ROOT.kBlue-6)
			L.AddEntry(testHis, "TTGamma", "f")
			
		print "identified TT and marked Blue"
	elif i<9:# select Z/W
		testHis.SetFillColor(ROOT.kRed)
		testHis.SetMarkerColor(ROOT.kRed)
		testHis.SetLineColor(ROOT.kRed)
		testHis.SetLineWidth(1)
		if i==2 or i==3:
			testHis.SetFillColor(ROOT.kRed-7)
			testHis.SetLineColor(ROOT.kRed-7)
			if i==3:
				L.AddEntry(testHis, "WGamma", "f")
		elif i==4 or i==5 or i==6:
			testHis.SetFillColor(ROOT.kRed)
			testHis.SetLineColor(ROOT.kRed)
			if i==6:
				L.AddEntry(testHis, "WJets", "f")
		elif i==7:
			i+=1
			continue
			testHis.SetFillColor(ROOT.kRed+2)
			testHis.SetLineColor(ROOT.kRed+2)
			L.AddEntry(testHis, "ZGammaNuNu", "f")
		elif i==8:
			testHis.SetFillColor(ROOT.kRed+3)
			testHis.SetLineColor(ROOT.kRed+3)
			L.AddEntry(testHis, "ZGamma", "f")
		print "identified W/Z and marked Red"
	elif i<13:#GJets
		testHis.SetFillColor(ROOT.kGreen)
		testHis.SetMarkerColor(ROOT.kGreen)
		testHis.SetLineColor(ROOT.kGreen)
		testHis.SetLineWidth(1)
		if i==12:
			L.AddEntry(testHis, "GJets", "f")
		print "identified GJets and marked Green"
	elif i<17:#QCD
		testHis.SetFillColor(ROOT.kRed+2)
		testHis.SetMarkerColor(ROOT.kRed+2)
		testHis.SetLineColor(ROOT.kRed+2)
		testHis.SetLineWidth(1)
		if i==16:
			L.AddEntry(testHis, "Multijet", "f")
		print "identified QCD and marked Yellow"
	elif i<21:#Data
		break

	testHis.Draw()
	ROOT.gPad.SaveAs(plotvar+"/"+variable+plotvar+".pdf")
	i+=1
	stack.Add(testHis)
	print 'weight is '+str(weight)
	print "Integral is: "+str(testHis.Integral())
	print "Added "+variable+IDVersion
	print "******************************************************************"

data = ROOT.TChain("myTree")

weight=1#set weight=1 for real data
#Data
i=0
for variable in Names:
	if i<17:
		i+=1
		continue
	print "******************************************************************"
	data.Add("/user/eicker/"+name+IDVersion+"/myTree")#Add Trees to TChain
	print "Added "+variable+IDVersion+"/myTree  to chain"
	print "weight is "+str(weight)

print "******************************************************************"
testHis = ROOT.TH1F( variable, variable, 30, 0, 2000 )
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
ROOT.gPad.SaveAs(plotvar+"/"+"ChainedData"+plotvar+".pdf")

print "Integral is: "+str(testHis.Integral())
print "Data is plotted"
print "******************************************************************"
stack.Draw()
ROOT.gPad.SaveAs(plotvar+"/"+"Background"+plotvar+".pdf")

stack.SetTitle("13.8fb^{-1}")
stack.GetXaxis().SetTitle(plotvar+"[GeV]")#"E_{T}^{miss}(GeV)"
stack.GetYaxis().SetTitle("Events")
stack.GetXaxis().SetTitleOffset(1)
stack.GetYaxis().SetTitleOffset(1)

stack.Draw("")
stack.SetMinimum( 0.01 )
stack.SetMaximum( 1000000 )
testHis.SetMinimum( 0.01 )
testHis.SetMaximum( 1000000 )
testHis.Draw("samePE")
L.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
ROOT.gPad.SaveAs("Stack"+plotvar+".pdf")
