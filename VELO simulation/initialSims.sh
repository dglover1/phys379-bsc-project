#from VP0-0 to VP3-2
sensorNames=(VP0-0  VP0-1  VP0-2  VP1-0  VP1-1  VP1-2  VP2-0  VP2-1  VP2-2  VP3-0  VP3-1  VP3-2)
#sensorNames=(VP0-0  VP0-1  VP0-2  VP1-0  VP1-1  VP1-2  VP2-0  VP2-1  VP3-0  VP3-1  VP3-2)

noisyFracs=(0.00382487
0.001607259
0.002492269
0.002385457
0.003555298
0.002797445
0.003448486
0.003519694
0.008641561
0.003687541
0.003631592
0.003204346)

deadFracs=(0.055582682
0.018834432
0.023732503
0.013702393
0.029078166
0.018274943
0.034306844
0.030710856
0.060506185
0.052820841
0.04679362
0.033370972)

source /cvmfs/lhcb.cern.ch/lib/LbEnv

for i in ${!sensorNames[@]}; do
	export NOISY_FRAC=0
	export DEAD_FRAC=${deadFracs[$i]}
	echo "$NOISY_FRAC , $DEAD_FRAC"
	resultsDir=./savedResults/noisy=0minusMasked_dead=DEFplusMasked/deadOnly/${sensorNames[$i]}
    mkdir -p $resultsDir
	

	rm Boole.log DaVinci.log MinBiasWithVPOnlySim-10ev-histos.root MinBiasWithVPOnlySim-10ev-Extended.digi || true
	rm ${resultsDir}/Boole.log ${resultsDir}/DaVinci.log ${resultsDir}/MinBiasWithVPOnlySim-10ev-histos.root ${resultsDir}/MinBiasWithVPOnlySim-10ev-Extended.digi || true
	
	lb-run Boole/v43r0 gaudirun.py Boole.py | tee Boole.log
	lb-run DaVinci/v54r0 gaudirun.py DaVinci.py | tee DaVinci.log 2>&1

	cp Boole.log DaVinci.log MinBiasWithVPOnlySim-10ev-histos.root MinBiasWithVPOnlySim-10ev-Extended.digi ${resultsDir}
done

