import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side

from pprint import pprint

class ExcelSaver():
    def __init__(self, filename):
        print(filename)
        self.filename = filename
    def saveComponents(self, components, offset = 0):
        pprint(components)
        wb = openpyxl.Workbook()
        sheet = wb.active
        self.setStyleHeaderCell(sheet.cell(1, 1 + offset), 'Виріб')
        self.setStyleHeaderCell(sheet.cell(1, 2 + offset), 'Деталь')
        self.setStyleHeaderCell(sheet.cell(1, 3 + offset), 'Кількість')

        for i in range (0, len(components)):
            self.setStyleCell(sheet.cell(i + 2, 1 + offset), components[i]['device'])
            self.setStyleCell(sheet.cell(i + 2, 2 + offset), components[i]['name'])
            self.setStyleCell(sheet.cell(i + 2, 3 + offset), components[i]['count'])
            #sheet.cell(i + 2, 1 + offset).value = components[i]['device']
            # sheet.cell(i + 2, 2 + offset).value = components[i]['name']
            # sheet.cell(i + 2, 3 + offset).value = components[i]['count']
        self.alignSheet(sheet)
        if self.filename.endswith(".xlsx"):
            wb.save(self.filename)
        else:
            wb.save(self.filename + ".xlsx")

    def setStyleHeaderCell(self, cell, value, bold = 'True'):
        cell.value = value
        cell.font = Font(bold = bold, size = 12)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = Border(bottom = Side(border_style = 'thin', color = 'dd0000'))

    def setStyleCell(self, cell, value):
        cell.value = value
        cell.alignment = Alignment(horizontal='center', vertical='center')

    def alignSheet(self, sheet):
        for column_cells in sheet.iter_cols(min_col=1, max_col=sheet.max_column):
            max_length = 0
            column = column_cells[0].column  # Отримуємо номер стовпця
            for cell in column_cells:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            sheet.column_dimensions[openpyxl.utils.get_column_letter(column)].width = max_length + 2

