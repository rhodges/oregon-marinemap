from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import get_rasterstats, raster_exists, get_keys, update_ports, update_state_totals, get_value

default_value = '---'
port_names = ['Astoria', 'Garibaldi/Tillamook', 'Salmon River', 'Depoe Bay', 'Newport', 'Florence', 'SOORC Ports', 'Gold Beach & Brookings']
port_abbrs = {  'Astoria': 'astr', 
                'Garibaldi/Tillamook': 'tllr', 
                'Salmon River': 'slmr', 
                'Depoe Bay': 'dpor', 
                'Newport': 'newr', 
                'Florence': 'flrr', 
                'SOORC Ports': 'srcr', 
                'Gold Beach & Brookings': 'bgdr' }

fisheries = [   #('Dungeness crab - trap', 'dcrab'),
                ('Flatfish - trap', 'flat'), 
                ('Pacific Halibut - longline', 'phal'),
                ('Rockfish - hook & line (dead)', 'rckf'),
                ('Salmon - troll', 'sal') ]                     

multipliers = { 'dcrab': 1., 
                'flat': 1., 
                'phal': 1., 
                'rckf': 1., 
                'sal': 1.  } 
 
'''
called by views.shoreside_analysis
Builds and returns a context dictionary for recreational fishing reports 
'''   
def get_recreational_context(aoi, type='rec', prefix='rec'):
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
            multiplier = multipliers[fishery_abbr]
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
    context = {type: {'aoi': aoi, 'default_value': default_value, 'ports': ports, 'state_totals': state_totals, 'pdf': False, 'printable': False}}
    create_econ_cache(aoi, type, context)
    return context
    