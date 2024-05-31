{
    "name": "Vertical Agro",
    "version": "17.0.1.0.0",
    "category": "Custom",
    "license": "LGPL-3",
    "depends": [
        # Odoo
        "contacts",
        "account",
        "stock",
        "base",
        "base_address_extended",
        # Oca
        "web_responsive",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/agricultural_holding_views.xml",
        "views/plantation_views.xml",
        "views/farm_views.xml",
        "views/seedbed_views.xml",
        "views/agro_menus_views.xml",
    ],
}
