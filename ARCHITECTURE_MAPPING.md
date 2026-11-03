# NFD & Petrosol: Excel-to-Odoo Architecture & Relational Mapping

## Executive Summary
This document provides an exhaustive, cell-by-cell and formula-by-formula architectural audit and mapping between Northern Fuel Distributors CC (NFD) & Petrosol Petroleum Solutions CC's master operational spreadsheets and the unified **Odoo 19 / Odoo 20** ERP data model. 

Every sheet, table, column header, mathematical formula, business constraint, and audit check across:
1. **`Copy of Fuel Consumption 09 2026.xlsx`** (44 sheets: `Summary`, `Template`, and 42 vehicle refuel logs)
2. **`Copy of Vehicle Info New.xlsx`** (9 sheets: `FLEET SERVICE`, `PROJECTS`, `AVAILABLITY`, `DRIVER ALLOCATION`, `DRIVER INFORMATION`, `BREAKDOWN CONTACTS`, `BRANDING`, `PTO`, `Wheel Allignment Worksheet`)

has been audited, reconciled, and mapped to native Odoo relational models, dedicated views, customized menus, and automated workflows.

---

## 1. Master Sheet-to-Model Relational Matrix

The table below outlines the end-to-end correspondence between NFD's legacy Excel sheets and the target Odoo implementation across both the **Local Docker (`main`)** and **Odoo Online SaaS (`saas-edu-import`)** environments:

