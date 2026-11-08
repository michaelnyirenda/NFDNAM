# NFDNAM Standard Operating Procedure (SOP)

**End-to-End Operational Lifecycle:** Sales Order &rarr; Dispatch &rarr; Refueling &rarr; Workshop &rarr; Invoicing

---

## Operational Workflow Overview

This standard operating procedure follows the chronological, real-life operational flow that NFDNAM follows to execute commercial bulk fuel haulage contracts, monitor vehicle telematics, manage fleet maintenance, and close customer billing:

* **Phase A: Order & Dispatch Preparation (Steps 1–6):** Commercial contract intake, driver statutory compliance audit, inspection schedule review, vehicle digital asset verification, and fleet readiness check.
* **Phase B: Depot Loading & In-Transit Dispatch (Steps 7–9):** Gantry bulk fuel metering, delivery dispatch creation, long-haul task tracking, and 24/7 emergency roadside vendor routing.
* **Phase C: Refueling, Telematics & Fuel Accounting (Steps 10–14):** Driver refuel slip submission, real-time executive Kanban triage, fleet-wide fuel rollup, financial variance pricing at Otjiwarongo COC benchmark (NAD 25.98 / L), and regional site analytics.
* **Phase D: Workshop Servicing & Fleet Maintenance (Steps 15–20):** Post-trip milestone tracking, laser wheel alignment drag diagnostics, workshop job card issuance, mechanic labor timesheets, depot spare parts requisition, and OEM replenishment purchase orders.
* **Phase E: Commercial Billing & Financial Close (Step 21):** Customer freight invoicing, fuel escalation reconciliation, and general ledger close.

---

## Sequential Step-by-Step Navigation & Operational Guide

---

### Step 1: System Access & Application Navigation
**Phase:** `PHASE A: ORDER & DISPATCH PREPARATION`  
**Excel Reference:** *Replaces disconnected desktop spreadsheets with a central ERP portal*

- **Navigation:** Top-left corner of any screen &gt; Click Waffle Icon `[ ☷ ]`
- **Buttons to Click:**
  1. Click the `[ ☷ Waffle Icon ]` in the top navbar.
  2. Select `[ Sales ]` to begin customer order intake, or `[ NFD Fuel Logistics ]` for fleet operations.
- **What Happens:**
  - The enterprise app launcher opens, displaying all 14 active departments.
  - Consolidates commercial haulage, fleet maintenance, fuel logistics, and accounting under a single unified sign-on with role-based access permissions.

![Step 1: System Access & Application Navigation](docs/screenshots/01_app_home_switcher.png)

---

### Step 2: Commercial Bulk Fuel Sales Order Booking
**Phase:** `PHASE A: ORDER & DISPATCH PREPARATION`  
**Excel Reference:** *Pre-installed Sales App > Commercial Haulage Pipeline (NAD 5.49M)*

- **Navigation:** `Sales > Orders > Sales Orders`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Sales ]` &gt; Click `[ Orders ]` &gt; `[ Sales Orders ]`.
  2. Select order `[ S00003 ]` (B2Gold Otjikoto) or click `[ New ]` to book a delivery.
- **What Happens:**
  - Confirms bulk fuel haulage contracts (e.g. `S00003`: 42,000 L Ultra-Low Sulphur Diesel to B2Gold Otjikoto Mine, NAD 1,091,160.00).
  - Confirmed order enters the transport dispatch queue with status *To Invoice*.

![Step 2: Commercial Bulk Fuel Sales Order Booking](docs/screenshots/18_sales_bulk_fuel_orders.png)

---

### Step 3: Driver Allocation & Statutory Compliance Audit
**Phase:** `PHASE A: ORDER & DISPATCH PREPARATION`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `DRIVER INFORMATION` *(A3:K45)*

- **Navigation:** `NFD Fuel Logistics > Personnel & Compliance > Hazchem Drivers & Licensing`
- **Buttons to Click:**
  1. Click `[ Personnel & Compliance ]` &gt; Click `[ Hazchem Drivers & Licensing ]`.
  2. Select driver `[ Mike Mburu ]` or trainee `[ Tobias Leopold ]`.
- **What Happens:**
  - Verifies the assigned driver possesses an unexpired Heavy Articulated Licence (Code CE), valid Public Driving Permit (PrDP), and active Hazchem Dangerous Goods Permit.
  - Blocks dispatch if certifications have lapsed.

![Step 3: Driver Allocation & Statutory Compliance Audit](docs/screenshots/15_hazchem_drivers_licensing.png)

---

### Step 4: Statutory Compliance Calendar & Inspection Schedule
**Phase:** `PHASE A: ORDER & DISPATCH PREPARATION`  
**Excel Reference:** *Pre-installed Calendar App > Statutory Fleet Deadlines*

- **Navigation:** `Calendar > Switch to List View [ ☰ ]`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Calendar ]`.
  2. Click the `[ ☰ List View ]` button in the top-right corner.
