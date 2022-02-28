from odoo import api, fields, models, tools


class HospitalDoctor(models.Model):
    _name = 'doctor.hospital'
    _description = 'Doctors data here '
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    ], required=True, default='male', tracking=True)

    note = fields.Text(string='Description')
    image = fields.Binary(string='doctor image')
    appointment_count = fields.Integer(string='appointments count', tracking=True, compute='_compute_appointment_count')
    active = fields.Boolean(string="Active", default=True)
    # newly added
    doctor_appointment_ids = fields.One2many('hospital.patient', 'appointment_ids', string='doctor_appointment_ids')

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = f'copy {self.doctor_name}'
        default['note'] = ""
        # to prevent copy other fields
        rec = super(HospitalDoctor, self).copy(default)
        return rec

    def _compute_appointment_count(self):
        for rec in self:
            print(rec)
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            # SELECT COUNT(*) FROM hospital.appointment WHERE patient_id = id
            rec.appointment_count = appointment_count
