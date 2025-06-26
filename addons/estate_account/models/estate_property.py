from odoo import models
import logging
_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def is_sold(self):
        # Debug statement to verify override works
        print("Hello World!!!")
        _logger.info("Hello World!!! - is_sold override triggered")

        res = super(EstateProperty, self).is_sold()
        return res
