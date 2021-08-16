# Copyright 2021, Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = 'id desc'

    name = fields.Char(
        required=True,
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(
            fields.Date.today(), months=+3),
    )
    expected_price = fields.Float(
        required=True,
    )
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(
        default=True,
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
        copy=False,
    )
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        ondelete='restrict',
    )
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        copy=False,
    )
    seller_id = fields.Many2one(
        comodel_name='res.users',
        default=lambda self: self.env.user,
        string='Salesman',
    )
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string="Tags",
    )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
    )
    total_area = fields.Float(
        compute='_compute_total_area',
    )
    best_price = fields.Float(
        compute='_compute_best_price',
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Property name already exist!'),
        ('expected_price_positive', 'check(expected_price > 0)', 'The expected price must be positive'),
        ('selling_price_positive', 'check(selling_price > 0)', 'The selling price must be positive'),
    ]

    def action_sold(self):
        for rec in self:
            if rec.state == 'canceled':
                raise UserError('You cannot sell a cancelled property.')
            rec.state = 'sold'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError('You cannot cancell a selled property.')
            rec.state = 'canceled'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            best_price = 0
            if rec.offer_ids:
                best_price = max(rec.offer_ids.mapped('price'))
            rec.best_price = best_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.update({
                'garden_area': 10,
                'garden_orientation': 'north',
            })
        else:
            self.update({
                'garden_area': 0,
                'garden_orientation': False,
            })

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for rec in self:
            expected_price = rec.expected_price * 0.9
            if rec.selling_price and float_compare(
                    rec.selling_price, expected_price, precision_digits=2
                    ) == -1:
                raise UserError(
                    'The selling price cannot be less than 90% of '
                    'the expected price.'
                )


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        required=True,
        ondelete='cascade',
    )
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    validity = fields.Integer(
        default=7,
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
    )

    _sql_constraints = [
        ('price_positive', 'check(price > 0)', 'The price must be positive'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.context_today(rec)
            rec.date_deadline = fields.Date.add(
                create_date, days=+rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - rec.create_date.date()).days

    def action_accept(self):
        for rec in self:
            if any([x == 'accepted' for x in rec.property_id.offer_ids.mapped('status')]):
                raise UserError('You can only accept 1 offer.')
            rec.property_id.write({
                'buyer_id': rec.partner_id.id,
                'selling_price': rec.price,
            })
            rec.status = 'accepted'

    def action_refuse(self):
        for rec in self:
            rec.status = 'refused'
