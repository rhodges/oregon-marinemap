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

feam_multipliers = {'astr':{'dcrabt': 1.5, 
                            'hagt': 1.76, 
                            'phall': 1.44, 
                            'pshpt': 1.56, 
                            'rdead': 1.43, 
                            'rlive': 1.25, 
                            'rdeadl': 1.87,
                            'rlivel': 1.,   #not included
                            'sabl': 1.4, 
                            'sabt': 1.4, 
                            'salt': 1.38, 
                            'srcat': 1.95, 
                            'shbt': 2.05, 
                            'wmidt': 3.2  },
                    'tllr':{'dcrabt': 1.23, 
                            'hagt': 1.66, 
                            'phall': 1.28, 
                            'pshpt': 1.33, 
                            'rdead': 1.21, 
                            'rlive': 1.1, 
                            'rdeadl': 1.59, 
                            'sabl': 1.19, 
                            'sabt': 1.22, 
                            'salt': 1.1, 
                            'srcat': 1.39, 
                            'shbt': 1.29, 
                            'urchd': 1.23 },
                    'dpor':{'dcrabt': 1.33,
                            'phall': 1.42, 
                            'rdead': 1.41, 
                            'rlive': 1.2,
                            'salt': 1.67,
                            'urchd': 1.24 },
                    'newr':{'dcrabt': 1.43, 
                            'hagt': 1.75, 
                            'phall': 1.37, 
                            'pshpt': 1.5, 
                            'rdead': 1.32, 
                            'rlive': 1.26, 
                            'rdeadl': 1.36, 
                            'sabl': 1.29, 
                            'sabt': 1.3, 
                            'salt': 1.68, 
                            'srcat': 1.73, 
                            'shbt': 1.8, 
                            'urchd': 1.24, 
                            'wmidt': 3.69 },
                    'flrr':{'dcrabt': 1.17, 
                            'phall': 1.34, 
                            'sabl': 1.18, 
                            'sabt': 1.3, 
                            'salt': 2.66, 
                            'srcat': 1.8 },
                    'srcr':{'dcrabt': 1.22,#avg 
                            'hagt': 1.86, 
                            'phall': 1.37, #avg
                            'pshpt': 1.31, #ignored state value
                            'rdead': 1.19, #ignored state value
                            'rlive': 1.21, 
                            'rdeadl': 1.23,#ignored state value
                            'rlivel': 1.21, 
                            'sabl': 1.18,  #avg - same
                            'sabt': 1.17,  #avg - same
                            'salt': 2.66,  #avg
                            'srcat': 1.38, 
                            'shbt': 1.41, 
                            'urchd': 1.22, 
                            'wmidt': 4.2  },
                    'orfr':{'dcrabt': 1.12, 
                            'hagt': 1.73, 
                            'phall': 1.13, 
                            'rdead': 1.17, 
                            'rlive': 1.11, 
                            'rdeadl': 1.17, 
                            'rlivel': 1.11, 
                            'sabl': 1.12, 
                            'sabt': 1.12, 
                            'salt': 2.5,
                            'urchd': .93 },
                    'bgdr':{'dcrabt': 1.11, #avg
                            'phall': 1.12, 
                            'pshpt': 1.14, 
                            'rdead': 1.15,  #avg 
                            'rlive': 1.11,  #avg - same
                            'rdeadl': 1.12, #ignored state value 
                            'rlivel': 1.11, #avg - same
                            'sabl': 1.12,   #ignored state value 
                            'sabt': 1.12,   
                            'salt': 2.52,   #ignored state value 
                            'srcat': 1.23, 
                            'shbt': 1.89, 
                            'urchd': 1.55 }
                    }
                    

   
'''
called by views.shoreside_analysis
Builds and returns a context dictionary for commercial fishing reports 
'''    
def get_commercial_context(aoi, type, prefix='com'):
    from econ_cache import econ_cache_exists, get_econ_cache, create_econ_cache
    if econ_cache_exists(aoi, type):
        context = get_econ_cache(aoi, type)
        return context
    ports = []
    state_totals = []       
    for port_name in port_names:
        port_abbr = port_abbrs[port_name]
        for fishery, fishery_abbr in fisheries:
            raster_name = prefix + '_' + fishery_abbr + '_' + port_abbr
            if raster_exists(raster_name):
                if 'noaa' in type:
                    multiplier = noaa_multipliers[fishery_abbr]
                    agency = 'NOAA'
                elif 'feam' in type:
                    multiplier = feam_multipliers[port_abbr][fishery_abbr]
                    agency = 'FEAM'
                else:
                    raise ValueError('%s is not a valid value for type parameter in get_commercial_context' %type)
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
    