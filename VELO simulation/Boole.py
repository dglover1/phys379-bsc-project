from Gaudi.Configuration import *
from Configurables import Boole, LHCbApp

from Configurables import Boole, CondDB, LHCbApp
# Set the detector simulated version
LHCbApp().DDDBtag   = "dddb-20210617"        
# Set the simulated conditions
LHCbApp().CondDBtag = "sim-20210617-vc-md100"
Boole().DataType = "Upgrade"

Boole().EvtMax = 10    # Run 10 events from the file: -1 = all 
Boole().DigiType = "Extended"
    
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(["/bundle/data/LHCb/users/hutchcroft/VPNoise/00152976_00000001_1.xdigi"])

Boole().DatasetName = "MinBiasWithVPOnlySim"


#####################################
### Adjust the simulation params  ###
#####################################
from Configurables import VPDigitCreator
vpd = VPDigitCreator()
# optionally set the values
import os
fracMasked = os.environ['DEAD_FRAC']
fracNoisy = os.environ['NOISY_FRAC']
#fracMasked = 0.06053162
#fracNoisy = 0
vpd.FractionMasked = fracMasked
vpd.FractionNoisy = fracNoisy
vpd.NoisyPixels = True
print("Set Fraction masked {} Fraction Noisy {}".format(fracMasked, fracNoisy))
# Print configuration:
vpd.PropertiesPrint = True
