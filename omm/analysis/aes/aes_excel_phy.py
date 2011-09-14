import xlwt
from analysis.excel.utils import major_heading_style
from analysis.excel.physical import phy_intertidal_headers, phy_intertidal_data, phy_subtidal_headers, phy_subtidal_data

def populate_phy_sheet(ws, context):
    phy_header(ws, context)
    phy_intertidal_headers(ws)
    phy_intertidal_data(ws, context)
    phy_subtidal_headers(ws)
    phy_subtidal_data(ws, context)
    
def phy_header(ws, context):
    ws.write(0, 0, "Energy Site Physical Report for %s" % context['aes'].name, major_heading_style)
    