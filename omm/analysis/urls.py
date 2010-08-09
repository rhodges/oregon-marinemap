from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #user requested nsh analysis
    url(r'nsh/(\d+)/(\w+)', nsh_analysis, name='nsh_analysis'),
    #url(r'aes/panel/(\d+)/(\w+)', aes_analysis_panel, name='aes_analysis_panel'),
    url(r'aes/(\d+)/(\w+)', aes_analysis, name='aes_analysis'),
)  