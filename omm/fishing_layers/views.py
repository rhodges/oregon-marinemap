from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from models import *
from lingcod.common.utils import load_session
from lingcod.common import default_mimetypes as mimetypes
from django.conf import settings
import os

 
def get_public_fishing_layers(request):
    """Returns uploaded kml from the :class:`PublicFishingLayer <fishing_layers.models.PublicFishingLayer>` object marked ``active``.
    """
    layer = get_object_or_404(PublicFishingLayer, active=True)
    return HttpResponse(layer.kml.read(), mimetype=mimetypes.KML)
    
def get_public_map(request, layer_name, z=None, x=None, y=None, ext=None, root=settings.GIS_DATA_ROOT):
    root_path = os.path.join(root, 'public_maps', layer_name)
    return get_map(root_path, z, x, y, ext)
    
def get_map(root_path, z, x, y, ext):    
    if z is None:
        doc_file = os.path.join(root_path, 'doc.kml')
        doc_kml = open(doc_file).read()
        return HttpResponse(doc_kml, mimetype=mimetypes.KML)  
    elif ext == 'kml':
        kml_file = os.path.join(root_path, z, x, y+'.kml')
        tile_kml = open(kml_file).read()
        return HttpResponse(tile_kml, mimetype=mimetypes.KML)
    elif ext == 'kmz':
        kmz_file = os.path.join(root_path, z, x, y+'.kmz')
        tile_kmz = open(kmz_file).read()
        return HttpResponse(tile_kmz, mimetype=mimetypes.KMZ)
    elif ext == 'png':
        png_file = os.path.join(root_path, z, x, y+'.png')
        tile_png = open(png_file, "rb").read()
        return HttpResponse(tile_png, mimetype='image/png')
    elif ext == 'jpg':
        png_file = os.path.join(root_path, z, x, y+'.jpg')
        tile_png = open(png_file, "rb").read()
        return HttpResponse(tile_png, mimetype='image/jpg')
    else:
        return HttpResponse("Unrecognized extension in request object: " + ext, status=501)
   
def get_public_contour(request, layer_name, z=None, x=None, y=None, ext=None, root=settings.GIS_DATA_ROOT):
    root_path = os.path.join(root, 'public_contours', layer_name)
    return get_contour(root_path, z, x, y, ext)
    
def get_contour(root_path, z, x, y, ext):    
    '''
    load_session(request, session_key)
    user = request.user
    if user.is_anonymous() or not user.is_authenticated():
        return HttpResponse('You must be logged in', status=401)
    elif input_username and user.username != input_username:
        return HttpResponse('Access denied', status=401)
    '''    
    if z is None:
        doc_file = os.path.join(root_path, 'doc.kml')
        doc_kml = open(doc_file).read()
        return HttpResponse(doc_kml, mimetype=mimetypes.KML)
    z = int(z)
    x = int(x)
    y = int(y)
    dims = (  "%02d" % z,
                "%03d" % int(x / 1000000),
                "%03d" % (int(x / 1000) % 1000),
                "%03d" % (int(x) % 1000),
                "%03d" % int(y / 1000000),
                "%03d" % (int(y / 1000) % 1000),
                "%03d.%s" % (int(y) % 1000, ext)
            )
            
    file_path = os.path.join(root_path, dims[0], dims[1], dims[2], dims[3], dims[4], dims[5], dims[6]) 
    if ext == 'kml':
        tile = open(file_path).read()
        return HttpResponse(tile, mimetype=mimetypes.KML)
    else:
        tile = open(file_path, "rb").read()
        return HttpResponse(tile, mimetype='image/png')

        
def get_public_other(request, folder, file, ext, root=settings.GIS_DATA_ROOT):
    #legend is stored in GIS_DATA_ROOT/images
    file_name = file + '.' + ext
    doc_path = os.path.join(root, folder, file_name)
    if folder == 'images':
        if ext.lower() == 'png':
            mimetype = 'image/png'
        elif ext.lower() == 'jpg':
            mimetype = 'image/png'
        else:
            return HttpResponse("Unrecognized extension in request object: " + ext, status=501)
        contents = open(doc_path, "rb").read()
        return HttpResponse(contents, mimetype=mimetype)
    else:
        return HttpResponse(folder + ' not implemented', status=501)
 
