import xlwt
from analysis.excel.utils import major_heading_style, heading_column_style, port_style, fishery_style, currency_style

def populate_chrt_sheet(ws, context):
    chrt_headers(ws, context)
    chrt_data(ws, context)
    
def chrt_headers(ws, context, row=3):
    ws.write(0, 0, "Charter Fishing Analysis Report for %s" % context['aoi'].name, major_heading_style)
    ws.write(row-1, 0, "Port/Fishery", heading_column_style)
    ws.col(0).width = 35*256
    ws.write(row-1, 1, "Estimated Gross Economic Revenue", heading_column_style)
    ws.col(1).width = 35*256
    ws.write(row-1, 2, "Estimated Economic Output", heading_column_style)
    ws.col(2).width = 35*256
    
def chrt_data(ws, context, row=3):
    offset = 0
    for port, fisheries in context['ports']:
        offset += 1
        ws.write(row+offset, 0, port, port_style)
        offset += 1
        for fishery_report in fisheries:
            ws.write(row+offset, 0, fishery_report[0], fishery_style)
            ws.write(row+offset, 1, round(fishery_report[2]), currency_style)
            ws.write(row+offset, 2, round(fishery_report[3]), currency_style)   
            offset += 1
    offset += 1
    ws.write(row+offset, 0, 'Statewide', port_style)
    offset += 1
    for state_report in context['state_totals']:
        ws.write(row+offset, 0, state_report[0], fishery_style)
        ws.write(row+offset, 1, round(state_report[1][1]), currency_style)
        ws.write(row+offset, 2, round(state_report[1][2]), currency_style)
        offset += 1
    