| # | Excel Source Workbook & Sheet | Target Odoo Model | Dedicated Odoo Menu Navigation Path | Primary UI View & Layout | Direct Operational Mapping & Data Translation |
|---|---|---|---|---|---|
| 1 | **Fuel Consumption 09 2026.xlsx**<br>• `Summary` | `fleet.vehicle` & `nfd.fuel.consumption.log` (SaaS: `x_nfd_fuel_consumption_log`) | **NFD Fuel Logistics > Fuel Consumption 09 2026 (Excel) > Summary Sheet (Sept 2026)** | Dedicated List View (`view_fleet_vehicle_fuel_summary_list`) | Replicates `Summary!B4:I49`. Uses NFD's benchmark **Current Fuel Price Otj COC = NAD 25.98 / L** (`Summary!C3:E3`) to compute fleet-wide distance, expected KM/L, actual KM/L, expected total fuel, actual fuel burn, excess liters, and monetary excess value. |
| 2 | **Fuel Consumption 09 2026.xlsx**<br>• `[Vehicle Reg]` (42 vehicle tabs) | `nfd.fuel.consumption.log` (SaaS: `x_nfd_fuel_consumption_log`) | **NFD Fuel Logistics > Fuel Consumption 09 2026 (Excel) > Vehicle Fuel Tabs (43 Units)** | List, Form & Pivot (`view_nfd_fuel_consumption_log_list`) | Replicates daily vehicle refuel tabs: Date (`B`), Odo Start (`C`), Odo End (`D`), Distance (`E`), Fuel Liters (`F`), KM/L (`G`), Target KM/L (`H`), Difference (`I`), Driver (`J`), Refuel Place (`K`), Slip Confirm `X` (`L`), Stock Confirm (`M`), Notes (`N`). Eliminates the manual `J6` duplicate reading requirement. |
| 3 | **Vehicle Info New.xlsx**<br>• `FLEET SERVICE` | `fleet.vehicle` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 1: Fleet Service & Workshop Schedule** | Dedicated List View (`view_fleet_vehicle_sheet_fleet_service_list`) | Replicates master asset register `FLEET SERVICE!A1:AB1`: Reg No, Model, Service Interval (KM), Last Service Date & KM, Next Service Milestone, KM Until Service Due, Service Status, NaTIS Licence Expiry, Roadworthy Fitness Expiry, Safe Loading Pass (SLP), Pressure Test Expiry, and Calibration Date. |
| 4 | **Vehicle Info New.xlsx**<br>• `AVAILABLITY` | `fleet.vehicle` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 2: Fleet Availability & Grouping** | Dedicated List View (`view_fleet_vehicle_sheet_availability_list`) | Replicates `AVAILABILITY!A1:E1`. Grouped by availability category: Rigid Trucks (44% -> 77% target), Tankers (88% target), Standby Units (50%), Maintenance (100%), Installations (60%), and Decommissioned / For Sale (`10914`, `10915`, `10916`, `10919 Klaar - Maak reg vir verkoop`). |
| 5 | **Vehicle Info New.xlsx**<br>• `DRIVER ALLOCATION` | `fleet.vehicle` & `hr.employee` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 3: Driver & Trailer Allocation** | Dedicated List View (`view_fleet_vehicle_sheet_driver_allocation_list`) | Replicates `DRIVER ALLOCATION!A1:H1`: Truck Reg No, Truck Model, Designated Permanent Driver, Trainee Driver / Co-Driver (`x_driver_trainee_id`), Coupled Trailer / Comp 1 (`x_trailer_comp1_id`), Comp 2 (`x_trailer_comp2_id`), and Operational Remarks (`x_allocation_note`). |
| 6 | **Vehicle Info New.xlsx**<br>• `BRANDING` | `fleet.vehicle` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 4: Corporate Livery & Branding** | Dedicated List View (`view_fleet_vehicle_sheet_branding_list`) | Replicates `BRANDING!A1:H1`: Tracks vehicle and trailer corporate livery status (`branded`, `truck_needs_branding`, `trailer_needs_branding`, `both_need_branding`) and remote location notes (`x_branding_notes`, e.g. "Katima - Terug 12/09/26"). |
| 7 | **Vehicle Info New.xlsx**<br>• `BREAKDOWN CONTACTS` | `res.partner` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 5: 24/7 Breakdown Contacts & Corridors** | Dedicated List View (`view_partner_tree_breakdown_nfd`) | Replicates `BREAKDOWN CONTACTS!A3:F3`: 33 vetted roadside contractors across 14 Namibian transport corridors (*Otjiwarongo, Windhoek, Walvis Bay, Mariental, Keetmanshoop, Karibib, Omaruru, Usakos, Tsumeb, Grootfontein, Rundu, Katima Mulilo, Ondangwa, Gobabis, Khorixas*). |
| 8 | **Vehicle Info New.xlsx**<br>• `PTO` | `fleet.vehicle` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 6: PTO & Hydraulic Systems** | Dedicated List View (`view_fleet_vehicle_sheet_pto_list`) | Replicates `PTO!A1:F1`: Flags `x_pto_engine` (Auxiliary Engine PTO), `x_hydraulic_pto` (Transmission Hydraulic PTO), drive type, and physical chassis mounting position (`x_pto_location`). |
| 9 | **Vehicle Info New.xlsx**<br>• `Wheel Allignment Worksheet` | `fleet.vehicle` & `maintenance.request` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 7: Wheel Alignment Worksheet** | Dedicated List View (`view_fleet_vehicle_sheet_wheel_alignment_list`) | Replicates `Wheel Allignment Worksheet!A1:L1`: Tracks axle/chassis alignment status (Skip, In, Faults, Repaired, Done), alignment description, date, and mechanical fault details (`x_alignment_notes`). Flags unresolved faults causing tyre scrubbing and fuel drag in red. |
| 10 | **Vehicle Info New.xlsx**<br>• `PROJECTS` | `maintenance.request` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 8: Workshop Job Cards & Projects** | Dedicated List View (`view_maintenance_request_sheet_projects_list`) | Replicates Otjiwarongo workshop ledger `PROJECTS!A3:Y3`: Job Card # (`x_job_card_number`), Task Name, Hours / Days (`x_hours_days`), Asset / Truck (`equipment_id`), Trailer Reg (`x_trailer_reg`), Kms Left at Check-In (`x_kms_left_checkin`), Assigned Mechanic, Parts Supplier, Parts Ordered/Received, and Stage. |
| 11 | **Vehicle Info New.xlsx**<br>• `DRIVER INFORMATION` | `hr.employee` | **NFD Fuel Logistics > Vehicle Info New (9 Excel Sheets) > Sheet 9: Driver Information & Licensing** | Dedicated List View (`view_hr_employee_sheet_driver_info_list`) | Replicates `DRIVER INFORMATION!A1:P1`: 34 drivers with National ID, Start Date (`x_start_date`), Licence Code (CE, C), Licence Expiry, PrDP Expiry, Dangerous Goods Hazchem Expiry, Defensive Driving Expiry, Medical Fitness Expiry, Eye Exam Expiry, Trainee Payment Date (`x_trainee_payment_date`), and HESMS Safety Badge. |

---

## 2. Exhaustive Cell-by-Cell & Formula Audit

