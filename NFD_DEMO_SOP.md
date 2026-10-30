# Standard Operating Procedure (SOP) & Guided Client Demonstration Script
## Client: Northern Fuel Distributors CC (NFD) & Petrosol Petroleum Solutions CC
**Head Office & Depot:** Otjiwarongo, Namibia  
**Key Client Stakeholders:** Johan Botes (Managing Member / GM) & Pierre Fourie (Financial Manager)  
**Presented by:** OreSolve Technical Architecture & Functional Consulting Team  
**System Platform:** Odoo 19 Enterprise (Custom Module: `nfd_petrosol_demo`)  
**Target Operations:** Bulk Fuel Logistics (>4,000,000 L/Month), Fleet Governance, In-House Workshop, HESMS Compliance & Forecourt Asset Care

---

## 1. Executive Summary & Demo Objectives

Northern Fuel Distributors CC (NFD) and their retail subsidiary brand Petrosol Petroleum Solutions CC represent one of the most operationally demanding petroleum distribution businesses in Namibia. With a 700,000-liter bulk storage depot and an in-house mechanical workshop in Otjiwarongo, NFD distributes over 4 million liters of fuel per month across Namibia to tier-1 mining operators (Husab Mine, B2Gold Otjikoto), national infrastructure projects (Grinaker-LTA, Raubex), commercial farms, and Petrosol forecourts.

### Core Demonstration Goals
1. **Volumetric Fuel Reconciliation & Shrinkage Control:** Prove how Odoo 19 bridges gantry loading meters, onboard calibrated truck flow meters, customer tank dips, and statutory 0.25% thermal variance allowances, instantly alerting on unexplainable discrepancies (>50 L).
2. **Autonomous Incident Remediation:** Show how a single click on a Leakage Alert immediately isolates inventory write-offs for finance (Pierre Fourie) and dispatches an emergency corrective work order to the Otjiwarongo mechanical workshop (Johan Botes).
3. **Fleet Governance & Life-Cycle Enforcement:** Demonstrate automated enforcement of NFD's strict fleet replacement policies (Prime Movers < 18 years, Tankers < 15 years) with Geotab OBC telematics integration.
4. **HESMS & Affirmative Action (AA) Compliance:** Demonstrate real-time driver tracking for Dangerous Goods Hazchem permits, Defensive Driving, and Annual Medical Fitness certificates to maintain NFD's >90% Chevron audit score.
5. **Retail & Customer Asset Maintenance:** Highlight free forecourt maintenance management for Petrosol CODO/DODO retail stations and calibration of customer on-site bulk tanks (Husab Mine).

---

## 2. Complete Local Environment Setup & Replication Guide (For Colleagues)

Follow these exact steps to clone, spin up, initialize, and run the NFD & Petrosol demo environment from scratch on any workstation with Docker installed.

### 2.1 Prerequisites
Ensure the host machine has:
- **Git** (`git --version`)
- **Docker & Docker Compose** (`docker --version`, `docker compose version`)

### 2.2 Clone the Repository
```bash
git clone https://github.com/michaelnyirenda/NFDNAM.git
cd NFDNAM
```

