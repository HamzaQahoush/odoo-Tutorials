from odoo import api, models, fields, _


class PatientReportWizard(models.TransientModel):
    _name = 'patient.report.wizard'
    _description = 'Model to show appointment wizard'

    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    ], string='gender')

    def action_print_report(self):
        data = {
            'form_data': self.read()[0]
        }
        return self.env.ref('hospital.action_report_all_patient').report_action(self, data=data)
