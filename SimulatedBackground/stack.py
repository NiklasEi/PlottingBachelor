import ROOT
import sys
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")

# change status to recreate if you change keys in .Write() otherwise "update"
TFileStack = ROOT.TFile("TFileStack.root", "update") # TFile to save histos

"""
This programm stacks all simulated events to be able to compare it to Data.
Plots are saved for every simulation and for stacked simulation (all QCD/all GJet)

"""

stack = ROOT.THStack("stack", "simulated back ground")
QCDStack = ROOT.THStack("QCDStack", "simulated QCD")
GJetsStack = ROOT.THStack("GJetsStack", "simulated GJets")
data = ROOT.TChain("myTree")


#programm ignores events with 0 tight photons!

# possible Variables:
# Met Ht PhotonPt PhotonEta PhotonPhi
plotvar="Ht" # set plotvar 
PrintBreak=0 # if set to 1 'break pdfs' will be printed when running with BreakFill=1
BreakFill=0 # if set to 1 the loop will break after 10000 Entries
PrintMaps=0 # if set to 1 the maps will be printed
Lint = 13771. # luminosity of the data
Title=["13.8fb^{-1}, #gamma_{tight}>0", plotvar, "Events"] # plottitle, axislabels (X,Y) is changed afterwards depending on plotvar
MinMax = [1.,1.,1.,1.,1.] # nBin, lowBin, highBin, Min, Max
path ="/user/eicker/test/"
IDVersion =".Test_tree.root" #Version of the trees
homePath="~/plotting/SimulatedBackground/"



if len(sys.argv)>1:
	if len(sys.argv)==2:
		print "found argument: "+sys.argv[1]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt" or sys.argv[1]=="PhotonEta" or sys.argv[1]=="PhotonPhi":
			plotvar=sys.argv[1]
			print "set plotvar = "+sys.argv[1]
	if len(sys.argv)==3:
		print "found arguments: "+sys.argv[1]+" and "+sys.argv[2]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt" or sys.argv[1]=="PhotonEta" or sys.argv[1]=="PhotonPhi":
			plotvar=sys.argv[1]
			BreakFill=int(sys.argv[2])
			print "set plotvar = "+sys.argv[1]+" and BreakFill was set to "+sys.argv[2]
		




integralGes=0
print "plotting against "+plotvar
print "Programm is:"
if BreakFill:
	print "breaking loops after 10000 entries and saving *Break.pdf files"
else:
	print "looping over all entries and saving 'main pdfs'"
if PrintMaps:
	print "printing maps with names, files, entries ..."
else:
	print "not printing maps"


if plotvar == "PhotonPt":
	Title[1]="PhotonPt(GeV)"
	MinMax = [30,145,1900,0.01,1000000]
elif plotvar == "PhotonEta":
	#ROOT.gStyle.SetOptLogy(0)
	MinMax=[30, -1.5, 1.5, 0.01, 1000000000]
elif plotvar == "PhotonPhi":
	#ROOT.gStyle.SetOptLogy(0)
	MinMax=[30, -3.5, 3.5, 0.01, 1000000000]
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
	print "############# N ##############"
	print N
	print "########### sigma ############"
	print sigma
	print "########### Lsim #############"
	print Lsim
	print "######### Filelist ###########"
	print FileList

	
L = ROOT.TLegend(.6,.6,.9,.9)


