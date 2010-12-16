from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from analysis.models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units
from analysis.utils import ensure_type, default_value, get_intersecting_geometries, get_distance_to_nearest_geometry
from aes_cache import has_cache, get_cache, create_cache


'''
Runs analysis for Biological report
Renders the Biological Report template
Called by aes_Analysis.display_aes_analysis
'''
def display_bio_analysis(request, aes, type='Biology', template='aes_bio_report.html'):
    type = ensure_type(type)
    #get context from cache or from running analysis
    if has_cache(aes, type):
        #retrieve context from cache
        context = get_cache(aes, type)
    else:
        #get context by running analysis
        context = run_bio_analysis(aes, type) 

    return render_to_response(template, RequestContext(request, context)) 
     
'''
Run the analysis, create the cache, and return the results as a context dictionary so they may be rendered with template
'''    
def run_bio_analysis(aes, type):     
    #get pinniped haulout details
    num_haulouts, haulout_details = get_haulout_details(aes)
    #get stellar sea lion rookery details
    num_rookeries = get_num_rookeries(aes)
    #get stellar sea lion critical habitat details
    num_sealion_habs, sealion_habs = get_sealion_habitats(aes)
    #get bird colony details
    num_colonies, bird_details = get_bird_colony_details(aes)
    #get habitat types and proportions
    habitat_proportions = get_habitat_proportions(aes)
    #get fish list
    fish_list = get_fish_list(aes)
    #get kelp survey data
    kelp_data = get_kelp_data(aes)
    #get seagrass area
    seagrass_area = get_seagrass_area(aes)
    #get green sturgeon data (yes/no and percentage)
    green_sturgeon, green_sturgeon_perc = get_green_sturgeon_data(aes)
    #get distance to nearest western snowy plover critical habitat
    nearest_snowy_plover = distance_to_snowy_plover(aes)
    #get distance to nearest marbled murrelet critical habitat
    nearest_marbled_murrelet = distance_to_marbled_murrelet(aes)
    #get nearest coho populated stream
    nearest_coho_stream = get_nearest_coho_stream(aes)
    #compile context
    context = {'aes': aes, 'default_value': default_value, 'area_units': settings.DISPLAY_AREA_UNITS, 'length_units': settings.DISPLAY_LENGTH_UNITS, 'num_haulouts': num_haulouts, 'num_rookeries': num_rookeries, 'haulout_sites': haulout_details, 'num_sealion_habs': num_sealion_habs, 'sealion_habs': sealion_habs, 'bird_colonies': num_colonies, 'bird_details': bird_details, 'habitat_proportions': habitat_proportions, 'fish_list': fish_list, 'kelp_data': kelp_data, 'seagrass_area': seagrass_area, 'green_sturgeon': green_sturgeon, 'green_sturgeon_perc': green_sturgeon_perc, 'nearest_snowy_plover': nearest_snowy_plover, 'nearest_marbled_murrelet': nearest_marbled_murrelet, 'nearest_coho_stream': nearest_coho_stream}
    #cache these results
    create_cache(aes, type, context)   
    return context
        
def get_nearest_coho_stream(aes):
    coho_streams = Coho.objects.all()
    distances = [stream.geometry.distance(aes.geometry_final) for stream in coho_streams if stream.geometry.buffer(60000).intersects(aes.geometry_final)]
    distances.sort()
    return length_in_display_units(distances[0])
        
def distance_to_marbled_murrelet(aes):
    #murrelets = MarbledMurrelet.objects.all()
    #distances = [hab.geometry.centroid.distance(aes.geometry_final) for hab in murrelets]
    #distances.sort()
    distance = get_distance_to_nearest_geometry(aes, 'marbledmurrelet')
    return length_in_display_units(distance)

def distance_to_snowy_plover(aes):
    #snowy_plovers = SnowyPlover.objects.all()
    #distances = [hab.geometry.centroid.distance(aes.geometry_final) for hab in snowy_plovers]
    #distances.sort()
    distance = get_distance_to_nearest_geometry(aes, 'snowyplover')
    return length_in_display_units(distance)
    
def get_green_sturgeon_data(aes):
    coastal_overlaps = get_intersecting_geometries(aes, 'sturgeoncoastal')
    estuary_overlaps = get_intersecting_geometries(aes, 'sturgeonestuaries')
    if len(coastal_overlaps) > 0 or len(estuary_overlaps) > 0:
        presence = 'Yes'
    else:
        presence = 'No'
    aes_area = aes.geometry_final.area
    coastal_overlap_area = sum([overlap.area for overlap in coastal_overlaps])
    estuary_overlap_area = sum([overlap.area for overlap in estuary_overlaps])
    overlap_area = coastal_overlap_area + estuary_overlap_area
    overlap_area_percentage = overlap_area / aes_area * 100
    return presence, overlap_area_percentage
    
 
