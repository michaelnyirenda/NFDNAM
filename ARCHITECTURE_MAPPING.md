# NFD & Petrosol: Excel-to-Odoo Architecture & Relational Mapping

## Executive Summary
This document defines the complete architectural mapping between Northern Fuel Distributors CC (NFD) & Petrosol Petroleum Solutions CC's master operational spreadsheets and the unified **Odoo 19 / Odoo 20** ERP data model. 

Every sheet, table, column header, business rule, and audit check across:
1. `Copy of Fuel Consumption 09 2026.xlsx` (44 sheets: Summary, Template, and 41 vehicle refuel logs)
2. `Copy of Vehicle Info New.xlsx` (9 sheets: Fleet Service, Projects, Availability, Driver Allocation, Driver Information, Breakdown Contacts, Branding, PTO, Wheel Alignment)

has been mapped to native Odoo relational models, views, menus, and automated workflows.

---

## 1. Master Sheet-to-Model Relational Matrix

| # | Excel Source Workbook & Sheet | Target Odoo Model | Odoo UI Menu & Layout | Direct Operational Mapping & Data Translation |
|---|---|---|---|---|
| 1 | **Fuel Consumption 09 2026.xlsx**<br>• `Summary` | `x_nfd_fuel_consumption_log`<br>(or `nfd.fuel.consumption.log`) | **NFD Fuel Logistics > Executive Dashboards & KPIs > Sept 2026 Excess Fuel & Otj COC Dashboard**<br>*(Pivot & Graph)* | Aggregates all 41 vehicle sheets using NFD's benchmark **Current Fuel Price Otj COC = NAD 25.98 / L** to compute fleet-wide distance, expected vs. actual KM/L, excess liters, and monetary penalty/savings. |
| 2 | **Fuel Consumption 09 2026.xlsx**<br>• `[Vehicle Reg]` (41 tabs) | `x_nfd_fuel_consumption_log`<br>(or `nfd.fuel.consumption.log`) | **NFD Fuel Logistics > Fleet Fuel Consumption (KM/L) > Vehicle Odometer & Refuel Logsheets (KM/L)**<br>*(List, Form & Kanban)* | Replicates daily refuel logs: Date, Odometer Start, Odometer End, Distance, Fuel (L), KM/L, Expected KM/L, Difference, Driver, Place, Confirm Logsheet (`X` vs confirmed), Confirm Stock, Notes. |
| 3 | **Vehicle Info New.xlsx**<br>• `FLEET SERVICE` | `fleet.vehicle` | **NFD Fuel Logistics > Fleet & Assets > Tankers & Rigids (Fleet Master)**<br>*(List & Form)* | Replicates master asset register: Truck Reg No, Comp 1, Comp 2, Type (Rigid, Tanker, Link, Drawbar, Pick-up), Department, Description, Diesel/ULP Capacity, Last Service Date & KMS, Service Intervals, Current KMS, and statutory expiry dates. |
| 4 | **Vehicle Info New.xlsx**<br>• `PROJECTS` | `maintenance.request` | **NFD Fuel Logistics > Fleet & Assets > Workshop Maintenance Work Orders & Job Cards**<br>*(Kanban, List & Form)* | Replicates Otjiwarongo workshop job card ledger: Job Card #, Reg No, Date In, Time In, Place (Main Workshop, NaTIS OTJ, CWWA Degas), Assigned To (Green, Clive, Japie, etc.), Job Type (Repair, Service, Roadworthy, Breakdown, Degass), Job Description, Parts Order, Supplier, and Hours/Days. |
| 5 | **Vehicle Info New.xlsx**<br>• `AVAILABLITY` | `fleet.vehicle` | **NFD Fuel Logistics > Fleet & Assets > Fleet Availability & Readiness Dashboard**<br>*(Search Filters & Group By)* | Replicates fleet readiness status groups: Active in Service, Rigid Trucks, Tankers, Standby Units, and Decommissioned / For Sale units (`10914`, `10915`, `10916`, `10919 Klaar - Maak reg vir verkoop`). |
| 6 | **Vehicle Info New.xlsx**<br>• `DRIVER ALLOCATION` | `fleet.vehicle` & `hr.employee` | **NFD Fuel Logistics > Fleet & Assets > Tankers & Rigids > Driver Allocations** | Links primary drivers (Niklas, Mike, Denzel, Simon, Oscar, etc.) and co-driver / trainee allocations (Nounongoue Kaaronda on Volvo FH440 `N 10544 OT`, Tobias Leopold on Mercedes rigid `N 4584 OT`) directly to assigned prime movers and trailers. |
| 7 | **Vehicle Info New.xlsx**<br>• `DRIVER INFORMATION` | `hr.employee` | **NFD Fuel Logistics > HESMS & Driver Safety > Hazchem Drivers & AA Compliance**<br>*(List & Form)* | Replicates the 34-driver compliance register: Namibian ID No, Start Date, Licence Code (CE, C, C1), Licence Expiry, PrDP Expiry, Medical Fitness Expiry, Hazchem Expiry, and Eye Test Expiry. Flags grounded drivers in real time. |
| 8 | **Vehicle Info New.xlsx**<br>• `BREAKDOWN CONTACTS` | `res.partner` | **NFD Fuel Logistics > Fleet & Assets > 24/7 Emergency Breakdown Network**<br>*(List & Search)* | Replicates NFD's vetted roadside contractor directory (33 partners) across 14 Namibian transport corridors (*Keetmanshoop, Mariental, Karibib, Omaruru, Windhoek, Walvis Bay, Usakos, Tsumeb, Grootfontein, Rundu, Katima Mulilo, Ondangwa, Kamanjab, Khorixas, Gobabis*). |
| 9 | **Vehicle Info New.xlsx**<br>• `BRANDING` | `fleet.vehicle` | **NFD Fuel Logistics > Fleet & Assets > Tankers & Rigids (Branding Filter)**<br>*(Field `x_branding_status` & Filter)* | Tracks vehicle and trailer exterior corporate branding status (*"Truck needs branding"*, *"Trailer needs branding"*, *"Truck & Trailer need branding"*). |
| 10 | **Vehicle Info New.xlsx**<br>• `PTO` | `fleet.vehicle` | **NFD Fuel Logistics > Fleet & Assets > Tankers & Rigids > Specifications Tab**<br>*(Fields `x_pto_type`, `x_pto_location`)* | Tracks PTO mechanism (Engine PTO, Hydraulic PTO, Both, None) and physical chassis mounting position (*"Behind the Cab"*, *"On Cab next to COC Tank"*, *"PTO Engine on Tanker"*). |
| 11 | **Vehicle Info New.xlsx**<br>• `Wheel Allignment Worksheet` | `maintenance.request` & `fleet.vehicle` | **NFD Fuel Logistics > Fleet & Assets > Maintenance Work Orders (Alignment Tasks)** | Tracks steering axle play, kingpin wear, V-bone bush wear, front diff play, and suspension re-torque schedules. |

