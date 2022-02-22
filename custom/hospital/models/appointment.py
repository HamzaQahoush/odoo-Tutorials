from odoo import api, fields, models, tools, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "hospital patient Appointment description"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(string='Patient ref', required=True, tracking=True, copy=False,
                      default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='patient')
    doctor_id = fields.Many2one('doctor.hospital', string='doctor',required=True)
    age = fields.Integer(string='age', related='patient_id.age', tracking=True)
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')

                              ], string='Status')
    date_appointment = fields.Date(string='Date')
    date_checkup = fields.Datetime(string='Check uptime')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    ], required=True, default='male', tracking=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # override create method
    @api.model
    def create(self, values):
        if values.get('ref', _('New')) == _('New'):
            values['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        # output values= {'state': 'draft', 'name':'Hamza', 'age':'34' }
        res = super(HospitalAppointment, self).create(values)
        return res

    @api.onchange('patient_id', )
    def on_change_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''
