import ROOT
import os
import ctypes
import shutil
from functools                      import partial

from RootTools.core.standard        import *

## 2016
data_directory = '/afs/hephy.at/data/dspitzbart02/cmgTuples/'
postProcessing_directory = "TopEFT_PP_2016_mva_v21/trilep/"
from TopEFT.samples.cmgTuples_Data25ns_80X_07Aug17_postProcessed import *
postProcessing_directory = "TopEFT_PP_2016_mva_v21/trilep/"
from TopEFT.samples.cmgTuples_Summer16_mAODv2_postProcessed import *

## 2017
data_directory = '/afs/hephy.at/data/dspitzbart02/cmgTuples/'
postProcessing_directory = "TopEFT_PP_2017_mva_v21/trilep/"
from TopEFT.samples.cmgTuples_Data25ns_94X_Run2017_postProcessed import *
postProcessing_directory = "TopEFT_PP_2017_mva_v21/trilep/"
from TopEFT.samples.cmgTuples_Fall17_94X_mAODv2_postProcessed import *


from TopEFT.Tools.user              import combineReleaseLocation, analysis_results, plot_directory
from TopEFT.Tools.niceColorPalette  import niceColorPalette, redColorPalette, newColorPalette
from TopEFT.Tools.helpers           import getCouplingFromName
from TopEFT.Analysis.Setup          import Setup
from TopEFT.Tools.resultsDB             import resultsDB
from TopEFT.Tools.u_float               import u_float

from TopEFT.samples.gen_fwlite_benchmarks import *


# Plot style
ROOT.gROOT.LoadMacro('$CMSSW_BASE/src/TopEFT/Tools/scripts/tdrstyle.C')
ROOT.setTDRStyle()
#niceColorPalette()
ROOT.gStyle.SetNumberContours(255)
#ROOT.gStyle.SetPalette(ROOT.kCherry)#, ctypes.c_int(112), 0.3)#, *nullptr, 0.3)
newColorPalette()

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--plot_directory',  action='store',         default='NLL_plots')
argParser.add_argument('--useBestFit',      action='store_true',    help="Use best fit value? Default is r=1")
argParser.add_argument('--smooth',          action='store_true',    help="Use histogram smoothing? Potentially dangerous (oversmoothing)!")
argParser.add_argument('--model',           action='store',         choices=["ewkDM", "dim6top_LO"], help="Which model?")
argParser.add_argument('--plane',           action='store',         choices=["currents", "dipoles"], default = "current", help="Current of dipole plane?")
argParser.add_argument("--useXSec",         action='store_true',    help="Use the x-sec information?")
argParser.add_argument("--useShape",        action='store_true',    help="Use the shape information?")
argParser.add_argument("--prefit",          action='store_true',    help="Use pre-fit NLL?")
argParser.add_argument("--expected",        action='store_true',    help="Use expected results?")
argParser.add_argument("--unblinded",       action='store_true',    help="Use unblinded results?")
argParser.add_argument("--preliminary",     action='store_true',    help="Use unblinded results?")
argParser.add_argument("--year",            action='store',         default=2016, choices = [ '2016', '2017', '20167' ], help='Which year?')
argParser.add_argument("--combined",        action='store_true',    help="Use combined results?")
argParser.add_argument("--sigma",           action='store_true',    help="Use sigma levels?")
args = argParser.parse_args()

year = int(args.year)

setup = Setup(year)

postFix = ""#"_fine_YR1"

def Eval(obj, x, params):
    return obj.Eval(x[0])

def toGraph2D(name,title,length,x,y,z):
    result = ROOT.TGraph2D(length)
    debug = ROOT.TGraph()
    result.SetName(name)
    result.SetTitle(title)
    for i in range(length):
        result.SetPoint(i, x[i], y[i], z[i])
        debug.SetPoint(i, x[i], y[i])
    c = ROOT.TCanvas()
    result.Draw()
    debug.Draw()
    del c
    #res = ROOT.TGraphDelaunay(result)
    return result,debug


# do the same stuff as in the analysis part

subDir = ''
baseDir = os.path.join(analysis_results, subDir)

cardDir = "regionsE_%s"%(year) if not args.combined else "regionsE_COMBINED"
if args.useXSec:
    cardDir += "_xsec"
if args.useShape:
    cardDir += "_shape"
exp = "_expected" if args.expected else ''
cardDir += "_lowUnc%s_SRandCR"%exp

#regionsE_COMBINED_xsec_shape_lowUnc_expected_SRandCR
#regionsE_2017_xsec_shape_lowUnc_expected_SRandCR

