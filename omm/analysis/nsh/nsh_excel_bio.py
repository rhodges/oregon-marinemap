import xlwt

major_heading_style = xlwt.easyxf('font: bold true, italic on; alignment: horizontal left;')
minor_heading_style = xlwt.easyxf('font: italic on; alignment: horizontal left;')
heading_column_style = xlwt.easyxf('font: bold true; alignment: horizontal center, wrap on;')
integer_data_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='#,##0')
data_style = xlwt.easyxf('alignment: horizontal center, wrap on;',num_format_str='#,##0.0')
integer_perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0%')
perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0.0%')

def populate_bio_sheet(ws, context):
    bio_header(ws, context)
    bio_terrestrial_headers(ws)
    bio_terrestrial_data(ws, context)
    bio_intertidal_headers(ws)
    bio_intertidal_data(ws, context)
    bio_subtidal_headers(ws, context)
    bio_subtidal_data(ws, context)
    
def bio_header(ws, context):
    ws.write(0, 0, "Nearshore Habitat Biology Report for %s" % context['nsh'].name, major_heading_style)
    
def bio_terrestrial_headers(ws, row=3):
    ws.write(row-1, 0, "Terrestrial Biological Characteristics", minor_heading_style)
    ws.write(row, 1, "Nearest Western Snowy Plover Critical Habitat", heading_column_style)
    ws.col(1).width = 60*256
    ws.write(row, 2, "Nearest Marbled Murrelet Critical Habitat", heading_column_style)
    ws.col(2).width = 60*256
    
def bio_terrestrial_data(ws, context, row=4):
    ws.write(row, 1, str('%.1f %s') % (context['nearest_snowy_plover'], context['length_units']), data_style)
    ws.write(row, 2, str('%.1f %s') % (context['nearest_marbled_murrelet'], context['length_units']), data_style)
        
def bio_intertidal_headers(ws, row=7):
    ws.write(row-1, 0, "Intertidal Biological Characteristics", minor_heading_style)
    ws.write(row, 1, "Pinniped Haulouts", heading_column_style)
    ws.write(row+3, 1, "Pinniped Haulout Details", heading_column_style)
    ws.write(row, 2, "Steller Sea Lion Rookeries", heading_column_style)
    ws.write(row+3, 2, "Steller Sea Lion Critical Habitats", heading_column_style)
    ws.write(row, 3, "Bird Colonies", heading_column_style)
    ws.write(row+3, 3, "Bird Colony Details", heading_column_style)
    ws.col(3).width = 45*256
    
def bio_intertidal_data(ws, context, row=8):
    ws.write(row, 1, str('%s haulouts') %context['num_haulouts'], integer_data_style)
    global subtidal_offset
    subtidal_offset = 0
    offset = 3
    if len(context['haulout_sites']) == 0:
        ws.write(row+offset, 1, '---', data_style)
        offset += 1
    for site in context['haulout_sites']:
        ws.write(row+offset, 1, str('%s, (%s)') %(site[0][0], site[0][1]), data_style)
        offset += 1
        for species in site[1]:
            ws.write(row+offset, 1, species, data_style)
            offset += 1
        offset += 1
    subtidal_offset = offset
    offset = 3
    ws.write(row, 2, str('%s rookeries') %context['num_rookeries'], integer_data_style)
    if len(context['sealion_habs']) == 0:
        ws.write(row+offset, 2, '---', data_style)
        offset += 1
    for hab in context['sealion_habs']:
        ws.write(row+offset, 2, str('%s        %s') %( hab[0],  hab[1]), data_style)
        offset += 1
    if offset > subtidal_offset: subtidal_offset = offset    
    offset = 3
    ws.write(row, 3, str('%s colonies') %context['bird_colonies'], integer_data_style)
    if len(context['bird_details']) == 0:
        ws.write(row+offset, 3, '---', data_style)
        offset += 1
    for details in context['bird_details']:
        ws.write(row+offset, 3, str('%s, Colony #%s') %(details[0][0], details[0][1]), data_style)
        offset += 1
        for bird in details[1]:
            ws.write(row+offset, 3, bird, data_style)
            offset += 1
        offset += 1
    if offset > subtidal_offset: subtidal_offset = offset 
    
def bio_subtidal_headers(ws, context, row=10):
    row += subtidal_offset
    ws.write(row-1, 0, "Subtidal Biological Characteristics", minor_heading_style)
    ws.write(row, 1, "Habitat Types & Proportions", heading_column_style)
    ws.write(row, 2, "Predicted Fish Species\n(Provided by NOAA's Northwest Fisheries Science Center)", heading_column_style)
    ws.write(row, 3, "Green Sturgeon", heading_column_style)
    ws.write(row+3, 3, "Green Sturgeon Area Percentage", heading_column_style)
    ws.write(row, 4, "Nearest Coho Populated Stream", heading_column_style)
    ws.col(4).width = 45*256
    ws.write(row, 5, "Seagrass", heading_column_style)
    ws.col(5).width = 35*256
    if context['kelp_data'][0][2] == context['default_value']:
        ws.write(row, 6, "Kelp Surveys", heading_column_style)
        ws.col(6).width = 35*256
    else:
        ws.write(row, 6, "Kelp Survey Year", heading_column_style)
        ws.col(6).width = 35*256
        ws.write(row, 7, "Kelp Proportions", heading_column_style)
        ws.col(7).width = 35*256
    
def bio_subtidal_data(ws, context, row=11):
    row += subtidal_offset
    offset = 0
    if len(context['habitat_proportions']) == 0:
        ws.write(row+offset, 1, '---', data_style)
        offset += 1
    for proportion in context['habitat_proportions']:
        ws.write(row+offset, 1, str('%.1f%%    %s    (%.2f %s)') %(proportion[0], proportion[1], proportion[2], context['area_units']), data_style)
        offset += 1
    offset = 0
    if len(context['fish_list']) == 0:
        ws.write(row+offset, 2, '---', data_style)
        offset += 1
    for fish in context['fish_list']:
        ws.write(row+offset, 2, fish, data_style)
        offset += 1
    ws.write(row, 3, context['green_sturgeon'], data_style)
    ws.write(row+3, 3, context['green_sturgeon_perc']/100, perc_style)
    ws.write(row, 4, str('%.1f %s') % (context['nearest_coho_stream'], context['length_units']), data_style)
    ws.write(row, 5, str('%.1f %s') % (context['seagrass_area'], context['area_units']), data_style)
    if context['kelp_data'][0][2] == context['default_value']:
        ws.write(row, 6, context['kelp_data'][0][0], data_style)
    else:
        offset = 0
        for data in context['kelp_data']:
            ws.write(row+offset, 6, data[0], data_style)
            ws.write(row+offset, 7, str('%.2f %s    %.2f%%') % (data[1], context['area_units'], data[2]), data_style)
            offset += 1