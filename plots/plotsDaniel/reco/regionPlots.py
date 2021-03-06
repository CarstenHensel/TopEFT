#!/usr/bin/env python
''' Analysis script for standard plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools

from math                         import sqrt, cos, sin, pi, log
from RootTools.core.standard      import *
from TopEFT.Tools.user            import plot_directory
from TopEFT.Tools.helpers         import deltaPhi, getObjDict, getVarValue
from TopEFT.Tools.objectSelection import getFilterCut
from TopEFT.Tools.cutInterpreter  import cutInterpreter

from TopEFT.Tools.user            import plot_directory

#ROOT.gROOT.SetBatch(True)
ROOT.gROOT.LoadMacro('$CMSSW_BASE/src/TopEFT/Tools/scripts/tdrstyle.C')
ROOT.setTDRStyle()

def calcAMS(s, b):
    return sqrt(2*((s+b)*log(1+s/b)-s))

postProcessing_directory = "TopEFT_PP_v10/trilep/"
from TopEFT.samples.cmgTuples_Summer16_mAODv2_postProcessed import *

signal  = [ TTZtoLLNuNu ]
bkg     = [ TTW, WZ,TZQ, TTX, rare ]

presel = "nlep==3&&lep_pt[0]>40&&lep_pt[1]>20&&lep_pt[2]>10&&Z_mass>0&&abs(Z_mass-91.2)<10"

channels = {'eee':'nGoodElectrons==3','eemu':'nGoodElectrons==2&&nGoodMuons==1','emumu':'nGoodElectrons==1&&nGoodMuons==2','mumumu':'nGoodElectrons==0&&nGoodMuons==3', 'all':'(1)'}
channels = {'all':'(1)'}


#btag = "nBTagDeepCSV"
#weight = "weight*35.9*reweightDeepCSV_SF"

btag = "nBTag"
weight = "weight*35.9*reweightBTagCSVv2_SF_b_Up"


regions = [\
            "nJetSelected==2&&%s==0"%btag,
            "nJetSelected==3&&%s==0"%btag,
            "nJetSelected>=4&&%s==0"%btag,
            "nJetSelected==2&&%s==1"%btag,
            "nJetSelected==3&&%s==1"%btag,
            "nJetSelected>=4&&%s==1"%btag,
            "nJetSelected==2&&%s>=2"%btag,
            "nJetSelected==3&&%s>=2"%btag,
            "nJetSelected>=4&&%s>=2"%btag,
            ]

nReg = len(regions)

#hists = []
#for sample in signal + bkg:
#    sample.hist = ROOT.TH1F(sample.name, "", nReg, 0, nReg)

h_sig   = ROOT.TH1F("signal", "", nReg, 0, nReg)
h_bkg   = ROOT.TH1F("bkg", "", nReg, 0, nReg)
#h_ratio = ROOT.TH1F("s/b", "", nReg, 0, nReg)

maxFOM = 0

for c in channels:
    print c
    for sample in signal + bkg:
        sample.hist = ROOT.TH1F(sample.name, "", nReg, 0, nReg)
        sample.hist.SetFillColor(sample.color)

    h_sig   = ROOT.TH1F("signal", "", nReg, 0, nReg)
    h_bkg   = ROOT.TH1F("bkg", "", nReg, 0, nReg)
    h_ratio = ROOT.TH1F("s/b", "", nReg, 0, nReg)
    h_ratio.Sumw2()

    for i, sample in enumerate(signal + bkg):
        print sample.name
        for j, r in enumerate(regions):
            val = sample.getYieldFromDraw('&&'.join([presel,channels[c],r]), weight)
            print j, val
            sample.hist.SetBinContent(j+1, val["val"])
            sample.hist.SetBinError(j+1, val["sigma"])
        
        
    h_sig.Add(TTZtoLLNuNu.hist)
    for s in bkg:
        h_bkg.Add(s.hist)

    for j, r in enumerate(regions):
        y_sig = h_sig.GetBinContent(j+1)
        y_bkg = h_bkg.GetBinContent(j+1)
        FOM = calcAMS(y_sig, y_bkg)#y_sig/sqrt(y_bkg+(0.1*y_bkg)**2)
        print FOM
        if FOM > maxFOM: maxFOM = FOM
        h_ratio.SetBinContent(j+1, FOM)
    #h_ratio = h_sig.Clone()
    #h_ratio.Divide(h_bkg)
    h_ratio.SetMaximum(20.0)
    h_ratio.SetMinimum(0.5)


    stack = ROOT.THStack('h_Stack','Stack')
    for s in reversed(signal+bkg):
        stack.Add(s.hist)
    
    print "Highest AMS value: %s"%maxFOM

    can = ROOT.TCanvas("can","can", 700,700)
    pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
    pad1.SetLeftMargin(0.1)
    pad1.SetBottomMargin(0.02)
    pad1.SetTopMargin(0.08)
    pad1.Draw()
    pad1.SetLogy()
    pad1.cd()
    stack.Draw("hist")
    stack.SetMaximum(10000)
    stack.SetMinimum(0.95)
    stack.GetXaxis().SetLabelOffset(10)

    leg2 = ROOT.TLegend(0.70,0.86-0.04*len(signal+bkg),0.98,0.86)
    leg2.SetFillColor(ROOT.kWhite)
    leg2.SetShadowColor(ROOT.kWhite)
    leg2.SetBorderSize(0)
    leg2.SetTextSize(0.035)
    for s in signal + bkg:
        leg2.AddEntry(s.hist,s.texName, 'f')
    leg2.Draw()

    can.cd()
    pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
    pad2.SetLeftMargin(0.1)
    pad2.SetBottomMargin(0.3)
    pad2.SetTopMargin(0.02)
    pad2.SetLogy()
    pad2.Draw()
    pad2.cd()

    h_ratio.GetXaxis().SetTitle("region")
    h_ratio.GetYaxis().SetTitle("FOM")

    h_ratio.GetXaxis().SetTitleSize(0.13)
    h_ratio.GetXaxis().SetLabelSize(0.11)
    h_ratio.GetXaxis().SetLabelOffset(0.02)
    h_ratio.GetYaxis().SetTitleSize(0.145)
    h_ratio.GetYaxis().SetLabelSize(0.13)
    h_ratio.GetYaxis().SetTitleOffset(0.32)
    h_ratio.GetYaxis().SetNdivisions(506)
    h_ratio.Draw("e1p")   
    
    can.cd()
    extraText = "Preliminary"
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11) # align right
    latex1.DrawLatex(0.10,0.955,'CMS #bf{#it{'+extraText+'}}')
    latex1.DrawLatex(0.72,0.955,"#bf{35.9fb^{-1}} (13TeV)")
    
    plot_dir = os.path.join(plot_directory, "regionPlot", "ttZ", "btagging", c)
    if not os.path.isdir(plot_dir): os.makedirs(plot_dir)
    for f in ['.png','.pdf','.root']:
        can.Print(plot_dir+"/regions_%s_reweightBTag_b_Up"%btag+f)
