# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_claims(self):
        res=[]
        for claim in self.env['crm.claim'].search(
               [('product_selected_ids', '!=' , False)]):
            if self.id in claim.product_selected_ids.ids:
                res.append(self.id)
        self.claim_ids = res
        self.total_claims =  len(res)
        return res
        
    claim_ids = fields.One2many(
        'crm.claim', 
        string='Claims associated to this product',
        compute= 'get_claims',
        store=False
    )

    total_claims = fields.Integer(
        compute='get_claims',
        store=False
    )
    @api.model
    def action_view_claims(self):
        result = self.env['ir.model.data'].res(
            'crm_claim.crm_case_categ_claim0'
        )
        result = self.pool['ir.actions.act_window'].read([result])[0]
        result['domain'] = "[('id','in', %s   )]" % self.get_claims()
        return result
