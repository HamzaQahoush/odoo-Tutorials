from odoo import models
import base64
import io


class PatientAppointmentXlsx(models.AbstractModel):
    _name = 'report.hospital.report_patient_appointment_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        print(data['appointments'], "data[appointments]")
        sheet = workbook.add_worksheet('patient appointment xls')
        bold = workbook.add_format({'bold': True})
        sheet.set_column('D:D', 12)
        row, col = 0, 0
        sheet.write(row, col, 'ref' ,bold)
        sheet.write(row, col + 1, 'patient ID', bold)
        for rec in data['appointments']:
            row += 1
            sheet.write(row, col, rec['ref'])
            sheet.write(row, col+1, rec['patient_id'][1])
