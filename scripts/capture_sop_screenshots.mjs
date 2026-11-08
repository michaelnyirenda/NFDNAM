import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

const SCREENSHOT_DIR = '/home/mikedotmp3/dev/projects/NFDNAM/docs/screenshots';
fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

console.log('🚀 Starting Chrome Headless via Flatpak with CDP on port 9222...');
const chrome = spawn('flatpak', [
  'run', 'com.google.Chrome',
  '--headless=new',
  '--remote-debugging-port=9222',
  '--no-sandbox',
  '--window-size=1600,1000'
]);

for (let i = 0; i < 25; i++) {
  await new Promise(r => setTimeout(r, 500));
  try {
    const res = await fetch('http://127.0.0.1:9222/json/version');
    if (res.ok) {
      const v = await res.json();
      console.log('✓ Connected to:', v.Browser);
      break;
    }
  } catch (e) {}
}

const targetRes = await fetch('http://127.0.0.1:9222/json/new?http://localhost:8069/web/login', { method: 'PUT' });
const target = await targetRes.json();
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);

let reqId = 1;
function send(method, params = {}) {
  return new Promise((resolve) => {
    const curId = reqId++;
    const handler = (evt) => {
      const msg = JSON.parse(evt.data);
      if (msg.id === curId) {
        ws.removeEventListener('message', handler);
        resolve(msg.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });
}

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });

console.log('🔑 Logging in to Odoo as admin...');
await new Promise(r => setTimeout(r, 1500));
await send('Runtime.evaluate', {
  expression: `
    document.querySelector('input[name="login"]').value = 'admin';
    document.querySelector('input[name="password"]').value = 'admin';
    document.querySelector('button[type="submit"]').click();
  `
});

for (let i = 0; i < 30; i++) {
  await new Promise(r => setTimeout(r, 500));
  const res = await send('Runtime.evaluate', { expression: `!!document.querySelector('.o_navbar')` });
  if (res.result?.value) {
    console.log('✓ Logged in and web client loaded.');
    break;
  }
}

async function captureScreen(filename, actionFn, waitMs = 2500) {
  console.log(`📸 Capturing: ${filename}...`);
  if (actionFn) {
    await send('Runtime.evaluate', {
      expression: `(${actionFn.toString()})()`,
      awaitPromise: true
    });
  }
  await new Promise(r => setTimeout(r, waitMs));

  const { data } = await send('Page.captureScreenshot', { format: 'png' });
  const filePath = path.join(SCREENSHOT_DIR, filename);
  fs.writeFileSync(filePath, Buffer.from(data, 'base64'));
  const sizeKb = (fs.statSync(filePath).size / 1024).toFixed(1);
  const title = (await send('Runtime.evaluate', { expression: `document.title` })).result?.value || '';
  console.log(`   ✓ Saved: ${filename} (${sizeKb} KB) - Title: "${title}"`);
}

// 1. App Switcher
await captureScreen('01_app_home_switcher.png', () => {
  document.querySelector('.o_navbar_apps_menu button')?.click();
}, 1200);

// Close menu
await send('Runtime.evaluate', {
  expression: `document.querySelector('.o_navbar_apps_menu button')?.click() || document.body.click()`
});
await new Promise(r => setTimeout(r, 600));

// 2. Executive Command Center
await captureScreen('02_exec_command_center.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_dash_command_center', { clearBreadcrumbs: true });
}, 3000);

// 3. Fuel Variance
await captureScreen('03_dash_fuel_variance.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_dash_fuel_variance', { clearBreadcrumbs: true });
}, 3000);

// 4. Driver & Site Analytics
await captureScreen('04_dash_driver_site.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_dash_driver_site', { clearBreadcrumbs: true });
}, 3000);

// 5. Fleet Readiness & Service Radar
await captureScreen('05_dash_fleet_radar.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_dash_fleet_radar', { clearBreadcrumbs: true });
}, 3000);

// 6. Workshop, Alignment & Timesheets
await captureScreen('06_dash_workshop_alignment.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_dash_workshop_alignment', { clearBreadcrumbs: true });
}, 3000);

// 7. Fuel Consumption Summary
await captureScreen('07_fuel_consumption_summary.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_fuel_summary', { clearBreadcrumbs: true });
}, 2500);

// 8. Vehicle Refuel Logsheets
await captureScreen('08_vehicle_refuel_logsheets.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_fuel_consumption_log', { clearBreadcrumbs: true });
}, 2500);

// 9. Cargo Fuel Dispatches & Loss Form View DISP/2026/0102
await captureScreen('09_cargo_fuel_dispatch_alert.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction({
    type: 'ir.actions.act_window',
    res_model: 'nfd.fuel.dispatch.log',
    res_id: 2,
    views: [[false, 'form']]
  }, { clearBreadcrumbs: true });
}, 2500);

// 10. Fleet Service Schedule
await captureScreen('10_fleet_service_schedule.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_fleet_service_schedule', { clearBreadcrumbs: true });
}, 2500);

// 11. Vehicle Lifecycle Form (Flagship N 7802 OT)
await captureScreen('11_vehicle_lifecycle_form_n7802ot.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction({
    type: 'ir.actions.act_window',
    res_model: 'fleet.vehicle',
    res_id: 42,
    views: [[false, 'form']]
  }, { clearBreadcrumbs: true });
}, 2500);

// 12. Wheel Alignment & Chassis Audit
await captureScreen('12_wheel_alignment_audit.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_wheel_alignment', { clearBreadcrumbs: true });
}, 2500);

// 13. Workshop Job Cards & Projects
await captureScreen('13_workshop_job_cards.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_workshop_job_cards', { clearBreadcrumbs: true });
}, 2500);

// 14. 24/7 Breakdown & Corridors
await captureScreen('14_breakdown_corridors.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_breakdown_corridors', { clearBreadcrumbs: true });
}, 2500);

// 15. Hazchem Drivers & Licensing
await captureScreen('15_hazchem_drivers_licensing.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('nfd_petrosol_demo.action_nfd_driver_compliance', { clearBreadcrumbs: true });
}, 2500);

// 16. Depot Inventory Stock
await captureScreen('16_depot_inventory_stock.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('stock.product_template_action_product', { clearBreadcrumbs: true });
}, 2500);

// 17. Purchases Spare Parts (PO App)
await captureScreen('17_purchases_spare_parts.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('purchase.purchase_form_action', { clearBreadcrumbs: true });
}, 2500);

// 18. Sales Bulk Fuel Orders (Sales App)
await captureScreen('18_sales_bulk_fuel_orders.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('sale.action_orders', { clearBreadcrumbs: true });
}, 2500);

// 19. Invoicing & Accounting
await captureScreen('19_invoicing_accounting.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('account.action_move_out_invoice_type', { clearBreadcrumbs: true });
}, 2500);

// 20. Calendar Compliance Schedule
await captureScreen('20_calendar_compliance_schedule.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction({
    type: 'ir.actions.act_window',
    res_model: 'calendar.event',
    name: 'Statutory Inspections & Compliance Calendar',
    views: [[false, 'list'], [false, 'calendar'], [false, 'form']]
  }, { clearBreadcrumbs: true });
}, 2500);

// 21. Project / To-Do Tasks
await captureScreen('21_project_todo_tasks.png', () => {
  return odoo.__WOWL_DEBUG__.root.env.services.action.doAction('project.action_view_all_task', { clearBreadcrumbs: true });
}, 2500);

console.log('🎉 All 21 screenshots successfully captured and saved into docs/screenshots/!');
chrome.kill();
process.exit(0);
