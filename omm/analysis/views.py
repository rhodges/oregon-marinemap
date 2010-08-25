from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from tsp.models import AOI

'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run nsh analysis on 
'''
def nsh_analysis(request, nsh_id, type):
    from NSH_Analysis import display_nsh_analysis
    return display_nsh_analysis(request, nsh_id, type)
    
'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run aes analysis on 
'''
def aes_analysis(request, aes_id, type):
    return HttpResponse('Energy Site Analysis is not yet available.')
    
def print_report(request, nsh_id, type):
    from NSH_Analysis import print_nsh_report
    from lingcod.common.utils import get_mpa_class
    from lingcod.sharing.utils import can_user_view
    from utils import type_is_geo
    user_can_view, response = can_user_view(get_mpa_class(), nsh_id, request.user)
    if not user_can_view:
        return response
    nsh = get_object_or_404(AOI, pk=nsh_id)
    return print_nsh_report(request, nsh, type)
    
'''
Empties NSHCache table
Handles POST requests
'''
def adminClearCache(request, template='admin/analysis/cache_is_cleared.html'):
    from NSH_Cache import clear_cache
    if not request.user.is_staff:
        return HttpResponse('You do not have permission to view this feature', status=401)
    if request.method == 'POST':
        clear_cache(i_am_sure=True)
        return render_to_response( template, RequestContext(request, {}) )  
    
        
    
   