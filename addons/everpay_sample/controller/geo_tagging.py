from odoo import models, fields

class GeoTagging(models.Model):
    _name = 'nbfc.geo_tagging'
    _description = 'Geo Tagging'

    latitude = fields.Float(string='Latitude', digits=(12, 8))
    longitude = fields.Float(string='Longitude', digits=(12, 8))
    accuracy = fields.Float(string='Accuracy (meters)')
    address = fields.Char(string='Address')
