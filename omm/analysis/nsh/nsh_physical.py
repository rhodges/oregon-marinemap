from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, default_value
from nsh_cache import has_cache, get_cache, create_cache


'''
Runs analysis for Physical report
Renders the Physical Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_phy_analysis(request, nsh, type='Physical', template='nsh_phy_report.html'):
    type = ensure_type(type)
    #get context from cache or from running analysis
    if has_cache(nsh, type):
        #retrieve context from cache
        context = get_cache(nsh, type)
    else:
        #get context by running analysis
        context = run_phy_analysis(nsh, type) 
    
    return render_to_response(template, RequestContext(request, context)) 
     
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_phy_analysis(nsh, type):     
     #Intertidal Shoreline Length
    length = get_shoreline_length(nsh) 
    if length is None:
        length = 0.0
        percent_shoreline = default_value
        islands = 0
        island_area = default_value
        shoreline_proportions = [(default_value, default_value)]
    else:
        #percent of Oregon Coast Shoreline
        percent_shoreline = get_shoreline_percentage(length) 
        #number of islands
        islands = get_num_islands(nsh) 
        #total island area
        island_area = get_island_area(nsh) 
        #shoreline types and proportions
        shoreline_proportions = get_shoreline_proportions(nsh) 
    #subtidal area
    subtidal_area = get_subtidal_area(nsh, island_area) 
    #percent percent shallow, percent deep, and average depth
    perc_shallow, perc_deep, average_depth = get_depth_stats(nsh)
    #seafloor lithology
    lithology_proportions = get_lithology_proportions(nsh)
    #proximity to shore
    distance_to_shore = get_distance_to_shore(nsh) 
    #compile context
    context = {'nsh': nsh, 'default_value': default_value, 'length': length, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'percent_shoreline': percent_shoreline, 'islands': islands, 'island_area': island_area, 'shoreline_proportions': shoreline_proportions, 'subtidal_area': subtidal_area, 'perc_shallow': perc_shallow, 'perc_deep': perc_deep, 'average_depth': average_depth, 'distance_to_shore': distance_to_shore, 'lithology_proportions': lithology_proportions}
    #cache these results
    create_cache(nsh, type, context)   
    return context
    
def get_depth_stats(nsh):
    bath_polys = Bathymetry.objects.all()
    inter_polys = [poly for poly in bath_polys if poly.geometry.intersects(nsh.geometry_final)]
    bath_dict = {}
    total_area = 0.0
    #generate depth dictionary {depth: total_area_at_that_depth}, and total area
    #currently assuming there are enough polygons in each nsh that we don't need to take the area of intersection from each polygon
    for poly in inter_polys:
        area = poly.geometry.area
        if poly.depth not in bath_dict.keys():
            bath_dict[poly.depth] = area
        else:
            bath_dict[poly.depth] += area
        total_area += area
    shallow_area = 0.0
    deep_area = 0.0
    numerator = 0.0
    denominator = 0.0
    #determine the total area of shallow waters (<=25m), total area of deep waters (>25m)
    #determine the average depth (depth * area / area)
    for depth, area in bath_dict.items():
        if -depth <= 25:
            shallow_area += area
        else:
            deep_area += area
        numerator += depth * area
        denominator += area
    perc_shallow = shallow_area / total_area * 100
    perc_deep = deep_area / total_area * 100
    average_depth = numerator / denominator
    return perc_shallow, perc_deep, average_depth
    
    
    
'''
Determines the Intertidal Shoreline Length for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_shoreline_length(nsh):
    shorelines = ClosedShoreline.objects.all()
    islands = Islands.objects.all()
    mainland_shorelines = [shoreline for shoreline in shorelines if shoreline.geometry.intersects(nsh.geometry_final)]
    island_shorelines = [island for island in islands if island.geometry.intersects(nsh.geometry_final)]
    if len(mainland_shorelines) == len(island_shorelines) == 0:
        return None
    mainland_shoreline_lengths = [shoreline.geometry.intersection(nsh.geometry_final).length for shoreline in mainland_shorelines]
    island_shoreline_lengths = [shoreline.geometry.intersection(nsh.geometry_final).length for shoreline in island_shorelines]
    total_length = sum(mainland_shoreline_lengths) + sum(island_shoreline_lengths)
    total_length_converted_units = length_in_display_units(total_length)
    return total_length_converted_units
     
