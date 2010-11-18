from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from lingcod.manipulators.manipulators import BaseManipulator, ClipToShapeManipulator


class EastOfTerritorialSeaLineManager(models.GeoManager):
    """Returns the currently active data layer (determined by the active attribute).
    """
    def current(self):
        return self.get(active=True)

class EastOfTerritorialSeaLine(models.Model):
    """Model used for storing data layer related to ExcludingFederalWatersManipulator

        ======================  ==============================================
        Attribute               Description
        ======================  ==============================================
        ``creation_date``       When the layer was created. Is not changed on
                                updates.
                                
        ``active``              Whether this layer represents the current 
                                data layer. If set to true and and another
                                layer is active, that old layer will be 
                                deactivated.

        ``geometry``            PolygonField representing the non-federal-waters
        ======================  ==============================================
    """    
    name = models.CharField(verbose_name="East Of Territorial Sea Line Name", max_length=255, blank=True)
    
    creation_date = models.DateTimeField(auto_now=True) 
    
    active = models.BooleanField(default=True, help_text="""
        Checking here indicates that this layer list should be the one used in
        the application. Copies of other layer lists are retained in the
        system so you can go back to an old version if necessary.
    """)
    
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Non-Federal-Waters")
    
    objects = EastOfTerritorialSeaLineManager()
    
    def __unicode__(self):
        return "EastOfTerritorialSeaLine Layer, created: %s" % (self.creation_date)
    
    def save(self, *args, **kwargs):
        super(EastOfTerritorialSeaLine, self).save(*args, **kwargs)
        if self.active and EastOfTerritorialSeaLine.objects.filter(active=True).count() > 1:
            # Ensure that any previously active layer is deactivated
            # There can be only one!
            EastOfTerritorialSeaLine.objects.filter(active=True).exclude(pk=self.pk).update(active=False)