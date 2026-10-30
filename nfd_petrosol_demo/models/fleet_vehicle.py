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
