from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #user requested nsh analysis
    url(r'nsh/(\d+)/(\w+)', nsh_analysis, name='nsh_analysis'),
    url(r'aes/(\d+)/(\w+)', aes_analysis, name='aes_analysis'),
    #user requested printable reports
    url(r'nsh/print_report/(\d+)/(\w+)', print_report, name='printable_geo_report'),
    url(r'nsh/print_report/(\d+)/(\w+)', print_report, name='printable_phy_report'),
    url(r'nsh/print_report/(\d+)/(\w+)', print_report, name='printable_bio_report'),
    url(r'nsh/print_report/(\d+)/(\w+)', print_report, name='printable_hum_report'),
    url(r'nsh/print_report/(\d+)/(\w+)', print_report, name='printable_comprehensive_report'),
    #admin request cache events
    url(r'adminClearNShCache', adminClearCache),
)  