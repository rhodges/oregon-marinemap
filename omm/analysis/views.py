from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from tsp.models import AOI

'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run nsh analysis on 
'''
def nsh_analysis(request, nsh_id, type):
    from nsh_analysis import display_nsh_analysis
    nsh = get_object_or_404(AOI, pk=nsh_id)
    return display_nsh_analysis(request, nsh, type)
    
'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run aes analysis on 
'''
def aes_analysis(request, aes_id, type):
    return HttpResponse('Energy Site Analysis is not yet available.')
    
'''
'''
def pdf_nsh_report(request, nsh_id, type):
    from nsh_analysis import pdf_report
    from lingcod.common.utils import get_mpa_class
    from lingcod.sharing.utils import can_user_view
    user_can_view, response = can_user_view(get_mpa_class(), nsh_id, request.user)
    if not user_can_view:
        return response
    nsh = get_object_or_404(AOI, pk=nsh_id)
    return pdf_report(request, nsh, type)
    
'''
Accessed via named url when user selects View Printable Report from analysis templates
'''    
def print_nsh_report(request, nsh_id, type):
    from nsh_analysis import printable_report
    from lingcod.common.utils import get_mpa_class
    from lingcod.sharing.utils import can_user_view
    user_can_view, response = can_user_view(get_mpa_class(), nsh_id, request.user)
    if not user_can_view:
        return response
    nsh = get_object_or_404(AOI, pk=nsh_id)
    return printable_report(request, nsh, type)
    
'''
Empties NSHCache table
Handles POST requests
'''
def admin_clear_nsh_cache(request, type=None, template='admin/analysis/cache_is_cleared.html'):
    from nsh_cache import clear_cache, remove_cache
    from utils import ensure_type
    if not request.user.is_staff:
        return HttpResponse('You do not have permission to view this feature', status=401)
    if request.method == 'POST':
        type = ensure_type(type)
        if type is None:
            clear_cache(i_am_sure=True)
            return render_to_response( template, RequestContext(request, {"type": "All"}) )  
        else:
            remove_cache(type=type)
            return render_to_response( template, RequestContext(request, {"type": type}) )  
    
        
    
   