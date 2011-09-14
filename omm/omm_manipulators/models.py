from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from lingcod.manipulators.models import BaseManipulatorGeometry


class EastOfTerritorialSeaLine(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="East Of Territorial Sea Line Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Non-Federal-Waters")
    
    def __unicode__(self):
        return "EastOfTerritorialSeaLine Layer, created: %s" % (self.creation_date)
        
class TerrestrialAndEstuaries(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="Terrestrial and Estuaries Geometry Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Terrestrial-and-Estuaries")

    def __unicode__(self):
        return "Terrestrial and Estuaries Layer, created: %s" % (self.creation_date)
        
class Terrestrial(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="Terrestrial Geometry Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Terrestrial-Only")

    def __unicode__(self):
        return "Terrestrial Layer, created: %s" % (self.creation_date)
        
class Estuaries(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="Estuaries Geometry Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Estuaries-Only")

    def __unicode__(self):
        return "Estuaries Layer, created: %s" % (self.creation_date)
        
