from odoo import models, fields, api
from odoo.exceptions import UserError
import csv
import base64
import re
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

        # Definición de expresiones regulares
        numeric_regex = re.compile(r'^\d+$')
        alphabetic_regex = re.compile(r'^[a-zA-Z\s]+$')

        for row_number, row in enumerate(csv_reader, start=2):  # Empieza la lectura para insertar datos después de la segunda línea
            # Se quitan los espacios en blanco
            row = list(map(str.strip, row))
            # Verificar si la fila tiene el número correcto de columnas
            if len(row) != len(header):
                errors.append(f"Row {row_number}: Incorrect number of columns.")
                continue
            vals = dict(zip(header, row))
            # Se ignoran las líneas en blanco
            if not any(vals.values()):
                continue

            external_id = vals.get('external_id')
            name = vals.get('name')
            phone = vals.get('phone')
            email = vals.get('email')
            street = vals.get('street')
            city = vals.get('city')
            zip_code = vals.get('zip')
            country = vals.get('country')

            # Se comprueba si los campos esenciales están presentes
            if not name:
                errors.append(f"Row {row_number}: Missing 'name'.")
                continue
            
            if name and not alphabetic_regex.match(name):
                errors.append(f"Row {row_number}: Name must contain only alphabetic characters.")
                continue

            # Validaciones de campos específicos
            if phone and not numeric_regex.match(phone):
                errors.append(f"Row {row_number}: Phone must be numeric.")
                continue

            if zip_code and not numeric_regex.match(zip_code):
                errors.append(f"Row {row_number}: ZIP must be numeric.")
                continue

            if city and not alphabetic_regex.match(city):
                errors.append(f"Row {row_number}: City must contain only alphabetic characters.")
                continue

            if external_id:
                # Comprobación de si existe el id externo
                existing_partner = self.env['res.partner'].search([('external_id', '=', external_id)], limit=1)
                if existing_partner:
                    duplicate_external_ids.append(external_id)
                    continue
            try:
                self.env['res.partner'].create({
                    'name': name,
                    'phone': phone if phone else '',
                    'email': email if email else '',
                    'street': street if street else '',
                    'city': city if city else '',
                    'zip': zip_code if zip_code else '',
                    'external_id': external_id.strip() if external_id else '',
                    'country_id': self.env['res.country'].search([('name', '=', country.strip())], limit=1).id if country else None,
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




