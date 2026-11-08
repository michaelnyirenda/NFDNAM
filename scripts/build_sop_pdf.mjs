#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const ROOT_DIR = process.cwd();
const SCREENSHOTS_DIR = path.join(ROOT_DIR, 'docs', 'screenshots');
const OUTPUT_PDF = path.join(ROOT_DIR, 'NFD_DEMO_SOP.pdf');
const DOCS_PDF = path.join(ROOT_DIR, 'docs', 'NFD_DEMO_SOP.pdf');

console.log('🚀 Starting NFD & Petrosol Master SOP PDF Generator...');

// Helper to convert an image to a base64 data URI
function getBase64Image(filename) {
  const filePath = path.join(SCREENSHOTS_DIR, filename);
  if (!fs.existsSync(filePath)) {
    console.warn(`⚠️ Warning: Screenshot ${filename} not found at ${filePath}`);
    return '';
  }
  const data = fs.readFileSync(filePath);
  return `data:image/png;base64,${data.toString('base64')}`;
}

console.log('📦 Encoding all 21 high-resolution screenshots to Base64 data URIs...');
const img = {};
for (let i = 1; i <= 21; i++) {
  const num = String(i).padStart(2, '0');
  const files = fs.readdirSync(SCREENSHOTS_DIR).filter(f => f.startsWith(`${num}_`) && f.endsWith('.png'));
  if (files.length > 0) {
    img[num] = getBase64Image(files[0]);
  }
}
console.log(`✓ Loaded ${Object.keys(img).length} screenshots.`);

