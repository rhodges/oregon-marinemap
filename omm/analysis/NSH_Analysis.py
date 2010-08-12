from django.http import HttpResponse

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
        from Geography import display_geo_analysis
        return display_geo_analysis(request, nsh_id)
    elif type_is_phy(type):
        from Physical import display_phy_analysis
        return display_phy_analysis(request, nsh_id)
    elif type_is_bio(type): 
        from Biology import display_bio_analysis
        return display_bio_analysis(request, nsh_id)
    else: #must be Human Uses
        #from Human import display_hum_analysis
        #return display_hum_analysis(request, nsh_id)
        return HttpResponse('Human Use requests not currently handled')
    