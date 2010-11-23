from django.conf.urls.defaults import *
from lingcod.common.utils import get_mpa_form, get_array_form
from views import *

#the following url pattern was acquired from lingcod.mpa.urls

AOIForm = get_mpa_form()
ArrayForm = get_array_form()

urlpatterns = patterns('lingcod.rest.views',
    url(r'^form/aoi/$', 'form_resources', {'form_class': AOIForm, 'create_title': 'Create a New Area of Inquiry'}, name='aoi_create_form'),
    url(r'^form/array/$', 'form_resources', {'form_class': ArrayForm, 'create_title': 'Create a New AOI Group'}, name='array_create_form'),
    url(r'shapefile/mpa/(?P<mpa_id_list_str>(\d+,?)+)/$', aoi_shapefile, name='mpa_shapefile'),
)