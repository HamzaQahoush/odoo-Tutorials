from odoo import api, models, fields, _


class SearchPurchaseWizard(models.TransientModel):
    _name = 'search.purchase.wizard'
    _description = 'Model to search purchase wizard'

    from_date = fields.Datetime('Date From')
    to_date = fields.Datetime('Date To')

    def print_pdf(self):
        pass

    def print_excel(self):
        pass


