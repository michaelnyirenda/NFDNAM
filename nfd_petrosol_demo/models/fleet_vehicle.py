# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    x_unit_classification = fields.Selection([
        ('prime_mover', 'Prime Mover / Tractor'),
        ('rigid_tanker', 'Rigid Tanker'),
        ('semi_trailer', 'Tri-Axle Semi-Trailer Tanker'),
        ('pup_trailer', 'Pup Trailer Tanker'),
        ('drawbar_trailer', 'Drawbar Trailer Tanker'),
    ], string='Unit Classification', default='prime_mover', tracking=True)

    x_max_volume_liters = fields.Float(
        string='Max Fuel Capacity (L)',
        digits=(12, 2),
        help='Maximum bulk cargo fuel carrying capacity in liters.'
    )

    x_compartment_count = fields.Integer(
        string='Number of Compartments',
        default=1,
        help='Number of isolated cargo compartments for multiple product loads.'
    )

    x_has_diesel_meter = fields.Boolean(
        string='Fitted with Calibrated Diesel Meter',
        default=False,
        help='Equipped with an onboard certified digital delivery meter.'
    )

    x_geotab_device_id = fields.Char(
        string='Geotab OBC Unit ID',
        help='On-Board Computer serial number linked to Geotab telematics.'
    )

    x_manufacture_year = fields.Integer(
        string='Manufacture Year',
        default=lambda self: date.today().year,
        help='Vehicle chassis or tanker body production year.'
    )

    x_vehicle_age = fields.Integer(
        string='Vehicle Age (Years)',
        compute='_compute_vehicle_age',
        store=True,
        help='Elapsed years calculated from manufacture year.'
    )

    x_replacement_policy_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('warning', 'Warning (Near Policy Limit)'),
        ('replace_due', 'Replacement Due'),
    ], string='Fleet Replacement Status',
       compute='_compute_replacement_policy_status',
       store=True,
       tracking=True,
       help='NFD Policy: Prime Movers < 18 yrs; Tankers & Trailers < 15 yrs.')

    x_avg_fuel_consumption = fields.Float(
        string='Avg Engine Burn (L/100km)',
        digits=(6, 2),
        help='Calculated average engine diesel consumption from Geotab telematics.'
    )

    # NFD September 2026 Fuel Consumption Workbook Metrics (Otj COC)
    x_expected_km_per_liter = fields.Float(
        string='Expected (KM/L)',
        digits=(8, 2),
        help='NFD benchmark fuel efficiency in kilometers per liter.'
    )
    x_actual_km_per_liter = fields.Float(
        string='Actual (KM/L) - Sept 2026',
        digits=(8, 2),
        help='Actual achieved fuel efficiency for September 2026.'
    )
    x_sept_distance_km = fields.Float(
        string='Distance Covered (KM) - Sept 2026',
        digits=(12, 1),
        help='Total odometer kilometers traversed in September 2026.'
    )
    x_sept_expected_fuel_l = fields.Float(
        string='Expected Total Fuel Used (L)',
        compute='_compute_sept_fuel_metrics',
        store=True,
        digits=(12, 2),
        help='Calculated target fuel consumption based on Expected KM/L.'
    )
    x_sept_actual_fuel_l = fields.Float(
        string='Actual Total Fuel Used (L) - Sept 2026',
        digits=(12, 2),
        help='Total fuel drawn from Otjiwarongo depot tanks and external sites.'
    )
    x_sept_excess_fuel_l = fields.Float(
        string='Excess Use (L)',
        compute='_compute_sept_fuel_metrics',
        store=True,
        digits=(12, 2),
        help='Discrepancy in liters: Actual Fuel Used minus Expected Fuel Used.'
    )
    x_otj_coc_fuel_price = fields.Float(
        string='Current Fuel Price Otj COC (NAD/L)',
        default=25.98,
        digits=(8, 2),
        help='Otjiwarongo Commercial Operations Cost benchmark price per liter.'
    )
    x_sept_excess_nad_value = fields.Float(
        string='Excess NAD Value (@ 25.98/L)',
        compute='_compute_sept_fuel_metrics',
        store=True,
        digits=(12, 2),
        help='Monetary financial impact in NAD valued at Otj COC benchmark price.'
    )

    @api.depends('x_sept_distance_km', 'x_expected_km_per_liter', 'x_sept_actual_fuel_l', 'x_otj_coc_fuel_price')
    def _compute_sept_fuel_metrics(self):
        for vehicle in self:
            price = vehicle.x_otj_coc_fuel_price or 25.98
            if vehicle.x_expected_km_per_liter and vehicle.x_expected_km_per_liter > 0:
                vehicle.x_sept_expected_fuel_l = round((vehicle.x_sept_distance_km or 0.0) / vehicle.x_expected_km_per_liter, 2)
            else:
                vehicle.x_sept_expected_fuel_l = 0.0

            if vehicle.x_sept_actual_fuel_l is not None and vehicle.x_sept_expected_fuel_l is not None:
                vehicle.x_sept_excess_fuel_l = round((vehicle.x_sept_actual_fuel_l or 0.0) - vehicle.x_sept_expected_fuel_l, 2)
            else:
                vehicle.x_sept_excess_fuel_l = 0.0

            vehicle.x_sept_excess_nad_value = round(vehicle.x_sept_excess_fuel_l * price, 2)

    @api.depends('x_manufacture_year')
    def _compute_vehicle_age(self):
        current_year = date.today().year
        for vehicle in self:
            if vehicle.x_manufacture_year:
                vehicle.x_vehicle_age = max(0, current_year - vehicle.x_manufacture_year)
            else:
                vehicle.x_vehicle_age = 0

    @api.depends('x_vehicle_age', 'x_unit_classification')
    def _compute_replacement_policy_status(self):
        for vehicle in self:
            age = vehicle.x_vehicle_age or 0
            classification = vehicle.x_unit_classification or 'prime_mover'

            if classification == 'prime_mover':
                # NFD Policy: Prime Movers < 18 years
                if age >= 18:
                    vehicle.x_replacement_policy_status = 'replace_due'
                elif age >= 17:
                    vehicle.x_replacement_policy_status = 'warning'
                else:
                    vehicle.x_replacement_policy_status = 'compliant'
            else:
                # NFD Policy: Tankers / Trailers < 15 years
                if age >= 15:
                    vehicle.x_replacement_policy_status = 'replace_due'
                elif age >= 14:
                    vehicle.x_replacement_policy_status = 'warning'
                else:
                    vehicle.x_replacement_policy_status = 'compliant'

