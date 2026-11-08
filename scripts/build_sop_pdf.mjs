#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const ROOT_DIR = process.cwd();
const SCREENSHOTS_DIR = path.join(ROOT_DIR, 'docs', 'screenshots');
const OUTPUT_PDF = path.join(ROOT_DIR, 'NFD_DEMO_SOP.pdf');
const DOCS_PDF = path.join(ROOT_DIR, 'docs', 'NFD_DEMO_SOP.pdf');

console.log('🚀 Starting NFDNAM Step-by-Step Operational SOP PDF Generator...');

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

console.log('📦 Loading all 21 high-resolution screenshots...');
const img = {};
for (let i = 1; i <= 21; i++) {
  const num = String(i).padStart(2, '0');
  const files = fs.readdirSync(SCREENSHOTS_DIR).filter(f => f.startsWith(`${num}_`) && f.endsWith('.png'));
  if (files.length > 0) {
    img[num] = getBase64Image(files[0]);
  }
}

// 21 Sequential Real-Life Operational Steps
const steps = [
  {
    stepNum: 1,
    phase: 'PHASE A: ORDER & DISPATCH PREPARATION',
    phaseColor: '#1e40af',
    title: 'System Access & Application Navigation',
    nav: 'Top-left corner of any screen > Click Waffle Icon [ ☷ ]',
    buttons: 'Click the [ ☷ Waffle Icon ] in the top navbar. Select [ Sales ] to begin customer order intake, or [ NFD Fuel Logistics ] for fleet operations.',
    happens: 'The enterprise app launcher opens, displaying all 14 active departments. Consolidates commercial haulage, fleet maintenance, fuel logistics, and accounting under a single unified sign-on.',
    excel: 'Replaces disconnected desktop spreadsheets with a central ERP portal',
    imgKey: '01'
  },
  {
    stepNum: 2,
    phase: 'PHASE A: ORDER & DISPATCH PREPARATION',
    phaseColor: '#1e40af',
    title: 'Commercial Bulk Fuel Sales Order Booking',
    nav: 'Sales > Orders > Sales Orders',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Sales ] > Click [ Orders ] > [ Sales Orders ]. Select order [ S00003 ] (B2Gold Otjikoto) or click [ New ] to book a delivery.',
    happens: 'Confirms bulk fuel haulage contracts (e.g. S00003: 42,000 L Ultra-Low Sulphur Diesel to B2Gold Otjikoto Mine, NAD 1,091,160.00). Confirmed order enters the transport dispatch queue.',
    excel: 'Pre-installed Sales App > Commercial Haulage Pipeline (NAD 5.49M)',
    imgKey: '18'
  },
  {
    stepNum: 3,
    phase: 'PHASE A: ORDER & DISPATCH PREPARATION',
    phaseColor: '#1e40af',
    title: 'Driver Allocation & Statutory Compliance Audit',
    nav: 'NFD Fuel Logistics > Personnel & Compliance > Hazchem Drivers & Licensing',
    buttons: 'Click [ Personnel & Compliance ] > Click [ Hazchem Drivers & Licensing ]. Select driver [ Mike Mburu ] or [ Tobias Leopold ].',
    happens: 'Verifies the assigned driver possesses an unexpired Heavy Articulated Licence (Code CE), valid Public Driving Permit (PrDP), and active Hazchem Dangerous Goods Permit. Blocks dispatch if certifications have lapsed.',
    excel: 'Copy of Vehicle Info New.xlsx > DRIVER INFORMATION (A3:K45)',
    imgKey: '15'
  },
  {
    stepNum: 4,
    phase: 'PHASE A: ORDER & DISPATCH PREPARATION',
    phaseColor: '#1e40af',
    title: 'Statutory Compliance Calendar & Inspection Schedule',
    nav: 'Calendar > Switch to List View [ ☰ ]',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Calendar ] > Click [ ☰ List View ] button in the top-right corner.',
    happens: 'Audits upcoming statutory inspection deadlines across the fleet: NaTIS vehicle roadworthy renewals, gantry LC master meter calibrations, and Hazchem audit dates, ensuring scheduled trips do not conflict with required testing.',
    excel: 'Pre-installed Calendar App > Statutory Fleet Deadlines',
    imgKey: '20'
  },
  {
    stepNum: 5,
    phase: 'PHASE A: ORDER & DISPATCH PREPARATION',
    phaseColor: '#1e40af',
    title: 'Vehicle Master Inspection & Trailer Coupling (Flagship N 7802 OT)',
    nav: 'Fleet > Vehicles > Select N 7802 OT',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Fleet ] > [ Vehicles ] > Open [ N 7802 OT ]. Click smart buttons [ Employee (1) ], [ Refuel Logs (9) ], [ Dispatches (1) ]. Switch between notebook tabs.',
    happens: 'Inspects the 360-degree digital asset twin of long-haul prime mover N 7802 OT: coupled B-double bulk tanker trailer 6776, benchmark fuel consumption (2.00 KM/L), current odometer, and GT Vinyl livery branding status.',
    excel: 'Copy of Vehicle Info New.xlsx > FLEET SERVICE & DRIVER ALLOCATION',
    imgKey: '11'
  },
  {
    stepNum: 6,
    phase: 'PHASE A: ORDER & DISPATCH PREPARATION',
    phaseColor: '#1e40af',
    title: 'Fleet Readiness & Operational Availability Radar',
    nav: 'NFD Fuel Logistics > Executive Dashboards > Fleet Readiness & Service Radar',
    buttons: 'Click [ Executive Dashboards ] > Click [ Fleet Readiness & Service Radar ]. Use [ Group By ] to filter by Availability Group.',
    happens: 'Verifies overall fleet readiness against operational targets: Tankers (88% target availability), Rigids (77% target availability). Ensures sufficient operational buffer before committing haulage units to commercial routes.',
    excel: 'Copy of Vehicle Info New.xlsx > AVAILABILITY (A2:G35)',
    imgKey: '05'
  },
  {
    stepNum: 7,
    phase: 'PHASE B: DEPOT LOADING & IN-TRANSIT DISPATCH',
    phaseColor: '#047857',
    title: 'Gantry Bulk Fuel Loading & Cargo Dispatch',
    nav: 'NFD Fuel Logistics > Fuel Operations > Cargo Fuel Dispatches & Loss',
    buttons: 'Click [ Fuel Operations ] > Click [ Cargo Fuel Dispatches & Loss ]. Select dispatch [ DISP/2026/0102 ].',
    happens: 'Records outbound bulk fuel departure: 42,000 L loaded at Otjiwarongo depot gantry into tanker 6776. Monitors destination discharge volume (41,790 L). A variance of -210 L (-0.50%) triggers an automated leak alert and emergency maintenance ticket.',
    excel: 'Operationalizes Bulk Haulage Dispatches & Gantry Loss Audit',
    imgKey: '09'
  },
  {
    stepNum: 8,
    phase: 'PHASE B: DEPOT LOADING & IN-TRANSIT DISPATCH',
    phaseColor: '#047857',
    title: 'In-Transit Task Tracking & Corridor Operations',
    nav: 'Project > Tasks > All Tasks',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Project ] > Click [ Tasks ] > [ All Tasks ]. Click any active haulage task.',
    happens: 'Coordinates long-haul corridor operations (e.g. Walvis Bay to Otjiwarongo Tank Farm Inbound Haulage, B2Gold Daily Haulage). Drivers and controllers track stage completion and log route timesheet hours.',
    excel: 'Copy of Vehicle Info New.xlsx > PROJECTS (A3:I35)',
    imgKey: '21'
  },
  {
    stepNum: 9,
    phase: 'PHASE B: DEPOT LOADING & IN-TRANSIT DISPATCH',
    phaseColor: '#047857',
    title: 'Roadside Emergency & 24/7 Breakdown Routing',
    nav: 'NFD Fuel Logistics > Workshop & Engineering > 24/7 Breakdown & Corridors',
    buttons: 'Click [ Workshop & Engineering ] > Click [ 24/7 Breakdown & Corridors ]. Filter by corridor (e.g. B1 North, Trans-Kalahari B6).',
    happens: 'If an en-route mechanical issue or puncture occurs, dispatchers immediately locate the nearest pre-vetted roadside service, towing, tyre, or auto-electrical vendor across 14 major Namibian transport corridors.',
    excel: 'Copy of Vehicle Info New.xlsx > BREAKDOWN (A3:E20)',
    imgKey: '14'
  },
  {
    stepNum: 10,
    phase: 'PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING',
    phaseColor: '#b45309',
    title: 'Driver Refuel Slip Submission (Depot & En-Route)',
    nav: 'NFD Fuel Logistics > Fuel Operations > Vehicle Refuel Logsheets',
    buttons: 'Click [ Fuel Operations ] > Click [ Vehicle Refuel Logsheets ]. Click [ New ] to enter a slip, then click [ Save ].',
    happens: 'Logs refuel slip: Vehicle, Driver, Start/End Odometer, Fuel Liters, and Place. System instantly calculates distance and KM/L efficiency, advances the vehicle master odometer reading, and evaluates audit compliance.',
    excel: 'Copy of Fuel Consumption 09 2026.xlsx > Vehicle Tabs (Rows 10:24)',
    imgKey: '08'
  },
  {
    stepNum: 11,
    phase: 'PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING',
    phaseColor: '#b45309',
    title: 'Real-Time Fuel Audit & Executive Kanban Triage',
    nav: 'NFD Fuel Logistics > Executive Dashboards > NFD Executive Command Center',
    buttons: 'Click [ Executive Dashboards ] > Click [ NFD Executive Command Center ]. Click any card to inspect trip audit details.',
    happens: 'Triages all 326 refuel slips into 3 operational Kanban lanes: Excess Burn (83 trips exceeding benchmark), Within Target (177 trips saving fuel), and Odometer / Logsheet Anomaly (66 trips with clerical errors or missing slips).',
    excel: 'Copy of Fuel Consumption 09 2026.xlsx > Summary Sheet & Tabs',
    imgKey: '02'
  },
  {
    stepNum: 12,
    phase: 'PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING',
    phaseColor: '#b45309',
    title: 'Fleet-Wide Fuel Consumption Summary & Excel Rollup',
    nav: 'NFD Fuel Logistics > Fuel Operations > Fuel Consumption Summary',
    buttons: 'Click [ Fuel Operations ] > Click [ Fuel Consumption Summary ]. Click any vehicle row to open the complete monthly breakdown.',
    happens: 'Rolls up the monthly performance of all 41 vehicles: 285,640.0 km traveled, 100,269.50 L actual fuel, and net +2,871.39 L excess fuel (+NAD 74,598.69 net financial variance). Exactly reconciles the master Excel summary.',
    excel: 'Copy of Fuel Consumption 09 2026.xlsx > Summary (B4:I50)',
    imgKey: '07'
  },
  {
    stepNum: 13,
    phase: 'PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING',
    phaseColor: '#b45309',
    title: 'Financial Fuel Variance & Commercial Pricing Analysis',
    nav: 'NFD Fuel Logistics > Executive Dashboards > Fuel & Otj COC Variance',
    buttons: 'Click [ Executive Dashboards ] > Click [ Fuel & Otj COC Variance ]. Toggle between [ Bar Chart ] and [ Pivot ] view in the top-right.',
    happens: 'Quantifies fuel variance in monetary terms using the Otjiwarongo Commercial Operations Cost benchmark price: NAD 25.98 / L. Isolates top excess burners (+NAD 122,701.18) against star savers (-NAD 48,102.49).',
    excel: 'Copy of Fuel Consumption 09 2026.xlsx > Summary (C3:E3, G4:I45)',
    imgKey: '03'
  },
  {
    stepNum: 14,
    phase: 'PHASE C: REFUELING, TELEMATICS & FUEL ACCOUNTING',
    phaseColor: '#b45309',
    title: 'Regional Station & Fuel Draw Analytics',
    nav: 'NFD Fuel Logistics > Executive Dashboards > Driver & Refueling Site Analytics',
    buttons: 'Click [ Executive Dashboards ] > Click [ Driver & Refueling Site Analytics ]. Click [ Measures ] to toggle between Liters and Count.',
    happens: 'Analyzes regional fuel draw across 13 stops (Otjiwarongo Depot, Walvis Bay, Agra Vivo, CJ Steenkamp, Ndama, Tokat, Veronika, Weimans). Identifies high-draw locations for bulk corporate rebate negotiations.',
    excel: 'Copy of Fuel Consumption 09 2026.xlsx > Vehicle Tabs (Column F: Place)',
    imgKey: '04'
  },
  {
    stepNum: 15,
    phase: 'PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Post-Trip Milestone Tracking & Service Due Triggers',
    nav: 'NFD Fuel Logistics > Fleet & Assets > Fleet Service Schedule',
    buttons: 'Click [ Fleet & Assets ] > Click [ Fleet Service Schedule ]. Click filter [ Service Due ] to view overdue vehicles.',
    happens: 'As refuel logsheets advance vehicle odometers, the system compares readings against 15,000 / 30,000 / 50,000 km intervals. When km remaining reaches 0, the vehicle automatically flips to Service Due.',
    excel: 'Copy of Vehicle Info New.xlsx > FLEET SERVICE (A5:L45)',
    imgKey: '10'
  },
  {
    stepNum: 16,
    phase: 'PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Laser Wheel Alignment & Chassis Drag Diagnostics',
    nav: 'NFD Fuel Logistics > Fleet & Assets > Wheel Alignment & Chassis Audit',
    buttons: 'Click [ Fleet & Assets ] > Click [ Wheel Alignment & Chassis Audit ]. Select red-flagged vehicle [ N 4584 OT ].',
    happens: 'Audits steering and tandem axle alignment. Flags misaligned vehicles (N 2455, N 4584, N 11028, N 11963) suffering severe tyre scrub, which drives a 3.43x higher excess fuel burn rate.',
    excel: 'Copy of Vehicle Info New.xlsx > Wheel Allignment Worksheet',
    imgKey: '12'
  },
  {
    stepNum: 17,
    phase: 'PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Workshop Job Card Issuance & Mechanic Assignment',
    nav: 'NFD Fuel Logistics > Workshop & Engineering > Workshop Job Cards & Projects',
    buttons: 'Click [ Workshop & Engineering ] > Click [ Workshop Job Cards & Projects ]. Select job card [ JC-1009 ] or click [ New ].',
    happens: 'Creates maintenance work order linking vehicle asset, coupled trailer, check-in odometer, and assigned lead mechanic (Green/Japie/Clive) for chassis repairs, laser alignment, or milestone servicing.',
    excel: 'Copy of Vehicle Info New.xlsx > PROJECTS (A3:I35)',
    imgKey: '13'
  },
  {
    stepNum: 18,
    phase: 'PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Workshop Labor Timesheets & Job Card Progress',
    nav: 'NFD Fuel Logistics > Executive Dashboards > Workshop, Alignment & Timesheets',
    buttons: 'Click [ Executive Dashboards ] > Click [ Workshop, Alignment & Timesheets ]. Click on any mechanic column to drill down.',
    happens: 'Tracks workshop labor timesheets and progress across active job cards. Balances mechanic workload between routine services, chassis overhauls, and pump calibrations.',
    excel: 'Copy of Vehicle Info New.xlsx > PROJECTS (Mechanic Allocation)',
    imgKey: '06'
  },
  {
    stepNum: 19,
    phase: 'PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Depot Inventory Requisition & Spare Parts Issue',
    nav: 'Inventory > Products > Products',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Inventory ] > Click [ Products ] > [ Products ]. Select product card.',
    happens: 'Issues workshop maintenance spares from central Otjiwarongo depot stock: Scania oil/air filter kits, Mercedes fuel filters, Pirelli 315/80 R22.5 tyres, and Shell Rimula heavy engine oil. Real-time stock decrements automatically.',
    excel: 'Pre-installed Inventory App > Central Spare Parts Catalog',
    imgKey: '16'
  },
  {
    stepNum: 20,
    phase: 'PHASE D: WORKSHOP SERVICING & FLEET MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Spare Parts Replenishment & 3-Way Matching Purchase Order',
    nav: 'Purchase > Purchase Orders',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Purchase ] > Click [ Purchase Orders ]. Select order [ PO00004 ] (Commercial Tyres Namibia).',
    happens: 'Generates supplier Purchase Order to replenish depot parts stock. Enforces 3-way matching between Purchase Order, Warehouse Delivery Receipt, and Vendor Invoices before payment authorization.',
    excel: 'Pre-installed Purchase App > OEM Supplier Procurement',
    imgKey: '17'
  },
  {
    stepNum: 21,
    phase: 'PHASE E: COMMERCIAL BILLING & FINANCIAL CLOSE',
    phaseColor: '#0f766e',
    title: 'Commercial Freight Invoicing & Customer Billing',
    nav: 'Invoicing > Customers > Invoices',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Invoicing ] > Click [ Customers ] > [ Invoices ]. Select invoice [ INV/2026/0003 ] for B2Gold Otjikoto.',
    happens: 'Generates customer freight invoice upon delivery confirmation. Integrates fuel escalation surcharges and reconciles trip revenue against fuel expenses into general ledger accounts, closing the operational cycle.',
    excel: 'Pre-installed Invoicing App > Freight Revenue & Margin Close',
    imgKey: '19'
  }
];

