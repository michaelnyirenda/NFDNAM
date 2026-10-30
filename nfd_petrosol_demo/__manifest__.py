# -*- coding: utf-8 -*-
{
    'name': 'NFD & Petrosol Fuel Logistics & Fleet Management Demo',
    'version': '19.0.1.0.0',
    'category': 'Operations/Fuel & Fleet Logistics',
    'summary': 'Bulk Fuel Distribution, Fleet Compliance, Shrinkage Reconciliation & Maintenance for Northern Fuel Distributors CC',
    'description': """
NFD & Petrosol Petroleum Solutions Demo Addon
=============================================
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
        'maintenance',
        'stock',
        'hr',
        'hr_skills',
        'purchase',
        'sale_management',
        'account',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/fuel_dispatch_log_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/hr_employee_views.xml',
        'views/maintenance_views.xml',
        'views/menus.xml',
        'data/demo_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
