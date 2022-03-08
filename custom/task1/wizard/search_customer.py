from odoo import api, models, fields, _


class SearchCustomerWizard(models.TransientModel):
    _name = 'search.customers.wizard'
    _description = 'Model to search customer wizard'

    partner_id = fields.Many2one(
        'res.partner', string='Customer',
    )

    from_date = fields.Datetime('Date From')
    to_date = fields.Datetime('Date To')

    def print_pdf(self):
        domain_of_order_lines_for_customer = []
        sales_order_count = set()
        partner_id = self.partner_id
        from_date = self.from_date
        to_date = self.to_date

        if partner_id:
            domain_of_order_lines_for_customer += [('order_partner_id', '=', partner_id.id)]
        if from_date:
            domain_of_order_lines_for_customer += [('create_date', '>=', from_date)]

        if to_date:
            domain_of_order_lines_for_customer += [('create_date', '<=', to_date)]

        order_lines = self.env['sale.order.line'].search_read(domain_of_order_lines_for_customer)

        print('order_line with the range or all ------------------', order_lines)

        for order_id in order_lines:
            if order_id['order_id'][1] not in sales_order_count:
                sales_order_count.add(order_id['order_id'][1])
        print('order_lines_count', sales_order_count)
        data = {
            'form_data': self.read()[0],
            'order_lines': order_lines,
            'sales_order_count': list(sales_order_count),
        }
        return self.env.ref('task1.action_report_sales_order').report_action(self, data=data)

    def print_excel(self):

        domain_of_order_lines_for_customer = []
        sales_order_count = set()

        partner_id = self.partner_id
        from_date = self.from_date
        to_date = self.to_date

        if partner_id:
            domain_of_order_lines_for_customer += [('order_partner_id', '=', partner_id.id)]
        if from_date:
            domain_of_order_lines_for_customer += [('create_date', '>=', from_date)]

        if to_date:
            domain_of_order_lines_for_customer += [('create_date', '<=', to_date)]

        order_lines = self.env['sale.order.line'].search_read(domain_of_order_lines_for_customer)
        print('order_line with the range or All------------------', order_lines)
        for order_id in order_lines:
            if order_id['order_id'][1] not in sales_order_count:
                sales_order_count.add(order_id['order_id'][1])
        data = {
            'form_data': self.read()[0],
            'order_lines': order_lines,
            'sales_order_count': list(sales_order_count),

        }
        return self.env.ref('task1.report_sales_order_xls').report_action(self, data=data)

