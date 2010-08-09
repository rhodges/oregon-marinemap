from django.http import HttpResponse

def type_is_geo(type):
    lc_type = type.lower()
    if lc_type in ['geo', 'geometry']:
        return True
    return False

def display_nsh_analysis(request, nsh_id, type):
    if type_is_geo(type):
        from Geography import display_geo_analysis
        return display_geo_analysis(request, nsh_id)
    return HttpResponse('non-Geography requests not currently handled')