def get_sealion_habitats(aes):
    sealion_habitats = StellerHabitats.objects.all()
    inter_habs = [hab for hab in sealion_habitats if hab.geometry.intersects(aes.geometry_final)==True]
    hab_tuples = [(hab.name, hab.type) for hab in inter_habs if hab.geometry.intersects(aes.geometry_final)==True]
    hab_tuples.sort()
    num_habs = len(hab_tuples)
    return num_habs, hab_tuples
        
    
def get_seagrass_area(aes):
    seagrass = Seagrass.objects.all()
    inter_grass = [grass for grass in seagrass if grass.geometry.intersects(aes.geometry_final)==True]
    area_of_intersect = 0.0
    for grass in inter_grass:
        area_of_intersect += grass.geometry.intersection(aes.geometry_final).area
    area_of_intersect_converted_units = area_in_display_units(area_of_intersect)
    return area_of_intersect_converted_units
    
'''
Determines the Pinniped Haulout Details for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_haulout_details(aes):
    pinniped_haulouts = PinnipedHaulouts.objects.all()
    inter_haulouts = [haulout for haulout in pinniped_haulouts if haulout.geometry.intersects(aes.geometry_final)]
    
    haulout_dict = {}
    for haulout in inter_haulouts:
        key_tuple = (haulout.location, haulout.site)
        use_list = []
        if haulout.pv_use > 0:
            use_list.append('Pacific Harbor Seals')
        if haulout.ej_use > 0:
            use_list.append('Stellar Sea Lions')
        if haulout.zc_use > 0:
            use_list.append('California Sea Lions')
        haulout_dict[key_tuple] = (use_list)
    haulout_tuples = haulout_dict.items()
    haulout_tuples.sort()
    num_haulouts = len(inter_haulouts)
    return num_haulouts, haulout_tuples
    
'''
Determines the Pinniped Haulout Details for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_num_rookeries(aes):
    pinniped_haulouts = PinnipedHaulouts.objects.all()
    inter_haulouts = [haulout for haulout in pinniped_haulouts if haulout.geometry.intersects(aes.geometry_final)]
    rookeries = [haulout for haulout in inter_haulouts if haulout.ej_rookery > 0]
    num_rookeries = len(rookeries)
    return num_rookeries
    
'''
Determines the Seabird Colony Details for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_bird_colony_details(aes):
    bird_colonies = SeabirdColonies.objects.all()
    inter_colonies = [colony for colony in bird_colonies if colony.geometry.intersects(aes.geometry_final)]
    
    colony_dict = {}
    for colony in inter_colonies:
        key_tuple = (colony.site_name, colony.colno)
        if key_tuple in colony_dict.keys():
            colony_dict[key_tuple].append(colony.species)
        else:
            colony_dict[key_tuple] = [colony.species]
        colony_dict[key_tuple].sort()
    colony_tuples = colony_dict.items()
    colony_tuples.sort()
    #num_colonies = len(inter_colonies)
    num_colonies = len(colony_tuples)
    return num_colonies, colony_tuples
    
'''
Determines the areas and ratios for each represented lithology within the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_habitat_proportions(aes):
    habitats = Habitats.objects.all()
    inter_habitats = [habitat for habitat in habitats if habitat.geometry.intersects(aes.geometry_final)]
    inter_habitat_tuples = [(habitat.hab_type, habitat.geometry.intersection(aes.geometry_final).area) for habitat in inter_habitats]
    total_area = 0.0
    habitat_dict = {}
    for tuple in inter_habitat_tuples:
        if tuple[0] not in habitat_dict.keys():
            habitat_dict[tuple[0]] = tuple[1]
        else:
            habitat_dict[tuple[0]] += tuple[1]
        total_area += tuple[1]
    habitat_proportion_list = []
    for key in habitat_dict.keys():
        hab_type = key
        area = habitat_dict[key]
        proportion = area / total_area * 100
        habitat_proportion_list.append((proportion, hab_type, area_in_display_units(area)))
    habitat_proportion_list.sort()
    habitat_proportion_list.reverse()
    return habitat_proportion_list    
     