- **What Happens:**
  - Audits upcoming statutory inspection deadlines across the fleet: NaTIS vehicle roadworthy renewals, gantry LC master meter calibrations, and Hazchem audit dates.
  - Ensures scheduled trips do not conflict with required vehicle inspections.

![Step 4: Statutory Compliance Calendar & Inspection Schedule](docs/screenshots/20_calendar_compliance_schedule.png)

---

### Step 5: Vehicle Master Inspection & Trailer Coupling (Flagship N 7802 OT)
**Phase:** `PHASE A: ORDER & DISPATCH PREPARATION`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `FLEET SERVICE` & `DRIVER ALLOCATION`

- **Navigation:** `Fleet > Vehicles > Select N 7802 OT`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Fleet ]` &gt; `[ Vehicles ]` &gt; Open `[ N 7802 OT ]`.
  2. Click smart buttons: `[ Employee (1) ]`, `[ Refuel Logs (9) ]`, `[ Dispatches (1) ]`.
  3. Switch between notebook tabs: *NFD Fuel Fleet & Policy Specs*, *Workshop Service & Statutory Compliance*, and *Wheel Alignment & Axle Audit*.
- **What Happens:**
  - Inspects the 360-degree digital asset twin of long-haul prime mover `N 7802 OT`: coupled B-double bulk tanker trailer `6776`, benchmark fuel consumption (2.00 KM/L), current odometer, and GT Vinyl livery branding status.

![Step 5: Vehicle Master Inspection & Trailer Coupling](docs/screenshots/11_vehicle_lifecycle_form_n7802ot.png)

---

### Step 6: Fleet Readiness & Operational Availability Radar
**Phase:** `PHASE A: ORDER & DISPATCH PREPARATION`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `AVAILABILITY` *(A2:G35)*

- **Navigation:** `NFD Fuel Logistics > Executive Dashboards > Fleet Readiness & Service Radar`
- **Buttons to Click:**
  1. Click `[ Executive Dashboards ]` &gt; Click `[ Fleet Readiness & Service Radar ]`.
  2. Use `[ Group By ]` to filter by Availability Group.
- **What Happens:**
  - Verifies overall fleet readiness against operational targets: Tankers (88% target availability), Rigids (77% target availability).
  - Ensures sufficient operational buffer before committing haulage units to commercial routes.

![Step 6: Fleet Readiness & Operational Availability Radar](docs/screenshots/05_dash_fleet_radar.png)

---

### Step 7: Gantry Bulk Fuel Loading & Cargo Dispatch
**Phase:** `PHASE B: DEPOT LOADING & IN-TRANSIT DISPATCH`  
**Excel Reference:** *Operationalizes Bulk Haulage Dispatches & Gantry Loss Audit*

- **Navigation:** `NFD Fuel Logistics > Fuel Operations > Cargo Fuel Dispatches & Loss`
- **Buttons to Click:**
  1. Click `[ Fuel Operations ]` &gt; Click `[ Cargo Fuel Dispatches & Loss ]`.
  2. Select dispatch `[ DISP/2026/0102 ]`.
- **What Happens:**
  - Records outbound bulk fuel departure: 42,000 L loaded at Otjiwarongo depot gantry into tanker `6776`.
  - Monitors destination discharge volume (41,790 L). A variance of -210 L (-0.50%) triggers an automated leak alert and emergency maintenance ticket.

![Step 7: Gantry Bulk Fuel Loading & Cargo Dispatch](docs/screenshots/09_cargo_fuel_dispatch_alert.png)

---

### Step 8: In-Transit Task Tracking & Corridor Operations
**Phase:** `PHASE B: DEPOT LOADING & IN-TRANSIT DISPATCH`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `PROJECTS` *(A3:I35)*

- **Navigation:** `Project > Tasks > All Tasks`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Project ]` &gt; Click `[ Tasks ]` &gt; `[ All Tasks ]`.
  2. Click any active haulage task.
- **What Happens:**
  - Coordinates long-haul corridor operations (e.g. Walvis Bay to Otjiwarongo Tank Farm Inbound Haulage, B2Gold Daily Haulage).
  - Drivers and controllers track stage completion and log route timesheet hours.

