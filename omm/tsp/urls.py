from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'shapefile/aoi/(?P<mpa_id_list_str>(\d+,?)+)/$', aoi_shapefile, name='aoi_shapefile'),
    url(r'shapefile/array/(?P<array_id_list_str>(\d+,?)+)/$', array_shapefile,name='array_shapefile'),
)
