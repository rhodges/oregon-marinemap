from analysis.models import AESCache
from analysis.utils import ensure_type, type_is_hum

'''
Checks to see if cache for a given aes and type exists in AESCache table
'''
def aes_cache_exists(aes, type):
    type = ensure_type(type)
    try:
        cache = AESCache.objects.get(wkt_hash=aes.hash, type=type)
        return True
    except:
        return False

'''
Retrieves cache for a given aes and type from the AESCache table
'''
def get_aes_cache(aes, type):
    type = ensure_type(type)
    try:
        cache = AESCache.objects.get(wkt_hash=aes.hash, type=type)
        return cache.context
    except:
        from django.core.exceptions import ObjectDoesNotExist
        raise ObjectDoesNotExist("Cache object not found:  make sure aes_cache_exists() is called prior to calling get_aes_cache()")
    
    
'''
Creates and saves a cache entry for a given aes, type, and context from the AESCache table
'''
def create_aes_cache(aes, type, context):
    cache = AESCache()
    cache.type = ensure_type(type)
    cache.wkt_hash = aes.hash
    cache.context = context
    cache.save()
    
'''
Remove a single geometry or single geometry with type from the cache table
'''    
def remove_aes_cache(aes=None, type=None):
    if type is not None and ensure_type(type) is None:
        raise Exception("The type you entered is not a valid type.")
    type = ensure_type(type)
    if type is None and aes is None:
        raise Exception("For clearing all cached data, use clear_aes_cache instead.")
    elif type is None:
        #remove all entries with given geometry
        entries = AESCache.objects.filter(wkt_hash=aes.hash)
    elif aes is None:
        #remove all entries with given type
        entries = AESCache.objects.filter(type=type)
    else:
        #remove only the entry with the given type and the same geometry
        entries = AESCache.objects.filter(wkt_hash=aes.hash, type=type)
    #remove entries from AESCache
    for entry in entries:
        AESCache.delete(entry)
       
'''
Called from admin_clear_nsh_cache 
Ensures that when nsh cache is emptied that would also affect aes reports, that related aes cache is emptied as well
'''       
def remove_related_aes_cache(type=None):
    if type is None:
        remove_aes_cache(type='Geography')
        remove_aes_cache(type='Physical')
        remove_aes_cache(type='Biology')
    elif not type_is_hum(type):
        remove_aes_cache(type=type)        
       
'''
Clear all entries from cache table
'''    
def clear_aes_cache(i_am_sure=False):
    if not i_am_sure:
        raise Exception("I don't believe you really want to do this...convice me.")
    entries = AESCache.objects.all()
    for entry in entries:
        AESCache.delete(entry)
        
