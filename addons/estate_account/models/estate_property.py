from odoo import models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def button_sold(self):
        # Debug statement to verify override works
        print("Hello World!!!")

        res = super().button_sold()
        return res
