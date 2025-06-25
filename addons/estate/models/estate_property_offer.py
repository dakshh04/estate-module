from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Offer Price')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('offer_accepted', 'Offer Accepted'),
        ('offer_refused', 'Offer Refused'),
    ], default='pending', copy=False, string='Status')
    
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', ondelete="set null")
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True
    )

    check = fields.Boolean(string="check", default=True)

    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    def button_accept(self):
        for offer in self:
            if offer.status != 'pending':
                continue  # Only accept pending offers

            # Accept this offer
            offer.status = 'offer_accepted'
            offer.check = False

            # Update property info
            estate_property = offer.property_id
            estate_property.buyer_id = offer.partner_id
            estate_property.selling_price = offer.price
            estate_property.state = 'offer_accepted'  # Update property state

            # Refuse all other pending offers for this property
            other_offers = self.search([
                ('property_id', '=', estate_property.id),
                ('id', '!=', offer.id),
                ('status', '=', 'pending')
            ])
            for other in other_offers:
                other.status = 'offer_refused'
                other.check = False

    def button_refuse(self):
        for offer in self:
            if offer.status != 'pending':
                continue  # Only refuse pending offers

            offer.status = 'offer_refused'
            offer.check = False

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        new_offer_price = vals.get('price')

        if property_id and new_offer_price:
            # Check if there's already an accepted offer
            accepted_offer = self.search([
                ('property_id', '=', property_id),
                ('status', '=', 'offer_accepted')
            ], limit=1)
            if accepted_offer:
                raise exceptions.UserError("An offer has already been accepted for this property.")

            # Check if the new offer is lower than existing ones
            existing_offers = self.search([
                ('property_id', '=', property_id)
            ])
            max_price = max(existing_offers.mapped('price'), default=0)
            if new_offer_price < max_price:
                raise ValidationError(
                    f"New offer ({new_offer_price:.2f}) must be at least equal to the highest existing offer ({max_price:.2f})."
                )

        return super().create(vals)

