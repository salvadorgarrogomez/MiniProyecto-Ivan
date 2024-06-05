from odoo import models, fields, api
from odoo.exceptions import UserError
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
            raise UserError('No file data found.')
        file_content = base64.b64decode(self.file_data)
        file_content = file_content.decode('utf-8')
        csv_reader = csv.reader(StringIO(file_content), delimiter=',')
        header = next(csv_reader)
        duplicate_external_ids = []
        errors = []
        for row_number, row in enumerate(csv_reader, start=2):  # Empieza la lectura para insertar datos despues de la segunda linea
            # Se quitan los espacios en blanco
            row = list(map(str.strip, row))
            # Verificar si la fila tiene el número correcto de columnas
            if len(row) != len(header):
                errors.append(f"Row {row_number}: Incorrect number of columns.")
                continue
            vals = dict(zip(header, row))
            # Se ignoran las lineas en blanco
            if not any(vals.values()):
                continue
            external_id = vals.get('external_id')
            name = vals.get('name')
            # Se comprueba si los campos esenciales están presentes
            if not name:
                errors.append(f"Row {row_number}: Missing 'name'.")
                continue
            if external_id:
                # Comprobacion de si existe el id externo
                existing_partner = self.env['res.partner'].search([('external_id', '=', external_id)], limit=1)
                if existing_partner:
                    duplicate_external_ids.append(external_id)
                    continue
            try:
                self.env['res.partner'].create({
                    'name': name,
                    'phone': vals.get('phone', '').strip() if vals.get('phone') else '',
                    'email': vals.get('email', '').strip() if vals.get('email') else '',
                    'street': vals.get('street', '').strip() if vals.get('street') else '',
                    'city': vals.get('city', '').strip() if vals.get('city') else '',
                    'zip': vals.get('zip', '').strip() if vals.get('zip') else '',
                    'external_id': external_id.strip(),
                    'country_id': self.env['res.country'].search([('name', '=', vals.get('country', '').strip())], limit=1).id if vals.get('country') else None,
                })
            except Exception as e:
                errors.append(f"Row {row_number}: Error creating record - {str(e)}")

        if duplicate_external_ids or errors:
            error_message = "Some issues were encountered during the import:\n"
            if duplicate_external_ids:
                error_message += f"The following External IDs already exist and were not imported: {', '.join(duplicate_external_ids)}\n"
            if errors:
                error_message += "\n".join(errors)
            raise UserError(error_message)

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




