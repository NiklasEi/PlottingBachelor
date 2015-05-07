import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")

plotvar="Ht"
stack = ROOT.THStack("stack", "Simulierter Untergrund")
datastack = ROOT.THStack("datastack", "Data")
Lint = 13012.


IDVersion =".03_tree.root"
Names=["TTGamma_V03", "TTJets_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
N = {'TTGamma_V03':1719954., 'TTJets_V03':6923652., 'WGamma_130_inf_V03':471458., 'WGamma_50_130_V03':1135698., 'WJets_250_300_V03':4940990., 'WJets_300_400_V03':5141023., 'WJets_400_inf_V03':2871847., 'ZGammaNuNu_V03':489474., 'ZGamma_V02':6321549., 'GJets_100_200_V09':9612703., 'GJets_200_400_V03':57627140., 'GJets_400_inf_V03':42391680., 'GJets_40_100_V09':19857930., 'QCD_250_500_V03':26109530., 'QCD_100_250_V09':50129520., 'QCD_500_1000_V03':29599290., 'QCD_1000_inf_V03':13843860. }
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':0.2571, 'WGamma_50_130_V03':1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':0.074, 'ZGamma_V02':123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204. }
Lsim = {}
FileList = {}

N["PhotonA_V04"]=Lint
N["SinglePhotonB_V04"]=Lint
N["SinglePhotonC_V04"]=Lint
N["PhotonParkedD_V10"]=Lint

sigma["PhotonA_V04"]=1.
sigma["SinglePhotonB_V04"]=1.
sigma["SinglePhotonC_V04"]=1.
sigma["PhotonParkedD_V10"]=1.

for name in Names:
	Lsim[name]=N[name]/sigma[name]
	FileList[name]=ROOT.TFile("/user/eicker/"+name+IDVersion)

print Lsim
	
L = ROOT.TLegend(.6,.6,.9,.9)


i=0#counting variable
for variable in Names:
	if i==17:
		break
	print "******************************************************************"
	tree = FileList[variable].Get("myTree")#Inputtree
	weight = Lint/Lsim[variable]
	#testHis=createHistoFromTree(tree, "met", str(weight), 25, 0., 500. )
	testHis = ROOT.TH1F( variable, variable, 30, 0, 1500 )
	stop=0
	for event in tree:
		#if stop>10000:
		#	break
		stop+=1	
		if event.photons.size() ==0:
			continue
		testHis.Fill( event.ht, weight )
	
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
		testHis.SetFillColor(ROOT.kYellow)
		testHis.SetMarkerColor(ROOT.kYellow)
		testHis.SetLineColor(ROOT.kYellow)
		testHis.SetLineWidth(1)
		if i==16:
			L.AddEntry(testHis, "Multijet", "f")
		print "identified QCD and marked Yellow"
	elif i<21:#Data
		break

	#testHis.SetFillStyle(1)
	#testHis.SetFillColor(i+1)
	#testHis.SetMarkerColor(i+1)
	#testHis.SetLineColor(i+1)
	testHis.Draw()
	ROOT.gPad.SaveAs(variable+plotvar+".pdf")
	i+=1
	stack.Add(testHis)
	print 'weight is '+str(weight)
	print "Integral is: "+str(testHis.Integral())
	print "Added "+variable+IDVersion
	print "******************************************************************"

data = ROOT.TChain("myTree")

weight=1
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
testHis = ROOT.TH1F( variable, variable, 30, 0, 1500 )
stop=0

for event in data:
	#if stop>10000:
	#	break
	stop+=1	
	if event.photons.size() ==0:
		continue
	testHis.Fill( event.ht, weight )


testHis.SetFillStyle(0)
testHis.SetLineColor(ROOT.kBlack)
testHis.SetLineWidth(2)

testHis.Draw()
ROOT.gPad.SaveAs("ChainedData"+plotvar+".pdf")

print "Integral is: "+str(testHis.Integral())
print "Data is plotted"
print "******************************************************************"
stack.Draw()
ROOT.gPad.SaveAs("Background"+plotvar+".pdf")


stack.Draw("")
stack.SetMinimum( 1. )
stack.SetMaximum( 100000000 )
testHis.Draw("same")
L.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
ROOT.gPad.SaveAs("Stack"+plotvar+".pdf")
