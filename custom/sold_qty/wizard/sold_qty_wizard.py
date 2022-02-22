from odoo import models, fields


class Sold_Report(models.TransientModel):
    _name = 'sold.qty.wizard'
    _description = 'add sold quantity to reporting'

    order_select = fields.Selection([('order_po', 'order PO'), ('order_so', 'order SO'), ], string='Sold Report',
                                    required=True)
    from_date = fields.Date('From')
    to_date = fields.Date('To')
