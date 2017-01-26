# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.model
    def get_delivery_pickings(self):
        return self.env['stock.picking.type'].search(
            [('code', '=', 'outgoing')]
        ).ids

    @api.onchange('delivery_id')
    def _compute_get_delivery_products(self):
        if self.delivery_id:
            products = []
            pack_products = self.mapped(
                'delivery_id.pack_operation_ids.product_id'
            )
            move_products =  self.mapped(
                'delivery_id.move_lines.product_id'
            )
            products = pack_products | move_products
            self.product_selection_ids = products.mapped('product_tmpl_id').ids

    def _inverse_set_delivery_products(self):
        if self.delivery_id:
            self.product_selected_ids = self.product_selection_ids
        else:
            self.product_selected_ids = None


    delivery_id = fields.Many2one(
        'stock.picking',
        string='delivery on wich to make the claim',
        domain=lambda self: [(
            'picking_type_id', 'in', self.get_delivery_pickings())]
    )

    product_selection_ids = fields.Many2many(
        'product.template', 'claim_ids',
        string='Select Products Involved in this Claim',
        compute='_compute_get_delivery_products',
        inverse='_inverse_set_delivery_products',
        store=False
    )

