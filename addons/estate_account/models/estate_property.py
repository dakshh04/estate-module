from odoo import models
import logging
_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def button_sold(self):
        print("Hello World!!!")
        _logger.info("Hello World!!! - button_sold override triggered")

        res = super().button_sold()

        for property in self:
            if property.buyer_id:
                _logger.info(f"Creating invoice for property {property.name} and partner {property.buyer_id.name}")

                selling_price = property.selling_price or 0.0
                commission = selling_price * 0.06
                admin_fee = 100.0

                self.env['account.move'].create({
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        (0, 0, {
                            'name': f"6% Commission for {property.name}",
                            'quantity': 1,
                            'price_unit': commission,
                        }),
                        (0, 0, {
                            'name': "Administrative Fees",
                            'quantity': 1,
                            'price_unit': admin_fee,
                        }),
                    ],
                })
            else:
                _logger.warning(f"Property {property.name} has no buyer; skipping invoice creation.")

        return res
