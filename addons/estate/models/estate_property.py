from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Date Availability',
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=+3)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])

    active = fields.Boolean(string='Active', default=True)

    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_refused', 'Offer Refused'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        required=True,
        copy=False,
        default='new',
        compute='_compute_state',
        store=True,
    )

    from odoo import models, fields, api

    # class EstateProperty(models.Model):
    #     _inherit = 'estate.property'

    @api.depends('offer_ids.status', 'selling_price', 'state')
    def _compute_state(self):
        for record in self:
            # Do not override if sold or cancelled
            if record.state in ['sold', 'cancelled']:
                continue

            accepted_offers = record.offer_ids.filtered(lambda o: o.status == 'offer_accepted')
            refused_offers = record.offer_ids.filtered(lambda o: o.status == 'offer_refused')
            
            if accepted_offers:
                record.state = 'offer_accepted'
            elif refused_offers:
                record.state = 'offer_refused'
            elif record.offer_ids:
                record.state = 'offer_received'
            else:
                record.state = 'new'


    is_sold = fields.Boolean(
        string='Is Sold',
        compute='_compute_is_sold',
        store=True
    )

    @api.depends('state')
    def _compute_is_sold(self):
        for record in self:
            record.is_sold = record.state == 'sold'

    offer_received = fields.Boolean(
        string='Offer Received',
        compute='_compute_offer_status',
        store=True,
    )

    offer_accepted = fields.Boolean(
        string='Offer Accepted',
        compute='_compute_offer_status',
        store=True,
    )

    @api.depends('offer_ids.status')
    def _compute_offer_status(self):
        for property in self:
            offers = property.offer_ids
            property.offer_received = bool(offers)
            property.offer_accepted = any(offer.status == 'offer_accepted' for offer in offers)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False,
    )

    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
    )

    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string= 'Tag',
    )

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers') 

    total_area = fields.Float(string='Total Area', compute='_compute_total_area', store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0.0) + (record.garden_area or 0.0)

    best_price = fields.Float(string='Best Offer Price', compute='_compute_best_price', store=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                # fallback if create_date not set yet
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days if delta.days >= 0 else 0
            else:
                offer.validity = 7  # fallback default

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False    

    def button_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("You cannot cancel a sold property."))
            record.state = 'cancelled'

    def button_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("You cannot mark a cancelled property as sold."))
            record.state = 'sold'

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive or zero.'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_vs_expected_price(self):
        for record in self:
            # If selling price is zero, skip the check (not validated yet)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            # Minimum allowed selling price is 90% of expected price
            min_price = record.expected_price * 0.9

            # Compare selling_price with min_price
            # float_compare returns:
            #   -1 if first < second
            #    0 if equal
            #    1 if first > second
            if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                raise ValidationError(_(
                    "The selling price cannot be lower than 90%% of the expected price.\n"
                    "Minimum allowed: %.2f, current selling price: %.2f"
                ) % (min_price, record.selling_price))

    sequence = fields.Integer(string='Sequence', default=10)

    @api.ondelete(at_uninstall = False)
    def _check_deletion_state(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(
                    f"You cannot delete property '{record.name}' unless it is in 'New' or 'Cancelled' state."
                )

    def action_print_property_offers(self):
        return self.env.ref('estate.action_report_property_offers').report_action(self)
