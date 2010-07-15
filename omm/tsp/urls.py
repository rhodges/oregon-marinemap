from django.conf.urls.defaults import *
from lingcod.common.utils import get_mpa_form

#the following url pattern was acquired from lingcod.mpa.urls

HabitatForm = get_mpa_form()

urlpatterns = patterns('lingcod.rest.views',
    url(r'^form/$', 'form_resources', {'form_class': HabitatForm, 'create_title': 'Create a New Nearshore Habitat'}, name='nsh_create_form'),
)