#/afs/hephy.at/data/dspitzbart01/TopEFT/results/cardFiles/regionsE_2016_xsec_shape_lowUnc_WZreweight_SRandCR/

limitDir    = os.path.join(baseDir, 'cardFiles', cardDir, subDir, '_'.join([args.model, args.plane]))

print limitDir
resDB = resultsDB(limitDir+'/results.sq', "results", setup.resultsColumns)

fitKey = "dNLL_postfit_r1" if not args.useBestFit else "dNLL_bestfit"


# get the absolute post fit NLL value of pure ttZ
if args.model == "ewkDM":
    ttZ_res = resDB.getDicts({"signal":ewkDM_central.name})[-1]
elif args.model == "dim6top_LO":
    ttZ_res = resDB.getDicts({"signal":dim6top_central.name})[-1]

if args.prefit:
    ttZ_NLL_abs = float(ttZ_res["NLL_prefit"])
else:
    ttZ_NLL_abs = float(ttZ_res["NLL_prefit"]) + float(ttZ_res[fitKey])

print "Max Likelihood ttZ SM"
print "{:10.2f}".format(ttZ_NLL_abs)

if args.model == "ewkDM":
    if args.plane == "currents":
        signals = [ ewkDM_central ] + [ x for x in ewkDM_currents ]
        #signals = [ x for x in ewkDM_currents ]
        x_var = 'DC1V'
        y_var = 'DC1A'
        #x_shift = 0.
        #y_shift = 0.
        x_shift = 0.24
        y_shift = -0.60
    
    elif args.plane == "dipoles":
        signals = [ ewkDM_central ] + [ x for x in ewkDM_dipoles ]
        x_var = 'DC2V'
        y_var = 'DC2A'
        x_shift = 0.
        y_shift = 0.

elif args.model == "dim6top_LO":
    if args.plane == "currents":
        signals = [ dim6top_central ] + [ x for x in dim6top_currents ]
        x_var = 'cpQM'
        y_var = 'cpt'
        x_shift = 0.
        y_shift = 0.
    
    elif args.plane == "dipoles":
        signals = [ dim6top_central ] + [ x for x in dim6top_dipoles ]
        x_var = 'ctZ'
        y_var = 'ctZI'
        x_shift = 0.
        y_shift = 0.
    

print "Number of results", len(signals)

var1_values = []
var2_values = []

for s in signals:
    s.var1 = getCouplingFromName(s.name, x_var)
    s.var2 = getCouplingFromName(s.name, y_var)
    if s.var1 != 0.0 and (s.var1+x_shift) not in var1_values:
        var1_values.append(s.var1 + x_shift)
    if s.var2 != 0.0 and (s.var2+y_shift) not in var2_values:
        var2_values.append(s.var2 + y_shift)


var1_values = sorted(var1_values)
var2_values = sorted(var2_values)

x_min = var1_values[0] - (abs(var1_values[0]) - abs(var1_values[1])) / 2
x_max = var1_values[-1] + (abs(var1_values[-1]) - abs(var1_values[-2])) / 2
nbins_x = len(var1_values)
bin_size_x = (x_max - x_min) / nbins_x

y_min = var2_values[0] - (abs(var2_values[0]) - abs(var2_values[1])) / 2
y_max = var2_values[-1] + (abs(var2_values[-1]) - abs(var2_values[-2])) / 2
nbins_y = len(var2_values)
bin_size_y = (y_max - y_min) / nbins_y


x = []
y = []
z = []

res_dic = {}

print "Searching for bestfit point"

bestNLL = 9999.

SMPoint = ('SM', x_shift, y_shift)
bestFitPoint = ('SM', x_shift, y_shift)

missing = []

# scan all results to find best fit
for i,s in enumerate(signals):
    if resDB.contains({"signal":s.name}):
        res = resDB.getDicts({"signal":s.name})[-1]
        #res = getResult(s)
        if type(res) == type({}):
            ttZ_NLL_abs_check = float(res["NLL_prefit"]) + float(res[fitKey])
            if ttZ_NLL_abs_check < ttZ_NLL_abs and ttZ_NLL_abs_check>0:
                ttZ_NLL_abs = ttZ_NLL_abs_check
                bestFitPoint = (s.name, s.var1 + x_shift, s.var2 + y_shift)
                #bestFitPoint_noShift = 
                print "Best NLL value", ttZ_NLL_abs_check
            #limit = float(res["NLL_prefit"]) + float(res[fitKey]) - ttZ_NLL_abs

    else:
        missing.append(s.name)

