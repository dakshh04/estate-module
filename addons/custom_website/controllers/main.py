from odoo import http
from odoo.http import request

class CustomWebsiteFormController(http.Controller):

    @http.route(['/custom-form'], type='http', auth="public", website=True)
    def show_form(self, **kwargs):
        return request.render('custom_website.custom_website_form', {})

    @http.route(['/submit/custom/form'], type='http', auth="public", methods=['POST'], csrf=True, website=True)
    def handle_form(self, **post):
        request.env['website.custom.form'].sudo().create({
            'borrower': post.get('borrower'),
            'loan_amount': post.get('loan_amount'),
            'monthly_income': post.get('monthly_income'),
            'cibil': post.get('cibil'),
            'bank_name': post.get('bank_name'),
            'purpose': post.get('purpose'),
            'address': post.get('address'),
        })
        return request.redirect('/custom-form?submitted=1')

