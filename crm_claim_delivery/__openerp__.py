# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "crm_claim_delivery",
    "version": "8.0.1.0.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "category": "Customer Relationship Management",
    "summary": "Claim connected to deliveries",
    "depends": [
        'stock',
        'crm_claim_type'
    ],
    "data": [
        'data/crm_claim_type.xml',
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