if args.expected: bestFitPoint = SMPoint

print "Best fit found for signal %s, %s, %s"%bestFitPoint
print
print "{:>10}{:>10}{:>10}".format(x_var, y_var, "2*dNLL")

zoom = False

for i,s in enumerate(signals):
    if resDB.contains({"signal":s.name}):
        res = resDB.getDicts({"signal":s.name})[-1]
        #res = getResult(s)
        print s.name
        if type(res) == type({}):
            if args.prefit:
                limit = float(res["NLL_prefit"]) - ttZ_NLL_abs
            else:
                limit = float(res["NLL_prefit"]) + float(res[fitKey]) - ttZ_NLL_abs

            if limit >= 0:
                # good result
                nll_value = 2*limit
            elif limit > -0.1 and limit < 0:
                # catch rounding errors
                print limit
                nll_value = 0
            elif limit < -900:
                # if the fit failed, add a dummy value (these points should easily be excluded)
                nll_value = 100
            else:
                print limit
                print "No good result found for %s, results is %s"%(s.name, limit)
                continue
            
            # Add results
            print "{:10.2f}{:10.2f}{:10.2f}".format(s.var1+x_shift, s.var2+y_shift, nll_value)
            #if s.var2 + y_shift > -0.9 and s.var1+x_shift<1.2:# and s.var1+x_shift>-0.9 and s.var1+x_shift<0.9:
            if args.model == 'dim6top_LO' and args.plane == 'currents':
                if  ( s.var1 + x_shift > 37): continue
                if ( s.var1 + x_shift < -12): continue
                if ( s.var2 + y_shift > 18): continue
                if ( s.var2 + y_shift < -28): continue
            if args.model == 'dim6top_LO' and args.plane == 'dipoles' and zoom:
                if abs(s.var1)>1 or abs(s.var2)>1: continue
            
            if args.model == "ewkDM" and args.plane == 'currents':
                if (s.var2 + y_shift < -1.) : continue

            if True:
                z.append(nll_value)
                x.append(s.var1 + x_shift)
                y.append(s.var2 + y_shift)
                res_dic[(round(s.var1 + x_shift,2), round(s.var2 + y_shift,2))] = round(nll_value,3)
            #else:
            #    print "Omitting..."

        else:
            print "No results for %s found"%s.name


proc = "ttZ"

#print res_dic

multiplier = 3 #5??

a,debug = toGraph2D(proc, proc, len(x), x,y,z)#res_dic)
nxbins = max(1, min(500, nbins_x*multiplier))
nybins = max(1, min(500, nbins_y*multiplier))

print "Number of bins on x-axis: %s"%nxbins
print "Number of bins on y-axis: %s"%nybins

print "Best fit found for signal %s, %s, %s"%bestFitPoint
print

hist = a.GetHistogram().Clone()

#nxbins = 200
#nybins = 200

a.SetNpx(nxbins)
a.SetNpy(nybins)
hist = a.GetHistogram().Clone()


if x_var == "DC1V":
    hist.GetXaxis().SetTitle("C_{1,V}")
elif x_var == "DC2V":
    hist.GetXaxis().SetTitle("C_{2,V}")
elif x_var == "cpQM":
#    hist.GetXaxis().SetTitle("c_{#varphiQ}^{-} #equiv C_{#varphiq}^{1(33)}-C_{#varphiq}^{3(33)}")
    hist.GetXaxis().SetTitle("c_{#varphiQ}^{#font[122]{\55}} /#Lambda^{2} [1/TeV^{2}]")
elif x_var == "ctZ":
#    hist.GetXaxis().SetTitle("c_{tZ} #equiv Re{-s_{W}C_{uB}^{(33)}+c_{W}C_{uW}^{(33)}}")
    hist.GetXaxis().SetTitle("c_{tZ} /#Lambda^{2} [1/TeV^{2}]")

hist.GetXaxis().SetNdivisions(505)
if y_var == "DC1A":
    hist.GetYaxis().SetTitle("C_{1,A}")
elif y_var == "DC2A":
    hist.GetYaxis().SetTitle("C_{2,A}")
elif y_var == "cpt":
#    hist.GetYaxis().SetTitle("c_{#varphit} #equiv C_{#varphiu}^{(33)}")
    hist.GetYaxis().SetTitle("c_{#varphit} /#Lambda^{2} [1/TeV^{2}]")
