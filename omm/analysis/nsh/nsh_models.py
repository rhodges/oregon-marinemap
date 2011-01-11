from django.contrib.gis.db import models
from django.conf import settings
#Used for Caching Report Context
from picklefield import PickledObjectField
    
class NSHCache(models.Model):
    type = models.CharField(max_length=50)
    context = PickledObjectField()
    wkt_hash = models.CharField(max_length=255)
    
    #ensure no duplicates (same geometry and type) 
    def save(self, *args, **kwargs):
        #remove any old entries
        old_entries = NSHCache.objects.filter(wkt_hash=self.wkt_hash, type=self.type)
        for entry in old_entries:
            NSHCache.delete(entry)
        #save the new entry
        super(NSHCache, self).save(*args, **kwargs)
        
    class Meta:
        app_label = 'analysis'


#Used for Geographic Reports
'''
###Outdatated###
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
    
    class Meta:
        app_label = 'analysis'
'''      
class Cities(models.Model):
    fips_code = models.CharField(max_length=5)
    name = models.CharField(max_length=30)
    acres = models.FloatField()
    gis_prc_dt = models.CharField(max_length=10)
    effectv_dt = models.CharField(max_length=15)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="City Boundaries")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'
    
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
    
    class Meta:
        app_label = 'analysis'  
    
class Ports(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=35)
    harbor = models.CharField(max_length=5)
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Oregon Ports")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'

class Counties(models.Model):
    objectid_1 = models.IntegerField()
    objectid = models.IntegerField()
    name = models.CharField(max_length=15)
    cobcode = models.CharField(max_length=5)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="County Boundaries")
    objects = models.GeoManager()  
    
    class Meta:
        app_label = 'analysis'  
    
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
    
    class Meta:
        app_label = 'analysis'   
    
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
    
    class Meta:
        app_label = 'analysis'   

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
    
    class Meta:
        app_label = 'analysis'   
    
class Lithology(models.Model):
    objectid = models.IntegerField()
    lith_inter = models.CharField(max_length=24)
    lithology = models.CharField(max_length=20)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Territorial Sea Lithology")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'
    
class Bathymetry(models.Model):
    depth = models.IntegerField() #formerly known as grid_code
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Bathymetry Polygon")
    objects = models.GeoManager()  
    
    class Meta:
        app_label = 'analysis'  
    
#Used for Biology Reports    
    
class PinnipedHaulouts(models.Model):
    objectid = models.IntegerField()
    location = models.CharField(max_length=254)
    site = models.CharField(max_length=254)
    lat = models.FloatField()
    lon = models.FloatField()
    generality = models.FloatField()
    pv_use = models.FloatField()
    ej_use = models.FloatField()
    zc_use = models.FloatField()
    ma_use = models.FloatField()
    pv_count = models.FloatField()
    ej_count = models.FloatField()
    zc_count = models.FloatField()
    ma_count = models.FloatField()
    ej_rookery = models.IntegerField()
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Pinniped Haulouts")
    objects = models.GeoManager() 
    
    class Meta:
        app_label = 'analysis'   
    
class SeabirdColonies(models.Model):
    objectid_1 = models.IntegerField()
    objectid = models.IntegerField()
    colno = models.CharField(max_length=15)
    colno_gis = models.CharField(max_length=10)
    complex = models.CharField(max_length=50)
    site_name = models.CharField(max_length=60)
    date = models.DateField()
    year = models.FloatField()
    dateinterp = models.CharField(max_length=1)
    observers = models.CharField(max_length=50)
    survtype = models.CharField(max_length=10)
    sp = models.CharField(max_length=4)
    species = models.CharField(max_length=40)
    tax_no = models.FloatField()
    actual_bir = models.FloatField()
    nonests = models.FloatField()
    est_no_bre = models.CharField(max_length=10)
    mostrecent = models.CharField(max_length=3)
    whatcount = models.CharField(max_length=3)
    esttype = models.CharField(max_length=3)
    convert = models.CharField(max_length=5, null=True, blank=True)
    reps = models.FloatField()
    qual = models.FloatField()
    dataent = models.DateField(null=True, blank=True)
    datahack = models.CharField(max_length=25, null=True, blank=True)
    biblno = models.FloatField()
    author = models.CharField(max_length=254)
    contact = models.CharField(max_length=100)
    document = models.CharField(max_length=100)
    year_pub = models.FloatField()
    cen_notes = models.CharField(max_length=254, null=True, blank=True)
    spnotes = models.CharField(max_length=254, null=True, blank=True)
    mapno = models.CharField(max_length=50)
    siteno = models.CharField(max_length=15)
    state = models.CharField(max_length=4)
    county = models.CharField(max_length=25)
    country = models.CharField(max_length=15)
    bcregion = models.FloatField()
    desc = models.CharField(max_length=254)
    datapg = models.FloatField()
    photo_inte = models.CharField(max_length=150, null=True, blank=True)
    use = models.CharField(max_length=3, null=True, blank=True)
    title = models.CharField(max_length=120)
    volume = models.CharField(max_length=10, null=True, blank=True)
    issue = models.CharField(max_length=10, null=True, blank=True)
    pages = models.CharField(max_length=15, null=True, blank=True)
    keywords = models.CharField(max_length=254, null=True, blank=True)
    utmx = models.FloatField()
    utmy = models.FloatField()
    cat07_mra = models.IntegerField()
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Seabird Colonies")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'
    
