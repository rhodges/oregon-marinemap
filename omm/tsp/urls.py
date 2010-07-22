from django.conf.urls.defaults import *
from lingcod.common.utils import get_mpa_form

#the following url pattern was acquired from lingcod.mpa.urls

AOIForm = get_mpa_form()

urlpatterns = patterns('lingcod.rest.views',
    url(r'^form/$', 'form_resources', {'form_class': AOIForm, 'create_title': 'Create a New Area of Inquiry'}, name='aoi_create_form'),
)