![Step 8: In-Transit Task Tracking & Corridor Operations](docs/screenshots/21_project_todo_tasks.png)

---

### Step 9: Roadside Emergency & 24/7 Breakdown Routing
**Phase:** `PHASE B: DEPOT LOADING & IN-TRANSIT DISPATCH`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `BREAKDOWN` *(A3:E20)*

- **Navigation:** `NFD Fuel Logistics > Workshop & Engineering > 24/7 Breakdown & Corridors`
- **Buttons to Click:**
  1. Click `[ Workshop & Engineering ]` &gt; Click `[ 24/7 Breakdown & Corridors ]`.
  2. Filter by corridor (e.g. B1 North, Trans-Kalahari B6).
- **What Happens:**
  - If an en-route mechanical issue or puncture occurs, dispatchers immediately locate the nearest pre-vetted roadside service, towing, tyre, or auto-electrical vendor across 14 major Namibian transport corridors.

![Step 9: Roadside Emergency & 24/7 Breakdown Routing](docs/screenshots/14_breakdown_corridors.png)

---

### Step 10: Driver Refuel Slip Submission (Depot & En-Route)
**Phase:** `PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING`  
**Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` &gt; *Vehicle Tabs (Rows 10:24)*

- **Navigation:** `NFD Fuel Logistics > Fuel Operations > Vehicle Refuel Logsheets`
- **Buttons to Click:**
  1. Click `[ Fuel Operations ]` &gt; Click `[ Vehicle Refuel Logsheets ]`.
  2. Click `[ New ]` to enter a slip, then click `[ Save ]`.
- **What Happens:**
  - Logs refuel slip: Vehicle, Driver, Start/End Odometer, Fuel Liters, and Place.
  - System instantly calculates distance and KM/L efficiency, advances the vehicle master odometer reading, and evaluates audit compliance.

![Step 10: Driver Refuel Slip Submission](docs/screenshots/08_vehicle_refuel_logsheets.png)

---

### Step 11: Real-Time Fuel Audit & Executive Kanban Triage
**Phase:** `PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING`  
**Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` &gt; *Summary Sheet & Tabs*

- **Navigation:** `NFD Fuel Logistics > Executive Dashboards > NFD Executive Command Center`
- **Buttons to Click:**
  1. Click `[ Executive Dashboards ]` &gt; Click `[ NFD Executive Command Center ]`.
  2. Click any card to inspect trip audit details.
- **What Happens:**
  - Triages all 326 refuel slips into 3 operational Kanban lanes: **Excess Burn (83 trips)**, **Within Target (177 trips)**, and **Odometer / Logsheet Anomaly (66 trips)**.

![Step 11: Real-Time Fuel Audit & Executive Kanban Triage](docs/screenshots/02_exec_command_center.png)

---

### Step 12: Fleet-Wide Fuel Consumption Summary & Excel Rollup
**Phase:** `PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING`  
**Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` &gt; `Summary` *(B4:I50)*

- **Navigation:** `NFD Fuel Logistics > Fuel Operations > Fuel Consumption Summary`
- **Buttons to Click:**
  1. Click `[ Fuel Operations ]` &gt; Click `[ Fuel Consumption Summary ]`.
  2. Click any vehicle row to open the complete monthly breakdown.
- **What Happens:**
  - Rolls up the monthly performance of all 41 vehicles: 285,640.0 km traveled, 100,269.50 L actual fuel, and net +2,871.39 L excess fuel (+NAD 74,598.69 net financial variance).
  - Exactly reconciles the master Excel summary.

![Step 12: Fleet-Wide Fuel Consumption Summary](docs/screenshots/07_fuel_consumption_summary.png)

---

### Step 13: Financial Fuel Variance & Commercial Pricing Analysis
**Phase:** `PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING`  
**Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` &gt; `Summary` *(C3:E3, G4:I45)*

- **Navigation:** `NFD Fuel Logistics > Executive Dashboards > Fuel & Otj COC Variance`
- **Buttons to Click:**
  1. Click `[ Executive Dashboards ]` &gt; Click `[ Fuel & Otj COC Variance ]`.
  2. Toggle between `[ Bar Chart ]` and `[ Pivot ]` view in the top-right.
- **What Happens:**
  - Quantifies fuel variance in monetary terms using the Otjiwarongo Commercial Operations Cost benchmark price: **NAD 25.98 / L**.
  - Isolates top excess burners (+NAD 122,701.18) against star savers (-NAD 48,102.49).

