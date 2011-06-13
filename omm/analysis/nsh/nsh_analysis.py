from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from nsh_geography import display_nsh_geo_analysis, get_nsh_geo_context
from nsh_physical import display_phy_analysis, get_nsh_phy_context
from nsh_biology import display_bio_analysis, get_nsh_bio_context
from nsh_human import display_nsh_hum_analysis, get_nsh_hum_context
from analysis.utils import type_is_geo, type_is_phy, type_is_bio, type_is_hum
from analysis.excel.utils import build_excel_response
from nsh_cache import nsh_cache_exists, get_nsh_cache
from django.template.defaultfilters import slugify
from lingcod.common.utils import fetch_resources

'''
calls display_<type>_analysis for a given type
called by views.nsh_analysis
'''
def display_nsh_analysis(request, nsh, type):
    if type_is_geo(type):
        return display_nsh_geo_analysis(request, nsh)
    elif type_is_phy(type):
        return display_phy_analysis(request, nsh)
    elif type_is_bio(type): 
        return display_bio_analysis(request, nsh)
    else: #must be Human Uses
        return display_nsh_hum_analysis(request, nsh)
    
'''
calls run_<type>_analysis for a given type
called by get_or_create_cache
'''    
def get_nsh_context(nsh, type):   
    if type_is_geo(type):
        return get_nsh_geo_context(nsh, type)
    elif type_is_phy(type):
        return get_nsh_phy_context(nsh, type)
    elif type_is_bio(type): 
        return get_nsh_bio_context(nsh, type)
    else: #must be Human Uses
        return get_nsh_hum_context(nsh, type)
    
'''
renders template with type-specific context
called by views.print_nsh_report
'''    
def printable_report(request, nsh, type):
    template = get_printable_template(type)
    context = get_or_create_cache(nsh, type)
    return render_to_response(template, RequestContext(request, context))
    
'''
currently in the testing phase: /analysis/nsh/excel_report/1112/all
'''    
def excel_report(request, nsh, type):
    from nsh_excel import generate_nsh_excel_doc
    context = get_or_create_cache(nsh, type)
    excel_doc = generate_nsh_excel_doc(context)
    
    return build_excel_response(slugify("NearshoreReport.xls"),excel_doc)    
    
'''
renders printable template as pdf
called by views.pdf_nsh_report
'''    
def pdf_report(request, nsh, type, template='nsh_pdf_comprehensive_report.html'):
    from django.template.loader import render_to_string
    import ho.pisa as pisa 
    import cStringIO as StringIO
    context = get_or_create_cache(nsh, type)
    html = render_to_string(template, context)
    result = StringIO.StringIO()
    #NOTE:  the following results in an error unless an error in PIL/Image.py file (PIL 1.7) is modified
    #       see omm_requirements.txt for further details
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
    if not pdf.err:
        res = HttpResponse(result.getvalue(), mimetype='application/pdf')
        res['Content-Disposition'] = 'filename=nsh_report_%s.pdf' % nsh.uid
        return res
    return HttpResponse('This PDF request is temporarily un-available.') 
    
'''
retrieves the type-specific context from cache, or if not yet cached, by running the analysis
called by printable_report and pdf_report
'''      
def get_or_create_cache(nsh, type):
    if type == 'all':
        all_context = {}
        for single_type in ['geo', 'phy', 'bio', 'hum']:
            if nsh_cache_exists(nsh, single_type):
                context = get_nsh_cache(nsh, single_type)
            else:
                context = get_nsh_context(nsh, single_type)
            all_context[single_type] = context
        return all_context
    elif nsh_cache_exists(nsh, type):
        return get_nsh_cache(nsh, type)
    else:
        context = get_nsh_context(nsh, type)
    return context
        
'''
Returns template name associated with given type
Called by printable_report and pdf_report
'''        
def get_printable_template(type):
    if type_is_geo(type):
        template='nsh_printable_geo_report.html'
    elif type_is_phy(type):
        template='nsh_printable_phy_report.html'
    elif type_is_bio(type):
        template='nsh_printable_bio_report.html'
    elif type_is_hum(type):
        template='nsh_printable_hum_report.html'
    else:
        template='nsh_printable_comprehensive_report.html'    
    return template
    
