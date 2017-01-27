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
    )

    claim_id = fields.Many2one(
        'crm.claim', string="Claim"
    )

    delivery_id = fields.Many2one(
       'stock.picking', string="Delivery"
    )

    product_selection = fields.Char()
    
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
            result['product_selected_ids'] = claim.product_selected_ids.ids
            result['product_selection'] = claim.product_selection_ids
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