# [{'id': 12, 'order_id': (9, 'S00009'), 'name': '[FURN_0008] Small Shelf', 'sequence': 10, 'invoice_lines': [],
# 'invoice_status': 'no', 'price_unit': 2.83, 'price_subtotal': 141.5, 'price_tax': 0.0, 'price_total': 141.5,
# 'price_reduce': 2.83, 'tax_id': [], 'price_reduce_taxinc': 2.83, 'price_reduce_taxexcl': 2.83, 'discount': 0.0,
# 'product_id': (12, '[FURN_0008] Small Shelf'), 'product_template_id': (12, '[FURN_0008] Small Shelf'),
# 'product_updatable': True, 'product_uom_qty': 50.0, 'product_uom': (1, 'Units'), 'product_uom_category_id': (1,
# 'Unit'), 'product_uom_readonly': True, 'product_custom_attribute_value_ids': [],
# 'product_no_variant_attribute_value_ids': [], 'qty_delivered': 0.0, 'qty_delivered_manual': 0.0, 'qty_to_invoice':
# 0.0, 'qty_invoiced': 0.0, 'untaxed_amount_invoiced': 0.0, 'untaxed_amount_to_invoice': 0.0, 'salesman_id': (2,
# 'Administrator'), 'currency_id': (2, 'USD'), 'company_id': (1, 'Aumet'), 'order_partner_id': (7,
# 'Azure Interiors'), 'analytic_tag_ids': [], 'analytic_line_ids': [], 'is_expense': False, 'is_downpayment': False,
# 'state': 'sale', 'customer_lead': 0.0, 'display_type': False, 'sale_order_option_ids': [], 'purchase_line_ids': [],
# 'purchase_line_count': 0, 'qty_delivered_method': 'stock_move', 'product_packaging': False, 'route_id': False,
# 'move_ids': [12, 14, 16], 'product_type': 'product', 'virtual_available_at_date': 0.0, 'scheduled_date':
# datetime.datetime(2022, 3, 2, 8, 27, 39), 'forecast_expected_date': False, 'free_qty_today': 0.0,
# 'qty_available_today': 0.0, 'warehouse_id': (1, 'San Francisco'), 'qty_to_deliver': 50.0, 'is_mto': True,
# 'display_qty_widget': True, 'is_delivery': False, 'product_qty': 50.0, 'recompute_delivery_price': False,
# 'project_id': False, 'task_id': False, 'is_service': False, 'display_name': 'S00009 - [FURN_0008] Small Shelf',
# 'create_uid': (2, 'Administrator'), 'create_date': datetime.datetime(2022, 3, 2, 8, 25, 15, 885552), 'write_uid': (
# 2, 'Administrator'), 'write_date': datetime.datetime(2022, 3, 5, 17, 1, 27, 586786), '__last_update':
# datetime.datetime(2022, 3, 5, 17, 1, 27, 586786)},
# {'id': 13, 'order_id': (9, 'S00009'), 'name': '[FURN_0009] Wall
# Shelf Unit', 'sequence': 10, 'invoice_lines': [], 'invoice_status': 'no', 'price_unit': 1.98, 'price_subtotal':
# 59.4, 'price_tax': 0.0, 'price_total': 59.4, 'price_reduce': 1.98, 'tax_id': [], 'price_reduce_taxinc': 1.98,
# 'price_reduce_taxexcl': 1.98, 'discount': 0.0, 'product_id': (11, '[FURN_0009] Wall Shelf Unit'),
# 'product_template_id': (11, '[FURN_0009] Wall Shelf Unit'), 'product_updatable': True, 'product_uom_qty': 30.0,
# 'product_uom': (1, 'Units'), 'product_uom_category_id': (1, 'Unit'), 'product_uom_readonly': True,
# 'product_custom_attribute_value_ids': [], 'product_no_variant_attribute_value_ids': [], 'qty_delivered': 0.0,
# 'qty_delivered_manual': 0.0, 'qty_to_invoice': 0.0, 'qty_invoiced': 0.0, 'untaxed_amount_invoiced': 0.0,
# 'untaxed_amount_to_invoice': 0.0, 'salesman_id': (2, 'Administrator'), 'currency_id': (2, 'USD'), 'company_id': (1,
# 'Aumet'), 'order_partner_id': (7, 'Azure Interiors'), 'analytic_tag_ids': [], 'analytic_line_ids': [],
# 'is_expense': False, 'is_downpayment': False, 'state': 'sale', 'customer_lead': 0.0, 'display_type': False,
# 'sale_order_option_ids': [], 'purchase_line_ids': [], 'purchase_line_count': 0, 'qty_delivered_method':
# 'stock_move', 'product_packaging': False, 'route_id': False, 'move_ids': [13, 15, 17], 'product_type': 'product',
# 'virtual_available_at_date': 0.0, 'scheduled_date': datetime.datetime(2022, 3, 2, 8, 27, 39),
# 'forecast_expected_date': False, 'free_qty_today': 0.0, 'qty_available_today': 0.0, 'warehouse_id': (1,
# 'San Francisco'), 'qty_to_deliver': 30.0, 'is_mto': True, 'display_qty_widget': True, 'is_delivery': False,
# 'product_qty': 30.0, 'recompute_delivery_price': False, 'project_id': False, 'task_id': False, 'is_service': False,
# 'display_name': 'S00009 - [FURN_0009] Wall Shelf Unit', 'create_uid': (2, 'Administrator'), 'create_date':
# datetime.datetime(2022, 3, 2, 8, 25, 15, 885552), 'write_uid': (2, 'Administrator'), 'write_date':
# datetime.datetime(2022, 3, 5, 16, 45, 14, 231036), '__last_update': datetime.datetime(2022, 3, 5, 16, 45, 14,
# 231036)}]
