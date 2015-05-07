import ROOT
ROOT.gSystem.Load("libTreeObjects.so")

file = ROOT.TFile("../singlePhoton/TreeWriter/test.root")
tree = file.Get("myTree")



h = ROOT.TH1F( "test", "T5wg;E_{T}^{miss}(GeV);Events", 100, 0, 2000 )
h2 = ROOT.TH1F( "test2", "test", 100, 0, 2000 )
h3 = ROOT.TH1F( "test3", "test", 100, 0, 2000 )
h4 = ROOT.TH1F( "test4", "test", 100, 0, 2000 )

h.SetLineColor(ROOT.kBlack)
h2.SetLineColor(ROOT.kRed)
h3.SetLineColor(ROOT.kGreen+9)
h4.SetLineColor(ROOT.kBlue)

for event in tree:
   h.Fill( event.met )
   if event.photons.size() >0 and event.photons[0].pt>40 and event.met > 100:
      h2.Fill( event.met )
   if event.photons.size() >0 and event.photons[0].pt>80 and event.ht > 500: 
      h3.Fill( event.met )
   if event.photons.size() >0 and event.photons[0].pt>140:
      h4.Fill( event.met )
   # h.Fill( event.jets[0].pt, event.weight )
   # h.Fill( event.metSig, event,weight )

h.Draw()
h2.Draw("same")
h3.Draw("same")
h4.Draw("same")

L = ROOT.TLegend(.6,.6,.9,.9)
L.AddEntry(h, "Inclusive", "L")
L.AddEntry(h2, "pt>40 Met>100", "L")
L.AddEntry(h3, "pt>80 ht>500", "L")
L.AddEntry(h4, "pt>140", "L")
L.Draw()
ROOT.gPad.SaveAs("test.pdf")

h5 = ROOT.TH1F( "test5", "Met bei Zwei Photonen;Anzahl;Events", 30, 1.5, 2.5)
ZweiPhotonenInclusive = ROOT.TH1F( "test6", "Anzahl Photonen pro event;Anzahl;Events", 20, 0, 2 )
ZweiPhotonenJohannes = ROOT.TH1F( "test7", "Anzahl der Photonen pro event;Anzahl;Events", 20, 0, 2 )
ZweiPhotonenKnut = ROOT.TH1F( "test8", "Anzahl der Photonen pro event;Anzahl;Events", 20, 0, 2 )
ZweiPhotonenNiklas = ROOT.TH1F( "test9", "Anzahl der Photonen pro event;Anzahl;Events", 20, 0, 2 )

ZweiPhotonenInclusive.SetLineColor(ROOT.kBlack)
ZweiPhotonenJohannes.SetLineColor(ROOT.kRed)
ZweiPhotonenKnut.SetLineColor(ROOT.kGreen+9)
ZweiPhotonenNiklas.SetLineColor(ROOT.kBlue)

for event in tree:
   if event.photons.size() >1:
      #ZweiPhotonenInclusive.Fill( event.met )
      ZweiPhotonenInclusive.Fill( event.photons.size())
   if event.photons.size() >1 and event.photons[0].pt>40 and event.met > 100:
      #ZweiPhotonenJohannes.Fill( event.met)
      ZweiPhotonenJohannes.Fill( event.photons.size())
   if event.photons.size() >1 and event.photons[0].pt>80 and event.ht > 500: 
      #ZweiPhotonenKnut.Fill( event.met )
      ZweiPhotonenKnut.Fill( event.photons.size() )
   if event.photons.size() >1 and event.photons[0].pt>140:
      #ZweiPhotonenNiklas.Fill( event.met )
      ZweiPhotonenNiklas.Fill( event.photons.size() )
      
ZweiPhotonenInclusive.Draw()
ZweiPhotonenJohannes.Draw("SAME")
ZweiPhotonenKnut.Draw("SAME")
ZweiPhotonenNiklas.Draw("SAME")

ROOT.gPad.SaveAs("VglZweiPhotonenAnzahl.pdf")

for event in tree:
	h5.Fill (event.photons.size())
	
h5.Draw()

ROOT.gPad.SaveAs("Photonen.pdf")

#raw_input()

