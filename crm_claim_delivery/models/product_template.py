# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class product_product(models.Model):
    _inherit = 'product.template'


    claim_ids = fields.One2many(
        'crm.claim', 'product_id',
        string='Claims associated to this product'
    )


