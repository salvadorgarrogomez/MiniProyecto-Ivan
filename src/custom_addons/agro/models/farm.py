from odoo import fields, models


class Farm(models.Model):
    _name = "farm"
    _description = "This is a farm for the agricultural proyect"

    name = fields.Char(string="Nombre", required=True)
    address_id = fields.Many2one(comodel_name="res.partner", string="Dirección")
    cadastral_size = fields.Float(string="Superficie Catastral (ha)", digits=(10, 4))
    city = fields.Char("City Name")

    # no pongo string aqui por que el string formaria una redundancia a la hora de hacer pre-commits y subirlo a GitLab
    color = fields.Integer()
    company_id = fields.Many2one(comodel_name="res.company", string="Compañía")
    cor = fields.Char(string="Coordenadas")
    exploitation_id = fields.Many2one(
        comodel_name="agricultural.holding",
        string="Explotación",
    )
    exploitation_systems = fields.Selection(
        [
            ("to_exploit", "Por explotar"),
            ("exploding", "Explotando"),
            ("already_exploited", "Ya explotado"),
        ],
        string="Sistema de Explotación",
    )

    # no pongo string aqui por que este formaria una redundancia a la hora de hacer pre-commits y subirlo a GitLab
    fields_count = fields.Integer()
    holder_id = fields.Many2one(comodel_name="res.partner", string="Holder")
    landlord_id = fields.Many2one(comodel_name="res.partner", string="Arrendador")

    # no pongo string aqui por que este formaria una redundancia a la hora de hacer pre-commits y subirlo a GitLab
    localization_count = fields.Integer()
    notes = fields.Text("Notas")
    partnert_id = fields.Many2one(comodel_name="res.partner", string="Productor")

    # no pongo string aqui por que este formaria una redundancia a la hora de hacer pre-commits y subirlo a GitLab
    pieces_count = fields.Integer()
    property_other = fields.Boolean("Propiedad Ajena")

    # no pongo string aqui por que este formaria una redundancia a la hora de hacer pre-commits y subirlo a GitLab
    sectors_count = fields.Integer()
    state_id = fields.Many2one(comodel_name="res.country.state", string="Provincia")
    street = fields.Char("Calle")
    tenure_regime_code = fields.Char("Código")
    tillable_size = fields.Float(string="Superficie Cultivable (ha)", digits=(10, 4))
    zip = fields.Char(string="Código Postal")

    # analytic_account_id con el string:"Cuenta Analitica" es una relacion many2one del modelo account.analytic.account del que no disponemos (facturacion)
    # certificate_ids con el string:"Certificado" es una relacion one2many del modelo ags.certificate.certificate (posible oca)
    # city_id no puedo ponerlo por que tenemos que instalar el módulo que instala res.city (a mirar)
    # contracts_id es de un modelo que no tenemos ags.agro.contract
    # fields_id con string "Plantaciones (UHC)" es de un modelo (agro/field) que no hemos creado
    # irrigation_sector_ids relacion one2many a un modelo que no hemos creado (agro.irrigation_sector)
    # en el word last_update aparece como "_last_update" pero lo dejare sin la "_" del principio de momento _last_update = fields.Date(string="Last Modified on")
    # location_id deberia ser un many2one a Stock.location un modelo que no disponemos y que creo que se instala con un módulo propio de Odoo por el momento se quedara sin poner para evitar posibles errores (preguntare mas tarde a Ivan)
    # pieces_id con string ="Recinto (DG)" es una relacion one2many a un modelo que no tenemos (agro.localization.piece)
    # localization_ids es un campo many2one a un modelo que no tenemos (agro.localization)
    # tenure_regime_id es un campo many2one en relacion a un modelo que no tenemos (agro.tenure_regime)
    # the_geom es un campo que representa un mapa y que de momento no vamos a usar
    # the_geom_display lo mismo que the_geom, no lo usaremos de momento
    # zone_id pertenece a una relacion many2one a un modelo que no tenemos (agro.zone)