class Habitats(models.Model):
    objectid_1 = models.IntegerField()
    area = models.FloatField()
    perimeter = models.FloatField()
    orsghg3rp_field = models.IntegerField()
    orsghg3rp1 = models.IntegerField()
    or_sgh_v3_field = models.IntegerField()
    objectid_2 = models.IntegerField()
    or_sgh_v31 = models.FloatField()
    or_sgh_v_1 = models.FloatField()
    or_sgh_v_2 = models.IntegerField()
    or_sgh_v_3 = models.IntegerField()
    poly_field = models.IntegerField()
    subclass = models.CharField(max_length=13, null=True, blank=True)
    subclass_field = models.IntegerField()
    rings_ok = models.IntegerField()
    rings_nok = models.IntegerField()
    objectid = models.FloatField()
    structure = models.CharField(max_length=20)
    structure2 = models.CharField(max_length=20)
    geo_hab = models.CharField(max_length=10)
    properties = models.CharField(max_length=50, null=True, blank=True)
    geo_hab2 = models.CharField(max_length=15)
    sgh_prefix = models.CharField(max_length=5)
    sgh_lith1 = models.CharField(max_length=15)
    sgh_lith2 = models.CharField(max_length=15, null=True, blank=True)
    sgh_lith = models.CharField(max_length=30)
    sgh_combo = models.CharField(max_length=30)
    len = models.FloatField()
    shape_leng = models.FloatField()
    shape_le_1 = models.FloatField()
    shape_le_2 = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Seafloor Habitats")
    objects = models.GeoManager()    
    
    class Meta:
        app_label = 'analysis'    
'''    
class Habitats_old(models.Model):
    objectid_1 = models.IntegerField()
    objectid_2 = models.FloatField()
    objectid = models.FloatField()
    structure = models.CharField(max_length=20)
    structure2 = models.CharField(max_length=20, null=True, blank=True)
    geo_hab = models.CharField(max_length=10, null=True, blank=True)
    lithology = models.CharField(max_length=19, null=True, blank=True)
    lithology2 = models.CharField(max_length=20, null=True, blank=True)
    properties = models.CharField(max_length=50, null=True, blank=True)
    gravel = models.FloatField()
    sand = models.FloatField()
    silt = models.FloatField()
    clay = models.FloatField()
    num_sample = models.FloatField()
    sum = models.FloatField()
    f_area = models.FloatField()
    hab_type = models.CharField(max_length=40)
    area = models.FloatField()
    len = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Seafloor Habitats")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 
'''    
class KelpSurveys(models.Model):
    objectid = models.IntegerField()
    kelp90 = models.IntegerField()
    kelp96 = models.IntegerField()
    kelp97 = models.IntegerField()
    kelp98 = models.IntegerField()
    kelp99 = models.IntegerField()
    area = models.FloatField()
    perimeter = models.FloatField()
    acres = models.FloatField()
    hectares = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Kelp Surveys")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 
    
