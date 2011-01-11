import xlwt
from analysis.excel.utils import major_heading_style
from analysis.excel.biology import bio_terrestrial_headers, bio_terrestrial_data, bio_intertidal_headers, bio_intertidal_data, bio_subtidal_headers, bio_subtidal_data

def populate_bio_sheet(ws, context):
    bio_header(ws, context)
    bio_terrestrial_headers(ws)
    bio_terrestrial_data(ws, context)
    bio_intertidal_headers(ws)
    bio_intertidal_data(ws, context)
    bio_subtidal_headers(ws, context)
    bio_subtidal_data(ws, context)
    
def bio_header(ws, context):
    ws.write(0, 0, "Energy Site Biology Report for %s" % context['aes'].name, major_heading_style)
    