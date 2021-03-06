To obtain a limit you first need the estimates (including systematic variations).
So far the default is to use 2016 data/MC. Be careful when trying to run 2017.

Run estimates with the following command will cache estimates including variations (for WZ only):
```
python run_estimates.py --sample WZ
```

Run PDF (including alpha_s) and scale uncertainties using the following command.
Calculation is done in parallel, but be careful not to run different regions on different machines.
The sqlite db can crash due to concurrency issues (this is an inherent limitation of sqlite).
```
python calcPDFuncertainty.py --sample TTZ_NLO_16 --PDFset NNPDF30
```
Afterwards, you can calculate the uncertainties the results using
```
python calcPDFuncertainty.py --sample TTZ_NLO_16 --PDFset NNPDF30 --combine
```

Signal reweighting templates should all be ready, and there's no need to rerun them soon.
However, they are created with
```
python SignalReweightingTemplate.py
```

Writing the card file and getting the likelihood ratio using both x-sec and shape information is done with
```
python run_limit_reweighting.py --model ewkDM --signal dipoles --useXSec --useShape --year 2016 --only 0
```
You can also do the same for some control regions. However, the fit seems to be meaningless/failing.
Anyway, the card file can be used to create plots.
Right now, unblinding only works in control regions using the options `--controlRegion nbtag0-njet0p --unblind`


If you ever happen to crash a sqlite DB, use the `recoverDB.sh` script inside the Tools section:
```
./recoverDB.sh DBNAME PATHTODB
```


Plots of observables including systematic uncertainties are produced with the following command (code to be found within plotsDaniel/uncertainties)
```
python systematicsPlots.py --plot_directory systematicsPlots_80X_v20 --selection trilep-Zcand-lepSelTTZ-njet3p-btag0-onZ --selectSys JECUp --runLocal
```
First run over the various sources separately (JECUp/Down, PU36fbUp/Down etc), then run with `--selectSys combine`.
Batch submission doesn't work atm, so please use `--runLocal`.

Plots of the signal regions, including _all_ pre-fit uncerertainties can be obtained using `signalRegionPlots.py` in plotsDaniel/regions.
Just specify a cardfile and enjoy the beauty.
