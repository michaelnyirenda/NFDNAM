# -*- coding: utf-8 -*-
{
    'name': 'NFD & Petrosol Fuel Logistics & Fleet Management Demo (SaaS edu Import)',
    'version': '1.0.0',
    'category': 'Operations/Fuel & Fleet Logistics',
    'summary': 'Bulk Fuel Distribution, Fleet Compliance, Shrinkage Reconciliation & Maintenance for Northern Fuel Distributors CC (Odoo Online / SaaS edu Edition)',
    'description': """
NFD & Petrosol Petroleum Solutions Demo Addon (SaaS edu Import)
=============================================================
Pure declarative XML/CSV module designed specifically for Odoo Online (`edu-*.odoo.com`)
via Apps > Import Module (base_import_module). Contains ZERO custom Python files.

Tailored for Northern Fuel Distributors CC (NFD) and Petrosol Petroleum Solutions CC (Otjiwarongo, Namibia).

Key Capabilities:
-----------------
* Bulk fuel distribution tracking (>4,000,000L/month) with meter vs. dip reconciliation.
* Thermal variance calculation (0.25% volumetric allowance) and leakage alert system (>50L discrepancy).
* Automated 1-click corrective maintenance ticketing for Otjiwarongo Workshop & stock shrinkage scrap logs.
* Fleet compliance & replacement policy tracking (Prime Movers < 18 years, Tankers < 15 years).
* Geotab OBC device tagging and calibrated diesel meter tracking.
* HESMS & Affirmative Action (AA) driver compliance monitoring (Hazchem, Defensive Driving, Medical Fitness).
* Forecourt equipment, depot gantry, and customer bulk tank asset maintenance.
    """,
    'author': 'OreSolve Namibia',
    'website': 'https://www.oresolve.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'fleet',
        'hr_fleet',
        'maintenance',
        'stock',
        'hr',
        'hr_skills',
        'purchase',
        'sale_management',
        'account',
        'project',
        'hr_timesheet',
        'sale_timesheet',
        'spreadsheet_dashboard',
    ],
    'data': [
        'data/ir_model_fields.xml',
        'security/ir.model.access.csv',
        'data/ir_actions_server.xml',
        'data/sequences.xml',
        'data/demo_data.xml',
        'views/fuel_dispatch_log_views.xml',
        'views/fuel_consumption_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/hr_employee_views.xml',
        'views/maintenance_views.xml',
        'views/res_partner_views.xml',
        'views/menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
