import ROOT
import sys
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
#ROOT.TH1.SetDefaultSumw2()
e=2.7182818284590452353602874713526624977572470937

simulated = ROOT.TChain("myTree")
data = ROOT.TChain("myTree")

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
path ="/user/eicker/test/"
IDVersion =".Test_tree.root" #Version of the trees
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
nBinsHt = 70
nBinsPt = 50

HistDataHtPtGT = ROOT.TH2F( "dataHtPtGT", "dataHtPtGT", nBinsPt, 100, 800, nBinsHt, 0, 1600)
HistDataHtPtGT.SetTitle(Title[0]+" #gamma_{tight}")
HistDataHtPtGT.GetXaxis().SetTitle("Pt")
HistDataHtPtGT.GetYaxis().SetTitle("Ht")

HistDataHtPtGL = ROOT.TH2F( "dataHtPtGL", "dataHtPtGL", nBinsPt, 100, 800, nBinsHt, 0, 1600)
HistDataHtPtGL.SetTitle(Title[0]+" #gamma_{loose}")
HistDataHtPtGL.GetXaxis().SetTitle("Pt")
HistDataHtPtGL.GetYaxis().SetTitle("Ht")

HistDataHtPtWeight = ROOT.TH2F( "dataHtPtWeight", "dataHtPtWeight", nBinsPt, 100, 800, nBinsHt, 0, 1600)
HistDataHtPtWeight.GetXaxis().SetTitle("Pt")
HistDataHtPtWeight.GetYaxis().SetTitle("Ht")
HistDataHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose}")

HistIsoGT = ROOT.TH2F( "IsoGT", "IsoGT", 100, 0, 30, 100, 0, 40)
HistIsoGT.SetTitle(Title[0]+" #gamma_{tight}")
HistIsoGT.GetXaxis().SetTitle("I_{#pm}")
HistIsoGT.GetYaxis().SetTitle("I_{0}")

HistIsoGL = ROOT.TH2F( "IsoGL", "IsoGL", 100, 0, 30, 100, 0, 40)
HistIsoGL.SetTitle(Title[0]+" #gamma_{loose}")
HistIsoGL.GetXaxis().SetTitle("I_{#pm}")
HistIsoGL.GetYaxis().SetTitle("I_{0}")

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
		HistDataHtPtGT.Fill(event.photons[0].pt, event.ht)
		HistIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso)
	if event.jetphotons.size()>0:
		HistDataHtPtGL.Fill(event.jetphotons[0].pt, event.ht)
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

HistDataHtPtGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"GLHtPtData.pdf")

HistDataHtPtGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"GTHtPtData.pdf")

ROOT.gStyle.SetOptLogz(0)
Canvas2 = ROOT.TCanvas ("canvas2", "canvas2")
HistDataHtPtWeight.Draw("colz")
ROOT.gPad.SaveAs(homePath+"GtGlRatioHtPtData.pdf")
Styles.tdrStyle2D()
Canvas1.cd()

HistIsoGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"GTIsoData.pdf")

HistIsoGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"GLIsoData.pdf")

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
ROOT.gPad.SaveAs(homePath+"GtGlRatioMetData.pdf")

print "*********************** simulated data ***************************"


HistSimHtPtGT = ROOT.TH2F( "SimHtPtGT", "SimHtPtGT", nBinsPt, 100, 800, nBinsHt, 0, 1600)
HistSimHtPtGT.SetTitle(Title[0]+" #gamma_{tight} simulated data")
HistSimHtPtGT.GetXaxis().SetTitle("Pt")
HistSimHtPtGT.GetYaxis().SetTitle("Ht")

HistSimHtPtGL = ROOT.TH2F( "SimHtPtGL", "SimHtPtGL", nBinsPt, 100, 800, nBinsHt, 0, 1600)
HistSimHtPtGL.SetTitle(Title[0]+" #gamma_{loose} simulated data")
HistSimHtPtGL.GetXaxis().SetTitle("Pt")
HistSimHtPtGL.GetYaxis().SetTitle("Ht")

HistSimHtPtWeight = ROOT.TH2F( "simHtPtWeight", "simHtPtWeight", nBinsPt, 100, 800, nBinsHt, 0, 1600)
HistSimHtPtWeight.GetXaxis().SetTitle("Pt")
HistSimHtPtWeight.GetYaxis().SetTitle("Ht")
HistSimHtPtWeight.SetTitle(Title[0]+" #gamma_{tight}/#gamma_{loose} simulated data")

HistSimIsoGT = ROOT.TH2F( "simIsoGT", "simIsoGT", 100, 0, 30, 100, 0, 40)
HistSimIsoGT.SetTitle(Title[0]+" #gamma_{tight} simulated data")
HistSimIsoGT.GetXaxis().SetTitle("I_{0}")
HistSimIsoGT.GetYaxis().SetTitle("I_{#pm}")

HistSimIsoGL = ROOT.TH2F( "simIsoGL", "simIsoGL", 100, 0, 30, 100, 0, 40)
HistSimIsoGL.SetTitle(Title[0]+" #gamma_{loose} simulated data")
HistSimIsoGL.GetXaxis().SetTitle("I_{0}")
HistSimIsoGL.GetYaxis().SetTitle("I_{#pm}")



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
		if BreakFill:
			stop+=1
			if stop==10000:
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
			HistSimHtPtGT.Fill(event.photons[0].pt, event.ht, weight*event.weight)
			HistSimIsoGT.Fill(event.photons[0].chargedIso, event.photons[0].neutralIso, weight*event.weight )
		if event.jetphotons.size()>0:
			HistSimHtPtGL.Fill(event.jetphotons[0].pt, event.ht, weight*event.weight)
			HistSimIsoGL.Fill(event.jetphotons[0].chargedIso, event.jetphotons[0].neutralIso, weight*event.weight )

	print "******************************************************************"



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
		"""
		if HistSimHtPtWeight.GetBinContent(pt, ht)>50:
			print "Bin Nr. "+str(pt)+"/"+str(ht)+" hat wert: "+str(HistSimHtPtWeight.GetBinContent(pt, ht))+" bei GL = "+str(GLBin)+" und GT = "+str(GTBin)+" Bin set zu 1 "
			HistSimHtPtWeight.SetBinContent(pt, ht, 1)
		"""
print str(count)+" out of "+str(nBinsHt*nBinsPt)+" Bins had to be set to zero because GLBin was empty"
print "*************** finished setting Bincontents *********************"

HistSimHtPtGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLHtPtSim.pdf")

HistSimHtPtGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTHtPtSim.pdf")

Canvas2.cd()
HistSimHtPtWeight.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GtGlRatioHtPtSim.pdf")
Canvas1.cd()

HistSimIsoGT.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GTIsoSim.pdf")

HistSimIsoGL.Draw("colz")
ROOT.gPad.SaveAs(homePath+"Sim/"+"GLIsoSim.pdf")


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
