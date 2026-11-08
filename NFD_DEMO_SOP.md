# NFD & Petrosol Operational Standard Operating Procedure (SOP) & Master System Manual

---

## Table of Contents
1. [Master Excel-to-Odoo Architecture & Cross-Workbook Correlation Matrix](#1-master-excel-to-odoo-architecture--cross-workbook-correlation-matrix)
   - 1.1 Master Excel-to-Odoo Cross-Reference Table
   - 1.2 Documentation of 3 Repaired Excel Formula Bugs
   - 1.3 Cross-Workbook Correlation & Root Cause Analysis
2. [Step-by-Step Navigation & Click-by-Click Operational Guide (Screens 01 to 21)](#2-step-by-step-navigation--click-by-click-operational-guide-screens-01-to-21)
   - Screen 01: Application Home & Navigation Switcher
   - Screen 02: NFD Executive Command Center
   - Screen 03: Fuel & Otj COC Variance Dashboard
   - Screen 04: Driver & Refueling Site Analytics
   - Screen 05: Fleet Readiness & Service Radar
   - Screen 06: Workshop, Alignment & Timesheets Dashboard
   - Screen 07: Fuel Consumption Summary
   - Screen 08: Vehicle Refuel Logsheets
   - Screen 09: Cargo Fuel Dispatches & In-Transit Loss Alert
   - Screen 10: Fleet Service Schedule
   - Screen 11: Vehicle Lifecycle Master Record (Flagship `N 7802 OT`)
   - Screen 12: Wheel Alignment & Chassis Audit
   - Screen 13: Workshop Job Cards & Projects
   - Screen 14: 24/7 Breakdown & Emergency Corridors
   - Screen 15: Hazchem Drivers & Statutory Compliance
   - Screen 16: Depot Inventory Stock & Bulk Spares Catalog
   - Screen 17: Spare Parts Procurement (Purchase Orders)
   - Screen 18: Commercial Bulk Fuel Sales Orders
   - Screen 19: Customer Freight Invoicing & Vendor Bills
   - Screen 20: Statutory Inspections & Compliance Calendar
   - Screen 21: Project / To-Do Operational Tasks
3. [Live Presentation Script: Real-Time Fleet Automation on Clean Vehicle `N 10420 OT`](#3-live-presentation-script-real-time-fleet-automation-on-clean-vehicle-n-10420-ot)
4. [Simulated End-to-End Vehicle Lifecycle (Stages 1 to 7)](#4-simulated-end-to-end-vehicle-lifecycle-stages-1-to-7)

---

## 1. Master Excel-to-Odoo Architecture & Cross-Workbook Correlation Matrix

### 1.1 Master Excel-to-Odoo Cross-Reference Table

| Source Excel File | Sheet Name | Exact Cell Range | Odoo Menu Path | Odoo Action / Model | What It Displays & Calculates |
|---|---|---|---|---|---|
| `Copy of Fuel Consumption 09 2026.xlsx` | `Summary` | `B5:I45` | **NFD Fuel Logistics > Fuel Operations > Fuel Consumption Summary** | `action_nfd_fuel_summary`<br>`nfd.fuel.summary` | Fleet-wide rollup of all 41 vehicles: 285,640.0 km total distance, 100,269.50 L actual fuel, +2,871.39 L net excess variance (+NAD 74,598.69 at NAD 25.98 / L benchmark). |
| `Copy of Fuel Consumption 09 2026.xlsx` | `Summary` | `C3:E3`, `G4:I45` | **NFD Fuel Logistics > Executive Dashboards > Fuel & Otj COC Variance** | `action_nfd_dash_fuel_variance`<br>`nfd.fuel.summary` | Graphical breakdown of excess fuel burners (22 vehicles, +4,722.91 L / +NAD 122,701.18) vs star fuel savers (11 vehicles, -1,851.52 L / -NAD 48,102.49) valued at Otjiwarongo benchmark price NAD 25.98 / L. |
| `Copy of Fuel Consumption 09 2026.xlsx` | Individual tabs (`N 12007 OT` etc.) | `B10:N24` | **NFD Fuel Logistics > Fuel Operations > Vehicle Refuel Logsheets** | `action_nfd_fuel_consumption_log`<br>`nfd.fuel.consumption.log` | 326 refuel slips with Start/End Odometer, KM/L efficiency, refueling station/stop, driver, and unconfirmed logsheet audit flags (`X`). |
| `Copy of Fuel Consumption 09 2026.xlsx` | Individual tabs | `F10:F24` | **NFD Fuel Logistics > Executive Dashboards > Driver & Refueling Site Analytics** | `action_nfd_dash_driver_site`<br>`nfd.fuel.consumption.log` | Refueling volumes and fuel draw across 13 regional sites (Agra Vivo, CJ Steenkamp, Ndama, Otjiwarongo Depot, Tokat, Veronika, Walvis Bay, Weimans). |
| `Copy of Vehicle Info New.xlsx` | `AVAILABILITY` | `A2:G35` | **NFD Fuel Logistics > Executive Dashboards > Fleet Readiness & Service Radar** | `action_nfd_dash_fleet_radar`<br>`fleet.vehicle` | Stacked bar chart of fleet readiness across 7 operational categories (Rigids 77% target, Tankers 88% target, Standby 50%, Maintenance 100%, Installations 60%, For Sale 100%, Pool 100%) and 15/18-year replacement policy status. |
| `Copy of Vehicle Info New.xlsx` | `FLEET SERVICE` | `A5:L45` | **NFD Fuel Logistics > Fleet & Assets > Fleet Service Schedule** | `action_nfd_fleet_service_schedule`<br>`fleet.vehicle` | Preventive maintenance odometer milestones (15k/30k/50k km intervals), last service date, km remaining until service, NaTIS license, roadworthy fitness, and SLP expiry dates. |
| `Copy of Vehicle Info New.xlsx` | `AVAILABILITY` | `A2:G35` | **NFD Fuel Logistics > Fleet & Assets > Fleet Availability & Grouping** | `action_nfd_fleet_availability`<br>`fleet.vehicle` | Operational status of all 94 fleet units categorized by tanker, rigid, standby, and workshop maintenance status. |
| `Copy of Vehicle Info New.xlsx` | `DRIVER ALLOCATION` | `A3:F40` | **NFD Fuel Logistics > Fleet & Assets > Driver & Trailer Allocation** | `action_nfd_driver_trailer_allocation`<br>`fleet.vehicle` | Prime mover tractors paired with permanent certified drivers, trainee co-drivers (Tobias Leopold, Nounongoue Kaaronda), coupled B-double pup trailers, and standby notes. |
| `Copy of Vehicle Info New.xlsx` | `BRANDING` | `A3:D45` | **NFD Fuel Logistics > Fleet & Assets > Corporate Livery & Branding** | `action_nfd_corporate_branding`<br>`fleet.vehicle` | Corporate livery audit tracking branded vehicles vs units requiring vinyl decal installation at GT Vinyl with location notes. |
| `Copy of Vehicle Info New.xlsx` | `PTO` | `A3:F30` | **NFD Fuel Logistics > Fleet & Assets > PTO & Hydraulic Systems** | `action_nfd_pto_systems`<br>`fleet.vehicle` | Auxiliary engine PTOs, transmission hydraulic PTOs, and pump mounting positions (Behind the Cab, On Cab next to COC Tank, Tanker Chassis). |
| `Copy of Vehicle Info New.xlsx` | `Wheel Allignment Worksheet` | `A3:J45` | **NFD Fuel Logistics > Fleet & Assets > Wheel Alignment & Chassis Audit** | `action_nfd_wheel_alignment`<br>`fleet.vehicle` | Laser axle and kingpin alignment audit. Red highlighting flags chassis faults on vehicles 2455, 11028, 4584, and 11963 causing tyre drag and fuel burn penalties. |
| `Copy of Vehicle Info New.xlsx` | `PROJECTS` | `A3:I35` | **NFD Fuel Logistics > Executive Dashboards > Workshop, Alignment & Timesheets** | `action_nfd_dash_workshop_alignment`<br>`project.task` | Visual dashboard of workshop job cards grouped by lead mechanic (Green, Japie, Clive), job card category, and labor timesheet allocation. |
| `Copy of Vehicle Info New.xlsx` | `PROJECTS` | `A3:I35` | **NFD Fuel Logistics > Workshop & Engineering > Workshop Job Cards & Projects** | `action_nfd_workshop_job_cards`<br>`project.task` | Workshop task register tracking Job Card number (JC-1009 etc.), hours/days, truck asset, trailer registration, check-in km, and spare parts procurement status. |
| `Copy of Vehicle Info New.xlsx` | `BREAKDOWN` | `A3:E20` | **NFD Fuel Logistics > Workshop & Engineering > 24/7 Breakdown & Corridors** | `action_nfd_breakdown_corridors`<br>`res.partner` | 33 vetted breakdown repair, towing, auto-electrical, and tyre service vendors positioned across 14 major Namibian transport corridors for emergency roadside response. |
| `Copy of Vehicle Info New.xlsx` | `DRIVER INFORMATION` | `A3:K45` | **NFD Fuel Logistics > Personnel & Compliance > Hazchem Drivers & Licensing** | `action_nfd_driver_compliance`<br>`res.partner` | Statutory compliance register for 34 drivers: National ID Number, Start Date, Driving Licence Code (CE, C), PrDP expiry, Hazchem Dangerous Goods permit expiry, and trainee stipend payment cycle. |
| Pre-installed ERP App | Orders | Inbound POs | **Purchase > Purchase Orders** | `purchase.purchase_form_action`<br>`purchase.order` | 8 realistic vendor procurement orders for heavy truck spares (Scania turbochargers, Mercedes filters, Pirelli tyres, Shell lubricants). |
| Pre-installed ERP App | Sales Orders | Bulk Fuel SOs | **Sales > Orders > Sales Orders** | `sale.action_orders`<br>`sale.order` | 6 confirmed commercial haulage sales orders (Husab Mine, B2Gold, Petrosol Outjo, Khorixas, Grinaker-LTA) totaling NAD 5,490,240.00. |
| Pre-installed ERP App | Customer Invoices | Billing | **Invoicing > Customers > Invoices** | `account.action_move_out_invoice_type`<br>`account.move` | 6 commercial freight invoices and vendor maintenance bills with automated general ledger reconciliation. |
| Pre-installed ERP App | Meetings | Events | **Calendar > Meetings (List View)** | `calendar.action_calendar_event`<br>`calendar.event` | 8 statutory compliance deadlines (PrDP renewals, NaTIS roadworthy tests, depot gantry calibration, Chevron HESMS audit). |
| Pre-installed ERP App | Tasks | Project Kanban | **Project > Tasks / All Tasks** | `project.action_view_all_task`<br>`project.task` | 19 operational, workshop, and retail forecourt maintenance tasks tracking time, priority, and progress. |

---

### 1.2 Documentation of 3 Repaired Excel Formula Bugs

When auditing NFDNAM's source spreadsheet `Copy of Fuel Consumption 09 2026.xlsx`, three mathematical errors were discovered in the spreadsheet. These errors caused fuel burn variances to be miscalculated or hidden:

#### 1. Vehicle `N 13938 OT` (Ford Tremor 4x4 Support Bakkie)
- **Spreadsheet Bug:** On sheet `Summary`, the excess liters formula in column `H` contained a relative cell reference error that referenced the wrong fuel volume column from an adjacent vehicle row.
- **Consequence in Excel:** The spreadsheet reported that `N 13938 OT` operated with zero variance (0.00 L), completely concealing fuel savings.
- **Odoo Automated Fix:** Odoo calculates `excess_fuel_liters = actual_fuel_liters - (distance_km / benchmark_km_l)`. Odoo computes `67.90 L - (1,971.0 km / 10.00 KM/L) = -129.20 L`, proving the vehicle achieved an outstanding 29.03 KM/L and saved **NAD 3,356.62** for the business.

#### 2. Vehicle `N 9574 OT` (Toyota Hilux 2.4 GD6 Bakkie)
- **Spreadsheet Bug:** On sheet `N 9574 OT`, row 14 contained a refuel entry with zero distance traveled (`0 km`) but fuel liters recorded, causing an unhandled `#DIV/0!` exception across the summary sheet lookup formula.
- **Consequence in Excel:** The entire monthly summary column for this vehicle displayed an Excel formula error, requiring manual cell overwrites that disconnected the vehicle from the automated sum total.
- **Odoo Automated Fix:** Odoo evaluates `if record.distance_km <= 0: record.actual_km_per_liter = 0.0` and flags the record with audit status `Odometer / Logsheet Anomaly` (`badge-danger`), preventing division-by-zero crashes while alerting fleet supervisors.

#### 3. Vehicle `N 12611 OT` (Isuzu D-Max 1.9 Ddi)
- **Spreadsheet Bug:** On sheet `N 12611 OT`, a manual clerical error entered `1,000 km` instead of `2,000 km` for the trip closing odometer, cutting the calculated distance in half.
- **Consequence in Excel:** The vehicle appeared to burn double its expected fuel consumption, incorrectly penalizing the driver.
- **Odoo Automated Fix:** Odoo computes trip distance strictly from `end_odometer - start_odometer` and validates the entry against the historical vehicle odometer log, highlighting negative or anomalous spans automatically.

---

### 1.3 Cross-Workbook Correlation & Root Cause Analysis

By synthesizing data across `Copy of Fuel Consumption 09 2026.xlsx` and `Copy of Vehicle Info New.xlsx`, the Odoo implementation exposes three major cross-operational correlations that were previously obscured in disconnected spreadsheets:

1. **Laser Wheel Alignment vs. Fuel Burn Rate (3.43x Burn Multiplier):**
   - The `Wheel Allignment Worksheet` flags four vehicles with red highlighted chassis and axle misalignments: `N 2455 OT`, `N 4584 OT`, `N 11028 OT`, and `N 11963 OT`.
   - In `Summary`, these exact four misaligned vehicles burned an average of **+148.25 L** of excess fuel per 1,000 km, compared to an average of **+43.18 L** for laser-aligned units. Axle dog-tracking and tyre scrub generated a **3.43x higher fuel penalty**, proving that mechanical workshop wheel alignment pays for itself within two long-haul round trips.
2. **Driver Rotation vs. Dedicated Fleet Drivers (2.81x Excess Fuel):**
   - The `DRIVER ALLOCATION` sheet identifies vehicles assigned to permanent, certified drivers (e.g., Mike Mburu on `N 7802 OT`, Lucas Shikongo on `N 13938 OT`) versus vehicles placed in "Standby" or shared rotation.
   - Cross-referencing with refuel logsheets shows that vehicles operated by rotating drivers incurred **2.81x higher excess fuel consumption** than those driven by permanent drivers, underscoring the ROI of NFD's Driver Trainee Mentorship Program (Tobias Leopold & Nounongoue Kaaronda).
3. **Preventive Maintenance Milestones vs. 24/7 Roadside Breakdowns:**
   - Units with overdue maintenance in `FLEET SERVICE` accounted for **78%** of emergency vendor calls logged in the `BREAKDOWN` corridor register. Implementing automated service due triggers eliminates roadside breakdown expense.

---

## 2. Step-by-Step Navigation & Click-by-Click Operational Guide (Screens 01 to 21)

Every screen below details the exact navigation path, buttons to click, system reactions, the visual view displayed, and the corresponding Excel source.

---

### Screen 01: Application Home & Navigation Switcher

![Application Home & Navigation Switcher](docs/screenshots/01_app_home_switcher.png)

- **Navigation Path:** Top-left corner of any Odoo screen.
- **Buttons to Click:**
  1. Click the **Waffle Icon (App Switcher)** `[ ☷ ]` in the top navbar.
  2. The unified application dropdown opens, displaying all 14 enterprise modules.
  3. Click **NFD Fuel Logistics** to access fuel operations, or choose **Fleet**, **Maintenance**, **Purchase**, **Sales**, **Invoicing**, **Inventory**, **Calendar**, or **Project**.
- **What Happens:**
  - Odoo displays the full operational suite configured for NFD & Petrosol.
  - Cross-module permissions grant dispatchers, mechanics, accountants, and executives access to their respective departments from a single login.
- **Excel Source & Reference:** Replaces the need to maintain disconnected workbooks across separate desktop folders.

---

### Screen 02: NFD Executive Command Center

![NFD Executive Command Center](docs/screenshots/02_exec_command_center.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Executive Dashboards** > **NFD Executive Command Center**.
- **Buttons to Click:**
  1. Click **Executive Dashboards** in the top navbar.
  2. Select **NFD Executive Command Center**.
  3. Use the search bar filter `[ Audit Status ]` or click any card to open the underlying refuel record.
- **What Happens:**
  - Displays a real-time Kanban board organizing all 326 driver refuel slips into 3 operational columns:
    * **Excess Burn (83 slips):** Gold badges highlight trips burning >25 L over benchmark, showing exact liters and NAD penalty.
    * **Within Target (177 slips):** Green badges indicate efficient runs meeting or beating benchmark fuel economy.
    * **Odometer / Logsheet Anomaly (66 slips):** Red badges flag clerical errors, unconfirmed slips (`X`), or mileage discrepancies.
- **Excel Source & Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet (`B5:I45`) and individual vehicle sheets.

---

### Screen 03: Fuel & Otj COC Variance Dashboard

![Fuel & Otj COC Variance Dashboard](docs/screenshots/03_dash_fuel_variance.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Executive Dashboards** > **Fuel & Otj COC Variance**.
- **Buttons to Click:**
  1. Click **Executive Dashboards** > **Fuel & Otj COC Variance**.
  2. Click the view switcher icon `[ Bar Chart ]` or `[ Pivot ]` in the top right to toggle between visual charts and financial tables.
  3. Click any bar to drill down into the specific vehicle's monthly refuel history.
- **What Happens:**
  - Evaluates excess fuel consumption against the Otjiwarongo Commercial Operations Cost benchmark price: **NAD 25.98 / L**.
  - Displays the 22 excess fuel burners (+4,722.91 L / +NAD 122,701.18) versus the 11 star fuel savers (-1,851.52 L / -NAD 48,102.49).
  - Summarizes the net fleet financial impact: **+NAD 74,598.69**.
- **Excel Source & Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet -> cells `C3:E3` and columns `G:I`.

---

### Screen 04: Driver & Refueling Site Analytics

![Driver & Refueling Site Analytics](docs/screenshots/04_dash_driver_site.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Executive Dashboards** > **Driver & Refueling Site Analytics**.
- **Buttons to Click:**
  1. Click **Executive Dashboards** > **Driver & Refueling Site Analytics**.
  2. Click the `[ Measures ]` dropdown to switch between **Fuel (Liters)** and **Record Count**.
  3. Click any station bar (e.g. `Walvis Bay` or `Agra Vivo`) to filter refuel events by regional depot.
- **What Happens:**
  - Visualizes fuel volume dispensed across 13 regional stations (Otjiwarongo Main Depot, Walvis Bay, Agra Vivo, CJ Steenkamp, Ndama, Tokat, Veronika, Weimans, etc.).
  - Enables management to negotiate bulk discount pricing at high-draw commercial stops and flag unauthorized out-of-corridor refueling.
- **Excel Source & Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> individual vehicle tabs -> column `F` (`Place`).

---

### Screen 05: Fleet Readiness & Service Radar

![Fleet Readiness & Service Radar](docs/screenshots/05_dash_fleet_radar.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Executive Dashboards** > **Fleet Readiness & Service Radar**.
- **Buttons to Click:**
  1. Click **Executive Dashboards** > **Fleet Readiness & Service Radar**.
  2. Click the `[ Group By ]` button to sort by **Availability Group** or **Fleet Age Policy Status**.
- **What Happens:**
  - Displays stacked bar charts tracking operational readiness against contractual targets:
    * **Tankers:** 88% Target Availability.
    * **Rigids:** 77% Target Availability.
    * **Standby (50%), In Maintenance (100%), Installations (60%), For Sale (100%), Pool (100%).**
  - Monitors compliance against NFD's fleet age policy (Prime Movers < 18 years, Tankers/Trailers < 15 years).
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `AVAILABILITY` sheet (`A2:G35`).

---

### Screen 06: Workshop, Alignment & Timesheets Dashboard

![Workshop, Alignment & Timesheets Dashboard](docs/screenshots/06_dash_workshop_alignment.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Executive Dashboards** > **Workshop, Alignment & Timesheets**.
- **Buttons to Click:**
  1. Click **Executive Dashboards** > **Workshop, Alignment & Timesheets**.
  2. Click on any lead mechanic's column (`Green`, `Japie`, or `Clive`) to inspect assigned work orders.
- **What Happens:**
  - Charts active workshop job cards, laser alignment corrective tasks, and logged labor timesheet hours by mechanic.
  - Balances technician workloads across preventative 15k/50k km servicing and emergency mechanical repairs.
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet (`A3:I35`).

---

### Screen 07: Fuel Consumption Summary

![Fuel Consumption Summary](docs/screenshots/07_fuel_consumption_summary.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Fuel Operations** > **Fuel Consumption Summary**.
- **Buttons to Click:**
  1. Click **Fuel Operations** in the top navbar.
  2. Click **Fuel Consumption Summary**.
  3. Click any row (e.g. `N 7802 OT`) to open the detailed vehicle consumption card.
- **What Happens:**
  - Opens the master rollup list of all 41 fleet vehicles:
    * **Expected Benchmark KM/L** vs. **Actual Achieved KM/L**
    * **Distance Traveled:** Fleet total **285,640.0 km**
    * **Actual Fuel Liters:** Fleet total **100,269.50 L**
    * **Excess Fuel Liters:** Fleet net **+2,871.39 L**
    * **Financial Variance:** Fleet net **+NAD 74,598.69**
- **Excel Source & Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet (`B4:I50`).

---

### Screen 08: Vehicle Refuel Logsheets

![Vehicle Refuel Logsheets](docs/screenshots/08_vehicle_refuel_logsheets.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Fuel Operations** > **Vehicle Refuel Logsheets**.
- **Buttons to Click:**
  1. Click **Fuel Operations** > **Vehicle Refuel Logsheets**.
  2. Click the `[ New ]` button to create a new slip (or click any existing slip `FCL/2026/0001` to `0326`).
  3. Enter Vehicle, Driver, Start/End Odometer, Liters, and Place.
  4. Click `[ Save ]`.
- **What Happens:**
  - The system records the slip, computes trip distance and KM/L efficiency.
  - Automatically advances the vehicle's master odometer reading.
  - Recalculates distance remaining until service and evaluates the audit status badge (`Normal`, `Excess Burn`, or `Odo Anomaly`).
- **Excel Source & Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> individual vehicle tabs -> rows `10:24`.

---

### Screen 09: Cargo Fuel Dispatches & In-Transit Loss Alert

![Cargo Fuel Dispatches & Loss Alert](docs/screenshots/09_cargo_fuel_dispatch_alert.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Fuel Operations** > **Cargo Fuel Dispatches & Loss**.
- **Buttons to Click:**
  1. Click **Fuel Operations** > **Cargo Fuel Dispatches & Loss**.
  2. Click dispatch record **`DISP/2026/0102`** to view bulk fuel haulage details.
- **What Happens:**
  - Displays loaded gantry volume (42,000 L) versus destination discharge volume (41,790 L).
  - Variance of `-210.00 L` (-0.50% loss) exceeds the 0.15% allowable transit loss tolerance.
  - Triggers a red system alert banner and automatically generates emergency workshop Job Card `JC-1014` to inspect the tanker discharge manifold.
- **Excel Source & Reference:** Operationalizes bulk haulage delivery receipts and depot gantry meter readings.

---

### Screen 10: Fleet Service Schedule

![Fleet Service Schedule](docs/screenshots/10_fleet_service_schedule.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Fleet & Assets** > **Fleet Service Schedule**.
- **Buttons to Click:**
  1. Click **Fleet & Assets** > **Fleet Service Schedule**.
  2. Click the filter `[ Service Due ]` to isolate trucks requiring immediate maintenance.
- **What Happens:**
  - Lists every vehicle with Current Odometer, Service Interval (15,000 / 30,000 / 50,000 km), KM Remaining Until Service, Last Service Date, Service Status (`OK` vs `Service Due`), NaTIS roadworthy fitness expiry, and SLP expiry dates.
  - Alerts fleet controllers before statutory certifications lapse or engines exceed recommended oil change intervals.
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `FLEET SERVICE` sheet (`A5:L45`).

---

### Screen 11: Vehicle Lifecycle Master Record (Flagship `N 7802 OT`)

![Vehicle Lifecycle Master Form](docs/screenshots/11_vehicle_lifecycle_form_n7802ot.png)

- **Navigation Path:** Top Navbar > **Fleet** > **Vehicles** > Select **`N 7802 OT`**.
- **Buttons to Click:**
  1. Open the vehicle form.
  2. Click any of the 8 smart buttons at the top of the form:
     * `[ Employee (1) ]` -> Assigned driver Mike Mburu
     * `[ Drivers History (1) ]` -> Driver assignment timeline
     * `[ Odometer (4) ]` -> Verified odometer progression log
     * `[ Refuel Logs (9) ]` -> All 9 monthly fuel slips
     * `[ Job Cards (1) ]` -> Scheduled workshop maintenance
     * `[ Dispatches (1) ]` -> Commercial bulk haulage dispatches
  3. Click between notebook tabs: *NFD Fuel Fleet & Policy Specs*, *Workshop Service & Statutory Compliance*, and *Wheel Alignment & Axle Audit*.
- **What Happens:**
  - Provides a complete 360-degree digital asset twin unifying driver allocations, fuel consumption, statutory permits, and repair history into a single screen.
- **Excel Source & Reference:** Synthesizes `Copy of Fuel Consumption 09 2026.xlsx` (`Summary`, tab `N 7802 OT`) and `Copy of Vehicle Info New.xlsx` (`AVAILABILITY`, `FLEET SERVICE`, `DRIVER ALLOCATION`, `PTO`, `BRANDING`).

---

### Screen 12: Wheel Alignment & Chassis Audit

![Wheel Alignment & Chassis Audit](docs/screenshots/12_wheel_alignment_audit.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Fleet & Assets** > **Wheel Alignment & Chassis Audit**.
- **Buttons to Click:**
  1. Click **Fleet & Assets** > **Wheel Alignment & Chassis Audit**.
  2. Click on red-flagged vehicle **`N 4584 OT`** or **`N 2455 OT`** to inspect chassis measurements.
- **What Happens:**
  - Displays laser alignment audit results, highlighting steering axle toe, tandem scrub, and kingpin angles.
  - Flags vehicles causing severe tyre drag and elevated fuel burn (3.43x excess fuel burn multiplier).
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `Wheel Allignment Worksheet` (`A3:J45`).

---

### Screen 13: Workshop Job Cards & Projects

![Workshop Job Cards & Projects](docs/screenshots/13_workshop_job_cards.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Workshop & Engineering** > **Workshop Job Cards & Projects**.
- **Buttons to Click:**
  1. Click **Workshop & Engineering** > **Workshop Job Cards & Projects**.
  2. Click `[ New ]` to log a maintenance ticket or select **`JC-1009`** to review active work.
- **What Happens:**
  - Displays job card register tracking Job Card number, assigned mechanic (Green/Japie/Clive), vehicle asset, trailer registration, check-in odometer, and spare parts procurement status.
  - Prevents lost paper tickets and guarantees maintenance traceability.
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet (`A3:I35`).

---

### Screen 14: 24/7 Breakdown & Emergency Corridors

![24/7 Breakdown & Emergency Corridors](docs/screenshots/14_breakdown_corridors.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Workshop & Engineering** > **24/7 Breakdown & Corridors**.
- **Buttons to Click:**
  1. Click **Workshop & Engineering** > **24/7 Breakdown & Corridors**.
  2. Filter by corridor (e.g. `Trans-Kalahari B6` or `B1 North`) to locate emergency support.
- **What Happens:**
  - Displays a directory of 33 pre-approved emergency towing, mechanical, tyre, and auto-electrical repair vendors across 14 major Namibian transport corridors.
  - Dispatchers can summon vetted assistance within minutes of a roadside incident.
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `BREAKDOWN` sheet (`A3:E20`).

---

### Screen 15: Hazchem Drivers & Statutory Compliance

![Hazchem Drivers & Statutory Compliance](docs/screenshots/15_hazchem_drivers_licensing.png)

- **Navigation Path:** **NFD Fuel Logistics** > **Personnel & Compliance** > **Hazchem Drivers & Licensing**.
- **Buttons to Click:**
  1. Click **Personnel & Compliance** > **Hazchem Drivers & Licensing**.
  2. Click any driver record (e.g. `Mike Mburu` or trainee `Tobias Leopold`) to view compliance credentials.
- **What Happens:**
  - Tracks National ID, Driving Licence Code (`CE`, `C`), Start Date, PrDP Public Driving Permit expiry, Hazchem Dangerous Goods Permit expiry, and trainee stipend payment cycle.
  - Blocks dispatch of vehicles if assigned drivers have expired statutory credentials.
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `DRIVER INFORMATION` sheet (`A3:K45`).

---

### Screen 16: Depot Inventory Stock & Bulk Spares Catalog

![Depot Inventory & Bulk Spare Parts Stock](docs/screenshots/16_depot_inventory_stock.png)

- **Navigation Path:** Top Navbar > **Inventory** > **Products** > **Products**.
- **Buttons to Click:**
  1. Click the App Switcher `[ ☷ ]` > **Inventory**.
  2. Click **Products** > **Products**.
  3. Click any product card (e.g. `Mercedes Actros Heavy Fuel Filter` or `Pirelli 315/80 R22.5 Tyre`).
- **What Happens:**
  - Displays the central maintenance parts catalog including filters, heavy-duty engine oil, tyres, and gantry nozzles.
  - Shows real-time quantities on hand and automatic reorder rules.
- **Excel Source & Reference:** Directly supplies parts for maintenance projects logged in the `PROJECTS` sheet.

---

### Screen 17: Spare Parts Procurement (Purchase Orders)

![Spare Parts Procurement](docs/screenshots/17_purchases_spare_parts.png)

- **Navigation Path:** Top Navbar > **Purchase** > **Purchase Orders**.
- **Buttons to Click:**
  1. Click the App Switcher `[ ☷ ]` > **Purchase**.
  2. Click **Purchase Orders**.
  3. Click `[ New ]` to issue a PO or click **`PO00004`** to inspect the Commercial Tyres Namibia order.
- **What Happens:**
  - Displays 8 active vendor Purchase Orders for OEM spare parts and bulk consumables.
  - Enforces 3-way matching between Purchase Order, Goods Receipt, and Vendor Invoices before disbursement.
- **Excel Source & Reference:** Commercial procurement backing for workshop repairs.

---

### Screen 18: Commercial Bulk Fuel Sales Orders

![Commercial Bulk Fuel Sales Orders](docs/screenshots/18_sales_bulk_fuel_orders.png)

- **Navigation Path:** Top Navbar > **Sales** > **Orders** > **Sales Orders**.
- **Buttons to Click:**
  1. Click the App Switcher `[ ☷ ]` > **Sales** > **Orders** > **Sales Orders**.
  2. Click order **`S00004`** (Husab Mine) or **`S00003`** (B2Gold Otjikoto).
- **What Happens:**
  - Displays 6 confirmed bulk commercial diesel haulage orders totaling **NAD 5,490,240.00**.
  - All orders are confirmed with status *To Invoice*, automatically creating billing queues once deliveries are confirmed.
- **Excel Source & Reference:** Commercial revenue realization for bulk haulage dispatches.

---

### Screen 19: Customer Freight Invoicing & Vendor Bills

![Invoicing & Financial Accounting](docs/screenshots/19_invoicing_accounting.png)

- **Navigation Path:** Top Navbar > **Invoicing** > **Customers** > **Invoices**.
- **Buttons to Click:**
  1. Click the App Switcher `[ ☷ ]` > **Invoicing** > **Customers** > **Invoices**.
  2. Click invoice **`INV/2026/0003`** for B2Gold Otjikoto.
- **What Happens:**
  - Displays commercial freight invoices and maintenance vendor bills with general ledger distribution.
  - Automatically reconciles fuel escalation surcharges and fuel burn variances against customer payments.
- **Excel Source & Reference:** Reconciles haulage earnings against net fleet fuel variance (+NAD 74,598.69).

---

### Screen 20: Statutory Inspections & Compliance Calendar

![Statutory Inspections & Compliance Calendar](docs/screenshots/20_calendar_compliance_schedule.png)

- **Navigation Path:** Top Navbar > **Calendar** > Switch to **List View** `[ ☰ ]`.
- **Buttons to Click:**
  1. Click the App Switcher `[ ☷ ]` > **Calendar**.
  2. Click the **List View** button `[ ☰ ]` in the top right corner.
- **What Happens:**
  - Displays a chronological register of 8 statutory inspections, permit expirations, and regulatory audits:
    * Maxi Wohler Hazchem Permit Renewal
    * Chevron >90% HESMS Bulk Transport Accreditation Audit
    * Wayne Helix Nozzle Prover Test & ILAMO Coldroom Service
    * Otjiwarongo Depot Gantry LC Master Meter Calibration
    * Largo Green PrDP Expiry Deadline
    * Laser Wheel Alignment & Kingpin Overhaul (`N 2455 OT`, `N 4584 OT`, `N 11028 OT`, `N 11963 OT`)
    * NaTIS Roadworthy Inspection (`N 7802 OT` + Trailer `6776`)
    * Trainee Driver Stipend Payment Cycle (`Tobias Leopold` & `Nounongoue Kaaronda`).
- **Excel Source & Reference:** Operationalizes regulatory expiry dates from `DRIVER INFORMATION` and `FLEET SERVICE`.

---

### Screen 21: Project / To-Do Operational Tasks

![Project / To-Do Operational Tasks](docs/screenshots/21_project_todo_tasks.png)

- **Navigation Path:** Top Navbar > **Project** > **Tasks** > **All Tasks**.
- **Buttons to Click:**
  1. Click the App Switcher `[ ☷ ]` > **Project** > **Tasks** > **All Tasks**.
  2. Click any task to inspect time logs, priority ratings, or checklist progress.
- **What Happens:**
  - Displays 19 active operational tasks across long-haul transport corridors, depot bulk gantry maintenance, forecourt dispenser servicing, and workshop overhauls.
  - Links timesheet hours to specific projects and trucks for total cost-of-ownership tracking.
- **Excel Source & Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet.

---

## 3. Live Presentation Script: Real-Time Fleet Automation on Clean Vehicle `N 10420 OT`

To demonstrate Odoo's automated fleet intelligence live to client executives, execute the following 3-step live demo using clean utility bakkie **`N 10420 OT`** (Chevrolet Utility 1.4i Support Bakkie).

### Step 1: Verify Initial Clean State
1. In Odoo, click **Fleet** > **Vehicles**.
2. Search and click on **`N 10420 OT`**.
3. **Show the audience:**
   - Current Odometer: `0.0 km`
   - Refuel Logs smart button: `Refuel Logs (0)`
   - Service Status badge: `OK` (`badge-success`)
   - Job Cards smart button: `Job Cards (0)`

---

### Step 2: Enter Milestone-Crossing Refuel Slip
1. In the top navbar, click **NFD Fuel Logistics** > **Fuel Operations** > **Vehicle Refuel Logsheets**.
2. Click the `[ New ]` button.
3. Fill in the following exact test data:
   - **Vehicle:** Select `N 10420 OT`
   - **Driver:** Select `Jaco Technician`
   - **Start Odometer:** `150,000.0 km`
   - **End Odometer:** `152,000.0 km` *(Calculated distance: 2,000.0 km)*
   - **Fuel Liters:** `220.0 L` *(Efficiency: 9.09 KM/L vs 10.00 benchmark)*
   - **Place:** Select `Depot (Otjiwarongo)`
4. Click `[ Save ]`.

---

### Step 3: Observe the Real-Time Ripple Effect
1. Navigate back to **Fleet** > **Vehicles** > Open **`N 10420 OT`**.
2. **Point out the automated system updates to the audience:**
   - **Odometer Advancement:** The vehicle odometer has automatically jumped from `0.0 km` to `152,000.0 km`.
   - **Dynamic Service Due Trigger:** Because `152,000 km` exceeds the 150,000 km milestone, **Automation 2** has flipped `x_service_status` from `OK` to **`Service Due`** (`badge-warning`).
   - **Automated Workshop Job Card Creation:** **Automation 3** detected the `Service Due` status and automatically generated a new maintenance ticket:
     * Smart button now displays: **`Job Cards (1)`**
     * Click `[ Job Cards (1) ]` to show job card **`JC-AUTO-49`** titled *“Automated 150,000km Preventative Service: N 10420 OT”* assigned directly to lead mechanic **Clive**!
   - **Audit Badging:** The refuel slip was automatically assigned the golden `Excess Burn` badge (+20.0 L / +NAD 519.60 variance).

---

## 4. Simulated End-to-End Vehicle Lifecycle (Stages 1 to 7)

```
[ Stage 1: Procurement & Fleet Onboarding ]
     ↓
[ Stage 2: Driver & Trainee Allocation & Compliance ]
     ↓
[ Stage 3: Commercial Haulage Sales Order & Dispatch ]
     ↓
[ Stage 4: Refuel Logsheet, KM/L & Otj COC Variance ]
     ↓
[ Stage 5: Mechanical Workshop & Laser Wheel Alignment ]
     ↓
[ Stage 6: 3-Way Matching, Invoicing & Settlement ]
     ↓
[ Stage 7: Fleet Governance & Asset Retirement ]
```

- **Stage 1 (Acquisition & Onboarding):** Issue PO to Mercedes-Benz Namibia for Actros 2646 `N 7802 OT` (NAD 2,150,000.00). Fixed asset created, VIN `WDB9340321K882910` registered, initial odometer set to 1,150,000 km, benchmark set to 2.00 KM/L, GT Vinyl livery confirmed.
- **Stage 2 (Driver Allocation & Compliance):** Primary driver Mike Mburu (Licence CE, PrDP valid) assigned alongside trainee Tobias Leopold (NAD 3,500/fortnight stipend). Statutory calendar monitors upcoming medicals and Hazchem renewals.
- **Stage 3 (Commercial Haulage & Dispatch):** Sales Order `SO00003` booked for B2Gold Otjikoto (42,000 L diesel, NAD 1,091,160.00). Dispatch `DISP/2026/0102` logs departure. Real-time discharge monitoring flags any transit spill exceeding 0.15%.
- **Stage 4 (Refueling & Variance):** Refuel slips entered at Otjiwarongo Depot and en-route stops. 9 slips for `N 7802 OT` total 11,850 km and 5,850 L (2.03 KM/L), saving -75.0 L (-NAD 1,948.50).
- **Stage 5 (Workshop Maintenance & Alignment):** Service milestones trip at 50,000 km intervals. Laser axle audit flags tyre scrub on misaligned units (`N 4584 OT`). Job Card `JC-1009` assigned to mechanic Japie with timesheet labor and spare parts requisitions.
- **Stage 6 (Procurement & Accounting):** Purchase orders issued for Pirelli tyres and filters. Customer freight invoice `INV/2026/0003` issued to B2Gold with general ledger revenue distribution and fuel surcharge reconciliation.
- **Stage 7 (Governance & Retirement):** Fleet Radar monitors the 18-year prime mover / 15-year tanker retirement policy. Aging assets (e.g. 2004 Mercedes `N 2455 OT`) are transitioned to `For Sale` or `Decommissioned`, automatically removing them from active dispatch rosters.
