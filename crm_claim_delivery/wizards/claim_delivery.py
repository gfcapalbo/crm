# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime
from openerp import api, fields, models
from openerp.tools import float_round
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DSDF


class ClaimDeliveryWizard(models.TransientModel):

    _name = "crm.delivery_wizard"
    _description = "wizard choose products"

    product_id = fields.Many2one(
        "product.template",
        string="product",
        domain=lambda self: [(
            'id',  'in', self._get_delivery_products()
        )]
    )

    claim_id = fields.Many2one(
        'crm.claim', string="Claim"
    )

    delivery_id = fields.Many2one(
       'stock.picking', string="Delivery"
    )

    @api.multi
    def _get_delivery_products(self):
        if self.delivery_id:
            products = []
            pack_products = self.mapped(
                'delivery_id.pack_operation_ids.product_id'
            )
            move_products =  self.mapped(
                'delivery_id.move_lines.product_id'
            )
            products = pack_products | move_products
            return products.mapped('product_tmpl_id').ids
        return []

    product_selection_domain = fields.Many2many(
        'product.template',
        compute='_compute_get_delivery_products',
    )

    @api.model
    def default_get(self, fields_list):
        result = {}
        result = super(ClaimDeliveryWizard, self).default_get(
            fields_list=fields_list
        )
        claim_model = self.env['crm.claim']
        claimID = self.env.context.get("active_ids", False)
        if claimID:
            claim = claim_model.browse(claimID[0])
            result['product_selection_domain'] = self.product_selection_domain
            result["claim_id"] = claim.id
            if claim:
                result['delivery_id'] = claim.delivery_id.id
        return result

    @api.multi
    def save(self):
        self.claim_id.write(
            {'product_selected_ids':[(4,self.product_id.id)]}
        )
        return True




