# Copyright 2021, Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

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


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

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
    )