![Step 13: Financial Fuel Variance & Commercial Pricing Analysis](docs/screenshots/03_dash_fuel_variance.png)

---

### Step 14: Regional Station & Fuel Draw Analytics
**Phase:** `PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING`  
**Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` &gt; *Vehicle Tabs (Column F: Place)*

- **Navigation:** `NFD Fuel Logistics > Executive Dashboards > Driver & Refueling Site Analytics`
- **Buttons to Click:**
  1. Click `[ Executive Dashboards ]` &gt; Click `[ Driver & Refueling Site Analytics ]`.
  2. Click `[ Measures ]` to toggle between Liters and Count.
- **What Happens:**
  - Analyzes regional fuel draw across 13 stops (Otjiwarongo Depot, Walvis Bay, Agra Vivo, CJ Steenkamp, Ndama, Tokat, Veronika, Weimans).
  - Identifies high-draw locations for bulk corporate rebate negotiations.

![Step 14: Regional Station & Fuel Draw Analytics](docs/screenshots/04_dash_driver_site.png)

---

### Step 15: Post-Trip Milestone Tracking & Service Due Triggers
**Phase:** `PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `FLEET SERVICE` *(A5:L45)*

- **Navigation:** `NFD Fuel Logistics > Fleet & Assets > Fleet Service Schedule`
- **Buttons to Click:**
  1. Click `[ Fleet & Assets ]` &gt; Click `[ Fleet Service Schedule ]`.
  2. Click filter `[ Service Due ]` to view overdue vehicles.
- **What Happens:**
  - As refuel logsheets advance vehicle odometers, the system compares readings against 15,000 / 30,000 / 50,000 km intervals.
  - When km remaining reaches 0, the vehicle automatically flips to **Service Due**.

![Step 15: Post-Trip Milestone Tracking & Service Due Triggers](docs/screenshots/10_fleet_service_schedule.png)

---

### Step 16: Laser Wheel Alignment & Chassis Drag Diagnostics
**Phase:** `PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `Wheel Allignment Worksheet`

- **Navigation:** `NFD Fuel Logistics > Fleet & Assets > Wheel Alignment & Chassis Audit`
- **Buttons to Click:**
  1. Click `[ Fleet & Assets ]` &gt; Click `[ Wheel Alignment & Chassis Audit ]`.
  2. Select red-flagged vehicle `[ N 4584 OT ]`.
- **What Happens:**
  - Audits steering and tandem axle alignment.
  - Flags misaligned vehicles (`N 2455`, `N 4584`, `N 11028`, `N 11963`) suffering severe tyre scrub, which drives a 3.43x higher excess fuel burn rate.

![Step 16: Laser Wheel Alignment & Chassis Drag Diagnostics](docs/screenshots/12_wheel_alignment_audit.png)

---

### Step 17: Workshop Job Card Issuance & Mechanic Assignment
**Phase:** `PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `PROJECTS` *(A3:I35)*

- **Navigation:** `NFD Fuel Logistics > Workshop & Engineering > Workshop Job Cards & Projects`
- **Buttons to Click:**
  1. Click `[ Workshop & Engineering ]` &gt; Click `[ Workshop Job Cards & Projects ]`.
  2. Select job card `[ JC-1009 ]` or click `[ New ]`.
- **What Happens:**
  - Creates maintenance work order linking vehicle asset, coupled trailer, check-in odometer, and assigned lead mechanic (Green/Japie/Clive) for chassis repairs, laser alignment, or milestone servicing.

![Step 17: Workshop Job Card Issuance & Mechanic Assignment](docs/screenshots/13_workshop_job_cards.png)

---

### Step 18: Workshop Labor Timesheets & Job Card Progress
**Phase:** `PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE`  
**Excel Reference:** `Copy of Vehicle Info New.xlsx` &gt; `PROJECTS` *(Mechanic Allocation)*

- **Navigation:** `NFD Fuel Logistics > Executive Dashboards > Workshop, Alignment & Timesheets`
- **Buttons to Click:**
  1. Click `[ Executive Dashboards ]` &gt; Click `[ Workshop, Alignment & Timesheets ]`.
  2. Click on any mechanic column to drill down into assigned job cards.
- **What Happens:**
  - Tracks workshop labor timesheets and progress across active job cards.
  - Balances mechanic workload between routine services, chassis overhauls, and pump calibrations.

![Step 18: Workshop Labor Timesheets & Job Card Progress](docs/screenshots/06_dash_workshop_alignment.png)

