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
    def get_delivery_products(self):
       if self.delivery_id:
           products = []
           packs = self.mapped('delivery_id.pack_operation_ids')
           for pack in packs:
               products.append(pack.product_id.id)
           moves =  self.mapped('delivery_id.move_lines')
           for move in moves:
               products.append(move.product_id.id)
           self.product_selection = self.env['product.product'].browse(
               list(set(products))
           ) 
           self.product_id = self.env['product.product'].browse([])
           

    delivery_id = fields.Many2one(
        'stock.picking',
        string='delivery on wich to make the claim',
        domain=lambda self: [(
            'picking_type_id', 'in', self.get_delivery_pickings())]
    )

    product_selection = fields.Many2one(
        'product.product',
        string='product',
        compute='get_delivery_products',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product Object of Claim',
    )

