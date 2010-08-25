from django.http import HttpResponse
from NSH_Geography import display_geo_analysis
from NSH_Physical import display_phy_analysis
from NSH_Biology import display_bio_analysis
from NSH_Human import display_hum_analysis
from utils import type_is_geo, type_is_phy, type_is_bio, type_is_hum


def display_nsh_analysis(request, nsh_id, type):
    if type_is_geo(type):
        return display_geo_analysis(request, nsh_id)
    elif type_is_phy(type):
        return display_phy_analysis(request, nsh_id)
    elif type_is_bio(type): 
        return display_bio_analysis(request, nsh_id)
    else: #must be Human Uses
        return display_hum_analysis(request, nsh_id)
    
def print_nsh_report(request, nsh, type, template=None):
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    if type_is_geo(type):
        template='printable_nsh_geo_report.html'
    elif type_is_phy(type):
        template='printable_nsh_phy_report.html'
    elif type_is_bio(type):
        template='printable_nsh_bio_report.html'
    elif type_is_hum(type):
        template='printable_nsh_hum_report.html'
    else:
        template='printable_nsh_comprehensive_report.html'    
    context = get_or_create_cache(nsh, type)
    return render_to_response(template, RequestContext(request, context))
    
      
def get_or_create_cache(nsh, type):
    from NSH_Cache import has_cache, get_cache, create_cache
    from NSH_Geography import run_geo_analysis
    from NSH_Physical import run_phy_analysis
    from NSH_Biology import run_bio_analysis
    from NSH_Human import run_hum_analysis
    if type == 'all':
        all_context = {}
        for single_type in ['geo', 'phy', 'bio', 'hum']:
            if has_cache(nsh, single_type):
                context = get_cache(nsh, single_type)
            else:
                context = run_geo_analysis(nsh)
                create_cache(nsh, single_type, context)
            all_context[single_type] = context
        return all_context
    elif has_cache(nsh, type):
        return get_cache(nsh, type)
    elif type == 'geo':
        context = run_geo_analysis(nsh)
    elif type == 'phy':
        context = run_phy_analysis(nsh)
    elif type == 'bio':
        context = run_bio_analysis(nsh)
    elif type == 'hum':
        context = run_hum_analysis(nsh)
    create_cache(nsh, type, context)
    return context
        