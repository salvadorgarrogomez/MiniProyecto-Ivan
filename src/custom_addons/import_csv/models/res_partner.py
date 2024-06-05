from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    external_id = fields.Char(
        string='External Id',
        )