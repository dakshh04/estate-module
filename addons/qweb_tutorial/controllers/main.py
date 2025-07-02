from odoo import http

class QwebTutorials(http.Controller):
    @http.route('/qweb_tutorials', type='http', auth='public')
    def qweb_tutorials(self):

        return http.request.render("qweb_tutorial.somePythonTemplate")

