from django.http import HttpResponse
from NSH_Geography import display_geo_analysis
from NSH_Physical import display_phy_analysis
from NSH_Biology import display_bio_analysis
from NSH_Human import display_hum_analysis
from utils import type_is_geo, type_is_phy, type_is_bio, type_is_hum


def display_nsh_analysis(request, nsh_id, type):
    if type_is_geo(type):
        return display_geo_analysis(request, nsh_id)
    elif type_is_phy(type):
        return display_phy_analysis(request, nsh_id)
    elif type_is_bio(type): 
        return display_bio_analysis(request, nsh_id)
    else: #must be Human Uses
        return display_hum_analysis(request, nsh_id)
    