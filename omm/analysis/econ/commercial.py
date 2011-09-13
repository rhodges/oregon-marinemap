from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import get_rasterstats, raster_exists, get_keys, update_ports, update_state_totals, get_value

default_value = '---'

port_names = [      'Astoria', 
                    'Garibaldi/Tillamook', 
                    'Depoe Bay', 
                    'Newport', 
                    'Florence', 
                    'SOORC Ports', 
                    'Port Orford', 
                    'Gold Beach & Brookings'  ]
                    
port_abbrs = {      'Astoria': 'astr', 
                    'Garibaldi/Tillamook': 'tllr', 
                    'Depoe Bay': 'dpor', 
                    'Newport': 'newr', 
                    'Florence': 'flrr', 
                    'SOORC Ports': 'srcr', 
                    'Port Orford': 'orfr', 
                    'Gold Beach & Brookings': 'bgdr' }

fisheries = [       ('Dungeness crab - trap', 'dcrabt'),
                    ('Hagfish - trap', 'hagt'), 
                    ('Pacific Halibut - longline', 'phall'), 
                    ('Petrale Sole - trawl', 'pshpt'), 
                    ('Rockfish - hook & line (dead)', 'rdead'), 
                    ('Rockfish - hook & line (live)', 'rlive'), 
                    ('Rockfish - longline (dead)', 'rdeadl'), 
                    ('Rockfish - longline (live)', 'rlivel'), 
                    ('Sablefish - trap', 'sabt'), 
                    ('Sablefish - longline', 'sabl'), 
                    ('Salmon - troll', 'salt'), 
                    ('Seaward RCA - trawl', 'srcat'), 
                    ('Shelf Bottom - trawl', 'shbt'), 
                    ('Urchin - dive', 'urchd'), 
                    ('Whiting - midwater trawl', 'wmidt')  ]                     

noaa_multipliers = {'dcrabt': 1.95, 
                    'hagt': 1.86, 
                    'phall': 1.86, 
                    'pshpt': 1.84, 
                    'rdead': 1.90, 
                    'rlive': 1.90, 
                    'rdeadl': 1.90, 
                    'rlivel': 1.90, 
                    'sabl': 1.90, 
                    'sabt': 1.90, 
                    'salt': 1.86, 
                    'srcat': 1.90, 
                    'shbt': 1.86, 
                    'urchd': 1.87, 
                    'wmidt': 1.90  } 

feam_multipliers = {'dcrabt': 1., 
                    'hagt': 1., 
                    'phall': 1., 
                    'pshpt': 1., 
                    'rdead': 1., 
                    'rlive': 1., 
                    'rdeadl': 1., 
                    'rlivel': 1., 
                    'sabl': 1., 
                    'sabt': 1., 
                    'salt': 1., 
                    'srcat': 1., 
                    'shbt': 1., 
                    'urchd': 1., 
                    'wmidt': 1.  }                     

   
'''
called by views.shoreside_analysis
Builds and returns a context dictionary for commercial fishing reports 
'''    
def get_commercial_context(aoi, type, prefix='com'):
    from econ_cache import *
    if econ_cache_exists(aoi, type):
        context = get_econ_cache(aoi, type)
        return context
    ports = []
    state_totals = []       
    for port_name in port_names:
        port_abbr = port_abbrs[port_name]
        for fishery, fishery_abbr in fisheries:
            raster_name = prefix + '_' + fishery_abbr + '_' + port_abbr
            if 'noaa' in type:
                multiplier = noaa_multipliers[fishery_abbr]
                agency = 'NOAA'
            elif 'feam' in type:
                multiplier = feam_multipliers[fishery_abbr]
                agency = 'FEAM'
            else:
                raise ValueError('%s is not a valid value for type parameter in get_commercial_context' %type)
            if raster_exists(raster_name):
                gross_revenue, total = get_rasterstats(aoi, raster_name, multiplier)
                fish_list = [fishery, multiplier, gross_revenue, total]
                if port_name in get_keys(ports):
                    update_ports(ports, port_name, fish_list)
                else:
                    ports.append((port_name, [fish_list]))
                if fishery in get_keys(state_totals):
                    update_state_totals(state_totals, fishery, (multiplier, gross_revenue, total))
                else:
                    state_totals.append((fishery, [multiplier, gross_revenue, total]))
        state_totals.sort()
    context = {type: {'aoi': aoi, 'agency': agency, 'default_value': default_value, 'ports': ports, 'state_totals': state_totals, 'pdf': False, 'printable': False}}
    create_econ_cache(aoi, type, context)
    return context
    