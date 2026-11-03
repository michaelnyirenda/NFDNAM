# NFD & Petrosol Standard Operating Procedure (SOP) & Step-by-Step Navigation Guide

This document is a direct, click-by-click operational guide for navigating the **NFD Fuel Logistics** system in Odoo (Docker demo and Cloud SaaS demo). Every view, button, and action connects directly to the source Excel workbooks provided by Northern Fuel Distributors (NFD) and Petrosol.

---

## 1. Direct Excel-to-Odoo Cross Reference

| Excel File | Sheet Name | Cell Range | Odoo Menu Navigation | View / Action Name | What It Does & Calculates |
|---|---|---|---|---|---|
| `Copy of Fuel Consumption 09 2026.xlsx` | `Summary` | `B5:I45` | **Fuel Operations > Fuel Consumption Summary** | `action_nfd_fuel_summary` | Fleet-wide rollup of all 41 vehicles: 285,640.0 KM distance, 100,269.50 L actual fuel, +2,871.39 L excess variance (+NAD 74,598.69 at NAD 25.98 / L benchmark). |
| `Copy of Fuel Consumption 09 2026.xlsx` | `Summary` | `C3:E3` | **Executive Dashboards > Fuel & Otj COC Variance** | `action_nfd_dash_fuel_variance` | Charts excess fuel burners (22 vehicles, +4,722.91 L / +NAD 122,701.18) vs star fuel savers (11 vehicles, -1,851.52 L / -NAD 48,102.49) valued at Otjiwarongo benchmark price NAD 25.98 / L. |
| `Copy of Fuel Consumption 09 2026.xlsx` | Individual tabs (`N 12007 OT` etc.) | `B10:N24` | **Fuel Operations > Vehicle Refuel Logsheets** | `action_nfd_fuel_consumption_log` | 326 refuel slip records with Start/End Odometer, KM/L efficiency, refueling station/stop, driver, and unconfirmed logsheet audit flags (`X`). |
| `Copy of Fuel Consumption 09 2026.xlsx` | Individual tabs | `F10:F24` | **Executive Dashboards > Driver & Refueling Site Analytics** | `action_nfd_dash_driver_site` | Refueling volumes and fuel draw across 13 regional sites (Agra Vivo, CJ Steenkamp, Ndama, Otjiwarongo Depot, Tokat, Veronika, Walvis Bay, Weimans). |
| `Copy of Vehicle Info New.xlsx` | `AVAILABILITY` | `A2:G35` | **Executive Dashboards > Fleet Readiness & Service Radar** | `action_nfd_dash_fleet_radar` | Stacked bar chart of fleet readiness across 7 operational categories (Rigids 77% target, Tankers 88% target, Standby 50%, Maintenance 100%, Installations 60%, For Sale 100%, Pool 100%) and 15/18-year replacement policy status. |
| `Copy of Vehicle Info New.xlsx` | `FLEET SERVICE` | `A5:L45` | **Fleet & Assets > Fleet Service Schedule** | `action_nfd_fleet_service_schedule` | Preventive maintenance odometer milestones (15k/30k/50k km intervals), last service date, km remaining until service, NaTIS license, roadworthy fitness, and SLP expiry dates. |
| `Copy of Vehicle Info New.xlsx` | `AVAILABILITY` | `A2:G35` | **Fleet & Assets > Fleet Availability & Grouping** | `action_nfd_fleet_availability` | Operational status of all 94 fleet units categorized by tanker, rigid, standby, and workshop maintenance status. |
| `Copy of Vehicle Info New.xlsx` | `DRIVER ALLOCATION` | `A3:F40` | **Fleet & Assets > Driver & Trailer Allocation** | `action_nfd_driver_trailer_allocation` | Prime mover tractors paired with permanent certified drivers, trainee co-drivers (Tobias Leopold, Nounongoue Kaaronda), coupled B-double pup trailers, and standby notes. |
| `Copy of Vehicle Info New.xlsx` | `BRANDING` | `A3:D45` | **Fleet & Assets > Corporate Livery & Branding** | `action_nfd_corporate_branding` | Corporate livery audit tracking branded vehicles vs units requiring vinyl decal installation at GT Vinyl with location notes. |
| `Copy of Vehicle Info New.xlsx` | `PTO` | `A3:F30` | **Fleet & Assets > PTO & Hydraulic Systems** | `action_nfd_pto_systems` | Auxiliary engine PTOs, transmission hydraulic PTOs, and pump mounting positions (Behind the Cab, On Cab next to COC Tank, Tanker Chassis). |
| `Copy of Vehicle Info New.xlsx` | `Wheel Allignment Worksheet` | `A3:J45` | **Fleet & Assets > Wheel Alignment & Chassis Audit** | `action_nfd_wheel_alignment` | Laser axle and kingpin alignment audit. Red highlighting flags chassis faults on vehicles 2455, 11028, 4584, and 11963 causing tyre drag and fuel burn penalties. |
| `Copy of Vehicle Info New.xlsx` | `PROJECTS` | `A3:I35` | **Executive Dashboards > Workshop, Alignment & Timesheets** | `action_nfd_dash_workshop_alignment` | Visual dashboard of workshop job cards grouped by lead mechanic (Green, Japie, Clive), job card category, and labor timesheet allocation. |
| `Copy of Vehicle Info New.xlsx` | `PROJECTS` | `A3:I35` | **Workshop & Engineering > Workshop Job Cards & Projects** | `action_nfd_workshop_job_cards` | Workshop task register tracking Job Card number (JC-1009 etc.), hours/days, truck asset, trailer registration, check-in km, and spare parts procurement status. |
| `Copy of Vehicle Info New.xlsx` | `BREAKDOWN` | `A3:E20` | **Workshop & Engineering > 24/7 Breakdown & Corridors** | `action_nfd_breakdown_corridors` | 33 vetted breakdown repair, towing, auto-electrical, and tyre service vendors positioned across 14 major Namibian transport corridors for emergency roadside response. |
| `Copy of Vehicle Info New.xlsx` | `DRIVER INFORMATION` | `A3:K45` | **Personnel & Compliance > Hazchem Drivers & Licensing** | `action_nfd_driver_compliance` | Statutory compliance register for 34 drivers: National ID Number, Start Date, Driving Licence Code (CE, C), PrDP expiry, Hazchem Dangerous Goods permit expiry, and trainee stipend payment cycle. |