class GeologicalHabitat(models.Model):
    objectid_1 = models.IntegerField()
    area = models.FloatField()
    perimeter = models.FloatField()
    orsghg3rp_field = models.IntegerField()
    orsghg3rp1 = models.IntegerField()
    or_sgh_v3_field = models.IntegerField()
    objectid_2 = models.IntegerField()
    or_sgh_v31 = models.FloatField()
    or_sgh_v_1 = models.FloatField()
    or_sgh_v_2 = models.IntegerField()
    or_sgh_v_3 = models.IntegerField()
    poly_field = models.IntegerField()
    subclass = models.CharField(max_length=13, null=True, blank=True)
    subclass_field = models.IntegerField()
    rings_ok = models.IntegerField()
    rings_nok = models.IntegerField()
    objectid = models.FloatField()
    structure = models.CharField(max_length=20)
    structure2 = models.CharField(max_length=20)
    geo_hab = models.CharField(max_length=10)
    properties = models.CharField(max_length=50, null=True, blank=True)
    geo_hab2 = models.CharField(max_length=15)
    sgh_prefix = models.CharField(max_length=5)
    sgh_lith1 = models.CharField(max_length=15)
    sgh_lith2 = models.CharField(max_length=15, null=True, blank=True)
    sgh_lith = models.CharField(max_length=30)
    sgh_combo = models.CharField(max_length=30)
    len = models.FloatField()
    shape_leng = models.FloatField()
    shape_le_1 = models.FloatField()
    shape_le_2 = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Surficial Geological Habitats")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 
    
# Used for Human Considerations Reports
'''
###Outdated (updating from 2008 data to 2010 data)###
class StateParks(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=50)
    editdate = models.DateField(null=True, blank=True)
    editperson = models.CharField(max_length=25, null=True, blank=True)
    datasource = models.IntegerField()
    createdate = models.DateField(null=True, blank=True)
    retiredate = models.DateField(null=True, blank=True)
    gis_id = models.IntegerField()
    hub_id = models.IntegerField()
    creator = models.CharField(max_length=50, null=True, blank=True)
    designatio = models.CharField(max_length=50, null=True, blank=True)
    use_type = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Sate Parks")
    objects = models.GeoManager() 
    
    class Meta:
        app_label = 'analysis'   
'''
class StateParks(models.Model):
    name = models.CharField(max_length=50)
    gisacres = models.FloatField(null=True, blank=True)
    editdate = models.DateField(null=True, blank=True)
    editperson = models.CharField(max_length=25, null=True, blank=True)
    datasource = models.IntegerField()
    createdate = models.DateField(null=True, blank=True)
    retiredate = models.DateField(null=True, blank=True)
    gis_id = models.IntegerField()
    hub_id = models.IntegerField()
    creator = models.CharField(max_length=50, null=True, blank=True)
    designatio = models.CharField(max_length=50, null=True, blank=True)
    use_type = models.CharField(max_length=50, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Sate Parks 2010")
    objects = models.GeoManager()
    
    class Meta:
        app_label = 'analysis'   
    
class PublicAccess(models.Model):
    objectid = models.IntegerField()
    dat1 = models.FloatField()
    dat1_id = models.FloatField()
    siteid = models.FloatField()
    name = models.CharField(max_length=31) #formerly known as loc
    addr = models.CharField(max_length=8, null=True, blank=True)
    county = models.CharField(max_length=9)
    range = models.CharField(max_length=7, null=True, blank=True)
    town = models.CharField(max_length=6, null=True, blank=True)
    section = models.CharField(max_length=9, null=True, blank=True)
    taxlot = models.CharField(max_length=8, null=True, blank=True)
    lat = models.FloatField()
    lon = models.FloatField()
    char = models.CharField(max_length=8)
    rdendtp = models.CharField(max_length=10, null=True, blank=True)
    typeacc = models.CharField(max_length=10)
    status = models.CharField(max_length=10, null=True, blank=True)
    chtype = models.CharField(max_length=9, null=True, blank=True)
    prop = models.CharField(max_length=9, null=True, blank=True)
    map = models.CharField(max_length=9, null=True, blank=True)
    locpln = models.CharField(max_length=8, null=True, blank=True)
    pathbch = models.CharField(max_length=10)
    ramp = models.CharField(max_length=8)
    benken1 = models.IntegerField()
    photos = models.IntegerField()
    photoid = models.CharField(max_length=12, null=True, blank=True)
    ped = models.CharField(max_length=5, null=True, blank=True)
    veh = models.CharField(max_length=5, null=True, blank=True)
    boat = models.CharField(max_length=6, null=True, blank=True)
    visual = models.CharField(max_length=7, null=True, blank=True)
    owner = models.CharField(max_length=12)
    trail = models.CharField(max_length=6)
    stairs = models.CharField(max_length=7)
    handi = models.CharField(max_length=7)
    water = models.CharField(max_length=7)
    tabben = models.CharField(max_length=9)
    restrm = models.CharField(max_length=9)
    camping = models.CharField(max_length=10)
    shower = models.CharField(max_length=9)
    phone = models.CharField(max_length=7)
    kiosk = models.CharField(max_length=6)
    parking = models.CharField(max_length=9)
    numpk = models.CharField(max_length=10)
    fees = models.CharField(max_length=6)
    horse = models.CharField(max_length=7)
    orv = models.CharField(max_length=5)
    tidepl = models.CharField(max_length=7)
    whale = models.CharField(max_length=7)
    surf = models.CharField(max_length=6)
    bike = models.CharField(max_length=5)
    hiking = models.CharField(max_length=7)
    boating = models.CharField(max_length=9)
    offshore = models.CharField(max_length=11)
    rockhead = models.CharField(max_length=11)
    rocktide = models.CharField(max_length=10)
    bluff = models.CharField(max_length=7)
    dune = models.CharField(max_length=6)
    forest = models.CharField(max_length=8)
    wetland = models.CharField(max_length=10)
    bay = models.CharField(max_length=5, null=True, blank=True)
    river = models.CharField(max_length=6)
    lake = models.CharField(max_length=6)
    lthouse = models.CharField(max_length=9)
    bridge = models.CharField(max_length=8)
    waterfrt = models.CharField(max_length=11)
    jetty = models.CharField(max_length=7)
    marina = models.CharField(max_length=8)
    dock = models.CharField(max_length=6)
    comments = models.CharField(max_length=25, null=True, blank=True)
    mgmt = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Public Access Points")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 
    
class DMDSites(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=25)
    status = models.CharField(max_length=25, null=True, blank=True)
    river = models.CharField(max_length=20)
    use = models.CharField(max_length=25)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Dredge Material Disposal Sites")
    objects = models.GeoManager()  
    
    class Meta:
        app_label = 'analysis'  
    
class Outfalls(models.Model):
    objectid = models.IntegerField()
    facility_i = models.IntegerField()
    sic_code = models.IntegerField()
    legal_name = models.CharField(max_length=71)
    name = models.CharField(max_length=70) #formerly known as common_nam
    city = models.CharField(max_length=14)
    county = models.CharField(max_length=9)
    permit_typ = models.CharField(max_length=13)
    status = models.CharField(max_length=4)
    lat = models.FloatField()
    long = models.FloatField()
    fac_type = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    class_field = models.CharField(max_length=10)
    permit_no = models.IntegerField()
    epa_number = models.CharField(max_length=10)
    perm_descr = models.CharField(max_length=254)
    geometry = models.PointField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="NPDES Outfalls")
    objects = models.GeoManager() 
    
    class Meta:
        app_label = 'analysis'

