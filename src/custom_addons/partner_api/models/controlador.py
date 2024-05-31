from odoo import http
from odoo.http import request

class PartnerAPIController(http.Controller):

    @http.route('/test/partner', type='http', auth='public', methods=['GET'], csrf=False)
    def create_partner(self, name=None, phone=None):
        if name and phone:
            partner = request.env['res.partner'].sudo().create({
                'name': name,
                'phone': phone,
                'to_review': True,
                'active': True
            })
            return "Partner created: %s" % partner.name
        return "Name and phone are required"

