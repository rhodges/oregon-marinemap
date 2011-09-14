from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from commercial import get_commercial_context
from charter import get_charter_context
from recreational import get_recreational_context

from analysis.excel.utils import build_excel_response
from econ_cache import econ_cache_exists, get_econ_cache
from django.template.defaultfilters import slugify
from lingcod.common.utils import fetch_resources


'''
called from analysis.views.excel_econ_report
'''    
def excel_report(request, aoi, type):
    from econ_excel import generate_econ_excel_doc
    context = get_or_create_cache(aoi, type)
    excel_doc = generate_econ_excel_doc(context, type)
    return build_excel_response(slugify("EconomicReport.xls"),excel_doc) 

'''
renders printable template as pdf
called from analysis.views.pdf_econ_report
'''    
def pdf_report(request, aoi, type):
    from django.template.loader import render_to_string
    import ho.pisa as pisa 
    import cStringIO as StringIO
    context = get_or_create_cache(aoi, type)
    context = toggle_pdf_var(context)
    #template = get_econ_template(type)
    template = 'econ/pdf_report.html'
    context['type'] = type
    context['name'] = aoi.name
    context['uid'] = aoi.uid
    context['title'] = get_title(type)
    context.update(add_includes(type))
    if type == 'all':
        html = render_to_string(template, context)
        filename = 'comprehensive_economic_report_%s.pdf' % aoi.uid
    else:
        html = render_to_string(template, context)
        filename = '%s_economic_report_%s.pdf' % (type, aoi.uid)
    result = StringIO.StringIO()
    #NOTE:  the following results in an error unless an error in PIL/Image.py file (PIL 1.7) is modified
    #       see omm_requirements.txt for further details
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
    if not pdf.err:
        res = HttpResponse(result.getvalue(), mimetype='application/pdf')
        res['Content-Disposition'] = 'filename=%s' % filename
        return res
    return HttpResponse('This PDF request is temporarily un-available.')     
   
def toggle_pdf_var(context):
    for key, items in context.items():
        context[key]['pdf'] = True
    return context
   
'''
renders template with type-specific context
called from views.print_econ_report
'''    
def printable_report(request, aoi, type):
    #template = get_printable_template(type)
    template = 'econ/printable_report.html'
    context = get_or_create_cache(aoi, type)
    toggle_printable_var(context)
    context['type'] = type
    context['name'] = aoi.name
    context['title'] = get_title(type)
    context.update(add_includes(type))
    return render_to_response(template, RequestContext(request, context))
    
def toggle_printable_var(context):
    for key, items in context.items():
        context[key]['printable'] = True
    return context
    
'''
retrieves the type-specific context from cache, or if not yet cached, by running the analysis
'''      
def get_or_create_cache(aoi, type):
    if type == 'all':
        context = {}
        for single_type in ['noaa', 'feam', 'chrt', 'rec']:
            if econ_cache_exists(aoi, single_type):
                context.update(get_econ_cache(aoi, single_type))
            else:
                context.update(get_econ_context(aoi, single_type))
        return context
    elif econ_cache_exists(aoi, type):
        context = get_econ_cache(aoi, type)
        return context
    else:
        context = get_econ_context(aoi, type)
    return context

'''
'''    
def get_econ_context(aoi, type):   
    if type == 'noaa':
        return get_commercial_context(aoi, type)
    elif type == 'feam':
        return get_commercial_context(aoi, type)
    elif type == 'chrt': 
        return get_charter_context(aoi, type)
    elif type == 'rec': 
        return get_recreational_context(aoi, type)
    else:
        raise ValueError('Incorrect type, %s, sent to get_econ_context' %type)

def get_econ_template(type):
    if type == 'noaa':
        template = 'econ/commercial_noaa_report.html'
    elif type == 'feam':
        template = 'econ/commercial_feam_report.html'
    elif type == 'chrt':
        template = 'econ/charter_report.html'
    elif type == 'rec':
        template = 'econ/recreational_report.html'   
    elif type == 'all':
        template = 'econ/comprehensive_pdf_report.html'
    else:
        raise ValueError("Invalid type, %s, sent to get_econ_template" %type)
    return template

def get_title(type):
    if type == 'noaa':
        title = 'NOAA Commercial Fishing Analysis'
    elif type == 'feam':
        title = 'FEAM Commercial Fishing Analysis'
    elif type == 'chrt':
        title = 'Charter Fishing Analysis'
    elif type == 'rec':
        title = 'Recreational Fishing Analysis'   
    elif type == 'all':
        title = 'Comprehensive Fishing Analysis'
    else:
        raise ValueError("Invalid type, %s, sent to get_econ_template" %type)
    return title    
    
def add_includes(type):
    includes = {}
    if type == 'noaa':
        includes['template'] = 'econ/commercial_noaa_report.html'
    elif type == 'feam':
        includes['template'] = 'econ/commercial_feam_report.html'
    elif type == 'chrt':
        includes['template'] = 'econ/charter_report.html'
    elif type == 'rec':
        includes['template'] = 'econ/recreational_report.html'   
    elif type == 'all':
        includes['templates'] = ['econ/commercial_noaa_report.html', 'econ/commercial_feam_report.html', 'econ/charter_report.html', 'econ/recreational_report.html']
    else:
        raise ValueError("Invalid type, %s, sent to get_econ_template" %type)
    return includes        
    
def get_printable_template(type):
    if type == 'noaa':
        template = 'econ/commercial_noaa_report.html'
    elif type == 'feam':
        template = 'econ/commercial_feam_report.html'
    elif type == 'chrt':
        template = 'econ/charter_report.html'
    elif type == 'rec':
        template = 'econ/recreational_report.html'   
    elif type == 'all':
        template = 'econ/comprehensive_printable_report.html'
    else:
        raise ValueError("Invalid type, %s, sent to get_econ_template" %type)
    return template    