class UnderseaCables(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=30)
    shape_leng = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Undersea Cables")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 
    
class Towlanes(models.Model):
    objectid = models.IntegerField()
    recnum = models.CharField(max_length=6)
    name = models.CharField(max_length=17)
    lat = models.CharField(max_length=12)
    lon = models.CharField(max_length=12)
    altitude = models.CharField(max_length=6)
    longname = models.CharField(max_length=17)
    lineclass = models.IntegerField()
    label = models.CharField(max_length=15)
    dateapplic = models.CharField(max_length=20, null=True, blank=True)
    shape_leng = models.FloatField()
    geometry = models.MultiLineStringField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Towlanes")
    objects = models.GeoManager() 
    
    class Meta:
        app_label = 'analysis'   
    
class WaveEnergyPermits(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=50) #formerly known as project
    company = models.CharField(max_length=30)
    contact = models.CharField(max_length=40)
    permit_no = models.IntegerField()
    county = models.CharField(max_length=40)
    location = models.CharField(max_length=30)
    app_date = models.DateField()
    ts = models.CharField(max_length=10, null=True, blank=True)
    no_devices = models.CharField(max_length=75)
    applicant = models.CharField(max_length=50)
    per_miles = models.FloatField()
    area_miles = models.FloatField()
    acres = models.FloatField()
    hectares = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Wave Energy Preliminary Permits")
    objects = models.GeoManager() 
    
    class Meta:
        app_label = 'analysis'
    
class MarineManagedAreas(models.Model):
    objectid = models.IntegerField()
    shape_leng = models.FloatField()
    name = models.CharField(max_length=75)
    shape_le_1 = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="State Marine Managed Areas")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis'

class FisheryClosures(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=50)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Fishery Closures")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 
    
class ConservationAreas(models.Model):
    objectid = models.IntegerField()
    name = models.CharField(max_length=50, null=True, blank=True) #formerly known as area_name
    prohibit = models.CharField(max_length=65, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, null=True, blank=True, verbose_name="Conservation Areas")
    objects = models.GeoManager()   
    
    class Meta:
        app_label = 'analysis' 