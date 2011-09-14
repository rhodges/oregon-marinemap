from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, default_value
from aes_cache import aes_cache_exists, get_aes_cache, create_aes_cache
from analysis.nsh.nsh_biology import get_nsh_bio_context
from analysis.nsh.nsh_cache import nsh_cache_exists, get_nsh_cache


'''
Runs analysis for Biological report
Renders the Biological Report template
Called by aes_Analysis.display_aes_analysis
'''
def display_bio_analysis(request, aes, type='Biology', template='aes_bio_report.html'):
    type = ensure_type(type)
    context = get_aes_bio_context(aes, type)
    return render_to_response(template, RequestContext(request, context)) 

'''
Called from display_aes_geo_analysis, and aes_analysis.
'''    
def get_aes_bio_context(aes, type): 
    #get context from cache or from running analysis
    if aes_cache_exists(aes, type):
        #retrieve context from cache
        context = get_aes_cache(aes, type)
    else:
        #get nsh context from cache or from running analysis
        nsh_context = get_nsh_bio_context(aes, type)  
        #get context by running analysis
        aes_context = run_aes_bio_analysis(aes, type) 
        #merge nsh and aes context
        context = dict(nsh_context.items() + aes_context.items()) 
        #cache these results
        create_aes_cache(aes, type, context) 
    return context    
     
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_aes_bio_analysis(aes, type): 
    #compile context
    context = {'aes': aes}
    #cache these results
    create_aes_cache(aes, type, context)   
    return context
        