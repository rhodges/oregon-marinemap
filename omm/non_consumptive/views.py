from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from models import *
from lingcod.common.utils import load_session
from lingcod.common import default_mimetypes as mimetypes
from django.conf import settings
import os

 
def get_non_consumptive_master(request):
    """Returns uploaded kml from the :class:`NonConsumptive <non_consumptive.models.PublicFishingLayer>` object marked ``active``.
    """
    layer = get_object_or_404(NonConsumptive, active=True)
    return HttpResponse(layer.kml.read(), mimetype=mimetypes.KML)
    
def get_non_consumptive_layer(request, layer_name, root=settings.GIS_DATA_ROOT):
    file_path = os.path.join(root, 'non_consumptive', layer_name)
    kml = open(file_path).read()
    return HttpResponse(kml, mimetype=mimetypes.KML)
        
    