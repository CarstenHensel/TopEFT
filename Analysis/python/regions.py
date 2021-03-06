from TopEFT.Analysis.Region import Region

def getRegionsFromThresholds(var, vals, gtLastThreshold = True):
    return [Region(var, (vals[i], vals[i+1])) for i in range(len(vals)-1)]

def getRegions2D(varOne, varOneThresholds, varTwo, varTwoThresholds):
    regions_varOne  = getRegionsFromThresholds(varOne,  varOneThresholds)
    regions_varTwo  = getRegionsFromThresholds(varTwo, varTwoThresholds)

    regions2D = []
    for r1 in regions_varOne:
        for r2 in regions_varTwo:
            regions2D.append(r1+r2)

    return regions2D



#Put all sets of regions that are used in the analysis, closure, tables, etc.

## 3l signal regions
regionsA = [ Region("Z_pt", (0, 200)), Region("Z_pt", (200, 400)), Region("Z_pt", (400, -1)) ] # first sensitivity study
regionsB = getRegions2D("Z_pt", [0,100,200,-1], "cosThetaStar", [-1,-0.6, 0.6, 1])
regionsC = getRegions2D("Z_pt", [0,100,200,-1], "abs(cosThetaStar)", [0, 0.6, 1])
regionsD = [ Region("Z_pt", (0, 100)), Region("Z_pt", (100, 200)), Region("Z_pt", (200, -1)) ]
regionsE = getRegions2D("Z_pt", [0,100,200,400,-1], "cosThetaStar", [-1,-0.6, 0.6, 1]) # best results
regionsF = getRegions2D("Z_pt", [0,100,200,400], "cosThetaStar", [-1,-0.6, 0.6, 1]) + [Region("Z_pt", (400, -1))]
regionsG = getRegions2D("Z_pt", [0,100,200,400,-1], "lep_pt[2]", [0,30, 60, -1])
regionsH = getRegions2D("Z_pt", [0,100,200,400,-1], "lep_pt[Z_l2_index]", [0, 30, 60, -1])

regionsXSec     = getRegions2D("nBTag", [1, 2, -1], "nJetSelected", [2,3,4,5,-1])
regionsXSecB    = getRegions2D("nBTag", [1, 2, -1], "nJetSelected", [1,2,3,-1])
regionsXSecC    = getRegions2D("nBTag", [1, -1], "nJetSelected", [3,4,5,-1])
regionsXSecD    = getRegions2D("nBTag", [0, 1, 2, -1], "nJetSelected", [1,2,3,4,5,-1])
regionsXSecE    = getRegions2D("nBTag", [0, 1], "nJetSelected", [1,2,3,-1]) + getRegions2D("nBTag", [1, 2, -1], "nJetSelected", [2,3,4,5,-1])

regionsXSecCR   = getRegions2D("nBTag", [0, 1], "nJetSelected", [1,2,3,4,-1]) + getRegions2D("nBTag", [1, 2], "nJetSelected", [2,3,4, 5, -1]) + getRegions2D("nBTag", [2,-1], "nJetSelected", [2,3,4, 5, -1])

## 4l signal regions
regions4l       = getRegions2D("Z1_pt_4l", [0,-1], "Z1_cosThetaStar_4l", [-1,-0.6, 0.6, 1])
regions4lB      = getRegions2D("Z1_pt_4l", [0,100,200,-1], "Z1_cosThetaStar_4l", [-1, 1])
regions4lXSec   = getRegions2D("nBTag", [1, -1], "nJetSelected", [1,-1])
regions4lXSecE  = getRegions2D("nBTag", [0, 1, -1], "nJetSelected", [1,-1])

## Upgrade regions
regionsUpgrade = getRegionsFromThresholds('Z_pt', [0,100,200,400,-1])

## regions for pT(Z), cos(Theta*) reweighting
regionsReweight     = getRegions2D("Z_pt", [0, 50, 100, 150, 200, 250, 300, 400, 500, 100000], "cosThetaStar", [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
regionsReweight4l   = getRegions2D("Z1_pt_4l", [0, 50, 100, 150, 200, 250, 300, 400, 500, 100000], "Z1_cosThetaStar_4l", [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])

## inclusive
noRegions = [Region("Z_pt", (0, -1)) + Region("cosThetaStar", (-1, -1))] # For TTZ CR 
noRegionsB = [ Region("nBTag", (0,-1)) ]
noRegionsC = [ Region("nBTag", (1,-1)) ]

## b-tag regions for WZ uncertainties
btagRegions = [ Region("nBTag", (0,0)), Region("nBTag", (1,1)), Region("nBTag", (2,-1)) ]
