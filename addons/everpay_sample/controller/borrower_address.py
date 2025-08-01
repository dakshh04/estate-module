from odoo import models, fields

class BorrowerAddress(models.Model):
    _name = 'nbfc.borrower.address'
    _description = 'Borrower Address'

    address = fields.Char(string='Address')
    type = fields.Char(string='Type')  # e.g., 'home', 'work', etc.
    is_verified = fields.Boolean(string='Is Verified')

    # lead_id = fields.Many2one('nbfc.lead', string='Lead', ondelete='cascade')
