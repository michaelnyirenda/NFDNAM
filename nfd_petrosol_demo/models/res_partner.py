# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_is_breakdown_partner = fields.Boolean(
        string='24/7 Breakdown Response Partner',
        default=False,
        help='Designates this partner as part of the Namibian 24/7 Emergency Breakdown Network.'
    )
    x_breakdown_coverage_area = fields.Char(
        string='Breakdown Coverage Area / Town',
        help='Geographical town or territory covered (e.g. Keetmanshoop, Mariental, Karibib, Walvis Bay, Tsumeb).'
    )
    x_breakdown_service_type = fields.Selection([
        ('mechanical', 'Heavy Mechanical Repairs'),
        ('auto_electrical', 'Auto Electrical & Diagnostic'),
        ('towing', 'Heavy Recovery & Towing'),
        ('tyres', 'Commercial Tyres & Alignment'),
        ('all_round', 'Full Breakdown & Field Service'),
    ], string='Breakdown Service Capability', default='mechanical',
       help='Primary emergency support discipline provided to stranded tankers.')
