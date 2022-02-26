from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[
        ('test', 'test')
    ], ondelete={'test': 'set default'})
