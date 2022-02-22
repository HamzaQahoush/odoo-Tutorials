from odoo import api, models, fields, _


class SearchAppointmentWizard(models.TransientModel):
    _name = 'search.appointment.wizard'
    _description = 'Model to search appointment wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)

    def view_appointments_action(self):
        action = self.env.ref('hospital.appointments_action').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action
