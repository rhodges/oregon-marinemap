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
    #get nearest urban growth boundaries
    nearest_ugbs = get_nearest_ugbs(aes)
    #get intersecting protected areas and 1 nearest protected area
    intersecting_protected_areas, nearest_protected_area = get_protected_areas_data(aes)
    #visible from shore
    visible = is_visible_from_shore(aes)
    #get intersecting or nearest buoys
    intersecting_buoys, nearest_buoy = get_buoy_data(aes)
    #get intersecting or nearest beacons
    intersecting_beacons, nearest_beacon = get_beacon_data(aes)
    #get intersecting or nearest signal equipment
    signal_data, num_signals = get_signal_data(aes)
    #get all intersecting airports or nearest single airport
    intersecting_airports, nearest_airport = get_airport_data(aes)
    #get distance to nearest transmission line (1993 lines)
    transmissionline1993 = get_distance_to_nearest_transmissionline1993(aes)
    #get distance to nearest transmission line (2010 lines)
    transmissionline2010 = get_distance_to_nearest_transmissionline2010(aes)
    #get nearest 3 substations
    substations = get_nearest_substations(aes)
    #get distance to nearest railroad
    railroad = get_distance_to_nearest_railroad(aes)
    #does it intersect a towlane
    towlanes = intersects_towlane(aes)
    #get intersecting or nearest wave energy sites
    intersecting_wave_energy_sites, nearest_wave_energy_site = get_wave_energy_data(aes)
    #compile context
    context = {'aes': aes, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'intersecting_airports': intersecting_airports, 'nearest_airport': nearest_airport, 'towlanes': towlanes, 'intersecting_wave_energy_sites': intersecting_wave_energy_sites, 'nearest_wave_energy_site': nearest_wave_energy_site, 'urbangrowthboundaries': nearest_ugbs, 'intersecting_protected_areas': intersecting_protected_areas, 'nearest_protected_area': nearest_protected_area, 'visible': visible, 'intersecting_buoys': intersecting_buoys, 'nearest_buoy': nearest_buoy, 'intersecting_beacons': intersecting_beacons, 'nearest_beacon': nearest_beacon, 'signal_data': signal_data, 'num_signals': num_signals, 'substations': substations, 'transmissionline1993': transmissionline1993, 'transmissionline2010': transmissionline2010, 'railroad': railroad}
    #cache these results
    create_aes_cache(aes, type, context)   
    return context
    
'''
Determines if the given nearshore habitat shape intersects with a Tow Lane
Called by run_nsh_hum_analysis
'''
def intersects_towlane(aes):
    towlanes = Towlanes.objects.all()
    inter_lanes = [lane for lane in towlanes if lane.geometry.intersects(aes.geometry_final)]
    if len(inter_lanes) > 0:
        intersects = 'Yes'
    else:
        intersects = 'No'
    return intersects
    
'''    
Get any intersecting wave energy sites or the three nearest wave energy sites along with their distances
'''
def get_wave_energy_data(aes):
    intersecting_wave_energy_sites = get_intersecting_wave_energy_sites(aes)
    nearest_wave_energy_site = get_nearest_geometries_with_distances(aes, 'waveenergypermits', length=1)[0]
    if len(intersecting_wave_energy_sites) == 0:
        intersecting_wave_energy_sites = ['None']
    return intersecting_wave_energy_sites, nearest_wave_energy_site
    
'''
Determines the Wave Energy Sites for the given nearshore habitat shape
Called by run_nsh_hum_analysis
'''
def get_intersecting_wave_energy_sites(nsh):
    wave_sites = WaveEnergyPermits.objects.all()
    inter_sites = [site for site in wave_sites if site.geometry.intersects(nsh.geometry_final)]
    inter_tuples = [(site.name, site.geometry.intersection(nsh.geometry_final).area / nsh.geometry_final.area * 100) for site in inter_sites]
    return inter_tuples
    
'''
'''
def get_airport_data(aes):
    airports = Airports.objects.all()
    inter_airports = [airport.fullname for airport in airports if airport.geometry.intersects(aes.geometry_final)]
    if len(inter_airports) == 0:
        inter_airports = ['None']
    buffered_aes = aes.geometry_final.buffer(80000)
    nearest_airports = [(length_in_display_units(airport.geometry.distance(aes.geometry_final)), airport.fullname) for airport in airports if (airport.fullname not in inter_airports) and (airport.geometry.intersects(buffered_aes))]
    nearest_airports.sort()
    nearest_airport = (nearest_airports[0][1], nearest_airports[0][0])
    return inter_airports, nearest_airport
    
