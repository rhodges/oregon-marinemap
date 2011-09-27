from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, get_nearest_geometries, get_nearest_geometries_with_distances, get_intersecting_shape_names, default_value
from nsh_cache import nsh_cache_exists, get_nsh_cache, create_nsh_cache
    

'''
Runs analysis for Human Considerations report
Renders the Human Considerations Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_nsh_hum_analysis(request, nsh, type='Human', template='nsh_hum_report.html'):
    type = ensure_type(type)
    context = get_nsh_hum_context(nsh, type)
    return render_to_response(template, RequestContext(request, context)) 

'''
Called from display_aes_geo_analysis, and aes_analysis.
'''    
def get_nsh_hum_context(nsh, type): 
    #get context from cache or from running analysis
    if nsh_cache_exists(nsh, type):
        #retrieve context from cache
        context = get_nsh_cache(nsh, type)
    else:
        #get context by running analysis
        context = run_nsh_hum_analysis(nsh, type)   
        #cache these results
        create_nsh_cache(nsh, type, context)   
    return context
     
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_nsh_hum_analysis(nsh, type):     
    #get nearest state parks
    nearest_parks = get_nearest_parks(nsh)
    #get nearest public access points
    nearest_access_sites = get_nearest_access_sites(nsh)
    #get nearest 3 rocky shores
    rockyshores = get_nearest_rockyshores(nsh)
    #get intersecting or nearest dredge material disposal sites
    intersecting_dmds, nearest_dmd = get_dmd_data(nsh)
    #get intersecting or nearest npde outfall sites
    intersecting_outfalls, nearest_outfall = get_outfall_data(nsh)
    #get intersecting or nearest undersea cable routes
    intersecting_cables, nearest_cable = get_cable_data(nsh)
    #get nearest ports
    nearest_ports = get_nearest_ports(nsh)
    #get nearest 3 marinas
    nearest_marinas = get_nearest_marinas(nsh)
    #get intersecting and nearest marine managed areas
    intersecting_mmas, nearest_mmas = get_mma_data(nsh)
    #get intersecting and nearest fishery closures
    intersecting_closures, nearest_closure = get_fishery_closures_data(nsh)
    #get intersecting and nearest conservation areas
    intersecting_conservation_areas, nearest_conservation_area = get_conservation_areas_data(nsh)
    #compile context
    context = {'nsh': nsh, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'parks': nearest_parks, 'access_sites': nearest_access_sites, 'rockyshores': rockyshores, 'intersecting_dmds': intersecting_dmds, 'nearest_dmd': nearest_dmd, 'intersecting_outfalls': intersecting_outfalls, 'nearest_outfall': nearest_outfall, 'intersecting_cables': intersecting_cables, 'nearest_cable': nearest_cable, 'nearest_ports': nearest_ports, 'nearest_marinas': nearest_marinas, 'intersecting_mmas': intersecting_mmas, 'nearest_mmas': nearest_mmas, 'intersecting_closures': intersecting_closures, 'nearest_closure': nearest_closure, 'intersecting_conservation_areas': intersecting_conservation_areas, 'nearest_conservation_area': nearest_conservation_area}
    #cache these results
    create_nsh_cache(nsh, type, context)   
    return context
    
'''
Determines the Nearest State Park for the given nearshore habitat shape
Called by run_nsh_hum_analysis
'''
def get_nearest_parks(nsh):
    return get_nearest_geometries_with_distances(nsh, 'stateparks')
    
'''
Determines the Nearest Public Access Sites for the given nearshore habitat shape
Called by run_nsh_hum_analysis
'''
def get_nearest_access_sites(nsh):
    nearest_sites = get_nearest_geometries(nsh, 'publicaccess')
    site_tuples = []
    for site in nearest_sites:
        output = site.name + ' , ' + site.city + ' ' + site.county + ' County'
        site_tuples.append( (output, length_in_display_units(site.geometry.distance(nsh.geometry_final))) )
    return site_tuples
    
'''
Determines the Nearest 3 Rocky Shores (in order of proximity) for the given nearshore habitat shape
Called by display_nsh_geo_analysis
'''    
def get_nearest_rockyshores(nsh):
    return get_nearest_geometries_with_distances(nsh, 'rockyshores')
    
'''    
Get any intersecting dmds or the three nearest dmds along with their distances
'''
def get_dmd_data(nsh):
    intersecting_dmds = get_intersecting_shape_names(nsh, 'dmdsites')
    if len(intersecting_dmds) == 0:
        intersecting_dmds = ['None']
    else:
        intersecting_dmds = list(set(intersecting_dmds))
    dmdsites = DMDSites.objects.all()
    nearest_dmds = [(length_in_display_units(dmd.geometry.distance(nsh.geometry_final)), dmd.name) for dmd in dmdsites if dmd.name not in intersecting_dmds]
    nearest_dmds.sort()
    nearest_dmd = (nearest_dmds[0][1], nearest_dmds[0][0])
    return intersecting_dmds, nearest_dmd
   
'''    
Get any intersecting outfalls or the three nearest outfalls along with their distances
'''
def get_outfall_data(nsh):
    intersecting_outfalls = get_intersecting_shape_names(nsh, 'outfalls')
    if len(intersecting_outfalls) == 0:
        intersecting_outfalls = ['None']
    outfalls = Outfalls.objects.all()
    nearest_outfalls = [(length_in_display_units(outfall.geometry.distance(nsh.geometry_final)), outfall.name) for outfall in outfalls if outfall.name not in intersecting_outfalls]
    nearest_outfalls.sort()
    nearest_outfall = (nearest_outfalls[0][1], nearest_outfalls[0][0])
    return intersecting_outfalls, nearest_outfall

'''    
Get any intersecting cables or the three nearest cables along with their distances
'''
def get_cable_data(nsh):
    intersecting_cables = get_intersecting_shape_names(nsh, 'underseacables')
    if len(intersecting_cables) == 0:
        intersecting_cables = ['None']
    cables = UnderseaCables.objects.all()
    nearest_cables = [(length_in_display_units(cable.geometry.distance(nsh.geometry_final)), cable.name) for cable in cables if cable.name not in intersecting_cables]
    nearest_cables.sort()
    nearest_cable = (nearest_cables[0][1], nearest_cables[0][0])
    return intersecting_cables, nearest_cable   
    
'''
Determines the Nearest Ports for the given nearshore habitat shape
Called by run_nsh_hum_analysis
'''
def get_nearest_ports(nsh):
    return get_nearest_geometries_with_distances(nsh, 'ports')
    
'''
Determines the Nearest 3 Ports (in order of proximity) for the given energy site shape
Called by display_aes_geo_analysis
'''    
def get_nearest_marinas(nsh):
    return get_nearest_geometries_with_distances(nsh, 'marinas')
    
'''
Determines any Intersecting Marine Managed Areas as well as 2 nearest (non-intersecting) MMAs
Called by run_nsh_hum_analysis
'''
def get_mma_data(nsh):
    managed_areas = MarineManagedAreas.objects.all()
    inter_areas = [area.name for area in managed_areas if area.geometry.intersects(nsh.geometry_final)]
    if len(inter_areas) == 0:
        inter_areas = ['None']
    else:
        inter_areas = list(set(inter_areas))
    nearest_areas = [(length_in_display_units(area.geometry.distance(nsh.geometry_final)), area.name) for area in managed_areas if area.name not in inter_areas]
    nearest_areas.sort()
    nearest_areas = [(nearest_areas[0][1], nearest_areas[0][0]), (nearest_areas[1][1], nearest_areas[1][0])]
    return inter_areas, nearest_areas
    
'''
Determines any Intersecting Fishery Closures as well as nearest (non-intersecting) Closure
Called by run_nsh_hum_analysis
'''
def get_fishery_closures_data(nsh):
    fishery_closures = FisheryClosures.objects.all()
    inter_closures = [closure.name for closure in fishery_closures if closure.geometry.intersects(nsh.geometry_final)]
    if len(inter_closures) == 0:
        inter_closures = ['None']
    else:
        inter_closures = list(set(inter_closures))
    nearest_closures = [(length_in_display_units(closure.geometry.distance(nsh.geometry_final)), closure.name) for closure in fishery_closures if closure.name not in inter_closures]
    nearest_closures.sort()
    nearest_closure = (nearest_closures[0][1], nearest_closures[0][0])
    return inter_closures, nearest_closure
    
'''
Determines any Intersecting Conservation Areas as well as nearest (non-intersecting) Conservation Area
Called by run_nsh_hum_analysis
'''
def get_conservation_areas_data(nsh):
    conservation_areas = ConservationAreas.objects.all()
    inter_areas = [area.name for area in conservation_areas if area.geometry.intersects(nsh.geometry_final)]
    if len(inter_areas) == 0:
        inter_areas = ['None']
    else:
        inter_areas = list(set(inter_areas))
    nearest_areas = [(length_in_display_units(area.geometry.distance(nsh.geometry_final)), area.name) for area in conservation_areas if area.name not in inter_areas]
    nearest_areas.sort()
    nearest_area = (nearest_areas[0][1], nearest_areas[0][0])
    return inter_areas, nearest_area
    