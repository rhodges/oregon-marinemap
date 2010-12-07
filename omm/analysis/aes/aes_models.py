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

class TransmissionLines1993(models.Model):
    fnode = models.FloatField()
    tnode = models.FloatField()
    lpoly = models.FloatField()
    rpoly = models.FloatField()
    length = models.FloatField()
    orpower = models.FloatField()
    orpower_id = models.FloatField()
    fename = models.CharField(max_length=30, null=True, blank=True)
    miles = models.FloatField()
    source = models.CharField(max_length=50, null=True, blank=True)
    edit_date = models.DateField(null=True, blank=True)
    shape_leng = models.FloatField()
    shape_le_1 = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Electrical Transmission Lines USGS DOQ 1993")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'
        
class TransmissionLines2010(models.Model):
    name = models.CharField(max_length=254)
    kv = models.FloatField()
    code = models.CharField(max_length=254)
    owner = models.CharField(max_length=60)
    shape_leng = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Electrical Transmission Lines BPA 2010")
    objects = models.GeoManager()  
    
    class Meta:
        app_label = 'analysis'      
    
class Viewsheds(models.Model):
    area = models.FloatField()
    perimeter = models.FloatField()
    viewshed = models.FloatField()
    viewshed_i = models.FloatField()
    inside = models.FloatField()
    major1 = models.IntegerField()
    minor1 = models.IntegerField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Viewsheds Oregon Coast OCMP 2002")
    objects = models.GeoManager()    
    
    class Meta:
        app_label = 'analysis'      
    
class Marinas(models.Model):
    name = models.CharField(max_length=109)
    location = models.CharField(max_length=254)
    address = models.CharField(max_length=53, null=True, blank=True)
    county = models.CharField(max_length=17)
    countyfips = models.CharField(max_length=13, null=True, blank=True)
    town = models.CharField(max_length=24)
    state = models.CharField(max_length=7, null=True, blank=True)
    waterway = models.CharField(max_length=40)
    port_name = models.CharField(max_length=61)
    mile = models.CharField(max_length=7, null=True, blank=True)
    bank = models.CharField(max_length=9, null=True, blank=True)
    latdec = models.FloatField()
    long_dec = models.FloatField()
    operator1 = models.CharField(max_length=160)
    owner = models.CharField(max_length=113, null=True, blank=True)
    purpose = models.CharField(max_length=247)
    rwy_conn = models.CharField(max_length=254)
    portseries = models.CharField(max_length=13)
    seqno = models.CharField(max_length=8, null=True, blank=True)
    loc_cd = models.CharField(max_length=8)
    pwdno = models.CharField(max_length=8)
    oldpwd = models.CharField(max_length=9)
    dockcd = models.CharField(max_length=9)
    ndccode = models.CharField(max_length=12, null=True, blank=True)
    cngdst = models.CharField(max_length=9, null=True, blank=True)
    commodity1 = models.CharField(max_length=14, null=True, blank=True)
    commodity2 = models.CharField(max_length=14, null=True, blank=True)
    commodity3 = models.CharField(max_length=14, null=True, blank=True)
    commodity4 = models.CharField(max_length=14, null=True, blank=True)
    remarks = models.CharField(max_length=254, null=True, blank=True)
    datum = models.CharField(max_length=8, null=True, blank=True)
    depth1 = models.CharField(max_length=8, null=True, blank=True)
    depth1a = models.CharField(max_length=10, null=True, blank=True)
    depth2 = models.CharField(max_length=8, null=True, blank=True)
    depth2a = models.CharField(max_length=10, null=True, blank=True)
    depth3 = models.CharField(max_length=8, null=True, blank=True)
    depth3a = models.CharField(max_length=10, null=True, blank=True)
    totberth1 = models.CharField(max_length=12, null=True, blank=True)
    totberth2 = models.CharField(max_length=12, null=True, blank=True)
    totberth3 = models.CharField(max_length=12, null=True, blank=True)
    year = models.CharField(max_length=6)
    mapno = models.CharField(max_length=8, null=True, blank=True)
    firstname = models.CharField(max_length=21, null=True, blank=True)
    lastname = models.CharField(max_length=33, null=True, blank=True)
    phone = models.CharField(max_length=24, null=True, blank=True)
    fax = models.CharField(max_length=22, null=True, blank=True)
    stfips = models.CharField(max_length=2)
    version = models.CharField(max_length=2)
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Marinas RITA NTA 2009")
    objects = models.GeoManager()    
    
    class Meta:
        app_label = 'analysis'        
    
