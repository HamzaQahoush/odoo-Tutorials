from odoo import api, models, fields, _


class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Model to print appointment wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    from_date = fields.Date('Date From')
    to_date = fields.Date('Date To')

    def action_print_report(self):
        """
       - This is method to trigger the on click button of print pdf from wizard
       - self.read()[0] is dict contains {key: val} of the model. for selected one {'patient_id' :1 , ... } 
        
       -  appointment= self.env['hospital.appointment'].search_read([]) --> give us *all* fields in the model 
        as list of dict e.g : 
        [{'id': 18, 'ref': 'OT00019', 'patient_id': (16, '[ HP00011]  ehab'), 'doctor_id': (7, 'samer'), 'age': 25, }

        """

        # all data as list of dict
        domain = []

        patient_id = self.patient_id
        from_date = self.from_date
        to_date = self.to_date

        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]
        if from_date:
            domain += [('date_appointment', '>=', from_date)]
        if to_date:
            domain += [('date_appointment', '<=', to_date)]

        appointments = self.env['hospital.appointment'].search_read(domain)  # to filter data
        data = {
            'form_data': self.read()[0],
            'appointments': appointments,
        }
        # action_report_appointment -> form Report record id
        return self.env.ref('hospital.action_report_appointment').report_action(self, data=data)

    def action_print_excel_report(self):
        """
        - This is function that send data to the function in report `generate_xlsx_report` in report directory.
        - report_patient_appointment_xls : is the record ID in report file.
        - .search([]) give all the data as record set .

        """
        domain = []

        patient_id = self.patient_id
        from_date = self.from_date
        to_date = self.to_date

        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]
        if from_date:
            domain += [('date_appointment', '>=', from_date)]
        if to_date:
            domain += [('date_appointment', '<=', to_date)]

        appointments = self.env['hospital.appointment'].search_read(domain)
        data = {
            'form_data': self.read()[0],  # as dict
            'appointments': appointments,
        }
        return self.env.ref('hospital.report_patient_appointment_xls').report_action(self, data=data)
