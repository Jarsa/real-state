# Copyright 2021, Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(
        required=True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exist!"),
    ]
