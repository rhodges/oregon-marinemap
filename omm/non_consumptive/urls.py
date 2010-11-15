from django.conf.urls.defaults import *

urlpatterns = patterns('non_consumptive.views',
    url(r'^$', 'get_non_consumptive_master', name='non-consumptive-data-layers'),
    url(r'^layer/([\.A-Za-z0-9_-]+)/$', 'get_non_consumptive_layer'),
    
)
