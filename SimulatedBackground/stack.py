import ROOT
import sys
from treeFunctions import *
from SignalScan import isSignal
ROOT.gSystem.Load("libTreeObjects.so")

"""
This program stacks all simulated events to be able to compare it to Data.
Plots are saved for every simulation and for stacked simulation (all QCD/all GJet)

"""

stack = ROOT.THStack("stack", "simulated back ground")
QCDStack = ROOT.THStack("QCDStack", "simulated QCD")
GJetsStack = ROOT.THStack("GJetsStack", "simulated GJets")


Canvas = ROOT.TCanvas ("Canvas", "Canvas")

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
path ="/user/eicker/08/"
IDVersion =".08_tree.root" #Version of the trees
homePath="~/plotting/SimulatedBackground/"



if len(sys.argv)>1:
	if len(sys.argv)==2:
		print "found argument: "+sys.argv[1]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt" or sys.argv[1]=="PhotonEta" or sys.argv[1]=="PhotonPhi":
			plotvar=sys.argv[1]
			print "set plotvar = "+sys.argv[1]
			sys.exit("need an argument for creating the TFile!")
	if len(sys.argv)==3:
		print "found arguments: "+sys.argv[1]+" and "+sys.argv[2]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt" or sys.argv[1]=="PhotonEta" or sys.argv[1]=="PhotonPhi":
			plotvar=sys.argv[1]
			BreakFill=int(sys.argv[2])
			print "set plotvar = "+sys.argv[1]+" and BreakFill was set to "+sys.argv[2]
			sys.exit("need an argument for creating the TFile!")
	if len(sys.argv)==4:
		print "found arguments: "+sys.argv[1]+" and "+sys.argv[2]+" and "+sys.argv[3]
		if sys.argv[1]=="Met" or sys.argv[1]=="Ht" or sys.argv[1]=="PhotonPt" or sys.argv[1]=="PhotonEta" or sys.argv[1]=="PhotonPhi":
			plotvar=sys.argv[1]
			BreakFill=int(sys.argv[2])
			print "creating TFile with "+sys.argv[3]
			print "set plotvar = "+sys.argv[1]+" and BreakFill was set to "+sys.argv[2]
else:
	sys.exit("need an argument for creating the TFile!")		


if sys.argv[3]=="recreate" or sys.argv[3]=="update":
	TFileStack = ROOT.TFile(homePath+"TFileStack.root", sys.argv[3]) # TFile to save histos
else:
	sys.exit("need a valid argument for creating the TFile!")


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
	MinMax=[32, -1.6, 1.6, 0.1, 1000000000]
	Title[1]="#eta_{Photon}"
elif plotvar == "PhotonPhi":
	#ROOT.gStyle.SetOptLogy(0)
	MinMax=[30, -3.5, 3.5, 0.1, 1000000000]
	Title[1]="#varphi_{Photon}"
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
# N for data is set to LumData and sigam for data is 1 => weight=1
Names=["TTJets_V03", "TTGamma_V03", "WGamma_130_inf_V03", "WGamma_50_130_V03", "WJets_250_300_V03", "WJets_300_400_V03", "WJets_400_inf_V03", "ZGammaNuNu_V03", "ZGamma_V02", "QCD_250_500_V03", "QCD_100_250_V09", "QCD_500_1000_V03", "QCD_1000_inf_V03", "GJets_100_200_V09", "GJets_200_400_V03", "GJets_400_inf_V03", "GJets_40_100_V09", "PhotonA_V04", "SinglePhotonB_V04", "SinglePhotonC_V04", "PhotonParkedD_V10"]
#N = {'TTGamma_V03':1719954., 'TTJets_V03':6923652., 'WGamma_130_inf_V03':471458., 'WGamma_50_130_V03':1135698., 'WJets_250_300_V03':4940990., 'WJets_300_400_V03':5141023., 'WJets_400_inf_V03':2871847., 'ZGammaNuNu_V03':489474., 'ZGamma_V02':6321549., 'GJets_100_200_V09':9612703., 'GJets_200_400_V03':57627140., 'GJets_400_inf_V03':42391680., 'GJets_40_100_V09':19857930., 'QCD_250_500_V03':26109530., 'QCD_100_250_V09':50129520., 'QCD_500_1000_V03':29599290., 'QCD_1000_inf_V03':13843860., "PhotonA_V04":Lint, "SinglePhotonB_V04":Lint, "SinglePhotonC_V04":Lint, "PhotonParkedD_V10":Lint }
N = {}
sigma = {'TTGamma_V03':2.166, 'TTJets_V03':225.2, 'WGamma_130_inf_V03':1.5*0.2571, 'WGamma_50_130_V03':1.5*1.17, 'WJets_250_300_V03':48., 'WJets_300_400_V03':38.3, 'WJets_400_inf_V03':25.2, 'ZGammaNuNu_V03':1.5*0.074, 'ZGamma_V02':1.5*123.9, 'GJets_100_200_V09':5212., 'GJets_200_400_V03':960.5, 'GJets_400_inf_V03':107.5, 'GJets_40_100_V09':20930., 'QCD_250_500_V03':276000., 'QCD_100_250_V09':10360000., 'QCD_500_1000_V03':8426., 'QCD_1000_inf_V03':204., 'PhotonA_V04':1.,  'SinglePhotonB_V04':1., 'SinglePhotonC_V04':1., 'PhotonParkedD_V10':1.}
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

