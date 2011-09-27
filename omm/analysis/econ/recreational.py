from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import get_rasterstats, raster_exists, get_keys, update_ports, update_state_totals, get_value
from econ_data.recreational_data import port_names, port_abbrs, fisheries, multipliers, rec_totals

default_value = '---'
 
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
                fishery_total = rec_totals[port_abbr][fishery_abbr]
                percentage = gross_revenue / fishery_total
                fish_list = [fishery, multiplier, gross_revenue, total, percentage]
                if port_name in get_keys(ports):
                    update_ports(ports, port_name, fish_list)
                else:
                    ports.append((port_name, [fish_list]))
                if fishery in get_keys(state_totals):
                    update_state_totals(state_totals, fishery, (multiplier, gross_revenue, total))
                else:
                    state_totals.append((fishery, [multiplier, gross_revenue, total]))
        state_totals.sort()
    add_state_percentages(state_totals)
    context = {type: {'aoi': aoi, 'default_value': default_value, 'ports': ports, 'state_totals': state_totals, 'pdf': False, 'printable': False}}
    create_econ_cache(aoi, type, context)
    return context
    
def add_state_percentages(state_totals):
    for tuple in state_totals:
        fishery_abbr = get_fishery_abbr(tuple[0])
        statewide_total = rec_totals['state'][fishery_abbr]
        percentage = tuple[1][1] / statewide_total
        tuple[1].append(percentage)
    
def get_fishery_abbr(fishery_name):
    for fishery in fisheries:
        if fishery[0] == fishery_name:
            return fishery[1]
    raise ValueError('incorrect value, %s, sent to get_fishery_abbr in recreational.py' % fishery_name)