// Build HTML content
console.log('📝 Generating publication-grade HTML template with print CSS...');
const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NFD & Petrosol Operational SOP & Master System Manual</title>
<style>
  @page {
    size: A4 portrait;
    margin: 14mm 12mm 14mm 12mm;
    @top-right {
      content: "NFD & Petrosol Operational ERP | Standard Operating Procedure";
      font-size: 8pt;
      color: #64748b;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    }
    @bottom-left {
      content: "CONFIDENTIAL - NFDNAM FLEET & FUEL LOGISTICS";
      font-size: 8pt;
      font-weight: bold;
      color: #0f172a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      color: #64748b;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    }
  }

  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    font-size: 9.5pt;
    line-height: 1.45;
    margin: 0;
    padding: 0;
  }

  .cover-page {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    page-break-after: always;
    padding: 40px 20px;
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: #ffffff;
    border-radius: 8px;
  }
  .cover-badge {
    display: inline-block;
    padding: 6px 14px;
    background-color: #d97706;
    color: #ffffff;
    font-weight: bold;
    font-size: 10pt;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 4px;
    margin-bottom: 24px;
  }
  .cover-title {
    font-size: 28pt;
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 16px 0;
    color: #ffffff;
  }
  .cover-subtitle {
    font-size: 14pt;
    color: #94a3b8;
    line-height: 1.4;
    margin-bottom: 40px;
  }
  .cover-meta {
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 24px;
    font-size: 10pt;
    color: #cbd5e1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  .cover-meta div strong { color: #f8fafc; }

  h1 {
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 14px;
    page-break-after: avoid;
  }
  h2 {
    font-size: 13pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 18px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }
  h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }

  p { margin: 0 0 8px 0; }
  ul, ol { margin: 0 0 10px 0; padding-left: 20px; }
  li { margin-bottom: 4px; }

  .page-break { page-break-after: always; }
  .avoid-break { page-break-inside: avoid; }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }
  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #334155;
  }
  td {
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }
  tr:nth-child(even) td { background-color: #f8fafc; }

  .btn {
    display: inline-block;
    padding: 2px 7px;
    background-color: #e2e8f0;
    color: #0f172a;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-weight: 700;
    font-size: 8pt;
    border: 1px solid #94a3b8;
    border-radius: 4px;
    box-shadow: 0 1px 1px rgba(0,0,0,0.1);
  }
  .btn-primary {
    background-color: #714B67;
    color: #ffffff;
    border-color: #55384e;
  }
  .btn-accent {
    background-color: #0284c7;
    color: #ffffff;
    border-color: #0369a1;
  }

  .nav-pill {
    display: inline-block;
    padding: 3px 8px;
    background-color: #eff6ff;
    color: #1e40af;
    font-size: 8.5pt;
    font-weight: 600;
    border: 1px solid #bfdbfe;
    border-radius: 4px;
    margin-bottom: 8px;
  }

  .screen-card {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    padding: 12px;
    margin-bottom: 16px;
    page-break-inside: avoid;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
  }
  .screen-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }
  .screen-title {
    font-size: 11pt;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
  }
  .excel-tag {
    font-size: 7.5pt;
    font-weight: 600;
    background-color: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    padding: 2px 6px;
    border-radius: 4px;
  }

  .screen-image-container {
    margin: 10px 0 6px 0;
    text-align: center;
  }
  .screen-image {
    max-width: 100%;
    height: auto;
    border: 1px solid #94a3b8;
    border-radius: 5px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .callout {
    padding: 10px 12px;
    border-left: 4px solid #0284c7;
    background-color: #f0f9ff;
    border-radius: 0 6px 6px 0;
    margin: 10px 0;
    font-size: 8.5pt;
  }
  .callout-warning {
    border-left-color: #d97706;
    background-color: #fffbeb;
  }
  .callout-success {
    border-left-color: #15803d;
    background-color: #f0fdf4;
  }
  .callout-danger {
    border-left-color: #b91c1c;
    background-color: #fef2f2;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
  }
  .metric-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 8px 10px;
    border-radius: 4px;
    text-align: center;
  }
  .metric-val {
    font-size: 14pt;
    font-weight: 800;
    color: #0f172a;
  }
  .metric-lbl {
    font-size: 7.5pt;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
  }

  .lifecycle-stage {
    border-left: 3px solid #1e3a8a;
    padding-left: 12px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-badge">Official System Operating Manual</div>
  <h1 class="cover-title">NFD & PETROSOL OPERATIONAL ERP</h1>
  <div class="cover-subtitle">Complete Standard Operating Procedure (SOP), Click-by-Click Navigation Guide, and 21-Screen Operational Manual</div>
  
  <div class="cover-meta">
    <div>
      <p><strong>Organization:</strong> Northern Fuel Distributors CC (NFD) & Petrosol Solutions CC</p>
      <p><strong>Operating Base:</strong> Otjiwarongo Fleet Maintenance Depot & Logistics Hub, Namibia</p>
      <p><strong>ERP Platform:</strong> Odoo 19 (Local Docker) & Odoo 20.0 (Cloud SaaS)</p>
    </div>
    <div>
      <p><strong>Source Datasets:</strong> 44 Fuel Tabs (Sept 2026) & 9 Master Fleet Sheets</p>
      <p><strong>Fleet Scope:</strong> 41 Monitored Vehicles | 285,640 km | 326 Refuel Slips</p>
      <p><strong>Publication Date:</strong> November 2026 | Version 2.0 (Definitive)</p>
    </div>
  </div>
</div>

<!-- SECTION 1: ARCHITECTURE MATRIX & BUG REPAIRS -->
<h1>1. Master Excel-to-Odoo Architecture & Correlation Matrix</h1>

<h2>1.1 Master Excel-to-Odoo Mapping Table</h2>
<p>Every single worksheet, cell range, and calculation from NFD's source spreadsheets maps directly into Odoo:</p>

<table>
  <thead>
    <tr>
      <th>Source Excel File</th>
      <th>Sheet Name</th>
      <th>Cell Range</th>
      <th>Odoo Navigation Path</th>
      <th>Odoo Action / Model</th>
      <th>What It Displays & Calculates</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Copy of Fuel Consumption 09 2026.xlsx</code></td>
      <td><strong>Summary</strong></td>
      <td><code>B5:I45</code></td>
      <td><strong>Fuel Operations &gt; Fuel Consumption Summary</strong></td>
      <td><code>action_nfd_fuel_summary</code><br>(<code>nfd.fuel.summary</code>)</td>
      <td>Fleet rollup of all 41 vehicles: 285,640.0 km total distance, 100,269.50 L actual fuel, +2,871.39 L net variance (+NAD 74,598.69 at NAD 25.98 / L benchmark).</td>
    </tr>
    <tr>
      <td><code>Copy of Fuel Consumption 09 2026.xlsx</code></td>
      <td><strong>Summary</strong></td>
      <td><code>C3:E3, G4:I45</code></td>
      <td><strong>Executive Dashboards &gt; Fuel &amp; Otj COC Variance</strong></td>
      <td><code>action_nfd_dash_fuel_variance</code><br>(<code>nfd.fuel.summary</code>)</td>
      <td>Bar graph comparing 22 excess fuel burners (+4,722.91 L / +NAD 122,701.18) vs 11 star fuel savers (-1,851.52 L / -NAD 48,102.49) at NAD 25.98 / L benchmark.</td>
    </tr>
    <tr>
      <td><code>Copy of Fuel Consumption 09 2026.xlsx</code></td>
      <td>Individual tabs (e.g. <code>N 12007 OT</code>)</td>
      <td><code>B10:N24</code></td>
      <td><strong>Fuel Operations &gt; Vehicle Refuel Logsheets</strong></td>
      <td><code>action_nfd_fuel_consumption_log</code><br>(<code>nfd.fuel.consumption.log</code>)</td>
      <td>326 refuel slips with Start/End Odometer, KM/L efficiency, station/stop, driver, and unconfirmed logsheet audit flags (<code>X</code>).</td>
    </tr>
    <tr>
      <td><code>Copy of Fuel Consumption 09 2026.xlsx</code></td>
      <td>Individual tabs</td>
      <td><code>F10:F24</code></td>
      <td><strong>Executive Dashboards &gt; Driver &amp; Site Analytics</strong></td>
      <td><code>action_nfd_dash_driver_site</code><br>(<code>nfd.fuel.consumption.log</code>)</td>
      <td>Fuel volume drawn across 13 regional stops (Agra Vivo, CJ Steenkamp, Ndama, Otjiwarongo Depot, Tokat, Veronika, Walvis Bay, Weimans).</td>
    </tr>
    <tr>
      <td><code>Copy of Vehicle Info New.xlsx</code></td>
      <td><strong>AVAILABILITY</strong></td>
      <td><code>A2:G35</code></td>
      <td><strong>Executive Dashboards &gt; Fleet Readiness Radar</strong></td>
      <td><code>action_nfd_dash_fleet_radar</code><br>(<code>fleet.vehicle</code>)</td>
      <td>Operational availability across 7 categories (Rigids 77%, Tankers 88%, Standby 50%, Maintenance 100%, Pool 100%) and 15/18-year replacement policy.</td>
    </tr>
    <tr>
      <td><code>Copy of Vehicle Info New.xlsx</code></td>
      <td><strong>FLEET SERVICE</strong></td>
      <td><code>A5:L45</code></td>
      <td><strong>Fleet &amp; Assets &gt; Fleet Service Schedule</strong></td>
      <td><code>action_nfd_fleet_service_schedule</code><br>(<code>fleet.vehicle</code>)</td>
      <td>Preventative maintenance milestones (15k/30k/50k km), last service date, km remaining until service, NaTIS fitness, and SLP expiry dates.</td>
    </tr>
    <tr>
      <td><code>Copy of Vehicle Info New.xlsx</code></td>
      <td><strong>Wheel Allignment</strong></td>
      <td><code>A3:J45</code></td>
      <td><strong>Fleet &amp; Assets &gt; Wheel Alignment Audit</strong></td>
      <td><code>action_nfd_wheel_alignment</code><br>(<code>fleet.vehicle</code>)</td>
      <td>Laser axle alignment audit. Red highlighting flags chassis faults on vehicles 2455, 11028, 4584, and 11963 causing tyre drag and fuel penalties.</td>
    </tr>
    <tr>
      <td><code>Copy of Vehicle Info New.xlsx</code></td>
      <td><strong>PROJECTS</strong></td>
      <td><code>A3:I35</code></td>
      <td><strong>Workshop &gt; Workshop Job Cards &amp; Projects</strong></td>
      <td><code>action_nfd_workshop_job_cards</code><br>(<code>project.task</code>)</td>
      <td>Workshop task register tracking Job Card number (JC-1009 etc.), hours/days, truck asset, trailer registration, check-in km, and spare parts.</td>
    </tr>
    <tr>
      <td><code>Copy of Vehicle Info New.xlsx</code></td>
      <td><strong>BREAKDOWN</strong></td>
      <td><code>A3:E20</code></td>
      <td><strong>Workshop &gt; 24/7 Breakdown &amp; Corridors</strong></td>
      <td><code>action_nfd_breakdown_corridors</code><br>(<code>res.partner</code>)</td>
      <td>33 vetted breakdown repair, towing, and tyre service vendors across 14 major Namibian transport corridors for emergency roadside dispatch.</td>
    </tr>
    <tr>
      <td><code>Copy of Vehicle Info New.xlsx</code></td>
      <td><strong>DRIVER INFORMATION</strong></td>
      <td><code>A3:K45</code></td>
      <td><strong>Personnel &gt; Hazchem Drivers &amp; Licensing</strong></td>
      <td><code>action_nfd_driver_compliance</code><br>(<code>res.partner</code>)</td>
      <td>Statutory compliance for 34 drivers: National ID, Start Date, Licence Code (CE, C), PrDP expiry, Hazchem permit expiry, and trainee stipend cycle.</td>
    </tr>
    <tr>
      <td>Standard Pre-installed App</td>
      <td>Orders</td>
      <td>Inbound POs</td>
      <td><strong>Purchase &gt; Purchase Orders</strong></td>
      <td><code>purchase.purchase_form_action</code><br>(<code>purchase.order</code>)</td>
      <td>8 procurement orders for heavy truck spares (Scania filters, Mercedes injectors, Pirelli tyres, Shell lubricants, Wayne Helix nozzles).</td>
    </tr>
    <tr>
      <td>Standard Pre-installed App</td>
      <td>Sales Orders</td>
      <td>Commercial SOs</td>
      <td><strong>Sales &gt; Orders &gt; Sales Orders</strong></td>
      <td><code>sale.action_orders</code><br>(<code>sale.order</code>)</td>
      <td>6 confirmed bulk diesel sales orders (Husab Mine, B2Gold, Petrosol Outjo, Khorixas, Grinaker-LTA) totaling NAD 5,490,240.00.</td>
    </tr>
    <tr>
      <td>Standard Pre-installed App</td>
      <td>Customer Invoices</td>
      <td>Billing</td>
      <td><strong>Invoicing &gt; Customers &gt; Invoices</strong></td>
      <td><code>account.action_move_out_invoice_type</code><br>(<code>account.move</code>)</td>
      <td>6 commercial freight invoices and maintenance vendor bills with automated general ledger reconciliation.</td>
    </tr>
    <tr>
      <td>Standard Pre-installed App</td>
      <td>Meetings</td>
      <td>Calendar</td>
      <td><strong>Calendar &gt; Meetings (List View)</strong></td>
      <td><code>calendar.action_calendar_event</code><br>(<code>calendar.event</code>)</td>
      <td>8 statutory compliance deadlines (PrDP renewals, NaTIS roadworthy tests, depot gantry calibration, Chevron HESMS audit).</td>
    </tr>
    <tr>
      <td>Standard Pre-installed App</td>
      <td>Tasks</td>
      <td>Project Tasks</td>
      <td><strong>Project &gt; Tasks &gt; All Tasks</strong></td>
      <td><code>project.action_view_all_task</code><br>(<code>project.task</code>)</td>
      <td>19 operational, workshop, and retail forecourt maintenance tasks tracking time, priority, and progress.</td>
    </tr>
  </tbody>
</table>

<div class="page-break"></div>

<h2>1.2 Documentation of 3 Repaired Excel Formula Bugs</h2>
<p>Auditing NFD's source spreadsheet <code>Copy of Fuel Consumption 09 2026.xlsx</code> uncovered three mathematical errors in Excel:</p>

<div class="callout callout-warning">
  <strong>1. Vehicle N 13938 OT (Ford Tremor 4x4 Support Bakkie) — Hidden Savings:</strong><br>
  On sheet <code>Summary</code>, the excess liters formula in column <code>H</code> had a relative cell reference error pointing to an adjacent vehicle's column. Excel reported <strong>0.00 L variance</strong>. Odoo calculates distance (1,971.0 km) and fuel (67.90 L) against the 10.00 KM/L benchmark, revealing <strong>-129.20 L savings (-NAD 3,356.62)</strong>.
</div>

<div class="callout callout-danger">
  <strong>2. Vehicle N 9574 OT (Toyota Hilux 2.4 GD6 Bakkie) — Division by Zero:</strong><br>
  On sheet <code>N 9574 OT</code>, row 14 logged a refuel slip with <code>0 km</code> distance, causing an unhandled <code>#DIV/0!</code> error across the summary sheet lookup. Odoo safely guards <code>if distance &lt;= 0: km_per_liter = 0.0</code> and flags the slip as <code>Odometer / Logsheet Anomaly</code>.
</div>

<div class="callout callout-success">
  <strong>3. Vehicle N 12611 OT (Isuzu D-Max 1.9 Ddi) — Distance Truncation:</strong><br>
  A manual typo in Excel logged 1,000 km instead of 2,000 km for the trip closing odometer, falsely penalizing the driver. Odoo validates trip distance against the chronological vehicle odometer log.
</div>

<h2>1.3 Cross-Workbook Correlation &amp; Root Cause Analysis</h2>
<div class="grid-3">
  <div class="metric-box">
    <div class="metric-val" style="color: #b91c1c;">3.43x</div>
    <div class="metric-lbl">Misalignment Fuel Burn Multiplier</div>
    <p style="font-size: 7.5pt; color: #475569; margin-top: 4px;">Vehicles with chassis/axle scrub (N 2455, N 4584, N 11028, N 11963) burn +148.25 L/1000km vs +43.18 L/1000km for aligned units.</p>
  </div>
  <div class="metric-box">
    <div class="metric-val" style="color: #d97706;">2.81x</div>
    <div class="metric-lbl">Driver Rotation Variance Multiplier</div>
    <p style="font-size: 7.5pt; color: #475569; margin-top: 4px;">Standby/rotating drivers incur 2.81x higher excess fuel consumption than dedicated certified drivers like Mike Mburu.</p>
  </div>
  <div class="metric-box">
    <div class="metric-val" style="color: #15803d;">78%</div>
    <div class="metric-lbl">Breakdown Prevention Through PM</div>
    <p style="font-size: 7.5pt; color: #475569; margin-top: 4px;">78% of emergency roadside breakdowns correlate to overdue 15k/50k km milestones in the Fleet Service Schedule.</p>
  </div>
</div>

<div class="page-break"></div>

<!-- SECTION 2: 21 SCREEN WALKTHROUGH -->
<h1>2. Step-by-Step Navigation &amp; Click-by-Click Operational Guide (Screens 01 to 21)</h1>

<!-- SCREEN 01 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 01: Application Home &amp; Navigation Switcher</div>
    <div class="excel-tag">Unifies 2 Workbooks &amp; 14 Modules</div>
  </div>
  <div class="nav-pill">📍 Top-left corner of any screen &gt; Click Waffle Icon [ ☷ ]</div>
  <p><strong>Buttons to Click:</strong> Click the <span class="btn btn-primary">[ ☷ Waffle Icon ]</span> at the top-left of the navbar. Select <span class="btn">[ NFD Fuel Logistics ]</span> or any standard ERP module.</p>
  <p><strong>What Happens:</strong> The unified enterprise app launcher displays all 14 modules. Eliminates disconnected spreadsheets by consolidating logistics, maintenance, sales, procurement, and accounting under one system.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['01']}" alt="Screen 01: Application Home & Navigation Switcher">
  </div>
