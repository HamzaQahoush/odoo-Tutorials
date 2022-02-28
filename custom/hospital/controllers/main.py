from odoo import http
from odoo.http import request


class Hospital(http.Controller):
    @http.route('/hospital1/', auth='public', type='http', website=True)
    def hospital_patient(self, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        print('=------------patients' , patients)
        # to render template ('moduleName.templateID'
        return request.render('hospital.patient_page_template', {'patients': patients})
