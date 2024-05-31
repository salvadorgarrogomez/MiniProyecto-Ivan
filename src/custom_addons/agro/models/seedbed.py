from odoo import fields, models


class Seedbed(models.Model):
    _name = "seedbed"
    _description = "Seedbed Model"

    name = fields.Char(string="Nombre")
    sectors_size = fields.Float(string="Superficie sectores", digits=(10, 4))
    partner_id = fields.Many2one(comodel_name="res.partner", string="Propietario")
    ciudad_id = fields.Many2one(comodel_name="res.city", string="Ciudad")
    exploitation_id = fields.Many2one(
        comodel_name="agricultural.holding", string="Explotación"
    )