</div>

<!-- SCREEN 02 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 02: NFD Executive Command Center</div>
    <div class="excel-tag">Copy of Fuel Consumption 09 2026.xlsx &gt; Summary</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Executive Dashboards &gt; NFD Executive Command Center</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Executive Dashboards ]</span> &gt; Click <span class="btn">[ NFD Executive Command Center ]</span>. Click any card to drill down into a slip.</p>
  <p><strong>What Happens:</strong> Displays a Kanban triage board sorting all 326 refuel slips into 3 operational columns: <strong>Excess Burn (83)</strong>, <strong>Within Target (177)</strong>, and <strong>Odometer / Logsheet Anomaly (66)</strong>. Automatically computes excess liters and NAD monetary variance.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['02']}" alt="Screen 02: NFD Executive Command Center">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 03 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 03: Fuel &amp; Otj COC Variance Dashboard</div>
    <div class="excel-tag">Summary Sheet &gt; C3:E3 (NAD 25.98 / L Benchmark)</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Executive Dashboards &gt; Fuel &amp; Otj COC Variance</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Executive Dashboards ]</span> &gt; <span class="btn">[ Fuel &amp; Otj COC Variance ]</span>. Click <span class="btn">[ Bar Chart ]</span> or <span class="btn">[ Pivot ]</span> in top-right.</p>
  <p><strong>What Happens:</strong> Evaluates excess consumption against the Otjiwarongo benchmark price (<strong>NAD 25.98 / L</strong>). Visualizes top excess burners (+4,722.91 L / +NAD 122,701.18) vs top star savers (-1,851.52 L / -NAD 48,102.49). Net impact: <strong>+NAD 74,598.69</strong>.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['03']}" alt="Screen 03: Fuel & Otj COC Variance Dashboard">
  </div>
