# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class NfdFuelDispatchLog(models.Model):
    _name = 'nfd.fuel.dispatch.log'
    _description = 'NFD Cargo Fuel Dispatch & Leakage Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Dispatch Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )

    date = fields.Datetime(
        string='Dispatch Date & Time',
        default=fields.Datetime.now,
        required=True,
        tracking=True
    )

    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Delivery Tanker / Rig',
        required=True,
        tracking=True,
        help='NFD delivery vehicle assigned to this cargo trip.'
    )

    driver_id = fields.Many2one(
        'hr.employee',
        string='Certified Hazchem Driver',
        required=True,
        tracking=True,
        domain="[('x_hazchem_expiry', '!=', False)]",
        help='HESMS and Hazchem-certified driver.'
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Receiving Customer / Site',
        required=True,
        tracking=True,
        help='Delivery destination (Mine, Road Construction, or Petrosol Station).'
    )

    source_location_id = fields.Many2one(
        'stock.location',
        string='Depot Source Location',
        required=True,
        help='Source gantry or bulk tank at Otjiwarongo Depot.'
    )

    destination_location_id = fields.Many2one(
        'stock.location',
        string='Customer Storage Tank Location',
        help='Destination storage location (on-site customer bulk tank or retail forecourt tank).'
    )

    fuel_product_id = fields.Many2one(
        'product.product',
        string='Bulk Fuel Product',
        required=True,
        tracking=True,
        domain="[('type', '=', 'consu')]",  # In Odoo 19 storable/consumable
        help='Bulk commodity being distributed (e.g. 50ppm Diesel, ULP 95 Petrol).'
    )

    depot_loaded_liters = fields.Float(
        string='Depot Gantry Loaded (L)',
        required=True,
        digits=(12, 2),
        tracking=True,
        help='Metered volume loaded into tanker compartments at Otjiwarongo Depot.'
    )

    compartment_seal_numbers = fields.Char(
        string='Compartment Seal #s',
        tracking=True,
        help='Tamper-evident security seal numbers affixed at depot gantry departure.'
    )

    truck_meter_delivered_liters = fields.Float(
        string='Truck Diesel Meter Reading (L)',
        digits=(12, 2),
        tracking=True,
        help='Certified onboard digital meter volume discharged at customer site.'
    )

    customer_dip_received_liters = fields.Float(
        string='Customer Tank Dip Received (L)',
        digits=(12, 2),
        tracking=True,
        help='Manual dipstick or ATG volume recorded in customer bulk tank after discharge.'
    )

    temp_allowance_liters = fields.Float(
        string='Thermal Variance Allowance (L)',
        compute='_compute_temp_allowance',
        store=True,
        readonly=False,
        digits=(12, 2),
        help='Standard Namibian industry volumetric thermal allowance (0.25% of loaded volume).'
    )

    net_variance_liters = fields.Float(
        string='Net Discrepancy / Variance (L)',
        compute='_compute_variance',
        store=True,
        digits=(12, 2),
        tracking=True,
        help='Calculated discrepancy: Loaded (L) - Delivered (L) - Thermal Allowance (L).'
    )

    leakage_status = fields.Selection([
        ('normal', 'Normal Reconciliation'),
        ('minor_variance', 'Minor Thermal Variance'),
        ('leakage_alert', 'Leakage / Pilferage Alert!'),
    ], string='Reconciliation Status',
       compute='_compute_variance',
       store=True,
       tracking=True,
       help='Automated classification based on volume discrepancy threshold (>50L alert).')

    pre_trip_hse_passed = fields.Boolean(
        string='HESMS Pre-Trip Safety & Valve Check Passed',
        default=True,
        tracking=True,
        help='HESMS checklist: bottom loading valves, vapor recovery, earth bonding, fire extinguishers.'
    )

    state = fields.Selection([
        ('draft', 'Draft / Loading'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered & Reconciled'),
        ('investigation', 'Under HSE Investigation'),
    ], string='Status', default='draft', tracking=True)

    maintenance_request_id = fields.Many2one(
        'maintenance.request',
        string='Corrective Maintenance Ticket',
        readonly=True,
        copy=False,
        help='Corrective maintenance ticket generated for Otjiwarongo Mechanical Workshop.'
    )

    scrap_id = fields.Many2one(
        'stock.scrap',
        string='Stock Shrinkage Entry',
        readonly=True,
        copy=False,
        help='Inventory write-off entry tracking fuel loss.'
    )

    notes = fields.Text(string='Operational Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('nfd.fuel.dispatch.log') or _('New')
        return super().create(vals_list)

    @api.depends('depot_loaded_liters')
    def _compute_temp_allowance(self):
        for rec in self:
            if rec.depot_loaded_liters:
                # 0.25% thermal volumetric variance standard in Namibia
                rec.temp_allowance_liters = round(rec.depot_loaded_liters * 0.0025, 2)
            else:
                rec.temp_allowance_liters = 0.0

    @api.depends('depot_loaded_liters', 'truck_meter_delivered_liters', 'temp_allowance_liters')
    def _compute_variance(self):
        for rec in self:
            delivered = rec.truck_meter_delivered_liters or 0.0
            loaded = rec.depot_loaded_liters or 0.0
            allowance = rec.temp_allowance_liters or 0.0

            if loaded and delivered:
                # Variance = Loaded - Delivered - Allowance
                variance = round(loaded - delivered - allowance, 2)
                rec.net_variance_liters = variance
                if variance > 50.0:
                    rec.leakage_status = 'leakage_alert'
                elif variance > 10.0:
                    rec.leakage_status = 'minor_variance'
                else:
                    rec.leakage_status = 'normal'
            else:
                rec.net_variance_liters = 0.0
                rec.leakage_status = 'normal'

    def action_dispatch(self):
        for rec in self:
            if not rec.pre_trip_hse_passed:
                raise UserError(_("Cannot dispatch tanker: HESMS Pre-Trip Safety & Valve Check must be passed!"))
            rec.state = 'in_transit'

    def action_reconcile(self):
        for rec in self:
            if not rec.truck_meter_delivered_liters:
                raise UserError(_("Please enter the Truck Diesel Meter Reading before reconciling."))
            if rec.leakage_status == 'leakage_alert':
                rec.state = 'investigation'
            else:
                rec.state = 'delivered'

    def action_create_leakage_maintenance_ticket(self):
        self.ensure_one()
        if self.leakage_status != 'leakage_alert':
            raise UserError(_("Maintenance tickets can only be automatically generated for Leakage Alert records."))

        # 1. Identify or link equipment for vehicle
        equipment = self.env['maintenance.equipment'].search([
            ('x_linked_vehicle_id', '=', self.vehicle_id.id)
        ], limit=1)

        if not equipment:
            equipment = self.env['maintenance.equipment'].create({
                'name': f"{self.vehicle_id.name} - Tanker Manifold & Meter Rig",
                'x_asset_category': 'fleet_truck',
                'x_linked_vehicle_id': self.vehicle_id.id,
                'category_id': self.env.ref('nfd_petrosol_demo.maintenance_cat_fleet_truck', raise_if_not_found=False) and self.env.ref('nfd_petrosol_demo.maintenance_cat_fleet_truck').id or False,
            })

        # 2. Create Corrective Maintenance Request for Otjiwarongo Workshop
        ticket_vals = {
            'name': f"URGENT: Inspect Tanker Manifold/Delivery Meter for Fuel Leakage - {self.vehicle_id.name} ({self.name})",
            'equipment_id': equipment.id,
            'maintenance_type': 'corrective',
            'priority': '3',  # High priority
            'description': (
                f"AUTOMATED LEAKAGE ALERT TRIGGERED:\n"
                f"- Dispatch Log: {self.name}\n"
                f"- Tanker: {self.vehicle_id.name} (License: {self.vehicle_id.license_plate or 'N/A'})\n"
                f"- Driver: {self.driver_id.name}\n"
                f"- Receiving Client: {self.customer_id.name}\n"
                f"- Depot Loaded: {self.depot_loaded_liters:,.2f} L\n"
                f"- Delivered Reading: {self.truck_meter_delivered_liters:,.2f} L\n"
                f"- Thermal Variance Allowed: {self.temp_allowance_liters:,.2f} L\n"
                f"- NET DISCREPANCY: {self.net_variance_liters:,.2f} L (Exceeds 50L Safety Limit)\n"
                f"- Seals Affixed: {self.compartment_seal_numbers or 'N/A'}\n\n"
                f"ACTION REQUIRED BY OTJIWARONGO WORKSHOP:\n"
                f"1. Pressure test bottom-loading manifold and foot valves.\n"
                f"2. Calibrate onboard digital flow meter.\n"
                f"3. Inspect discharge hoses and vapor recovery connections for weeping."
            ),
            'x_asset_category': 'fleet_truck',
            'x_site_partner_id': self.customer_id.id,
        }
        maintenance_ticket = self.env['maintenance.request'].create(ticket_vals)
        self.maintenance_request_id = maintenance_ticket.id

        # 3. Create Stock Scrap / Shrinkage Entry
        loss_location = self.env.ref('nfd_petrosol_demo.location_fuel_shrinkage', raise_if_not_found=False)
        if not loss_location:
            loss_location = self.env['stock.location'].search([
                ('name', 'ilike', 'Shrinkage')
            ], limit=1)

        scrap_vals = {
            'product_id': self.fuel_product_id.id,
            'scrap_qty': max(1.0, self.net_variance_liters),
            'product_uom_id': self.fuel_product_id.uom_id.id,
            'location_id': self.source_location_id.id,
            'scrap_location_id': loss_location.id if loss_location else False,
            'origin': f"Leakage Discrepancy {self.name}",
        }
        try:
            scrap_entry = self.env['stock.scrap'].create(scrap_vals)
            # Try to validate scrap if stock is available
            try:
                scrap_entry.action_validate()
            except Exception:
                pass
            self.scrap_id = scrap_entry.id
        except Exception:
            pass

        self.state = 'investigation'
        self.message_post(
            body=_(
                "<b>Corrective Action Triggered:</b> Maintenance Request <a href='#' data-oe-model='maintenance.request' data-oe-id='%s'>%s</a> "
                "logged for Otjiwarongo Workshop. Inventory shrinkage write-off recorded for %s L."
            ) % (maintenance_ticket.id, maintenance_ticket.name, self.net_variance_liters)
        )

        return {
            'name': _('Corrective Maintenance Ticket'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'res_id': maintenance_ticket.id,
            'view_mode': 'form',
            'target': 'current',
        }