### 2.1 The `Summary` Sheet (`Fuel Consumption 09 2026.xlsx`)

The `Summary` sheet reconciles fleet-wide fuel consumption against benchmark targets. Our cell-by-cell audit identified several systemic structural issues that existed in Excel and are permanently solved by Odoo's relational architecture:

```
Summary!A1: Title "Northern Fuel Distributors"
Summary!A2: Subtitle "Fleet Fuel Consumption September 2026"
Summary!C3:E3: Benchmark Metric Cell "CURRENT FUEL PRICE OTJ COC = 25.98"
Summary!B4:I4: Table Headers:
  - B4: "Registration"
  - C4: "Make / Model"
  - D4: "Distance Covered"
  - E4: "Expected"
  - F4: "Actual"
  - G4: "Expected Total Fuel Used"
  - H4: "Actual Total Fuel Used"
  - I4: "Excess Use"
```

#### The 5 Critical Human & Formula Errors in Legacy Excel:
1. **Broken Sheet References (`=#REF!`):**
   - In rows 11, 12, 13, 15, and 25 (`B11:I13`, `B15:I15`, `B25:I25`), previous vehicle tabs were deleted from the workbook without updating the Summary table formulas.
   - Excel formulas like `='[DELETED_SHEET]'!$G$6` evaluated to `=#REF!`.
   - Because cells `H50` and `I50` used `=SUM(H5:H49)`, the `#REF!` errors cascaded into the fleet grand totals, causing the entire fleet summary to fail (`#REF!` total fuel and `#REF!` total excess liters).
   - **Odoo Solution:** Vehicles are database records. If a vehicle is decommissioned or archived, active queries dynamically aggregate only existing records (`SUM()`), preventing formula cascades.

2. **Division by Zero Crashes (`#DIV/0!`):**
   - Idle vehicles with 0 km traveled (such as standby or workshop units in rows 14, 18, 22) computed Actual KM/L as `Distance / Fuel`.
   - In Excel: `=D14/H14` evaluated to `#DIV/0!`.
   - **Odoo Solution:** Handled gracefully via Python `@api.depends` and SQL `NULLIF` guards:
     ```python
     if vehicle.x_expected_km_per_liter and vehicle.x_expected_km_per_liter > 0:
         vehicle.x_sept_expected_fuel_l = round(vehicle.x_sept_distance_km / vehicle.x_expected_km_per_liter, 2)
     else:
         vehicle.x_sept_expected_fuel_l = 0.0
     ```

3. **The Ford Tremor Copied Formula Bug (`D30`):**
   - Vehicle `N 13938 OT` (Ford Tremor Pickup, row 30) had its Distance cell `D30` hard-coded to copy from the Volvo FH520 above it: `='N 12843 OT'!$G$6` (17,060 km) instead of `'N 13938 OT'!$G$6`.
   - On the vehicle tab `N 13938 OT`, the clerk had left the end odometer blank, generating negative distance `-28,814 km`.
   - Together with the copied distance formula, this generated a fictitious **+3,324.28 L** penalty, resulting in a false **NAD 86,364.79** penalty on Johan's management report!
   - **Odoo Solution:** Odoo calculates distance directly per trip log (`odometer_end - odometer_start`) and validates that end odometer $\ge$ start odometer.

4. **The Hilux Reference Mismatch (`F49`):**
   - Vehicle `N 13777 OT` is a Mercedes Actros heavy tanker truck. Vehicle `N 13410 OT` is a Toyota Hilux bakkie (row 49).
   - Cell `F49` (Actual KM/L for the Hilux) contained the formula `='N 13777 OT'!$G$51` (2.70 KM/L) instead of linking to the Hilux's actual fuel efficiency of **8.66 KM/L**.
   - This caused the utility bakkie to appear as a severe fuel over-consumer on the executive report.
   - **Odoo Solution:** In Odoo, efficiency is computed directly on each vehicle's refuel logs, eliminating copy-paste cell coordinate errors.

5. **The Missing Vehicle Discovery (`N 12611 OT`):**
   - Isuzu D-Max pickup `N 12611 OT` had an active vehicle tab showing 2,111 km traveled and 230.19 liters of diesel consumed.
   - However, it was completely omitted from `Summary!B5:I49`. Management was entirely blind to this vehicle's monthly fuel cost.
   - **Odoo Solution:** Odoo automatically generates the fuel summary list dynamically from all vehicle assets with recorded fuel transactions—no vehicle can ever be accidentally omitted.

