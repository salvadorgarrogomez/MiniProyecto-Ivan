from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    to_review = fields.Boolean(string='To Review', default=False)
