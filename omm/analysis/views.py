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
        
    
'''
Accessed via named url when user selects a type (Geographic, Physical, Biological, Human Uses) to run aes analysis on 
def aes_analysis_panel(request, aoi_id, type, template='aes_analysis_panel.html'):
    aes = get_object_or_404(AOI, id=aoi_id)
    return render_to_response(template, {'aes': aes} )
'''
   