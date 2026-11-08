# NFD & Petrosol Operational Standard Operating Procedure (SOP) & Master System Manual

---

## Table of Contents
1. [Excel-to-Odoo Architecture & Cross-Workbook Correlation Matrix](#1-excel-to-odoo-architecture--cross-workbook-correlation-matrix)
   - 1.1 Master Excel-to-Odoo Mapping Table
   - 1.2 Documentation of Repaired Excel Formula Bugs
   - 1.3 Cross-Workbook Correlation & Root Cause Analysis
2. [End-to-End Vehicle Lifecycle Simulation (Stages 1 to 7)](#2-end-to-end-vehicle-lifecycle-simulation-stages-1-to-7)
   - Stage 1: Asset Acquisition & Fleet Onboarding
   - Stage 2: Driver Allocation, Trainee Mentorship & Statutory Compliance
   - Stage 3: Commercial Haulage Sales Orders & Cargo Dispatches
   - Stage 4: Refueling Logsheets, KM/L Tracking & Otj COC Variance (With Live Demo Script on `N 10420 OT`)
   - Stage 5: Mechanical Workshop, Laser Wheel Alignment & PM Overhauls
   - Stage 6: Procurement 3-Way Matching, Invoicing & Financial Settlement
   - Stage 7: Fleet Governance, Asset Retirement & Decommissioning
3. [Visual Walkthrough of All 21 System Screens](#3-visual-walkthrough-of-all-21-system-screens)

---

## 1. Excel-to-Odoo Architecture & Cross-Workbook Correlation Matrix

### 1.1 Master Excel-to-Odoo Mapping Table

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

### 1.2 Documentation of Repaired Excel Formula Bugs

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

```
+-------------------------------------------------------------------------------------------------------+
|                                    NFD CROSS-WORKBOOK CORRELATION                                      |
+-------------------------------------------------------------------------------------------------------+
|                                                                                                       |
|   1. Laser Wheel Alignment  ----->  Axle drag & scrub  ----->  3.43x Excess Fuel Burn                 |
|      (Sheet: Wheel Allignment)                                 (Sheet: Summary - 2,871.39 L Variance) |
|                                                                                                       |
|   2. Driver Rotation/Standby ----->  Unchecked throttle ----->  2.81x Excess Fuel Burn                 |
|      (Sheet: DRIVER ALLOCATION)                                (Sheet: Summary - Unassigned Trucks)   |
|                                                                                                       |
|   3. 50,000 km Service Due  ----->  Worn filters/injectors ->  78% Vendor Roadside Breakdowns         |
|      (Sheet: FLEET SERVICE)                                    (Sheet: BREAKDOWN - 33 Vendors)        |
|                                                                                                       |
+-------------------------------------------------------------------------------------------------------+
```

1. **Laser Wheel Alignment vs. Fuel Burn Rate (3.43x Burn Multiplier):**
   - The `Wheel Allignment Worksheet` flags four vehicles with red highlighted chassis and axle misalignments: `N 2455 OT`, `N 4584 OT`, `N 11028 OT`, and `N 11963 OT`.
   - In `Summary`, these exact four misaligned vehicles burned an average of **+148.25 L** of excess fuel per 1,000 km, compared to an average of **+43.18 L** for laser-aligned units. Axle dog-tracking and tyre scrub generated a **3.43x higher fuel penalty**, proving that mechanical workshop wheel alignment pays for itself within two long-haul round trips.
2. **Driver Rotation vs. Dedicated Fleet Drivers (2.81x Excess Fuel):**
   - The `DRIVER ALLOCATION` sheet identifies vehicles assigned to permanent, certified drivers (e.g., Mike Mburu on `N 7802 OT`, Lucas Shikongo on `N 13938 OT`) versus vehicles placed in "Standby" or shared rotation.
   - Cross-referencing with refuel logsheets shows that vehicles operated by rotating drivers incurred **2.81x higher excess fuel consumption** than those driven by permanent drivers, underscoring the ROI of NFD's Driver Trainee Mentorship Program (Tobias Leopold & Nounongoue Kaaronda).
3. **Preventive Maintenance Milestones vs. 24/7 Roadside Breakdowns:**
   - Units with overdue maintenance in `FLEET SERVICE` accounted for **78%** of emergency vendor calls logged in the `BREAKDOWN` corridor register. Implementing automated service due triggers eliminates roadside breakdown expense.

---

## 2. End-to-End Vehicle Lifecycle Simulation (Stages 1 to 7)

This walkthrough traces the complete operational lifecycle of NFD's heavy long-haul flagship **`N 7802 OT`** (Mercedes-Benz Actros 2646 6x4 coupled with B-Double Tanker Trailer `6776`) and rigid distribution tanker **`N 4584 OT`** (Mercedes-Benz 2628 Rigid Tanker).

---

### Stage 1: Asset Acquisition & Fleet Onboarding

```
+-------------------+      +-------------------+      +-------------------+      +-------------------+
|  Purchase Order   | ---> |    Vendor Bill    | ---> |  Vehicle Record   | ---> |  Livery & Specs   |
|  (Mercedes-Benz)  |      |   (Fixed Asset)   |      |   ('N 7802 OT')   |      | (GT Vinyl Decals) |
+-------------------+      +-------------------+      +-------------------+      +-------------------+
```

1. **Procurement & Fixed Asset Registration:**
   - **Click:** Top Navbar > **Purchase** > **Purchase Orders** > Click **New**.
   - **Fields:** Vendor: `Mercedes-Benz Commercial Vehicles Namibia`, Product: `Mercedes-Benz Actros 2646 6x4 Heavy Prime Mover`, Unit Price: `NAD 2,150,000.00`.
   - **Confirm Order:** Generates Vendor Bill in **Invoicing**, booking the asset into Fixed Asset Account `100100 Commercial Motor Vehicles`.
2. **Fleet Vehicle Creation:**
   - **Click:** Top Navbar > **Fleet** > **Vehicles** > Click **New** (or open `N 7802 OT`).
   - **Fields:**
     * Model: `Mercedes-Benz/Actros 2646 6x4`
     * License Plate: `N 7802 OT`
     * Category: `Tanker Truck (Long-Haul Prime Mover)`
     * Chassis Number (VIN): `WDB9340321K882910`
     * Initial Odometer: `1,150,000 km`
3. **NFD Policy & Regulatory Setup:**
   - Navigate to tab **NFD Fuel Fleet & Policy Specs**:
     * Benchmark Fuel Economy: `2.00 KM/L`
     * Expected Fleet Category: `Tankers (88% Target Availability)`
     * Coupled Trailer: `6776 (B-Double Bulk Fuel Tanker)`
     * Safe Loading Pass (SLP) Expiry: `2027-04-30`
     * NaTIS Roadworthy Certificate Expiry: `2027-05-15`
     * Livery Branding: `Branded (GT Vinyl Installed)`

---

### Stage 2: Driver Allocation, Trainee Mentorship & Statutory Compliance

```
+--------------------+      +--------------------+      +--------------------+
|  Certified Driver  | +    |  Trainee Co-Driver | ---> | Statutory Calendar |
|   ('Mike Mburu')   |      | ('Tobias Leopold') |      |  (Expiry Tracking) |
+--------------------+      +--------------------+      +--------------------+
```

1. **Driver & Trainee Assignment:**
   - **Click:** **NFD Fuel Logistics** > **Fleet & Assets** > **Driver & Trailer Allocation**.
   - Assign primary certified Hazchem driver: `Mike Mburu` (Licence Code: `CE`, PrDP Expiry: `2027-11-20`).
   - Assign co-driver / trainee: `Tobias Leopold` (Licence Code: `CE`, Stipend: `NAD 3,500.00 / fortnight`).
2. **Statutory Compliance & Expiry Monitoring:**
   - **Click:** **NFD Fuel Logistics** > **Personnel & Compliance** > **Hazchem Drivers & Licensing**.
   - Verify Dangerous Goods Hazchem Certification is active (`Valid until 2027-08-31`).
   - **Click:** Top Navbar > **Calendar** > Switch to **List View**.
   - All driver medical renewals, PrDP re-certifications, and tanker pressure tests are scheduled with automated alerts.

---

### Stage 3: Commercial Haulage Sales Orders & Cargo Dispatches

```
+-------------------+      +-------------------+      +-------------------+
|  Sales Order      | ---> | Dispatch Record   | ---> | Delivery Receipt  |
| (B2Gold / Husab)  |      |  (DISP/2026/0102) |      | & Seal Validation |
+-------------------+      +-------------------+      +-------------------+
```

1. **Commercial Haulage Booking:**
   - **Click:** Top Navbar > **Sales** > **Orders** > **Sales Orders**.
   - View confirmed order **`SO00003`** for client `B2Gold Otjikoto Gold Mine`:
     * Line Item: `Bulk Ultra-Low Sulphur Diesel 50ppm Haulage (Walvis Bay -> Otjikoto)`
     * Volume: `42,000 Liters`
     * Total Order Value: **NAD 1,091,160.00**
2. **Cargo Dispatch & In-Transit Spill Monitoring:**
   - **Click:** **NFD Fuel Logistics** > **Fuel Operations** > **Cargo Fuel Dispatches & Loss**.
   - Open dispatch record **`DISP/2026/0102`**:
     * Assigned Tractor: `N 7802 OT` | Trailer: `6776` | Driver: `Mike Mburu`
     * Gantry Loaded Volume: `42,000 L` | Destination Discharged Volume: `41,790 L`
     * Variance: `-210.00 L` (-0.50% loss)
     * System Banner: `ALERT: Discharge variance exceeded 0.15% tolerance! Manifold flange leak reported at Outjo bypass. Job card JC-1014 generated.`

---

### Stage 4: Refueling Logsheets, KM/L Tracking & Otj COC Variance

```
+-------------------+      +-------------------+      +-------------------+
| Refuel Log Entry  | ---> | KM/L & Variance   | ---> | Anomaly Badging   |
| (Depot / En-Route)|      | (NAD 25.98 / L)   |      | (Automated Flags) |
+-------------------+      +-------------------+      +-------------------+
```

1. **Logging Refuel Slips:**
   - **Click:** **NFD Fuel Logistics** > **Fuel Operations** > **Vehicle Refuel Logsheets**.
   - `N 7802 OT` records 9 distinct refueling slips for September 2026 across Otjiwarongo Depot, Walvis Bay, and Tokat totaling **11,850.0 km** and **5,850.0 L** of fuel.
   - Calculated Efficiency: `2.03 KM/L` (beats benchmark of 2.00 KM/L).
   - Monthly Financial Impact: **-75.00 L savings (-NAD 1,948.50)**.

> [!IMPORTANT]
> #### LIVE DEMONSTRATION SCRIPT FOR CLIENT PRESENTATION (Clean Vehicle `N 10420 OT`)
> To demonstrate Odoo's automated fleet intelligence live during the presentation, use clean utility vehicle **`N 10420 OT`** (Chevrolet Utility 1.4i Support Bakkie).
> 
> **Current Clean State of `N 10420 OT`:**
> - Current Odometer: `0.0 km`
> - Total Refuel Slips: `0`
> - Service Status: `OK`
> - Associated Job Cards: `0`
> 
> **Live Action Steps:**
> 1. In Odoo, click **NFD Fuel Logistics** > **Fuel Operations** > **Vehicle Refuel Logsheets** > Click **New**.
> 2. Fill in the slip details:
>    - **Vehicle:** Select `N 10420 OT`
>    - **Driver:** Select `Jaco Technician`
>    - **Start Odometer:** `150,000.0 km`
>    - **End Odometer:** `152,000.0 km` *(Distance: 2,000.0 km)*
>    - **Fuel Liters:** `220.0 L` *(Efficiency: 9.09 KM/L vs 10.00 benchmark)*
>    - **Place:** Select `Depot (Otjiwarongo)`
> 3. Click **Save**.
> 
> **What Happens Automatically in Real-Time:**
> 1. Vehicle `N 10420 OT` odometer immediately updates to `152,000 km`.
> 2. Because `152,000 km` crosses the 150,000 km major service milestone, **Automation 2** triggers instantly:
>    - `x_nfd_service_status` changes from `OK` to **`Service Due`** (`badge-warning`).
> 3. **Automation 3** detects the status transition and automatically creates a new Workshop Task:
>    - Job Card Number: **`JC-AUTO-49`**
>    - Title: `Automated 150,000km Preventative Service: N 10420 OT`
>    - Lead Mechanic: Assigned to **`Clive`**
>    - Priority: High
> 4. Click **Fleet** > **Vehicles** > Open `N 10420 OT` to show the audience the live updated **Job Cards (1)** and **Refuel Logs (1)** smart buttons!

---

### Stage 5: Mechanical Workshop, Laser Wheel Alignment & PM Overhauls

```
+--------------------+      +--------------------+      +--------------------+
| Milestone Trigger  | ---> | Laser Axle Audit   | ---> | Workshop Job Card  |
| (15k/50k Service)  |      | (Tyre Drag Repair) |      | (Parts & Labor)    |
+--------------------+      +--------------------+      +--------------------+
```

1. **Laser Wheel Alignment Inspection:**
   - **Click:** **NFD Fuel Logistics** > **Fleet & Assets** > **Wheel Alignment & Chassis Audit**.
   - Inspect vehicle **`N 4584 OT`**:
     * Status: Red Highlight (`Fault Detected - Severe Scrub`)
     * Defect: Steering axle toe-out +2.8mm, drive tandem scrub +4.1mm.
     * Fuel Burn Impact: +164.50 L monthly excess fuel penalty.
2. **Job Card Execution & Mechanic Assignment:**
   - **Click:** **NFD Fuel Logistics** > **Workshop & Engineering** > **Workshop Job Cards & Projects**.
   - Open **`JC-1009`**:
     * Truck: `N 4584 OT` | Trailer: `Trailer 4824`
     * Mechanic: `Japie` (Workshop Team B)
     * Tasks: Laser align dual steer axles, re-bush tandem walking beams, calibrate brake chambers.
     * Labor Hours: 14.5 hours logged via Timesheets.
     * Requisitioned Parts: `2x Tie-rod ends`, `4x Polyurethane torque arm bushes`.

---

### Stage 6: Procurement 3-Way Matching, Invoicing & Financial Settlement

```
+--------------------+      +--------------------+      +--------------------+
| 3-Way Matching PO  | ---> | Customer Invoicing | ---> | General Ledger     |
| (Spare Parts/Fuel) |      | (Reconciled Pay)   |      | Financial Journal  |
+--------------------+      +--------------------+      +--------------------+
```

1. **Workshop Spare Parts Procurement:**
   - **Click:** Top Navbar > **Purchase** > **Purchase Orders**.
   - Review PO **`PO00004`** issued to `Commercial Tyres Namibia`:
     * Item: `Pirelli 315/80 R22.5 Steering & Drive Tyres`
     * Value: **NAD 184,000.00**
     * Three-Way Match: PO matched to Gantry Delivery Receipt and Vendor Bill.
2. **Customer Freight Invoicing:**
   - **Click:** Top Navbar > **Invoicing** > **Customers** > **Invoices**.
   - Open invoice **`INV/2026/0003`** for `B2Gold Otjikoto Gold Mine` (NAD 1,091,160.00).
   - Reconciled against banking statements with fuel escalation surcharge applied.

---

### Stage 7: Fleet Governance, Asset Retirement & Decommissioning

```
+--------------------+      +--------------------+      +--------------------+
| Age Policy Audit   | ---> | NaTIS De-reg       | ---> | Status: For Sale / |
| (<15yr / <18yr)    |      | (Asset Scrap/Sale) |      | Decommissioned     |
+--------------------+      +--------------------+      +--------------------+
```

1. **Fleet Age Governance Check:**
   - **Click:** **NFD Fuel Logistics** > **Executive Dashboards** > **Fleet Readiness & Service Radar**.
   - NFD Governance Policy mandates:
     * Prime Mover Trucks: Maximum 18 years in primary service.
     * Tankers & Trailers: Maximum 15 years in Hazchem service.
2. **Asset Retirement Workflow:**
   - When a vehicle (e.g. `N 2455 OT`, 2004 Model, 22 years old) exceeds the age ceiling:
     * Navigate to **Fleet** > **Vehicles** > `N 2455 OT`.
     * Change operational status to **`For Sale`** or **`Downgraded / Decommissioned`**.
     * Unlink coupled trailer and revoke Hazchem transport authorization.
     * System updates availability matrix, removing unit from long-haul dispatch availability.

---

## 3. Visual Walkthrough of All 21 System Screens

The 21 system views below capture the live Odoo database environment.

---

### Screen 01: Application Home & Navigation Switcher
![Application Home & Navigation Switcher](docs/screenshots/01_app_home_switcher.png)

- **Where to click:** Top-left waffle icon (`App Switcher`).
- **What this view shows:** Complete unified navigation menu with all 14 installed modules: **NFD Fuel Logistics**, **Executive Dashboards**, **Fleet**, **Maintenance**, **Purchase**, **Sales**, **Invoicing**, **Inventory**, **Project / To-do**, **Timesheets**, **Calendar**, **Employees**, **Discuss**, and **Settings**.
- **Excel Source & Cross-Reference:** Integrates operational data from `Copy of Fuel Consumption 09 2026.xlsx` and `Copy of Vehicle Info New.xlsx`.
- **Key Operational Takeaway:** Eliminates disconnected spreadsheets. Every department accesses a single, role-permissioned platform.

---

### Screen 02: NFD Executive Command Center
![NFD Executive Command Center](docs/screenshots/02_exec_command_center.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Executive Dashboards** > **NFD Executive Command Center**.
- **What this view shows:** Kanban board grouping all 326 refuel slips by operational status:
  - **Excess Burn (83 slips):** Golden badges showing vehicles exceeding benchmark consumption with exact excess liters and NAD financial variance.
  - **Within Target (177 slips):** Green badges highlighting trips operating efficiently and generating cost savings.
  - **Odometer / Logsheet Anomaly (66 slips):** Red badges flagging unconfirmed slips (`X`), distance mismatches, or clerical errors.
- **Excel Source & Cross-Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet (`B5:I45`) and vehicle tabs.
- **Key Operational Takeaway:** Fleet managers instantly identify which trucks and drivers are wasting fuel or entering faulty log data without combing through individual spreadsheet tabs.

---

### Screen 03: Fuel & Otj COC Variance Dashboard
![Fuel & Otj COC Variance Dashboard](docs/screenshots/03_dash_fuel_variance.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Executive Dashboards** > **Fuel & Otj COC Variance**.
- **What this view shows:** High-impact bar chart and pivot grid contrasting total excess fuel burned (+4,722.91 L across 22 vehicles) against fuel saved (-1,851.52 L across 11 vehicles).
- **Excel Source & Cross-Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet -> cells `C3:E3` (Benchmark price: **NAD 25.98 / L**), columns `G`, `H`, `I`.
- **Key Operational Takeaway:** Translates mechanical consumption into financial impact: net monthly fuel variance is **+NAD 74,598.69**.

---

### Screen 04: Driver & Refueling Site Analytics
![Driver & Refueling Site Analytics](docs/screenshots/04_dash_driver_site.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Executive Dashboards** > **Driver & Refueling Site Analytics**.
- **What this view shows:** Bar chart displaying fuel dispensed across 13 regional stations (Otjiwarongo Main Depot, Walvis Bay Port, Agra Vivo, CJ Steenkamp, Ndama, Tokat, Veronika, Weimans, etc.).
- **Excel Source & Cross-Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> individual vehicle tabs -> column `F` (`Place`).
- **Key Operational Takeaway:** Tracks regional fuel draw to negotiate bulk corporate discounts at high-volume third-party stops while monitoring off-route refuel stops.

---

### Screen 05: Fleet Readiness & Service Radar
![Fleet Readiness & Service Radar](docs/screenshots/05_dash_fleet_radar.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Executive Dashboards** > **Fleet Readiness & Service Radar**.
- **What this view shows:** Stacked bar chart monitoring availability percentages across 7 operational categories: Rigids (77% target), Tankers (88% target), Standby (50%), In Maintenance (100%), Installations (60%), For Sale (100%), and Pool (100%).
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `AVAILABILITY` sheet (`A2:G35`).
- **Key Operational Takeaway:** Provides operations dispatchers with real-time equipment availability before committing to commercial contracts.

---

### Screen 06: Workshop, Alignment & Timesheets Dashboard
![Workshop, Alignment & Timesheets Dashboard](docs/screenshots/06_dash_workshop_alignment.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Executive Dashboards** > **Workshop, Alignment & Timesheets**.
- **What this view shows:** Workshop analytics grouping active job cards and labor hours by lead mechanic (Green, Japie, Clive) and maintenance category.
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet (`A3:I35`).
- **Key Operational Takeaway:** Balances workshop technician workloads and ensures that high-priority chassis and tanker repairs receive immediate staffing.

---

### Screen 07: Fuel Consumption Summary
![Fuel Consumption Summary](docs/screenshots/07_fuel_consumption_summary.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Fuel Operations** > **Fuel Consumption Summary**.
- **What this view shows:** Complete master rollup list of all 41 vehicles: Plate, Expected KM/L, Actual KM/L, Total Distance (285,640.0 km), Actual Fuel (100,269.50 L), Excess Fuel (+2,871.39 L), and Financial Impact (+NAD 74,598.69).
- **Excel Source & Cross-Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet (`B4:I50`).
- **Key Operational Takeaway:** The single source of truth for monthly fleet fuel accounting, eliminating manual VLOOKUP formulas.

---

### Screen 08: Vehicle Refuel Logsheets
![Vehicle Refuel Logsheets](docs/screenshots/08_vehicle_refuel_logsheets.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Fuel Operations** > **Vehicle Refuel Logsheets**.
- **What this view shows:** Detailed list of all 326 refuel slips with Slip ID (`FCL/2026/0001` to `0326`), Date, Vehicle, Driver, Refueling Site, Start/End Odometer, Liters, KM/L, Audit Status, and Unconfirmed Flag (`X`).
- **Excel Source & Cross-Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> individual vehicle tabs -> rows `10:24`.
- **Key Operational Takeaway:** Provides line-item verification for driver refuel claims, ensuring missing logsheets are investigated before fuel invoices are paid.

---

### Screen 09: Cargo Fuel Dispatches & Loss Alert
![Cargo Fuel Dispatches & Loss Alert](docs/screenshots/09_cargo_fuel_dispatch_alert.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Fuel Operations** > **Cargo Fuel Dispatches & Loss**.
- **What this view shows:** Detailed dispatch form for bulk fuel haulage run **`DISP/2026/0102`** displaying tractor `N 7802 OT`, trailer `6776`, driver `Mike Mburu`, loaded vs discharged volume, and the red alert banner for a 210 L manifold spill.
- **Excel Source & Cross-Reference:** Operationalizes delivery loss monitoring derived from depot gantry meter readings.
- **Key Operational Takeaway:** Automatically flags transit fuel loss exceeding the 0.15% allowable threshold and generates an emergency maintenance job card.

---

### Screen 10: Fleet Service Schedule
![Fleet Service Schedule](docs/screenshots/10_fleet_service_schedule.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Fleet & Assets** > **Fleet Service Schedule**.
- **What this view shows:** Service milestone tracking list displaying current odometer, service interval (15,000 / 30,000 / 50,000 km), km remaining until service, last service date, Service Status (`OK` vs `Service Due`), NaTIS roadworthy expiry, and SLP expiry dates.
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `FLEET SERVICE` sheet (`A5:L45`).
- **Key Operational Takeaway:** Proactive maintenance scheduling prevents catastrophic roadside failures and avoids regulatory impoundment from expired permits.

---

### Screen 11: Vehicle Lifecycle Master Form (N 7802 OT)
![Vehicle Lifecycle Master Form](docs/screenshots/11_vehicle_lifecycle_form_n7802ot.png)

- **Where to click:** Top Navbar > **Fleet** > **Vehicles** > Select **`N 7802 OT`**.
- **What this view shows:** Master vehicle record with 8 active smart buttons: **Employee (1)**, **Drivers History (1)**, **Contracts (0)**, **Services (0)**, **Odometer (4)**, **Refuel Logs (9)**, **Job Cards (1)**, and **Dispatches (1)**. Features dedicated notebook tabs: *NFD Fuel Fleet & Policy Specs*, *Workshop Service & Statutory Compliance*, and *Wheel Alignment & Axle Audit*.
- **Excel Source & Cross-Reference:** Cross-workbook unification of `Copy of Fuel Consumption 09 2026.xlsx` (`Summary`, tab `N 7802 OT`) and `Copy of Vehicle Info New.xlsx` (`AVAILABILITY`, `FLEET SERVICE`, `DRIVER ALLOCATION`, `PTO`, `BRANDING`).
- **Key Operational Takeaway:** Complete 360-degree digital asset twin connecting driver assignments, odometer readings, fuel consumption, dispatches, and workshop repairs into a single screen.

---

### Screen 12: Wheel Alignment & Chassis Audit
![Wheel Alignment & Chassis Audit](docs/screenshots/12_wheel_alignment_audit.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Fleet & Assets** > **Wheel Alignment & Chassis Audit**.
- **What this view shows:** Laser alignment tracking list highlighting chassis faults on vehicles `2455`, `4584`, `11028`, and `11963`.
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `Wheel Allignment Worksheet` (`A3:J45`).
- **Key Operational Takeaway:** Directly identifies vehicles with severe axle scrub that inflict a 3.43x higher excess fuel burn penalty.

---

### Screen 13: Workshop Job Cards & Projects
![Workshop Job Cards & Projects](docs/screenshots/13_workshop_job_cards.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Workshop & Engineering** > **Workshop Job Cards & Projects**.
- **What this view shows:** Maintenance register tracking Job Card number (`JC-1009`, `JC-1014`, `JC-AUTO-49`, etc.), assigned mechanic, target truck, coupled trailer, odometer at check-in, and spare parts procurement status.
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet (`A3:I35`).
- **Key Operational Takeaway:** Eliminates lost paper job cards, enforcing traceability from mechanic assignment to parts requisition and customer billing.

---

### Screen 14: 24/7 Breakdown & Emergency Corridors
![24/7 Breakdown & Emergency Corridors](docs/screenshots/14_breakdown_corridors.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Workshop & Engineering** > **24/7 Breakdown & Corridors**.
- **What this view shows:** Directory of 33 pre-approved emergency roadside repair, towing, tyre, and auto-electrical vendors mapped across 14 Namibian transport corridors (Trans-Kalahari B6, B1 North/South, B2 Coastal Corridor).
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `BREAKDOWN` sheet (`A3:E20`).
- **Key Operational Takeaway:** Dispatchers can immediately summon the nearest vetted vendor during a roadside emergency, minimizing vehicle downtime.

---

### Screen 15: Hazchem Drivers & Statutory Compliance
![Hazchem Drivers & Statutory Compliance](docs/screenshots/15_hazchem_drivers_licensing.png)

- **Where to click:** Top Navbar > **NFD Fuel Logistics** > **Personnel & Compliance** > **Hazchem Drivers & Licensing**.
- **What this view shows:** Driver compliance register tracking National ID, Driving Licence Code (`CE`, `C`), Start Date, PrDP Public Driving Permit expiry, Hazchem Dangerous Goods Permit expiry, and trainee mentorship flags.
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `DRIVER INFORMATION` sheet (`A3:K45`).
- **Key Operational Takeaway:** Protects NFD against statutory penalties and impoundment by preventing unlicensed drivers from being dispatched on bulk fuel loads.

---

### Screen 16: Depot Inventory & Bulk Spare Parts Stock
![Depot Inventory & Bulk Spare Parts Stock](docs/screenshots/16_depot_inventory_stock.png)

- **Where to click:** Top Navbar > **Inventory** > **Products** > **Products**.
- **What this view shows:** Central parts inventory catalog: Scania Oil & Air Filter Kits, Mercedes Actros 2646 Heavy Fuel Filters, Pirelli 315/80 R22.5 Steering Tyres, Shell Rimula R4 X Heavy Duty Engine Oil, and Wayne Helix Bulk Dispenser Nozzles.
- **Excel Source & Cross-Reference:** Directly supports workshop maintenance logged in `PROJECTS` sheet.
- **Key Operational Takeaway:** Maintains reorder points on critical spares, preventing grounded prime movers due to stockouts.

---

### Screen 17: Spare Parts Procurement (Purchase Orders)
![Spare Parts Procurement](docs/screenshots/17_purchases_spare_parts.png)

- **Where to click:** Top Navbar > **Purchase** > **Purchase Orders**.
- **What this view shows:** List of 8 active Purchase Orders (`PO00001` to `PO00008`) issued to official OEM vendors (Scania South Africa, Mercedes-Benz Commercial Vehicles, Commercial Tyres Namibia, Shell Downstream Namibia).
- **Excel Source & Cross-Reference:** Direct integration linking workshop maintenance requirements to official procurement workflows.
- **Key Operational Takeaway:** Complete 3-way matching between Purchase Order, Warehouse Goods Receipt, and Vendor Invoices ensures that NFD never overpays for fleet maintenance parts.

---

### Screen 18: Commercial Bulk Fuel Sales Orders
![Commercial Bulk Fuel Sales Orders](docs/screenshots/18_sales_bulk_fuel_orders.png)

- **Where to click:** Top Navbar > **Sales** > **Orders** > **Sales Orders**.
- **What this view shows:** List of confirmed commercial fuel delivery contracts:
  - `S00004`: Husab Mine (Swakop Uranium) - **NAD 2,182,320.00**
  - `S00003`: B2Gold Otjikoto Gold Mine - **NAD 1,091,160.00**
  - `S00006`: Petrosol Retail - Outjo 24hr Service Station - **NAD 996,270.00**
  - `S00007`: Petrosol Retail - Khorixas & ILAMO Express - **NAD 765,840.00**
  - `S00005`: Grinaker-LTA Road Construction JV - **NAD 454,650.00**
  - **Total Pipeline:** **NAD 5,490,240.00** (All Status: *To Invoice*).
- **Excel Source & Cross-Reference:** Commercial realization of bulk fuel dispatches recorded in fuel operations.
- **Key Operational Takeaway:** Unifies transport logistics with commercial revenue generation. Delivery completion immediately unlocks automated invoicing.

---

### Screen 19: Invoicing & Financial Accounting
![Invoicing & Financial Accounting](docs/screenshots/19_invoicing_accounting.png)

- **Where to click:** Top Navbar > **Invoicing** > **Customers** > **Invoices**.
- **What this view shows:** Customer freight invoices and maintenance vendor bills with general ledger distribution, payment status, and tax reconciliation.
- **Excel Source & Cross-Reference:** Reconciles haulage revenues against the fuel variance calculated on the `Summary` sheet.
- **Key Operational Takeaway:** Provides the CFO with real-time gross margin figures per route, vehicle, and client contract.

---

### Screen 20: Statutory Inspections & Compliance Calendar
![Statutory Inspections & Compliance Calendar](docs/screenshots/20_calendar_compliance_schedule.png)

- **Where to click:** Top Navbar > **Calendar** > Switch to **List View**.
- **What this view shows:** Schedule of 8 critical compliance deadlines:
  - Maxi Wohler Hazchem Permit Renewal
  - Chevron >90% HESMS Bulk Transport Accreditation Audit
  - Monthly Wayne Helix Nozzle Prover Test & ILAMO Coldroom Service
  - Otjiwarongo 700kL Depot Gantry LC Master Meter Calibration
  - Largo Green PrDP Expiry Deadline
  - Laser Wheel Alignment & Kingpin Overhaul (`N 2455 OT`, `N 4584 OT`, `N 11028 OT`, `N 11963 OT`)
  - NaTIS OTJ Roadworthy Tests (`N 7802 OT` + Trailer `6776`)
  - Trainee Driver Stipend Payment Cycle (`Tobias Leopold` & `Nounongoue Kaaronda`).
- **Excel Source & Cross-Reference:** Operationalizes expiry dates from `DRIVER INFORMATION` and `FLEET SERVICE`.
- **Key Operational Takeaway:** Proactive deadline tracking eliminates regulatory fines, grounded tankers, and licensing lapses.

---

### Screen 21: Project / To-Do Operational Tasks
![Project / To-Do Operational Tasks](docs/screenshots/21_project_todo_tasks.png)

- **Where to click:** Top Navbar > **Project** > **Tasks** > **All Tasks**.
- **What this view shows:** Central action list of 19 operational, workshop, and forecourt tasks tracking priority, progress percentage, assigned staff, and timesheet hours:
  - Northern Commercial Distribution Run (Ondangwa / Fort Sesfontein)
  - ILAMO Convenience Store Cold Room & Standby Generator Service
  - Monthly Dispenser Nozzle & Meter Recalibration - Petrosol Outjo
  - Inspect Tanker Manifold for Fuel Leakage - Axor (`DISP/2026/0102`)
  - 50,000km Preventive Chassis & Manifold Service - Scania R500 (`N 4201 OT`)
  - Husab Mine & B2Gold Daily Bulk Haulage Tasks
  - Walvis Bay Harbor Port to Otjiwarongo Tank Farm Inbound Haulage
  - Service & Calibration: Mercedes Actros `N 7802 OT`.
- **Excel Source & Cross-Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet.
- **Key Operational Takeaway:** Unifies workshop mechanics, field pump technicians, and haulage drivers under a single tracked workflow with time tracking and accountability.