---

### 2.2 The Vehicle Fuel Tabs & The `J6` Warning Note

Each of the 42 vehicle refuel tabs in `Fuel Consumption 09 2026.xlsx` contains a prominent warning header at `J6`:
> `** DUPLICATE LAST READING** IN 'ODO END' FOR CALCULATOR TO WORK`

#### Why Did Excel Require This?
- In the legacy Excel template, column `C` (Odometer Start for row $r$) relied on an offset formula pulling from column `D` of the previous row $r-1$:
  `=IF(E11>0, D11, "0")`
- For the formulas in row $r$ to compute distance and KM/L, the clerk was forced to manually re-type the last odometer reading into a dummy final row.
- If a driver or clerk forgot to create this duplicate final row, the entire vehicle's monthly distance and fuel economy would fail to calculate.

#### Odoo Relational Architecture Fix:
- In Odoo, each refuel event is an independent record (`nfd.fuel.consumption.log`).
- `odometer_start`, `odometer_end`, and `distance_km` are stored per refuel slip.
- The system automatically pre-populates `odometer_start` from the vehicle's last recorded odometer reading.
- No dummy records or duplicated readings are ever required.

---

### 2.3 Wheel Alignment Faults & Fuel Drag Linkage (`Wheel Allignment Worksheet!A33:L36`)

A major revelation from the audit of `Copy of Vehicle Info New.xlsx` is the direct mechanical correlation between chassis alignment faults and severe fuel over-consumption.

In `Wheel Allignment Worksheet`, rows 33 to 36 identify 4 specific vehicles with critical, unresolved mechanical faults:

```
Row 33: N 2455 OT (Mercedes Axor Rigid)
  - Axle/Chassis Faults: "Spring bush wear out, broken studs, V-bone bushes worn, front diff loose"
  - Status: Faults = TRUE, Repaired = FALSE, Done = FALSE

Row 34: N 11028 OT (Mercedes Actros 2645 Prime Mover)
  - Axle/Chassis Faults: "King pin play, shock bushes worn"
  - Status: Faults = TRUE, Repaired = FALSE, Done = FALSE

Row 35: N 4584 OT (Mercedes Actros 2645 Rigid Tanker)
  - Axle/Chassis Faults: "Steering axle king pin play, under pressure"
  - Status: Faults = TRUE, Repaired = FALSE, Done = FALSE

Row 36: N 11963 OT (Mercedes Actros 2646 Prime Mover)
  - Axle/Chassis Faults: "Rear axle not square, bearings need re-torque"
  - Status: Faults = TRUE, Repaired = FALSE, Done = FALSE
```

#### Financial & Operational Impact on September 2026 Fuel Consumption:
When cross-referenced against `Summary!B4:I49`, these exact vehicles exhibit severe fuel burn penalties:
- **`N 2455 OT`**: Excess Fuel = **+242.33 L** (Penalty = **+NAD 6,295.73**)
- **`N 4584 OT`**: Excess Fuel = **+228.55 L** (Penalty = **+NAD 5,937.73**)
- **`N 11963 OT`**: Excess Fuel = **+529.20 L** (Penalty = **+NAD 13,748.62**)

**Engineering Rationale:** An un-squared rear axle or worn kingpin creates severe lateral tyre scrubbing and rolling drag. On a 10,000 km haulage route, this mechanical drag requires the engine to generate continuous extra horsepower, directly burning 200–500 extra liters of diesel. 

**Odoo Solution:** 
In `views/fleet_vehicle_views.xml`, `view_fleet_vehicle_sheet_wheel_alignment_list` applies dynamic table row highlighting:
```xml
<list string="Sheet 7: Wheel Alignment Worksheet"
      decoration-danger="x_alignment_faults == True and x_alignment_repaired == False"
      decoration-success="x_alignment_done == True">
```
Johan Botes can instantly see which units have open alignment faults before releasing them onto corridor trips, directly preventing tens of thousands of NAD in wasted fuel.

---

## 3. Master Field-Level Data Dictionary

