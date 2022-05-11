from Gaudi.Configuration import *
from Configurables import DaVinci, CondDB, LHCbApp
dv = DaVinci()
dv.InputType  = 'DIGI'
dv.Simulation = True
dv.DataType   = 'Upgrade'
# Set the detector simulated version
dv.DDDBtag    = "dddb-20210617"        
# Set the simulated conditions
dv.CondDBtag  = "sim-20210617-vc-md100"
dv.TupleFile = "DaVinciTuple.root"

# find all files in this directory ending with Extended.digi
import glob
fList = glob.glob("*Extended.digi")
inputList = ['PFN:'+f for f in fList]
if len(inputList) == 0 :
    print("No .digi files found!")
    import sys
    sys.exit(-1)

# Use those files as input
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(inputList)

from Configurables import GaudiSequencer
VPSeq = GaudiSequencer("VPSeq")

# do VP pattern recognition
from Configurables import VeloClusterTrackingSIMD, TracksVPMergerConverter, VPClus
prPixelTracking = VeloClusterTrackingSIMD("VeloClusterTracking")
prPixelTracking.TracksLocation = "Rec/Track/Velo" + "SOA"
vpConverter = TracksVPMergerConverter("ConverterVP")
vpConverter.TracksForwardLocation = prPixelTracking.TracksLocation
vpConverter.TracksBackwardLocation = prPixelTracking.TracksBackwardLocation
vpConverter.OutputTracksLocation = "Rec/Track/Velo"

from Configurables import LHCb__Converters__Track__v1__fromV2TrackV1Track as FromV2TrackV1Track
trconverter = FromV2TrackV1Track("VeloConverter")
trconverter.InputTracksName = "Rec/Track/Velo"
trconverter.OutputTracksName = "Rec/Track/Keyed/Velo"

VPSeq.Members = [VPClus("VPClustering"), prPixelTracking, vpConverter, trconverter]

# Now add MC Checking adapted from
# $TRACKSYSROOT/python/TrackSys/PrUpgradeChecking.py

# default types to check (you can tweak this to taste)
MCCuts = {
    "Velo": {
        "01_velo": "isVelo",
        "02_long": "isLong",
        "03_long>5GeV": "isLong & over5",
        "04_long_strange": "isLong & strange",
        "05_long_strange>5GeV": "isLong & strange & over5",
        "06_long_fromB": "isLong & fromB",
        "07_long_fromB>5GeV": "isLong & fromB & over5",
        "08_long_electrons": "isLong & isElectron",
        "09_long_fromB_electrons": "isLong & isElectron & fromB",
        "10_long_fromB_electrons_P>5GeV": "isLong & isElectron & over5 & fromB"
    }
}
def getMCCuts(key):
    cuts = dict(MCCuts[key]) if key in MCCuts else {}
    for name in cuts.keys():
        cuts[name] = cuts[name] + " & (MCETA > 2.0) & (MCETA < 5.0)"
    return cuts

from Configurables import \
    UnpackMCParticle, UnpackMCVertex, PrLHCbID2MCParticleVP, \
    VPCluster2MCParticleLinker, VPFullCluster2MCParticleLinker, VPClusFull
prLHCbID2MCParticle = PrLHCbID2MCParticleVP()
prLHCbID2MCParticle.VPFullClustersLocation = 'Raw/VP/FullClusters'
prLHCbID2MCParticle.VPFullClustersLinkLocation = 'Link/' + \
  str(prLHCbID2MCParticle.VPFullClustersLocation)

VPCheckSeq = GaudiSequencer("VPCheck")
VPCheckSeq.Members = [
    UnpackMCParticle(), UnpackMCVertex(), # need MCParticles and vertices
    VPClusFull(), # and VP clusters
    VPFullCluster2MCParticleLinker(), # Make linker table
    prLHCbID2MCParticle # link to full clusters from LHCbID
]

from Configurables import PrTrackAssociator
from Configurables import PrTrackChecker

trassociator = PrTrackAssociator("VeloAssociator")
trassociator.SingleContainer = "Rec/Track/Keyed/Velo"
trassociator.OutputLocation = 'Link/Rec/Track/Keyed/Velo'

veloChecker = PrTrackChecker(
        "VeloMCCheck",
        Title="Velo",
        Tracks="Rec/Track/Keyed/Velo",
        Links="Link/Rec/Track/Keyed/Velo",
        TriggerNumbers=False,
        CheckNegEtaPlot=True,
        HitTypesToCheck=3, # Has to mirror the enum HitType in PrTrackCounter.h
        MyCuts=getMCCuts("Velo"),
        WriteHistos=2)

VPCheckSeq.Members += [trassociator,veloChecker]

from Configurables import VPTrackEff
from Configurables import DataPacking__Unpack_LHCb__MCVPHitPacker_
MCHitCheckSeq = GaudiSequencer("MCHitCheckSeq")
VPTrackEff().TrackLocation = "Rec/Track/Keyed/Velo"
MCHitCheckSeq.Members = [DataPacking__Unpack_LHCb__MCVPHitPacker_("UnpackVPHits"),
                         VPTrackEff()]

dv.UserAlgorithms = [VPSeq, VPCheckSeq, MCHitCheckSeq]
