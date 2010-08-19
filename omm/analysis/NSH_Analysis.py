from django.http import HttpResponse
from NSH_Geography import display_geo_analysis
from NSH_Physical import display_phy_analysis
from NSH_Biology import display_bio_analysis
from NSH_Human import display_hum_analysis

def type_is_geo(type):
    lc_type = type.lower()
    if lc_type in ['geo', 'geometry']:
        return True
    return False
    
def type_is_phy(type):
    lc_type = type.lower()
    if lc_type in ['phy', 'physical']:
        return True
    return False
    
def type_is_bio(type):
    lc_type = type.lower()
    if lc_type in ['bio', 'biological']:
        return True
    return False
    
def type_is_hum(type):
    lc_type = type.lower()
    if lc_type in ['hum', 'human']:
        return True
    return False

def display_nsh_analysis(request, nsh_id, type):
    if type_is_geo(type):
        return display_geo_analysis(request, nsh_id)
    elif type_is_phy(type):
        return display_phy_analysis(request, nsh_id)
    elif type_is_bio(type): 
        return display_bio_analysis(request, nsh_id)
    else: #must be Human Uses
        return display_hum_analysis(request, nsh_id)
    