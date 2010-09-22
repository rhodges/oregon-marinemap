from django.contrib.gis.db import models
from django.conf import settings

#import NSH_Geographic models
from nsh_models import Cities, Islands, Ports, Counties, Shoreline, RockyShores
#import NSH_Physical models
from nsh_models import ClosedShoreline, Lithology, Bathymetry
#import NSH_Biological models 
from nsh_models import PinnipedHaulouts, SeabirdColonies, Habitats, KelpSurveys, GeologicalHabitat
#import NSH_Human Use models
from nsh_models import StateParks, PublicAccess, DMDSites, Outfalls, UnderseaCables, Towlanes, WaveEnergyPermits
                        
#import NSH_Caching models
from nsh_models import NSHCache
                        
#from AES_models import *                        