from odoo import models
import base64
import io

class PatientXlsx(models.AbstractModel):
    _name = 'report.hospital.report_patient_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet('patient ID xls')
        bold = workbook.add_format({'bold': True})
        sheet.set_column('D:D', 12)
        row, col = 3, 3
        for obj in patients:
            bold = workbook.add_format({'bold': True})
            row += 1
            sheet.merge_range(row, col, row, col + 1, 'ID Card')
            row += 1
            sheet.write(row, col, 'Name')
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'age')
            sheet.write(row, col + 1, obj.age)
            row+=1
            sheet.write(row, col, 'ref')
            sheet.write(row, col + 1, obj.reference)
