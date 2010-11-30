from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from aes_geography import display_geo_analysis, run_geo_analysis
from aes_physical import display_phy_analysis, run_phy_analysis
from aes_biology import display_bio_analysis, run_bio_analysis
from aes_human import display_hum_analysis, run_hum_analysis
from analysis.utils import type_is_geo, type_is_phy, type_is_bio, type_is_hum
from aes_cache import has_cache, get_cache

'''
calls display_<type>_analysis for a given type
called by views.aes_analysis
'''
def display_aes_analysis(request, aes, type):
    if type_is_geo(type):
        return display_geo_analysis(request, aes)
    elif type_is_phy(type):
        return display_phy_analysis(request, aes)
    elif type_is_bio(type):
        return display_bio_analysis(request, aes)
    elif type_is_hum(type):
        return display_hum_analysis(request, aes)
    else: 
        return HttpResponse('Energy Site Analysis for this selection is not available.')
    
'''
calls run_<type>_analysis for a given type
called by get_or_create_cache
'''    
def run_aes_analysis(aes, type):   
    if type_is_geo(type):
        return run_geo_analysis(aes, type)
    elif type_is_phy(type):
        return run_phy_analysis(aes, type)
    elif type_is_bio(type): 
        return run_bio_analysis(aes, type)
    else: #must be Human Uses
        return run_hum_analysis(aes, type)
    
'''
renders template with type-specific context
called by views.print_aes_report
'''    
def printable_report(request, aes, type):
    template = get_printable_template(type)
    context = get_or_create_cache(aes, type)
    return render_to_response(template, RequestContext(request, context))
    
'''
renders printable template as pdf
called by views.pdf_aes_report
'''    
def pdf_report(request, aes, type, template='pdf_aes_comprehensive_report.html'):
    from django.template.loader import render_to_string
    import ho.pisa as pisa 
    import cStringIO as StringIO
    context = get_or_create_cache(aes, type)
    html = render_to_string(template, context)
    result = StringIO.StringIO()
    #NOTE:  the following results in an error unless an error in PIL/Image.py file (PIL 1.7) is modified
    #       see omm_requirements.txt for further details
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
def get_or_create_cache(aes, type):
    if type == 'all':
        all_context = {}
        for single_type in ['geo', 'phy', 'bio', 'hum']:
            if has_cache(aes, single_type):
                context = get_cache(aes, single_type)
            else:
                context = run_aes_analysis(aes, single_type)
            all_context[single_type] = context
        return all_context
    elif has_cache(aes, type):
        return get_cache(aes, type)
    else:
        context = run_aes_analysis(aes, type)
    return context
        
'''
Returns template name associated with given type
Called by printable_report and pdf_report
'''        
def get_printable_template(type):
    if type_is_geo(type):
        template='aes_printable_geo_report.html'
    elif type_is_phy(type):
        template='aes_printable_phy_report.html'
    elif type_is_bio(type):
        template='aes_printable_bio_report.html'
    elif type_is_hum(type):
        template='aes_printable_hum_report.html'
    else:
        template='aes_printable_comprehensive_report.html'    
    return template
    