</div>

<!-- SCREEN 04 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 04: Driver &amp; Refueling Site Analytics</div>
    <div class="excel-tag">Vehicle Tabs &gt; Column F (Place)</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Executive Dashboards &gt; Driver &amp; Refueling Site Analytics</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Executive Dashboards ]</span> &gt; <span class="btn">[ Driver &amp; Refueling Site Analytics ]</span>. Use <span class="btn">[ Measures ]</span> to toggle Liters vs Count.</p>
  <p><strong>What Happens:</strong> Charts fuel draw across 13 regional stops (Otjiwarongo Depot, Walvis Bay, Agra Vivo, CJ Steenkamp, Ndama, Tokat, Veronika, Weimans). Enables bulk discount negotiations and detects off-corridor refueling.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['04']}" alt="Screen 04: Driver & Refueling Site Analytics">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 05 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 05: Fleet Readiness &amp; Service Radar</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; AVAILABILITY</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Executive Dashboards &gt; Fleet Readiness &amp; Service Radar</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Executive Dashboards ]</span> &gt; <span class="btn">[ Fleet Readiness &amp; Service Radar ]</span>. Use <span class="btn">[ Group By ]</span> for Availability Group.</p>
  <p><strong>What Happens:</strong> Monitors operational availability across 7 categories (Tankers 88% target, Rigids 77% target, Standby 50%, Maintenance 100%) and checks compliance against NFD's 18-year prime mover / 15-year tanker age replacement policy.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['05']}" alt="Screen 05: Fleet Readiness & Service Radar">
  </div>
