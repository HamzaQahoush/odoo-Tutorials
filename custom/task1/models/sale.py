from odoo import api, fields, models, tools


class SalesOrderInherit(models.Model):
    _inherit = "sale.order"

    # product_qty, product_id

    #    order_line > available Quantity - > RFQ\
    #     quant_obj = self.env['stock.quant']
    #     qty_available = quant_obj._get_available_quantity(product_id)

    def product_qty_location_check(self):
        dic = {}
        if self.order_line:
            for key in self.order_line:
                dic[key['product_id']['id']] = key['product_qty']

            print(dic)
        quant_obj = self.env['stock.quant'].search_read([])
        # qty_available = quant_obj._get_available_quantity(14)
        print(quant_obj)

        # sale_order_lines = self.env['sale.order.line'].sudo().browse(sale_line_ids | empty_line_ids)

    # 'qty_available_today': 0.0
    # 'qty_to_deliver': 1.0
    # 'product_qty': 1.0
    # 'product_uom_qty': 1.0


class StockQuant(models.Model):
    _inherit = "stock.quant"


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
