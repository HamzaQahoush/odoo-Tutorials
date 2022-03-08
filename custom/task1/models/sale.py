from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError


class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

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
        if self.order_line:
            for key in self.order_line:
                order_lines.append({'order_line_id': key['id'], 'product_id': key['product_id']['id'],
                                    'partner_id': key['order_partner_id'].id,
                                    'product_qty': key['product_qty'], 'price_unit': key['price_unit'],
                                    'display_name': key['display_name']})
        for order in order_lines:
            id = order.get('product_id')
            product = self.env['product.product'].browse(id)
            available_qty = product.qty_available
            if available_qty < order['product_qty']:
                missing_qty.append(
                    {'product_id': order.get('product_id'), 'missing': order.get('product_qty') - available_qty,
                     'order_line_id': order.get('order_line_id'), 'partner_id': order.get('partner_id'),
                     'price_unit': order.get('price_unit'), 'display_name': order.get('display_name')
                     })

        return missing_qty

    # 'free_qty': line.product_id.free_qty,
    def po_button(self):
        lines = []
        for line in self.order_line:
            lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.product_qty if line.product_id.free_qty >= line.product_qty else line.product_id.free_qty,
                'price_unit': line.price_unit,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,

            }))
        purchase_rec = self.env["purchase.order"].create(
            {"partner_id": self.partner_id.id, "origin": self.origin, "order_line": lines})

        return {
            'name': 'RFQ',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
            'res_model': 'purchase.order',
            'target': 'current',
            'res_id': purchase_rec.id,

        }



