
noisyFracs=(0.0 0.00001 0.00002 0.00003 0.00004 0.00005 0.00006 0.00007 0.00008 0.00009 0.0001)

source /cvmfs/lhcb.cern.ch/lib/LbEnv

resultsDir=./savedResults/noisyCurveMapping

for i in ${!noisyFracs[@]}; do
	#echo "$i"
	export NOISY_FRAC=${noisyFracs[$i]}
	export DEAD_FRAC=0
	echo "$NOISY_FRAC , $DEAD_FRAC"
	subDir=$resultsDir/${noisyFracs[$i]}-noisy_0-dead
	mkdir -p $subDir

	rm Boole.log DaVinci.log MinBiasWithVPOnlySim-10ev-histos.root MinBiasWithVPOnlySim-10ev-Extended.digi || true
	rm ${subDir}/Boole.log ${subDir}/DaVinci.log ${subDir}/MinBiasWithVPOnlySim-10ev-histos.root ${subDir}/MinBiasWithVPOnlySim-10ev-Extended.digi || true
	
	lb-run Boole/v43r0 gaudirun.py Boole.py | tee Boole.log
	lb-run DaVinci/v54r0 gaudirun.py DaVinci.py | tee DaVinci.log 2>&1

	cp Boole.log DaVinci.log MinBiasWithVPOnlySim-10ev-histos.root MinBiasWithVPOnlySim-10ev-Extended.digi ${subDir}
done

./resultsParser.py $resultsDir