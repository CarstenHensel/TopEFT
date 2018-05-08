from RootTools.core.standard import *
base_dir = '/afs/hephy.at/data/rschoefbeck01/cmgTuples/sync/'
mc_2016  = Sample.fromCMGOutput('mc_2016',  base_dir, chunkString='TTJets_SingleLeptonFromTbar', isData = True)
mc_2017  = Sample.fromCMGOutput('mc_2017',  base_dir, chunkString='TTSemi_pow', isData = True)
data_2016= Sample.fromCMGOutput('data_2016',base_dir, chunkString='MuonEG_Run2016F_03Feb2017', isData = True)
data_2017= Sample.fromCMGOutput('data_2017',base_dir, chunkString='MuonEG_Run2017F_17Nov2017', isData = True)
