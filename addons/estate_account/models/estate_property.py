from odoo import models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # Debug statement to verify override works
        print("action_sold overridden in estate_account")

        res = super().action_sold()
        return res
