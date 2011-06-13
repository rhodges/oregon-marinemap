from lingcod.common import utils
from lingcod.shapes.views import ShpResponder
from lingcod.features.views import get_object_for_viewing
from django.http import HttpResponse
from django.template.defaultfilters import slugify

def omm_shapefile(request, instances):
    from tsp.models import AOI, AOIArray, AOIShapefile
    aois = []
    for inst in instances:
        viewable, response = inst.is_viewable(request.user)
        if not viewable:
            return response

        if isinstance(inst, AOI):
            inst.convert_to_shp()
            aois.append(inst)
        elif isinstance(inst, AOIArray):
            for aoi in inst.feature_set(recurse=True,feature_classes=[AOI]):
                aoi.convert_to_shp()
                aois.append(aoi)
        else:
            pass # ignore anything else

    filename = '_'.join([slugify(inst.name) for inst in instances])
    pks = [aoi.pk for aoi in aois]
    qs = AOIShapefile.objects.filter(aoi_id_num__in=pks)
    if len(qs) == 0:
        return HttpResponse(
            "Nothing in the query set; you don't want an empty shapefile", 
            status=404
        )
    shp_response = ShpResponder(qs)
    shp_response.file_name = slugify(filename[0:8])
    return shp_response()
