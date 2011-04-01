from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from aes_geography import display_aes_geo_analysis, get_aes_geo_context
from aes_physical import display_phy_analysis, get_aes_phy_context
from aes_biology import display_bio_analysis, get_aes_bio_context
from aes_human import display_aes_hum_analysis, get_aes_hum_context
from analysis.utils import type_is_geo, type_is_phy, type_is_bio, type_is_hum
from analysis.excel.utils import build_excel_response
from aes_cache import aes_cache_exists, get_aes_cache
from django.template.defaultfilters import slugify
from lingcod.common.utils import fetch_resources

'''
calls display_<type>_analysis for a given type
called by views.aes_analysis
'''
def display_aes_analysis(request, aes, type):
    if type_is_geo(type):
        return display_aes_geo_analysis(request, aes)
    elif type_is_phy(type):
        return display_phy_analysis(request, aes)
    elif type_is_bio(type):
        return display_bio_analysis(request, aes)
    elif type_is_hum(type):
        return display_aes_hum_analysis(request, aes)
    else: 
        return HttpResponse('Energy Site Analysis for this selection is not available.')
    
'''
calls run_<type>_analysis for a given type
called by get_or_create_cache
'''    
def get_aes_context(aes, type):   
    if type_is_geo(type):
        return get_aes_geo_context(aes, type)
    elif type_is_phy(type):
        return get_aes_phy_context(aes, type)
    elif type_is_bio(type): 
        return get_aes_bio_context(aes, type)
    else: #must be Human Uses
        return get_aes_hum_context(aes, type)
    
'''
renders template with type-specific context
called by views.print_aes_report
'''    
def printable_report(request, aes, type):
    template = get_printable_template(type)
    context = get_or_create_cache(aes, type)
    return render_to_response(template, RequestContext(request, context))
    
'''
currently in the testing phase: /analysis/aes/excel_report/1112/all
'''    
def excel_report(request, aes, type):
    from aes_excel import generate_aes_excel_doc
    context = get_or_create_cache(aes, type)
    excel_doc = generate_aes_excel_doc(context)
    
    return build_excel_response(slugify("EnergySiteReport.xls"),excel_doc) 
    
'''
renders printable template as pdf
called by views.pdf_aes_report
'''    
def pdf_report(request, aes, type, template='aes_pdf_comprehensive_report.html'):
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
        res = HttpResponse(result.getvalue(), mimetype='application/pdf')
        res['Content-Disposition'] = 'filename=aes_report_%s.pdf' % aes.uid
        return res
    return HttpResponse('This PDF request is temporarily un-available.') 
    
'''
retrieves the type-specific context from cache, or if not yet cached, by running the analysis
called by printable_report and pdf_report
'''      
def get_or_create_cache(aes, type):
    if type == 'all':
        all_context = {}
        for single_type in ['geo', 'phy', 'bio', 'hum']:
            if aes_cache_exists(aes, single_type):
                context = get_aes_cache(aes, single_type)
            else:
                context = get_aes_context(aes, single_type)
            all_context[single_type] = context
        return all_context
    elif aes_cache_exists(aes, type):
        return get_aes_cache(aes, type)
    else:
        context = get_aes_context(aes, type)
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
    
