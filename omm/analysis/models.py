from django.contrib.gis.db import models
from django.conf import settings

#NSH RELATED IMPORTS

#import NSH_Geographic models
from nsh.nsh_models import Cities, Islands, Ports, Counties, Shoreline, RockyShores
#import NSH_Physical models
from nsh.nsh_models import ClosedShoreline, Lithology, Bathymetry
#import NSH_Biological models 
from nsh.nsh_models import PinnipedHaulouts, SeabirdColonies, Habitats, KelpSurveys, GeologicalHabitat
#import NSH_Human Use models
from nsh.nsh_models import StateParks, PublicAccess, DMDSites, Outfalls, UnderseaCables, Towlanes, WaveEnergyPermits
                        
#import NSH_Caching models
from nsh.nsh_models import NSHCache


#AES RELATED IMPORTS
                        
#import AES_Geographic models
from aes.aes_models import Substations, TransmissionLines1993, TransmissionLines2010, Viewsheds, Marinas

#import AES_Physical models

#import AES_Biological models
from aes.aes_models import Seagrass, StellerHabitats

#import AES_Human Use models

#import AES_Caching models
from aes.aes_models import AESCache
                     