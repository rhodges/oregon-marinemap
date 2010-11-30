from django.contrib.gis.db import models
from django.conf import settings
#Used for Caching Report Context
from picklefield import PickledObjectField
    
class AESCache(models.Model):
    type = models.CharField(max_length=50)
    context = PickledObjectField()
    wkt_hash = models.CharField(max_length=255)
    
    #ensure no duplicates (same geometry and type) 
    def save(self, *args, **kwargs):
        #remove any old entries
        old_entries = AESCache.objects.filter(wkt_hash=self.wkt_hash, type=self.type)
        for entry in old_entries:
            AESCache.delete(entry)
        #save the new entry
        super(AESCache, self).save(*args, **kwargs)
        
    class Meta:
        app_label = 'analysis'


#Used for Geographic Reports

#we already have the following from nsh_models:
#   Cities, Ports, Islands, StateParks
    
#Used for Biology Reports

class Seagrass(models.Model):
    seagrass1 = models.CharField(max_length=10, null=True, blank=True)
    seagrass2 = models.CharField(max_length=10, null=True, blank=True)
    seagrass3 = models.CharField(max_length=10, null=True, blank=True)
    year1 = models.IntegerField()
    year2 = models.IntegerField()
    year3 = models.IntegerField()
    source1 = models.CharField(max_length=10, null=True, blank=True)
    source2 = models.CharField(max_length=10, null=True, blank=True)
    source3 = models.CharField(max_length=10, null=True, blank=True)
    sg_flag = models.CharField(max_length=10, null=True, blank=True)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Seagrass")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'

class StellarSeaLions(models.Model):
    objectid = models.IntegerField()
    region = models.CharField(max_length=35)
    site_name = models.CharField(max_length=50)
    or_county = models.CharField(max_length=15)
    areatype = models.CharField(max_length=50)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Stellar Sealions Critical Habitats")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis'

        