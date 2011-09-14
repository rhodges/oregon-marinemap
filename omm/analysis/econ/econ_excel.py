import xlwt
from econ_excel_noaa import populate_noaa_sheet
from econ_excel_feam import populate_feam_sheet
from econ_excel_chrt import populate_chrt_sheet
from econ_excel_rec import populate_rec_sheet

'''
called from analysis.econ.econ_exports.excel_report
'''
def generate_econ_excel_doc(context, type):
    #create a workbook
    wb = xlwt.Workbook()
    #add and populate individual sheets
    if type in ['noaa', 'all']:
        noaa_context = context['noaa']
        generate_noaa_sheet(wb, noaa_context)
    if type in ['feam', 'all']:
        feam_context = context['feam']
        generate_feam_sheet(wb, feam_context)
    if type in ['chrt', 'all']:
        chrt_context = context['chrt']
        generate_chrt_sheet(wb, chrt_context)
    if type in ['rec', 'all']:
        rec_context = context['rec']
        generate_rec_sheet(wb, rec_context)
    return wb
    
def generate_noaa_sheet(wb, noaa_context):
    ws = wb.add_sheet("Commercial (NOAA)", cell_overwrite_ok=True)
    populate_noaa_sheet(ws, noaa_context)
    
def generate_feam_sheet(wb, feam_context):
    ws = wb.add_sheet("Commercial (FEAM)")
    populate_feam_sheet(ws, feam_context)
    
def generate_chrt_sheet(wb, chrt_context):
    ws = wb.add_sheet("Charter")
    populate_chrt_sheet(ws, chrt_context)
    
def generate_rec_sheet(wb, rec_context):
    ws = wb.add_sheet("Recreational") 
    populate_rec_sheet(ws, rec_context)
    