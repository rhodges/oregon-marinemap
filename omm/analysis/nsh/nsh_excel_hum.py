import xlwt

major_heading_style = xlwt.easyxf('font: bold true, italic on; alignment: horizontal left;')
minor_heading_style = xlwt.easyxf('font: italic on; alignment: horizontal left;')
heading_column_style = xlwt.easyxf('font: bold true; alignment: horizontal center, wrap on;')
integer_data_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='#,##0')
data_style = xlwt.easyxf('alignment: horizontal center, wrap on;',num_format_str='#,##0.0')
integer_perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0%')
perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0.0%')

def populate_hum_sheet(ws, context):
    hum_header(ws, context)
    hum_recreational_headers(ws)
    hum_recreational_data(ws, context)
    #for infrastructure, data will determine header location
    hum_infrastructure_data(ws, context)
    hum_infrastructure_headers(ws)
    #for fishery, data will determine header location
    hum_fishery_data(ws, context)
    hum_fishery_headers(ws)
    
def hum_header(ws, context):
    ws.write(0, 0, "Nearshore Habitat Human Report for %s" % context['nsh'].name, major_heading_style)
    
def hum_recreational_headers(ws, row=3):
    ws.write(row-1, 0, "Community & Recreational Considerations", minor_heading_style)
    ws.write(row, 1, "Nearest State Parks", heading_column_style)
    ws.col(1).width = 45*256
    ws.write(row, 2, "Nearest Public Access Sites", heading_column_style)
    ws.col(2).width = 60*256
    ws.write(row, 3, "Nearest Rocky Shore Areas", heading_column_style)
    ws.col(3).width = 45*256
    
def hum_recreational_data(ws, context, row=4):
    offset = 0
    for park in context['parks']:
        ws.write(row+offset, 1, str('%s State Park (%.1f %s)') % (park[0], park[1], context['length_units']), data_style)
        offset += 1
    offset = 0
    for site in context['access_sites']:
        ws.write(row+offset, 2, str('%s (%.1f %s)') % (site[0], site[1], context['length_units']), data_style)
        offset += 1
    offset = 0
    for rockyshore in context['rockyshores']:
        ws.write(row+offset, 3, str('%s (%.1f %s)') % (rockyshore[0], rockyshore [1], context['length_units']), data_style)
        offset += 1
        
def hum_infrastructure_data(ws, context, row=10):
    global infrastructure_offset
    infrastructure_offset = 2
    offset = 0
    for data in context['intersecting_dmds']:
        ws.write(row+offset, 1, data, data_style)
        offset += 1
    if offset+2 > infrastructure_offset: infrastructure_offset = offset+2  
    ws.write(row+infrastructure_offset, 1, str('%s (%.2f %s)') % (context['nearest_dmd'][0], context['nearest_dmd'][1], context['length_units']), data_style)
        
    offset = 0
    for data in context['intersecting_outfalls']:
        ws.write(row+offset, 2, data, data_style)
        offset += 1
    if offset+2 > infrastructure_offset: infrastructure_offset = offset+2  
    ws.write(row+infrastructure_offset, 2, str('%s (%.2f %s)') % (context['nearest_outfall'][0], context['nearest_outfall'][1], context['length_units']), data_style)
        
    offset = 0
    for data in context['intersecting_cables']:
        ws.write(row+offset, 3, data, data_style)
        offset += 1
    if offset+2 > infrastructure_offset: infrastructure_offset = offset+2  
    ws.write(row+infrastructure_offset, 3, str('%s (%.2f %s)') % (context['nearest_cable'][0], context['nearest_cable'][1], context['length_units']), data_style)
    
def hum_infrastructure_headers(ws, row=9):
    ws.write(row-1, 0, "Transportation & Infrastructure Considerations", minor_heading_style)
    ws.write(row, 1, "Dredge Materials Disposal Sites", heading_column_style)
    ws.write(row+infrastructure_offset, 1, "Nearest (non-intersecting) DMD Site", heading_column_style)
    ws.write(row, 2, "NPDES Outfall Sites", heading_column_style)
    ws.write(row+infrastructure_offset, 2, "Nearest (non-intersecting) Outfall Site", heading_column_style)
    ws.write(row, 3, "Undersea Cable Routes", heading_column_style)
    ws.write(row+infrastructure_offset, 3, "Nearest (non-intersecting) Cable Route", heading_column_style)
    
def hum_fishery_data(ws, context, row=14):
    row += infrastructure_offset
    offset = 0
    for port in context['nearest_ports']:
        ws.write(row+offset, 1, str('%s (%.1f %s)') % (port[0], port[1], context['length_units']), data_style)
        offset += 1
    offset = 0
    for marina in context['nearest_marinas']:
        ws.write(row+offset, 2, str('%s (%.1f %s)') % (marina[0], marina[1], context['length_units']), data_style)
        offset += 1
        
    global fishery_offset1
    fishery_offset1 = 5
    mma_offset = 0
    for data in context['intersecting_mmas']:
        ws.write(row+fishery_offset1+mma_offset, 1, data, data_style)
        mma_offset += 1
        
    odfw_offset = 0
    for data in context['intersecting_closures']:
        ws.write(row+fishery_offset1+odfw_offset, 2, data, data_style)
        odfw_offset += 1
        
    efh_offset = 0
    for data in context['intersecting_conservation_areas']:
        ws.write(row+fishery_offset1+efh_offset, 3, data, data_style)
        efh_offset += 1
        
    global fishery_offset2
    offset_list = [mma_offset, odfw_offset, efh_offset]
    offset_list.sort()
    largest_offset = offset_list[-1]
    fishery_offset2 = largest_offset + 2
    offset = 0
    for mma in context['nearest_mmas']:
        ws.write(row+fishery_offset1+fishery_offset2+offset, 1, str('%s (%.2f %s)') % (mma[0], mma[1], context['length_units']), data_style)
        offset += 1
    ws.write(row+fishery_offset1+fishery_offset2, 2, str('%s (%.2f %s)') % (context['nearest_closure'][0], context['nearest_closure'][1], context['length_units']), data_style)
    ws.write(row+fishery_offset1+fishery_offset2, 3, str('%s (%.2f %s)') % (context['nearest_conservation_area'][0], context['nearest_conservation_area'][1], context['length_units']), data_style)
    
        
def hum_fishery_headers(ws, row=13):
    row += infrastructure_offset
    ws.write(row-1, 0, "Fishery Considerations", minor_heading_style)
    ws.write(row, 1, "Proximity to Ports", heading_column_style)
    ws.write(row, 2, "Nearest Marinas", heading_column_style)
    row += fishery_offset1
    ws.write(row, 1, "Marine Managed Areas", heading_column_style)
    ws.write(row+fishery_offset2, 1, "Nearest (non-intersecting) MMAs", heading_column_style)
    ws.write(row, 2, "ODFW Closures", heading_column_style)
    ws.write(row+fishery_offset2, 2, "Nearest (non-intersecting) ODFW Closure", heading_column_style)
    ws.write(row, 3, "EFH Conservation Areas", heading_column_style)
    ws.write(row+fishery_offset2, 3, "Nearest (non-intersecting) Conservation Area", heading_column_style)
    
    
    