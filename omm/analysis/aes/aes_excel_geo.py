import xlwt
from analysis.excel.utils import major_heading_style, minor_heading_style, heading_column_style, data_style, perc_style
from analysis.excel.geography import geo_spatial_headers, geo_spatial_data

def populate_geo_sheet(ws, context):
    geo_header(ws, context)
    geo_spatial_headers(ws)
    geo_spatial_data(ws, context)
    geo_setting_headers(ws, context)
    geo_setting_data(ws, context)
    
def geo_header(ws, context):
    ws.write(0, 0, "Energy Site Geography Report for %s" % context['aes'].name, major_heading_style)
    
def geo_setting_headers(ws, context, row=7):
    ws.write(row-1, 0, "Geographic Setting", minor_heading_style)
    if len(context['county']) > 1:
        ws.write(row, 1, "Adjacent Counties", heading_column_style)
    else:
        ws.write(row, 1, "Adjacent County", heading_column_style)
    ws.write(row, 2, 'Nearest Cities', heading_column_style)
    ws.write(row, 3, "Nearest Ports", heading_column_style)
    ws.write(row, 4, "Nearest Marinas", heading_column_style)
    
def geo_setting_data(ws, context, row=8):
    offset = 0
    for county in context['county']:
        ws.write(row+offset, 1, county, data_style)
        offset += 1
    offset = 0
    for city in context['cities']:
        ws.write(row+offset, 2, str(city[0]) + ' (%.1f %s)' % (city[1], context['length_units']), data_style)
        offset += 1
    offset = 0
    for port in context['ports']:
        ws.write(row+offset, 3, str(port[0]) + ' (%.1f %s)' % (port[1], context['length_units']), data_style)
        offset += 1
    offset = 0
    for marina in context['marinas']:
        ws.write(row+offset, 4, str(marina[0]) + ' (%.1f %s)' % (marina[1], context['length_units']), data_style)
        offset += 1
    