---

### Step 19: Depot Inventory Requisition & Spare Parts Issue
**Phase:** `PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE`  
**Excel Reference:** *Pre-installed Inventory App > Central Spare Parts Catalog*

- **Navigation:** `Inventory > Products > Products`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Inventory ]` &gt; Click `[ Products ]` &gt; `[ Products ]`.
  2. Select product card (e.g. Scania filter kits, Mercedes fuel filters, Pirelli tyres).
- **What Happens:**
  - Issues workshop maintenance spares from central Otjiwarongo depot stock.
  - Real-time stock levels decrement automatically.

![Step 19: Depot Inventory Requisition & Spare Parts Issue](docs/screenshots/16_depot_inventory_stock.png)

---

### Step 20: Spare Parts Replenishment & 3-Way Matching Purchase Order
**Phase:** `PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE`  
**Excel Reference:** *Pre-installed Purchase App > OEM Supplier Procurement*

- **Navigation:** `Purchase > Purchase Orders`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Purchase ]` &gt; Click `[ Purchase Orders ]`.
  2. Select order `[ PO00004 ]` (Commercial Tyres Namibia).
- **What Happens:**
  - Generates supplier Purchase Order to replenish depot parts stock.
  - Enforces 3-way matching between Purchase Order, Warehouse Delivery Receipt, and Vendor Invoices before payment authorization.

![Step 20: Spare Parts Replenishment & Purchase Orders](docs/screenshots/17_purchases_spare_parts.png)

---

### Step 21: Commercial Freight Invoicing & Customer Billing
**Phase:** `PHASE E: COMMERCIAL BILLING & FINANCIAL CLOSE`  
**Excel Reference:** *Pre-installed Invoicing App > Freight Revenue & Margin Close*

- **Navigation:** `Invoicing > Customers > Invoices`
- **Buttons to Click:**
  1. Click App Switcher `[ ☷ ]` &gt; Click `[ Invoicing ]` &gt; Click `[ Customers ]` &gt; `[ Invoices ]`.
  2. Select invoice `[ INV/2026/0003 ]` for B2Gold Otjikoto.
- **What Happens:**
  - Generates customer freight invoice upon delivery confirmation.
  - Integrates fuel escalation surcharges and reconciles trip revenue against fuel expenses into general ledger accounts, closing the operational cycle.

![Step 21: Commercial Freight Invoicing & Customer Billing](docs/screenshots/19_invoicing_accounting.png)

---

## Appendix: Live Presentation Script (Clean Vehicle N 10420 OT)

To demonstrate Odoo's automated fleet intelligence live to client executives, execute the following 3-step live demo sequence using clean utility bakkie **`N 10420 OT`** (Chevrolet Utility 1.4i Support Bakkie).

### Step 1: Verify Initial Clean State in Fleet
1. Click **Fleet** &gt; **Vehicles** &gt; Open **`N 10420 OT`**.
2. Point out to the audience:
   - Current Odometer: `0.0 km`
   - Refuel Logs smart button: `Refuel Logs (0)`
   - Service Status badge: `OK` (`badge-success`)
   - Job Cards smart button: `Job Cards (0)`

### Step 2: Enter Milestone-Crossing Refuel Slip
1. Click **NFD Fuel Logistics** &gt; **Fuel Operations** &gt; **Vehicle Refuel Logsheets** &gt; Click `[ New ]`.
2. Fill in:
   - Vehicle: `N 10420 OT`
   - Driver: `Jaco Technician`
   - Start Odometer: `150,000.0 km`
   - End Odometer: `152,000.0 km` *(Distance: 2,000.0 km)*
   - Fuel Liters: `220.0 L` *(Efficiency: 9.09 KM/L vs 10.00 benchmark)*
   - Place: `Depot (Otjiwarongo)`
3. Click `[ Save ]`.

### Step 3: Observe the Real-Time Ripple Effect
1. Return to **Fleet** &gt; **Vehicles** &gt; Open **`N 10420 OT`**.
2. Point out the automated system updates:
   - **Odometer Auto-Advance:** Vehicle odometer jumped from `0.0 km` to `152,000.0 km`.
   - **Dynamic Service Status:** Crossing the 150,000 km threshold flipped status from `OK` to **`Service Due`**.
   - **Automated Job Card Creation:** Automation 3 detected the status and generated maintenance task **`JC-AUTO-49`** assigned directly to lead mechanic **Clive**! Smart button now displays **`Job Cards (1)`**.
