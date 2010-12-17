from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, default_value, get_intersecting_geometries, get_distance_to_nearest_geometry
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
    #get stellar sea lion critical habitat details
    num_sealion_habs, sealion_habs = get_sealion_habitats(aes)
    #get seagrass area
    seagrass_area = get_seagrass_area(aes)
    #get green sturgeon data (yes/no and percentage)
    green_sturgeon, green_sturgeon_perc = get_green_sturgeon_data(aes)
    #get distance to nearest western snowy plover critical habitat
    nearest_snowy_plover = distance_to_snowy_plover(aes)
    #get distance to nearest marbled murrelet critical habitat
    nearest_marbled_murrelet = distance_to_marbled_murrelet(aes)
    #get nearest coho populated stream
    nearest_coho_stream = get_nearest_coho_stream(aes)
    #compile context
    context = {'aes': aes, 'default_value': default_value, 'area_units': settings.DISPLAY_AREA_UNITS, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'num_sealion_habs': num_sealion_habs, 'sealion_habs': sealion_habs, 'seagrass_area': seagrass_area, 'green_sturgeon': green_sturgeon, 'green_sturgeon_perc': green_sturgeon_perc, 'nearest_snowy_plover': nearest_snowy_plover, 'nearest_marbled_murrelet': nearest_marbled_murrelet, 'nearest_coho_stream': nearest_coho_stream}
    #cache these results
    create_aes_cache(aes, type, context)   
    return context
        
def get_nearest_coho_stream(aes):
    coho_streams = Coho.objects.all()
    distances = [stream.geometry.distance(aes.geometry_final) for stream in coho_streams if stream.geometry.buffer(60000).intersects(aes.geometry_final)]
    distances.sort()
    return length_in_display_units(distances[0])
        
def distance_to_marbled_murrelet(aes):
    #murrelets = MarbledMurrelet.objects.all()
    #distances = [hab.geometry.centroid.distance(aes.geometry_final) for hab in murrelets]
    #distances.sort()
    distance = get_distance_to_nearest_geometry(aes, 'marbledmurrelet')
    return length_in_display_units(distance)

def distance_to_snowy_plover(aes):
    #snowy_plovers = SnowyPlover.objects.all()
    #distances = [hab.geometry.centroid.distance(aes.geometry_final) for hab in snowy_plovers]
    #distances.sort()
    distance = get_distance_to_nearest_geometry(aes, 'snowyplover')
    return length_in_display_units(distance)
    
def get_green_sturgeon_data(aes):
    coastal_overlaps = get_intersecting_geometries(aes, 'sturgeoncoastal')
    estuary_overlaps = get_intersecting_geometries(aes, 'sturgeonestuaries')
    if len(coastal_overlaps) > 0 or len(estuary_overlaps) > 0:
        presence = 'Yes'
    else:
        presence = 'No'
    aes_area = aes.geometry_final.area
    coastal_overlap_area = sum([overlap.area for overlap in coastal_overlaps])
    estuary_overlap_area = sum([overlap.area for overlap in estuary_overlaps])
    overlap_area = coastal_overlap_area + estuary_overlap_area
    overlap_area_percentage = overlap_area / aes_area * 100
    return presence, overlap_area_percentage
    
 
def get_sealion_habitats(aes):
    sealion_habitats = StellerHabitats.objects.all()
    inter_habs = [hab for hab in sealion_habitats if hab.geometry.intersects(aes.geometry_final)==True]
    hab_tuples = [(hab.name, hab.type) for hab in inter_habs if hab.geometry.intersects(aes.geometry_final)==True]
    hab_tuples.sort()
    num_habs = len(hab_tuples)
    return num_habs, hab_tuples
        
    
def get_seagrass_area(aes):
    seagrass = Seagrass.objects.all()
    inter_grass = [grass for grass in seagrass if grass.geometry.intersects(aes.geometry_final)==True]
    area_of_intersect = 0.0
    for grass in inter_grass:
        area_of_intersect += grass.geometry.intersection(aes.geometry_final).area
    area_of_intersect_converted_units = area_in_display_units(area_of_intersect)
    return area_of_intersect_converted_units
   