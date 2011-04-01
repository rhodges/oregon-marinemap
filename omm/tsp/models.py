from django.db import models
from django.conf import settings
from django.contrib.gis.db import models

from lingcod.features.models import PolygonFeature, FeatureCollection
from lingcod.features import register
from lingcod.layers.models import PrivateLayerList
from lingcod.manipulators.manipulators import ClipToStudyRegionManipulator
#from omm_manipulators.manipulators import *
from lingcod.unit_converter.models import area_in_display_units

#if the names of the following two classes are changed, the related settings should also be changed (MPA_CLASS, ARRAY_CLASS)

@register
class AOI(PolygonFeature):
    description = models.TextField(default="", null=True, blank=True)
    
    @property
    def export_version(self):
        '''
        Port the AOIs attributes over to the AOIShapefile model so we can export the shapefile.
        '''
        msf, created = AOIShapefile.objects.get_or_create(aoi=self)
        if created or msf.date_modified < self.date_modified:
            msf.name = self.name
            msf.aoi_id_num = self.pk
            msf.geometry = self.geometry_final
            #short_name = self.name
            if self.array:
                msf.group = self.array
                msf.group_name = self.array.name
            #units based on the settings variable DISPLAY_AREA_UNITS (currently sq miles)
            msf.area_sq_mi = area_in_display_units(self.geometry_final)
            msf.author = self.user.username
            msf.aoi_modification_date = self.date_modified
            msf.save()
        return msf
    
    @property
    def export_query_set(self):
        # This is a round about way of gettting a queryset with just this one AOI
        return AOIShapefile.objects.filter(pk=self.export_version.pk)
    
    @classmethod
    def mapnik_style(self):
        import mapnik
        polygon_style = mapnik.Style()
        ps = mapnik.PolygonSymbolizer(mapnik.Color('#DC640C'))
        ps.fill_opacity = 0.6
        ls = mapnik.LineSymbolizer(mapnik.Color('#ff0000'),0.2)
        ls.stroke_opacity = 1.0
        r = mapnik.Rule()
        r.symbols.append(ps)
        r.symbols.append(ls)
        polygon_style.rules.append(r)
        return polygon_style

    class Options:
        manipulators = []
        optional_manipulators = [ 
                'omm_manipulators.manipulators.ExcludeTerrestrialManipulator', 
                'omm_manipulators.manipulators.ExcludeEstuariesManipulator', 
                'omm_manipulators.manipulators.ExcludeFederalWatersManipulator', 
                'omm_manipulators.manipulators.ExcludeStateWatersManipulator']
        geometry_input_methods = ['load_shp']
        verbose_name = 'Area of Interest (AOI)'
        show_template = 'mpa/show.html'
        form = 'tsp.forms.AOIForm'
        

@register
class AOIArray(FeatureCollection):
        
    @property
    def export_query_set(self):
        for aoi in self.mpa_set.all():
            aoi.export_version # update these records
        qs = AOIShapefile.objects.filter(group=self)
        return qs

    class Options:
        verbose_name = 'Folder'
        valid_children = ( 'tsp.models.AOI', 
                'tsp.models.AOIArray',
                'tsp.models.UserKml')
        form = 'tsp.forms.ArrayForm'
        show_template = 'array/show.html'
    

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
    aoi_modification_date = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    objects = models.GeoManager()

@register
class UserKml(PrivateLayerList):
    class Options:
        form = 'tsp.forms.UserKmlForm'
