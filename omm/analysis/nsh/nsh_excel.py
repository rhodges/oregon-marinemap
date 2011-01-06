import xlwt
from nsh_excel_geo import populate_geo_sheet
from nsh_excel_phy import populate_phy_sheet
from nsh_excel_bio import populate_bio_sheet
from nsh_excel_hum import populate_hum_sheet

def generate_nsh_excel_doc(context):
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
        
              
'''

STYLE_FACTORY = {}
FONT_FACTORY = {}
major_heading_style = xlwt.easyxf('font: bold true, italic on; alignment: horizontal left;')
minor_heading_style = xlwt.easyxf('font: italic on; alignment: horizontal left;')
heading_column_style = xlwt.easyxf('font: bold true; alignment: horizontal center;')
heading_row_style = xlwt.easyxf('font: bold true; alignment: horizontal center, wrap true;')
data_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='#,##0.0')
perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0.00%')

def test_doc(ws):    
    # Tweak printer settings
    # following makes a landscape layout on Letter paper
    # the width of the columns
    ws.fit_num_pages = 1
    ws.fit_height_to_pages = 0
    ws.fit_width_to_pages = 1
    # Set to Letter paper
    # See BiffRecords.SetupPageRecord for paper types/orientation
    ws.paper_size_code = 1
    # Set to landscape
    ws.portrait = 0
    # Write some stuff using our helper function
    # Formatting - hint, look at Format code in OOo
    #               format cells... Numbers tab
    # Write a percent
    write(ws, 0, 0, .495, {"format":"0%"})
    # Write a percent with negatives red
    write(ws, 1, 0, -.495, {"format":"0%;[RED]-0%"})
    # Dollar amounts
    write(ws, 2, 0, 10.99, {"format":'$#,##0'})
    
    # Font
    # Size
    write(ws, 0, 1, "Size 160(8pt)", {"font": (("height", 160),)})
    write(ws, 1, 1, "Size 200(10pt)", {"font": (("height", 200),)})
    # Bold
    write(ws, 2, 1, "Bold text", {"font": (("bold", True),)})
    
    # Background color
    # See http://groups.google.com.au/group/python-excel/attach/9362140b0dddf464/palette_trial.xls?part=2
    # for colour indices
    YELLOW = 5
    write(ws, 3, 1, "Yellow (5) Background", {"background": (("pattern", xlwt.Pattern.SOLID_PATTERN), ("pattern_fore_colour", YELLOW) )})
                            
    # Border
    write(ws, 0, 2, "Border", {"border": (("bottom",xlwt.Formatting.Borders.THIN), ("bottom_colour", YELLOW))})
    
    # Wrapping
    write(ws, 0, 3, "A bunch of long text to wrap", {"alignment":(("wrap", xlwt.Alignment.WRAP_AT_RIGHT),)})
    
    # Set column width
    # (see xlwt.BIFFRecords.ColInfoRecord for details, width in
    # 1/256th of zero character)
    write(ws, 0, 4, "A bunch of longer text not wrapped")
    ws.col(4).width = len("A bunch of longer text not wrapped")*256
    
    # Freeze/split headers when scrolling
    write(ws, 0, 5, "Header")
    ws.panes_frozen = True
    ws.horz_split_pos = 1
    for row in range(1, 20):
        write(ws, row, 5, row)
    
    
def write(ws, row, col, data, style=None):
    """
    Write data to row, col of worksheet (ws) using the style
    information.
    Again, I'm wrapping this because you'll have to do it if you
    create large amounts of formatted entries in your spreadsheet
    (else Excel, but probably not OOo will crash).
    """
    if style:
        s = get_style(style)
        ws.write(row, col, data, s)
    else:
        ws.write(row, col, data)    
    
def get_style(style):
    """
    Style is a dict maping key to values.
    Valid keys are: background, format, alignment, border
    The values for keys are lists of tuples containing (attribute,
    value) pairs to set on model instances...
    """
    style_key = tuple(style.items())
    s = STYLE_FACTORY.get(style_key, None)
    if s is None:
        s = xlwt.XFStyle()
        for key, values in style.items():
            if key == "background":
                p = xlwt.Pattern()
                for attr, value in values:
                    p.__setattr__(attr, value)
                s.pattern = p
            elif key == "format":
                s.num_format_str = values
            elif key == "alignment":
                a = xlwt.Alignment()
                for attr, value in values:
                    a.__setattr__(attr, value)
                s.alignment = a
            elif key == "border":
                b = xlwt.Formatting.Borders()
                for attr, value in values:
                    b.__setattr__(attr, value)
                s.borders = b
            elif key == "font":
                f = get_font(values)
                s.font = f
        STYLE_FACTORY[style_key] = s
    return s
    
def get_font(values):
    """
    'height' 10pt = 200, 8pt = 160
    """
    font_key = values
    f = FONT_FACTORY.get(font_key, None)
    if f is None:
        f = xlwt.Font()
        for attr, value in values:
            f.__setattr__(attr, value)
        FONT_FACTORY[font_key] = f
    return f    
'''    