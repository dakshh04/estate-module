from odoo import models, fields

class BorrowerBankAccount(models.Model):
    _name = 'nbfc.borrower.bank.account'
    _description = 'Borrower Bank Account'

    bank = fields.Char(string='Bank')
    account_number = fields.Char(string='Account Number')
    ifsc = fields.Char(string='IFSC Code')
