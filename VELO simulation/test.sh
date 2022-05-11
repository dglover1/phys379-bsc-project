#from VP0-0 to VP3-2
sensorNames=(VP0-0  VP0-1  VP0-2  VP1-0  VP1-1  VP1-2  VP2-0  VP2-1  VP2-2  VP3-0  VP3-1  VP3-2)
noisyFracs=(0.00355530 0.00166321 0.00247192 0.00250244 0.00357056 0.0027771 0.00340271 0.00350952 0 0.00350952 0.00364685 0.00334167)
deadFracs=(0.05580139 0.01870728 0.02384949 0.01364136 0.02908325 0.0184021 0.03430176 0.03062439 0 0.05316162 0.04708862 0.03323364)

source /cvmfs/lhcb.cern.ch/lib/LbEnv

for i in ${!sensorNames[@]}; do
	export NOISY_FRAC=0
	export DEAD_FRAC=${deadFracs[$i]}
	echo "$NOISY_FRAC , $DEAD_FRAC"
	resultsDir=./savedResults/DEF-plus-premasked-masked_0-minus-premasked_noisy/deadOnly/${sensorNames[$i]}
	

	rm Boole.log DaVinci.log MinBiasWithVPOnlySim-10ev-histos.root MinBiasWithVPOnlySim-10ev-Extended.digi || true
	rm ${resultsDir}/Boole.log ${resultsDir}/DaVinci.log ${resultsDir}/MinBiasWithVPOnlySim-10ev-histos.root ${resultsDir}/MinBiasWithVPOnlySim-10ev-Extended.digi || true
	
	lb-run Boole/v43r0 gaudirun.py Boole.py | tee Boole.log
	lb-run DaVinci/v54r0 gaudirun.py DaVinci.py | tee DaVinci.log 2>&1

	cp Boole.log DaVinci.log MinBiasWithVPOnlySim-10ev-histos.root MinBiasWithVPOnlySim-10ev-Extended.digi ${resultsDir}
done