'''
'''
def get_nearest_ugbs(aes):
    #return get_nearest_geometries_with_distances(aes, 'urbangrowthboundaries')
    growth_boundaries = UrbanGrowthBoundaries.objects.all()
    buffered_aes = aes.geometry_final.buffer(60000)
    nearest_ubgs = [(length_in_display_units(boundary.geometry.distance(aes.geometry_final)), boundary.name) for boundary in growth_boundaries if boundary.geometry.intersects(buffered_aes)]
    nearest_ubgs.sort()
    nearest_ubgs = [(nearest_ubgs[0][1], nearest_ubgs[0][0]), (nearest_ubgs[1][1], nearest_ubgs[1][0]), (nearest_ubgs[2][1], nearest_ubgs[2][0])]
    return nearest_ubgs
    
'''
'''
def get_protected_areas_data(aes):
    protected_areas = ProtectedAreas.objects.all()
    inter_areas = [area.site_name for area in protected_areas if area.geometry.intersects(aes.geometry_final)]
    if len(inter_areas) == 0:
        inter_areas = ['None']
    else:
        inter_areas = list(set(inter_areas))
    buffered_aes = aes.geometry_final.buffer(60000)
    nearest_areas = [(length_in_display_units(area.geometry.distance(aes.geometry_final)), area.site_name) for area in protected_areas if (area.site_name not in inter_areas) and (area.geometry.intersects(buffered_aes))]
    nearest_areas.sort()
    nearest_area = (nearest_areas[0][1], nearest_areas[0][0])
    return inter_areas, nearest_area
   
'''
'''
def is_visible_from_shore(aes):
    viewsheds = Viewsheds.objects.all()
    intersections = [viewshed for viewshed in viewsheds if viewshed.geometry.intersects(aes.geometry_final)==True]
    if len(intersections) > 0:
        return 'Yes'
    else:
        return 'No'
        
'''    
'''
def get_buoy_data(aes):
    intersecting_buoys = get_intersecting_shape_names(aes, 'buoys')
    if len(intersecting_buoys) == 0:
        intersecting_buoys = ['None']
    buoys = Buoys.objects.all()
    nearest_buoys = [(length_in_display_units(buoy.geometry.distance(aes.geometry_final)), buoy.name) for buoy in buoys if buoy.name not in intersecting_buoys]
    nearest_buoys.sort()
    nearest_buoy = (nearest_buoys[0][1], nearest_buoys[0][0])
    return intersecting_buoys, nearest_buoy
    
'''    
'''
def get_beacon_data(aes):
    intersecting_beacons = get_intersecting_shape_names(aes, 'beacons')
    nearest_beacon = get_nearest_geometries_with_distances(aes, 'beacons', length=1)[0]
    if len(intersecting_beacons) == 0:
        intersecting_beacons = ['None']
    return intersecting_beacons, nearest_beacon
   
'''    
'''
def get_signal_data(aes):
    intersecting_signals = get_intersecting_shape_names(aes, 'signalequipment')
    #nearest_signal = get_nearest_geometries_with_distances(aes, 'signalequipment', length=1)
    if len(intersecting_signals) > 0:
        signal_data = 'Yes'
        num_signals = len(intersecting_signals)
    else:
        signal_data = 'None'
        num_signals = 0
    return signal_data, num_signals     
    
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
    buffered_aes = aes.geometry_final.buffer(80000)
    distances = [line.geometry.distance(aes.geometry_final) for line in lines if (line.geometry is not None) and (line.geometry.intersects(buffered_aes))]
    distances.sort()
    distance = length_in_display_units(distances[0])
    return distance 
    
'''
'''
def get_distance_to_nearest_transmissionline2010(aes):
    lines = TransmissionLines2010.objects.all()
    buffered_aes = aes.geometry_final.buffer(80000)
    distances = [line.geometry.distance(aes.geometry_final) for line in lines if (line.geometry is not None) and (line.geometry.intersects(buffered_aes))]
    distances.sort()
    distance = length_in_display_units(distances[0])
    return distance 
    
'''
'''
def get_distance_to_nearest_railroad(aes):
    railroads = Railroads.objects.all()
    buffered_aes = aes.geometry_final.buffer(100000)
    distances = [rail.geometry.distance(aes.geometry_final) for rail in railroads if rail.geometry.intersects(buffered_aes)]
    distances.sort()
    distance = length_in_display_units(distances[0])
    return distance 
    