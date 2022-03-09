from odoo import models


class CustomerSalesXlsx(models.AbstractModel):
    _name = 'report.task1.report_customer_sales_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partner_id):
        print('data[order_lines]------------------------>', data['order_lines'])
        print('data[form_data]--------------------------->', data['form_data'])
        print('data[sales_order_count]--------------------------->', data['sales_order_count'])
        order_lines = data['order_lines']
        form_data = data['form_data']
        sales_order_count = sorted(data['sales_order_count'])
        print(sales_order_count)
        required_order_lines = []

        # To clean data from order lines and show it as required
        for i in order_lines:
            required_order_lines.append(
                {'Description': i.get('name', None), "Quantity": i.get('product_uom_qty', None),
                 'Unit Price': i.get('price_unit', None), 'Price Tax': i.get('price_tax', None),
                 "Price Subtotal": i.get('price_subtotal', None), "order_id": i['order_id'][1],

                 })
        print(required_order_lines)
        all_keys = ['Description', "Quantity", "Unit Price", "Price Tax", "Price Subtotal", 'order_id']
        sorted_required_order_lines = sorted(required_order_lines, key=lambda d: d['order_id'])
        print('sorted_required_order_lines---------', sorted_required_order_lines)
        header_data = {}

        # loop over Form data to get it ,to  store ,render it .
        header_data.update(
            [('Customer', form_data.get('partner_id')[1] if form_data.get('partner_id') else None),
             ('Date From', form_data.get('from_date', None)),
             ('To Date', form_data.get('to_date', None))])
        print('header_data------------->', header_data)

        # loop over all sales order
        for rec in sales_order_count:
            bold = workbook.add_format({'bold': True})
            sheet = workbook.add_worksheet(f'customer_sale_order# {rec}')
            sheet.set_column('B:F', 12)
            sheet.set_column('A:B', 30)

            sheet.set_row(0, 30)
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': 'b7e4c7'})
            sheet.merge_range('B1:D1', 'Sale Order Details ', merge_format)

            # to get order ID and show it in Excel , cause it not provided from wizard:
            for id in order_lines:
                if rec == id['order_id'][1]:
                    r, c = 5, 0
                    sheet.write(r, c, 'Sale Order ID', bold)
                    sheet.write(r, c + 1, id['order_id'][1])

            # to write headers and its value of sheet
            for y, (name, info) in enumerate(header_data.items(), start=2):
                sheet.write(y, 0, name, bold)
                sheet.write(y, 1, info)

            # to write table headers and its data
            row = 8
            for header in required_order_lines:
                for col, (k, v) in enumerate(header.items(), start=0):
                    sheet.write(row, col, k, bold)
            row = 9
            for order in sorted_required_order_lines:
                print('order-----------', order)
                if order.get('order_id') == rec:
                    for _key, _value in order.items():
                        col = all_keys.index(_key)
                        sheet.write(row, col, _value)
                    row += 1  # enter the next row
