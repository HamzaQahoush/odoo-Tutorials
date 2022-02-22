from odoo import api, fields, models, tools


class HospitalDoctor(models.Model):
    _name = 'doctor.hospital'
    _description = 'Doctors data here '
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    ], required=True, default='male', tracking=True)

    note = fields.Text(string='Description')
    image = fields.Binary(string='doctor image')
