import xlwt
from aes_excel_geo import populate_geo_sheet
from aes_excel_phy import populate_phy_sheet
from aes_excel_bio import populate_bio_sheet
from aes_excel_hum import populate_hum_sheet

def generate_aes_excel_doc(context):
    #create a workbook
    wb = xlwt.Workbook()
    #add and populate individual sheets
    geo_context = context['geo']
    generate_geo_sheet(wb, geo_context)
    phy_context = context['phy']
    generate_phy_sheet(wb, phy_context)
    bio_context = context['bio']
    generate_bio_sheet(wb, bio_context)
    hum_context = context['hum']
    generate_hum_sheet(wb, hum_context)
    return wb
    
def generate_geo_sheet(wb, geo_context):
    ws = wb.add_sheet("Geography", cell_overwrite_ok=True)
    populate_geo_sheet(ws, geo_context)
    
def generate_phy_sheet(wb, phy_context):
    ws = wb.add_sheet("Physical")
    populate_phy_sheet(ws, phy_context)
    
def generate_bio_sheet(wb, bio_context):
    ws = wb.add_sheet("Biology")
    populate_bio_sheet(ws, bio_context)
    
def generate_hum_sheet(wb, hum_context):
    ws = wb.add_sheet("Human") 
    populate_hum_sheet(ws, hum_context)
        
    