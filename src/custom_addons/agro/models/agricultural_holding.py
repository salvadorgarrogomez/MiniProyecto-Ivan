from odoo import api, fields, models


class AgriculturalHolding(models.Model):
    _name = "agricultural.holding"
    _description = "Set of farms with their related equipment and seedbedsy"

    name = fields.Char(string="Nombre", required=True)
    cadastral_size = fields.Float(string="Superficie catastral", digits=(10, 4))
    tillable_size = fields.Float(string="Superficie cultivable", digits=(10, 4))
    create_date = fields.Date(string="Fecha de alta")
    leave_date = fields.Date(string="Fecha de baja")
    farm_ids = fields.One2many(
        comodel_name="farm", inverse_name="exploitation_id", string="Fincas"
    )
    owner = fields.Many2one(comodel_name="res.partner", string="Titular")
    manager = fields.Many2one(comodel_name="res.partner", string="Gerente")
    notes = fields.Text(string="Notas")

    @api.onchange("name")
    def _onchange_name(self):
        if self.name:
            # Crear un nuevo res.partner con el nombre ingresado
            partner = self.env["res.partner"].create({"name": self.name})
            # Asignar el nuevo socio al campo many2one
            self.owner = partner.id
            self.manager = partner.id