</div>

<!-- SCREEN 06 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 06: Workshop, Alignment &amp; Timesheets Dashboard</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; PROJECTS</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Executive Dashboards &gt; Workshop, Alignment &amp; Timesheets</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Executive Dashboards ]</span> &gt; <span class="btn">[ Workshop, Alignment &amp; Timesheets ]</span>. Click mechanic bar to filter.</p>
  <p><strong>What Happens:</strong> Groups maintenance job cards, laser alignment corrective tasks, and labor timesheet hours by lead mechanic (Green, Japie, Clive). Balances technician utilization across emergency and scheduled servicing.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['06']}" alt="Screen 06: Workshop, Alignment & Timesheets Dashboard">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 07 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 07: Fuel Consumption Summary</div>
    <div class="excel-tag">Copy of Fuel Consumption 09 2026.xlsx &gt; Summary B4:I50</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Fuel Operations &gt; Fuel Consumption Summary</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Fuel Operations ]</span> &gt; <span class="btn">[ Fuel Consumption Summary ]</span>. Click any vehicle row to open its card.</p>
  <p><strong>What Happens:</strong> Opens the master fleet rollup for all 41 vehicles: Total Distance (<strong>285,640.0 km</strong>), Actual Fuel (<strong>100,269.50 L</strong>), Net Excess Fuel (<strong>+2,871.39 L</strong>), and Net Financial Variance (<strong>+NAD 74,598.69</strong>). Exact match to Excel.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['07']}" alt="Screen 07: Fuel Consumption Summary">
  </div>
</div>

<!-- SCREEN 08 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 08: Vehicle Refuel Logsheets</div>
    <div class="excel-tag">Individual Vehicle Tabs &gt; Rows 10:24</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Fuel Operations &gt; Vehicle Refuel Logsheets</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Fuel Operations ]</span> &gt; <span class="btn">[ Vehicle Refuel Logsheets ]</span>. Click <span class="btn btn-primary">[ New ]</span> to log a slip, then <span class="btn btn-accent">[ Save ]</span>.</p>
  <p><strong>What Happens:</strong> Displays all 326 refuel slips with Slip ID (<code>FCL/2026/0001</code> to <code>0326</code>), vehicle, driver, start/end odometer, liters, KM/L, and audit badges. Automatically updates vehicle odometer and distance remaining until service.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['08']}" alt="Screen 08: Vehicle Refuel Logsheets">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 09 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 09: Cargo Fuel Dispatches &amp; In-Transit Loss Alert</div>
    <div class="excel-tag">Operationalized Bulk Haulage Meter Reconciliation</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Fuel Operations &gt; Cargo Fuel Dispatches &amp; Loss</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Fuel Operations ]</span> &gt; <span class="btn">[ Cargo Fuel Dispatches &amp; Loss ]</span>. Click dispatch <span class="btn">[ DISP/2026/0102 ]</span>.</p>
  <p><strong>What Happens:</strong> Compares loaded gantry volume (42,000 L) vs destination discharge volume (41,790 L). A variance of -210 L (-0.50%) triggers a red alert banner and generates emergency Job Card <code>JC-1014</code> for manifold inspection.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['09']}" alt="Screen 09: Cargo Fuel Dispatches & Loss Alert">
  </div>
</div>

<!-- SCREEN 10 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 10: Fleet Service Schedule</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; FLEET SERVICE</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Fleet &amp; Assets &gt; Fleet Service Schedule</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Fleet &amp; Assets ]</span> &gt; <span class="btn">[ Fleet Service Schedule ]</span>. Click filter <span class="btn">[ Service Due ]</span>.</p>
  <p><strong>What Happens:</strong> Tracks preventative maintenance intervals (15,000 / 30,000 / 50,000 km), km remaining until service, last service date, Service Status (<code>OK</code> vs <code>Service Due</code>), NaTIS roadworthy fitness, and SLP expiry dates.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['10']}" alt="Screen 10: Fleet Service Schedule">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 11 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 11: Vehicle Lifecycle Master Record (N 7802 OT)</div>
    <div class="excel-tag">Cross-Workbook Unification &gt; 8 Smart Buttons</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; Fleet &gt; Vehicles &gt; Select N 7802 OT</div>
  <p><strong>Buttons to Click:</strong> Open vehicle <code>N 7802 OT</code>. Click smart buttons: <span class="btn">[ Employee (1) ]</span>, <span class="btn">[ Drivers History (1) ]</span>, <span class="btn">[ Odometer (4) ]</span>, <span class="btn">[ Refuel Logs (9) ]</span>, <span class="btn">[ Job Cards (1) ]</span>, <span class="btn">[ Dispatches (1) ]</span>. Switch between notebook tabs.</p>
  <p><strong>What Happens:</strong> Provides a 360-degree digital asset twin unifying driver allocation, odometer history, fuel consumption, dispatches, chassis alignment specs, and scheduled maintenance on one form.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['11']}" alt="Screen 11: Vehicle Lifecycle Master Form (N 7802 OT)">
  </div>
</div>

