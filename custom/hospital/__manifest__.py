{
    'name': 'Hospital Management',
    'version': '1.1',
    'summary': 'Hospital management',
    'sequence': 10,
    'description': """Hospital management""",
    'category': 'Productivity/Discuss',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['sale',
                'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_wizard.xml',
        'wizard/search_appointment_view.xml',
        'views/patient_view.xml',
        'views/sale_view.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'report/patient_details_template.xml',
        'report/patient_card.xml',
        'report/report.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
