from lingcod.raster_stats.models import RasterDataset, zonal_stats


'''
'''    
def get_rasterstats(aoi, name, multiplier=1):
    raster = RasterDataset.objects.get(name=name)
    rasterstats = zonal_stats(aoi.geometry_final, raster)
    gross_revenue = rasterstats.sum
    total = gross_revenue * multiplier
    return gross_revenue, total
    
def raster_exists(name):
    try:
        RasterDataset.objects.get(name=name)
        return True
    except:
        return False
        
def get_keys(tuple_list):
    return [x for x,y in tuple_list]
    
def update_ports(ports, port_name, fish_list):
    old_fishlist = get_value(ports, port_name)
    old_fishlist.append(fish_list)
    
def update_state_totals(state_totals, key, values):
    old_values = get_value(state_totals, key)
    old_values[1] += values[1]
    old_values[2] += values[2]
    
def get_value(tuple_list, key):
    for x,y in tuple_list:
        if x == key:
            return y
    return None 
    