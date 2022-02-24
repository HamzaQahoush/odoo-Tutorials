from odoo import api, models, fields, _


class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment_wizard'
    _description = 'Model to creat appointment wizard'

    appointment_date = fields.Date(string='Date', required=False)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)

    def create_appointment_action(self):
        """
        method to insert data from wizard into data base
        -vals:: data will be inserted from wizard, and it's value from model.
        - self.env['table.name'].create(vals) :: method will take values and insert it in required table instance of class .
          it will create a record.
        - return :: will return view , we can add {... 'target' : 'new'} to make it pop up.

        """
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_id' : 1,
            'date_appointment': self.appointment_date
        }
        print(vals)
        appointment_rec = self.env['hospital.appointment'].create(vals)
        return {
            'name': _('appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id
        }

    def view_appointments_action(self):
        """
        method onClick(view appointment) to view appointment for specific  patient
        action:: we grab the action that we want to render `moduleName.actionID` .
        set the domain for our conditions.
        return the action.
        """
        #  method 1 ::
        # action = self.env.ref('hospital.appointments_action').read()[0]
        # action['domain'] = [('patient_id', '=', self.patient_id.id)]
        # return action

        #  method 2::
        # action=self.env['ir.actions.actions']._for_xml_id('hospital.appointments_action')
        # action['domain'] = [('patient_id', '=', self.patient_id.id)]
        # return action

        # 3rd method if we can return action as dic:
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.patient_id.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current'
        }

