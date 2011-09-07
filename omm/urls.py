from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^tsp/', include('tsp.urls')),
    (r'^analysis/', include('analysis.urls')),
    (r'^fishing/', include('fishing_layers.urls')),
    (r'^loadshp/', include('lingcod.loadshp.urls')),
    #(r'^non_consumptive/', include('non_consumptive.urls')),
)

urlpatterns += patterns('',
    # Include all lingcod app urls. 
    (r'', include('lingcod.common.urls')),
)
