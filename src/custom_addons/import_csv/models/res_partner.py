import base64
import csv
from io import StringIO
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    external_id = fields.Char(
        string='External Id',
        )
    
    def action_download_contacts_csv(self):
        # Se definen todos los header o nombres de columnas
        headers = ['external_id', 'name', 'phone', 'email', 'street', 'city', 'zip', 'country']
        
        # Se recopilan los datos del registro de partner actual.
        partner_data = [{
            'external_id': self.external_id or '',
            'name': self.name or '',
            'phone': self.phone or '',
            'email': self.email or '',
            'street': self.street or '',
            'city': self.city or '',
            'zip': self.zip or '',
            'country': self.country_id.name if self.country_id else ''
        }]
        
        # Creacion del csv con los datos
        csv_file = StringIO()
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()
        csv_writer.writerows(partner_data)
        
        # Preparacion del archivo para su descarga
        csv_content = csv_file.getvalue()
        csv_file.close()
        
        file_base64 = base64.b64encode(csv_content.encode('utf-8'))
        
        # Crea un archivo adjunto con el archivo CSV
        attachment = self.env['ir.attachment'].create({
            'name': f'partner_{self.id}_contacts.csv',
            'type': 'binary',
            'datas': file_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'text/csv'
        })
        
        # Devuelve la acción para descargar el archivo.
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }