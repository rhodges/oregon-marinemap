import xlwt
from analysis.excel.utils import major_heading_style, minor_heading_style, heading_column_style, data_style, integer_data_style


def populate_hum_sheet(ws, context):
    hum_header(ws, context)
    hum_community_headers(ws)
    hum_community_data(ws, context)
    hum_planning_data(ws, context)
    hum_planning_headers(ws)
    hum_transportation_data(ws, context)
    hum_transportation_headers(ws)
    hum_infrastructure_data(ws, context)
    hum_infrastructure_headers(ws)
    hum_fishery_data(ws, context)
    hum_fishery_headers(ws)
    
def hum_header(ws, context):
    ws.write(0, 0, "Energy Site Human Report for %s" % context['aes'].name, major_heading_style)
    
def hum_community_headers(ws, row=3):
    ws.write(row-1, 0, "Community Considerations", minor_heading_style)
    ws.write(row, 1, "Nearest Urban Growth Boundaries", heading_column_style)
    ws.col(1).width = 45*256
    ws.write(row, 2, "Nearest State Parks", heading_column_style)
    ws.col(2).width = 45*256
    ws.write(row, 3, "Nearest Public Access Sites", heading_column_style)
    ws.col(3).width = 60*256
    ws.write(row, 4, "Visible From Shore", heading_column_style)
    ws.col(4).width = 45*256
        
def hum_community_data(ws, context, row=4):
    #urban growth boundaries
    offset = 0
    for ugb in context['urbangrowthboundaries']:
        ws.write(row+offset, 1, str('%s (%.1f %s)') % (ugb[0], ugb[1], context['length_units']), data_style)
        offset += 1
    #state parks
    offset = 0
    for park in context['parks']:
        ws.write(row+offset, 2, str('%s State Park (%.1f %s)') % (park[0], park[1], context['length_units']), data_style)
        offset += 1
    #public access sites
    offset = 0
    for site in context['access_sites']:
        ws.write(row+offset, 3, str('%s (%.1f %s)') % (site[0], site[1], context['length_units']), data_style)
        offset += 1
    ws.write(row, 4, context['visible'], data_style)
    
def hum_planning_data(ws, context, row=10):
    global planning_offset
    #rockyshores
    offset = 0
    for rockyshore in context['rockyshores']:
        ws.write(row+offset, 1, str('%s (%.1f %s)') % (rockyshore[0], rockyshore[1], context['length_units']), data_style)
        offset += 1
    #protected areas
    offset = 0
    for area in context['intersecting_protected_areas']:
        ws.write(row+offset, 2, area, data_style)
        offset += 1
    planning_offset = offset+2  
    ws.write(row+planning_offset, 2, str('%s (%.2f %s)') % (context['nearest_protected_area'][0], context['nearest_protected_area'][1], context['length_units']), data_style)
    #marine managed areas
    offset = 0
    for mma in context['intersecting_mmas']:
        ws.write(row+offset, 3, mma, data_style)
        offset += 1
    if offset+2 > planning_offset: planning_offset = offset+2  
    offset = 0
    for mma in context['nearest_mmas']:
        ws.write(row+planning_offset+offset, 3, str('%s (%.1f %s)') % (mma[0], mma[1], context['length_units']), data_style)
        offset += 1
    #wave energy sites
    offset = 0
    for site in context['intersecting_wave_energy_sites']:
        ws.write(row+offset, 4, site, data_style)
        offset += 1
    if offset+2 > planning_offset: planning_offset = offset+2  
    ws.write(row+planning_offset, 4, str('%s (%.2f %s)') % (context['nearest_wave_energy_site'][0], context['nearest_wave_energy_site'][1], context['length_units']), data_style)
        
def hum_planning_headers(ws, row=9):
    ws.write(row-1, 0, "Planning Considerations", minor_heading_style)
    ws.write(row, 1, "Nearest Rocky Shore Areas", heading_column_style)
    ws.write(row, 2, "Protected Areas", heading_column_style)
    ws.write(row+planning_offset, 2, "Nearest (non-intersecting) Protected Area", heading_column_style)
    ws.write(row, 3, "Marine Managed Areas", heading_column_style)
    ws.write(row+planning_offset, 3, "Nearest (non-intersecting) MMAs", heading_column_style)
    ws.write(row, 4, "Wave Energy Sites", heading_column_style)
    ws.write(row+planning_offset, 4, "Nearest (non-intersecting) Wave Energy Site", heading_column_style)

def hum_transportation_data(ws, context, row=15):
    row += planning_offset
    global transportation_offset
    #buoys
    offset = 0
    for data in context['intersecting_buoys']:
        ws.write(row+offset, 1, data, data_style)
        offset += 1
    transportation_offset = offset+2 
    ws.write(row+transportation_offset, 1, str('%s (%.2f %s)') % (context['nearest_buoy'][0], context['nearest_buoy'][1], context['length_units']), data_style)
    #beacons
    offset = 0
    for data in context['intersecting_beacons']:
        ws.write(row+offset, 2, data, data_style)
        offset += 1
    if offset+2 > transportation_offset: transportation_offset = offset+2  
    ws.write(row+transportation_offset, 2, str('%s (%.2f %s)') % (context['nearest_beacon'][0], context['nearest_beacon'][1], context['length_units']), data_style)
    #signals
    ws.write(row, 3, context['signal_data'], data_style)
    ws.write(row+transportation_offset, 3, context['num_signals'], integer_data_style)
    #towlanes
    ws.write(row, 4, context['towlanes'], data_style)
    #airports
    offset = 0
    for data in context['intersecting_airports']:
        ws.write(row+offset, 5, data, data_style)
        offset += 1
    if offset+2 > transportation_offset: transportation_offset = offset+2  
    ws.write(row+transportation_offset, 5, str('%s (%.2f %s)') % (context['nearest_airport'][0], context['nearest_airport'][1], context['length_units']), data_style)
    
def hum_transportation_headers(ws, row=14):
    row += planning_offset
    ws.write(row-1, 0, "Transportation Considerations", minor_heading_style)
    ws.write(row, 1, "Buoys", heading_column_style)
    ws.write(row+transportation_offset, 1, "Nearest (non-intersecting) Buoy", heading_column_style)
    ws.write(row, 2, "Beacons", heading_column_style)
    ws.write(row+transportation_offset, 2, "Nearest (non-intersecting) Beacon", heading_column_style)
    ws.write(row, 3, "Signal Equipment", heading_column_style)
    ws.write(row+transportation_offset, 3, "Signal Equipment Count", heading_column_style)
    ws.write(row, 4, "Tugboat Towlanes", heading_column_style)
    ws.write(row, 5, "Airports", heading_column_style)
    ws.write(row+transportation_offset, 5, "Nearest (non-intersecting) Airport", heading_column_style)
    ws.col(5).width = 45*256
    
def hum_infrastructure_data(ws, context, row=19):
    row += planning_offset + transportation_offset
    global infrastructure_offset
    #dredge materials disposal sites
    offset = 0
    for data in context['intersecting_dmds']:
        ws.write(row+offset, 1, data, data_style)
        offset += 1
    infrastructure_offset = offset+2 
    ws.write(row+infrastructure_offset, 1, str('%s (%.2f %s)') % (context['nearest_dmd'][0], context['nearest_dmd'][1], context['length_units']), data_style)
    #npdes outfalls
    offset = 0
    for data in context['intersecting_outfalls']:
        ws.write(row+offset, 2, data, data_style)
        offset += 1
    if offset+2 > infrastructure_offset: infrastructure_offset = offset+2  
    ws.write(row+infrastructure_offset, 2, str('%s (%.2f %s)') % (context['nearest_outfall'][0], context['nearest_outfall'][1], context['length_units']), data_style)
    #cable routes
    offset = 0
    for data in context['intersecting_cables']:
        ws.write(row+offset, 3, data, data_style)
        offset += 1
    if offset+2 > infrastructure_offset: infrastructure_offset = offset+2  
    ws.write(row+infrastructure_offset, 3, str('%s (%.2f %s)') % (context['nearest_cable'][0], context['nearest_cable'][1], context['length_units']), data_style)
    #transmission lines
    ws.write(row, 4, str('%.1f %s') % (context['transmissionline1993'], context['length_units']), data_style)
    ws.write(row+infrastructure_offset, 4, str('%.1f %s') % (context['transmissionline2010'], context['length_units']), data_style)
    #electrical substations
    offset = 0
    for data in context['substations']:
        ws.write(row+offset, 5, str('%s (%.2f %s)') % (data[0], data[1], context['length_units']), data_style)
        offset += 1
    #railroad
    ws.write(row, 6, str('%.2f %s') % (context['railroad'], context['length_units']), data_style)
        
def hum_infrastructure_headers(ws, row=18):
    row += planning_offset + transportation_offset
    ws.write(row-1, 0, "Infrastructure Considerations", minor_heading_style)
    ws.write(row, 1, "Dredge Materials Disposal Sites", heading_column_style)
    ws.write(row+infrastructure_offset, 1, "Nearest (non-intersecting) DMD Site", heading_column_style)
    ws.write(row, 2, "NPDES Outfall Sites", heading_column_style)
    ws.write(row+infrastructure_offset, 2, "Nearest (non-intersecting) Outfall Site", heading_column_style)
    ws.write(row, 3, "Undersea Cable Routes", heading_column_style)
    ws.write(row+infrastructure_offset, 3, "Nearest (non-intersecting) Cable Route", heading_column_style)
    ws.write(row, 4, "Nearest Transmission Line (1993)", heading_column_style)
    ws.write(row+infrastructure_offset, 4, "Nearest Transmission Line (2010)", heading_column_style)
    ws.write(row, 5, "Nearest Electrical Substations", heading_column_style)
    ws.write(row, 6, "Distance to Nearest Railroad", heading_column_style)
    ws.col(6).width = 45*256
    

def hum_fishery_data(ws, context, row=23):
    row += planning_offset + transportation_offset + infrastructure_offset
    global fishery_offset
    #ports
    offset = 0
    for data in context['nearest_ports']:
        ws.write(row+offset, 1, str('%s (%.2f %s)') % (data[0], data[1], context['length_units']), data_style)
        offset += 1
    #marinas
    offset = 0
    for data in context['nearest_marinas']:
        ws.write(row+offset, 2, str('%s (%.2f %s)') % (data[0], data[1], context['length_units']), data_style)
        offset += 1
    #odfw closures
    offset = 0
    for data in context['intersecting_closures']:
        ws.write(row+offset, 3, data, data_style)
        offset += 1
    fishery_offset = offset+2 
    ws.write(row+fishery_offset, 3, str('%s (%.2f %s)') % (context['nearest_closure'][0], context['nearest_closure'][1], context['length_units']), data_style)
    #conservation areas
    offset = 0
    for data in context['intersecting_conservation_areas']:
        ws.write(row+offset, 4, data, data_style)
        offset += 1
    if offset+2 > fishery_offset: fishery_offset = offset+2  
    ws.write(row+fishery_offset, 4, str('%s (%.2f %s)') % (context['nearest_conservation_area'][0], context['nearest_conservation_area'][1], context['length_units']), data_style)
    
def hum_fishery_headers(ws, row=22):
    row += planning_offset + transportation_offset + infrastructure_offset
    ws.write(row-1, 0, "Fishery Considerations", minor_heading_style)
    ws.write(row, 1, "Proximity to Ports", heading_column_style)
    ws.write(row, 2, "Nearest Marinas", heading_column_style)
    ws.write(row, 3, "ODFW Closures", heading_column_style)
    ws.write(row+fishery_offset, 3, "Nearest (non-intersecting) ODFW Closure", heading_column_style)
    ws.write(row, 4, "EFH Conservation Areas", heading_column_style)
    ws.write(row+fishery_offset, 4, "Nearest (non-intersecting) Conservation Areas", heading_column_style)
    