i=0#counting variable
for variable in Names:
	if variable =="PhotonA_V04" or variable =="SinglePhotonB_V04" or variable =="SinglePhotonC_V04" or variable =="PhotonParkedD_V10":
		continue # filter simulated data
	print "******************************************************************"
	print "looping over: "+path+variable+IDVersion
	if variable == "ZGammaNuNu_V03":
		print "skipping ZGammaNuNu"
		print "******************************************************************"
		i+=1
		continue
	tree = FileList[variable].Get("myTree")#Inputtree
	weight = Lint/Lsim[variable]
	testHis = ROOT.TH1F( variable, variable, MinMax[0], MinMax[1], MinMax[2]  )
	testHis.SetLineWidth(1)
	stop=0
	for event in tree:
		if stop==100000 and BreakFill:
			break
		stop+=1	
		if event.photons.size() ==0:
			continue
		if plotvar=="PhotonPt":
			testHis.Fill( event.photons[0].pt, weight*event.weight )
		elif plotvar=="PhotonEta":
			testHis.Fill( event.photons[0].eta, weight*event.weight )
		elif plotvar=="PhotonPhi":
			testHis.Fill( event.photons[0].phi, weight*event.weight )
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
			testHis.SetFillColor(ROOT.kRed+2)
			testHis.SetLineColor(ROOT.kRed+2)
			L.AddEntry(testHis, "ZGammaNuNu", "f")
			print "identified ZGammaNuNu"
		elif i==8:
			testHis.SetFillColor(ROOT.kGreen+3)
			testHis.SetLineColor(ROOT.kGreen+3)
			L.AddEntry(testHis, "ZGamma", "f")
			print "identified ZGamma"
	elif i<13:#QCD
		testHis.SetFillColor(ROOT.kGreen)
		testHis.SetLineColor(ROOT.kGreen)
		if i==12:
			L.AddEntry(testHis, "Multijet", "f")
		QCDStack.Add(testHis)
		print "Added "+path+variable+IDVersion+"/myTree  to QCDStack"
		print "identified QCD and marked Green"
	elif i<17:#GJets
		testHis.SetFillColor(ROOT.kRed+3)
		testHis.SetLineColor(ROOT.kRed+3)
		if i==16:
			L.AddEntry(testHis, "GJets", "f")
		GJetsStack.Add(testHis)
		print "Added "+path+variable+IDVersion+"/myTree  to GJetsStack"
		print "identified GJets and marked Yellow"

	testHis.Draw()
	
	if not BreakFill:
		ROOT.gPad.SaveAs(homePath+plotvar+"/"+variable+plotvar+".pdf")
	
	if BreakFill and PrintBreak:
		ROOT.gPad.SaveAs(homePath+plotvar+"/"+variable+plotvar+"Break.pdf")
		
	i+=1
	stack.Add(testHis)
	print 'weight is '+str(weight)+' times weight from event'
	print "Integral is: "+str(testHis.Integral())
	integralGes+=testHis.Integral()
	print "Added "+variable+IDVersion
	TFileStack.cd()
	testHis.Write(variable+plotvar)
	print "******************************************************************"

QCDStack.SetMinimum( 0.001 )
QCDStack.SetMaximum( 1000000 )
QCDStack.Draw()
if not BreakFill:
	ROOT.gPad.SaveAs(homePath+plotvar+"/QCDComplete.pdf")

GJetsStack.SetMinimum( 0.001 )
GJetsStack.SetMaximum( 1000000 )
GJetsStack.Draw()
if not BreakFill:
	ROOT.gPad.SaveAs(homePath+plotvar+"/GJetsComplete.pdf")

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
	print "Added "+path+name+IDVersion+"/myTree  to chain"
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
	elif plotvar=="PhotonEta":
		testHis.Fill( event.photons[0].eta, weight )
	elif plotvar=="PhotonPhi":
		testHis.Fill( event.photons[0].phi, weight )
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
	ROOT.gPad.SaveAs(homePath+plotvar+"/"+"ChainedData"+plotvar+".pdf")

if BreakFill and PrintBreak:
	ROOT.gPad.SaveAs(homePath+plotvar+"/"+"ChainedData"+plotvar+"Break.pdf")	

print "Integral is: "+str(testHis.Integral())
print "gesammtes Sim-Integral zum Vergleich: "+str(integralGes)
print "Data is plotted"
TFileStack.cd()
testHis.Write("Data"+plotvar)
print "******************************************************************"
stack.Draw()

if not BreakFill:
	ROOT.gPad.SaveAs(homePath+plotvar+"/"+"Background"+plotvar+".pdf")

if BreakFill and PrintBreak:
	ROOT.gPad.SaveAs(homePath+plotvar+"/"+"Background"+plotvar+"Break.pdf")
	
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

	
if BreakFill and PrintBreak:
	ROOT.gPad.SaveAs(homePath+"Stack"+plotvar+"Break.pdf")
