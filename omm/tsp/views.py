from lingcod.common import utils
from lingcod.sharing.utils import get_viewable_object_or_respond
from lingcod.shapes.views import ShpResponder
from django.template.defaultfilters import slugify

def aoi_shapefile(request, mpa_id_list_str):
    aoi_class = utils.get_mpa_class()
    aoi_id_list = mpa_id_list_str.split(',')
    aoi_id = aoi_id_list[0] # only expecting one for now
    aoi = get_viewable_object_or_respond(aoi_class, aoi_id, request.user)
    shp_response = ShpResponder(aoi.export_query_set)
    shp_response.file_name = slugify(aoi.name[0:8])
    return shp_response()