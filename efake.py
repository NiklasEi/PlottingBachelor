import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")
e=2.7182818284590452353602874713526624977572470937


file = ROOT.TFile("/user/eicker/V02/SinglePhotonB_V04.niklas02_tree.root")#Inputfile
tree = file.Get("myTree")#Inputtree

Photonenmet = ROOT.TH1F( "Photonen", "SinglePhotonB;E_{T}^{miss}(GeV);Events", 25, 0, 500 )#define histogramms
EUntermet = ROOT.TH1F( "EUnter", "SinglePhotonB;E_{T}^{miss}(GeV);Events", 25, 0, 500 )
Photonenmet.SetLineColor(ROOT.kBlack)
EUntermet.SetLineColor(ROOT.kRed)
Photonenmet.GetYaxis().SetRangeUser( 0.1, 10000 )

Photonenht = ROOT.TH1F( "Photonenht", "SinglePhotonB;ht(GeV);Events", 50, 0, 1000 )#define histogramms
EUnterht = ROOT.TH1F( "EUnterht", "SinglePhotonB;ht(GeV);Events", 50, 0, 1000 )
Photonenht.SetLineColor(ROOT.kBlack)
EUnterht.SetLineColor(ROOT.kRed)
Photonenht.GetYaxis().SetRangeUser( 0.01, 9000 )

weight = 0.
meanweight=0.
i=0

for event in tree:
	if event.photons.size() >0:
		Photonenmet.Fill ( event.met )
	if event.Elektrons.size() >0:
		weight = (1.-(1.-0.00194)*(1.-pow((event.Elektrons[0].pt/14.1)+1.,-4.9))*(1.-0.14*pow(e,(-0.296*event.nTracksPV)))*(1.-0.000315*event.nVertex))
		#print weight
		EUntermet.Fill (event.met, weight )


Photonenmet.Draw("P")
#Photonenmet.Draw("same")
EUntermet.Draw("same")

L = ROOT.TLegend(.55,.7,.9,.9)
L.AddEntry(Photonenmet, "Photonen", "P")
L.AddEntry(EUntermet, "Elektronen Untergrund", "L")
L.Draw()

ROOT.gPad.SaveAs("SignalMet.pdf")

Photonenmet.Draw()
ROOT.gPad.SaveAs("PhotonenMet.pdf")

EUntermet.Draw()
ROOT.gPad.SaveAs("EUnterMet.pdf")


for event in tree:
	if event.photons.size() >0:
		Photonenht.Fill ( event.ht )
	if event.Elektrons.size() >0:
		weight = (1. - 0.993 * (1. - pow(event.Elektrons[0].pt / 2.9 + 1., -2.4)) * (1. - 0.23 * pow(e,(-0.2777 * event.nTracksPV)))* (1. - 5.66e-4 * event.nVertex))
		#print weight
		EUnterht.Fill (event.ht, weight )
		i+=1
		meanweight+=weight
		#(1. - 0.993 * (1. - std::pow(photons[0].pt / 2.9 + 1., -2.4)) * (1. - 0.23 * std::exp(-0.2777 * nTracksPV))* (1. - 5.66e-4 * nVertex))
        #(1.-(1.-0.00194)*(1.-pow((event.Elektrons[0].pt/14.1)+1.,-4.9))*(1.-0.14*pow(e,(-0.296*event.nTracksPV)))*(1.-0.000315*event.nVertex))
        
        
meanweight=meanweight/i
print meanweight
Photonenht.Draw("P")
#Photonenht.Draw("same")
EUnterht.Draw("same")

L1 = ROOT.TLegend(.6,.75,.9,.9)
L1.AddEntry(Photonenht, "Photonen", "P")
L1.AddEntry(EUnterht, "Elektronen Untergrund", "L")
L1.Draw()

ROOT.gPad.SaveAs("SignalHt.pdf")

Photonenht.Draw()
ROOT.gPad.SaveAs("PhotonenHt.pdf")

EUnterht.Draw()
ROOT.gPad.SaveAs("EUnterHt.pdf")


"""
for variable in ["met", "photons[0].pt", "photons[0].eta", "ht"]:
	#h1=createHistoFromTree( tree, 
	h=createHistoFromTree(tree, variable, "1-(1-0.00194)*(1-((electrons[0].pt/14.1)+1)^(-4.9))*(1-0.14*exp(-0.296*nTracksPV))*(1-0.000315*nVertex)")
	#h1.Draw()
	h.Draw()
	ROOT.gPad.SaveAs("Hinter/"+variable+".pdf")
"""
