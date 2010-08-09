from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tsp.models import AOI
from models import *
from settings import *
from lingcod.unit_converter.models import area_in_display_units, length_in_display_units

'''
Runs analysis for Geographic report
Renders the Geographic Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_geo_analysis(request, nsh_id, template='Geo_Report.html'):
    #nsh = AOI.objects.get(id=nsh_id)
    nsh = get_object_or_404(AOI, pk=nsh_id)
    #get adjacent county
    county = get_adjacent_county(nsh)
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
    #get islands that reside within nsh boundaries
    islands = len(get_islands(nsh))
    #get ratio to territorial sea
    ratio = get_ratio(nsh)
    context = {'aoi': nsh, 'county': county, 'ports': ports, 'cities': cities, 'rockyshores': rockyshores, 'area': area, 'area_units': settings.DISPLAY_AREA_UNITS, 'perimeter': perimeter, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'intertidal': intertidal, 'islands': islands, 'ratio': ratio}
    return render_to_response(template, RequestContext(request, context)) 
    #return HttpResponse('adjacent county: ' + county + ' nearest ports: ' + ports)
    
'''
Determines the Adjacent County for the given nearshore habitat shape
Called by display_geo_analysis
'''
def get_adjacent_county(nsh):
    counties = Counties.objects.all()
    for county in counties:
        #the following returns the first intersection found
        #it does not account for AOIs that intersect multiple counties
        if county.geometry.intersects(nsh.geometry_final):
            return county.county_nam
    return 'this geometry does not intersect an Oregon county'
    
'''
Determines the Nearest 3 Ports for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_nearest_ports(nsh):
    ports = OregonPorts.objects.all()
    distance_to_ports = [(nsh.geometry_final.distance(port.geometry), port.name) for port in ports]
    distance_to_ports.sort()
    closest3 = [tuple[1] for tuple in distance_to_ports[:3]]
    return closest3
    
'''
Determines the Nearest 3 Cities for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_nearest_cities(nsh):
    cities = Cities.objects.all()
    distance_to_cities = [(nsh.geometry_final.distance(city.geometry.centroid), city.city_name) for city in cities]
    distance_to_cities.sort()
    closest3 = [tuple[1] for tuple in distance_to_cities[:3]]
    return closest3    
    
'''
Determines the Nearest 3 Rocky Shores for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_nearest_rockyshores(nsh):
    rockyshores = RockyShores.objects.all()
    distance_to_rockyshores = [(nsh.geometry_final.distance(rockyshore.geometry.centroid), rockyshore.name) for rockyshore in rockyshores]
    distance_to_rockyshores.sort()
    closest3 = [tuple[1] for tuple in distance_to_rockyshores[:3]]
    return closest3    

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
            return True
    islands = Islands.objects.all()
    for island in islands:
        if nsh.geometry_final.intersects(island.geometry):
            return True
    return False        
    
  
'''
Determines any overlapping Islands for the given nearshore habitat shape
Called by display_geo_analysis
'''    
def get_islands(nsh):
    islands = Islands.objects.all()
    island_tuples = [(island.geometry.intersects(nsh.geometry_final), island.name) for island in islands]
    inter_islands = [tuple[1] for tuple in island_tuples if tuple[0]==True]
    return inter_islands        
    
'''
Determines the Ratio for the given nearshore habitat shape area and the territorial sea area
Called by display_geo_analysis
'''    
def get_ratio(nsh):
    nsh_area = nsh.geometry_final.area
    from lingcod.studyregion.models import StudyRegion
    tsea_area = StudyRegion.objects.current().geometry.area
    ratio = nsh_area / tsea_area * 100
    return ratio     
  