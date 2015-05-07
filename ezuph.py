import ROOT
from treeFunctions import *
ROOT.gSystem.Load("libTreeObjects.so")

file = ROOT.TFile("~/singlePhoton/TreeWriter/test.root")
tree = file.Get("myTree")


i=0
AnzE=0
AnzEm=0
AnzP=0
AnzPm=0
doublematch=0.
result=0.
for event in tree:
   if event.photons.size() >0:
      AnzP+=1
      if event.photons[0].genPhoton:
         AnzPm+=1
   if event.electrons.size() >0:
      AnzE+=1
      if event.electrons[0].genElectron:
         AnzEm+=1
         if event.electrons[0].genPhoton:
            doublematch+=1
   i=i+1

print 'AnzEm',AnzEm
print 'doublematch',doublematch
result=doublematch/AnzEm
print 'es sind',(result*100.),'% der Elektronen doppelt gematcht'

"""
for variable in ["met", "photons[0].pt", "photons[0].eta", "ht"]:
	#x=1-(1-0.00194)*(1-((event.electrons[0].pt/14.1)+1)^(-4.9))*(1-0.14*exp(-0.296*event.nTracksPV))*(1-0.000315*event.nVertex)
	h=createHistoFromTree(tree, variable, "1-(1-0.00194)*(1-((electrons[0].pt/14.1)+1)^(-4.9))*(1-0.14*exp(-0.296*nTracksPV))*(1-0.000315*nVertex)")
	#print x
	h.Draw()
	ROOT.gPad.SaveAs(variable+".pdf")
"""	
	

