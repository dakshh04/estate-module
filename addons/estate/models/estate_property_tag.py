from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _sql_constraints = [
        ('tag_name_unique', 'UNIQUE(name)', 'The tag name must be unique.'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer(string='Color')
