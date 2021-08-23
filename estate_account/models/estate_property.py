# Copyright 2021, Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        super().action_sold()
        invoice_ids = []
        for rec in self:
            invoice = self.env['account.move'].create({
                'partner_id': rec.buyer_id.id,
                'ref': rec.name,
                'invoice_user_id': rec.seller_id.id,
                'type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'name': rec.name,
                    'quantity': 1,
                    'price_unit': rec.selling_price,
                }), (0, 0, {
                    'name': 'Comission',
                    'quantity': 1,
                    'price_unit': rec.selling_price * 0.06,
                }), (0, 0, {
                    'name': 'Adminstrative Fee',
                    'quantity': 1,
                    'price_unit': 100,
                }),
                ],
            })
            invoice_ids.append(invoice.id)
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoice_ids) == 1:
            action.update({
                'res_id': invoice_ids[0],
                'view_mode': 'form',
            })
        elif len(invoice_ids) > 1:
            action.update({
                'domain': [('id', 'in', invoice_ids)],
            })
        return action
