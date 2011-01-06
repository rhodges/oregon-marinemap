import xlwt

major_heading_style = xlwt.easyxf('font: bold true, italic on; alignment: horizontal left;')
minor_heading_style = xlwt.easyxf('font: italic on; alignment: horizontal left;')
heading_column_style = xlwt.easyxf('font: bold true; alignment: horizontal center;')
heading_row_style = xlwt.easyxf('font: bold true; alignment: horizontal center, wrap true;')
data_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='#,##0.0')
perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0.00%')

def populate_geo_sheet(ws, context):
    geo_header(ws, context)
    geo_spatial_headers(ws)
    geo_spatial_data(ws, context)
    geo_setting_headers(ws, context)
    geo_setting_data(ws, context)
    
def geo_header(ws, context):
    ws.write(0, 0, "Nearshore Habitat Geography Report for %s" % context['nsh'].name, major_heading_style)
    
def geo_spatial_headers(ws, row=3):
    ws.write(row-1, 0, "General Spatial Characteristics", minor_heading_style)
    ws.write(row, 1, "Area", heading_column_style)
    ws.col(1).width = 35*256
    ws.write(row, 2, "Perimeter", heading_column_style)
    ws.col(2).width = 35*256
    ws.write(row, 3, "Intertidal", heading_column_style)
    ws.col(3).width = 35*256
    ws.write(row, 4, "Islands", heading_column_style)
    ws.col(4).width = 35*256
    ws.write(row, 5, "Percent of Territorial Sea", heading_column_style)
    ws.col(5).width = 35*256
    
def geo_spatial_data(ws, context, row=4):
    ws.write(row, 1, str('%.1f %s') % (context['area'], context['area_units']), data_style)
    ws.write(row, 2, str('%.1f %s') % (context['perimeter'], context['length_units']), data_style)
    ws.write(row, 3, context['intertidal'], data_style)
    ws.write(row, 4, context['islands'], data_style)
    ws.write(row, 5, context['ratio']/100, perc_style)
        
def geo_setting_headers(ws, context, row=7):
    ws.write(row-1, 0, "Geographic Setting", minor_heading_style)
    if len(context['county']) > 1:
        ws.write(row, 1, "Adjacent Counties", heading_column_style)
        ws.write(row, 2, "County Shoreline Percentages", heading_column_style)
    else:
        ws.write(row, 1, "Adjacent County", heading_column_style)
        ws.write(row, 2, "County Shoreline Percentage", heading_column_style)
    ws.write(row, 3, "Nearest Ports", heading_column_style)
    ws.write(row, 4, "Nearest Incorporated Cities", heading_column_style)
    
def geo_setting_data(ws, context, row=8):
    offset = 0
    for county in context['county']:
        ws.write(row+offset, 1, county, data_style)
        offset += 1
    offset = 0
    for perc in context['county_shoreline_percentages']:
        ws.write(row+offset, 2, perc/100, perc_style)
        offset += 1
    offset = 0
    for port in context['ports']:
        ws.write(row+offset, 3, str(port[0]) + ' (%.1f %s)' % (port[1], context['length_units']), data_style)
        offset += 1
    offset = 0
    for city in context['cities']:
        ws.write(row+offset, 4, str(city[0]) + ' (%.1f %s)' % (city[1], context['length_units']), data_style)
        offset += 1
    