elif y_var == "ctZI":
#    hist.GetYaxis().SetTitle("c_{tZ}^{[I]} #equiv Im{-s_{W}C_{uB}^{(33)}+c_{W}C_{uW}^{(33)}}")
    hist.GetYaxis().SetTitle("c_{tZ}^{[I]} /#Lambda^{2} [1/TeV^{2}]")

hist.GetXaxis().SetTitleOffset(1.10)
hist.GetYaxis().SetNdivisions(505)
hist.GetYaxis().SetTitleOffset(1.15)
#hist.GetZaxis().SetTitle("-2 #DeltalnL")
#hist.GetZaxis().SetTitle("q")
hist.GetZaxis().SetTitleOffset(1.0)
hist.SetStats(0)
if args.prefit:
    postFix += "_prefit"
if args.useXSec:
    postFix += "_useXSec"
if args.useShape:
    postFix += "_useShape"
if args.expected:
    postFix += "_expected"
if args.smooth:
    for i in range(2):
        hist.Smooth(1,"k5b")
    postFix += "_smooth"
if args.preliminary:
    postFix += "_preliminary"

cans = ROOT.TCanvas("can_%s"%proc,"",700,700)


## contours, either 1/2 sigma or 68/95% CL (2 d.o.f)
# https://stattrek.com/online-calculator/chi-square.aspx

if args.sigma:
    contours = {'ttZ': [1.515**2,2.486**2]} # 1/2 sigma levels
else:
    contours = {'ttZ': [2.28, 5.99]} # 68/95 % CL

drawContours = True
if drawContours:
    histsForCont = hist.Clone()
    c_contlist = ((ctypes.c_double)*(len(contours[proc])))(*contours[proc])
    histsForCont.SetContour(len(c_contlist),c_contlist)
    histsForCont.Draw("contzlist")
    cans.Update()
    conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    #cont_m2 = conts.At(0).Clone()
    #cont_m1 = conts.At(1).Clone()
    cont_p1 = conts.At(0).Clone()
    cont_p2 = conts.At(1).Clone()

pads = ROOT.TPad("pad_%s"%proc,"",0.,0.,1.,1.)
pads.SetRightMargin(0.20)
pads.SetLeftMargin(0.16)
pads.SetTopMargin(0.15)
if args.model == "ewkDM" and args.plane == "currents":
    pads.SetTopMargin(0.19)
pads.SetBottomMargin(0.15)
pads.Draw()
pads.cd()

hist.GetZaxis().SetRangeUser(0,4.95)
if zoom:
    hist.SetMaximum(1.95)
else:
    hist.SetMaximum(19.95) #19.95
hist.SetMinimum(0.)
#hist.GetZaxis().SetRangeUser(0,4.95)


hist.Draw("colz")
alpha = 0.5

if drawContours and not zoom:
    for conts in [cont_p2]:
        for cont in conts:
            cont.SetLineColor(ROOT.kBlack)
            cont.SetLineWidth(3)
            cont.SetLineStyle(2)
            cont.Draw("L same")
    for conts in [cont_p1]:
        for cont in conts:
            #cont.SetLineColor(ROOT.kBlue-6)
            cont.SetLineColor(ROOT.kBlack)
            cont.SetLineWidth(3)
            cont.Draw("L same")


if args.model == "ewkDM" and args.plane == "currents":

    inner = ROOT.TEllipse(0,0, 3*0.24, 0.8*0.6)
    

    outer_upper = ROOT.TF1("inner_upper", "[0]*(1-x**2/[1]**2)**(0.5)", hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax())
    inner_upper = ROOT.TF1("inner_upper", "[0]*(1-x**2/[1]**2)**(0.5)", -3*0.24, 3*0.24 )

    outer_lower = ROOT.TF1("inner_upper", "[0]*(1-x**2/[1]**2)**(0.5)", hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax() )
    inner_lower = ROOT.TF1("inner_lower", "[0]*(1-x**2/[1]**2)**(0.5)", -3*0.24, 3*0.24 )
    
    outer_upper.SetParameters(1.5*0.6, 5*0.24)
    inner_upper.SetParameters(0.8*0.6, 3*0.24)
    outer_lower.SetParameters(-1.5*0.6, 5*0.24)
    inner_lower.SetParameters(-0.8*0.6, 3*0.24)

    for l in [outer_upper,outer_lower]:
        l.SetLineStyle(5)
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kGray+1)
        l.Draw("same")

    for ell in [inner]:
        ell.SetFillColorAlpha(0,0)
        ell.SetFillStyle(1001)
        ell.SetLineColor(ROOT.kGray+1)
        ell.SetLineWidth(2)
        ell.SetLineStyle(5)
        ell.Draw("same")

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.035)
latex1.SetTextAlign(11)

