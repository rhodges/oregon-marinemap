from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import get_rasterstats, raster_exists, get_keys, update_ports, update_state_totals, get_value

default_value = '---'
 
'''
called by views.shoreside_analysis
Builds and returns a context dictionary for commercial fishing reports 
'''    
def get_shoreside_context(aoi, type):
    if type == 'com':
        from commercial import port_names, port_abbrs, fisheries, multipliers
    elif type == 'chrt':
        from charter import ports, port_abbrs, fisheries, multipliers
    elif type == 'rec':
        from recreational import ports, port_abbrs, fisheries, multipliers
    else:
        raise ValueError('%s is not a valid shoreside fishery type' %type)
    ports = []
    state_totals = []      
    for port_name in port_names:
        port_abbr = port_abbrs[port_name]
        for fishery, fishery_abbr in fisheries:
            raster_name = fishery_abbr + '_' + port_abbr
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
    context = {'aoi': aoi, 'default_value': default_value, 'ports': ports, 'state_totals': state_totals}
    return context
    