class Railroads(models.Model):
    fraarcid = models.IntegerField()
    miles = models.FloatField()
    stateab = models.CharField(max_length=2)
    statefips = models.CharField(max_length=2)
    cntyfips = models.CharField(max_length=3)
    stcntyfips = models.CharField(max_length=5)
    fraregion = models.IntegerField()
    rrowner1 = models.CharField(max_length=4, null=True, blank=True)
    rrowner2 = models.CharField(max_length=4, null=True, blank=True)
    rrowner3 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts1 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts2 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts3 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts4 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts5 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts6 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts7 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts8 = models.CharField(max_length=4, null=True, blank=True)
    trkrghts9 = models.CharField(max_length=4, null=True, blank=True)
    stracnet = models.CharField(max_length=1, null=True, blank=True)
    sigsys = models.CharField(max_length=3, null=True, blank=True)
    tracks = models.IntegerField()
    frfranode = models.IntegerField()
    tofranode = models.IntegerField()
    net = models.CharField(max_length=1)
    passngr = models.CharField(max_length=4, null=True, blank=True)
    den07code = models.IntegerField()
    yards = models.CharField(max_length=20, null=True, blank=True)
    subdiv = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=2)
    shape_leng = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Railroad lines RITA NTA 2009")
    objects = models.GeoManager()     
    
    class Meta:
        app_label = 'analysis'       
    
#Used for Physical Reports    
    
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

class StellerHabitats(models.Model):
    objectid = models.IntegerField()
    region = models.CharField(max_length=35)
    name = models.CharField(max_length=50)
    county = models.CharField(max_length=15)
    type = models.CharField(max_length=50)
    length = models.FloatField()
    area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Stellar Sealions Critical Habitats")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis'
        
class Substations(models.Model):
    objectid = models.IntegerField()
    sta_code = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    owner = models.CharField(max_length=60)
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Electrical Substations")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis'

#For Human Use Reports

class UrbanGrowthBoundaries(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=254)
    shape_leng = models.FloatField()
    shape_le_1 = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Urban Growth Boundaries DLCD 2009")
    objects = models.GeoManager()      
    
    class Meta:
        app_label = 'analysis'

class Buoys(models.Model):
    inform = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    recdat = models.CharField(max_length=254, null=True, blank=True)
    recind = models.CharField(max_length=254, null=True, blank=True)
    sordat = models.CharField(max_length=254)
    sorind = models.CharField(max_length=254)
    scamax = models.IntegerField()
    scamin = models.IntegerField()
    txtdsc = models.CharField(max_length=254, null=True, blank=True)
    ninfom = models.CharField(max_length=254, null=True, blank=True)
    nobjnm = models.CharField(max_length=254, null=True, blank=True)
    ntxtds = models.CharField(max_length=254, null=True, blank=True)
    lnam = models.CharField(max_length=20)
    id_name = models.CharField(max_length=20)
    rver = models.IntegerField()
    ruin = models.CharField(max_length=254)
    grup = models.CharField(max_length=254)
    catcam = models.IntegerField()
    catlam = models.IntegerField()
    catspm = models.CharField(max_length=254, null=True, blank=True)
    colour = models.CharField(max_length=254)
    colpat = models.CharField(max_length=254, null=True, blank=True)
    conrad = models.IntegerField()
    datend = models.CharField(max_length=254, null=True, blank=True)
    datsta = models.CharField(max_length=254, null=True, blank=True)
    marsys = models.IntegerField()
    natcon = models.CharField(max_length=254, null=True, blank=True)
    perend = models.CharField(max_length=254, null=True, blank=True)
    persta = models.CharField(max_length=254, null=True, blank=True)
    picrep = models.CharField(max_length=254, null=True, blank=True)
    status = models.CharField(max_length=254)
    veracc = models.FloatField()
    verlen = models.FloatField()
    boyshp = models.IntegerField()
    catinb = models.IntegerField()
    prodct = models.CharField(max_length=254, null=True, blank=True)
    buoy_type = models.IntegerField()
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Buoys")
    objects = models.GeoManager()      
    
    class Meta:
        app_label = 'analysis'       

