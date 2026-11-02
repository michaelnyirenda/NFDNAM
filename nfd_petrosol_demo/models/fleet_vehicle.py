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

    # Multi-Trailer Coupling
    x_trailer_comp1_id = fields.Many2one(
        'fleet.vehicle',
        string='Coupled Trailer 1 / Comp 1',
        ondelete='restrict',
        help='Primary coupled tanker trailer or lead B-double link.'
    )
    x_trailer_comp2_id = fields.Many2one(
        'fleet.vehicle',
        string='Coupled Trailer 2 / Comp 2',
        ondelete='restrict',
        help='Secondary coupled pup trailer or rear tank.'
    )

    # Compartment Fuel Capacities
    x_diesel_capacity = fields.Float(
        string='Diesel Carrying Capacity (L)',
        digits=(12, 2),
        help='Dedicated diesel compartment volume.'
    )
    x_ulp_capacity = fields.Float(
        string='ULP 95 Carrying Capacity (L)',
        digits=(12, 2),
        help='Dedicated Unleaded Petrol (ULP 95) compartment volume.'
    )

    # Workshop Service & Odometer Milestones
    x_last_service_date = fields.Date(string='Last Service Date')
    x_last_service_km = fields.Float(string='Last Service Odometer (KM)', digits=(12, 1))
    x_service_interval_km = fields.Float(
        string='Service Interval (KM)',
        default=30000.0,
        digits=(12, 1),
        help='Routine service interval cycle (e.g. 15,000 km, 30,000 km, 50,000 km).'
    )
    x_next_service_km = fields.Float(string='Next Service Milestone (KM)', digits=(12, 1))
    x_km_until_service = fields.Float(
        string='KM Until Service Due',
        compute='_compute_service_due',
        store=True,
        digits=(12, 1)
    )
    x_service_status = fields.Selection([
        ('ok', 'Service OK'),
        ('due_soon', 'Service Due Soon (< 5,000 KM)'),
        ('overdue', 'Service Overdue'),
    ], string='Service Status', compute='_compute_service_due', store=True, default='ok')

    # Statutory Compliance Certificates & Expirations
    x_licence_expiry_date = fields.Date(
        string='NaTIS Vehicle Licence Expiry',
        help='Namibian Traffic Information System annual license disk expiry.'
    )
    x_fitness_certificate_expiry = fields.Date(
        string='NaTIS Roadworthy Fitness Expiry',
        help='Statutory vehicle fitness and roadworthy certificate expiry.'
    )
    x_safe_loading_pass_expiry = fields.Date(
        string='Safe Loading Pass (SLP) Expiry',
        help='Oil Industry Safe Loading Pass (SLP) validation for gantry bottom-loading.'
    )
    x_pressure_test_expiry = fields.Date(
        string='Tanker Pressure Test Expiry',
        help='2.5/5-year statutory hydrostatic/pneumatic tanker pressure test certificate.'
    )
    x_tanker_calibration_date = fields.Date(
        string='Depot Calibration Date',
        help='Depot meter and dipstick chart calibration verification date.'
    )
    x_last_wheel_alignment_date = fields.Date(
        string='Last Wheel Alignment Date',
        help='Laser axle and kingpin alignment test date.'
    )

    # PTO Specifications
    x_pto_type = fields.Selection([
        ('hydraulic_pto', 'Hydraulic PTO'),
        ('engine_pto', 'Auxiliary Engine PTO'),
        ('both', 'Dual PTO (Engine & Hydraulic)'),
        ('none', 'None / Gravity Discharge'),
    ], string='PTO Drive Type', default='none',
       help='Power Take-Off mechanism used to drive fuel offloading discharge pumps.')
    x_pto_location = fields.Char(
        string='PTO Mounting Position',
        help='e.g., Behind the Cab, On Cab next to COC Tank, PTO Engine on Tanker.'
    )

    # Fleet Operational Availability
    x_operational_availability = fields.Selection([
        ('active', 'Active In Service'),
        ('standby', 'Standby Unit'),
        ('maintenance', 'In Maintenance / Workshop'),
        ('accident', 'Grounded - Accident Damage'),
        ('roadworthy', 'Awaiting NaTIS Roadworthy'),
        ('for_sale', 'Decommissioned - For Sale'),
    ], string='Operational Availability', default='active', tracking=True)

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

    @api.depends('odometer', 'x_next_service_km')
    def _compute_service_due(self):
        for vehicle in self:
            if vehicle.x_next_service_km:
                current_km = vehicle.odometer or 0.0
                remaining = vehicle.x_next_service_km - current_km
                vehicle.x_km_until_service = remaining
                if remaining < 0:
                    vehicle.x_service_status = 'overdue'
                elif remaining <= 5000:
                    vehicle.x_service_status = 'due_soon'
                else:
                    vehicle.x_service_status = 'ok'
            else:
                vehicle.x_km_until_service = 0.0
                vehicle.x_service_status = 'ok'


