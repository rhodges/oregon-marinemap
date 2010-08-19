from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tsp.models import AOI
from models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from utils import get_nearest_geometries_with_distances, get_intersecting_geometries
from NSH_Cache import has_cache, get_cache, create_cache
    
default_value = '---'

'''
Runs analysis for Human Considerations report
Renders the Human Considerations Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_hum_analysis(request, nsh_id, type='Human', template='Hum_Report.html'):
    nsh = get_object_or_404(AOI, pk=nsh_id)
    
    #get context from cache or from running analysis
    if has_cache(nsh, type):
        #retrieve context from cache
        context = get_cache(nsh, type)
    else:
        #get context by running analysis
        context = run_hum_analysis(nsh)
        #cache these results
        create_cache(nsh, type, context)      
    
    return render_to_response(template, RequestContext(request, context)) 
     
'''
Run the analysis and return the results as a context dictionary so they may be rendered with template
'''    
def run_hum_analysis(nsh):     
    #get nearest state parks
    nearest_parks = get_nearest_parks(nsh)
    #get nearest public access points
    nearest_access_sites = get_nearest_access_sites(nsh)
    #get intersecting or nearest dredge material disposal sites
    intersecting_dmds, nearest_dmds = get_intersecting_or_nearest_dmds(nsh)
    #get intersecting or nearest npde outfall sites
    intersecting_outfalls, nearest_outfalls = get_intersecting_or_nearest_outfalls(nsh)
    #get intersecting or nearest undersea cable routes
    intersecting_cables, nearest_cables = get_intersecting_or_nearest_cables(nsh)
    #does it intersect a towlane
    towlanes = intersects_towlane(nsh)
    #get intersecting or nearest wave energy sites
    intersecting_wave_sites, nearest_wave_sites = get_intersecting_or_nearest_wave_energy_sites(nsh)
    #get nearest ports
    nearest_ports = get_nearest_ports(nsh)
    #get nearest marine managed areas
    nearest_mmas = get_nearest_mmas(nsh)
    #get nearest fishery closures
    nearest_closures = get_nearest_fishery_closures(nsh)
    #get nearest conservation areas
    nearest_conservation_areas = get_nearest_conservation_areas(nsh)
    
    return {'aoi': nsh, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'parks': nearest_parks, 'access_sites': nearest_access_sites, 'dmd_sites': intersecting_dmds, 'nearest_dmds': nearest_dmds, 'outfall_sites': intersecting_outfalls, 'nearest_outfalls': nearest_outfalls, 'cables': intersecting_cables, 'nearest_cables': nearest_cables, 'towlanes': towlanes, 'wave_sites': intersecting_wave_sites, 'nearest_wave_sites': nearest_wave_sites, 'nearest_ports': nearest_ports, 'nearest_mmas': nearest_mmas, 'nearest_closures': nearest_closures, 'nearest_conservation_areas': nearest_conservation_areas}

'''
Determines the Nearest State Park for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_parks(nsh):
    return get_nearest_geometries_with_distances(nsh, 'stateparks')
    
'''
Determines the Nearest Public Access Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_access_sites(nsh):
    return get_nearest_geometries_with_distances(nsh, 'publicaccess')
    
'''    
Get any intersecting dmds or the three nearest dmds along with their distances
'''
def get_intersecting_or_nearest_dmds(nsh):
    intersecting_dmds = get_intersecting_geometries(nsh, 'dmdsites')
    nearest_dmds = []
    if intersecting_dmds[0] == default_value:
        nearest_dmds = get_nearest_geometries_with_distances(nsh, 'dmdsites')
    return intersecting_dmds, nearest_dmds
   
'''    
Get any intersecting outfalls or the three nearest outfalls along with their distances
'''
def get_intersecting_or_nearest_outfalls(nsh):
    intersecting_outfalls = get_intersecting_geometries(nsh, 'outfalls')
    nearest_outfalls = []
    if intersecting_outfalls[0] == default_value:
        nearest_outfalls = get_nearest_geometries_with_distances(nsh, 'outfalls')
    return intersecting_outfalls, nearest_outfalls

'''    
Get any intersecting cables or the three nearest cables along with their distances
'''
def get_intersecting_or_nearest_cables(nsh):
    intersecting_cables = get_intersecting_geometries(nsh, 'underseacables')
    nearest_cables = []
    if intersecting_cables[0] == default_value:
        nearest_cables = get_nearest_geometries_with_distances(nsh, 'underseacables')
    return intersecting_cables, nearest_cables
    
'''
Determines if the given nearshore habitat shape intersects with a Tow Lane
Called by display_phy_analysis
'''
def intersects_towlane(nsh):
    towlanes = Towlanes.objects.all()
    inter_lanes = [lane for lane in towlanes if lane.geometry.intersects(nsh.geometry_final)]
    if len(inter_lanes) == 0:
        intersects = 'No'
    else:
        intersects = 'Yes'
    return intersects
    
'''    
Get any intersecting wave energy sites or the three nearest wave energy sites along with their distances
'''
def get_intersecting_or_nearest_wave_energy_sites(nsh):
    intersecting_wave_energy_sites = get_intersecting_wave_energy_sites(nsh)
    nearest_wave_energy_sites = []
    if intersecting_wave_energy_sites[0] == (default_value, default_value):
        nearest_wave_energy_sites = get_nearest_geometries_with_distances(nsh, 'waveenergypermits')
    return intersecting_wave_energy_sites, nearest_wave_energy_sites
    
'''
Determines the Wave Energy Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_intersecting_wave_energy_sites(nsh):
    wave_sites = WaveEnergyPermits.objects.all()
    inter_sites = [site for site in wave_sites if site.geometry.intersects(nsh.geometry_final)]
    if len(inter_sites) == 0:
        inter_sites.append((default_value, default_value))
    else:
        inter_sites = [(site.name, site.geometry.intersection(nsh.geometry_final).area / nsh.geometry_final.area * 100) for site in inter_sites]
    return inter_sites
    
'''
Determines the Nearest Ports for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_ports(nsh):
    return get_nearest_geometries_with_distances(nsh, 'ports')
    
'''
Determines the Nearest Marine Managed Areas for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_mmas(nsh):
    return get_nearest_geometries_with_distances(nsh, 'marinemanagedareas')
    
'''
Determines the Fishery Closures for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_fishery_closures(nsh):
    return get_nearest_geometries_with_distances(nsh, 'fisheryclosures')
    
'''
Determines the Nearest Conservation Areas for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_conservation_areas(nsh):
    return get_nearest_geometries_with_distances(nsh, 'conservationareas')
    