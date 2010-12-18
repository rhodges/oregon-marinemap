from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, get_nearest_geometries, get_nearest_geometries_with_distances, get_intersecting_shape_names, default_value
from aes_cache import aes_cache_exists, get_aes_cache, create_aes_cache
from analysis.nsh.nsh_human import get_nsh_hum_context
from analysis.nsh.nsh_cache import nsh_cache_exists, get_nsh_cache
    

'''
Runs analysis for Human Considerations report
Renders the Human Considerations Report template
Called by aes_Analysis.display_aes_analysis
'''
def display_aes_hum_analysis(request, aes, type='Human', template='aes_hum_report.html'):
    type = ensure_type(type)
    context = get_aes_hum_context(aes, type)
    return render_to_response(template, RequestContext(request, context)) 

'''
Called from display_aes_geo_analysis, and aes_analysis.
'''    
def get_aes_hum_context(aes, type): 
    #get context from cache or from running analysis
    if aes_cache_exists(aes, type):
        #retrieve context from cache
        context = get_aes_cache(aes, type)
    else:
        #get nsh context from cache or from running analysis
        nsh_context = get_nsh_hum_context(aes, type)  
        #get context by running analysis
        aes_context = run_aes_hum_analysis(aes, type) 
        #merge nsh and aes context
        context = dict(nsh_context.items() + aes_context.items()) 
        #cache these results
        create_aes_cache(aes, type, context) 
    return context    
     
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_aes_hum_analysis(aes, type): 
    #get all intersecting airports or nearest single airport
    intersecting_airports, nearest_airport = get_airport_data(aes)
    #get nearest urban growth boundaries
    nearest_ugbs = get_nearest_ugbs(aes)
    #get intersecting protected areas and 1 nearest protected area
    intersecting_protected_areas, nearest_protected_area = get_protected_areas_data(aes)
    #get intersecting or nearest buoys
    buoy_data = get_buoy_data(aes)
    #get intersecting or nearest beacons
    beacon_data = get_beacon_data(aes)
    #get intersecting or nearest signal equipment
    signal_data, num_signals = get_signal_data(aes)
    #compile context
    context = {'aes': aes, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'intersecting_airports': intersecting_airports, 'nearest_airport': nearest_airport, 'urbangrowthboundaries': nearest_ugbs, 'intersecting_protected_areas': intersecting_protected_areas, 'nearest_protected_area': nearest_protected_area, 'buoy_data': buoy_data, 'beacon_data': beacon_data, 'signal_data': signal_data, 'num_signals': num_signals}
    #cache these results
    create_aes_cache(aes, type, context)   
    return context
    
'''
'''
def get_airport_data(aes):
    airports = Airports.objects.all()
    inter_airports = [airport.fullname for airport in airports if airport.geometry.intersects(aes.geometry_final)]
    if len(inter_airports) == 0:
        inter_airports = ['None']
    nearest_airports = [(length_in_display_units(airport.geometry.distance(aes.geometry_final)), airport.fullname) for airport in airports if airport.fullname not in inter_airports]
    nearest_airports.sort()
    nearest_airport = (nearest_airports[0][1], nearest_airports[0][0])
    return inter_airports, nearest_airport
    
'''
'''
def get_nearest_ugbs(aes):
    return get_nearest_geometries_with_distances(aes, 'urbangrowthboundaries')
        
'''
'''
def get_protected_areas_data(aes):
    protected_areas = ProtectedAreas.objects.all()
    inter_areas = [area.site_name for area in protected_areas if area.geometry.intersects(aes.geometry_final)]
    if len(inter_areas) == 0:
        inter_areas = ['None']
    else:
        inter_areas = list(set(inter_areas))
    nearest_areas = [(length_in_display_units(area.geometry.distance(aes.geometry_final)), area.site_name) for area in protected_areas if area.site_name not in inter_areas]
    nearest_areas.sort()
    nearest_area = (nearest_areas[0][1], nearest_areas[0][0])
    return inter_areas, nearest_area
   
'''    
'''
def get_buoy_data(aes):
    intersecting_buoys = get_intersecting_shape_names(aes, 'buoys')
    nearest_buoy = get_nearest_geometries_with_distances(aes, 'buoys', length=1)
    if len(intersecting_buoys) > 0:
        buoy_data = ('Yes', intersecting_buoys)
    else:
        buoy_data = ('No', nearest_buoy[0])
    return buoy_data 
    
'''    
'''
def get_beacon_data(aes):
    intersecting_beacons = get_intersecting_shape_names(aes, 'beacons')
    nearest_beacon = get_nearest_geometries_with_distances(aes, 'beacons', length=1)
    if len(intersecting_beacons) > 0:
        beacon_data = ('Yes', intersecting_beacons)
    else:
        beacon_data = ('No', nearest_beacon[0])
    return beacon_data 
   
'''    
'''
def get_signal_data(aes):
    intersecting_signals = get_intersecting_shape_names(aes, 'signalequipment')
    #nearest_signal = get_nearest_geometries_with_distances(aes, 'signalequipment', length=1)
    if len(intersecting_signals) > 0:
        signal_data = 'Yes'
        num_signals = len(intersecting_signals)
    else:
        signal_data = 'No'
        num_signals = 0
    return signal_data, num_signals     
    