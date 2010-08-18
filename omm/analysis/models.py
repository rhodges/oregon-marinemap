from django.contrib.gis.db import models
from django.conf import settings

#import NSH_Geographic models
from NSH_models import  Cities, Islands, Ports, Counties, Shoreline, RockyShores
#import NSH_Physical models
from NSH_models import  ClosedShoreline, Lithology
#import NSH_Biological models 
from NSH_models import  PinnipedHaulouts, SeabirdColonies, Habitats, KelpSurveys
#import NSH_Human Use models
from NSH_models import  StateParks, PublicAccess, DMDSites, Outfalls, UnderseaCables, Towlanes, WaveEnergyPermits
                        
                        
#from AES_models import *                        