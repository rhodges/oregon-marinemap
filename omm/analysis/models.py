from django.contrib.gis.db import models
from django.conf import settings

#Used for Geographic Reports

class Cities(models.Model):
    objectid = models.IntegerField()
    fips_code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    acres = models.FloatField()
    gis_prc_dt = models.CharField(max_length=10)
    effectv_dt = models.CharField(max_length=15)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="City Boundaries")
    objects = models.GeoManager()
    
class Islands(models.Model):
    objectid = models.IntegerField()
    area = models.FloatField()
    perimeter = models.FloatField()
    org_bnd = models.IntegerField()
    org_bnd_id = models.IntegerField()
    status = models.CharField(max_length=5)
    nwrunit = models.CharField(max_length=3)
    nwrname = models.CharField(max_length=3)
    ifwsno = models.CharField(max_length=5)
    acreage = models.FloatField()
    tractno = models.CharField(max_length=15)
    islandno = models.CharField(max_length=10, null=True, blank=True)
    namenoaa = models.CharField(max_length=50, null=True, blank=True)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Islands")
    objects = models.GeoManager()    
    
class Ports(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=35)
    harbor = models.CharField(max_length=5)
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Oregon Ports")
    objects = models.GeoManager()

class Counties(models.Model):
    objectid_1 = models.IntegerField()
    objectid = models.IntegerField()
    name = models.CharField(max_length=15)
    cobcode = models.CharField(max_length=5)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="County Boundaries")
    objects = models.GeoManager()    
    
class Shoreline(models.Model):
    objectid = models.IntegerField()
    fnode = models.FloatField()
    tnode = models.FloatField()
    lpoly = models.FloatField()
    rpoly = models.FloatField()
    length = models.FloatField()
    esi_line = models.FloatField()
    esi_line_i = models.FloatField()
    fnode_1 = models.FloatField()
    tnode_1 = models.FloatField()
    lpoly_1 = models.FloatField()
    rpoly_1 = models.FloatField()
    esi_field = models.FloatField()
    esi_id = models.FloatField()
    esi = models.CharField(max_length=10)
    line = models.CharField(max_length=1)
    source_id = models.FloatField()
    shape_leng = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Shoreline")
    objects = models.GeoManager()    
    
class RockyShores(models.Model):
    objectid = models.IntegerField()
    rsindx = models.IntegerField()
    name = models.CharField(max_length=45)
    desig = models.IntegerField()
    reg = models.FloatField()
    site = models.IntegerField()
    size = models.IntegerField()
    bc = models.IntegerField()
    pc = models.IntegerField()
    it_cl = models.IntegerField()
    bm_cl = models.IntegerField()
    te_species = models.CharField(max_length=12, null=True, blank=True)
    visitor = models.IntegerField()
    ed_u = models.IntegerField()
    com_u = models.IntegerField()
    rec_u = models.IntegerField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Rocky Shores")
    objects = models.GeoManager()    
    
#Used for Physical Reports    
    
class ClosedShoreline(models.Model):
    objectid = models.IntegerField()
    fnode = models.IntegerField()
    tnode = models.IntegerField()
    lpoly = models.IntegerField()
    rpoly = models.IntegerField()
    length = models.FloatField()
    esi_ln = models.IntegerField()
    esi_ln_id = models.IntegerField()
    shape_leng = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Closed Shoreline")
    objects = models.GeoManager()    
    
class Lithology(models.Model):
    objectid = models.IntegerField()
    lith_inter = models.CharField(max_length=24)
    lithology = models.CharField(max_length=20)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Territorial Sea Lithology")
    objects = models.GeoManager()
    
    