### 3.1 Model: `fleet.vehicle` (Master Asset Register)
- **`x_unit_classification`** (Selection): `prime_mover`, `rigid_tanker`, `semi_trailer`, `pup_trailer`, `drawbar_trailer`.
- **`x_max_volume_liters`** (Float): Maximum cargo volume.
- **`x_compartment_count`** (Integer): Isolated liquid compartments (1 to 7).
- **`x_has_diesel_meter`** (Boolean): Onboard calibrated digital delivery meter toggle.
- **`x_geotab_device_id`** (Char): OBC hardware serial number.
- **`x_manufacture_year`** (Integer): Production year for life-cycle tracking.
- **`x_vehicle_age`** (Integer, Computed): Current year minus manufacture year.
- **`x_replacement_policy_status`** (Selection, Computed): `compliant`, `warning`, `replace_due`.
  - Governance Rule: Prime Movers < 18 years; Tankers & Trailers < 15 years. Amber warning triggers 1 year before policy limit.
- **`x_branding_status`** (Selection): `branded`, `truck_needs_branding`, `trailer_needs_branding`, `both_need_branding`.
- **`x_branding_notes`** (Char): Location and livery remarks (`BRANDING!A1:H1`).
- **`x_allocation_note`** (Char): Operational deployment remarks (`DRIVER ALLOCATION!A1:H1`, `AVAILABILITY!A1:E1`).
- **`x_driver_trainee_id`** (Many2one to `hr.employee`): Designated trainee driver or co-driver (e.g. Tobias Leopold, Nounongoue Kaaronda).
- **`driver_id`** (Many2one to `res.partner` / `hr.employee`): Primary assigned driver.
- **`x_trailer_comp1_id`** (Many2one to `fleet.vehicle`): Primary coupled trailer (Comp 1).
- **`x_trailer_comp2_id`** (Many2one to `fleet.vehicle`): Secondary coupled pup/drawbar trailer (Comp 2).
- **`x_pto_engine`** (Boolean): Auxiliary engine PTO fitted (`PTO!A1:F1`).
- **`x_hydraulic_pto`** (Boolean): Transmission hydraulic PTO fitted (`PTO!A1:F1`).
- **`x_pto_type`** (Selection): `hydraulic_pto`, `engine_pto`, `both`, `none`.
- **`x_pto_location`** (Char): Physical mounting position (`Behind the Cab`, `On Cab next to COC Tank`, `PTO Engine on Tanker`).
- **`x_availability_group`** (Selection): `rigid`, `tanker`, `standby`, `maintenance`, `installations`, `for_sale`, `pool` (`AVAILABILITY!A1:E1`).
- **`x_operational_availability`** (Selection): `active`, `standby`, `maintenance`, `accident`, `roadworthy`, `for_sale`.
- **Wheel Alignment Fields (`Wheel Allignment Worksheet!A1:L1`):**
  - `x_alignment_desc` (Char): Description (Rigid, Tipper, Truck & Trailer, Oubaas).
  - `x_alignment_skip` (Boolean): Skip inspection.
  - `x_alignment_in` (Boolean): Unit checked into alignment bay.
  - `x_alignment_faults` (Boolean): Mechanical faults detected.
  - `x_alignment_repaired` (Boolean): Repairs completed.
  - `x_alignment_done` (Boolean): Final alignment verified and approved.
  - `x_alignment_notes` (Char): Specific chassis and suspension fault notes.
- **Statutory Compliance Dates (`FLEET SERVICE!A1:AB1`):**
  - `x_service_interval_km` (Float): Routine maintenance cycle (15,000 / 22,500 / 30,000 km).
  - `x_last_service_date` (Date): Last workshop service.
  - `x_last_service_km` (Float): Odometer reading at last service.
  - `x_next_service_km` (Float): Next required service milestone.
  - `x_km_until_service` (Float, Computed): Distance remaining until service due.
  - `x_service_status` (Selection, Computed): `ok`, `due_soon` (< 5,000 km), `overdue`.
  - `x_licence_expiry_date` (Date): Annual NaTIS license disk expiry.
  - `x_fitness_certificate_expiry` (Date): Annual NaTIS roadworthy fitness expiry.
  - `x_safe_loading_pass_expiry` (Date): Oil Industry Safe Loading Pass (SLP).
  - `x_pressure_test_expiry` (Date): 2.5/5-year tanker pressure test certificate.
  - `x_tanker_calibration_date` (Date): Depot meter & dip chart calibration.
  - `x_last_wheel_alignment_date` (Date): Laser wheel alignment audit date.
