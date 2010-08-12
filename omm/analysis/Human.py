from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tsp.models import AOI
from models import *
from settings import *
from lingcod.unit_converter.models import length_in_display_units, area_in_display_units

default_value = '---'

'''
Runs analysis for Human Considerations report
Renders the Human Considerations Report template
Called by NSH_Analysis.display_nsh_analysis
'''
def display_hum_analysis(request, nsh_id, template='Hum_Report.html'):
    nsh = get_object_or_404(AOI, pk=nsh_id)
    
    
    context = {'aoi': nsh, 'default_value': default_value, 'area_units': settings.DISPLAY_AREA_UNITS}
    return render_to_response(template, RequestContext(request, context)) 
     