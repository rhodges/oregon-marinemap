from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #user requested nsh analysis
    url(r'nsh/(\d+)/(\w+)', nsh_analysis, name='nsh_analysis'),
    url(r'aes/(\d+)/(\w+)', aes_analysis, name='aes_analysis'),
    #user requested printable reports
    url(r'nsh/print_report/(\d+)/(\w+)', print_nsh_report, name='printable_nsh_report'),
    url(r'nsh/pdf_report/(\d+)/(\w+)', pdf_nsh_report, name='pdf_nsh_report'),
    #admin request cache events
    url(r'admin_clear_cache/nsh/(\w+)/', admin_clear_nsh_cache),
)  