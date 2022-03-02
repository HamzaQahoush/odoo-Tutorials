from odoo import api, fields, models, tools


class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

    # product_qty, product_id

    #    order_line > available Quantity - > RFQ\
    #     quant_obj = self.env['stock.quant']
    #     qty_available = quant_obj._get_available_quantity(product_id)
    def check_available_products(self):
        dic = {}
        missing_qty = {}
        if self.order_line:
            for key in self.order_line:
                dic[key['product_id']['id']] = key['product_qty']

        for product_id in [*dic]:
            product = self.env['product.product'].browse(product_id)
            available_qty = product.qty_available
            if available_qty < dic[product_id]:
                missing_qty[product_id] = dic[product_id] - available_qty
        print(missing_qty)
        return missing_qty

    def create_po_button(self):

        return {
            'name': 'RFQ',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
            'res_model': 'purchase.order',
            'target': 'current',
            'domain': [()]
        }

        # sale_order_lines = self.env['sale.order.line'].sudo().browse(sale_line_ids | empty_line_ids)

    # 'qty_available_today': 0.0
    # 'qty_to_deliver': 1.0
    # 'product_qty': 1.0
    # 'product_uom_qty': 1.0


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        """
        triggerd on save
        """
        # missed_qut_dic = SalesOrderInherit.check_available_products(self)
        # print('missed_qut_dic------------------>', missed_qut_dic)

        # vals = {
        #     'product_id': 1,
        #     'partner_id': 1,
        #     'product_qty': 1,
        #     'name': 1,
        #
        # }
        res = super(PurchaseOrderInherit, self).create(vals)
        print('vals create-------------------', vals.get('order_line')[0][2])
        print('vals res create ', res)
        return res

    @api.model
    def default_get(self, fields):
        """
         - override the default get function and set default values for fields.
         - res : will be a dic {key:value} for each field.
         - triggered when clicking on create.
         - fields is list []  contain all fields , and res will be dic {key:value}

        """
        res = super(PurchaseOrderInherit, self).default_get(fields)
        print('res default_get-------------', res)
        print('fields default_get-------------------', fields)
        return res


class StockQuant(models.Model):
    _inherit = "stock.quant"


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
