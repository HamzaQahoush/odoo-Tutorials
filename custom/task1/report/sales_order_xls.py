from odoo import models
import base64
import io


class CustomerSalesXlsx(models.AbstractModel):
    _name = 'report.task1.report_customer_sales_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partner_id):
        print('data[order_lines]------------------------>', data['order_lines'])
        print('data[form_data]--------------------------->', data['form_data'])
        print('data[sales_order_count]--------------------------->', data['sales_order_count'])
        order_lines = data['order_lines']
        form_data = data['form_data']
        sales_order_count = data['sales_order_count']
        required_order_lines = []
        for i in order_lines:
            required_order_lines.append(
                {'Description': i.get('name', None), "Quantity": i.get('product_uom_qty', None),
                 'Unit Price': i.get('price_unit', None), 'Price Tax': i.get('price_tax', None),
                 "Price Subtotal": i.get('price_subtotal', None),

                 })
        print(required_order_lines)
        # ids = []

        header_data = {}
        header_data.update(
            [('Customer', form_data.get('partner_id')[1] if form_data.get('partner_id') else None),
             ('Date From', form_data.get('from_date', None)),
             ('To Date', form_data.get('to_date', None))])
        print('header_data------------->', header_data)
        for rec in sales_order_count:
            bold = workbook.add_format({'bold': True})
            sheet = workbook.add_worksheet(f'Customer Sale order xls{rec}')
            sheet.set_column('B:D', 12)
            sheet.set_row(0, 30)
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'fg_color': '#00FF00'})
            sheet.merge_range('B1:D1', 'Sale Order Details ', merge_format)

            # ids += [d['order_id'][1] for d in order_lines if 'order_id' in d]
            # unique_ids = list(set(ids))
            # print('ids..........', ids)

            for id in order_lines:
                if rec == id['order_id'][1]:
                    r, c = 5, 0
                    sheet.write(r, c, 'Sale Order ID')
                    sheet.write(r, c + 1, id['order_id'][1])

            for y, (name, info) in enumerate(header_data.items(), start=2):
                sheet.write(y, 0, name)
                sheet.write(y, 1, info)

            for i in order_lines:
                for j, (k, v) in enumerate(i.items(), start=9):
                    print(f'j-------> {j}', f'k---{k}', f'v----{v}')

            # sheet.set_column('D:D', 12)
    # row, col = 0, 0
    # sheet.write(row, col, 'ref' ,bold)
    # sheet.write(row, col + 1, 'patient ID', bold)
    # for rec in data['appointments']:
    #     row += 1
    #     sheet.write(row, col, rec['ref'])
    #     sheet.write(row, col+1, rec['patient_id'][1])
