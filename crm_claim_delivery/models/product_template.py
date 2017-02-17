# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def find_ids(self):
        res = []
        for claim in self.env['crm.claim'].search(
               [('product_selected_ids', '!=', False)]):
            if self.id in claim.product_selected_ids.ids:
                res.append(claim.id)
        return res

    @api.multi
    def get_claims(self):
        res = self.find_ids()
        self.claim_ids = res
        self.total_claims = len(res)

    def get_claims_for_domain(self):
        res = self.find_ids()
        return res

    claim_ids = fields.One2many(
        'crm.claim',
        string='Claims associated to this product',
        compute='get_claims',
        store=False
    )
    total_claims = fields.Integer(
        compute='get_claims',
        store=False
    )

    @api.multi
    def action_view_claims(self):
        template_model = self.env['product.template']
        result = template_model._get_act_window_dict(
            'crm_claim.crm_case_categ_claim0'
        )
        result['domain'] = \
            "[('id', 'in', %s)]" % self.get_claims_for_domain()
        return result
