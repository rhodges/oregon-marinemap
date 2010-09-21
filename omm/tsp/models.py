from django.db import models
from django.contrib.gis.db import models

from lingcod.mpa.models import Mpa as BaseMpa
from lingcod.array.models import MpaArray as BaseMpaArray

#if the names of the following two classes are changed, the related settings should also be changed (MPA_CLASS, ARRAY_CLASS)

class AOI(BaseMpa):
    description = models.TextField(default="", null=True, blank=True)

class AOIArray(BaseMpaArray):
    pass
    
class MRS(BaseMpa):
    description = models.TextField(default="", null=True, blank=True)
    
class MRS_original(models.Model):
    import settings
    sitename = models.CharField(default="", max_length="255", null=True, blank=True)
    label = models.CharField(default="", max_length="255", null=True, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True)
    objects = models.Manager()