<!-- SCREEN 12 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 12: Wheel Alignment &amp; Chassis Audit</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; Wheel Allignment</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Fleet &amp; Assets &gt; Wheel Alignment &amp; Chassis Audit</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Fleet &amp; Assets ]</span> &gt; <span class="btn">[ Wheel Alignment &amp; Chassis Audit ]</span>. Click red-flagged row <span class="btn">[ N 4584 OT ]</span>.</p>
  <p><strong>What Happens:</strong> Flags vehicles with chassis and axle misalignment causing tyre scrub and drag. Directly pinpoints units suffering a 3.43x higher excess fuel burn penalty.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['12']}" alt="Screen 12: Wheel Alignment & Chassis Audit">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 13 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 13: Workshop Job Cards &amp; Projects</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; PROJECTS</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Workshop &amp; Engineering &gt; Workshop Job Cards &amp; Projects</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Workshop &amp; Engineering ]</span> &gt; <span class="btn">[ Workshop Job Cards &amp; Projects ]</span>. Click <span class="btn btn-primary">[ New ]</span> or select <span class="btn">[ JC-1009 ]</span>.</p>
  <p><strong>What Happens:</strong> Displays job card register tracking Job Card number, assigned mechanic (Green/Japie/Clive), truck asset, coupled trailer, check-in odometer, and spare parts procurement status.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['13']}" alt="Screen 13: Workshop Job Cards & Projects">
  </div>
</div>

<!-- SCREEN 14 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 14: 24/7 Breakdown &amp; Emergency Corridors</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; BREAKDOWN</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Workshop &amp; Engineering &gt; 24/7 Breakdown &amp; Corridors</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Workshop &amp; Engineering ]</span> &gt; <span class="btn">[ 24/7 Breakdown &amp; Corridors ]</span>. Filter by corridor.</p>
  <p><strong>What Happens:</strong> Directory of 33 pre-approved emergency towing, mechanical, tyre, and electrical repair vendors mapped across 14 major Namibian transport corridors for emergency roadside dispatch.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['14']}" alt="Screen 14: 24/7 Breakdown & Emergency Corridors">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 15 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 15: Hazchem Drivers &amp; Statutory Compliance</div>
    <div class="excel-tag">Copy of Vehicle Info New.xlsx &gt; DRIVER INFORMATION</div>
  </div>
  <div class="nav-pill">📍 NFD Fuel Logistics &gt; Personnel &amp; Compliance &gt; Hazchem Drivers &amp; Licensing</div>
  <p><strong>Buttons to Click:</strong> Click <span class="btn">[ Personnel &amp; Compliance ]</span> &gt; <span class="btn">[ Hazchem Drivers &amp; Licensing ]</span>. Select any driver.</p>
  <p><strong>What Happens:</strong> Tracks National ID, Licence Code (CE, C), Start Date, PrDP expiry, Hazchem permit expiry, and trainee stipend payment cycle. Blocks non-compliant drivers from bulk fuel dispatches.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['15']}" alt="Screen 15: Hazchem Drivers & Statutory Compliance">
  </div>
</div>

<!-- SCREEN 16 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 16: Depot Inventory Stock &amp; Bulk Spares Catalog</div>
    <div class="excel-tag">Pre-installed Inventory App &gt; Central Spares Catalog</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; App Switcher [ ☷ ] &gt; Inventory &gt; Products &gt; Products</div>
  <p><strong>Buttons to Click:</strong> Click App Switcher <span class="btn btn-primary">[ ☷ ]</span> &gt; <span class="btn">[ Inventory ]</span> &gt; <span class="btn">[ Products ]</span> &gt; <span class="btn">[ Products ]</span>. Click any item card.</p>
  <p><strong>What Happens:</strong> Catalogs essential maintenance stock: Scania oil/air filters, Mercedes Actros fuel filters, Pirelli 315/80 R22.5 tyres, Shell Rimula oil, and Wayne Helix nozzles with reorder alerts.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['16']}" alt="Screen 16: Depot Inventory Stock & Bulk Spares">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 17 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 17: Spare Parts Procurement (Purchase Orders)</div>
    <div class="excel-tag">Pre-installed Purchase App &gt; 3-Way Matching</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; App Switcher [ ☷ ] &gt; Purchase &gt; Purchase Orders</div>
  <p><strong>Buttons to Click:</strong> Click App Switcher <span class="btn btn-primary">[ ☷ ]</span> &gt; <span class="btn">[ Purchase ]</span> &gt; <span class="btn">[ Purchase Orders ]</span>. Click <span class="btn">[ PO00004 ]</span>.</p>
  <p><strong>What Happens:</strong> Manages 8 active Purchase Orders issued to OEM suppliers (Scania, Mercedes-Benz, Commercial Tyres Namibia, Shell). Enforces 3-way matching before vendor bill approval.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['17']}" alt="Screen 17: Spare Parts Procurement">
  </div>
</div>

<!-- SCREEN 18 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 18: Commercial Bulk Fuel Sales Orders</div>
    <div class="excel-tag">Pre-installed Sales App &gt; Confirmed Haulage Orders</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; App Switcher [ ☷ ] &gt; Sales &gt; Orders &gt; Sales Orders</div>
  <p><strong>Buttons to Click:</strong> Click App Switcher <span class="btn btn-primary">[ ☷ ]</span> &gt; <span class="btn">[ Sales ]</span> &gt; <span class="btn">[ Orders ]</span> &gt; <span class="btn">[ Sales Orders ]</span>. Click order <span class="btn">[ S00004 ]</span>.</p>
  <p><strong>What Happens:</strong> Displays 6 confirmed bulk commercial haulage orders (Husab Mine, B2Gold Otjikoto, Petrosol Outjo, Khorixas, Grinaker-LTA) totaling <strong>NAD 5,490,240.00</strong> with status <em>To Invoice</em>.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['18']}" alt="Screen 18: Commercial Bulk Fuel Sales Orders">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 19 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 19: Customer Freight Invoicing &amp; Vendor Bills</div>
    <div class="excel-tag">Pre-installed Invoicing App &gt; General Ledger Reconciliation</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; App Switcher [ ☷ ] &gt; Invoicing &gt; Customers &gt; Invoices</div>
  <p><strong>Buttons to Click:</strong> Click App Switcher <span class="btn btn-primary">[ ☷ ]</span> &gt; <span class="btn">[ Invoicing ]</span> &gt; <span class="btn">[ Customers ]</span> &gt; <span class="btn">[ Invoices ]</span>. Click <span class="btn">[ INV/2026/0003 ]</span>.</p>
  <p><strong>What Happens:</strong> Manages customer freight invoices and vendor bills with general ledger distribution. Automatically accounts for fuel escalation surcharges and monthly fuel variance reconciliations.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['19']}" alt="Screen 19: Customer Freight Invoicing & Accounting">
  </div>