console.log('📝 Building HTML document for 21 sequential operational steps...');
const stepsHtml = steps.map(s => `
<div class="screen-card">
  <div class="screen-header">
    <div>
      <span class="phase-badge" style="background-color: ${s.phaseColor};">${s.phase}</span>
      <h2 class="screen-title">Step ${s.stepNum}: ${s.title}</h2>
    </div>
    <div class="excel-tag">${s.excel}</div>
  </div>
  
  <div class="nav-pill">📍 <strong>Navigation:</strong> ${s.nav}</div>
  
  <div class="step-meta">
    <p><strong>Buttons to Click:</strong> ${s.buttons}</p>
    <p><strong>What Happens:</strong> ${s.happens}</p>
  </div>
  
  <div class="screen-image-container">
    <img class="screen-image" src="${img[s.imgKey]}" alt="Step ${s.stepNum}: ${s.title}">
  </div>
</div>
`).join('\n<div class="page-break"></div>\n');

const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NFDNAM Standard Operating Procedure (SOP)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 12mm 12mm 12mm;
  }

  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    background-color: #ffffff;
    font-size: 9pt;
    line-height: 1.4;
    margin: 0;
    padding: 0;
  }

  .sop-header {
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 10px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .sop-title {
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
    line-height: 1.1;
  }
  .sop-subtitle {
    font-size: 9.5pt;
    color: #475569;
    margin: 4px 0 0 0;
    font-weight: 500;
  }
  .sop-meta-tag {
    font-size: 8pt;
    font-weight: 700;
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    color: #334155;
    padding: 4px 10px;
    border-radius: 4px;
    text-align: right;
  }

  .page-break { page-break-after: always; }

  .screen-card {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    padding: 10px 12px;
    page-break-inside: avoid;
  }
  .screen-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .phase-badge {
    display: inline-block;
    color: #ffffff;
    font-size: 7pt;
    font-weight: 800;
    letter-spacing: 0.5px;
    padding: 2px 6px;
    border-radius: 3px;
    margin-bottom: 4px;
    text-transform: uppercase;
  }
  .screen-title {
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
    line-height: 1.2;
  }
  .excel-tag {
    font-size: 7pt;
    font-weight: 600;
    background-color: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    padding: 3px 6px;
    border-radius: 4px;
    max-width: 42%;
    text-align: right;
  }

  .nav-pill {
    background-color: #eff6ff;
    color: #1e40af;
    font-size: 8pt;
    font-weight: 600;
    border: 1px solid #bfdbfe;
    border-radius: 4px;
    padding: 4px 8px;
    margin-bottom: 6px;
  }

  .step-meta p {
    margin: 0 0 4px 0;
    font-size: 8.5pt;
    line-height: 1.35;
  }
  .step-meta strong {
    color: #1e293b;
  }

  .screen-image-container {
    margin-top: 8px;
    text-align: center;
  }
  .screen-image {
    width: 100%;
    max-width: 100%;
    height: auto;
    border: 1px solid #94a3b8;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  }
</style>
</head>
<body>

<div class="sop-header">
  <div>
    <h1 class="sop-title">NFDNAM Standard Operating Procedure (SOP)</h1>
    <p class="sop-subtitle">End-to-End Operational Lifecycle: Sales Order &rarr; Dispatch &rarr; Refueling &rarr; Workshop &rarr; Invoicing</p>
  </div>
  <div class="sop-meta-tag">
    Operational Manual<br>21 Sequential Steps
  </div>
</div>

${stepsHtml}

</body>
</html>
`;

console.log('🌐 Starting local HTTP server for Chrome headless print...');
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(htmlContent);
});

server.listen(8097, async () => {
  console.log('✓ Server listening on http://127.0.0.1:8097');

  console.log('🖥️ Launching Chrome Flatpak via CDP on port 9227...');
  const chrome = spawn('flatpak', [
    'run', 'com.google.Chrome',
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--remote-debugging-port=9227',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 2500));

  try {
    const listRes = await fetch('http://127.0.0.1:9227/json/list');
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
    await send('Page.navigate', { url: 'http://127.0.0.1:8097/' });

    console.log('⏳ Waiting 4000ms for images and layout to settle...');
    await new Promise(r => setTimeout(r, 4000));

    console.log('🖨️ Printing PDF with Page.printToPDF (no header/footer)...');
    const pdfResult = await send('Page.printToPDF', {
      printBackground: true,
      paperWidth: 8.27,  // A4 Width
      paperHeight: 11.69, // A4 Height
      marginTop: 0.35,
      marginBottom: 0.35,
      marginLeft: 0.35,
      marginRight: 0.35,
      displayHeaderFooter: false,
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
