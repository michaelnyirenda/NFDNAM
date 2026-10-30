# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    x_aa_category = fields.Selection([
        ('designated_namibian', 'Designated Namibian Group'),
        ('women_in_transport', 'Women in Transport Initiative'),
        ('pw_disabilities', 'Persons with Disabilities'),
        ('general', 'General / Non-Designated Group'),
    ], string='Affirmative Action Category', default='designated_namibian', tracking=True,
       help='Namibian Affirmative Action (Employment) Act compliance classification.')

    x_hazchem_expiry = fields.Date(
        string='Dangerous Goods / Hazchem Permit Expiry',
        tracking=True,
        help='Namibian Transport Dangerous Goods Hazchem Certification expiry date.'
    )

    x_defensive_driving_expiry = fields.Date(
        string='HESMS Defensive Driving Expiry',
        tracking=True,
        help='Chevron/HESMS Certified Defensive Driving refresher expiry date.'
    )

    x_medical_fitness_expiry = fields.Date(
        string='Annual Medical Fitness Expiry',
        tracking=True,
        help='Annual Occupational Medical Practitioner fitness-to-drive certificate expiry date.'
    )

    x_hse_compliant = fields.Boolean(
        string='HESMS Compliant',
        compute='_compute_hse_compliance',
        store=True,
        tracking=True,
        help='Evaluated true only when Hazchem, Defensive Driving, and Medical Fitness permits are all active.'
    )

    x_hse_status_badge = fields.Selection([
        ('compliant', 'Fully Compliant'),
        ('expiring_soon', 'Expiring Within 30 Days'),
        ('expired', 'Permit Expired / Non-Compliant'),
        ('not_applicable', 'Non-Driver / Exempt'),
    ], string='HESMS Safety Status',
       compute='_compute_hse_compliance',
       store=True,
       tracking=True)

    @api.depends('x_hazchem_expiry', 'x_defensive_driving_expiry', 'x_medical_fitness_expiry')
    def _compute_hse_compliance(self):
        today = date.today()
        warning_window = today + timedelta(days=30)

        for emp in self:
            # Check if this employee has driver certifications tracked
            has_certs = any([
                emp.x_hazchem_expiry,
                emp.x_defensive_driving_expiry,
                emp.x_medical_fitness_expiry
            ])

            if not has_certs:
                emp.x_hse_compliant = False
                emp.x_hse_status_badge = 'not_applicable'
                continue

            # Check if any certificate is missing or expired
            hazchem_ok = emp.x_hazchem_expiry and emp.x_hazchem_expiry >= today
            defensive_ok = emp.x_defensive_driving_expiry and emp.x_defensive_driving_expiry >= today
            medical_ok = emp.x_medical_fitness_expiry and emp.x_medical_fitness_expiry >= today

            if hazchem_ok and defensive_ok and medical_ok:
                emp.x_hse_compliant = True
                # Check if any expires within 30 days
                expiring_soon = any([
                    emp.x_hazchem_expiry <= warning_window,
                    emp.x_defensive_driving_expiry <= warning_window,
                    emp.x_medical_fitness_expiry <= warning_window
                ])
                if expiring_soon:
                    emp.x_hse_status_badge = 'expiring_soon'
                else:
                    emp.x_hse_status_badge = 'compliant'
            else:
                emp.x_hse_compliant = False
                emp.x_hse_status_badge = 'expired'