### 2.3 Spin Up Docker Containers
The repository contains a pre-configured [`docker-compose.yml`](file:///home/mikedotmp3/dev/projects/NFDNAM/docker-compose.yml) linking PostgreSQL 16 (`nfd-db`) and Odoo 19 (`nfd-odoo19`) with the custom addon mounted into `/mnt/extra-addons`:

```bash
# Start PostgreSQL 16 and Odoo 19 in background
docker compose up -d

# Verify both containers are up and healthy
docker compose ps
```

> **Handling Name Conflicts with Existing Odoo/Postgres Containers:**
> If you already have existing containers using generic names (like `odoo-db` or `odoo19`) or port 8069:
> - **Option A (Use your existing Odoo 19 setup):** If you already run an Odoo 19 instance, you do not need docker compose. Simply copy the addon into your container:
>   ```bash
>   docker cp ./nfd_petrosol_demo odoo19:/mnt/extra-addons/
>   ```
> - **Option B (Clean up old stopped containers):** If the conflict is from an old stopped test container, remove it:
>   ```bash
>   docker rm -f odoo-db odoo19
>   docker compose up -d
>   ```

### 2.4 Initialize Database & Install Addon
Run the following commands to provision the `nfd_demo` database, install standard dependencies, and install the `nfd_petrosol_demo` module with all seed data:

```bash
# 1. Create the dedicated demo database in Postgres
docker exec nfd-db psql -U odoo -d postgres -c "CREATE DATABASE nfd_demo OWNER odoo;"

# 2. Install base system and core dependency modules
docker exec nfd-odoo19 odoo -d nfd_demo --db_host=nfd-db --db_user=odoo --db_password=odoo_secure_db_pass -i base,fleet,maintenance,stock,hr,hr_skills,purchase,sale_management,account,project --stop-after-init

# 3. Install the NFD & Petrosol Demo Module and seed records
docker exec nfd-odoo19 odoo -d nfd_demo --db_host=nfd-db --db_user=odoo --db_password=odoo_secure_db_pass -i nfd_petrosol_demo --stop-after-init
```
*(Note: Explicitly passing `--db_host=nfd-db --db_user=odoo --db_password=odoo_secure_db_pass` ensures the CLI connects to the database container over TCP port 5432 instead of defaulting to a local UNIX domain socket. If you are using your own existing containers, replace `nfd-db` and `nfd-odoo19` with your container names, e.g. `odoo-db` and `odoo19`.)*

### 2.5 Accessing Odoo & Logins
Once initialized, the Odoo server is accessible at:
- **URL:** [http://localhost:8069](http://localhost:8069)
- **Database:** Select `nfd_demo` (if prompted, or via `http://localhost:8069/web/database/selector`)
- **Default Master / Admin Credentials:**
  - **Email / Username:** `admin`
  - **Password:** `admin` (or configured password)

---

## 3. Pre-Demo Environment Verification Checklist

Execute these verification steps 30 minutes before joining the demonstration session with Johan Botes and Pierre Fourie.

### 3.1 Container & Database Health Check
Ensure Docker containers are running and responsive:

```bash
# 1. Verify container status
docker ps --filter "name=nfd" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 2. Confirm database connectivity
docker exec nfd-db psql -U odoo -d nfd_demo -c "SELECT count(*) FROM ir_module_module WHERE name = 'nfd_petrosol_demo' AND state = 'installed';"
# Expected output: 1
```

### 3.2 Addon Hot-Reload / Upgrade Verification
If any adjustments were made to views or Python models, sync and re-initialize the addon:

```bash
# 1. Sync repository files to Odoo extra-addons mount
docker cp ./nfd_petrosol_demo nfd-odoo19:/mnt/extra-addons/

# 2. Upgrade the module in the demo database
docker exec nfd-odoo19 odoo -d nfd_demo --db_host=nfd-db --db_user=odoo --db_password=odoo_secure_db_pass -u nfd_petrosol_demo --stop-after-init

# 3. Restart Odoo server process (or ensure background daemon is active)
# Accessible at: http://localhost:8069 (Select Database: nfd_demo)
```

### 3.3 Automated Sanity Smoke Test
Run the pre-flight verification script inside the Odoo Python shell:

```bash
docker exec nfd-odoo19 python3 -c "
import odoo
from odoo.modules.registry import Registry

registry = Registry('nfd_demo')
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    # 1. Check Depot Stock
    d_stock = env['stock.quant']._get_available_quantity(
        env.ref('nfd_petrosol_demo.product_diesel_50ppm'),
        env.ref('nfd_petrosol_demo.location_tank_1_diesel')
    )
    assert d_stock == 485000.0, f'Expected 485,000L diesel, found {d_stock}'
    
    # 2. Check Fleet Policy Warnings
    argosy = env.ref('nfd_petrosol_demo.vehicle_argosy')
    assert argosy.x_replacement_policy_status == 'warning', 'Argosy should be in warning state'
    
    # 3. Check Leakage Alert Record
    alert_disp = env.ref('nfd_petrosol_demo.dispatch_log_002')
    assert alert_disp.leakage_status == 'leakage_alert', 'DISP/2026/0102 must be leakage_alert'
    assert alert_disp.net_variance_liters == 210.0, 'DISP/2026/0102 variance must be 210L'
    
    print('>>> ALL PRE-DEMO SMOKE TESTS PASSED SUCCESSFULLY! <<<')
"
```

### 3.4 Presenter Setup & Screen Pre-requisites
- **Browser Window 1:** Chrome logged into Odoo as `Administrator` (or `Johan Botes` persona).
- **Default Database:** `nfd_demo`.
- **Zoom/Meet Window:** Shared at 1080p, display scaled to 110% for crisp projector/remote viewing.
- **Bookmarks Bar:** Direct links to:
  - NFD Fuel Logistics Dashboard: `http://localhost:8069/odoo/action-nfd_petrosol_demo.action_nfd_fuel_dispatch_log`
  - Fleet Vehicles: `http://localhost:8069/odoo/action-fleet.fleet_vehicle_action`
  - Maintenance Equipment: `http://localhost:8069/odoo/action-maintenance.hr_equipment_action`

---

## 4. 25-Minute Guided Live Demonstration Script

### Timeline & Persona Agenda
| Elapsed Time | Target Stakeholder | Demonstration Focus Area | Key Impact Metric |
| :--- | :--- | :--- | :--- |
| **00:00 - 03:00** | Johan & Pierre | Executive Welcome & Operational Architecture | 700kL Otjiwarongo Depot & 4M+ L/mo scale |
| **03:00 - 08:30** | Johan Botes | Fleet Governance, Replacement Limits & Geotab | Aging Prime Movers (17y) & Rigid Tankers (14y) |
| **08:30 - 15:30** | Johan & Pierre | Bulk Cargo Dispatch, Thermal Variances & Leakage | The 210L Grinaker-LTA Loss & 1-Click Action |
| **15:30 - 20:30** | Pierre Fourie | Financial Reconciliations, Scrap Valuation & Forecourts | Shrinkage Write-off & Free Forecourt Care |
| **20:30 - 23:30** | Johan Botes | HESMS Driver Safety & Affirmative Action (AA) | Chevron >90% Audit Score & Hazchem Expiry |
| **23:30 - 25:00** | Johan & Pierre | Summary, Roadmap & Commercial Alignment | Next Steps for Pilot Go-Live |

---

### Act 1: Executive Welcome & Operational Context (00:00 – 03:00)
**Presenter Click Path:**
1. Open browser to Odoo home dashboard.
2. Highlight the custom application icon: **NFD Fuel Logistics**.

**Presenter Talking Points:**
> *"Goeie dag Johan, goeie dag Pierre. Thank you for welcoming OreSolve today. We understand that Northern Fuel Distributors isn't just another transport company—you are the economic lifeline powering mining giants like Husab and B2Gold Otjikoto, national infrastructure for Grinaker-LTA, and your own flagship Petrosol retail forecourts from Otjiwarongo.*
>
> *Moving over 4 million liters of bulk fuel every month across thousands of kilometers of Namibian highways leaves zero room for guesswork. A 0.5% unexplained discrepancy on 4 million liters is 20,000 liters—nearly half a million Namibian Dollars lost straight off your bottom line every single month.*
>
> *Today, we demonstrate how Odoo 19 gives Johan the operational visibility to keep every prime mover, tanker manifold, and hazchem driver compliant, while giving Pierre the uncompromising financial and inventory controls to eliminate unaccounted fuel shrinkage."*

---

### Act 2: Johan Botes Flow — Fleet Governance, Replacement Policy & Geotab Telematics (03:00 – 08:30)

**Presenter Click Path:**
1. Navigate to: **NFD Fuel Logistics > Fleet & Assets > Tankers & Rigids** (or **Fleet App**).
2. The list view displays NFD's fleet vehicles with custom badges.
3. Group By: **Fleet Replacement Status** or filter by **Replacement Due / Warning**.
4. Open record: **Freightliner Argosy Prime Mover (N 1809 OT)**.
5. Navigate to tab: **NFD Fuel Fleet & Policy Specs**.
6. Return to list and open: **Mercedes-Benz Axor 17,500L Rigid Tanker (N 1750 OT)**.

**Key Visual Elements on Screen:**
- **Unit Classification:** Selection showing Prime Mover, Semi-Trailer, Rigid Tanker, Pup Trailer.
- **Replacement Policy Badges:**
  - `Scania R500 (N 4201 OT)`: Green badge `Compliant` (Age: 5 yrs).
  - `Mercedes-Benz Actros 2645 (N 4202 OT)`: Green badge `Compliant` (Age: 7 yrs).
  - `Freightliner Argosy (N 1809 OT)`: Amber badge `Warning (Near Policy Limit)` (Age: 17 yrs / Limit: 18 yrs).
  - `Scania P360 Rigid (N 1601 OT)`: Amber badge `Warning (Near Policy Limit)` (Age: 14 yrs / Limit: 15 yrs).
- **Calibrated Diesel Meter Toggle:** Active on the rigid tankers used for construction and farm deliveries.
- **Geotab Unit ID:** Live hardware serial tracking (`GT-NFD-01` to `GT-NFD-15`).

**Presenter Talking Points (Speaking to Johan Botes):**
> *"Johan, let's start with your fleet. NFD operates a diverse mix: 42,000L 7-compartment tri-axles for high-volume mine runs, down to 17,500L and 16,000L rigids fitted with certified flow meters for construction sites.*
>
> *You have a strict company governance rule: Prime Movers must not exceed 18 years, and Tankers must not exceed 15 years. In standard ERPs, fleet managers rely on spreadsheets that are only reviewed once a year when vehicle licenses expire.*
>
> *Notice what Odoo 19 is doing right here. Look at `Freightliner Argosy (N 1809 OT)`. Manufactured in 2009, its calculated age is 17 years. The system has automatically elevated its status to an amber `Warning` because it is within 12 months of your 18-year cap. Look at the `Scania P360 (N 1601 OT)` 16,000L rigid—manufactured in 2012, age 14 years, also flagged as `Warning` against your 15-year tanker threshold.*
>
> *This gives your Otjiwarongo management committee automated capital replacement forecasting well before a vehicle becomes an HSE reliability liability or fails a Chevron transport audit."*

---

### Act 3: The Climax — Bulk Cargo Fuel Dispatch, Meter vs. Dip & The 210L Leakage Incident (08:30 – 15:30)

**Presenter Click Path:**
1. Navigate to: **NFD Fuel Logistics > Cargo Dispatch & Dip Logs > Fuel Dispatch & Variance Logs**.
2. Notice the list view with columns: `Depot Loaded (L)`, `Truck Meter Delivered (L)`, `Thermal Allowance (L)`, `Net Discrepancy (L)`, and color-coded status badges.
3. First, click on record: **`DISP/2026/0101`** (Normal Delivery to B2Gold Otjikoto Mine).
   - Point out: 42,000 L loaded, 41,895 L delivered.
   - Point out the automatically computed **0.25% Thermal Allowance (105.00 L)**.
   - Net variance is `0.00 L` -> Green ribbon `RECONCILED`, Status badge `Normal Reconciliation`.
4. Go back to list and open: **`DISP/2026/0102`** (Incident Delivery to Grinaker-LTA Road Project).
   - Point out the bold red banner: `LEAKAGE ALERT!`.
   - Loaded at Otjiwarongo Gantry: 17,500 L.
   - Truck Digital Flow Meter Reading: 17,246.25 L.
   - Thermal Allowance (0.25%): 43.75 L.
   - **Net Discrepancy: 210.00 Liters!** (Exceeds the 50L safety threshold).
5. Click the red button in the header: **"Log Corrective Workshop Ticket & Shrinkage Scrap"**.
6. The screen automatically generates and transitions to the new **Corrective Maintenance Ticket** in the Otjiwarongo Workshop and creates an inventory shrinkage entry.

**Presenter Talking Points (Speaking to Johan & Pierre):**
> *"Now let's examine NFD's core daily heartbeat: Cargo Fuel Dispatch and Reconciliation. In Namibia, temperatures between Otjiwarongo, Otavi, and the Namib Desert fluctuate drastically. Fuel expands and contracts. If you don't calculate volumetric thermal compensation, your drivers and customers will constantly dispute discrepancies.*
>
> *Look at `DISP/2026/0101` to B2Gold Otjikoto Mine. The tanker loaded 42,000 liters at your Otjiwarongo gantry. On site, the calibrated meter delivered 41,895 liters. The system automatically calculated your standard 0.25% thermal allowance—105 liters. The delivery reconciled to the exact decimal point. Zero discrepancy. Green ribbon.*
>
> *Now, look at `DISP/2026/0102`. Rigid tanker `N 1750 OT` loaded 17,500 liters of 50ppm diesel for the Grinaker-LTA road construction camp. The truck's digital meter recorded 17,246.25 liters delivered. After factoring in the 43.75-liter thermal variance, there is an unexplained discrepancy of **210.00 liters**!*
>
> *Because that exceeds NFD's 50-liter tolerance limit, Odoo immediately triggered a red `LEAKAGE ALERT`. Look at what Johan can do right now with one click—I press 'Log Corrective Workshop Ticket & Shrinkage Scrap'.*
>
> *Instantly, two critical things happen simultaneously: First, the Otjiwarongo workshop receives a Priority-3 Emergency Work Order: 'Inspect Tanker Manifold/Delivery Meter for Fuel Leakage'. Second, Pierre's finance ledger immediately isolates the 210 liters into the virtual Fuel Shrinkage / Leakage Write-Off account so your trading margins remain 100% accurate."*

---

### Act 4: Pierre Fourie Flow — Financial Reconciliation, Inventory Shrinkage & Forecourt Assets (15:30 – 20:30)

**Presenter Click Path:**
1. Navigate to: **NFD Fuel Logistics > Depot Stock & Losses > Fuel Shrinkage & Scraps** (Stock Scrap).
2. Point out the recorded scrap entries: Product `Diesel 50ppm Bulk`, Quantity: `210.00 L`, Scrap Location: `Fuel Shrinkage / Leakage Write-Off`.
3. Navigate to: **NFD Fuel Logistics > Depot Stock & Losses > Fuel & Lubricant Inventory**.
4. Open: **Diesel 50ppm Bulk** -> click on **On Hand Quantity**:
   - Location `OTJ/Stock/Bulk Fuel Tank Farm/Tank 1 - Diesel 50ppm (500,000L)`: 485,000 L.
   - Location `Tank 2 - ULP 95 (200,000L)`: 165,000 L.
   - Workshop Store: 45 drums 15W-40, 60 buckets Chassis Grease EP2.
5. Navigate to: **NFD Fuel Logistics > Fleet & Assets > Maintenance Work Orders**.
6. Filter by Agreement Type: **Free Forecourt Maintenance Agreement (Petrosol/ILAMO)**.
7. Open: **Monthly Dispenser Nozzle & Meter Recalibration - Petrosol Outjo**.

**Presenter Talking Points (Speaking to Pierre Fourie):**
> *"Pierre, as Financial Manager, this is your control center. In standard operations, volume losses sit in limbo until month-end physical stocktakes, distorting your buying pool reconciliations and fuel gross margins.*
>
> *Here, the moment that 210-liter alert was processed, Odoo logged an inventory scrap write-off directly against your dedicated `Fuel Shrinkage / Leakage Write-Off` virtual location. At current wholesale diesel cost, that's exactly NAD 4,515.00 cleanly recognized and attributed to vehicle `N 1750 OT` on that specific trip.*
>
> *Next, let's look at your Petrosol retail forecourts and ILAMO convenience stores. At Outjo (CODO) and Khorixas (DODO), NFD provides free forecourt equipment maintenance. Look at this work order: 'Monthly Dispenser Nozzle & Meter Recalibration - Petrosol Outjo'.*
>
> *Your workshop technicians log parts used—whether it's seal kits or dispenser filters—and their labor hours under the agreement type `Free Forecourt Maintenance Agreement`. You have complete, transparent visibility into the exact cost of forecourt equipment subsidies per retail station, allowing you to accurately evaluate dealer fuel throughput margins versus forecourt upkeep expenses."*

---

### Act 5: HESMS Safety Compliance & Namibian Affirmative Action (AA) (20:30 – 23:30)

**Presenter Click Path:**
1. Navigate to: **NFD Fuel Logistics > HESMS & Driver Safety > Hazchem Drivers & AA Compliance** (or **HR Employees**).
2. List view displays columns: `Name`, `Job Position`, `Affirmative Action Category`, and `HESMS Safety Status`.
3. Point out driver: **`Hendrik Shilongo`** -> Badge: Green `Fully Compliant`.
4. Point out driver: **`Matheus Shikongo`** -> Badge: Amber `Expiring Within 30 Days`.
5. Open **`Matheus Shikongo`** -> Tab: **HESMS & Affirmative Action**.
   - Show: Dangerous Goods / Hazchem Permit Expiry: **`2026-11-01`** (Expires in 5 days!).
   - Show: Defensive Driving and Medical Fitness are valid until 2027.
   - Point out the automated rule: Because his Hazchem permit is expiring within 30 days, Odoo prevents dispatching him once expired!

**Presenter Talking Points (Speaking to Johan Botes):**
> *"Johan, Chevron audits require a score above 90% to maintain bulk transport accreditation. That requires rigorous proof of driver fitness, dangerous goods hazchem permits, and defensive driving certifications.*
>
> *Notice Matheus Shikongo. His Hazchem permit expires in just 5 days (1 November 2026). The system automatically displays an amber warning badge `Expiring Within 30 Days`. If his permit lapses, the Cargo Fuel Dispatch screen will block him from being assigned to any hazardous tanker dispatch.*
>
> *Furthermore, for your annual compliance reporting under the Namibian Affirmative Action (Employment) Act 29 of 1998, every employee is classified into their designated groups—Designated Namibian Group, Women in Transport, or Persons with Disabilities. Your Affirmative Action compliance report can be generated in seconds with zero manual spreadsheets."*

---

### Act 6: Q&A, Next Steps & Pilot Implementation (23:30 – 25:00)

**Presenter Talking Points:**
> *"Johan, Pierre—to summarize what we have experienced together today:
> 1. Complete transparency over your 700,000L bulk depot inventory and lubricant stocks.
> 2. Automated enforcement of your 18-year Prime Mover and 15-year Tanker replacement rules with Geotab telematics linkage.
> 3. Zero-loss cargo reconciliation with automatic 0.25% thermal adjustments and 1-click corrective maintenance ticketing for unexplainable losses.
> 4. Automated HESMS and Affirmative Action compliance protecting your Chevron accreditation.
>
> OreSolve's proposed next step is a 3-week pilot at the Otjiwarongo Depot, loading live dispatches from Tank 1 and Tank 2, integrating with your Geotab API feed, and running your upcoming month-end fuel shrinkage reconciliation in parallel.
>
> What questions can we answer for you?"*

---

## 5. End-to-End Functional Test Matrix (QA Verification)

| Test ID | Feature / Workflow Area | Test Objective & Pre-conditions | Step-by-Step Test Actions | Expected Results | Verification Command / Screen | Pass / Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Depot Bulk Inventory Setup | Verify 700kL Otjiwarongo Depot bulk tank locations and seed stock. | 1. Navigate to Inventory > Stock On Hand.<br>2. Filter by Location: `Bulk Fuel Tank Farm`. | Tank 1 displays 485,000 L of Diesel 50ppm; Tank 2 displays 165,000 L of ULP 95 Petrol; Workshop Store displays lubricants & spares. | `stock.quant` search on `OTJ/Stock` locations | **PASS** |
| **TC-02** | Fleet Replacement Governance | Verify automated policy status calculation based on unit class and age. | 1. Navigate to Fleet > Vehicles.<br>2. Inspect Freightliner Argosy (2009, 17 yrs).<br>3. Inspect Scania P360 (2012, 14 yrs). | Argosy (Prime Mover) shows `warning` (Limit: 18 yrs). Scania P360 (Tanker) shows `warning` (Limit: 15 yrs). Younger trucks show `compliant`. | `fleet.vehicle` field `x_replacement_policy_status` | **PASS** |
| **TC-03** | Normal Fuel Dispatch Reconciliation | Reconcile standard mine delivery with 0.25% thermal allowance. | 1. Open dispatch `DISP/2026/0101` (B2Gold).<br>2. Inspect loaded (42,000L), delivered (41,895L). | Thermal allowance auto-computes to 105.00 L. Net variance is 0.00 L. Status displays green `Normal Reconciliation` and green ribbon. | `nfd.fuel.dispatch.log` record `DISP/2026/0101` | **PASS** |
| **TC-04** | High-Variance Leakage Alert Trigger | Trigger leakage alert when discrepancy exceeds 50 Liters. | 1. Open dispatch `DISP/2026/0102` (Grinaker-LTA).<br>2. Loaded: 17,500L, Delivered: 17,246.25L. | Thermal allowance is 43.75 L. Net discrepancy is 210.00 L (>50L). Banner displays bold red `LEAKAGE ALERT!`. Status is `leakage_alert`. | `nfd.fuel.dispatch.log` record `DISP/2026/0102` | **PASS** |
| **TC-05** | Automated Workshop & Scrap Action | Validate 1-click generation of corrective ticket and scrap entry. | 1. On `DISP/2026/0102`, click button `action_create_leakage_maintenance_ticket`. | 1. Corrective ticket is created for Otjiwarongo Workshop (Priority 3).<br>2. Stock scrap entry created for 210L.<br>3. State updates to `investigation`. | `maintenance.request` linked to dispatch; `stock.scrap` created | **PASS** |
| **TC-06** | HESMS Driver Safety Permit Tracking | Detect permit expirations within 30-day safety warning window. | 1. Navigate to HR Employees.<br>2. Inspect Hendrik Shilongo.<br>3. Inspect Matheus Shikongo. | Hendrik has valid permits -> `Fully Compliant`. Matheus has Hazchem permit expiring in 5 days -> `Expiring Within 30 Days` amber badge. | `hr.employee` field `x_hse_status_badge` | **PASS** |
| **TC-07** | Affirmative Action (AA) Classification | Ensure compliance with Namibian Affirmative Action Act categories. | 1. Group employees by `Affirmative Action Category`. | Staff categorized into `Designated Namibian Group`, `Women in Transport`, or `General`. | `hr.employee` field `x_aa_category` | **PASS** |
| **TC-08** | Petrosol Forecourt & Bulk Tank Assets | Track maintenance on customer tanks and free forecourt pumps. | 1. Navigate to Maintenance > Equipment.<br>2. Check Wayne Helix pump at Outjo.<br>3. Check 60kL tank at Husab Mine. | Pump linked to Petrosol Outjo (CODO) under `Free Forecourt Agreement`. Husab tank linked to client under `Customer Bulk Installation Contract`. | `maintenance.equipment` fields `x_asset_category`, `x_site_partner_id` | **PASS** |

---

## 6. Post-Demo Follow-Up Checklist for OreSolve Consultants
1. **Send Executive Summary Email** to Johan Botes (`johan@nfdnamibia.com`) and Pierre Fourie (`pierre@nfdnamibia.com`) within 2 hours of the call, recapping the 210L leakage reconciliation and the Otjiwarongo workshop workflow.
2. **Export Seed Data Spreadsheet** containing NFD's 24 fleet units and Geotab identifiers for their review.
3. **Schedule Technical Architecture Discovery** with NFD's IT lead for Geotab OBC API endpoint integration and digital gantry meter protocol compatibility.

