from odoo import api, models, fields, _


class SearchPurchaseWizard(models.TransientModel):
    _name = 'search.purchase.wizard'
    _description = 'Model to search purchase wizard'
    partner_id = fields.Many2one(
        'res.partner', string='Vendor',
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
            domain_of_order_lines_for_customer += [('partner_id', '=', partner_id.id)]
        if from_date:
            domain_of_order_lines_for_customer += [('date_order', '>=', from_date)]

        if to_date:
            domain_of_order_lines_for_customer += [('date_order', '<=', to_date)]

        order_lines = self.env['purchase.order.line'].search_read(domain_of_order_lines_for_customer)

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
        print('data-------------->',data)
        return self.env.ref('task1.action_report_purchase_order').report_action(self, data=data)


    def print_excel(self):
        domain_of_order_lines_for_customer = []
        sales_order_count = set()
        partner_id = self.partner_id
        from_date = self.from_date
        to_date = self.to_date

        if partner_id:
            domain_of_order_lines_for_customer += [('partner_id', '=', partner_id.id)]
        if from_date:
            domain_of_order_lines_for_customer += [('date_order', '>=', from_date)]

        if to_date:
            domain_of_order_lines_for_customer += [('date_order', '<=', to_date)]

        order_lines = self.env['purchase.order.line'].search_read(domain_of_order_lines_for_customer)

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
        print('data-------------->', data)
        return self.env.ref('task1.report_purchase_orders_xls').report_action(self, data=data)