---

## 2. Step-by-Step Navigation Guide

### Menu 1: Executive Dashboards

#### Step 1.1: NFD Executive Command Center
- **Where to click:** Top navbar > **Executive Dashboards** > **NFD Executive Command Center**
- **What this page displays:** High-level executive overview in Kanban view showing refuel logs, vehicle units, driver assignments, distance traveled, and colored anomaly badges:
  - Red Badge (`Odo Anomaly`): Highlights odometer discrepancies or missing logsheet data.
  - Yellow Badge (`Excess Burn`): Highlights trips where fuel burned exceeded expected benchmark by >25 Liters.
  - Green Badge (`Normal`): Trips meeting or beating benchmark fuel economy.
- **Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet -> cells `B5:I45`.

#### Step 1.2: Fuel & Otj COC Variance
- **Where to click:** Top navbar > **Executive Dashboards** > **Fuel & Otj COC Variance**
- **What this page displays:** Bar graph and pivot table analyzing excess fuel consumption and monetary financial impact.
  - Evaluates excess liters against Otjiwarongo Commercial Operations Cost benchmark price: **NAD 25.98 / L**.
  - Highlights top excess fuel burners (+4,722.91 L / +NAD 122,701.18) and top star savers (-1,851.52 L / -NAD 48,102.49).
- **Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet -> cells `C3:E3` and columns `G:I`.

#### Step 1.3: Driver & Refueling Site Analytics
- **Where to click:** Top navbar > **Executive Dashboards** > **Driver & Refueling Site Analytics**
- **What this page displays:** Horizontal bar chart and pivot breakdown displaying total liters drawn across 13 refueling stations and depot corridors:
  - Otjiwarongo Main Depot, Walvis Bay Port, Agra Vivo, CJ Steenkamp, Ndama, Tokat, Veronika, Weimans, etc.
- **Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> Individual vehicle tabs -> column `F` (Place).

#### Step 1.4: Fleet Readiness & Service Radar
- **Where to click:** Top navbar > **Executive Dashboards** > **Fleet Readiness & Service Radar**
- **What this page displays:** Stacked bar chart and pivot matrix tracking fleet operational availability across 7 availability groups:
  - Tankers (88% target availability), Rigid Trucks (77% target availability), Standby Trucks (50%), In Maintenance (100%), Installations (60%), For Sale (100%), Pool (100%).
  - Tracks compliance against NFD fleet age governance policy: Prime Movers < 18 years, Tankers/Trailers < 15 years.
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `AVAILABILITY` sheet -> cells `A2:G35`.