Data = ROOT.TH1F( "data", "data", MinMax[0], MinMax[1], MinMax[2] )

i=0#counting variable
for variable in Names:
	status = "default"
	print "******************************************************************"
	print "looping over: "+path+variable+IDVersion
	#if variable == "ZGammaNuNu_V03":
		#print "skipping ZGammaNuNu"
		#print "******************************************************************"
		#i+=1
		#continue
	if variable =="PhotonA_V04" or variable =="SinglePhotonB_V04" or variable =="SinglePhotonC_V04" or variable =="PhotonParkedD_V10":
		print "idetified real data"
		status = "data"
		weight = 1.
		print "status set to "+status # filter simulated data
	else:
		print "identified simulated data"
		status = "sim"
		weight = Lint/Lsim[variable]
		print "status set to "+status
	tree = FileList[variable].Get("myTree")#Inputtree
	testHis = ROOT.TH1F( variable, variable, MinMax[0], MinMax[1], MinMax[2]  )
	testHis.SetLineWidth(1)
	stop=0
	for event in tree:
		if isSignal(event)!="GT":
			continue
		if stop==10000 and BreakFill:
			print "breaking loop..."
			break
		stop+=1	
		if event.photons.size() ==0:
			continue
		if status=="sim":
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
				
		if status=="data":
			if event.photons.size() ==0:
				continue
			if plotvar=="PhotonPt":
				Data.Fill( event.photons[0].pt, weight )
			elif plotvar=="PhotonEta":
				Data.Fill( event.photons[0].eta, weight )
			elif plotvar=="PhotonPhi":
				Data.Fill( event.photons[0].phi, weight )
			elif plotvar=="Ht":
				Data.Fill( event.ht, weight )
			elif plotvar=="Met":
				Data.Fill( event.met, weight )
		
	
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
		
	
	if i!=8 and status=="sim":
		stack.Add(testHis)
		print "Added "+variable+IDVersion+" to stack"
	print 'weight is '+str(weight)+' times weight from event'
	if status!="data":
		print "Integral is: "+str(testHis.Integral())
	else:
		print "Integral is: "+str(Data.Integral())
	if i!=8 and status=="sim":
		integralGes+=testHis.Integral()
	TFileStack.cd()
	testHis.Write(variable+plotvar)
	i+=1
	print "******************************************************************"

Canvas.cd()
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

	

print "Data integral is: "+str(Data.Integral())
print "gesammtes Sim-Integral zum Vergleich: "+str(integralGes)
print "Data is plotted"
print "******************************************************************"
print "looping over T5wg"
T5wg1 = ROOT.TFile(path+"T5wg_1000_175_tree.root")
T5wg2 = ROOT.TFile(path+"T5wg_1200_1025_tree.root")
T5wg1tree = T5wg1.Get("myTree")
T5wg2tree = T5wg2.Get("myTree")
HistT5wg1 = ROOT.TH1F( "T5wg1", "T5wg1", MinMax[0], MinMax[1], MinMax[2]  )
HistT5wg2 = ROOT.TH1F( "T5wg2", "T5wg2", MinMax[0], MinMax[1], MinMax[2]  )
sigwg1 = 0.0243547
sigwg2 = 0.00440078
GenHist = T5wg1.Get("nGen")
LT5wg1 = GenHist.GetEntries()/sigwg1
GenHist = T5wg2.Get("nGen")
LT5wg2 = GenHist.GetEntries()/sigwg2


