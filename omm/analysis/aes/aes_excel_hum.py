import xlwt
from analysis.excel.utils import major_heading_style, minor_heading_style, heading_column_style, data_style


def populate_hum_sheet(ws, context):
    hum_header(ws, context)
    
def hum_header(ws, context):
    ws.write(0, 0, "Energy Site Human Report for %s" % context['aes'].name, major_heading_style)
    