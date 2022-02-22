from odoo import api, fields, models, tools


class SalesOrder(models.Model):
    _inherit = "sale.order"
    sale_description= fields.Char(string='sale description' , required=True)