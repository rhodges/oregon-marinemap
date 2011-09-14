from analysis.models import EconCache
from analysis.utils import ensure_type, type_is_hum

'''
Checks to see if cache for a given aoi and type exists in EconCache table
'''
def econ_cache_exists(aoi, type):
    try:
        cache = EconCache.objects.get(wkt_hash=aoi.hash, type=type)
        return True
    except:
        return False

'''
Retrieves cache for a given aoi and type from the EconCache table
'''
def get_econ_cache(aoi, type):
    try:
        cache = EconCache.objects.get(wkt_hash=aoi.hash, type=type)
        return cache.context
    except:
        from django.core.exceptions import ObjectDoesNotExist
        raise ObjectDoesNotExist("Cache object not found:  make sure econ_cache_exists() is called prior to calling get_econ_cache()")
    
    
'''
Creates and saves a cache entry for a given aoi, type, and context from the EconCache table
'''
def create_econ_cache(aoi, type, context):
    cache = EconCache()
    cache.aoi_id = aoi.id
    cache.type = type
    cache.wkt_hash = aoi.hash
    cache.context = context
    cache.save()
    
'''
Remove a single geometry or single geometry with type from the cache table
'''    
def remove_econ_cache(aoi=None, type=None):
    if type is not None and ensure_type(type) is None:
        raise Exception("The type you entered is not a valid type.")
    if type is None and aoi is None:
        raise Exception("For clearing all cached data, use clear_econ_cache instead.")
    elif type is None:
        #remove all entries with given geometry
        entries = EconCache.objects.filter(wkt_hash=aoi.hash)
    elif aoi is None:
        #remove all entries with given type
        entries = EconCache.objects.filter(type=type)
    else:
        #remove only the entry with the given type and the same geometry
        entries = EconCache.objects.filter(wkt_hash=aoi.hash, type=type)
    #remove entries from EconCache
    for entry in entries:
        EconCache.delete(entry)
       
'''
Called from admin_clear_nsh_cache 
Ensures that when cache is emptied that would affect other reports from same aoi, related econ cache is emptied as well
'''       
def remove_related_econ_cache(type=None):
    if type is None:
        remove_econ_cache(type='com-noaa')
        remove_econ_cache(type='com-feam')
        remove_econ_cache(type='chrt')
        remove_econ_cache(type='rec')
    elif not type_is_hum(type):
        remove_econ_cache(type=type)        
       
'''
Clear all entries from cache table
'''    
def clear_econ_cache(i_am_sure=False):
    if not i_am_sure:
        raise Exception("I don't believe you really want to do this...convice me.")
    entries = EconCache.objects.all()
    for entry in entries:
        EconCache.delete(entry)
        
