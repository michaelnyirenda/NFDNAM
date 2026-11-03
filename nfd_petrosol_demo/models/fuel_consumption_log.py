# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NfdFuelConsumptionLog(models.Model):
    _name = 'nfd.fuel.consumption.log'
    _description = 'NFD Vehicle Refuel & Odometer LogSheet'
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Log Reference',
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('nfd.fuel.consumption.log') or 'NEW'
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today
    )
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle Registration',
        required=True,
        ondelete='restrict'
    )
    driver_id = fields.Many2one(
        'hr.employee',
        string='Driver',
        required=True,
        ondelete='restrict'
    )
    place = fields.Selection([
        ('Depot', 'Depot (Otjiwarongo)'),
        ('OKH', 'OKH (Okahandja)'),
        ('Office', 'Office'),
        ('Walvis', 'Walvis Bay'),
        ('Ohakane', 'Ohakane'),
        ('Fort Sesfontein', 'Fort Sesfontein'),
        ('Mareintal', 'Mariental'),
        ('Ondangwa', 'Ondangwa'),
        ('Omakange', 'Omakange'),
        ('Otavi Shell', 'Otavi Shell'),
        ('B1 PUMA', 'B1 PUMA'),
        ('Agra Karibib', 'Agra Karibib'),
        ('Agra Gobabis', 'Agra Gobabis'),
        ('Agra Vivo', 'Agra Vivo'),
        ('CJ Steenkamp', 'CJ Steenkamp'),
        ('Ndama', 'Ndama'),
        ('Tokat', 'Tokat'),
        ('Veronika', 'Veronika'),
        ('Weimans', 'Weimans'),
    ], string='Refueling Place / Facility', required=True, default='Depot')

    odometer_start = fields.Float(
        string='Odometer Start',
        required=True,
        digits=(12, 1)
    )
    odometer_end = fields.Float(
        string='Odometer End',
        required=True,
        digits=(12, 1)
    )
    distance_traveled_km = fields.Float(
        string='Distance Traveled (KM)',
        compute='_compute_fuel_consumption_metrics',
        store=True,
        digits=(12, 1)
    )
    fuel_liters = fields.Float(
        string='Fuel (L)',
        required=True,
        digits=(12, 2)
    )
    expected_km_per_liter = fields.Float(
        string='Expected Fuel Consumption (KM/L)',
        compute='_compute_expected_km_per_liter',
        store=True,
        readonly=False,
        digits=(8, 2)
    )
    actual_km_per_liter = fields.Float(
        string='Fuel Consumption (KM/L)',
        compute='_compute_fuel_consumption_metrics',
        store=True,
        digits=(8, 2)
    )
    fuel_usage_difference = fields.Float(
        string='Fuel Usage Difference (KM/L)',
        compute='_compute_fuel_consumption_metrics',
        store=True,
        digits=(8, 2)
    )
    expected_fuel_liters = fields.Float(
        string='Expected Fuel Used (L)',
        compute='_compute_fuel_consumption_metrics',
        store=True,
        digits=(12, 2)
    )
    excess_use_liters = fields.Float(
        string='Excess Use (L)',
        compute='_compute_fuel_consumption_metrics',
        store=True,
        digits=(12, 2)
    )
    otj_coc_fuel_price = fields.Float(
        string='Current Fuel Price Otj COC (NAD/L)',
        default=25.98,
        digits=(8, 2)
    )
    nad_value = fields.Float(
        string='NAD Value (@ 25.98 Otj COC)',
        compute='_compute_fuel_consumption_metrics',
        store=True,
        digits=(12, 2)
    )
    confirm_logsheet = fields.Selection([
        ('confirmed', '√ Confirmed'),
        ('unconfirmed', 'X Unconfirmed Logsheet'),
    ], string='Confirm Logsheet', default='confirmed', required=True)

    confirm_stock = fields.Selection([
        ('confirmed', '√ Confirmed'),
        ('unconfirmed', 'X Unconfirmed Stock'),
    ], string='Confirm Stock', default='confirmed', required=True)

    notes = fields.Char(string='Notes / Audit Remarks')

    anomaly_flag = fields.Selection([
        ('normal', 'Within Target'),
        ('excess_burn', 'Excess Burn'),
        ('odo_error', 'Odometer / Logsheet Anomaly'),
    ], string='Audit Status', compute='_compute_fuel_consumption_metrics', store=True)

    @api.depends('vehicle_id', 'vehicle_id.x_expected_km_per_liter')
    def _compute_expected_km_per_liter(self):
        for log in self:
            if log.vehicle_id and log.vehicle_id.x_expected_km_per_liter:
                log.expected_km_per_liter = log.vehicle_id.x_expected_km_per_liter
            elif not log.expected_km_per_liter:
                log.expected_km_per_liter = 2.5

    @api.depends('odometer_start', 'odometer_end', 'fuel_liters', 'expected_km_per_liter',
                 'confirm_logsheet', 'otj_coc_fuel_price')
    def _compute_fuel_consumption_metrics(self):
        for log in self:
            # 1. Distance Traveled
            if log.odometer_end is not None and log.odometer_start is not None:
                log.distance_traveled_km = max(0.0, round(log.odometer_end - log.odometer_start, 1))
            else:
                log.distance_traveled_km = 0.0

            # 2. Actual KM/L
            if log.fuel_liters and log.fuel_liters > 0:
                log.actual_km_per_liter = round(log.distance_traveled_km / log.fuel_liters, 2)
            else:
                log.actual_km_per_liter = 0.0

            # 3. Difference (Actual KM/L - Expected KM/L)
            exp_kml = log.expected_km_per_liter or 0.0
            log.fuel_usage_difference = round(log.actual_km_per_liter - exp_kml, 2)

            # 4. Expected Fuel Liters
            if exp_kml > 0:
                log.expected_fuel_liters = round(log.distance_traveled_km / exp_kml, 2)
            else:
                log.expected_fuel_liters = 0.0

            # 5. Excess Use Liters
            log.excess_use_liters = round((log.fuel_liters or 0.0) - log.expected_fuel_liters, 2)

            # 6. Financial NAD Value
            price = log.otj_coc_fuel_price or 25.98
            log.nad_value = round(log.excess_use_liters * price, 2)

            # 7. Audit Anomaly Flag
            if log.confirm_logsheet == 'unconfirmed' or (exp_kml > 0 and log.actual_km_per_liter < (exp_kml * 0.5) and log.fuel_liters > 50):
                log.anomaly_flag = 'odo_error'
            elif log.excess_use_liters > 25.0:
                log.anomaly_flag = 'excess_burn'
            else:
                log.anomaly_flag = 'normal'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.vehicle_id and rec.odometer_end:
                if rec.odometer_end > (rec.vehicle_id.odometer or 0.0):
                    rec.vehicle_id.write({'odometer': rec.odometer_end})
                is_overdue = (rec.vehicle_id.x_next_service_km and rec.odometer_end > rec.vehicle_id.x_next_service_km) or (rec.vehicle_id.x_service_status == 'overdue')
                if is_overdue:
                    self._check_create_service_job_card(rec.vehicle_id)
        return records

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.vehicle_id and rec.odometer_end:
                if rec.odometer_end > (rec.vehicle_id.odometer or 0.0):
                    rec.vehicle_id.write({'odometer': rec.odometer_end})
                is_overdue = (rec.vehicle_id.x_next_service_km and rec.odometer_end > rec.vehicle_id.x_next_service_km) or (rec.vehicle_id.x_service_status == 'overdue')
                if is_overdue:
                    self._check_create_service_job_card(rec.vehicle_id)
        return res

    def _check_create_service_job_card(self, vehicle):
        # Auto-create scheduled maintenance ticket if vehicle exceeds service interval
        existing = self.env['maintenance.request'].search([
            ('x_linked_vehicle_id', '=', vehicle.id),
            ('x_job_type', '=', 'service'),
            ('stage_id.done', '=', False),
        ], limit=1)
        if not existing:
            equipment = self.env['maintenance.equipment'].search([
                ('x_linked_vehicle_id', '=', vehicle.id)
            ], limit=1)
            if not equipment:
                equipment = self.env['maintenance.equipment'].create({
                    'name': vehicle.name,
                    'x_linked_vehicle_id': vehicle.id,
                    'x_asset_category': 'fleet_truck',
                })
            self.env['maintenance.request'].create({
                'name': f'[AUTOMATED] Routine Service Milestone Overdue - {vehicle.name}',
                'equipment_id': equipment.id,
                'x_job_type': 'service',
                'x_job_card_number': f'JC-AUTO-{vehicle.id}',
                'x_workshop_location': 'workshop_otj',
                'x_assigned_mechanic': 'green',
                'priority': '3',
                'description': f'Automated ERP Trigger: Vehicle {vehicle.name} has exceeded its routine service milestone by {abs(vehicle.x_km_until_service):.1f} KM based on driver refuel slip. Scheduled workshop service inspection required.',
            })

