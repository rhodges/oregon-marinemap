from django.db import models
from django.contrib.gis.db import models

from lingcod.mpa.models import Mpa as BaseMpa
from lingcod.array.models import MpaArray as BaseMpaArray
from lingcod.manipulators.manipulators import ClipToStudyRegionManipulator
from omm_manipulators.manipulators import ClipToTerritorialSeaManipulator

#if the names of the following two classes are changed, the related settings should also be changed (MPA_CLASS, ARRAY_CLASS)

class AOI(BaseMpa):
    description = models.TextField(default="", null=True, blank=True)
    
    class Options:
        manipulators = []
        optional_manipulators = [ ClipToTerritorialSeaManipulator, ]

class AOIArray(BaseMpaArray):
    pass
    