---

## 2. Field-Level Data Dictionary

### 2.1 Model: `fleet.vehicle` (Master Asset Register)
- **`x_unit_classification`** (Selection): `prime_mover`, `rigid_tanker`, `semi_trailer`, `pup_trailer`, `drawbar_trailer`.
- **`x_max_volume_liters`** (Float): Maximum cargo volume.
- **`x_compartment_count`** (Integer): Isolated liquid compartments (1 to 7).
- **`x_has_diesel_meter`** (Boolean): Onboard calibrated digital delivery meter toggle.
- **`x_geotab_device_id`** (Char): OBC hardware serial number.
- **`x_manufacture_year`** (Integer): Production year for life-cycle tracking.
- **`x_vehicle_age`** (Integer, Computed): Current year minus manufacture year.
- **`x_replacement_policy_status`** (Selection, Computed): `compliant`, `warning`, `replace_due`.
  - Policy: Prime Movers < 18 years; Tankers & Trailers < 15 years. Warning triggers 1 year before limit.
- **`x_branding_status`** (Selection): `branded`, `truck_needs_branding`, `trailer_needs_branding`, `both_need_branding`.
  - Mapped directly from `BRANDING` sheet.
- **`x_driver_trainee_id`** (Many2one to `hr.employee`): Assigned co-driver or trainee driver on long-haul routes (e.g. Tobias Leopold, Nounongoue Kaaronda).
- **`driver_employee_id`** (Many2one to `hr.employee`): Primary assigned driver.
- **`x_trailer_comp1_id`** (Many2one to `fleet.vehicle`): Primary coupled trailer (Comp 1).
- **`x_trailer_comp2_id`** (Many2one to `fleet.vehicle`): Secondary coupled pup/drawbar trailer (Comp 2).
- **`x_pto_type`** (Selection): `hydraulic_pto`, `engine_pto`, `both`, `none`.
- **`x_pto_location`** (Char): Physical location (`Behind the Cab`, `On Cab next to COC Tank`, `PTO Engine on Tanker`).
- **`x_operational_availability`** (Selection): `active`, `standby`, `maintenance`, `accident`, `roadworthy`, `for_sale`.
- **Statutory Dates**:
  - `x_licence_expiry_date` (Date): Annual NaTIS license disk.
  - `x_fitness_certificate_expiry` (Date): Annual NaTIS roadworthy fitness certificate.
  - `x_safe_loading_pass_expiry` (Date): Oil industry Safe Loading Pass (SLP).
  - `x_pressure_test_expiry` (Date): 2.5/5-year hydrostatic pressure test.
  - `x_tanker_calibration_date` (Date): Depot meter & dip chart calibration.
  - `x_last_wheel_alignment_date` (Date): Laser wheel alignment date.

