from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from lingcod.manipulators.models import BaseManipulatorGeometry


class EastOfTerritorialSeaLine(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="East Of Territorial Sea Line Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Non-Federal-Waters")
    
    def __unicode__(self):
        return "EastOfTerritorialSeaLine Layer, created: %s" % (self.creation_date)
    
    def save(self, *args, **kwargs):
        super(EastOfTerritorialSeaLine, self).save(*args, **kwargs)
        if self.active and EastOfTerritorialSeaLine.objects.filter(active=True).count() > 1:
            # Ensure that any previously active layer is deactivated -- There can be only one!
            EastOfTerritorialSeaLine.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
            
class TerrestrialAndEstuaries(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="Terrestrial and Estuaries Geometry Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Terrestrial-and-Estuaries")

    def __unicode__(self):
        return "Terrestrial and Estuaries Layer, created: %s" % (self.creation_date)
    
    def save(self, *args, **kwargs):
        super(TerrestrialAndEstuaries, self).save(*args, **kwargs)
        if self.active and TerrestrialAndEstuaries.objects.filter(active=True).count() > 1:
            # Ensure that any previously active layer is deactivated -- There can be only one!
            TerrestrialAndEstuaries.objects.filter(active=True).exclude(pk=self.pk).update(active=False)

class Terrestrial(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="Terrestrial Geometry Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Terrestrial-Only")

    def __unicode__(self):
        return "Terrestrial Layer, created: %s" % (self.creation_date)
    
    def save(self, *args, **kwargs):
        super(Terrestrial, self).save(*args, **kwargs)
        if self.active and Terrestrial.objects.filter(active=True).count() > 1:
            # Ensure that any previously active layer is deactivated -- There can be only one!
            Terrestrial.objects.filter(active=True).exclude(pk=self.pk).update(active=False)

class Estuaries(BaseManipulatorGeometry):
    name = models.CharField(verbose_name="Estuaries Geometry Name", max_length=255, blank=True)
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Estuaries-Only")

    def __unicode__(self):
        return "Estuaries Layer, created: %s" % (self.creation_date)
    
    def save(self, *args, **kwargs):
        super(Estuaries, self).save(*args, **kwargs)
        if self.active and Estuaries.objects.filter(active=True).count() > 1:
            # Ensure that any previously active layer is deactivated -- There can be only one!
            Estuaries.objects.filter(active=True).exclude(pk=self.pk).update(active=False)

