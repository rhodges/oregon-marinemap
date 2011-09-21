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
                    ('Petrale Sole - trawl', 'psolet'), 
                    ('Pink Shrimp - trawl', 'pshpt'),
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
                    'psolet': 1.9,
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

#the following are gleaned from the '110921 FEAM Economic Factors Final.xlsx' doc
feam_multipliers = {'astr':{'dcrabt': 1.5, 
                            'hagt': 1.77, 
                            'phall': 1.45,  
                            'psolet': 1.44,
                            'pshpt': 1.94, 
                            'rdead': 2.28, 
                            'rlive': 1.26, 
                            'rdeadl': 2.28,
                            'rlivel': 1.26,   
                            'sabl': 1.4, 
                            'sabt': 1.4, 
                            'salt': 1.38, 
                            'srcat': 2., 
                            'shbt': 2., 
                            'wmidt': 3.22  },  
                    'tllr':{'dcrabt': 1.24, 
                            'hagt': 1.67, 
                            'phall': 1.28,  
                            'psolet': 1.28,
                            'pshpt': 1.55, 
                            'rdead': 1.23, 
                            'rlive': 1.09, 
                            'rdeadl': 1.23, 
                            'sabl': 1.22, 
                            'sabt': 1.22, 
                            'salt': 1.1, 
                            'srcat': 1.37, 
                            'shbt': 1.37, 
                            'urchd': 1.24 },
                    'dpor':{'dcrabt': 1.44,
                            'phall': 1.37,  
                            'psolet': 1.4,
                            'rdead': 1.55, 
                            'rlive': 1.25,
                            'salt': 1.3,
                            'urchd': 1.24 },
                    'newr':{'dcrabt': 1.44, 
                            'hagt': 1.76, 
                            'phall': 1.37,  
                            'psolet': 1.4,
                            'pshpt': 1.89, 
                            'rdead': 1.55, 
                            'rlive': 1.25, 
                            'rdeadl': 1.55, 
                            'sabl': 1.29, 
                            'sabt': 1.29, 
                            'salt': 1.3, 
                            'srcat': 1.75, 
                            'shbt': 1.75, 
                            'urchd': 1.24, 
                            'wmidt': 3.71 },
                    'flrr':{'dcrabt': 1.23, 
                            'phall': 1.38,  
                            'psolet': 1.27,
                            'sabl': 1.18, 
                            'sabt': 1.18, 
                            'salt': 1.23, 
                            'srcat': 1.4 },
                    'srcr':{'dcrabt': 1.23,
                            'hagt': 1.86, 
                            'phall': 1.38,  
                            'psolet': 1.27,
                            'pshpt': 1.96, 
                            'rdead': 1.29, 
                            'rlive': 1.21, 
                            'rdeadl': 1.29,
                            'rlivel': 1.21, 
                            'sabl': 1.18,  
                            'sabt': 1.18,  
                            'salt': 1.23,  
                            'srcat': 1.4, 
                            'shbt': 1.41, 
                            'urchd': 1.22, 
                            'wmidt': 4.21  },
                    'orfr':{'dcrabt': 1.12, 
                            'hagt': 1.73, 
                            'phall': 1.14,  
                            'psolet': 1.13,
                            'rdead': 1.18, 
                            'rlive': 1.12, 
                            'rdeadl': 1.18, 
                            'rlivel': 1.12, 
                            'sabl': 1.13, 
                            'sabt': 1.13, 
                            'salt': 1.09,
                            'urchd': .94 },
                    'bgdr':{'dcrabt': 1.12, 
                            'phall': 1.14,  
                            'psolet': 1.13,
                            'pshpt': 1.18, 
                            'rdead': 1.18,   
                            'rlive': 1.12,  
                            'rdeadl': 1.18,  
                            'rlivel': 1.12, 
                            'sabl': 1.13,    
                            'sabt': 1.13,   
                            'salt': 1.09,    
                            'srcat': 1.23, 
                            'shbt': 1.23, 
                            'urchd': .94 },
                    'statewide':
                           {'dcrabt': 1.75, 
                            'hagt': 2.17, 
                            'phall': 1.61,  
                            'psolet': 1.74,
                            'pshpt': 2.32, 
                            'rdead': 1.94, 
                            'rlive': 1.47, 
                            'rdeadl': 1.94, 
                            'rlivel': 1.47,
                            'sabl': 1.59, 
                            'sabt': 1.59, 
                            'salt': 1.53, 
                            'srcat': 2.26, 
                            'shbt': 2.26, 
                            'urchd': 1.55, 
                            'wmidt': 4.42 },
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
                    statewide_multiplier = feam_multipliers['statewide'][fishery_abbr]
                    agency = 'FEAM'
                else:
                    raise ValueError('%s is not a valid value for type parameter in get_commercial_context' %type)
                gross_revenue, total = get_rasterstats(aoi, raster_name, multiplier)
                fish_list = [fishery, multiplier, gross_revenue, total]
                if port_name in get_keys(ports):
                    update_ports(ports, port_name, fish_list)
                else:
                    ports.append((port_name, [fish_list]))
                #update statewide totals 
                if fishery in get_keys(state_totals):
                    if 'feam' in type:
                        total = gross_revenue * statewide_multiplier
                    update_state_totals(state_totals, fishery, (multiplier, gross_revenue, total))
                else:
                    if 'feam' in type:
                        total = gross_revenue * statewide_multiplier
                    state_totals.append((fishery, [multiplier, gross_revenue, total]))
        state_totals.sort()
    context = {type: {'aoi': aoi, 'agency': agency, 'default_value': default_value, 'ports': ports, 'state_totals': state_totals, 'pdf': False, 'printable': False}}
    create_econ_cache(aoi, type, context)
    return context
    