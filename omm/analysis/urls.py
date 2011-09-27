from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    #user requested nsh analysis
    url(r'nsh/(\d+)/(\w+)', nsh_analysis, name='nsh_analysis'),
    url(r'aes/(\d+)/(\w+)', aes_analysis, name='aes_analysis'),
    url(r'econ/shoreside/(\d+)/([-\w]+)', shoreside_analysis, name='shoreside_analysis'),
    #user requested printable reports
    url(r'nsh/print_report/(\d+)/(\w+)', print_nsh_report, name='printable_nsh_report'),
    url(r'aes/print_report/(\d+)/(\w+)', print_aes_report, name='printable_aes_report'),
    url(r'econ/print_report/(\d+)/([-\w]+)', print_econ_report, name='printable_econ_report'),
    #user requested pdf reports
    url(r'nsh/pdf_report/(\d+)/(\w+)', pdf_nsh_report, name='pdf_nsh_report'),
    url(r'aes/pdf_report/(\d+)/(\w+)', pdf_aes_report, name='pdf_aes_report'),
    url(r'econ/pdf_report/(\d+)/([-\w]+)', pdf_econ_report, name='pdf_econ_report'),
    #user requested excel reports
    url(r'nsh/excel_report/(\d+)/(\w+)', excel_nsh_report, name='excel_nsh_report'),
    url(r'aes/excel_report/(\d+)/(\w+)', excel_aes_report, name='excel_aes_report'),
    url(r'econ/excel_report/(\d+)/([-\w]+)', excel_econ_report, name='excel_econ_report'),
    #admin request cache events
    url(r'admin_clear_cache/nsh/(\w+)/', admin_clear_nsh_cache),
    url(r'admin_clear_cache/aes/(\w+)/', admin_clear_aes_cache),
    url(r'admin_clear_cache/econ/(\w+)/', admin_clear_econ_cache),
)  