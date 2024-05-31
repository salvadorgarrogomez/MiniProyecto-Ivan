from odoo import api, fields, models


class Plantation(models.Model):
    _name = "plantation"
    _description = "Plantation"

    code = fields.Char(string="Código", required=True)
    name = fields.Char(string="Nombre", required=True, store=True)
    notes = fields.Text(store=True)
    estate_id = fields.Many2one(comodel_name="farm", string="Finca (UPA)", store=True)
    explotation_id = fields.Many2one(
        comodel_name="agricultural.holding", string="Explotación", store=True
    )
    origin = fields.Char(string="Documento origen", store=True)
    plants_qty_planned = fields.Integer(
        string="Número de plantas previstas", store=True
    )
    plants_qty = fields.Integer(string="Número de plantas plantadas", store=True)
    plants_qty_planned_planted = fields.Float(
        string="Número de plantas previstas/plantadas",
        compute="_compute_plants_qty_planned_planted",
        store=True,
        digits=(10, 2),
    )
    real_size = fields.Float(
        string="Superficie plantada (real medida)", digits=(10, 4), store=True
    )
    production_prevision = fields.Float(
        string="Previsión de producción en Kg:", digits=(10, 4), store=True
    )
    production = fields.Float(string="Producción", digits=(10, 4), store=True)
    prevision_production = fields.Float(
        string="Previsión/Producción",
        compute="_compute_productions",
        store=True,
        digits=(10, 4),
    )
    production_start = fields.Date(string="Fecha de inicio de producción")
    date_deadline = fields.Date(string="Fecha de plazo de seguridad")
    end_date = fields.Date(string="Fecha fin producción", store=True)
    plannes_planting_date = fields.Date(
        string="Fecha prevista de plantación", store=True
    )
    planned_harvesting_date = fields.Date(
        string="Fecha prevista de recolección", store=True
    )
    no_waste_date = fields.Date(string="Fecha sin residuo", store=True)
    ipm_type = fields.Selection(
        [
            ("adviser", "Asistida de un asesor"),
            ("expert", "Asistida de un perito"),
        ],
        string="Gestión Integrada de Plagas",
        store=True,
    )
    status = fields.Selection(
        [
            ("draft", "Borrador"),
            ("transplanting", "Transplante"),
            ("growing", "En cultivo"),
            ("ready_to_harvest", "Listo para recolectar"),
            ("harvesting", "En recolección"),
            ("collected", "Recolectado"),
        ],
        string="Estado",
    )
    landlord_id = fields.Many2one(
        comodel_name="res.partner",
        string="Arrendador",
        store=True,
    )
    message_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Seguidores (Contactos)",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Socio",
        store=True,
    )
    activity_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible User ",
    )
    activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Next Activity Type",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        store=True,
    )
    message_main_attachment_id = fields.Many2one(
        comodel_name="ir.attachment",
        string="Adjunto principal",
        store=True,
    )
    production_uom = fields.Char(
        string="Unidad de medida",
        default="ha",
    )

    # Revisar mas tarde esto es un Many2one con ags.agro.farming
    farming_id = fields.Char(string="Cultivo")

    # Revisar mas tarde esto debe de ser un One2many con ags.agro.field.irrigation_sector
    field_irrigation_sector_ids = fields.Char(string="Sectores")

    # Revisar mas tarde, es un Many2one con ags.agro.farming.planting_network
    planting_framework_id = fields.Char(string="Marco de plantación")

    # Revisar mas tarde, es un Many2many con ags.certificate.certificate
    certificate_ids = fields.Char(string="Certificado")

    # Revisar las mas tarde, es un Many2one con ags.agro.cycle
    cycle_id = fields.Char(string="Periodo")

    # Revisar mas tarde, es un Many2one con ags.agro.field.group
    group_id = fields.Char(string="Agrupación")

    # No estan en los campos de las capturas
    seed = fields.Char(string="Variedad/Semilla")
    area = fields.Float(string="Superficie (ha)", digits=(10, 4))
    previst_teoric = fields.Float(
        string="Superficie prevista (teorica)", digits=(10, 4)
    )
    planted_teoric = fields.Float(
        string="Superficie plantada (teorica)", digits=(10, 4)
    )
    campaign = fields.Char(string="Campaña")
    type_irrigation = fields.Char(string="Tipo de riego")
    test = fields.Boolean(string="Ensayo")
    plantula = fields.Char(string="Plántula")

    @api.depends("plants_qty_planned", "plants_qty")
    def _compute_plants_qty_planned_planted(self):
        for record in self:
            if record.plants_qty_planned != 0:
                percentage = record.plants_qty / record.plants_qty_planned
                record.plants_qty_planned_planted = round(percentage, 2)
            else:
                record.plants_qty_planned_planted = 0.00

    @api.depends("production_prevision", "production")
    def _compute_productions(self):
        for record in self:
            if record.production_prevision != 0:
                percentage = record.production / record.production_prevision
                record.prevision_production = round(percentage, 2)
            else:
                record.prevision_production = 0.00
