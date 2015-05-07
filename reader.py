import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")

#file = ROOT.TFile("/user/eicker/GJets_100_200_V09.niklas01_tree.root")
file = ROOT.TFile("/user/eicker/ZGammaNuNu_V03.niklas01_tree.root")
tree = file.Get("myTree")

filePP = ROOT.TFile("/user/eicker/PhotonParkedD_V10.niklas01_tree.root")
treePP = filePP.Get("myTree")

PhotonPt = ROOT.TH1F( "PhotonPt", "GJets_100_200;E_{T}^{miss}(GeV);Events", 100, 0, 2000 )
Ht = ROOT.TH1F( "Ht", "PhotonParkedD;Ht(GeV);Events", 100, 0, 2000 )
ElektronPt = ROOT.TH1F( "ElektronPt", "", 100, 0, 2000 )

for variable in ["met", "photons[0].pt", "photons[0].eta", "ht"]:
	h=createHistoFromTree(tree, variable)
	h.Draw()
	ROOT.gPad.SaveAs(variable+".pdf")
i=0
for event in tree:
   if i>500000: 
      break
   if event.photons.size() >0 and not event.photons[0].pixelseed:
      PhotonPt.Fill ( event.met )
   if event.photons.size() >0 and event.photons[0].pixelseed:
      ElektronPt.Fill ( event.met )
   i=i+1

PhotonPt.Draw()
ElektronPt.Draw("same")
ROOT.gPad.SaveAs("PhotonPt.pdf")

i=0
for event in treePP:
   if i>50000:
      break
   Ht.Fill ( event.ht )
   i=i+1

Ht.Draw()
ROOT.gPad.SaveAs("Ht.pdf")



