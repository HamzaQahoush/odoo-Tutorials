from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "hospital patient description"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    @api.model
    def default_get(self, fields):
        """
         - override the default get function and set default values for fields.
         - res : will be a dic {key:value} for each field.
         - triggered when clicking on create.
         - fields is list []  contain all fields , and res will be dic {key:value}

        """
        res = super(HospitalPatient, self).default_get(fields)
        res['note'] = 'New Patient Created'
        return res

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    ], required=True, default='male', tracking=True)

    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')

                              ], string='Status')
    responsible_id = fields.Many2one(comodel_name='res.partner', string='Responsible')

    reference = fields.Char(string='Patient Reference', required='True', copy=False, readonly=True,
                            default=lambda self: _('New'))
    appointment_count = fields.Integer(string='appointments count', compute='_compute_appointment_count')
    image = fields.Binary(string='patient name')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count
            # SELECT COUNT(*) FROM hospital.appointment WHERE patient_id = id

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    # override create method
    @api.model
    def create(self, values):
        if not values['note']:
            values['note'] = 'New patient'
        if values.get('reference', _('New')) == _('New'):
            values['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        # output values= {'state': 'draft', 'name':'Hamza', 'age':'34' }
        res = super(HospitalPatient, self).create(values)
        return res

    @api.constrains('name')
    def check_name(self):
        # check duplicate record
        for rec in self:
            patient = self.env["hospital.patient"].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patient:
                raise ValidationError(f'You cannot add  {rec.name} twice !!')

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(f'You cannot add  {rec.age} cannot be 0  !!')

    def name_get(self):
        # to modify the name in list view
        result = []
        for rec in self:
            name = f'[ {rec.reference}]  {rec.name}'
            result.append((rec.id, name))
        return result

    def action_open_appointment(self):
        # to return view of appointment after clicking on Smart Buttons
        return {
            'name': _('appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)]
        }
