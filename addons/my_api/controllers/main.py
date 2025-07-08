from odoo import http
from odoo.http import request
import json

class MyAPIController(http.Controller):

    @http.route('/api/partners', type='json', auth='public', methods=['POST'], csrf=False)
    def get_partners(self, **kwargs):
        token = request.httprequest.headers.get('Authorization')
        if token != 'Bearer my-secret-token':
            return {'error': 'Unauthorized'}, 401

        partners = request.env['res.partner'].sudo().search([])
        return [{
            'id': partner.id,
            'name': partner.name,
            'email': partner.email,
        } for partner in partners]

