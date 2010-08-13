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
    
    context = {'aoi': nsh, 'default_value': default_value, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'area_units': settings.DISPLAY_AREA_UNITS, 'parks': parks, 'access_sites': access_sites, 'dmd_sites': dmd_sites, 'nearest_dmds': nearest_dmds}
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
    