'''
Determines the Shoreline Percentage for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_shoreline_percentage(length):  
    shorelines = ClosedShoreline.objects.all()
    islands = Islands.objects.all()
    shorelines_length = sum([shoreline.geometry.length for shoreline in shorelines])
    islands_length = sum([island.geometry.length for island in islands])
    total_length = shorelines_length + islands_length
    total_length_converted_units = length_in_display_units(total_length)
    percentage = length / total_length_converted_units * 100
    return percentage 
      
'''
Determines the proportions for the various types of shoreline
Called by display_phy_analysis
'''    
def get_shoreline_proportions(nsh):
    shorelines = Shoreline.objects.all()
    inter_shorelines = [shoreline for shoreline in shorelines if shoreline.geometry.intersects(nsh.geometry_final)]
    esi_length_tuples = [(esi_to_text(shoreline.esi[0]), length_in_display_units(shoreline.geometry.intersection(nsh.geometry_final).length)) for shoreline in inter_shorelines]
    esi_length_dict = {}
    total_length = 0.0
    for tuple in esi_length_tuples:
        if tuple[0] not in esi_length_dict.keys():
            esi_length_dict[tuple[0]] = tuple[1]
        else:
            esi_length_dict[tuple[0]] += tuple[1]
        total_length += tuple[1]
    esi_proportion_list = []
    for key in esi_length_dict.keys():
        esi_shoretype = key
        length = esi_length_dict[key]
        proportion = length / total_length * 100
        esi_proportion_list.append((proportion, esi_shoretype, length))
    esi_proportion_list.sort()
    esi_proportion_list.reverse()
    return esi_proportion_list    
    
'''    
Called from get_shoreline_proportions
'''
def esi_to_text(esi):
    esi_dict = {    '1': 'Exposed Rocky Shores', 
                    '2': 'Exposed Rocky Platforms', 
                    '3': 'Fine-grained Sandy Beaches', 
                    '4': 'Coarse-grained Sandy Beaches', 
                    '5': 'Mixed Sand and Gravel Beaches', 
                    '6': 'Gravel Beaches / Exposed Riprap', 
                    '7': 'Exposed Tidal Flats', 
                    '8': 'Sheltered Rocky / Artificial Shores', 
                    '9': 'Sheltered Tidal Flats', 
                    '10': 'Marsh', 
                    'U': 'Undefined'    }
    return esi_dict[esi]
    
'''
Determines the number of overlapping Islands for the given nearshore habitat shape
Called by display_phy_analysis
'''    
def get_num_islands(nsh):
    islands = Islands.objects.all()
    inter_islands = [island for island in islands if island.geometry.intersects(nsh.geometry_final)==True]
    return len(inter_islands)
    
'''
Determines the area of overlapping Islands for the given nearshore habitat shape
Called by display_phy_analysis
'''    
def get_island_area(nsh):
    islands = Islands.objects.all()
    inter_islands = [island for island in islands if island.geometry.intersects(nsh.geometry_final)==True]
    area_of_intersect = 0.0
    for island in inter_islands:
        area_of_intersect += island.geometry.intersection(nsh.geometry_final).area
    area_of_intersect_converted_units = area_in_display_units(area_of_intersect)
    return area_of_intersect_converted_units
   
'''
Determines the subtidal area for the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_subtidal_area(nsh, island_area):
    total_area = area_in_display_units(nsh.geometry_final.area)
    if island_area != default_value:
        return total_area - island_area
    return total_area
    
'''
Determines the distance to shore for the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_distance_to_shore(nsh):
    if nsh_touches_shoreline(nsh):
        return 0.0
    shorelines = ClosedShoreline.objects.all()
    from django.contrib.gis.geos import Polygon
    bbox = Polygon.from_bbox(nsh.geometry_final.extent)
    buffered_bbox = bbox.buffer(8000) #buffer by 5 miles (8000 meters)
    inter_shorelines = [shoreline for shoreline in shorelines if shoreline.geometry.intersects(buffered_bbox)]
    distances = [shoreline.geometry.distance(nsh.geometry_final) for shoreline in inter_shorelines]
    distances.sort()
    return length_in_display_units(distances[0])
    
'''
Called from get_distance_to_shore
'''    
def nsh_touches_shoreline(nsh):
    shorelines = ClosedShoreline.objects.all()
    intersections = [shoreline.geometry.intersects(nsh.geometry_final) for shoreline in shorelines]
    if True in intersections:
        return True
    else:
        return False
    
'''
Determines the areas and ratios for each represented lithology within the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_lithology_proportions(nsh):
    lithologies = Lithology.objects.all()
    inter_lithologies = [lithology for lithology in lithologies if lithology.geometry.intersects(nsh.geometry_final)]
    inter_lithology_tuples = [(lithology.lithology, lithology.geometry.intersection(nsh.geometry_final).area) for lithology in inter_lithologies]
    total_area = 0.0
    lithology_dict = {}
    for tuple in inter_lithology_tuples:
        if tuple[0] not in lithology_dict.keys():
            lithology_dict[tuple[0]] = tuple[1]
        else:
            lithology_dict[tuple[0]] += tuple[1]
        total_area += tuple[1]
    lithology_proportion_list = []
    for key in lithology_dict.keys():
        area = lithology_dict[key]
        proportion = area / total_area * 100
        lithology_proportion_list.append((proportion, key, area_in_display_units(area)))
    lithology_proportion_list.sort()
    lithology_proportion_list.reverse()
    return lithology_proportion_list    

    