# run in CMSSW_9_3_1
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = "tmp"
config.General.workArea = 'crab_dim6top_18Mai18'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '../cfg/2017/GEN-SIM-LHE_LO_0j_CMSSW_9_3_1.py'
config.JobType.disableAutomaticOutputCollection = False

config.section_("Data")
config.Data.splitting = 'EventBased'

config.Data.unitsPerJob = 5000
config.Data.totalUnits  = 5000000 
config.Data.publication = True
config.Data.publishDBS = 'phys03'

#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())

config.section_("Site")
config.Site.storageSite = 'T2_AT_Vienna'
#config.Site.whitelist = ['T2_*']

config.section_("User")

if __name__ == '__main__':
    gridpack_dir = "/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018_ref/ttgamma/order2/"

    import os

    from CRABAPI.RawCommand import crabCommand

    for outputDatasetTag, gridpack in [

        ('dim6top_18Mai18_ref','ttgamma0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.tar.xz'),
    ]:
        config.Data.outputDatasetTag = outputDatasetTag
        config.JobType.inputFiles = [os.path.join(gridpack_dir, gridpack)]
        config.General.requestName = gridpack.rstrip('.tar.xz').replace('-','m').replace('.','p')
        config.Data.outputPrimaryDataset = config.General.requestName # dataset name
        
        config.JobType.pyCfgParams = ['gridpack=../'+gridpack]

        #crabCommand('submit', '--dryrun', config = config)
        crabCommand('submit', config = config)
