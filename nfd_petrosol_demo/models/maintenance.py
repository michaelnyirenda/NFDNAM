# -*- coding: utf-8 -*-
from odoo import models, fields


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    x_asset_category = fields.Selection([
        ('fleet_truck', 'Fleet Tanker / Heavy Vehicle'),
        ('depot_gantry', 'Otjiwarongo Depot Gantry & Tanks'),
        ('customer_bulk_tank', 'Customer On-Site Bulk Storage Tank'),
        ('petrosol_forecourt_pump', 'Petrosol Forecourt Dispenser Pump'),
    ], string='NFD Asset Category', default='fleet_truck', tracking=True)

    x_linked_vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Linked Fleet Vehicle',
        help='Vehicle chassis or trailer associated with this equipment.'
    )

    x_site_partner_id = fields.Many2one(
        'res.partner',
        string='Site Owner / Client Partner',
        help='Customer site (e.g. Husab Mine, B2Gold, Petrosol Outjo Forecourt).'
    )

    x_tank_capacity_liters = fields.Float(
        string='Tank / Gantry Capacity (L)',
        digits=(12, 2),
        help='Storage volume capacity for bulk tanks or gantry bays.'
    )


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    x_asset_category = fields.Selection(
        related='equipment_id.x_asset_category',
        string='Asset Category',
        store=True,
        readonly=True
    )

    x_linked_vehicle_id = fields.Many2one(
        related='equipment_id.x_linked_vehicle_id',
        string='Linked Vehicle',
        store=True,
        readonly=True
    )

    x_site_partner_id = fields.Many2one(
        'res.partner',
        string='Service Site / Client Partner',
        compute='_compute_site_partner_id',
        store=True,
        readonly=False,
        help='Client location or retail fuel station receiving maintenance support.'
    )

    x_dispatch_log_id = fields.Many2one(
        'nfd.fuel.dispatch.log',
        string='Originating Dispatch Log',
        readonly=True,
        help='Fuel dispatch record that automatically generated this corrective ticket.'
    )

    x_service_agreement_type = fields.Selection([
        ('free_retail_forecourt', 'Free Forecourt Maintenance Agreement (Petrosol/ILAMO)'),
        ('internal_fleet', 'Internal Fleet Maintenance (Otjiwarongo Workshop)'),
        ('customer_contract', 'Customer Bulk Installation Contract (Mine/Road Project)'),
    ], string='Service Agreement Type', default='internal_fleet', tracking=True,
       help='Commercial basis of maintenance work provided by NFD mechanical workshop.')

    def _compute_site_partner_id(self):
        for req in self:
            if req.equipment_id and req.equipment_id.x_site_partner_id:
                req.x_site_partner_id = req.equipment_id.x_site_partner_id
            elif not req.x_site_partner_id:
                req.x_site_partner_id = False
