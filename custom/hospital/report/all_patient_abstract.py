from odoo import api, fields, models, tools


class AllPatientReport(models.AbstractModel):
    # report.moduleName.report.template
    _name = 'report.hospital.report_all_patient_list'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        # 'form_data' from all_patient_report.py in wizard it's dict contains all the fields
        gender = data.get('form_data').get('gender')
        age = data.get('form_data').get('age')
        if gender:
            domain += [('gender', '=', gender)]
        if age != 0:
            domain += [('age', '=', age)]

        docs = self.env['hospital.patient'].search(domain)

        print(docs)
        return {
            'docs': docs,
        }


class PatientReport(models.AbstractModel):
    # report.moduleName.templateId
    _name = 'report.hospital.report_patient_details'
    _description = 'Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # browse(docids) == search([('id', '=', docids)]) get value for specific record.
        docs = self.env['hospital.patient'].browse(docids)

        print(docs)
        return {
            'docs': docs,
        }