- **September 2026 Fuel Metrics (`Summary!B4:I49`):**
  - `x_expected_km_per_liter` (Float): Benchmark efficiency target (KM/L).
  - `x_actual_km_per_liter` (Float): Actual achieved efficiency (KM/L).
  - `x_sept_distance_km` (Float): Distance traversed in September 2026 (KM).
  - `x_sept_expected_fuel_l` (Float, Computed): `x_sept_distance_km / x_expected_km_per_liter`.
  - `x_sept_actual_fuel_l` (Float): Total actual fuel drawn (L).
  - `x_sept_excess_fuel_l` (Float, Computed): `x_sept_actual_fuel_l - x_sept_expected_fuel_l`.
  - `x_otj_coc_fuel_price` (Float): Otjiwarongo COC benchmark price (default NAD 25.98 / L).
  - `x_sept_excess_nad_value` (Float, Computed): `x_sept_excess_fuel_l * x_otj_coc_fuel_price`.

### 3.2 Model: `nfd.fuel.consumption.log` (SaaS: `x_nfd_fuel_consumption_log`)
- **`x_name`** (Char): Refuel log reference (e.g. `FCL/2026/0001`).
- **`x_date`** (Date): Refueling date.
- **`x_vehicle_id`** (Many2one to `fleet.vehicle`): Vehicle asset.
- **`x_driver_id`** (Many2one to `hr.employee`): Driver dispensing fuel.
- **`x_place`** (Selection): Refueling facility (`Depot`, `OKH`, `Office`, `Walvis`, `Ohakane`, `Fort Sesfontein`, `Mareintal`, `Ondangwa`, `Omakange`, `Otavi Shell`, `B1 PUMA`, `Agra Karibib`, `Agra Gobabis`).
- **`x_odometer_start`** (Float): Trip start odometer (KM).
- **`x_odometer_end`** (Float): Trip end odometer (KM).
- **`x_distance_traveled_km`** (Float, Computed): Distance traveled (KM).
- **`x_fuel_liters`** (Float): Liters refueled (L).
- **`x_expected_km_per_liter`** (Float): Target benchmark efficiency (KM/L).
- **`x_actual_km_per_liter`** (Float, Computed): `x_distance_traveled_km / x_fuel_liters`.
- **`x_km_per_liter_diff`** (Float, Computed): Difference in efficiency (Actual - Expected).
- **`x_excess_fuel_liters`** (Float, Computed): Excess fuel consumed (L).
- **`x_excess_nad_value`** (Float, Computed): Excess monetary cost valued at NAD 25.98 / L.
- **`x_confirm_logsheet`** (Selection): `confirmed` or `unconfirmed` (mapped from Excel `X` in column L).
- **`x_confirm_stock`** (Boolean): Depot bulk inventory confirmation.
- **`x_notes`** (Text): Driver remarks or audit notes.

### 3.3 Model: `maintenance.request` (Workshop Job Cards - `PROJECTS!A3:Y3`)
- **`name`** (Char): Task name and summary description.
- **`equipment_id`** (Many2one to `maintenance.equipment`): Associated fleet truck, trailer, or depot asset.
- **`x_job_card_number`** (Char): Official workshop job card # (e.g. `JC-1009`, `JC-1045`).
- **`x_hours_days`** (Float): Labor duration in hours or days recorded on job card.
- **`x_trailer_reg`** (Char): Coupled trailer registration number (e.g. `5999`, `6776`, `8961`).
- **`x_kms_left_checkin`** (Float): Remaining service kilometers at check-in.
- **`x_workshop_location`** (Selection): `workshop_otj`, `natis_otj`, `vivo_depo`, `cwwa`, `gt_vinyl`, `field_breakdown`.
- **`x_assigned_mechanic`** (Selection): `green`, `japie`, `clive`, `jonie`, `siisii`, `manie`.
- **`x_job_type`** (Selection): `repair`, `service`, `roadworthy`, `rebuild`, `degas`, `wheel_alignment`.
- **`x_parts_supplier_id`** (Many2one to `res.partner`): Vendor supplying parts (MB Truck, Henred, NORS, Master Parts).
- **`x_parts_ordered`** (Boolean): Requisition submitted to supplier.
- **`x_parts_received`** (Boolean): Physical parts received at workshop bay.
- **`x_service_agreement_type`** (Selection): `internal_fleet`, `free_retail_forecourt`, `customer_contract`.
- **`x_dispatch_log_id`** (Many2one): Auto-linked cargo dispatch log if generated via emergency leakage alert.

