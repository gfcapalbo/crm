# -*- coding: utf-8 -*-
# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('claim_ids')
    def _get_total_claims(self):
        for this in self:
            this.total_claims = len(this.claim_ids)

    claim_ids = fields.Many2many(
        comodel_name='crm.claim',
        relation="product_selected_claim_rel",
        column1='claim_ids',
        column2='product_id',
        copy=False,
        string='Claims associated to this product')
    total_claims = fields.Integer(
        compute='_get_total_claims',
        store=True)

    @api.multi
    def action_view_claims(self):
        template_model = self.env['product.template']
        result = template_model._get_act_window_dict(
            'crm_claim.crm_case_categ_claim0')
        result['domain'] = "[('id', 'in', %s)]" % self.claim_ids.ids
        return result
