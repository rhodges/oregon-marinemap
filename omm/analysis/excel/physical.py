import xlwt
from analysis.excel.utils import minor_heading_style, heading_column_style, data_style, integer_data_style, perc_style


def phy_intertidal_headers(ws, row=3):
    ws.write(row-1, 0, "Intertidal Physical Characteristics", minor_heading_style)
    ws.write(row, 1, "Length of Intertidal Shoreline", heading_column_style)
    ws.col(1).width = 35*256
    ws.write(row, 2, "Percent of Oregon Coast Shoreline", heading_column_style)
    ws.col(2).width = 35*256
    ws.write(row, 3, "Shoreline Types and Proportions", heading_column_style)
    ws.col(3).width = 50*256
    ws.write(row, 4, "Number of Islands", heading_column_style)
    ws.col(4).width = 35*256
    ws.write(row, 5, "Total Island Area", heading_column_style)
    ws.col(5).width = 35*256
    
def phy_intertidal_data(ws, context, row=4):
    if context['percent_shoreline'] == context['default_value']:
        ws.write(row, 1, str('0.0 %s') % context['length_units'], data_style)
        ws.write(row, 2, 0.0, perc_style)
    else:
        ws.write(row, 1, str('%.2f %s') % (context['length'], context['length_units']), data_style)
        ws.write(row, 2, context['percent_shoreline']/100, perc_style)
    global subtidal_offset
    subtidal_offset = 0
    offset = 0
    for proportion in context['shoreline_proportions']:
        if proportion[1] == context['default_value']:
            ws.write(row+offset, 3, context['default_value'], data_style)
            subtidal_offset += 1
        else:
            ws.write(row+offset, 3, str('%.1f%%    %s    (%.2f %s)') %(proportion[0], proportion[1], proportion[2], context['length_units']), data_style)
            offset += 1
            subtidal_offset += 1
    ws.write(row, 4, context['islands'], integer_data_style)
    ws.write(row, 5, str('%.3f %s') % (context['island_area'], context['area_units']), data_style)
        
def phy_subtidal_headers(ws, row=6):
    row += subtidal_offset
    ws.write(row-1, 0, "Subtidal Physical Characteristics", minor_heading_style)
    ws.write(row, 1, "Subtidal Area", heading_column_style)
    ws.write(row, 2, "Percent Shallow (<=25m)\n Percent Deep (>25m)", heading_column_style)
    ws.write(row, 3, "Seafloor Lithology", heading_column_style)
    ws.write(row, 4, "Average Depth", heading_column_style)
    ws.write(row+3, 4, "Min Depth", heading_column_style)
    ws.write(row+6, 4, "Max Depth", heading_column_style)
    ws.write(row, 5, "Proximity to Shore", heading_column_style)
    
def phy_subtidal_data(ws, context, row=7):
    row += subtidal_offset
    ws.write(row, 1, str('%.1f %s') % (context['subtidal_area'], context['area_units']), data_style)
    if context['subtidal_area'] > 0.0:
        ws.write(row, 2, context['perc_shallow']/100, perc_style)
        ws.write(row+1, 2, context['perc_deep']/100, perc_style)
    else:
        ws.write(row, 2, context['default_value'], data_style)
        ws.write(row+1, 2, context['default_value'], data_style)
    offset = 0
    for proportion in context['lithology_proportions']:
        ws.write(row+offset, 3, str('%.1f%%    %s    (%.2f %s)') %(proportion[0], proportion[1], proportion[2], context['area_units']), data_style)
        offset += 1
    if context['subtidal_area'] > 0.0:
        ws.write(row, 4, str('%.1f meters') % context['average_depth'], data_style)
        ws.write(row+3, 4, str('%.1f meters') % context['min_depth'], data_style)
        ws.write(row+6, 4, str('%.1f meters') % context['max_depth'], data_style)
    else:
        ws.write(row, 3, context['default_value'], data_style)
        ws.write(row, 4, context['default_value'], data_style)
        ws.write(row+3, 4, context['default_value'], data_style)
        ws.write(row+6, 4, context['default_value'], data_style)
    ws.write(row, 5, str('%.1f %s') % (context['distance_to_shore'], context['length_units']), data_style)
    