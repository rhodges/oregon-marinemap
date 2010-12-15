from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import area_in_display_units, length_in_display_units
from analysis.utils import ensure_type, get_nearest_geometries_with_distances, get_intersecting_shape_names, default_value
from aes_cache import has_cache, get_cache, create_cache


'''
Runs analysis for Geographic report
Renders the Geographic Report template
Called by AES_Analysis.display_aes_analysis
'''
def display_geo_analysis(request, aes, type='Geography', template='aes_geo_report.html'):
    type = ensure_type(type)
    #get context from cache or from running analysis
    if has_cache(aes, type):
        #retrieve context from cache
        context = get_cache(aes, type)
    else:
        #get context by running analysis
        context = run_geo_analysis(aes, type)   
    return render_to_response(template, RequestContext(request, context)) 
    
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_geo_analysis(aes, type):
    #get adjacent county
    counties = get_adjacent_counties(aes)
    #get distance to nearest railroad
    railroad = get_distance_to_nearest_railroad(aes)
    #get nearest 3 ports
    ports = get_nearest_ports(aes)
    #get nearest 3 marinas
    marinas = get_nearest_marinas(aes)
    #get nearest 3 cities
    cities = get_nearest_cities(aes)
    #get nearest 3 rocky shores
    rockyshores = get_nearest_rockyshores(aes)
    #get nearest 3 substations
    substations = get_nearest_substations(aes)
    #get distance to nearest transmission line (1993 lines)
    transmissionline1993 = get_distance_to_nearest_transmissionline1993(aes)
    #get distance to nearest transmission line (2010 lines)
    transmissionline2010 = get_distance_to_nearest_transmissionline2010(aes)
    #get the area
    area = get_area(aes)
    #get the perimeter
    perimeter = get_perimeter(aes)
    #determine whether aes touches the Oregon Shoreline (including any island shorelines)
    intertidal = is_intertidal(aes)
    #get number of islands that reside within aes boundaries
    islands = has_islands(aes)
    #visible from shore
    visible = is_visible_from_shore(aes)
    #get ratio to territorial sea
    ratio = get_ratio(aes)
    #compile context
    context = {'aes': aes, 'county': counties, 'railroad': railroad, 'ports': ports, 'marinas': marinas, 'cities': cities, 'rockyshores': rockyshores, 'substations': substations, 'transmissionline1993': transmissionline1993, 'transmissionline2010': transmissionline2010, 'area': area, 'area_units': settings.DISPLAY_AREA_UNITS, 'perimeter': perimeter, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'intertidal': intertidal, 'islands': islands, 'visible': visible, 'ratio': ratio}
    #cache these results
    create_cache(aes, type, context)   
    return context
       
'''
Determines the Adjacent Counties for the given energy site shape
Called by display_geo_analysis
'''
def get_adjacent_counties(aes):
    intersecting_geometries = get_intersecting_shape_names(aes, 'counties')
    if len(intersecting_geometries) == 0:
        intersecting_geometries.append(default_value)
    return intersecting_geometries
   
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
Called by display_geo_analysis
'''    
def get_nearest_ports(aes):
    return get_nearest_geometries_with_distances(aes, 'ports')
    
'''
Determines the Nearest 3 Ports (in order of proximity) for the given energy site shape
Called by display_geo_analysis
'''    
def get_nearest_marinas(aes):
    return get_nearest_geometries_with_distances(aes, 'marinas')
    
'''
Determines the Nearest 3 Cities (in order of proximity) for the given energy site shape
Called by display_geo_analysis
'''    
def get_nearest_cities(aes):
    return get_nearest_geometries_with_distances(aes, 'cities')
    
'''
Determines the Nearest 3 Rocky Shores (in order of proximity) for the given energy site shape
Called by display_geo_analysis
'''    
def get_nearest_rockyshores(aes):
    return get_nearest_geometries_with_distances(aes, 'rockyshores')
    
'''
Determines the Nearest 3 Electrical Substations (in order of proximity) for the given energy site shape
Called by display_geo_analysis
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
Determines the Area for the given energy site shape
Called by display_geo_analysis
'''    
def get_area(aes):
    area = area_in_display_units(aes.geometry_final)
    return area        
    
'''
Determines the Perimeter for the given energy site shape
Called by display_geo_analysis
'''    
def get_perimeter(aes):
    perimeter = length_in_display_units(aes.geometry_final)
    return perimeter     
  
'''
Determine whether aes touches the Oregon Shoreline (including any island shorelines)
Called by display_geo_analysis
'''    
def is_intertidal(aes):
    shorelines = Shoreline.objects.all()
    for shoreline in shorelines:
        if aes.geometry_final.intersects(shoreline.geometry):
            return 'Yes'
    islands = Islands.objects.all()
    for island in islands:
        if aes.geometry_final.intersects(island.geometry):
            return 'Yes'
    return 'No'        
    
'''
Determines the number of overlapping Islands for the given energy site shape
Called by display_geo_analysis
'''    
def has_islands(aes):
    islands = Islands.objects.all()
    inter_islands = [island for island in islands if island.geometry.intersects(aes.geometry_final)==True]
    if len(inter_islands) > 0:
        return 'Yes'
    else:
        return 'No'
    
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
Determines the Ratio for the given energy site area and the territorial sea area
Called by display_geo_analysis
'''    
def get_ratio(aes):
    from lingcod.studyregion.models import StudyRegion
    sr_geom = StudyRegion.objects.current().geometry
    tsea_area = sr_geom.area
    aes_area = aes.geometry_final.intersection(sr_geom).area
    ratio = aes_area / tsea_area * 100
    return ratio     
  