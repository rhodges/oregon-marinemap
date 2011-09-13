from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from tsp.models import AOI
import settings

'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run nsh analysis on 
'''
def nsh_analysis(request, nsh_id, type):
    from nsh.nsh_analysis import display_nsh_analysis
    nsh = get_object_or_404(AOI, pk=nsh_id)
    #check permissions
    viewable, response = nsh.is_viewable(request.user)
    if not viewable:
        return response
    return display_nsh_analysis(request, nsh, type)
    
'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run aes analysis on 
'''
def aes_analysis(request, aes_id, type):
    from aes.aes_analysis import display_aes_analysis
    aes = get_object_or_404(AOI, pk=aes_id)
    #check permissions
    viewable, response = aes.is_viewable(request.user)
    if not viewable:
        return response
    return display_aes_analysis(request, aes, type)

'''
'''    
def shoreside_analysis(request, aoi_id, type):
    from econ import commercial, charter, recreational
    aoi = get_object_or_404(AOI, pk=aoi_id)
    
    #check permissions
    viewable, response = aoi.is_viewable(request.user)
    if not viewable:
        return response
    #use something similar to the following to limit url access to these reports 
    #might have settings var for shoreside group 
    if request.user.groups.filter(name=settings.SHORESIDE_GROUP).count() == 0:
        return HttpResponse("access denied", status=403)
    
    if type == 'noaa':
        context = commercial.get_commercial_context(aoi, type)
        template = 'econ/commercial_noaa_report.html'
    elif type == 'feam':
        context = commercial.get_commercial_context(aoi, type)
        template = 'econ/commercial_feam_report.html'
    elif type == 'chrt':
        context = charter.get_charter_context(aoi)
        template = 'econ/charter_report.html'
    elif type == 'rec':
        context = recreational.get_recreational_context(aoi)
        template = 'econ/recreational_report.html'
    else:
        context = None
        template = None
    return render_to_response(template, RequestContext(request, context)) 
    
'''
'''    
def excel_nsh_report(request, nsh_id, type):
    from nsh.nsh_analysis import excel_report
    nsh = get_object_or_404(AOI, pk=nsh_id)
    user_can_view, response = nsh.is_viewable(request.user)
    if not user_can_view:
        return response
    return excel_report(request, nsh, type)
    
'''
'''    
def excel_aes_report(request, aes_id, type):
    from aes.aes_analysis import excel_report
    aes = get_object_or_404(AOI, pk=aes_id)
    user_can_view, response = aes.is_viewable(request.user)
    if not user_can_view:
        return response
    return excel_report(request, aes, type)
    
'''
'''    
def excel_econ_report(request, aoi_id, type):
    from econ.econ_exports import excel_report
    aoi = get_object_or_404(AOI, pk=aoi_id)
    user_can_view, response = aoi.is_viewable(request.user)
    if not user_can_view:
        return response
    return excel_report(request, aoi, type)    
    
'''
'''
def pdf_nsh_report(request, nsh_id, type):
    from nsh.nsh_analysis import pdf_report
    nsh = get_object_or_404(AOI, pk=nsh_id)
    user_can_view, response = nsh.is_viewable(request.user)
    if not user_can_view:
        return response
    return pdf_report(request, nsh, type)
    
'''
'''
def pdf_aes_report(request, aes_id, type):
    from aes.aes_analysis import pdf_report
    aes = get_object_or_404(AOI, pk=aes_id)
    user_can_view, response = aes.is_viewable(request.user)
    if not user_can_view:
        return response
    return pdf_report(request, aes, type)
    
'''
'''
def pdf_econ_report(request, aoi_id, type):
    from econ.econ_exports import pdf_report
    aoi = get_object_or_404(AOI, pk=aoi_id)
    user_can_view, response = aoi.is_viewable(request.user)
    if not user_can_view:
        return response
    return pdf_report(request, aoi, type)
    
'''
Accessed via named url when user selects View Printable Report from analysis templates
'''    
def print_nsh_report(request, nsh_id, type):
    from nsh.nsh_analysis import printable_report
    nsh = get_object_or_404(AOI, pk=nsh_id)
    user_can_view, response = nsh.is_viewable(request.user)
    if not user_can_view:
        return response
    return printable_report(request, nsh, type)
    
'''
Accessed via named url when user selects View Printable Report from analysis templates
'''    
def print_aes_report(request, aes_id, type):
    from aes.aes_analysis import printable_report
    aes = get_object_or_404(AOI, pk=aes_id)
    user_can_view, response = aes.is_viewable(request.user)
    if not user_can_view:
        return response
    return printable_report(request, aes, type)
    
'''
'''
def print_econ_report(request, aoi_id, type):
    from econ.econ_exports import printable_report
    aoi = get_object_or_404(AOI, pk=aoi_id)
    user_can_view, response = aoi.is_viewable(request.user)
    if not user_can_view:
        return response
    return printable_report(request, aoi, type)
    
    
'''
Empties NSHCache table
Handles POST requests
'''
def admin_clear_nsh_cache(request, type=None, template='admin/analysis/nshcache/cache_is_cleared.html'):
    from nsh.nsh_cache import clear_nsh_cache, remove_nsh_cache
    from aes.aes_cache import remove_related_aes_cache
    from utils import ensure_type
    if not request.user.is_staff:
        return HttpResponse('You do not have permission to view this feature', status=401)
    if request.method == 'POST':
        type = ensure_type(type)
        if type is None:
            clear_nsh_cache(i_am_sure=True)
            remove_related_aes_cache(type)
            return render_to_response( template, RequestContext(request, {"type": "All"}) )  
        else:
            remove_nsh_cache(type=type)
            remove_related_aes_cache(type)
            return render_to_response( template, RequestContext(request, {"type": type}) )  
    
'''
Empties NSHCache table
Handles POST requests
'''
def admin_clear_aes_cache(request, type=None, template='admin/analysis/aescache/cache_is_cleared.html'):
    from aes.aes_cache import clear_aes_cache, remove_aes_cache
    from utils import ensure_type
    if not request.user.is_staff:
        return HttpResponse('You do not have permission to view this feature', status=401)
    if request.method == 'POST':
        type = ensure_type(type)
        if type is None:
            clear_aes_cache(i_am_sure=True)
            return render_to_response( template, RequestContext(request, {"type": "All"}) )  
        else:
            remove_aes_cache(type=type)
            return render_to_response( template, RequestContext(request, {"type": type}) )  
    
        
    
   
