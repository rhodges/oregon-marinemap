import xlwt
from analysis.excel.utils import major_heading_style, heading_column_style, port_style, fishery_style, currency_style, notes_style, percentage_style

def populate_feam_sheet(ws, context):
    feam_headers(ws, context)
    feam_data(ws, context)
    
def feam_headers(ws, context, row=3):
    ws.write(0, 0, "FEAM Commercial Fishing Analysis Report for %s" % context['aoi'].name, major_heading_style)
    ws.write(row-1, 0, "Port/Fishery", heading_column_style)
    ws.col(0).width = 35*256
    ws.write(row-1, 1, "Average Annual Gross Economic Revenue", heading_column_style)
    ws.col(1).width = 35*256
    ws.write(row-1, 2, "Estimated Personal Income", heading_column_style)
    ws.col(2).width = 35*256
    ws.write(row-1, 3, "Percentage", heading_column_style)
    ws.col(3).width = 35*256
    
def feam_data(ws, context, row=3):
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
    ws.write(row+1, 0, '1. Average annual gross economic revenue (GER) for commercial fisheries was calculated using ODFW ex-vessel landings revenue data for the years 2004-2008 and is displayed in 2008 dollar values.', notes_style)
    ws.write(row+2, 0, '2. Estimated personal income (EPI) is a measure of the portion of direct and indirect economic activity associated with sales or expenditures in a certain sector that accrues to households in terms of wages, salaries, and profits; estimates were derived from the Fisheries Economic Assessment Model (FEAM) produced by The Research Group (2005).', notes_style)
    ws.write(row+3, 0, '3. The percent values represent the percentage of Estimate Personal Income (EPI) found in your Area of Interest for a particular port-fishery or state-fishery combination.', notes_style)