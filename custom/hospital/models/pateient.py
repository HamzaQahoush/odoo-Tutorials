from odoo import api, fields, models, tools, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "hospital patient description"
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    appointment_count = fields.Integer(string='appointments count', tracking=True, compute='_compute_appointment_count')
    image = fields.Binary(string='patient name')

    def _compute_appointment_count(self):
        for rec in self:
            print(rec)
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            # SELECT COUNT(*) FROM hospital.appointment WHERE patient_id = id
            rec.appointment_count = appointment_count

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
        print(values)
        res = super(HospitalPatient, self).create(values)
        return res

    @api.model
    def default_get(self, fields):
        """
         - override the default get function and set default values for fields.
         - res : will be a dic {key:value} for each field.
         - triggered when clicking on create.
         - fields is list []  contain all fields , and res will be dic {key:value}

        """
        res = super(HospitalPatient, self).default_get(fields)
        print('here is the overriding method')

        return res
