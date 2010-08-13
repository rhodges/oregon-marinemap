from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tsp.models import AOI
from models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
import operator
    
default_value = '---'

'''
Runs analysis for Human Considerations report
Renders the Human Considerations Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_hum_analysis(request, nsh_id, template='Hum_Report.html'):
    nsh = get_object_or_404(AOI, pk=nsh_id)
    #get nearest state park
    parks = get_nearest_parks(nsh)
    #get nearest public access
    access_sites = get_nearest_access_sites(nsh)
    #get intersecting dredge material disposal sites
    dmd_sites = get_intersecting_dmds(nsh)
    #get nearest dredge material disposal sites
    nearest_dmds = get_nearest_dmds(nsh)
    #get intersecting npde outfall sites
    outfall_sites = get_intersecting_outfalls(nsh)
    #get nearest outfall sites
    nearest_outfalls = get_nearest_outfalls(nsh)
    #get intersecting undersea cable routes
    cables = get_intersecting_cables(nsh)
    #get nearest undersea cable route
    nearest_cables = get_nearest_cables(nsh)
    #does it intersect a towlane
    towlanes = intersects_towlane(nsh)
    #get intersecting wave energy sites
    wave_sites = get_intersecting_wave_energy_sites(nsh)
    #get nearest wave energy sites
    nearest_wave_sites = get_nearest_wave_energy_sites(nsh)
    #get nearest ports
    nearest_ports = get_nearest_ports(nsh)
    #get nearest marine managed areas
    nearest_mmas = get_nearest_mmas(nsh)
    #get nearest fishery closures
    nearest_closures = get_nearest_fishery_closures(nsh)
    #get nearest conservation areas
    nearest_conservation_areas = get_nearest_conservation_areas(nsh)
    
    context = {'aoi': nsh, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'parks': parks, 'access_sites': access_sites, 'dmd_sites': dmd_sites, 'nearest_dmds': nearest_dmds, 'outfall_sites': outfall_sites, 'nearest_outfalls': nearest_outfalls, 'cables': cables, 'nearest_cables': nearest_cables, 'towlanes': towlanes, 'wave_sites': wave_sites, 'nearest_wave_sites': nearest_wave_sites, 'nearest_ports': nearest_ports, 'nearest_mmas': nearest_mmas, 'nearest_closures': nearest_closures, 'nearest_conservation_areas': nearest_conservation_areas}
    return render_to_response(template, RequestContext(request, context)) 
     
'''
Determines the Nearest State Park for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_parks(nsh):
    parks = StateParks.objects.all()
    park_tuples = [(park.geometry.centroid.distance(nsh.geometry_final), park) for park in parks]
    park_tuples.sort()
    park_tuples = park_tuples[:3]
    nearest_parks = []
    for tuple in park_tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_parks.append( (name, distance) )
    #sorting here just in case distance by centroid differed from distance by polygons
    nearest_parks = sorted(nearest_parks, key=operator.itemgetter(1))
    return nearest_parks
    
'''
Determines the Nearest Public Access Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_access_sites(nsh):
    access_sites = PublicAccess.objects.all()
    #getting distance by centroid here since distance by polygon is so painstakingly slow
    site_tuples = [(site.geometry.centroid.distance(nsh.geometry_final), site) for site in access_sites]
    site_tuples.sort()
    site_tuples = site_tuples[:3]
    nearest_sites = []
    for tuple in site_tuples:
        name = tuple[1].loc
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_sites.append( (name, distance) )
    #sorting here just in case distance by centroid differed from distance by polygons
    nearest_sites = sorted(nearest_sites, key=operator.itemgetter(1))
    return nearest_sites
    
'''
Determines the Intersecting Dredge Material Disposal Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_intersecting_dmds(nsh):
    dmd_sites = DMDSites.objects.all()
    inter_sites = [site for site in dmd_sites if site.geometry.intersects(nsh.geometry_final)]
    if len(inter_sites) == 0:
        inter_sites.append(default_value)
    else:
        inter_sites = [site.name for site in inter_sites]
    return inter_sites
    
'''
Determines the Nearest Dredge Material Disposal Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_dmds(nsh):
    dmd_sites = DMDSites.objects.all()
    site_tuples = [(site.geometry.centroid.distance(nsh.geometry_final), site) for site in dmd_sites]
    site_tuples.sort()
    site_tuples = site_tuples[:3]
    nearest_sites = []
    for tuple in site_tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_sites.append( (name, distance) )
    #sorting here just in case distance by centroid differed from distance by polygons
    nearest_sites = sorted(nearest_sites, key=operator.itemgetter(1))
    return nearest_sites
    
'''
Determines the Intersecting NPDE Outfall Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_intersecting_outfalls(nsh):
    outfall_sites = Outfalls.objects.all()
    inter_sites = [site for site in outfall_sites if site.geometry.intersects(nsh.geometry_final)]
    if len(inter_sites) == 0:
        inter_sites.append(default_value)
    else:
        inter_sites = [site.common_nam for site in inter_sites]
    return inter_sites
    
