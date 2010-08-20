from analysis.models import NSHCache

'''
Checks to see if cache for a given nsh and type exists in NSHCache table
'''
def has_cache(nsh, type):
    try:
        cache = NSHCache.objects.get(wkt_hash=nsh.geometry_final.wkt.__hash__(), type=type)
        return True
    except:
        return False

'''
Retrieves cache for a given nsh and type from the NSHCache table
'''
def get_cache(nsh, type):
    try:
        cache = NSHCache.objects.get(wkt_hash=nsh.geometry_final.wkt.__hash__(), type=type)
        return cache.context
    except:
        from django.core.exceptions import ObjectDoesNotExist
        raise ObjectDoesNotExist("Cache object not found:  make sure has_cache() is called prior to calling get_cache()")
    
'''
Creates and saves a cache entry for a given nsh, type, and context from the NSHCache table
'''
def create_cache(nsh, type, context):
    cache = NSHCache()
    cache.type = type
    cache.wkt_hash = nsh.geometry_final.wkt.__hash__()
    cache.context = context
    cache.save()
    
'''
Remove a single geometry or single geometry with type from the cache table
'''    
def remove_cache(nsh, type=None):
    if type is None:
        #remove all entries with same geometry
        entries = NSHCache.objects.filter(wkt_hash=nsh.geometry_final.wkt.__hash__())
    else:
        #remove only the entry with the given type and the same geometry
        entries = NSHCache.objects.filter(wkt_hash=nsh.geometry_final.wkt.__hash__(), type=type)
    for entry in entries:
        NSHCache.delete(entry)
    
'''
Remove all entries from cache table that have a particular type (Geography, Physical, Biological, or Human)
'''    
def remove_cache_of_type(type):
    entries = NSHCache.objects.filter(type=type)
    for entry in entries:
        NSHCache.delete(entry)
    
'''
Clear all entries from cache table
'''    
def clear_cache(i_am_sure=False):
    if not i_am_sure:
        raise Exception("I don't believe you really want to do this...convice me.")
    entries = NSHCache.objects.all()
    for entry in entries:
        NSHCache.delete(entry)
        