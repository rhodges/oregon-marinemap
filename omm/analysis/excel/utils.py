import xlwt

major_heading_style = xlwt.easyxf('font: bold true, italic on; alignment: horizontal left;')
minor_heading_style = xlwt.easyxf('font: italic on; alignment: horizontal left;')
heading_column_style = xlwt.easyxf('font: bold true; alignment: horizontal center, wrap true;')
heading_row_style = xlwt.easyxf('font: bold true; alignment: horizontal center, wrap true;')
data_style = xlwt.easyxf('alignment: horizontal center, wrap true;',num_format_str='#,##0.0')
integer_data_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='#,##0')
perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0.00%')
integer_perc_style = xlwt.easyxf('alignment: horizontal center;',num_format_str='0%')


'''
'''
def build_excel_response(file_name, workbook):
    """
    This method assumes you've built an excel workbook elsewhere and just want to build a response object from it.
    """
    from django.http import HttpResponse
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=%s.xls' % ( file_name )
    workbook.save(response)

    return response        

    