if not args.unblinded:
    latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Simulation}}')
else:
    if args.preliminary:
        latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
    else:
        latex1.DrawLatex(0.16,0.96,'CMS')# #bf{#it{Preliminary}}')

if args.model == "ewkDM":
    latex1.DrawLatex(0.18,0.91,'#bf{Anomalous}')
    latex1.DrawLatex(0.18,0.87,'#bf{coupling model}')
else:
    latex1.DrawLatex(0.18,0.91,'#bf{SMEFT}')
#    latex1.DrawLatex(0.14,0.87,'#bf{model}')

latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.05)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.87, 0.87, '#bf{q}')

if args.combined:
    setup.lumi = 35900+41600

if not args.unblinded:
    latex1.DrawLatex(0.6,0.96,'#bf{%.1f fb^{-1} MC (13 TeV)}'%(setup.lumi/1e3))
else:
    latex1.DrawLatex(0.56,0.96,'#bf{%.1f fb^{-1} (13 TeV)}'%(setup.lumi/1e3))

SMpoint = ROOT.TGraph(1)
SMpoint.SetName("SMpoint")
BFpoint = ROOT.TGraph(1)
BFpoint.SetName("BFpoint")

print SMPoint[1], SMPoint[2], 1
SMpoint.SetPoint(0, SMPoint[1], SMPoint[2])
BFpoint.SetPoint(0, bestFitPoint[1], bestFitPoint[2])

SMpoint.SetMarkerStyle(34)
SMpoint.SetMarkerSize(2)
SMpoint.SetMarkerColor(ROOT.kRed+2)
BFpoint.SetMarkerStyle(33)
BFpoint.SetMarkerSize(2)
BFpoint.SetMarkerColor(ROOT.kBlue-6)

SMpoint.Draw("p same")
BFpoint.Draw("p same")

l1 = ROOT.TLine()
l1.SetLineColor(ROOT.kBlack)
l1.SetLineWidth(1)
l1.DrawLineNDC(0.16,0.80,0.16,0.95)
l1.DrawLineNDC(0.80,0.80,0.80,0.95)
l1.DrawLineNDC(0.16,0.95,0.80,0.95)

#if args.model == 'ewkDM' and args.plane == 'currents':
#    leg = ROOT.TLegend(0.44,0.82,0.60,0.94)
#else:
leg = ROOT.TLegend(0.44,0.86,0.60,0.94)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(0)
leg.SetTextSize(0.035)
try:
    if args.sigma:
        leg.AddEntry(cont_p2[0], '#bf{2#sigma}', 'l')
    else:
        leg.AddEntry(cont_p2[0], '#bf{95% CL}', 'l')
except:
    pass

if args.sigma:
    leg.AddEntry(cont_p1[0], '#bf{1#sigma}', 'l')
else:
    leg.AddEntry(cont_p1[0], '#bf{68% CL}', 'l')

leg.Draw()

if args.model == 'ewkDM' and args.plane == 'currents':
    leg3 = ROOT.TLegend(0.18,0.82,0.60,0.86)
    leg3.SetFillColor(ROOT.kWhite)
    leg3.SetShadowColor(ROOT.kWhite)
    leg3.SetBorderSize(0)
    leg3.SetTextSize(0.035)
    leg3.AddEntry(inner, '#bf{CMS 19.5 fb^{-1} (8 TeV) 68% CL}', 'l')
    leg3.Draw()



leg2 = ROOT.TLegend(0.62,0.86,0.79,0.94)
leg2.SetFillColor(ROOT.kWhite)
leg2.SetShadowColor(ROOT.kWhite)
leg2.SetBorderSize(0)
leg2.SetTextSize(0.035)
leg2.AddEntry(SMpoint, '#bf{SM}', 'p')
leg2.AddEntry(BFpoint, '#bf{best fit}', 'p')
leg2.Draw()


plotDir = os.path.join( plot_directory,"NLL_plots_2D_finalV3/" )
if not os.path.isdir(plotDir):
    os.makedirs(plotDir)

args.year = "COMBINED" if args.combined else args.year

for e in [".png",".pdf",".root"]:
    cans.Print(plotDir+"%s_%s_%s_%s%s"%(args.model, args.plane, setup.name, args.year, postFix)+e)

print "Missing points:"
for m in missing:
    print m

if True:
    debug.Draw("ap0")
    cans.Print(plotDir+"%s_%s_%s_%s%s"%(args.model, args.plane, setup.name, args.year, postFix+"_grid")+'.png')