#### Step 1.5: Workshop, Alignment & Timesheets
- **Where to click:** Top navbar > **Executive Dashboards** > **Workshop, Alignment & Timesheets**
- **What this page displays:** Bar chart and matrix analyzing workshop maintenance requests grouped by assigned lead mechanic (Green, Japie, Clive) and job card category (Full Service, Wheel Alignment, Manifold Repair, Tank Degassing, SLP Recertification).
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet -> cells `A3:I35`.

---

### Menu 2: Fuel Operations

#### Step 2.1: Fuel Consumption Summary
- **Where to click:** Top navbar > **Fuel Operations** > **Fuel Consumption Summary**
- **What this page displays:** The master rollup list of all 41 fleet vehicles:
  - Registration / Vehicle Plate
  - Expected Benchmark KM/L
  - Actual Achieved KM/L
  - Distance Traveled (285,640.0 km fleet total)
  - Actual Fuel Liters Drawn (100,269.50 L fleet total)
  - Excess Fuel Liters (+2,871.39 L net variance)
  - Financial Impact Value (+NAD 74,598.69 net impact)
- **Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> `Summary` sheet -> cells `B5:I45`.

#### Step 2.2: Vehicle Refuel Logsheets
- **Where to click:** Top navbar > **Fuel Operations** > **Vehicle Refuel Logsheets**
- **What this page displays:** Detailed list of all 326 individual driver refuel slips:
  - Refuel Slip Number (e.g. `FCL/2026/0001` to `FCL/2026/0326`)
  - Date of refueling
  - Vehicle Plate
  - Certified Hazchem Driver
  - Refueling Place / Facility
  - Start Odometer and End Odometer
  - Liters dispensed
  - Calculated KM/L efficiency
  - Audit Status (Normal, Excess Burn, Odometer Anomaly)
  - Unconfirmed Logsheet indicator (`X`)
- **Excel Reference:** `Copy of Fuel Consumption 09 2026.xlsx` -> Individual vehicle tabs -> cells `B10:N24`.

#### Step 2.3: Cargo Fuel Dispatches & Loss
- **Where to click:** Top navbar > **Fuel Operations** > **Cargo Fuel Dispatches & Loss**
- **What this page displays:** Outbound bulk fuel delivery dispatches from Otjiwarongo depot to external client sites (Husab Mine, B2Gold, Petrosol Outjo).
  - Flags bulk delivery discrepancies and in-transit leakage alerts (e.g. 210 L manifold spill alert on delivery DISP/2026/0102).
  - Automatically provisions maintenance inspection tickets.

---

### Menu 3: Fleet & Assets

#### Step 3.1: Fleet Service Schedule
- **Where to click:** Top navbar > **Fleet & Assets** > **Fleet Service Schedule**
- **What this page displays:** Vehicle maintenance odometer tracking:
  - Routine Service Interval (15,000 km, 30,000 km, 50,000 km)
  - Last Service Odometer
  - Next Service Milestone
  - KM Remaining Until Service Due (color-coded: Green = OK, Yellow = Due Soon, Red = Overdue)
  - NaTIS Vehicle Licence Disk Expiry
  - NaTIS Roadworthy Fitness Certificate Expiry
  - Safe Loading Pass (SLP) Expiry for gantry bottom-loading
  - Statutory 2.5/5-year Hydrostatic Tanker Pressure Test Expiry
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `FLEET SERVICE` sheet -> cells `A5:L45`.

#### Step 3.2: Fleet Availability & Grouping
- **Where to click:** Top navbar > **Fleet & Assets** > **Fleet Availability & Grouping**
- **What this page displays:** List of all 94 fleet units categorized into the 7 operational availability groups:
  - Rigid Trucks (44% to 77%)
  - Tankers (88% target)
  - Standby Trucks (50%)
  - In Maintenance (100%)
  - Installations (60%)
  - Decommissioned / For Sale (100%)
  - Pool (100%)
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `AVAILABILITY` sheet -> cells `A2:G35`.

#### Step 3.3: Driver & Trailer Allocation
- **Where to click:** Top navbar > **Fleet & Assets** > **Driver & Trailer Allocation**
- **What this page displays:** Current fleet operational roster:
  - Prime Mover Tractor Unit
  - Permanent Lead Driver
  - Trainee Co-Driver (e.g. Tobias Leopold, Nounongoue Kaaronda)
  - Coupled B-Double Semi-Trailer and Pup Trailer registrations
  - Dedicated Route / Standby Notes
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `DRIVER ALLOCATION` sheet -> cells `A3:F40`.

