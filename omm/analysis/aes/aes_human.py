from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, get_nearest_geometries, get_nearest_geometries_with_distances, get_intersecting_geometries
from aes_cache import has_cache, get_cache, create_cache
    
default_value = '---'

'''
Runs analysis for Human Considerations report
Renders the Human Considerations Report template
Called by aes_Analysis.display_aes_analysis
'''
def display_hum_analysis(request, aes, type='Human', template='aes_hum_report.html'):
    type = ensure_type(type)
    #get context from cache or from running analysis
    if has_cache(aes, type):
        #retrieve context from cache
        context = get_cache(aes, type)
    else:
        #get context by running analysis
        context = run_hum_analysis(aes, type)   
    
    return render_to_response(template, RequestContext(request, context)) 
     
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_hum_analysis(aes, type):     
    #get nearest state parks
    nearest_parks = get_nearest_parks(aes)
    #get nearest public access points
    nearest_access_sites = get_nearest_access_sites(aes)
    #get intersecting or nearest dredge material disposal sites
    dmd_data = get_dmd_data(aes)
    #get intersecting or nearest npde outfall sites
    outfall_data = get_outfall_data(aes)
    #get intersecting or nearest undersea cable routes
    cable_data = get_cable_data(aes)
    #does it intersect a towlane
    towlanes = intersects_towlane(aes)
    #get intersecting or nearest wave energy sites
    wave_energy_data = get_wave_energy_data(aes)
    #get nearest ports
    nearest_ports = get_nearest_ports(aes)
    #get nearest marine managed areas
    nearest_mmas = get_nearest_mmas(aes)
    #get nearest fishery closures
    nearest_closures = get_nearest_fishery_closures(aes)
    #get nearest conservation areas
    nearest_conservation_areas = get_nearest_conservation_areas(aes)
    #compile context
    context = {'aes': aes, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'parks': nearest_parks, 'access_sites': nearest_access_sites, 'dmd_data': dmd_data, 'outfall_data': outfall_data, 'cable_data': cable_data, 'towlanes': towlanes, 'wave_energy_data': wave_energy_data, 'nearest_ports': nearest_ports, 'nearest_mmas': nearest_mmas, 'nearest_closures': nearest_closures, 'nearest_conservation_areas': nearest_conservation_areas}
    #cache these results
    create_cache(aes, type, context)   
    return context
    
'''
Determines the Nearest State Park for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_parks(aes):
    return get_nearest_geometries_with_distances(aes, 'stateparks')
    
'''
Determines the Nearest Public Access Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_access_sites(aes):
    nearest_sites = get_nearest_geometries(aes, 'publicaccess')
    site_tuples = []
    for site in nearest_sites:
        output = site.name + ' , ' + site.city + ' ' + site.county + ' County'
        site_tuples.append( (output, length_in_display_units(site.geometry.distance(aes.geometry_final))) )
    return site_tuples
    
'''    
Get any intersecting dmds or the three nearest dmds along with their distances
'''
def get_dmd_data(aes):
    intersecting_dmds = get_intersecting_geometries(aes, 'dmdsites')
    nearest_dmd = get_nearest_geometries_with_distances(aes, 'dmdsites', length=1)
    if len(intersecting_dmds) > 0:
        dmd_data = ('Yes', intersecting_dmds)
    else:
        dmd_data = ('No', nearest_dmd[0])
    return dmd_data
   
'''    
Get any intersecting outfalls or the three nearest outfalls along with their distances
'''
def get_outfall_data(aes):
    intersecting_outfalls = get_intersecting_geometries(aes, 'outfalls')
    nearest_outfall = get_nearest_geometries_with_distances(aes, 'outfalls', length=1)
    if len(intersecting_outfalls) > 0:
        outfall_data = ('Yes', intersecting_outfalls)
    else:
        outfall_data = ('No', nearest_outfall[0])
    return outfall_data

'''    
Get any intersecting cables or the three nearest cables along with their distances
'''
def get_cable_data(aes):
    intersecting_cables = get_intersecting_geometries(aes, 'underseacables')
    nearest_cable = get_nearest_geometries_with_distances(aes, 'underseacables', line=True, length=1)
    if len(intersecting_cables) > 0:
        cable_data = ('Yes', intersecting_cables)
    else:
        cable_data = ('No', nearest_cable[0])
    return cable_data
    
'''
Determines if the given nearshore habitat shape intersects with a Tow Lane
Called by display_phy_analysis
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
    nearest_wave_energy_site = get_nearest_geometries_with_distances(aes, 'waveenergypermits', length=1)
    if len(intersecting_wave_energy_sites) > 0:
        wave_data = ('Yes', intersecting_wave_energy_sites)
    else:
        wave_data = ('No', nearest_wave_energy_site)
    return wave_data
    
'''
Determines the Wave Energy Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_intersecting_wave_energy_sites(aes):
    wave_sites = WaveEnergyPermits.objects.all()
    inter_sites = [site for site in wave_sites if site.geometry.intersects(aes.geometry_final)]
    inter_tuples = [(site.name, site.geometry.intersection(aes.geometry_final).area / aes.geometry_final.area * 100) for site in inter_sites]
    return inter_tuples
    
'''
Determines the Nearest Ports for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_ports(aes):
    return get_nearest_geometries_with_distances(aes, 'ports')
    
'''
Determines the Nearest Marine Managed Areas for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_mmas(aes):
    return get_nearest_geometries_with_distances(aes, 'marinemanagedareas')
    
'''
Determines the Fishery Closures for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_fishery_closures(aes):
    return get_nearest_geometries_with_distances(aes, 'fisheryclosures')
    
'''
Determines the Nearest Conservation Areas for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_conservation_areas(aes):
    return get_nearest_geometries_with_distances(aes, 'conservationareas')
    