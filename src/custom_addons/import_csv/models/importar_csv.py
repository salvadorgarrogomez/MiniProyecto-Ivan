from odoo import models, fields, api
import csv
import base64
from io import StringIO

class ImportContactsWizard(models.TransientModel):
    _name = 'import.contacts.wizard'
    _description = 'Import Contacts Wizard'

    file_data = fields.Binary('CSV File', required=True)
    file_name = fields.Char('File Name')

    def import_contacts(self):
        self.ensure_one()
        if not self.file_data:
            return
        
        file_content = base64.b64decode(self.file_data)
        file_content = file_content.decode('utf-8')
        
        csv_reader = csv.reader(StringIO(file_content), delimiter=',')
        header = next(csv_reader)
        
        for row in csv_reader:
            vals = dict(zip(header, row))
            if vals.get('name'): 
                self.env['res.partner'].create({
                    'name': vals.get('name'),
                    'phone': vals.get('phone'),
                    'email': vals.get('email'),
                    'street': vals.get('street'),
                    'city': vals.get('city'),
                    'zip': vals.get('zip'),
                    'country_id': self.env['res.country'].search([('name', '=', vals.get('country'))], limit=1).id,
                })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Import Completed',
                'message': 'Contacts have been imported successfully.',
                'type': 'success',
                'sticky': False,
            }
        }

