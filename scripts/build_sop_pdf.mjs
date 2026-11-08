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

// 21 Sequential Real-Life Operational Steps (Flow: Order -> Preparation -> Dispatch -> Refueling -> Workshop -> Invoicing)
const steps = [
  {
    stepNum: 1,
    phase: 'STAGE 1: ORDER & PREPARATION',
    phaseColor: '#1e40af',
    title: 'Log In & Main Menu',
    nav: 'Top-left menu icon [ ☷ ]',
    buttons: 'Click the [ ☷ ] icon in the top-left navbar to open the main menu.',
    happens: 'Opens the main menu showing Sales, Fleet, Maintenance, Inventory, and Invoicing in one place.',
    excel: 'Replaces scattered spreadsheets with one central system',
    imgKey: '01'
  },
  {
    stepNum: 2,
    phase: 'STAGE 1: ORDER & PREPARATION',
    phaseColor: '#1e40af',
    title: 'Customer Fuel Orders',
    nav: 'Sales > Orders > Orders',
    buttons: 'Click [ Sales ] > [ Orders ] > [ Orders ]. Click order [ S00003 ] (B2Gold Otjikoto).',
    happens: 'Shows the confirmed order: 42,000 Litres of Diesel to B2Gold Otjikoto Mine (NAD 1,091,160.00). The delivery is now ready to dispatch.',
    excel: 'Sales App > Fuel delivery contract',
    imgKey: '18'
  },
  {
    stepNum: 3,
    phase: 'STAGE 1: ORDER & PREPARATION',
    phaseColor: '#1e40af',
    title: 'Drivers & Licences',
    nav: 'NFD Fuel Logistics > Drivers > Drivers & Licences',
    buttons: 'Click [ Drivers ] > [ Drivers & Licences ]. Click driver [ Mike Mburu ].',
    happens: 'Confirms the assigned driver has a valid heavy vehicle licence (Code CE), dangerous goods permit, and medical clearance. The system flags if any licence is expired.',
    excel: 'Replaces Driver Info sheet',
    imgKey: '15'
  },
  {
    stepNum: 4,
    phase: 'STAGE 1: ORDER & PREPARATION',
    phaseColor: '#1e40af',
    title: 'Permit & Inspection Calendar',
    nav: 'Calendar > Switch to List View [ ☰ ]',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Calendar ] > Click [ ☰ List View ] in the top-right corner.',
    happens: 'Shows upcoming expiry dates for roadworthy tests (NaTIS), pump calibrations, and driver permits so trucks are not stopped on the road.',
    excel: 'Calendar App > Renewal schedule',
    imgKey: '20'
  },
  {
    stepNum: 5,
    phase: 'STAGE 1: ORDER & PREPARATION',
    phaseColor: '#1e40af',
    title: 'Truck & Trailer Details (Truck N 7802 OT)',
    nav: 'Fleet > Vehicles > Select N 7802 OT',
    buttons: 'Click [ Fleet ] > [ Vehicles ] > Click [ N 7802 OT ]. Click smart buttons [ Drivers ], [ Fuel Receipts ], or [ Dispatches ].',
    happens: 'Shows everything about the truck: attached tanker trailer 6776, assigned driver, current odometer reading, target fuel consumption (2.00 KM/L), and branding.',
    excel: 'Vehicle Info sheet > Fleet list',
    imgKey: '11'
  },
  {
    stepNum: 6,
    phase: 'STAGE 1: ORDER & PREPARATION',
    phaseColor: '#1e40af',
    title: 'Fleet Availability',
    nav: 'NFD Fuel Logistics > Dashboards > Fleet Availability',
    buttons: 'Click [ Dashboards ] > [ Fleet Availability ]. Group by truck group.',
    happens: 'Shows which trucks are active, in the workshop, or on standby. Ensures backup trucks are available before sending out new deliveries.',
    excel: 'Vehicle Info sheet > Availability tab',
    imgKey: '05'
  },
  {
    stepNum: 7,
    phase: 'STAGE 2: LOADING & ON THE ROAD',
    phaseColor: '#047857',
    title: 'Fuel Dispatches & Deliveries',
    nav: 'NFD Fuel Logistics > Fuel Operations > Fuel Dispatches & Deliveries',
    buttons: 'Click [ Fuel Operations ] > [ Fuel Dispatches & Deliveries ]. Click dispatch [ DISP/2026/0102 ].',
    happens: 'Records fuel loaded at Otjiwarongo depot (42,000 L) into tanker 6776, and fuel delivered at B2Gold (41,790 L). If loss exceeds 0.25%, an alert flags a potential leak or theft.',
    excel: 'Tracks bulk fuel loaded vs delivered',
    imgKey: '09'
  },
  {
    stepNum: 8,
    phase: 'STAGE 2: LOADING & ON THE ROAD',
    phaseColor: '#047857',
    title: 'Delivery Tasks',
    nav: 'Project > Tasks > All Tasks',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Project ] > Click [ Tasks ] > [ All Tasks ]. Click any active delivery task.',
    happens: 'Tracks trips as they move along transport routes (e.g. Walvis Bay to Otjiwarongo, or Otjiwarongo to B2Gold). Controllers see trip status and driver hours.',
    excel: 'Vehicle Info sheet > Projects tab',
    imgKey: '21'
  },
  {
    stepNum: 9,
    phase: 'STAGE 2: LOADING & ON THE ROAD',
    phaseColor: '#047857',
    title: 'Emergency Repair Contacts',
    nav: 'NFD Fuel Logistics > Workshop > Emergency Repair Contacts',
    buttons: 'Click [ Workshop ] > [ Emergency Repair Contacts ]. Filter by town or route (e.g. B1 North).',
    happens: 'If a truck breaks down or gets a flat tyre on the road, dispatchers quickly find the nearest approved mechanic, towing service, or tyre shop along that highway.',
    excel: 'Vehicle Info sheet > Breakdown tab',
    imgKey: '14'
  },
  {
    stepNum: 10,
    phase: 'STAGE 3: FUEL CONSUMPTION & AUDIT',
    phaseColor: '#b45309',
    title: 'Driver Fuel Receipts',
    nav: 'NFD Fuel Logistics > Fuel Operations > Driver Fuel Receipts',
    buttons: 'Click [ Fuel Operations ] > [ Driver Fuel Receipts ]. Click [ New ] to add a receipt, then [ Save ].',
    happens: 'Enters the refuel slip: Truck, Driver, Odometer Start/End, Litres pumped, and Station. The system calculates distance traveled, KM/L, and updates the truck odometer.',
    excel: 'Fuel Consumption workbook > Vehicle sheets',
    imgKey: '08'
  },
  {
    stepNum: 11,
    phase: 'STAGE 3: FUEL CONSUMPTION & AUDIT',
    phaseColor: '#b45309',
    title: 'Fuel Review (Cards)',
    nav: 'NFD Fuel Logistics > Dashboards > Fuel Review (Cards)',
    buttons: 'Click [ Dashboards ] > [ Fuel Review (Cards) ]. Click any card to see trip details.',
    happens: 'Sorts all 326 refuel slips into 3 clear groups: High Fuel Burn (used too much fuel), Within Target (good consumption), and Needs Check (odometer mistakes or missing slips).',
    excel: 'Replaces manual fuel audit checks',
    imgKey: '02'
  },
  {
    stepNum: 12,
    phase: 'STAGE 3: FUEL CONSUMPTION & AUDIT',
    phaseColor: '#b45309',
    title: 'Monthly Fuel Summary',
    nav: 'NFD Fuel Logistics > Fuel Operations > Monthly Fuel Summary',
    buttons: 'Click [ Fuel Operations ] > [ Monthly Fuel Summary ]. Click a truck to view its full monthly log.',
    happens: 'Summarizes all 41 vehicles for the month: 285,640 km driven, 100,269.5 L consumed, and +2,871.4 L excess fuel. Exactly matches the master monthly Excel summary sheet.',
    excel: 'Fuel Consumption workbook > Summary tab',
    imgKey: '07'
  },
  {
    stepNum: 13,
    phase: 'STAGE 3: FUEL CONSUMPTION & AUDIT',
    phaseColor: '#b45309',
    title: 'Fuel Costs & Savings',
    nav: 'NFD Fuel Logistics > Dashboards > Fuel Costs & Savings',
    buttons: 'Click [ Dashboards ] > [ Fuel Costs & Savings ]. Switch between Bar Chart and Table view.',
    happens: 'Converts fuel variance into Namibia Dollars using the fuel price (NAD 25.98 / L). Shows how much money was lost on high-burn trucks (+NAD 122,701) and saved on efficient trucks (-NAD 48,102).',
    excel: 'Fuel Consumption workbook > Cost variance',
    imgKey: '03'
  },
  {
    stepNum: 14,
    phase: 'STAGE 3: FUEL CONSUMPTION & AUDIT',
    phaseColor: '#b45309',
    title: 'Fuel by Station',
    nav: 'NFD Fuel Logistics > Dashboards > Fuel by Station',
    buttons: 'Click [ Dashboards ] > [ Fuel by Station ]. Click [ Measures ] to view Litres or Number of Refuels.',
    happens: 'Shows where the fleet refuels most often (Otjiwarongo Depot, Walvis Bay, Agra Vivo, etc.). Helps management negotiate bulk discounts at the busiest fuel stops.',
    excel: 'Fuel Consumption workbook > Refuel locations',
    imgKey: '04'
  },
  {
    stepNum: 15,
    phase: 'STAGE 4: WORKSHOP & MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Vehicle Service Due Dates',
    nav: 'NFD Fuel Logistics > Fleet & Assets > Vehicle Service Due Dates',
    buttons: 'Click [ Fleet & Assets ] > [ Vehicle Service Due Dates ]. Click [ Service Due ] filter.',
    happens: 'As drivers log km on refuel slips, the system counts down to the next service (15,000, 30,000, or 50,000 km). When km remaining hits 0, it flags the truck as Service Due.',
    excel: 'Vehicle Info sheet > Fleet Service tab',
    imgKey: '10'
  },
  {
    stepNum: 16,
    phase: 'STAGE 4: WORKSHOP & MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Wheel Alignment Check',
    nav: 'NFD Fuel Logistics > Fleet & Assets > Wheel Alignment Check',
    buttons: 'Click [ Fleet & Assets ] > [ Wheel Alignment Check ]. Click truck [ N 4584 OT ].',
    happens: 'Tracks laser wheel alignment measurements. Flags trucks with bad alignment (like N 4584 OT), which scrubs tyres and burns up to 3 times more fuel than normal.',
    excel: 'Vehicle Info sheet > Wheel Alignment tab',
    imgKey: '12'
  },
  {
    stepNum: 17,
    phase: 'STAGE 4: WORKSHOP & MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Workshop Job Cards',
    nav: 'NFD Fuel Logistics > Workshop > Workshop Job Cards',
    buttons: 'Click [ Workshop ] > [ Workshop Job Cards ]. Click job card [ JC-1009 ] or click [ New ].',
    happens: 'Creates a repair order for the workshop. Links the truck, trailer, current odometer, and assigns mechanics (e.g. Japie or Clive) to fix the issue or do a service.',
    excel: 'Vehicle Info sheet > Projects & Work Orders',
    imgKey: '13'
  },
  {
    stepNum: 18,
    phase: 'STAGE 4: WORKSHOP & MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Mechanic Hours & Progress',
    nav: 'NFD Fuel Logistics > Dashboards > Mechanic Hours & Progress',
    buttons: 'Click [ Dashboards ] > [ Mechanic Hours & Progress ]. Click a mechanic\'s column to see their tasks.',
    happens: 'Shows hours worked by each mechanic and the progress on each job card. Helps workshop managers see who is busy and keep repairs on schedule.',
    excel: 'Vehicle Info sheet > Mechanic hours',
    imgKey: '06'
  },
  {
    stepNum: 19,
    phase: 'STAGE 4: WORKSHOP & MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Spare Parts in Depot',
    nav: 'Inventory > Products > Products',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Inventory ] > Click [ Products ] > [ Products ]. Click any part card (e.g. Oil Filter, Tyres).',
    happens: 'Shows spare parts available in the Otjiwarongo workshop: filters, tyres, and engine oil. Stock counts decrease automatically whenever parts are used on a job card.',
    excel: 'Inventory App > Spare parts catalog',
    imgKey: '16'
  },
  {
    stepNum: 20,
    phase: 'STAGE 4: WORKSHOP & MAINTENANCE',
    phaseColor: '#7c3aed',
    title: 'Orders to Parts Suppliers',
    nav: 'Purchase > Purchase Orders',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Purchase ] > Click [ Purchase Orders ]. Click order [ PO00004 ] (Commercial Tyres Namibia).',
    happens: 'Creates purchase orders to buy replacement parts from suppliers. Matches the purchase order against the delivery receipt and supplier invoice before payment is approved.',
    excel: 'Purchase App > Parts purchasing',
    imgKey: '17'
  },
  {
    stepNum: 21,
    phase: 'STAGE 5: INVOICING & PAYMENT',
    phaseColor: '#0f766e',
    title: 'Customer Invoices',
    nav: 'Invoicing > Customers > Invoices',
    buttons: 'Click App Switcher [ ☷ ] > Click [ Invoicing ] > Click [ Customers ] > [ Invoices ]. Click invoice [ INV/2026/0003 ] for B2Gold.',
    happens: 'Creates the final customer invoice after fuel is delivered. Calculates the delivery rate, adds fuel surcharges, and records revenue into accounting to complete the order.',
    excel: 'Invoicing App > Customer Billing',
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
    <p class="sop-subtitle">Real-Life Workflow: Customer Order &rarr; Dispatch &rarr; Refueling &rarr; Workshop &rarr; Invoicing</p>
  </div>
  <div class="sop-meta-tag">
    21 Operational Steps
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
