#!/usr/bin/env python3

import sys
from glob import glob
searchString = str(sys.argv[1])+"/*/DaVinci.log"
print("\nDAVINCI LOGFILE RESULTS PARSER\n\nSearching for "+searchString+" ...")
filenames = glob(searchString)

for filename in filenames:
	lines = open(filename, 'r').readlines()

	for line in lines:
		if "VeloMCCheck          INFO   01_velo" in line:
			print("\nFound file: "+filename)
			index = line.find("from")
			print("# Total tracks simulated: "+str(float(line[index+10:index+13])))
			print("# Tracks reconstructed: "+str(float(line[index-4:index-1])))
			print("Fraction reconstructed: "+str(float(line[index-4:index-1]) / float(line[index+10:index+13])))
			break