### 2.2 Model: `x_nfd_fuel_consumption_log` / `nfd.fuel.consumption.log` (Fuel Ledger)
- **`vehicle_id`** (Many2one to `fleet.vehicle`): Vehicle asset.
- **`driver_id`** (Many2one to `hr.employee`): Driver dispensing fuel.
- **`date`** (Date): Dispense date.
- **`odometer_start`** (Float): Trip start odometer (km).
- **`odometer_end`** (Float): Trip end odometer (km).
- **`distance_km`** (Float, Computed): Distance traveled in kilometers.
- **`fuel_liters`** (Float): Liters refueled.
- **`actual_km_per_liter`** (Float, Computed): Distance divided by Fuel Liters.
- **`expected_km_per_liter`** (Float): NFD standard target for vehicle class.
- **`difference_km_per_liter`** (Float, Computed): Expected minus Actual.
- **`excess_fuel_liters`** (Float, Computed): Actual Liters minus Expected Liters.
- **`excess_nad_value`** (Float, Computed): Excess Liters multiplied by Otj COC benchmark (NAD 25.98).
- **`confirm_logsheet`** (Selection): `confirmed` or `unconfirmed` (mapped from Excel `X`).
- **`confirm_stock`** (Boolean): Internal depot tank dispense verification.
- **`refuel_place`** (Char): Refueling depot or corridor town (Otjiwarongo, Walvis Bay, Windhoek, etc.).
- **`notes`** (Text): Driver or accounting notes (e.g., driver notes on odometer differences).

### 2.3 Model: `maintenance.request` (Workshop Job Cards)
- **`x_job_card_number`** (Char): Unique job card reference (e.g. `JC-1009`, `JC-1045`).
- **`vehicle_id`** (Many2one to `fleet.vehicle`): Target vehicle or trailer.
- **`x_service_location`** (Selection): `main_workshop`, `natis_otj`, `cwwa_degas`, `roadside`, `other`.
- **`x_assigned_mechanic_id`** (Many2one to `hr.employee`): Assigned mechanic (Green, Clive, Japie, Manie, Jonie).
- **`x_job_type`** (Selection): `repair`, `routine_service`, `roadworthy`, `breakdown`, `degas`.
- **`x_parts_supplier`** (Char): Supplier sourcing parts (MB Truck, Henred, NORS).
- **`x_parts_ordered`** (Boolean): Parts requisitioned.
- **`x_parts_received`** (Boolean): Parts delivered to workshop bay.
- **`x_labor_hours`** (Float): Total mechanic hours logged.

---

## 3. Dual Architecture Alignment

| Aspect | `main` Branch (Local Docker & Odoo.sh) | `saas-edu-import` Branch (Odoo Online edu-*.odoo.com) |
|---|---|---|
| **Language & Engine** | Python ORM + XML Views + Security Access | Declarative Pure XML (`data/ir_model_fields.xml`) + CSV |
| **Model Names** | `fleet.vehicle`, `nfd.fuel.dispatch.log`, `nfd.fuel.consumption.log` | `fleet.vehicle`, `x_nfd_fuel_dispatch_log`, `x_nfd_fuel_consumption_log` |
| **Field Prefixes** | Custom fields prefixed with `x_` | All custom model fields strictly prefixed with `x_` |
| **Computed Fields** | Python methods (`@api.depends`) | Declarative inline Python in XML (`<field name="compute">`) |
| **Security Directory** | Present (`security/ir.model.access.csv`) | **Completely purged** (disallowed by `base_import_module`) |
| **Packaging Automation** | Standard git commit / mount | Bundled via `scripts/sync_and_pack_saas.sh` into 48 KB zip |
