from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tsp.models import AOI
from models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units

default_value = '---'

'''
Runs analysis for Biological report
Renders the Biological Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_bio_analysis(request, nsh_id, template='Bio_Report.html'):
    nsh = get_object_or_404(AOI, pk=nsh_id)
    #get pinniped haulout details
    haulout_details = get_haulout_details(nsh)
    #get stellar sea lion rookery details
    
    #get bird colony details
    bird_details = get_bird_colony_details(nsh)
    #get habitat types and proportions
    habitat_proportions = get_habitat_proportions(nsh)
    #get kelp survey data
    kelp_data = get_kelp_data(nsh)
    
    context = {'aoi': nsh, 'default_value': default_value, 'area_units': settings.DISPLAY_AREA_UNITS, 'haulouts': len(haulout_details), 'haulout_sites': haulout_details, 'bird_colonies': len(bird_details), 'bird_details': bird_details, 'habitat_proportions': habitat_proportions, 'kelp_data': kelp_data}
    return render_to_response(template, RequestContext(request, context)) 
     
'''
Determines the Pinniped Haulout Details for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_haulout_details(nsh):
    pinniped_haulouts = PinnipedHaulouts.objects.all()
    inter_haulouts = [haulout for haulout in pinniped_haulouts if haulout.geometry.intersects(nsh.geometry_final)]
    locations_and_sites = [(haulout.location, haulout.site) for haulout in inter_haulouts]
    return locations_and_sites
    
'''
Determines the Seabird Colony Details for the given nearshore habitat shape
Called by display_phy_analysis
'''
def get_bird_colony_details(nsh):
    bird_colonies = SeabirdColonies.objects.all()
    inter_colonies = [colony for colony in bird_colonies if colony.geometry.intersects(nsh.geometry_final)]
    species = [colony.species for colony in inter_colonies]
    species_dict = {}
    for spec in species:
        if spec in species_dict.keys():
            species_dict[spec] += 1
        else:
            species_dict[spec] = 1
    species_tuples = species_dict.items()
    species_tuples.sort()
    return species_tuples
     
'''
Determines the areas and ratios for each represented lithology within the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_habitat_proportions(nsh):
    habitats = Habitats.objects.all()
    inter_habitats = [habitat for habitat in habitats if habitat.geometry.intersects(nsh.geometry_final)]
    inter_habitat_tuples = [(habitat.hab_type, habitat.geometry.intersection(nsh.geometry_final).area) for habitat in inter_habitats]
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
        proportion = habitat_dict[key] / total_area * 100
        habitat_proportion_list.append((key, proportion))
    habitat_proportion_list.sort()
    return habitat_proportion_list    
     
'''
Determines the areas and ratios for each kelp survey year represented within the given nearshore habitat shape
Called by display_phy_analysis
'''   
def get_kelp_data(nsh):
    kelp_surveys = KelpSurveys.objects.all()
    inter_surveys = [survey for survey in kelp_surveys if survey.geometry.intersects(nsh.geometry_final)]
    survey_dict = {}
    for survey in inter_surveys:
        if survey.kelp90 != 0:
            if survey.kelp90 not in survey_dict.keys():
                survey_dict[survey.kelp90] = survey.geometry.intersection(nsh.geometry_final).area
            else:
                survey_dict[survey.kelp90] += survey.geometry.intersection(nsh.geometry_final).area
        if survey.kelp96 != 0:
            if survey.kelp96 not in survey_dict.keys():
                survey_dict[survey.kelp96] = survey.geometry.intersection(nsh.geometry_final).area
            else:
                survey_dict[survey.kelp96] += survey.geometry.intersection(nsh.geometry_final).area
        if survey.kelp97 != 0:
            if survey.kelp97 not in survey_dict.keys():
                survey_dict[survey.kelp97] = survey.geometry.intersection(nsh.geometry_final).area
            else:
                survey_dict[survey.kelp97] += survey.geometry.intersection(nsh.geometry_final).area
        if survey.kelp98 != 0: 
            if survey.kelp98 not in survey_dict.keys():
                survey_dict[survey.kelp98] = survey.geometry.intersection(nsh.geometry_final).area
            else:
                survey_dict[survey.kelp98] += survey.geometry.intersection(nsh.geometry_final).area
        if survey.kelp99 != 0:
            if survey.kelp99 not in survey_dict.keys():
                survey_dict[survey.kelp99] = survey.geometry.intersection(nsh.geometry_final).area
            else:
                survey_dict[survey.kelp99] += survey.geometry.intersection(nsh.geometry_final).area
    survey_proportion_list = []
    for key in survey_dict.keys():
        proportion = survey_dict[key] / nsh.geometry_final.area * 100
        survey_proportion_list.append((key, area_in_display_units(survey_dict[key]), proportion))
    survey_proportion_list.sort()
    survey_proportion_list.reverse()
    return survey_proportion_list    
    
     