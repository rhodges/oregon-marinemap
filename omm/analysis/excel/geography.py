import xlwt
from utils import minor_heading_style, heading_column_style, data_style, perc_style

def geo_spatial_headers(ws, row=3):
    ws.write(row-1, 0, "General Spatial Characteristics", minor_heading_style)
    ws.write(row, 1, "Area", heading_column_style)
    ws.col(1).width = 35*256
    ws.write(row, 2, "Perimeter", heading_column_style)
    ws.col(2).width = 35*256
    ws.write(row, 3, "Intertidal", heading_column_style)
    ws.col(3).width = 35*256
    ws.write(row, 4, "Islands", heading_column_style)
    ws.col(4).width = 40*256
    ws.write(row, 5, "Percent of Territorial Sea", heading_column_style)
    ws.col(5).width = 35*256
    
def geo_spatial_data(ws, context, row=4):
    ws.write(row, 1, str('%.1f %s') % (context['area'], context['area_units']), data_style)
    ws.write(row, 2, str('%.1f %s') % (context['perimeter'], context['length_units']), data_style)
    ws.write(row, 3, context['intertidal'], data_style)
    ws.write(row, 4, context['islands'], data_style)
    ws.write(row, 5, context['ratio']/100, perc_style)
        