'''
Determines the areas and ratios for each kelp survey year represented within the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_kelp_data(aes):
    kelp_surveys = KelpSurveys.objects.all()
    inter_surveys = [survey for survey in kelp_surveys if survey.geometry.intersects(aes.geometry_final)]
    if len(inter_surveys) == 0:
        return [('None Recorded', default_value, default_value)]
    survey_dict = {}
    for survey in inter_surveys:
        if survey.kelp90 != 0:
            key = 'Coastwide Survey ' + str(survey.kelp90)
            if key not in survey_dict.keys():
                survey_dict[key] = survey.geometry.intersection(aes.geometry_final).area
            else:
                survey_dict[key] += survey.geometry.intersection(aes.geometry_final).area
        if survey.kelp96 != 0:
            key = 'Southern Oregon ' + str(survey.kelp96)
            if key not in survey_dict.keys():
                survey_dict[key] = survey.geometry.intersection(aes.geometry_final).area
            else:
                survey_dict[key] += survey.geometry.intersection(aes.geometry_final).area
        if survey.kelp97 != 0:
            key = 'Southern Oregon ' + str(survey.kelp97)
            if key not in survey_dict.keys():
                survey_dict[key] = survey.geometry.intersection(aes.geometry_final).area
            else:
                survey_dict[key] += survey.geometry.intersection(aes.geometry_final).area
        if survey.kelp98 != 0: 
            key = 'Southern Oregon ' + str(survey.kelp98)
            if key not in survey_dict.keys():
                survey_dict[key] = survey.geometry.intersection(aes.geometry_final).area
            else:
                survey_dict[key] += survey.geometry.intersection(aes.geometry_final).area
        if survey.kelp99 != 0:
            key = 'Southern Oregon ' + str(survey.kelp99)
            if key not in survey_dict.keys():
                survey_dict[key] = survey.geometry.intersection(aes.geometry_final).area
            else:
                survey_dict[key] += survey.geometry.intersection(aes.geometry_final).area
    survey_proportion_list = []
    for key in survey_dict.keys():
        area = survey_dict[key]
        proportion = survey_dict[key] / aes.geometry_final.area * 100
        survey_proportion_list.append((key, area_in_display_units(area), proportion))
    survey_proportion_list.sort()
    return survey_proportion_list    
    
def get_fish_list(aes):
    #get habitat types
    habs = GeologicalHabitat.objects.all()
    inter_habs = [hab for hab in habs if hab.geometry.intersects(aes.geometry_final)]
    hab_set = []
    for hab in inter_habs:
        sgh = hab.sgh_prefix + "/" + hab.sgh_lith1.lower()
        if hab.sgh_lith2 is not None:
            sgh += "/" + hab.sgh_lith2.lower()
        if sgh not in hab_set:
            hab_set.append(sgh)
    #hab_types = [hab.sgh_combo for hab in inter_habs]
    #hab_set = list(set(hab_types))
    hab_str = ','.join(hab for hab in hab_set)
    
    #get latitude range
    import settings
    from django.contrib.gis.geos import Polygon
    aes_geom = aes.geometry_final
    poly = Polygon.from_bbox(aes_geom.extent)
    poly.srid = settings.GEOMETRY_DB_SRID
    poly.transform(4326)
    latmin = poly.extent[1]
    latmax = poly.extent[3]
    #turns out the following messes with the wkt hash of the geometry used in caching
    #the cache is basically not found for Biology with the following code present:  
    #aes_geom.transform(4326) #transform into lat/lon
    #latmin = aes_geom.extent[1]
    #latmax = aes_geom.extent[3]
    #aes_geom.transform(settings.GEOMETRY_DB_SRID)
    
    #get depth range
    baths = Bathymetry.objects.all()
    inter_baths = [bath for bath in baths if bath.geometry.intersects(aes.geometry_final)]
    depths = [bath.depth for bath in inter_baths]
    depths.sort()
    deepmax = -depths[0] #smallest value will be the deepest
    deepmin = -depths[-1] #both should be expressed as a positive value
    
    #generate fish query
    query = "https://www.webapps.nwfsc.noaa.gov/pacoos/listfish?"
    query += "hab=" + hab_str
    query += "&latmin=" + str(latmin)
    query += "&latmax=" + str(latmax)
    query += "&depmin=" + str(deepmin)
    query += "&depmax=" + str(deepmax)
    
    #acquire the page source
    import urllib
    sock = urllib.urlopen(query)
    sourcelines = sock.readlines()
    sock.close()
        
    #scrape the fish names
    hrefs = [line for line in sourcelines if line.find("A HREF") != -1]
    fish = [href[href.find(')">')+3:href.find('</A>')] for href in hrefs]
    
    #scrape the latin names
    spans = [line for line in sourcelines if line.find("<span style=font-style:italic;>") != -1]
    latin_names = [span[span.find(";>")+2:span.find(")")] for span in spans]
    
    #create fish list
    fish_list = []
    for name in latin_names:
        fish_list.append(fish.pop(0) + " (" + name + ") ")
    fish_list.sort()
    return fish_list