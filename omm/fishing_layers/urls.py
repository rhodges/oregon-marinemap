from django.conf.urls.defaults import *

urlpatterns = patterns('fishing_layers.views',
    url(r'^public/$', 'get_public_fishing_layers', name='public-fishing-data-layers'),
    url(r'^public/tiles/map/([A-Za-z]+)/$', 'get_public_map'),
    url(r'^public/tiles/contour/([A-Za-z]+)/$', 'get_public_contour'),
    url(r'^public/other/([A-Za-z]+)/([A-Za-z0-9_,-\.]+)/$', 'get_public_other'),
    #note on the following 2 url patterns:
    #providing for an optional trailing slash ('/') to prevent GE big red X's generated from missed url attempts (301's)
    url(r'^public/tiles/map/([A-Za-z]+)/([0-9]+)/([0-9]+)/([0-9]+)\.([A-Za-z]+)/?$', 'get_public_map'),
    url(r'^public/tiles/contour/([A-Za-z]+)/([0-9]+)/([0-9]+)/([0-9]+)\.([A-Za-z]+)/?$', 'get_public_contour'),    
)
