from django.conf.urls.defaults import *

urlpatterns = patterns('fishing_layers.views',
    url(r'^public/$', 'get_fishing_layers', name='public-fishing-data-layers'),
    url(r'^public/tiles/map/([A-Za-z]+)/$', 'get_map'),
    url(r'^(\w+)/(\w+)/ecotrust/tiles/contour/([A-Za-z]+)/([A-Za-z0-9_,]+)/$', 'get_contour'),
    url(r'^(\w+)/(\w+)/ecotrust/other/([A-Za-z]+)/([A-Za-z0-9_,-\.]+)/$', 'get_other'),
    #note on the following 2 url patterns:
    #providing for an optional trailing slash ('/') to prevent GE big red X's generated from missed url attempts (301's)
    url(r'^(\w+)/(\w+)/ecotrust/tiles/map/([A-Za-z]+)/([A-Za-z0-9_,]+)/([0-9]+)/([0-9]+)/([0-9]+)\.([A-Za-z]+)/?$', 'get_map'),
    url(r'^(\w+)/(\w+)/ecotrust/tiles/contour/([A-Za-z]+)/([A-Za-z0-9_,]+)/([0-9]+)/([0-9]+)/([0-9]+)\.([A-Za-z]+)/?$', 'get_contour'),    
)