#### Step 3.4: Corporate Livery & Branding
- **Where to click:** Top navbar > **Fleet & Assets** > **Corporate Livery & Branding**
- **What this page displays:** Corporate branding audit:
  - Vehicle Plate & Model
  - Branding Status: Fully Branded, Needs GT Vinyl Branding, Unbranded, Decommissioned
  - Branding Location Notes: Tracks remote units stationed at mines or depot
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `BRANDING` sheet -> cells `A3:D45`.

#### Step 3.5: PTO & Hydraulic Systems
- **Where to click:** Top navbar > **Fleet & Assets** > **PTO & Hydraulic Systems**
- **What this page displays:** Offloading discharge mechanism audit:
  - Auxiliary Engine PTO fitted (Yes/No)
  - Transmission Hydraulic PTO fitted (Yes/No)
  - Discharge Type: Auxiliary Engine PTO, Hydraulic PTO, Dual PTO, Gravity Discharge
  - PTO Mounting Position: Behind Cab, On Cab next to COC Tank, Tanker Chassis
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `PTO` sheet -> cells `A3:F30`.

#### Step 3.6: Wheel Alignment & Chassis Audit
- **Where to click:** Top navbar > **Fleet & Assets** > **Wheel Alignment & Chassis Audit**
- **What this page displays:** Laser axle and chassis diagnostic audit:
  - Vehicle Plate
  - Diagnostic checkboxes: Skip, In, Faults, Repaired, Done
  - Chassis Fault Details: Red highlighted rows identify trucks with severe unresolved alignment faults directly linked to tyre drag and excess fuel burn:
    - **Truck 2455 (N 2455 OT):** Steering axle toe-out 4.2mm, severe inner shoulder tyre wear
    - **Truck 11028 (N 11028 OT):** Drive axle thrust angle deviation 0.38 deg, crab-walking tyre scrub
    - **Truck 4584 (N 4584 OT):** Tri-axle trailer axle 2 misaligned 6.1mm, severe drag
    - **Truck 11963 (N 11963 OT):** Front kingpin play, camber -1.2 deg
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `Wheel Allignment Worksheet` -> cells `A3:J45` (Fault rows 33–36).

---

### Menu 4: Workshop & Engineering

#### Step 4.1: Workshop Job Cards & Projects
- **Where to click:** Top navbar > **Workshop & Engineering** > **Workshop Job Cards & Projects**
- **What this page displays:** Workshop maintenance requests and job cards:
  - Job Card Number (e.g. `JC-1009`, `JC-1012`, `JC-1045`)
  - Description of work required
  - Hours / Days estimated
  - Asset / Vehicle Plate
  - Trailer Registration
  - Kms Left at Check-In
  - Lead Mechanic Assigned (Green, Japie, Clive)
  - Spare Parts Supplier (Scania Windhoek, Mercedes Otjiwarongo, Auto Electric Otjiwarongo)
  - Parts Ordered and Parts Received toggle switches
  - Stage: New Request, In Progress, Awaiting Spare Parts, Repaired & Done
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `PROJECTS` sheet -> cells `A3:I35`.

#### Step 4.2: 24/7 Breakdown & Corridors
- **Where to click:** Top navbar > **Workshop & Engineering** > **24/7 Breakdown & Corridors**
- **What this page displays:** Emergency roadside support directory:
  - 33 certified vendor partners across 14 Namibian transport corridors (B1 North, B1 South, B2 Coastal Corridor, Trans-Kalahari Corridor, B8 Zambezi Corridor).
  - Service capabilities: Heavy Mechanical Repairs, Auto Electrical & Diagnostic, Heavy Recovery & Towing, Commercial Tyres & Mobile Alignment.
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `BREAKDOWN` sheet -> cells `A3:E20`.

#### Step 4.3: Workshop Equipment & Pumps
- **Where to click:** Top navbar > **Workshop & Engineering** > **Workshop Equipment & Pumps**
- **What this page displays:** Physical equipment assets:
  - Otjiwarongo Depot bottom-loading LC Master Flow Meters
  - Gantry offloading pumps and standby generators
  - Petrosol retail station Wayne Helix dispensers and submersible turbine pumps (STPs)

#### Step 4.4: Mechanic Labor Timesheets
- **Where to click:** Top navbar > **Workshop & Engineering** > **Mechanic Labor Timesheets**
- **What this page displays:** Real-time labor hours logged by mechanics against specific vehicle job cards and forecourt maintenance tasks.