weight = Lint/LT5wg1
for event in T5wg1tree:		
	if event.photons.size() ==0:
		continue
	if plotvar=="PhotonPt":
		HistT5wg1.Fill( event.photons[0].pt, weight )
	elif plotvar=="PhotonEta":
		HistT5wg1.Fill( event.photons[0].eta, weight )
	elif plotvar=="PhotonPhi":
		HistT5wg1.Fill( event.photons[0].phi, weight )
	elif plotvar=="Ht":
		HistT5wg1.Fill( event.ht, weight )
	elif plotvar=="Met":
		HistT5wg1.Fill( event.met, weight )
HistT5wg1.Draw()
ROOT.gPad.SaveAs(homePath+"T5wg1"+plotvar+".pdf")
		

weight = Lint/LT5wg2
for event in T5wg2tree:		
	if event.photons.size() ==0:
		continue
	if plotvar=="PhotonPt":
		HistT5wg2.Fill( event.photons[0].pt, weight )
	elif plotvar=="PhotonEta":
		HistT5wg2.Fill( event.photons[0].eta, weight )
	elif plotvar=="PhotonPhi":
		HistT5wg2.Fill( event.photons[0].phi, weight )
	elif plotvar=="Ht":
		HistT5wg2.Fill( event.ht, weight )
	elif plotvar=="Met":
		HistT5wg2.Fill( event.met, weight )
HistT5wg2.Draw()
ROOT.gPad.SaveAs(homePath+"T5wg2"+plotvar+".pdf")
	


print "******************************************************************"	
L.AddEntry(Data, "Data", "lep")
Data.SetFillStyle(0)
Data.SetLineColor(ROOT.kBlack)
Data.SetLineWidth(2)
Data.SetMarkerStyle(20)
Data.Draw()


ROOT.gPad.SaveAs(homePath+plotvar+"/"+"ChainedData"+plotvar+".pdf")


stack.SetMinimum( MinMax[3] )
stack.SetMaximum( MinMax[4] )
stack.Draw()
stack.SetTitle(Title[0])
stack.GetXaxis().SetTitle(Title[1])
stack.GetYaxis().SetTitle(Title[2])
stack.GetXaxis().SetTitleOffset(1)
stack.GetYaxis().SetTitleOffset(1)

ROOT.gPad.SaveAs(homePath+plotvar+"/"+"Background"+plotvar+".pdf")




#stack.Draw("")
"""
testHis.SetMinimum( MinMax[3] )
testHis.SetMaximum( MinMax[4] )
testHis.Draw("samePE")
"""
HistT5wg1.SetLineColor(ROOT.kGreen)
HistT5wg1.SetMinimum( MinMax[3] )
HistT5wg1.SetMaximum( MinMax[4] )
HistT5wg1.Draw("same")
L.AddEntry(HistT5wg1, "T5wg_1000_175", "l")
HistT5wg2.SetLineColor(ROOT.kRed)
HistT5wg2.SetMinimum( MinMax[3] )
HistT5wg2.SetMaximum( MinMax[4] )
HistT5wg2.Draw("same")
Data.Draw("same PEX0")
L.AddEntry(HistT5wg2, "T5wg_1200_1025", "l")
L.Draw()
#ROOT.gPad.Update()
#ROOT.gPad.RedrawAxis()

#if not BreakFill:
#ROOT.gPad.SaveAs(homePath+"Stack"+plotvar+".pdf")
	
	
#if BreakFill and PrintBreak:
#	ROOT.gPad.SaveAs(homePath+"Stack"+plotvar+"Break.pdf")


TFileStack.cd()
HistT5wg2.Write("T5wg2"+plotvar)
HistT5wg1.Write("T5wg1"+plotvar)
Data.Write("Data"+plotvar)