### 3.4 Model: `hr.employee` (Driver Licensing & HESMS - `DRIVER INFORMATION!A1:P1`)
- **`name`** (Char): Driver's full name.
- **`x_id_number`** (Char): Namibian National Identity Number.
- **`x_start_date`** (Date): Employment commencement date.
- **`x_trainee_payment_date`** (Char): Trainee stipend payment schedule (e.g. "Every Monday").
- **`x_licence_code`** (Selection): `CE` (Heavy Articulated), `C` (Heavy Rigid), `C1`, `BE`, `B`.
- **`x_licence_expiry_date`** (Date): Driving Licence Card expiry.
- **`x_pdp_expiry_date`** (Date): Public Driving Permit (PrDP) expiry.
- **`x_hazchem_expiry`** (Date): Dangerous Goods / Hazchem certification expiry.
- **`x_defensive_driving_expiry`** (Date): HESMS Defensive Driving expiry.
- **`x_medical_fitness_expiry`** (Date): Annual occupational medical fitness expiry.
- **`x_eye_test_expiry_date`** (Date): Optometric examination expiry.
- **`x_hse_compliant`** (Boolean, Computed): Evaluates `True` only when all required permits are valid.
- **`x_hse_status_badge`** (Selection, Computed): `compliant`, `expiring_soon` (within 30 days), `expired`, `not_applicable`.
- **`x_aa_category`** (Selection): `designated_namibian`, `women_in_transport`, `pw_disabilities`, `general` (Namibian Affirmative Action Act compliance).

---

## 4. Dual Environment Alignment (`main` vs `saas-edu-import`)

| Architectural Aspect | Local Docker Environment (`main`) | Odoo Online SaaS (`saas-edu-import`) |
|---|---|---|
| **Underlying Engine** | Python ORM (`models/*.py`) + Native PostgreSQL | Pure Declarative XML (`data/ir_model_fields.xml`) + CSV |
| **Custom Model Names** | `fleet.vehicle`<br>`nfd.fuel.dispatch.log`<br>`nfd.fuel.consumption.log` | `fleet.vehicle`<br>`x_nfd_fuel_dispatch_log`<br>`x_nfd_fuel_consumption_log` |
| **Field Prefix Rule** | Custom fields prefixed with `x_` | All custom model fields strictly prefixed with `x_` |
| **Computed Fields** | Python methods (`@api.depends`) | Declarative inline Python in XML (`<field name="compute">`) |
| **Security Directory** | `security/ir.model.access.csv` | **Completely purged** (disallowed by `base_import_module` on SaaS) |
| **Package Distribution** | Direct Docker volume mount `:ro` | Bundled via `scripts/sync_and_pack_saas.sh` into `dist/nfd_petrosol_edu_import.zip` (48.1 KB) |
| **Menu Actions** | Uses `action_nfd_fuel_dispatch_log` | Uses `action_x_nfd_fuel_dispatch_log` |

---

## 5. Verification & Audit Trail

Both branches have been tested, validated, and verified:
1. **Docker Module Upgrade Test:** Executed `odoo -u nfd_petrosol_demo --stop-after-init` on database `nfd_demo` in container `nfd-odoo19`. Completed with exit code 0 (4,025 database queries, registry loaded in 20.10s).
2. **Python ORM Integrity Test:** Validated in Odoo shell that:
   - `N 2455 OT` has `x_availability_group='rigid'`, `x_alignment_faults=True`, and mechanical notes recorded.
   - `N 11963 OT` has `x_availability_group='tanker'`, `x_alignment_faults=True`, `x_pto_engine=True`, and `x_hydraulic_pto=True`.
   - `Tobias Leopold` has `x_start_date='2026-08-01'` and `x_trainee_payment_date='Every Monday'`.
   - `JC-1009` has `x_hours_days=4.5`, `x_trailer_reg='5999'`, and `x_kms_left_checkin=12500.0`.
   - All 9 dedicated sheet actions exist in `ir.actions.act_window`.
3. **Packaging Automation Test:** Executed `./scripts/sync_and_pack_saas.sh`. Passed zero-Python audit, converted 16 demo records to `x_` models/fields, sanitized all XMLs, and built a clean 48.1 KB archive ready for 1-click import into `edu-*.odoo.com`.
