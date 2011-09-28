import xlwt
from analysis.excel.utils import major_heading_style, heading_column_style, port_style, fishery_style, currency_style, notes_style, percentage_style

def populate_noaa_sheet(ws, context):
    noaa_headers(ws, context)
    noaa_data(ws, context)
    
def noaa_headers(ws, context, row=3):
    ws.write(0, 0, "NOAA Commercial Fishing Analysis Report for %s" % context['aoi'].name, major_heading_style)
    ws.write(row-1, 0, "Port/Fishery", heading_column_style)
    ws.col(0).width = 35*256
    ws.write(row-1, 1, "Average Annual Gross Economic Revenue", heading_column_style)
    ws.col(1).width = 35*256
    ws.write(row-1, 2, "Estimated Economic Output", heading_column_style)
    ws.col(2).width = 35*256
    ws.write(row-1, 3, "Percentage", heading_column_style)
    ws.col(3).width = 35*256
    
def noaa_data(ws, context, row=3):
    offset = 0
    for port, fisheries in context['ports']:
        offset += 1
        ws.write(row+offset, 0, port, port_style)
        offset += 1
        for fishery_report in fisheries:
            ws.write(row+offset, 0, fishery_report[0], fishery_style)
            ws.write(row+offset, 1, round(fishery_report[2]), currency_style)
            ws.write(row+offset, 2, round(fishery_report[3]), currency_style) 
            ws.write(row+offset, 3, fishery_report[4], percentage_style)   
            offset += 1
    offset += 1
    ws.write(row+offset, 0, 'Statewide', port_style)
    offset += 1
    for state_report in context['state_totals']:
        ws.write(row+offset, 0, state_report[0], fishery_style)
        ws.write(row+offset, 1, round(state_report[1][1]), currency_style)
        ws.write(row+offset, 2, round(state_report[1][2]), currency_style)
        ws.write(row+offset, 3, state_report[1][3], percentage_style)
        offset += 1
        
    add_footnotes(ws, row+offset+1)
    
def add_footnotes(ws, row):
    ws.write(row, 0, 'Notes:', major_heading_style)
    ws.write(row+1, 0, '1. In the commercial sector average annual gross economic revenue (GER) was calculated using annual gross economic revenue (e.g., ex-vessel landings revenue) data for the years 2004-2008 and is displayed in 2008 dollar values.', notes_style)
    ws.write(row+2, 0, '2. Estimated economic output (EEO) is a measure of the total direct and indirect economic activity associated with sales or expenditures in a certain sector.', notes_style)
    ws.write(row+3, 0, '3. The percentage indicates the percent value of a given fishery at a given port.', notes_style)