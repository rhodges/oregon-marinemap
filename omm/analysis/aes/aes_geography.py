from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import area_in_display_units, length_in_display_units
from analysis.utils import ensure_type, get_nearest_geometries_with_distances, get_intersecting_shape_names, default_value
from aes_cache import aes_cache_exists, get_aes_cache, create_aes_cache
from analysis.nsh.nsh_geography import get_nsh_geo_context
from analysis.nsh.nsh_cache import nsh_cache_exists, get_nsh_cache


'''
Runs analysis for Geographic report
Renders the Geographic Report template
Called by AES_Analysis.display_aes_analysis
'''
def display_aes_geo_analysis(request, aes, type='Geography', template='aes_geo_report.html'):
    type = ensure_type(type)
    context = get_aes_geo_context(aes, type)
    return render_to_response(template, RequestContext(request, context)) 
    
'''
Called from display_aes_geo_analysis, and aes_analysis.
'''    
def get_aes_geo_context(aes, type):
    #get context from cache or from running analysis
    if aes_cache_exists(aes, type):
        #retrieve context from cache
        context = get_aes_cache(aes, type)
    else:
        #get nsh context from cache or from running analysis
        nsh_context = get_nsh_geo_context(aes, type)  
        #get context by running analysis
        aes_context = run_aes_geo_analysis(aes, type) 
        #merge nsh and aes context
        context = dict(nsh_context.items() + aes_context.items()) 
        #cache these results
        create_aes_cache(aes, type, context) 
    return context
    
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_aes_geo_analysis(aes, type):
    #get distance to nearest railroad
    railroad = get_distance_to_nearest_railroad(aes)
    #get nearest 3 marinas
    marinas = get_nearest_marinas(aes)
    #get nearest 3 substations
    substations = get_nearest_substations(aes)
    #get distance to nearest transmission line (1993 lines)
    transmissionline1993 = get_distance_to_nearest_transmissionline1993(aes)
    #get distance to nearest transmission line (2010 lines)
    transmissionline2010 = get_distance_to_nearest_transmissionline2010(aes)
    #visible from shore
    visible = is_visible_from_shore(aes)
    #compile context
    context = {'aes': aes, 'railroad': railroad, 'marinas': marinas, 'substations': substations, 'transmissionline1993': transmissionline1993, 'transmissionline2010': transmissionline2010, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'visible': visible}
    return context
    
    
'''
'''
def get_distance_to_nearest_railroad(aes):
    railroads = Railroads.objects.all()
    distances = [rail.geometry.distance(aes.geometry_final) for rail in railroads]
    distances.sort()
    distance = length_in_display_units(distances[0])
    return distance 
    
   
'''
Determines the Nearest 3 Ports (in order of proximity) for the given energy site shape
Called by display_aes_geo_analysis
'''    
def get_nearest_marinas(aes):
    return get_nearest_geometries_with_distances(aes, 'marinas')
    
'''
Determines the Nearest 3 Electrical Substations (in order of proximity) for the given energy site shape
Called by display_aes_geo_analysis
'''    
def get_nearest_substations(aes):
    return get_nearest_geometries_with_distances(aes, 'substations', point=True)
      
'''
'''
def get_distance_to_nearest_transmissionline1993(aes):
    lines = TransmissionLines1993.objects.all()
    distances = [line.geometry.distance(aes.geometry_final) for line in lines if line.geometry is not None]
    distances.sort()
    distance = length_in_display_units(distances[0])
    return distance 
    
'''
'''
def get_distance_to_nearest_transmissionline2010(aes):
    nearest_line = get_nearest_geometries_with_distances(aes, 'transmissionlines2010', length=1)
    return nearest_line
    
'''
'''
def is_visible_from_shore(aes):
    viewsheds = Viewsheds.objects.all()
    intersections = [viewshed for viewshed in viewsheds if viewshed.geometry.intersects(aes.geometry_final)==True]
    if len(intersections) > 0:
        return 'Yes'
    else:
        return 'No'
        
  