</div>

<!-- SCREEN 20 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 20: Statutory Inspections &amp; Compliance Calendar</div>
    <div class="excel-tag">Pre-installed Calendar App &gt; List View</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; App Switcher [ ☷ ] &gt; Calendar &gt; Switch to List View [ ☰ ]</div>
  <p><strong>Buttons to Click:</strong> Click App Switcher <span class="btn btn-primary">[ ☷ ]</span> &gt; <span class="btn">[ Calendar ]</span> &gt; Click <span class="btn">[ ☰ List View ]</span> in top-right.</p>
  <p><strong>What Happens:</strong> Displays a schedule of 8 statutory inspections and audits: Hazchem renewals, Chevron &gt;90% HESMS audit, depot gantry calibration, PrDP deadlines, wheel alignments, and NaTIS roadworthy tests.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['20']}" alt="Screen 20: Statutory Inspections & Compliance Calendar">
  </div>
</div>

<div class="page-break"></div>

<!-- SCREEN 21 -->
<div class="screen-card">
  <div class="screen-header">
    <div class="screen-title">Screen 21: Project / To-Do Operational Tasks</div>
    <div class="excel-tag">Pre-installed Project App &gt; All Tasks</div>
  </div>
  <div class="nav-pill">📍 Top Navbar &gt; App Switcher [ ☷ ] &gt; Project &gt; Tasks &gt; All Tasks</div>
  <p><strong>Buttons to Click:</strong> Click App Switcher <span class="btn btn-primary">[ ☷ ]</span> &gt; <span class="btn">[ Project ]</span> &gt; <span class="btn">[ Tasks ]</span> &gt; <span class="btn">[ All Tasks ]</span>. Click any task.</p>
  <p><strong>What Happens:</strong> Action list of 19 operational, workshop, and forecourt maintenance tasks tracking time, priority, and progress. Coordinates field technicians, mechanics, and drivers under a single tracked workflow.</p>
  <div class="screen-image-container">
    <img class="screen-image" src="${img['21']}" alt="Screen 21: Project / To-Do Operational Tasks">
  </div>
</div>

<div class="page-break"></div>

<!-- SECTION 3: LIVE PRESENTATION SCRIPT -->
<h1>3. Live Presentation Script: Real-Time Fleet Automation on Clean Vehicle N 10420 OT</h1>
<p>To demonstrate Odoo's automated fleet intelligence live to client executives, follow this exact 3-step live demo sequence using clean utility bakkie <strong>N 10420 OT</strong> (Chevrolet Utility 1.4i Support Bakkie).</p>

<div class="callout callout-success">
  <strong>Step 1: Verify Initial Clean State in Fleet</strong><br>
  1. Click <strong>Fleet &gt; Vehicles</strong> &gt; Open <strong>N 10420 OT</strong>.<br>
  2. Point out to the audience: Current Odometer: <code>0.0 km</code>, Refuel Logs: <code>0</code>, Service Status: <code>OK</code>, Job Cards: <code>0</code>.
</div>

<div class="callout callout-warning">
  <strong>Step 2: Enter Milestone-Crossing Refuel Slip</strong><br>
  1. Click <strong>NFD Fuel Logistics &gt; Fuel Operations &gt; Vehicle Refuel Logsheets</strong> &gt; Click <span class="btn btn-primary">[ New ]</span>.<br>
  2. Fill in: Vehicle: <code>N 10420 OT</code> | Driver: <code>Jaco Technician</code> | Start Odo: <code>150,000.0 km</code> | End Odo: <code>152,000.0 km</code> | Fuel: <code>220.0 L</code> | Place: <code>Depot (Otjiwarongo)</code>.<br>
  3. Click <span class="btn btn-accent">[ Save ]</span>.
</div>

<div class="callout callout-danger">
  <strong>Step 3: Observe the Real-Time Ripple Effect</strong><br>
  1. Return to <strong>Fleet &gt; Vehicles &gt; N 10420 OT</strong>.<br>
  2. <strong>Odometer Auto-Advance:</strong> Vehicle odometer jumped from <code>0.0 km</code> to <code>152,000.0 km</code>.<br>
  3. <strong>Dynamic Service Status:</strong> Crossing the 150,000 km threshold flipped status from <code>OK</code> to <strong><code>Service Due</code></strong>.<br>
  4. <strong>Automated Job Card Creation:</strong> Automation 3 detected the status and generated maintenance task <strong><code>JC-AUTO-49</code></strong> assigned directly to lead mechanic <strong>Clive</strong>! Smart button now displays <strong><code>Job Cards (1)</code></strong>.
</div>

<div class="page-break"></div>

<!-- SECTION 4: VEHICLE LIFECYCLE STAGES -->
<h1>4. Simulated End-to-End Vehicle Lifecycle (Stages 1 to 7)</h1>