class SignalEquipment(models.Model):
    inform = models.CharField(max_length=254, null=True, blank=True)
    objnam = models.CharField(max_length=254, null=True, blank=True)
    recdat = models.CharField(max_length=254, null=True, blank=True)
    recind = models.CharField(max_length=254, null=True, blank=True)
    sordat = models.CharField(max_length=254)
    sorind = models.CharField(max_length=254)
    scamax = models.IntegerField()
    scamin = models.IntegerField()
    txtdsc = models.CharField(max_length=254, null=True, blank=True)
    ninfom = models.CharField(max_length=254, null=True, blank=True)
    nobjnm = models.CharField(max_length=254, null=True, blank=True)
    ntxtds = models.CharField(max_length=254, null=True, blank=True)
    lnam = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    rver = models.IntegerField()
    ruin = models.CharField(max_length=254)
    grup = models.CharField(max_length=254)
    catfog = models.IntegerField()
    catlit = models.CharField(max_length=254, null=True, blank=True)
    catsit = models.CharField(max_length=254, null=True, blank=True)
    catsiw = models.CharField(max_length=254, null=True, blank=True)
    catspm = models.CharField(max_length=254, null=True, blank=True)
    colour = models.CharField(max_length=254, null=True, blank=True)
    colpat = models.CharField(max_length=254, null=True, blank=True)
    comcha = models.CharField(max_length=254, null=True, blank=True)
    datend = models.CharField(max_length=254, null=True, blank=True)
    datsta = models.CharField(max_length=254, null=True, blank=True)
    elevat = models.FloatField()
    exclit = models.FloatField()
    height = models.FloatField()
    litchr = models.IntegerField()
    litvis = models.CharField(max_length=254, null=True, blank=True)
    marsys = models.IntegerField()
    mltylt = models.IntegerField()
    natcon = models.CharField(max_length=254, null=True, blank=True)
    orient = models.FloatField()
    perend = models.CharField(max_length=254, null=True, blank=True)
    persta = models.CharField(max_length=254, null=True, blank=True)
    picrep = models.CharField(max_length=254, null=True, blank=True)
    sectr1 = models.FloatField()
    sectr2 = models.FloatField()
    sigfrq = models.IntegerField()
    siggen = models.IntegerField()
    siggrp = models.CharField(max_length=254, null=True, blank=True)
    sigper = models.FloatField()
    sigseq = models.CharField(max_length=254, null=True, blank=True)
    status = models.CharField(max_length=254, null=True, blank=True)
    topshp = models.IntegerField()
    valnmr = models.FloatField()
    valmxr = models.FloatField()
    veracc = models.FloatField()
    verdat = models.IntegerField()
    verlen = models.FloatField()
    light_type = models.IntegerField()
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Signal Equipment")
    objects = models.GeoManager()      
    
    class Meta:
        app_label = 'analysis'   

class Beacons(models.Model):
    inform = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    recdat = models.CharField(max_length=254, null=True, blank=True)
    recind = models.CharField(max_length=254, null=True, blank=True)
    sordat = models.CharField(max_length=254)
    sorind = models.CharField(max_length=254)
    scamax = models.IntegerField()
    scamin = models.IntegerField()
    txtdsc = models.CharField(max_length=254, null=True, blank=True)
    ninfom = models.CharField(max_length=254, null=True, blank=True)
    nobjnm = models.CharField(max_length=254, null=True, blank=True)
    ntxtds = models.CharField(max_length=254, null=True, blank=True)
    lnam = models.CharField(max_length=20)
    id_name = models.CharField(max_length=20)
    rver = models.IntegerField()
    ruin = models.CharField(max_length=254)
    grup = models.CharField(max_length=254)
    catcam = models.IntegerField()
    catlam = models.IntegerField()
    catspm = models.CharField(max_length=254, null=True, blank=True)
    colour = models.CharField(max_length=254, null=True, blank=True)
    colpat = models.CharField(max_length=254, null=True, blank=True)
    conrad = models.IntegerField()
    datend = models.CharField(max_length=254, null=True, blank=True)
    datsta = models.CharField(max_length=254, null=True, blank=True)
    marsys = models.IntegerField()
    natcon = models.CharField(max_length=254, null=True, blank=True)
    perend = models.CharField(max_length=254, null=True, blank=True)
    persta = models.CharField(max_length=254, null=True, blank=True)
    picrep = models.CharField(max_length=254, null=True, blank=True)
    status = models.CharField(max_length=254)
    veracc = models.FloatField()
    verlen = models.FloatField()
    bcnshp = models.IntegerField()
    condtn = models.IntegerField()
    convis = models.IntegerField()
    elevat = models.FloatField()
    height = models.FloatField()
    verdat = models.IntegerField()
    beacon_typ = models.IntegerField()
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Beacons")
    objects = models.GeoManager()      
    
    class Meta:
        app_label = 'analysis'         
        