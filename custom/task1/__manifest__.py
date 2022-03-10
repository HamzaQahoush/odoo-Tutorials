{
    'name': 'check sales order',
    'version': '1.1',
    'summary': '',
    'sequence': 10,
    'description': """add button to check sales order""",
    'category': 'Sales',
    'website': '',
    'depends': ['sale',
                'purchase',
                'report_xlsx'
                ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/search_customer_view.xml',
        'wizard/search_purchase.xml',
        'report/report.xml',
        'report/sales_order.xml',
        'report/purchase_order.xml',
        'views/menu.xml',
        'views/quotation_view.xml',



        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}