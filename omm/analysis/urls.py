from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #user requested nsh analysis
    url(r'nsh/(\d+)/(\w+)', nsh_analysis, name='nsh_analysis'),
    url(r'aes/(\d+)/(\w+)', aes_analysis, name='aes_analysis'),
    #user requested printable reports
    url(r'nsh/print_report/(\d+)/(\w+)', print_report, name='printable_report'),
    #admin request cache events
    url(r'adminClearNShCache/(\w+)/', adminClearCache),
)  