from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from NSH_Geography import display_geo_analysis, run_geo_analysis
from NSH_Physical import display_phy_analysis, run_phy_analysis
from NSH_Biology import display_bio_analysis, run_bio_analysis
from NSH_Human import display_hum_analysis, run_hum_analysis
from utils import type_is_geo, type_is_phy, type_is_bio, type_is_hum
from NSH_Cache import has_cache, get_cache

'''
calls display_<type>_analysis for a given type
called by views.nsh_analysis
'''
def display_nsh_analysis(request, nsh, type):
    if type_is_geo(type):
        return display_geo_analysis(request, nsh)
    elif type_is_phy(type):
        return display_phy_analysis(request, nsh)
    elif type_is_bio(type): 
        return display_bio_analysis(request, nsh)
    else: #must be Human Uses
        return display_hum_analysis(request, nsh)
    
'''
calls run_<type>_analysis for a given type
called by get_or_create_cache
'''    
def run_nsh_analysis(nsh, type):   
    if type_is_geo(type):
        return run_geo_analysis(nsh, type)
    elif type_is_phy(type):
        return run_phy_analysis(nsh, type)
    elif type_is_bio(type): 
        return run_bio_analysis(nsh, type)
    else: #must be Human Uses
        return run_hum_analysis(nsh, type)
    
'''
renders template with type-specific context
called by views.print_nsh_report
'''    
def printable_report(request, nsh, type):
    template = get_printable_template(type)
    context = get_or_create_cache(nsh, type)
    return render_to_response(template, RequestContext(request, context))
    
'''
renders printable template as pdf
called by views.pdf_nsh_report
'''    
def pdf_report(request, nsh, type):
    from django.template.loader import render_to_string
    import ho.pisa as pisa 
    import cStringIO as StringIO
    template = get_printable_template(type)
    context = get_or_create_cache(nsh, type)
    html = render_to_string(template, context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('This PDF request is temporarily un-available.') 
    
'''
Returns a path to desired resource (image file)
Called from within pisaDocument via link_callback parameter (from pdf_report)
'''    
def fetch_resources(uri, rel):
    import os
    import settings
    from lingcod.staticmap.temp_save import save_to_temp
    params = get_params_from_uri(uri)
    if len(params) > 0:
        path = save_to_temp(params)
    else:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path
    
'''
Returns a dictionary representation of the parameters attached to the given uri
Called by fetch_resources
'''    
def get_params_from_uri(uri):
    from urlparse import urlparse
    results = urlparse(uri)
    params = {}
    if results.query == '':
        return params
    params_list = results.query.split('&')
    for param in params_list:
        pair = param.split('=')
        params[pair[0]] = pair[1]
    return params
    
'''
retrieves the type-specific context from cache, or if not yet cached, by running the analysis
called by printable_report and pdf_report
'''      
def get_or_create_cache(nsh, type):
    if type == 'all':
        all_context = {}
        for single_type in ['geo', 'phy', 'bio', 'hum']:
            if has_cache(nsh, single_type):
                context = get_cache(nsh, single_type)
            else:
                context = run_nsh_analysis(nsh, single_type)
            all_context[single_type] = context
        return all_context
    elif has_cache(nsh, type):
        return get_cache(nsh, type)
    else:
        context = run_nsh_analysis(nsh, type)
    return context
        
'''
Returns template name associated with given type
Called by printable_report and pdf_report
'''        
def get_printable_template(type):
    if type_is_geo(type):
        template='printable_nsh_geo_report.html'
    elif type_is_phy(type):
        template='printable_nsh_phy_report.html'
    elif type_is_bio(type):
        template='printable_nsh_bio_report.html'
    elif type_is_hum(type):
        template='printable_nsh_hum_report.html'
    else:
        template='printable_nsh_comprehensive_report.html'    
    return template
    