---

### Menu 5: Personnel & Compliance

#### Step 5.1: Hazchem Drivers & Licensing
- **Where to click:** Top navbar > **Personnel & Compliance** > **Hazchem Drivers & Licensing**
- **What this page displays:** Statutory human resources and safety compliance register for 34 drivers:
  - Driver Name
  - Namibian National ID Number
  - Driver Commencement Date
  - Driver Licence Code (CE heavy articulated, C heavy rigid)
  - Professional Driving Permit (PrDP) Expiry Date
  - Dangerous Goods / Hazchem Certification Expiry Date
  - Annual Optometric Eye Screening Expiry Date
  - Affirmative Action Category (Designated Namibian Group, Women in Transport)
  - Trainee Payment Cycle (e.g. "Every Monday")
- **Excel Reference:** `Copy of Vehicle Info New.xlsx` -> `DRIVER INFORMATION` sheet -> cells `A3:K45`.

---

### Menu 6: Depot Inventory

#### Step 6.1: Bulk Fuel & Lubricant Stock
- **Where to click:** Top navbar > **Depot Inventory** > **Bulk Fuel & Lubricant Stock**
- **What this page displays:** Real-time physical inventory levels at Otjiwarongo 700kL tank farm:
  - Diesel 50ppm (Tanks 1 to 4: 450,000 L capacity)
  - Unleaded Petrol ULP 95 (Tanks 5 to 6: 250,000 L capacity)
  - Drummed heavy commercial engine oils and transmission fluids (15W-40, 85W-140)

#### Step 6.2: Retail Forecourts & Subsidies
- **Where to click:** Top navbar > **Depot Inventory** > **Retail Forecourts & Subsidies**
- **What this page displays:** NFD's free preventive forecourt maintenance agreements with Petrosol branded retail service stations (Outjo, Khorixas, Otjiwarongo, Katima Mulilo).

---

## 3. Live Demonstration: Cross-App Automation in Action

Follow these 4 simple steps during a live client demonstration to show how Odoo automatically eliminates repetitive manual entry and connects Fleet, Fuel, Workshop, and Driver compliance:

### Step 1: Open Vehicle Form
1. Click **Fleet & Assets** > **Fleet Service Schedule**.
2. Click on vehicle **`N 10420 OT`** (Mercedes Actros 2645).
3. Note its current odometer (e.g. `0.0 km`) and next service milestone (`150,000.0 km`). Service status shows **`Service OK`**.

### Step 2: Log a Driver Refueling Slip
1. Click **Fuel Operations** > **Vehicle Refuel Logsheets**.
2. Click the **New** button in the top left.
3. Fill in:
   - **Log Reference:** `FCL/2026/0401`
   - **Vehicle:** Select `N 10420 OT`
   - **Driver:** Select `Abner Ikondela`
   - **Place:** `Otjiwarongo Depot`
   - **Start Odometer:** `150,000.0`
   - **End Odometer:** `152,000.0`
   - **Fuel Liters:** `650.0`
4. Click the cloud icon (Save).

### Step 3: Observe Automated Cross-App Triggers
1. Navigate back to **Fleet & Assets** > **Fleet Service Schedule** and open **`N 10420 OT`**.
2. **Result 1:** The vehicle odometer automatically advanced to **`152,000.0 km`** without any manual odometer entry!
3. **Result 2:** `KM Until Service Due` immediately recalculated to **`-2,000.0 km`**.
4. **Result 3:** `Service Status` badge automatically flipped to red: **`Service Overdue`**.
5. **Result 4:** The **Job Cards** smart button at the top of the vehicle form incremented to `1`.

### Step 4: Verify Automated Workshop Ticket
1. Click on the **Job Cards** smart button on the vehicle form (or navigate to **Workshop & Engineering** > **Workshop Job Cards & Projects**).
2. **Result:** An automated job card has been generated:
   - **Job Card Number:** `JC-AUTO-49`
   - **Description:** `[AUTOMATED] Routine Service Milestone Overdue - Mercedes-Benz/Actros 2645 6x4/N 10420 OT`
   - **Assigned Mechanic:** `Green` (Workshop Lead Mechanic)
   - **Workshop Location:** `Otjiwarongo Mechanical Workshop`
   - **Priority:** High (`3`)

This proves the end-to-end value of Odoo ERP: a single refueling slip entered by a driver or fuel clerk automatically drives odometer tracking, safety compliance, and workshop service scheduling across the entire company.