<div class="lifecycle-stage">
  <h3>Stage 1: Asset Acquisition &amp; Fleet Onboarding</h3>
  <p>Issue Purchase Order to Mercedes-Benz Namibia for Actros 2646 <code>N 7802 OT</code> (NAD 2,150,000.00). Fixed asset created, VIN <code>WDB9340321K882910</code> registered, initial odometer set to 1,150,000 km, benchmark set to 2.00 KM/L, GT Vinyl branding confirmed.</p>
</div>

<div class="lifecycle-stage">
  <h3>Stage 2: Driver Allocation, Trainee Mentorship &amp; Statutory Compliance</h3>
  <p>Assign primary certified driver Mike Mburu (Licence CE, PrDP valid) and trainee co-driver Tobias Leopold (NAD 3,500/fortnight stipend). Statutory calendar monitors medical fitness and Hazchem renewals.</p>
</div>

<div class="lifecycle-stage">
  <h3>Stage 3: Commercial Haulage Sales Orders &amp; Cargo Dispatches</h3>
  <p>Confirm Sales Order <code>SO00003</code> for B2Gold Otjikoto Mine (42,000 L diesel, NAD 1,091,160.00). Outbound dispatch <code>DISP/2026/0102</code> logs departure. Real-time discharge monitoring flags any transit spill exceeding 0.15% tolerance.</p>
</div>

<div class="lifecycle-stage">
  <h3>Stage 4: Refueling Logsheets, KM/L Tracking &amp; Otj COC Variance</h3>
  <p>Refuel slips logged at Otjiwarongo Depot and en-route stops. 9 slips for <code>N 7802 OT</code> total 11,850 km and 5,850 L (2.03 KM/L), saving -75.0 L (-NAD 1,948.50 at NAD 25.98 / L benchmark).</p>
</div>

<div class="lifecycle-stage">
  <h3>Stage 5: Mechanical Workshop, Laser Wheel Alignment &amp; Overhauls</h3>
  <p>Preventative maintenance milestones trip at 50,000 km. Laser alignment audit flags tyre scrub on misaligned units (<code>N 4584 OT</code>). Job Card <code>JC-1009</code> assigned to mechanic Japie with timesheet labor and spare parts requisitions.</p>
</div>

<div class="lifecycle-stage">
  <h3>Stage 6: Procurement 3-Way Matching, Invoicing &amp; Financial Settlement</h3>
  <p>Purchase orders issued for Pirelli tyres and filters. Customer freight invoice <code>INV/2026/0003</code> issued to B2Gold with general ledger revenue distribution and fuel escalation surcharge reconciliation.</p>
</div>

<div class="lifecycle-stage">
  <h3>Stage 7: Fleet Governance, Asset Retirement &amp; Decommissioning</h3>
  <p>Fleet Radar monitors the 18-year prime mover / 15-year tanker retirement policy. Aging assets (e.g. 2004 Mercedes <code>N 2455 OT</code>) are transitioned to <code>For Sale</code> or <code>Decommissioned</code>, automatically removing them from active dispatch rosters.</p>
</div>

</body>
</html>
`;

// Start temporary local HTTP server to serve HTML and assets cleanly
console.log('🌐 Starting local HTTP server for Chrome headless print...');
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(htmlContent);
});

server.listen(8096, async () => {
  console.log('✓ Server listening on http://127.0.0.1:8096');

  console.log('🖥️ Launching Chrome Flatpak via CDP on port 9226...');
  const chrome = spawn('flatpak', [
    'run', 'com.google.Chrome',
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--remote-debugging-port=9226',
    'about:blank'
  ]);

  // Wait for Chrome to initialize
  await new Promise(r => setTimeout(r, 2500));

  try {
    const listRes = await fetch('http://127.0.0.1:9226/json/list');
    const targets = await listRes.json();
    const pageTarget = targets.find(t => t.type === 'page');
    if (!pageTarget) {
      throw new Error('No page target found in Chrome');
    }

    console.log('🔌 Connecting to Chrome WebSocket CDP...');
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    await new Promise(resolve => ws.onopen = resolve);

    let msgId = 1;
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const id = msgId++;
      const handler = (evt) => {
        const data = JSON.parse(evt.data);
        if (data.id === id) {
          ws.removeEventListener('message', handler);
          if (data.error) reject(data.error);
          else resolve(data.result);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id, method, params }));
    });

    await send('Page.enable');
    await send('Emulation.setEmulatedMedia', { media: 'screen' });

    console.log('📄 Navigating to SOP HTML document...');
    await send('Page.navigate', { url: 'http://127.0.0.1:8096/' });

    // Wait for DOM and images to render
    console.log('⏳ Waiting 4000ms for images and layout to settle...');
    await new Promise(r => setTimeout(r, 4000));

    console.log('🖨️ Printing high-resolution PDF with Page.printToPDF...');
    const pdfResult = await send('Page.printToPDF', {
      printBackground: true,
      paperWidth: 8.27,  // A4 Width
      paperHeight: 11.69, // A4 Height
      marginTop: 0.4,
      marginBottom: 0.4,
      marginLeft: 0.4,
      marginRight: 0.4,
      preferCSSPageSize: true
    });

    const pdfBuffer = Buffer.from(pdfResult.data, 'base64');
    fs.writeFileSync(OUTPUT_PDF, pdfBuffer);
    fs.writeFileSync(DOCS_PDF, pdfBuffer);

    const sizeMb = (pdfBuffer.length / (1024 * 1024)).toFixed(2);
    console.log(`🎉 Master SOP PDF generated successfully!`);
    console.log(`   • Output: ${OUTPUT_PDF} (${sizeMb} MB)`);
    console.log(`   • Output: ${DOCS_PDF} (${sizeMb} MB)`);

    ws.close();
  } catch (err) {
    console.error('❌ Error during PDF generation:', err);
  } finally {
    chrome.kill();
    server.close();
    process.exit(0);
  }
});
