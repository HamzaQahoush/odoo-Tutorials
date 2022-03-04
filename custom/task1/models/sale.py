from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

    # product_qty, product_id

    #    order_line > available Quantity - > RFQ\
    #     quant_obj = self.env['stock.quant']
    #     qty_available = quant_obj._get_available_quantity(product_id)

    def check_available_products(self):
        """
        - this method is to check all order-lines quantities  in sale-order and compare
        it to available quantities.
        return :: dict , contains the {product_id : missed Quantities}
        for example : [{'product_id': 12, 'order_line_id': 12, 'missing': 1.0 , 'partner_id': 7}]
        """
        order_lines = []
        global missing_qty
        missing_qty = []
        for rec in self:
            print(rec['partner_id'])
        if self.order_line:
            for key in self.order_line:
                order_lines.append({'order_line_id': key['id'], 'product_id': key['product_id']['id'],
                                    'partner_id': key['order_partner_id'].id,
                                    'product_qty': key['product_qty'], 'price_unit': key['price_unit']})
        for order in order_lines:
            id = order.get('product_id')
            product = self.env['product.product'].browse(id)
            available_qty = product.qty_available
            if available_qty < order['product_qty']:
                missing_qty.append(
                    {'product_id': order.get('product_id'), 'missing': order.get('product_qty') - available_qty,
                     'order_line_id': order.get('order_line_id'), 'partner_id': order.get('partner_id'),
                     'price_unit': order.get('price_unit')
                     })
        print(missing_qty)

        return missing_qty

    @staticmethod
    def get_required_field(missing_qty, field):
        field, = [x[str(field)] for x in missing_qty]
        return field

    def po_button(self):

        missing_qty = self.check_available_products()
        if not missing_qty:
            raise ValidationError(
                ' Your sale order will complete  No need to create PO.')

        # print('missing_qty--------', missing_qty)
        # order_line, = [x['order_line_id'] for x in missing_qty]

        vals = {
            'partner_id': self.get_required_field(missing_qty, 'partner_id'),
            'order_line': [
                (0, 0, {

                    'product_id': self.get_required_field(missing_qty, 'product_id'),
                    'product_qty': self.get_required_field(missing_qty, 'missing'),
                    'price_unit': self.get_required_field(missing_qty, 'price_unit'),
                })]

        }
        purchase_rec = self.env['purchase.order'].create(vals)

        return {
            'name': 'RFQ',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
            'res_model': 'purchase.order',
            'target': 'current',
            'res_id': purchase_rec.id,

        }

        # sale_order_lines = self.env['sale.order.line'].sudo().browse(sale_line_ids | empty_line_ids)



class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    @api.model_create_multi
    def create(self, vals):
        """
        triggerd on save
        """
        # vals = {
        #     'product_id': 1,
        #     'partner_id': 1,
        #     'product_qty': 1,
        #     'name': 1,
        #
        # }
        res = super(PurchaseOrderInherit, self).create(vals)
        # print('vals create-------------------', vals.get('order_line')[0][2])
        # print('vals res create ', res)
        return res

    # @api.model
    # def default_get(self, fields):
    #
    #     print('missed_qut_dic self.helper() this is form PurchaseOrderInherit default_get------------------>')
    #
    #     """
    #      - override the default get function and set default values for fields.
    #      - res : will be a dic {key:value} for each field.
    #      - triggered when clicking on create.
    #      - fields is list []  contain all fields , and res will be dic {key:value}
    #
    #     """
    #     res = super(PurchaseOrderInherit, self).default_get(fields)
    #
    #     print('res default_get-------------', res)
    #     print('fields default_get-------------------', fields)
    #     return res


class StockQuant(models.Model):
    _inherit = "stock.quant"


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
