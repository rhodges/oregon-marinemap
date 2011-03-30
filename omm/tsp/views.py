from lingcod.common import utils
from lingcod.shapes.views import ShpResponder
from django.template.defaultfilters import slugify

def aoi_shapefile(request, mpa_id_list_str):
    aoi_class = utils.get_mpa_class()
    aoi_id_list = mpa_id_list_str.split(',')
    aoi_id = aoi_id_list[0] # only expecting one for now
    #MP TODO 
    aoi = get_viewable_object_or_respond(aoi_class, aoi_id, request.user)
    shp_response = ShpResponder(aoi.export_query_set)
    shp_response.file_name = slugify(aoi.name[0:8])
    return shp_response()
    
    
def array_shapefile(request, array_id_list_str):
    array_class = utils.get_array_class()
    array_id_list = array_id_list_str.split(',')
    #array_set = mlpa.MpaArray.objects.filter(pk__in=array_id_list_str.split(',') )
    array_id = array_id_list[0] # for now we're only expecting to get one
    #MP TODO 
    array = get_viewable_object_or_respond(array_class,array_id,request.user)
    #if array.short_name:
    #    file_name = array.short_name
    #else:
    file_name = array.name[0:8]
    
    shp_response = ShpResponder(array.export_query_set)
    shp_response.file_name = slugify(file_name)
    return shp_response()
