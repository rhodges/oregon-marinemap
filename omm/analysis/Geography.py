from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tsp.models import AOI
from models import *
from settings import *
from lingcod.unit_converter.models import area_in_display_units, length_in_display_units
from utils import get_nearest_geometries, get_intersecting_geometries

'''
Runs analysis for Geographic report
Renders the Geographic Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_geo_analysis(request, nsh_id, template='Geo_Report.html'):
    nsh = get_object_or_404(AOI, pk=nsh_id)
    #get adjacent county
    counties = get_adjacent_counties(nsh)
    #get nearest 3 ports
    ports = get_nearest_ports(nsh)
    #get nearest 3 cities
    cities = get_nearest_cities(nsh)
    #get nearest 3 rocky shores
    rockyshores = get_nearest_rockyshores(nsh)
    #get the area
    area = get_area(nsh)
    #get the perimeter
    perimeter = get_perimeter(nsh)
    #determine whether nsh touches the Oregon Shoreline (including any island shorelines)
    intertidal = is_intertidal(nsh)
    #get number of islands that reside within nsh boundaries
    islands = get_num_islands(nsh)
    #get ratio to territorial sea
    ratio = get_ratio(nsh)
    
    context = {'aoi': nsh, 'county': counties, 'ports': ports, 'cities': cities, 'rockyshores': rockyshores, 'area': area, 'area_units': settings.DISPLAY_AREA_UNITS, 'perimeter': perimeter, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'intertidal': intertidal, 'islands': islands, 'ratio': ratio}
    return render_to_response(template, RequestContext(request, context)) 
    
'''
Determines the Adjacent Counties for the given nearshore habitat shape
Called by display_geo_analysis
'''
def get_adjacent_counties(nsh):
    return get_intersecting_geometries(nsh, 'counties')
    
'''
Determines the Nearest 3 Ports (in order of proximity) for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_nearest_ports(nsh):
    return get_nearest_geometries(nsh, 'ports')
    
'''
Determines the Nearest 3 Cities (in order of proximity) for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_nearest_cities(nsh):
    return get_nearest_geometries(nsh, 'cities')
    
'''
Determines the Nearest 3 Rocky Shores (in order of proximity) for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_nearest_rockyshores(nsh):
    return get_nearest_geometries(nsh, 'rockyshores')
    
'''
Determines the Area for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_area(nsh):
    area = area_in_display_units(nsh.geometry_final)
    return area        
    
'''
Determines the Perimeter for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_perimeter(nsh):
    perimeter = length_in_display_units(nsh.geometry_final)
    return perimeter     
  
'''
Determine whether nsh touches the Oregon Shoreline (including any island shorelines)
Called by display_geo_analysis
'''    
def is_intertidal(nsh):
    shorelines = Shoreline.objects.all()
    for shoreline in shorelines:
        if nsh.geometry_final.intersects(shoreline.geometry):
            return 'Yes'
    islands = Islands.objects.all()
    for island in islands:
        if nsh.geometry_final.intersects(island.geometry):
            return 'Yes'
    return 'No'        
    
'''
Determines the number of overlapping Islands for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_num_islands(nsh):
    islands = Islands.objects.all()
    inter_islands = [island for island in islands if island.geometry.intersects(nsh.geometry_final)==True]
    return len(inter_islands)
    
'''
Determines the Ratio for the given nearshore habitat area and the territorial sea area
Called by display_geo_analysis
'''    
def get_ratio(nsh):
    nsh_area = nsh.geometry_final.area
    from lingcod.studyregion.models import StudyRegion
    tsea_area = StudyRegion.objects.current().geometry.area
    ratio = nsh_area / tsea_area * 100
    return ratio     
  