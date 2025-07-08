from odoo import models, fields

class CustomWebsiteForm(models.Model):
    _name = 'website.custom.form'
    _description = 'Custom Website Form'

    borrower = fields.Char(string="Borrower")
    loan_amount = fields.Float(string="Loan Amount")
    monthly_income = fields.Float(string="Monthly Income")
    cibil = fields.Float(string="CIBIL Score")
    bank_name = fields.Char(string="Bank Name")
    purpose = fields.Char(string="Purpose")
    address = fields.Char(string="Address")