'''
Determines the Nearest Outfall Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_outfalls(nsh):
    outfall_sites = Outfalls.objects.all()
    site_tuples = [(site.geometry.centroid.distance(nsh.geometry_final), site) for site in outfall_sites]
    site_tuples.sort()
    site_tuples = site_tuples[:3]
    nearest_sites = []
    for tuple in site_tuples:
        name = tuple[1].common_nam
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_sites.append( (name, distance) )
    #sorting here just in case distance by centroid differed from distance by polygons
    nearest_sites = sorted(nearest_sites, key=operator.itemgetter(1))
    return nearest_sites
     
'''
Determines the Intersecting Undersea Cable Routes for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_intersecting_cables(nsh):
    cable_routes = UnderseaCables.objects.all()
    inter_cables = [cable for cable in cable_routes if cable.geometry.intersects(nsh.geometry_final)]
    if len(inter_cables) == 0:
        inter_cables.append(default_value)
    else:
        inter_cables = [cable.name for cable in inter_cables]
    return inter_cables
    
'''
Determines the Nearest Undersea Cable Routes for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_cables(nsh):
    cable_routes = UnderseaCables.objects.all()
    cable_tuples = [(cable.geometry.distance(nsh.geometry_final), cable) for cable in cable_routes]
    cable_tuples.sort()
    cable_tuples = cable_tuples[:3]
    nearest_cables = []
    for tuple in cable_tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[0])
        nearest_cables.append( (name, distance) )
    return nearest_cables
     
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
Determines the Wave Energy Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_intersecting_wave_energy_sites(nsh):
    wave_sites = WaveEnergyPermits.objects.all()
    inter_sites = [site for site in wave_sites if site.geometry.intersects(nsh.geometry_final)]
    if len(inter_sites) == 0:
        inter_sites.append((default_value, default_value))
    else:
        inter_sites = [(site.project, site.geometry.intersection(nsh.geometry_final).area / nsh.geometry_final.area * 100) for site in inter_sites]
    return inter_sites
    
'''
Determines the Nearest Wave Energy Sites for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_wave_energy_sites(nsh):
    wave_sites = WaveEnergyPermits.objects.all()
    wave_tuples = [(site.geometry.centroid.distance(nsh.geometry_final), site) for site in wave_sites]
    wave_tuples.sort()
    wave_tuples = wave_tuples[:3]
    nearest_sites = []
    for tuple in wave_tuples:
        name = tuple[1].project
        distance = length_in_display_units(tuple[0])
        nearest_sites.append( (name, distance) )
    return nearest_sites
     
'''
Determines the Nearest Ports for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_ports(nsh):
    ports = Ports.objects.all()
    port_tuples = [(port.geometry.distance(nsh.geometry_final), port) for port in ports]
    port_tuples.sort()
    port_tuples = port_tuples[:3]
    nearest_ports = []
    for tuple in port_tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[0])
        nearest_ports.append( (name, distance) )
    return nearest_ports
    
'''
Determines the Nearest Marine Managed Areas for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_mmas(nsh):
    mmas = MarineManagedAreas.objects.all()
    mma_tuples = [(mma.geometry.centroid.distance(nsh.geometry_final), mma) for mma in mmas]
    mma_tuples.sort()
    mma_tuples = mma_tuples[:3]
    nearest_mmas = []
    for tuple in mma_tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_mmas.append( (name, distance) )
    return nearest_mmas
    
'''
Determines the Fishery Closures for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_fishery_closures(nsh):
    closures = FisheryClosures.objects.all()
    closure_tuples = [(closure.geometry.centroid.distance(nsh.geometry_final), closure) for closure in closures]
    closure_tuples.sort()
    closure_tuples =closure_tuples[:3]
    nearest_closures = []
    for tuple in closure_tuples:
        name = tuple[1].name
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_closures.append( (name, distance) )
    return nearest_closures
    
'''
Determines the Nearest Conservation Areas for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_nearest_conservation_areas(nsh):
    con_areas = ConservationAreas.objects.all()
    area_tuples = [(area.geometry.centroid.distance(nsh.geometry_final), area) for area in con_areas]
    area_tuples.sort()
    area_tuples = area_tuples[:3]
    nearest_areas = []
    for tuple in area_tuples:
        name = tuple[1].area_name
        distance = length_in_display_units(tuple[1].geometry.distance(nsh.geometry_final))
        nearest_areas.append( (name, distance) )
    return nearest_areas