from django.db import models
from django.contrib.gis.db import models

from lingcod.mpa.models import Mpa as BaseMpa
from lingcod.array.models import MpaArray as BaseMpaArray
from lingcod.manipulators.manipulators import ClipToStudyRegionManipulator
from omm_manipulators.manipulators import *
from lingcod.unit_converter.models import area_in_display_units

#if the names of the following two classes are changed, the related settings should also be changed (MPA_CLASS, ARRAY_CLASS)

class AOI(BaseMpa):
    description = models.TextField(default="", null=True, blank=True)
    
    @property
    def export_version(self):
        '''
        Port the AOIs attributes over to the AOIShapefile model so we can export the shapefile.
        geometry = models.PolygonField(srid=settings.GEOMETRY_DB_SRID,blank=True,null=True)
        name = models.CharField(max_length=255)
        aoi_id_num = models.IntegerField(blank=True, null=True)
        group = models.ForeignKey(MpaArray, null=True, blank=True)
        group_name = models.CharField(blank=True, max_length=255, null=True)
        area_sq_mi = models.FloatField(blank=True,null=True)
        author = models.CharField(blank=True, max_length=255,null=True)
        aoi = models.OneToOneField(MlpaMpa, related_name="aoi")
        date_modified = models.DateTimeField(blank=True, null=True, auto_now_add=True)
        '''
        msf, created = AOIShapefile.objects.get_or_create(aoi=self)
        if created or msf.date_modified < self.date_modified:
            msf.name = self.name
            msf.aoi_id_num = self.pk
            msf.geometry = self.geometry_final
            short_name = self.name
            if self.array:
                msf.group = self.array
                msf.group_name = self.array.name
            #units based on the settings variable DISPLAY_AREA_UNITS (currently sq miles)
            msf.area_sq_mi = area_in_display_units(self.geometry_final)
            msf.author = self.user.username
            msf.save()
        return msf
    
    @property
    def export_query_set(self):
        # This is a round about way of gettting a queryset with just this one AOI
        return AOIShapefile.objects.filter(pk=self.export_version.pk)
    
    class Options:
        manipulators = []
        optional_manipulators = [ ExcludeTerrestrialManipulator, ExcludeEstuariesManipulator, ExcludeFederalWatersManipulator, ExcludeStateWatersManipulator]
        #optional_manipulators = [ ClipToTerritorialSeaManipulator, ]

class AOIArray(BaseMpaArray):
    pass
    

class AOIShapefile(models.Model):
    """
    This model will provide the correct fields for the export of shapefiles using the django-shapes app.
    """
    geometry = models.PolygonField(srid=settings.GEOMETRY_DB_SRID,blank=True,null=True)
    name = models.CharField(max_length=255)
    aoi_id_num = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey(AOIArray, null=True, blank=True)
    group_name = models.CharField(blank=True, max_length=255, null=True)
    area_sq_mi = models.FloatField(blank=True,null=True)
    author = models.CharField(blank=True, max_length=255,null=True)
    aoi = models.OneToOneField(AOI, related_name="aoi")
    date_modified = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    objects = models.GeoManager()

