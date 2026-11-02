#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-End Master Data and Declarative Schema Generator
for NFD & Petrosol Logistics Demo Addon.
Reads 'Copy of Vehicle Info New.xlsx' and generates:
1. ir_model_fields extensions for saas-edu-import
2. demo_data.xml for main and saas-edu-import
"""

import openpyxl
import re
import os
from datetime import datetime, date

EXCEL_PATH = '/tmp/Copy of Vehicle Info New.xlsx' if os.path.exists('/tmp/Copy of Vehicle Info New.xlsx') else 'Copy of Vehicle Info New.xlsx'

def parse_date(val):
    if not val or val == 'N/A' or val == 0:
        return None
    if isinstance(val, (datetime, date)):
        return val.strftime('%Y-%m-%d')
    s = str(val).strip()
    for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d', '%d/%n/%Y'):
        try:
            return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
        except Exception:
            pass
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', s)
    if m:
        d, mth, y = m.groups()
        return f'{y}-{int(mth):02d}-{int(d):02d}'
    return None

def parse_num(val):
    if val is None or val == '' or val == 'N/A':
        return 0.0
    try:
        return float(val)
    except:
        return 0.0

def xml_escape(s):
    if not s:
        return ''
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def main():
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    
    # -------------------------------------------------------------------------
    # 1. DRIVERS
    # -------------------------------------------------------------------------
    ws_di = wb['DRIVER INFORMATION']
    driver_rows = list(ws_di.iter_rows(values_only=True))
    
    known_driver_ids = {
        'niklas ashipala': 'employee_niklas',
        'mike mburu': 'employee_mike',
        'denzel tjombonde': 'employee_denzel',
        'benhard kangandi': 'employee_benhardt',
        'gabriel tjiueza': 'employee_gabriel',
        'raymond booysen': 'employee_raymond',
        'andreas iipinge': 'employee_andreas_i',
        'maxi wohler': 'employee_maxi',
        'conrall davids': 'employee_conrall',
        'simon tsaoseb': 'employee_simon',
        'oscar': 'employee_oscar',
        'stefanus kefas': 'employee_stefanus',
        'kamuteke kauaine': 'employee_kamuteke',
        'matheus aluendo': 'employee_matheus_shikongo',
        'matheus shikongo': 'employee_matheus_shikongo',
        'elrico hoaeb': 'employee_elrico',
        'lucas': 'employee_lucas',
        'laythonne': 'employee_laythonne',
    }
    
    drivers = []
    driver_lookup = {}
    
    for r in driver_rows[1:]:
        if not r[0] or not r[1]:
            continue
        first = str(r[0]).strip().title()
        last = str(r[1]).strip().title()
        full_name = f'{first} {last}'
        name_key = full_name.lower()
        
        xml_id = known_driver_ids.get(name_key)
        if not xml_id:
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', f'{first.lower()}_{last.lower()}').strip('_')
            xml_id = f'employee_{clean_name}'
            
        phone = str(r[2]).strip() if r[2] else ''
        id_num = str(r[3]).strip() if r[3] else ''
        lic_exp = parse_date(r[8])
        code = str(r[9]).strip() if r[9] else 'CE'
        if code not in ('CE', 'C', 'C1', 'BE', 'B'):
            code = 'CE'
        pdp_exp = parse_date(r[10])
        med_exp = parse_date(r[11])
        haz_exp = parse_date(r[12])
        eye_exp = parse_date(r[13])
        
        # Franzua Tsuseb flagged EXPIRED (6 months ago)
        if 'franzua' in first.lower() or 'tsuseb' in last.lower():
            haz_exp = '2026-05-25'
            
        # Largo Green expiring within 30 days
        if 'largo' in first.lower() or 'green' in last.lower():
            pdp_exp = '2026-11-14'
            
        driver_data = {
            'xml_id': xml_id,
            'name': full_name,
            'first': first,
            'last': last,
            'phone': phone,
            'id_num': id_num,
            'lic_exp': lic_exp,
            'code': code,
            'pdp_exp': pdp_exp,
            'med_exp': med_exp,
            'haz_exp': haz_exp,
            'eye_exp': eye_exp,
        }
        drivers.append(driver_data)
        driver_lookup[first.lower()] = xml_id
        driver_lookup[last.lower()] = xml_id
        driver_lookup[name_key] = xml_id

    # -------------------------------------------------------------------------
    # 2. BREAKDOWN PARTNERS & SUPPLIERS
    # -------------------------------------------------------------------------
    ws_bd = wb['BREAKDOWN CONTACTS']
    bd_rows = list(ws_bd.iter_rows(values_only=True))
    
    breakdown_partners = []
    current_town = 'Namibia'
    
    for idx, r in enumerate(bd_rows[3:], 1):
        if r[0]:
            current_town = str(r[0]).strip()
        cat = str(r[1]).strip() if r[1] else ''
        comp = str(r[2]).strip() if r[2] else ''
        contact = str(r[3]).strip() if r[3] else ''
        email = str(r[4]).strip() if r[4] else ''
        phone = str(r[5]).strip() if r[5] else ''
        
        if not (comp or contact or phone):
            continue
            
        name = ''
        if comp and contact:
            name = f"{comp} ({contact}) - {current_town}"
        elif comp:
            name = f"{comp} - {current_town}"
        elif contact:
            name = f"{contact} Breakdown - {current_town}"
        else:
            name = f"{current_town} Emergency Service"
            
        stype = 'mechanical'
        clow = cat.lower()
        if 'electric' in clow: stype = 'auto_electrical'
        elif 'towing' in clow: stype = 'towing'
        elif 'tyre' in clow: stype = 'tyres'
        elif 'assistance' in clow or 'all' in clow: stype = 'all_round'
        
        clean_town = re.sub(r'[^a-zA-Z0-9_]', '_', current_town.lower())
        xml_id = f"partner_bd_{clean_town}_{idx}"
        breakdown_partners.append({
            'xml_id': xml_id,
            'name': name,
            'town': current_town,
            'phone': phone,
            'email': email,
            'service_type': stype,
            'contact': contact,
            'company': comp,
        })
        
    # -------------------------------------------------------------------------
    # 3. FLEET SERVICE, AVAILABILITY, PTO & DRIVER ALLOCATION
    # -------------------------------------------------------------------------
    ws_pto = wb['PTO']
    pto_map = {}
    for r in list(ws_pto.iter_rows(values_only=True))[1:]:
        reg = str(r[0]).strip() if r[0] else None
        if reg:
            eng = bool(r[3]) if r[3] is not None else False
            hyd = bool(r[4]) if r[4] is not None else False
            loc = str(r[5]).strip() if r[5] else ''
            ptype = 'none'
            if eng and hyd: ptype = 'both'
            elif eng: ptype = 'engine_pto'
            elif hyd: ptype = 'hydraulic_pto'
            pto_map[reg] = {'type': ptype, 'location': loc}
            
    ws_da = wb['DRIVER ALLOCATION']
    driver_alloc = {}
    for r in list(ws_da.iter_rows(values_only=True))[1:]:
        reg = str(r[0]).strip() if r[0] else None
        if reg:
            c1 = str(r[1]).strip() if r[1] and str(r[1]).strip() not in ('', '0') else None
            c2 = str(r[2]).strip() if r[2] and str(r[2]).strip() not in ('', '0') else None
            driver_name = str(r[6]).strip().title() if r[6] else None
            note = str(r[7]).strip() if r[7] else ''
            driver_alloc[reg] = {'c1': c1, 'c2': c2, 'driver': driver_name, 'note': note}
            
    ws_av = wb['AVAILABLITY']
    avail_map = {}
    for r in list(ws_av.iter_rows(values_only=True))[2:]:
        if r[0]:
            reg = str(r[0]).strip()
            note = str(r[2]).strip().lower() if r[2] else ''
            status = 'active'
            if 'accident' in note: status = 'accident'
            elif 'engine' in note: status = 'maintenance'
            elif 'roadworthy' in note: status = 'roadworthy'
            avail_map[reg] = status
        if len(r) > 4 and r[4]:
            reg = str(r[4]).strip()
            note = str(r[6]).strip().lower() if r[6] else ''
            status = 'active'
            if 'roadworthy' in note: status = 'roadworthy'
            avail_map[reg] = status
        if len(r) > 8 and r[8]:
            reg = str(r[8]).strip()
            avail_map[reg] = 'standby'
        if len(r) > 12 and r[12]:
            reg = str(r[12]).strip()
            avail_map[reg] = 'for_sale'
            
    ws_fs = wb['FLEET SERVICE']
    fs_rows = list(ws_fs.iter_rows(values_only=True))
    
    vehicles = []
    trailers = []
    all_fleet = {}
    
    known_vehicle_ids = {
        '7802': 'vehicle_n7802ot',
        '11751': 'vehicle_n11751ot',
        '11963': 'vehicle_n11963ot',
        '10544': 'vehicle_n10544ot',
        '2745': 'vehicle_n2745ot',
        '12916': 'vehicle_n12916ot',
        '10684': 'vehicle_n10684ot',
        '12917': 'vehicle_n12917ot',
        '13938': 'vehicle_n13938ot',
        '12611': 'vehicle_n12611ot',
        '13831': 'vehicle_n13831ot',
        '11255': 'vehicle_n11255ot',
        '12043': 'vehicle_n12043ot',
        '13566': 'vehicle_n13566ot',
    }
    
    # September 2026 workbook metrics map (preserving excess fuel values)
    sept_metrics = {
        '7802': {'km_l': 2.3, 'act_km_l': 2.05, 'km': 13024.0, 'exp_fuel': 5662.61, 'act_fuel': 6280.21, 'excess': 617.60, 'nad': 16045.25},
        '11751': {'km_l': 2.2, 'act_km_l': 2.04, 'km': 6415.0, 'exp_fuel': 2915.91, 'act_fuel': 3144.60, 'excess': 228.69, 'nad': 5941.37},
        '11963': {'km_l': 2.4, 'act_km_l': 2.29, 'km': 10582.0, 'exp_fuel': 4409.17, 'act_fuel': 4621.00, 'excess': 211.83, 'nad': 5503.34},
        '10544': {'km_l': 2.5, 'act_km_l': 2.36, 'km': 6825.0, 'exp_fuel': 2730.00, 'act_fuel': 2891.90, 'excess': 161.90, 'nad': 4206.16},
        '2745': {'km_l': 2.1, 'act_km_l': 1.63, 'km': 158.0, 'exp_fuel': 75.24, 'act_fuel': 97.00, 'excess': 21.76, 'nad': 565.32},
        '12916': {'km_l': 2.5, 'act_km_l': 2.65, 'km': 10118.0, 'exp_fuel': 4047.20, 'act_fuel': 3818.00, 'excess': -229.20, 'nad': -5954.62},
        '10684': {'km_l': 2.7, 'act_km_l': 2.78, 'km': 13812.0, 'exp_fuel': 5115.56, 'act_fuel': 4968.32, 'excess': -147.24, 'nad': -3825.30},
        '12917': {'km_l': 2.4, 'act_km_l': 2.47, 'km': 9840.0, 'exp_fuel': 4100.00, 'act_fuel': 3983.80, 'excess': -116.20, 'nad': -3018.88},
        '13938': {'km_l': 10.0, 'act_km_l': 10.24, 'km': 630.0, 'exp_fuel': 63.00, 'act_fuel': 61.50, 'excess': -1.50, 'nad': -38.97},
        '12611': {'km_l': 9.5, 'act_km_l': 9.13, 'km': 594.0, 'exp_fuel': 62.53, 'act_fuel': 65.06, 'excess': 2.53, 'nad': 65.73},
        '13831': {'km_l': 12.0, 'act_km_l': 11.85, 'km': 850.0, 'exp_fuel': 70.83, 'act_fuel': 71.73, 'excess': 0.90, 'nad': 23.38},
        '11255': {'km_l': 2.5, 'act_km_l': 2.48, 'km': 11200.0, 'exp_fuel': 4480.00, 'act_fuel': 4516.13, 'excess': 36.13, 'nad': 938.66},
        '12043': {'km_l': 2.4, 'act_km_l': 2.38, 'km': 8950.0, 'exp_fuel': 3729.17, 'act_fuel': 3760.50, 'excess': 31.33, 'nad': 813.95},
        '13566': {'km_l': 2.4, 'act_km_l': 2.41, 'km': 10450.0, 'exp_fuel': 4354.17, 'act_fuel': 4336.10, 'excess': -18.07, 'nad': -469.46},
    }
    
    trailer_xml_ids = {}
    for r in fs_rows[1:]:
        reg = str(r[0]).strip() if r[0] is not None else None
        if not reg or reg == 'TRUCK' or reg == '0':
            continue
        if len(reg) > 20 or any(w in reg.lower() for w in ('rooi', 'groen', 'blou', 'pers', 'trok kan', 'datum')):
            continue
        clean_reg = re.sub(r'[^a-zA-Z0-9_]', '_', str(reg).lower()).strip('_')
        vtype = str(r[3]).strip().upper() if r[3] else 'TRUCK'
        if any(t in vtype for t in ('TANKER', 'LINK', 'TRAILER', 'DRAWBAR')):
            trailer_xml_ids[reg] = f"vehicle_n{clean_reg}ot"
            
    for r in fs_rows[1:]:
        reg = str(r[0]).strip() if r[0] is not None else None
        if not reg or reg == 'TRUCK' or reg == '0':
            continue
        if len(reg) > 20 or any(w in reg.lower() for w in ('rooi', 'groen', 'blou', 'pers', 'trok kan', 'datum')):
            continue
            
        clean_reg = re.sub(r'[^a-zA-Z0-9_]', '_', str(reg).lower()).strip('_')
        xml_id = known_vehicle_ids.get(reg)
        if not xml_id:
            xml_id = f"vehicle_n{clean_reg}ot"
            
        c1 = str(r[1]).strip() if r[1] is not None and str(r[1]).strip() not in ('', '0') else None
        c2 = str(r[2]).strip() if r[2] is not None and str(r[2]).strip() not in ('', '0') else None
        
        if reg in driver_alloc:
            if driver_alloc[reg]['c1']: c1 = driver_alloc[reg]['c1']
            if driver_alloc[reg]['c2']: c2 = driver_alloc[reg]['c2']
            
        vtype = str(r[3]).strip().upper() if r[3] else 'TRUCK'
        desc = str(r[5]).strip() if r[5] else ''
        diesel = parse_num(r[6])
        ulp = parse_num(r[7])
        last_srv = parse_date(r[9])
        last_km = parse_num(r[10])
        interval = parse_num(r[11]) or 30000.0
        next_km = parse_num(r[12])
        lic_exp = parse_date(r[19])
        fit_exp = parse_date(r[20])
        slp_exp = parse_date(r[21])
        press_exp = parse_date(r[22])
        wheel_date = parse_date(r[23])
        
        classification = 'prime_mover'
        if 'RIGID' in vtype:
            classification = 'rigid_tanker'
        elif 'TANKER' in vtype:
            classification = 'semi_trailer'
        elif 'LINK' in vtype:
            classification = 'pup_trailer'
        elif 'TRAILER' in vtype or 'DRAWBAR' in vtype:
            classification = 'drawbar_trailer'
            
        brand_ref = 'brand_mercedes'
        model_ref = 'model_actros_2645'
        d_lower = desc.lower()
        if 'scania' in d_lower or 'r500' in d_lower:
            brand_ref = 'brand_scania'
            model_ref = 'model_scania_r500'
        elif 'volvo' in d_lower or 'fh' in d_lower:
            brand_ref = 'brand_volvo'
            model_ref = 'model_volvo_fh440'
        elif 'nissan' in d_lower or 'ud' in d_lower:
            brand_ref = 'brand_nissan'
            model_ref = 'model_nissan_ud100'
        elif 'hilux' in d_lower or 'toyota' in d_lower:
            brand_ref = 'brand_toyota'
            model_ref = 'model_toyota_hilux'
        elif 'grw' in d_lower:
            brand_ref = 'brand_grw'
            model_ref = 'model_grw_tanker'
        elif 'tank clinic' in d_lower:
            brand_ref = 'brand_tankclinic'
            model_ref = 'model_tankclinic_tanker'
        elif 'link' in d_lower:
            brand_ref = 'brand_henred'
            model_ref = 'model_henred_link'
        elif '2652' in d_lower:
            model_ref = 'model_actros_2652'
        elif '2646' in d_lower:
            model_ref = 'model_actros_2646'
        elif '3350' in d_lower or '3352' in d_lower:
            model_ref = 'model_actros_3352'
        elif 'axor' in d_lower:
            model_ref = 'model_axor_rigid'
        elif 'crane' in vtype.lower():
            brand_ref = 'brand_tadano'
            model_ref = 'model_mobile_crane'
        elif reg in ('10914', '10915', '10916', '10919'):
            model_ref = 'model_actros_3344'
            
        pto_info = pto_map.get(reg, {'type': 'none', 'location': ''})
        availability = avail_map.get(reg, 'active')
        if reg in ('10914', '10915', '10916', '10919'):
            availability = 'for_sale'
            
        driver_xml_id = None
        if reg in driver_alloc and driver_alloc[reg]['driver']:
            d_name = driver_alloc[reg]['driver'].lower()
            driver_xml_id = driver_lookup.get(d_name)
            
        odo = last_km or 0.0
        remaining_km = 0.0
        service_status = 'ok'
        if next_km:
            remaining_km = next_km - odo
            if remaining_km < 0:
                service_status = 'overdue'
            elif remaining_km <= 5000:
                service_status = 'due_soon'
                
        c1_ref = trailer_xml_ids.get(c1) if c1 else None
        c2_ref = trailer_xml_ids.get(c2) if c2 else None
        
        has_meter = bool(diesel > 0 or ulp > 0)
        
        # Determine manufacture year roughly from mileage or model
        mfg_year = 2021
        if odo > 1200000: mfg_year = 2012
        elif odo > 800000: mfg_year = 2016
        elif odo > 400000: mfg_year = 2019
        elif odo > 0: mfg_year = 2022
        
        v_entry = {
            'xml_id': xml_id,
            'reg': reg,
            'plate': f"N {reg} OT",
            'desc': desc or f"NFD Unit {reg}",
            'vtype': vtype,
            'classification': classification,
            'brand_ref': brand_ref,
            'model_ref': model_ref,
            'c1_ref': c1_ref,
            'c2_ref': c2_ref,
            'driver_ref': driver_xml_id,
            'diesel': diesel,
            'ulp': ulp,
            'max_vol': max(diesel + ulp, diesel, ulp, 0.0),
            'last_srv': last_srv,
            'last_km': last_km,
            'odometer': odo,
            'interval': interval,
            'next_km': next_km,
            'remaining_km': remaining_km,
            'service_status': service_status,
            'lic_exp': lic_exp,
            'fit_exp': fit_exp,
            'slp_exp': slp_exp,
            'press_exp': press_exp,
            'wheel_date': wheel_date,
            'pto_type': pto_info['type'],
            'pto_location': pto_info['location'],
            'availability': availability,
            'has_meter': has_meter,
            'mfg_year': mfg_year,
            'sept': sept_metrics.get(reg)
        }
        all_fleet[reg] = v_entry
        if classification in ('semi_trailer', 'pup_trailer', 'drawbar_trailer'):
            trailers.append(v_entry)
        else:
            vehicles.append(v_entry)

    # -------------------------------------------------------------------------
    # 4. ASSEMBLE DEMO_DATA.XML
    # -------------------------------------------------------------------------
    out = []
    out.append('<?xml version="1.0" encoding="utf-8"?>')
    out.append('<odoo>')
    out.append('    <data noupdate="0">')
    
    # 1. Warehouse & Stock Locations
    out.append('''
    <!-- ============================================================== -->
    <!-- 1. WAREHOUSE & STOCK LOCATIONS (OTJIWARONGO DEPOT)            -->
    <!-- ============================================================== -->
    <record id="stock.warehouse0" model="stock.warehouse">
        <field name="name">Otjiwarongo Bulk Fuel Depot</field>
        <field name="code">OTJ</field>
    </record>

    <record id="location_otjiwarongo_depot" model="stock.location">
        <field name="name">Otjiwarongo Tank Farm</field>
        <field name="usage">internal</field>
        <field name="location_id" ref="stock.stock_location_stock"/>
    </record>

    <record id="location_depot_diesel_tank1" model="stock.location">
        <field name="name">Depot Tank 1 - Diesel 50ppm (500kL)</field>
        <field name="usage">internal</field>
        <field name="location_id" ref="location_otjiwarongo_depot"/>
    </record>

    <record id="location_depot_ulp_tank1" model="stock.location">
        <field name="name">Depot Tank 2 - ULP 95 (200kL)</field>
        <field name="usage">internal</field>
        <field name="location_id" ref="location_otjiwarongo_depot"/>
    </record>

    <record id="location_husab_mine" model="stock.location">
        <field name="name">Husab Mine Bulk Storage Depot</field>
        <field name="usage">customer</field>
    </record>

    <record id="location_b2gold_mine" model="stock.location">
        <field name="name">B2Gold Otjikoto Mine Tank Farm</field>
        <field name="usage">customer</field>
    </record>

    <record id="location_petrosol_outjo" model="stock.location">
        <field name="name">Petrosol Retail Forecourt - Outjo</field>
        <field name="usage">customer</field>
    </record>

    <!-- Legacy Demo Stock Locations (b84fb91 compatibility) -->
    <record id="location_depot_bulk" model="stock.location">
        <field name="name">Bulk Fuel Tank Farm</field>
        <field name="location_id" ref="stock.stock_location_stock"/>
        <field name="usage">internal</field>
    </record>

    <record id="location_tank_1_diesel" model="stock.location">
        <field name="name">Tank 1 - Diesel 50ppm (500,000L)</field>
        <field name="location_id" ref="location_depot_bulk"/>
        <field name="usage">internal</field>
    </record>

    <record id="location_tank_2_ulp95" model="stock.location">
        <field name="name">Tank 2 - ULP 95 (200,000L)</field>
        <field name="location_id" ref="location_depot_bulk"/>
        <field name="usage">internal</field>
    </record>

    <record id="location_workshop_store" model="stock.location">
        <field name="name">Workshop Spare Parts &amp; Consumables</field>
        <field name="location_id" ref="stock.stock_location_stock"/>
        <field name="usage">internal</field>
    </record>

    <record id="location_transit_tankers" model="stock.location">
        <field name="name">Fuel In-Transit (Fleet Road Tankers)</field>
        <field name="location_id" ref="stock.stock_location_stock"/>
        <field name="usage">transit</field>
    </record>

    <record id="location_fuel_shrinkage" model="stock.location">
        <field name="name">Fuel Handling Loss &amp; Shrinkage</field>
        <field name="location_id" ref="stock.stock_location_company"/>
        <field name="usage">inventory</field>
    </record>

    <!-- ============================================================== -->
    <!-- 2. PRODUCTS (FUELS, LUBRICANTS & WORKSHOP SPARES)             -->
    <!-- ============================================================== -->
    <record id="product_diesel_50ppm" model="product.product">
        <field name="name">Diesel 50ppm (Low Sulphur Bulk)</field>
        <field name="type">consu</field>
        <field name="default_code">FUEL-DSL-50PPM</field>
        <field name="list_price">24.50</field>
        <field name="standard_price">22.80</field>
    </record>

    <record id="product_ulp_95" model="product.product">
        <field name="name">Unleaded Petrol 95 (ULP 95 Bulk)</field>
        <field name="type">consu</field>
        <field name="default_code">FUEL-ULP-95</field>
        <field name="list_price">23.80</field>
        <field name="standard_price">22.10</field>
    </record>

    <record id="product_engine_oil_15w40" model="product.product">
        <field name="name">Delo 400 Heavy Duty Engine Oil 15W-40 (210L Drum)</field>
        <field name="type">consu</field>
        <field name="default_code">LUB-DELO-15W40</field>
        <field name="list_price">14500.00</field>
        <field name="standard_price">11200.00</field>
    </record>

    <record id="product_brake_fluid_dot4" model="product.product">
        <field name="name">Heavy Duty Brake Fluid DOT 4 (20L)</field>
        <field name="type">consu</field>
        <field name="default_code">LUB-BRK-DOT4</field>
        <field name="list_price">1850.00</field>
        <field name="standard_price">1350.00</field>
    </record>

    <record id="product_fuel_dispenser_pump" model="product.product">
        <field name="name">Wayne Helix 4-Hose Electronic Fuel Dispenser Pump</field>
        <field name="type">consu</field>
        <field name="default_code">EQ-DISP-HELIX4</field>
        <field name="list_price">185000.00</field>
        <field name="standard_price">142000.00</field>
    </record>

    <record id="product_bulk_flow_meter" model="product.product">
        <field name="name">LC Master Calibrated Bulk Cargo Flow Meter (M-15)</field>
        <field name="type">consu</field>
        <field name="default_code">EQ-MTR-LC-M15</field>
        <field name="list_price">95000.00</field>
        <field name="standard_price">74000.00</field>
    </record>

    <!-- Legacy Spares & Consumables (b84fb91 compatibility) -->
    <record id="product_oil_15w40" model="product.product">
        <field name="name">Heavy Duty Engine Oil 15W-40 (210L Drum)</field>
        <field name="type">consu</field>
        <field name="default_code">OIL-15W40-DRUM</field>
        <field name="list_price">12500.00</field>
        <field name="standard_price">9800.00</field>
    </record>

    <record id="product_grease_ep2" model="product.product">
        <field name="name">High-Temp Lithium EP2 Grease (18kg Pail)</field>
        <field name="type">consu</field>
        <field name="default_code">GRS-EP2-18KG</field>
        <field name="list_price">2400.00</field>
        <field name="standard_price">1850.00</field>
    </record>

    <record id="product_scania_filter_kit" model="product.product">
        <field name="name">Scania R500 Fuel &amp; Oil Filter Service Kit</field>
        <field name="type">consu</field>
        <field name="default_code">KIT-SCANIA-R500</field>
        <field name="list_price">4850.00</field>
        <field name="standard_price">3600.00</field>
    </record>

    <record id="product_tanker_seal_kit" model="product.product">
        <field name="name">Bottom-Loading Foot Valve Seal Replacement Kit</field>
        <field name="type">consu</field>
        <field name="default_code">KIT-VALVE-SEAL</field>
        <field name="list_price">3200.00</field>
        <field name="standard_price">2100.00</field>
    </record>

    <!-- ============================================================== -->
    <!-- 3. FLEET BRANDS & VEHICLE MODELS                               -->
    <!-- ============================================================== -->
    <record id="brand_scania" model="fleet.vehicle.model.brand">
        <field name="name">Scania</field>
    </record>
    <record id="brand_mercedes" model="fleet.vehicle.model.brand">
        <field name="name">Mercedes-Benz</field>
    </record>
    <record id="brand_freightliner" model="fleet.vehicle.model.brand">
        <field name="name">Freightliner</field>
    </record>
    <record id="brand_volvo" model="fleet.vehicle.model.brand">
        <field name="name">Volvo</field>
    </record>
    <record id="brand_isuzu" model="fleet.vehicle.model.brand">
        <field name="name">Isuzu</field>
    </record>
    <record id="brand_suzuki" model="fleet.vehicle.model.brand">
        <field name="name">Suzuki</field>
    </record>
    <record id="brand_ford" model="fleet.vehicle.model.brand">
        <field name="name">Ford</field>
    </record>
    <record id="brand_nissan" model="fleet.vehicle.model.brand">
        <field name="name">Nissan UD</field>
    </record>
    <record id="brand_toyota" model="fleet.vehicle.model.brand">
        <field name="name">Toyota</field>
    </record>
    <record id="brand_grw" model="fleet.vehicle.model.brand">
        <field name="name">GRW Tankers</field>
    </record>
    <record id="brand_tankclinic" model="fleet.vehicle.model.brand">
        <field name="name">Tank Clinic</field>
    </record>
    <record id="brand_henred" model="fleet.vehicle.model.brand">
        <field name="name">Henred Fruehauf</field>
    </record>
    <record id="brand_tadano" model="fleet.vehicle.model.brand">
        <field name="name">Tadano Mobile Cranes</field>
    </record>

    <record id="model_scania_r500" model="fleet.vehicle.model">
        <field name="name">R500 6x4 Heavy Hauler</field>
        <field name="brand_id" ref="brand_scania"/>
    </record>
    <record id="model_actros_2645" model="fleet.vehicle.model">
        <field name="name">Actros 2645 6x4</field>
        <field name="brand_id" ref="brand_mercedes"/>
    </record>
    <record id="model_argosy" model="fleet.vehicle.model">
        <field name="name">Argosy Prime Mover</field>
        <field name="brand_id" ref="brand_freightliner"/>
    </record>
    <record id="model_axor_rigid" model="fleet.vehicle.model">
        <field name="name">Axor 17,500L Rigid Tanker</field>
        <field name="brand_id" ref="brand_mercedes"/>
    </record>
    <record id="model_scania_p360" model="fleet.vehicle.model">
        <field name="name">P360 16,000L Rigid Tanker</field>
        <field name="brand_id" ref="brand_scania"/>
    </record>
    <record id="model_volvo_fh440" model="fleet.vehicle.model">
        <field name="name">Volvo FH440 6x4</field>
        <field name="brand_id" ref="brand_volvo"/>
    </record>
    <record id="model_volvo_fh520" model="fleet.vehicle.model">
        <field name="name">Volvo FH520 6x4 Long-Haul</field>
        <field name="brand_id" ref="brand_volvo"/>
    </record>
    <record id="model_isuzu_dmax" model="fleet.vehicle.model">
        <field name="name">Isuzu 1.9 D-MAX</field>
        <field name="brand_id" ref="brand_isuzu"/>
    </record>
    <record id="model_suzuki_carry" model="fleet.vehicle.model">
        <field name="name">Suzuki Carry 1.2</field>
        <field name="brand_id" ref="brand_suzuki"/>
    </record>
    <record id="model_ford_tremor" model="fleet.vehicle.model">
        <field name="name">Ford Tremor 4x4</field>
        <field name="brand_id" ref="brand_ford"/>
    </record>
    <record id="model_actros_2646" model="fleet.vehicle.model">
        <field name="name">Actros 2646 6x4</field>
        <field name="brand_id" ref="brand_mercedes"/>
    </record>
    <record id="model_actros_2652" model="fleet.vehicle.model">
        <field name="name">Actros 2652 6x4</field>
        <field name="brand_id" ref="brand_mercedes"/>
    </record>
    <record id="model_actros_3352" model="fleet.vehicle.model">
        <field name="name">Actros 3352 6x4 Severe-Duty</field>
        <field name="brand_id" ref="brand_mercedes"/>
    </record>
    <record id="model_actros_3344" model="fleet.vehicle.model">
        <field name="name">Actros 3344 6x4</field>
        <field name="brand_id" ref="brand_mercedes"/>
    </record>
    <record id="model_nissan_ud100" model="fleet.vehicle.model">
        <field name="name">Nissan UD100 10,200L Rigid Tanker</field>
        <field name="brand_id" ref="brand_nissan"/>
    </record>
    <record id="model_toyota_hilux" model="fleet.vehicle.model">
        <field name="name">Toyota Hilux 4x4 Support Bakkie</field>
        <field name="brand_id" ref="brand_toyota"/>
    </record>
    <record id="model_grw_tanker" model="fleet.vehicle.model">
        <field name="name">GRW Tri-Axle Bulk Fuel Tanker</field>
        <field name="brand_id" ref="brand_grw"/>
    </record>
    <record id="model_tankclinic_tanker" model="fleet.vehicle.model">
        <field name="name">Tank Clinic 36,000L Semi-Trailer</field>
        <field name="brand_id" ref="brand_tankclinic"/>
    </record>
    <record id="model_henred_link" model="fleet.vehicle.model">
        <field name="name">Henred Fruehauf B-Double Link</field>
        <field name="brand_id" ref="brand_henred"/>
    </record>
    <record id="model_mobile_crane" model="fleet.vehicle.model">
        <field name="name">Tadano Heavy Mobile Recovery Crane</field>
        <field name="brand_id" ref="brand_tadano"/>
    </record>
''')

    # 4. Partners (Customers, Spare Parts Suppliers & 24/7 Breakdown Network)
    out.append('''
    <!-- ============================================================== -->
    <!-- 4. PARTNERS: CUSTOMERS, SUPPLIERS & 24/7 BREAKDOWN NETWORK     -->
    <!-- ============================================================== -->
    <record id="partner_husab_mine" model="res.partner">
        <field name="name">Husab Mine (Swakop Uranium)</field>
        <field name="is_company">True</field>
        <field name="street">Swakopmund Mining District</field>
        <field name="city">Swakopmund</field>
        <field name="email">logistics@husabmine.com</field>
        <field name="phone">+264 64 410 9000</field>
    </record>

    <record id="partner_b2gold" model="res.partner">
        <field name="name">B2Gold Otjikoto Mine</field>
        <field name="is_company">True</field>
        <field name="street">B1 Highway 70km North of Otjiwarongo</field>
        <field name="city">Otjiwarongo</field>
        <field name="email">fuel.orders@b2gold.com</field>
        <field name="phone">+264 67 300 100</field>
    </record>

    <record id="partner_petrosol_retail" model="res.partner">
        <field name="name">Petrosol Outjo Service Station</field>
        <field name="is_company">True</field>
        <field name="street">C38 Etosha Route, Hage Geingob St</field>
        <field name="city">Outjo</field>
        <field name="email">outjo@petrosol.com.na</field>
        <field name="phone">+264 67 313 000</field>
    </record>

    <record id="partner_namdeb" model="res.partner">
        <field name="name">Namdeb Diamond Corporation</field>
        <field name="is_company">True</field>
        <field name="street">Mining Area 1</field>
        <field name="city">Oranjemund</field>
    </record>

    <record id="partner_dune7" model="res.partner">
        <field name="name">Dune 7 Road Construction JV</field>
        <field name="is_company">True</field>
        <field name="city">Walvis Bay</field>
    </record>

    <!-- Spare Parts Suppliers (from Workshop Projects) -->
    <record id="partner_mb_truck" model="res.partner">
        <field name="name">Mercedes-Benz Commercial Vehicles Namibia</field>
        <field name="is_company">True</field>
        <field name="city">Windhoek</field>
        <field name="phone">+264 61 280 4000</field>
    </record>

    <record id="partner_nors" model="res.partner">
        <field name="name">NORS Group / Volvo Trucks Namibia</field>
        <field name="is_company">True</field>
        <field name="city">Windhoek</field>
        <field name="phone">+264 61 380 500</field>
    </record>

    <record id="partner_master_parts" model="res.partner">
        <field name="name">Master Parts Otjiwarongo</field>
        <field name="is_company">True</field>
        <field name="city">Otjiwarongo</field>
        <field name="phone">+264 67 304 888</field>
    </record>

    <record id="partner_henred" model="res.partner">
        <field name="name">Henred Fruehauf Namibia (Trailers &amp; Axles)</field>
        <field name="is_company">True</field>
        <field name="city">Windhoek</field>
        <field name="phone">+264 61 261 327</field>
    </record>

    <record id="partner_indongo_toyota" model="res.partner">
        <field name="name">Indongo Toyota Otjiwarongo</field>
        <field name="is_company">True</field>
        <field name="city">Otjiwarongo</field>
        <field name="phone">+264 67 302 555</field>
    </record>

    <record id="partner_cymot" model="res.partner">
        <field name="name">Cymot Automotive Otjiwarongo</field>
        <field name="is_company">True</field>
        <field name="city">Otjiwarongo</field>
        <field name="phone">+264 67 302 333</field>
    </record>

    <record id="partner_smart_fuels" model="res.partner">
        <field name="name">Smart Fuels Namibia (Pty) Ltd</field>
        <field name="is_company">True</field>
        <field name="city">Windhoek</field>
        <field name="phone">081 660 1220</field>
        <field name="email">joos@fuelis.co.za</field>
    </record>
''')

    # Breakdown Network Partners
    for bp in breakdown_partners:
        out.append(f'    <record id="{bp["xml_id"]}" model="res.partner">')
        out.append(f'        <field name="name">{xml_escape(bp["name"])}</field>')
        out.append(f'        <field name="is_company">True</field>')
        out.append(f'        <field name="city">{xml_escape(bp["town"])}</field>')
        out.append(f'        <field name="phone">{xml_escape(bp["phone"])}</field>')
        if bp["email"]: out.append(f'        <field name="email">{xml_escape(bp["email"])}</field>')
        out.append(f'        <field name="x_is_breakdown_partner">True</field>')
        out.append(f'        <field name="x_breakdown_coverage_area">{xml_escape(bp["town"])}</field>')
        out.append(f'        <field name="x_breakdown_service_type">{bp["service_type"]}</field>')
        out.append('    </record>')

    out.append('''
    <!-- Legacy Customers & Sites (b84fb91 compatibility) -->
    <record id="partner_b2gold_mine" model="res.partner">
        <field name="name">B2Gold Otjikoto Gold Mine</field>
        <field name="is_company">True</field>
        <field name="street">B1 Highway 70km North of Otjiwarongo</field>
        <field name="city">Otjiwarongo</field>
        <field name="email">procurement@b2gold.com</field>
        <field name="phone">+264 67 300 100</field>
    </record>

    <record id="partner_grinaker_lta" model="res.partner">
        <field name="name">Grinaker-LTA Road Construction JV</field>
        <field name="is_company">True</field>
        <field name="street">MR101 Trunk Road Project Camp</field>
        <field name="city">Outjo</field>
        <field name="email">supplies@grinaker-namibia.com</field>
        <field name="phone">+264 67 313 500</field>
    </record>

    <record id="partner_petrosol_outjo" model="res.partner">
        <field name="name">Petrosol Retail - Outjo 24hr Service Station</field>
        <field name="is_company">True</field>
        <field name="street">C38 Etosha Gateway Highway</field>
        <field name="city">Outjo</field>
        <field name="email">outjo.station@petrosol.com.na</field>
        <field name="phone">+264 67 313 010</field>
    </record>

    <record id="partner_petrosol_khorixas" model="res.partner">
        <field name="name">Petrosol Retail - Khorixas Service Station &amp; ILAMO Express</field>
        <field name="is_company">True</field>
        <field name="street">C39 Damaraland Main Road</field>
        <field name="city">Khorixas</field>
        <field name="email">khorixas.station@petrosol.com.na</field>
        <field name="phone">+264 67 331 020</field>
    </record>

    <!-- ============================================================== -->
    <!-- 5. EMPLOYEES: OPERATIONS, HSE, MECHANICS & 34 DRIVERS          -->
    <!-- ============================================================== -->
    <record id="employee_johan_botes" model="hr.employee">
        <field name="name">Johan Botes</field>
        <field name="job_title">Chief Operating Officer / Logistics Director</field>
        <field name="work_phone">+264 81 124 5001</field>
        <field name="work_email">johan@nfd.com.na</field>
        <field name="x_aa_category">general</field>
    </record>

    <record id="employee_pierre_fourie" model="hr.employee">
        <field name="name">Pierre Fourie</field>
        <field name="job_title">HESMS Safety &amp; Depot Compliance Manager</field>
        <field name="work_phone">+264 81 128 7744</field>
        <field name="work_email">safety@nfd.com.na</field>
        <field name="x_aa_category">general</field>
    </record>

    <record id="employee_hendrik_shilongo" model="hr.employee">
        <field name="name">Hendrik Shilongo</field>
        <field name="job_title">Senior Master Tanker Driver (Hazchem Level 1)</field>
        <field name="work_phone">+264 81 334 1120</field>
        <field name="x_aa_category">designated_namibian</field>
        <field name="x_hazchem_expiry">2027-10-15</field>
        <field name="x_defensive_driving_expiry">2027-04-10</field>
        <field name="x_medical_fitness_expiry">2027-06-20</field>
        <field name="x_licence_code">CE</field>
    </record>

    <record id="employee_lukas_van_wyk" model="hr.employee">
        <field name="name">Lukas van Wyk</field>
        <field name="job_title">Senior Petroleum Installation Technician</field>
        <field name="work_phone">+264 81 445 8899</field>
        <field name="x_aa_category">designated_namibian</field>
    </record>

    <record id="employee_laythonne" model="hr.employee">
        <field name="name">Laythonne Oubaas</field>
        <field name="job_title">Heavy Haulage Tanker Driver</field>
        <field name="x_aa_category">designated_namibian</field>
        <field name="x_licence_code">CE</field>
        <field name="x_hazchem_expiry">2027-09-15</field>
        <field name="x_medical_fitness_expiry">2027-08-20</field>
    </record>

    <record id="employee_lucas" model="hr.employee">
        <field name="name">Lucas Shikongo</field>
        <field name="job_title">Fleet Logistics Coordinator</field>
        <field name="x_aa_category">designated_namibian</field>
        <field name="x_licence_code">B</field>
    </record>

    <!-- Workshop Mechanics (from PROJECTS sheet) -->
    <record id="employee_green" model="hr.employee">
        <field name="name">Green Mechanic</field>
        <field name="job_title">Workshop Master Mechanic</field>
        <field name="x_aa_category">designated_namibian</field>
    </record>

    <record id="employee_japie" model="hr.employee">
        <field name="name">Japie Avis</field>
        <field name="job_title">Tanker Re-Build Specialist</field>
        <field name="x_aa_category">designated_namibian</field>
        <field name="x_licence_code">CE</field>
    </record>

    <record id="employee_clive" model="hr.employee">
        <field name="name">Clive Workshop</field>
        <field name="job_title">Air Brakes &amp; Pneumatics Mechanic</field>
        <field name="x_aa_category">designated_namibian</field>
    </record>

    <record id="employee_jonie" model="hr.employee">
        <field name="name">Jonie Useb</field>
        <field name="job_title">Auto Electrician &amp; Diagnostic Specialist</field>
        <field name="x_aa_category">designated_namibian</field>
        <field name="x_licence_code">BE</field>
    </record>

    <record id="employee_siisii" model="hr.employee">
        <field name="name">Siisii Suspension</field>
        <field name="job_title">Laser Wheel Alignment Specialist</field>
        <field name="x_aa_category">designated_namibian</field>
    </record>

    <record id="employee_manie" model="hr.employee">
        <field name="name">Manie Foreman</field>
        <field name="job_title">Otjiwarongo Workshop Foreman</field>
        <field name="x_aa_category">general</field>
    </record>
''')

    for d in drivers:
        out.append(f'    <record id="{d["xml_id"]}" model="hr.employee">')
        out.append(f'        <field name="name">{xml_escape(d["name"])}</field>')
        out.append(f'        <field name="job_title">Hazchem Tanker Driver</field>')
        out.append(f'        <field name="work_phone">{xml_escape(d["phone"])}</field>')
        if d["id_num"]: out.append(f'        <field name="x_id_number">{xml_escape(d["id_num"])}</field>')
        out.append(f'        <field name="x_licence_code">{d["code"]}</field>')
        if d["lic_exp"]: out.append(f'        <field name="x_licence_expiry_date">{d["lic_exp"]}</field>')
        if d["pdp_exp"]: out.append(f'        <field name="x_pdp_expiry_date">{d["pdp_exp"]}</field>')
        if d["med_exp"]: out.append(f'        <field name="x_medical_fitness_expiry">{d["med_exp"]}</field>')
        if d["haz_exp"]: out.append(f'        <field name="x_hazchem_expiry">{d["haz_exp"]}</field>')
        if d["eye_exp"]: out.append(f'        <field name="x_eye_test_expiry_date">{d["eye_exp"]}</field>')
        out.append(f'        <field name="x_defensive_driving_expiry">2027-08-30</field>')
        out.append(f'        <field name="x_aa_category">designated_namibian</field>')
        out.append('    </record>')

    out.append('''
    <record id="employee_oscar" model="hr.employee">
        <field name="name">Oscar Haulage</field>
        <field name="job_title">Fuel Transport Driver</field>
        <field name="work_phone">+264 81 501 0012</field>
        <field name="x_aa_category">designated_namibian</field>
        <field name="x_hazchem_expiry">2027-08-08</field>
        <field name="x_defensive_driving_expiry">2027-07-01</field>
        <field name="x_medical_fitness_expiry">2027-05-15</field>
        <field name="x_licence_code">CE</field>
    </record>

    <!-- ============================================================== -->
    <!-- 6. TANKER TRAILERS, LINKS & COMPARTMENTS (FLEET SERVICE)       -->
    <!-- ============================================================== -->
''')
    for t in trailers:
        out.append(f'    <record id="{t["xml_id"]}" model="fleet.vehicle">')
        out.append(f'        <field name="model_id" ref="{t["model_ref"]}"/>')
        out.append(f'        <field name="license_plate">{t["plate"]}</field>')
        out.append(f'        <field name="x_unit_classification">{t["classification"]}</field>')
        out.append(f'        <field name="x_max_volume_liters">{t["max_vol"]}</field>')
        out.append(f'        <field name="x_diesel_capacity">{t["diesel"]}</field>')
        out.append(f'        <field name="x_ulp_capacity">{t["ulp"]}</field>')
        out.append(f'        <field name="x_compartment_count">4</field>')
        out.append(f'        <field name="x_has_diesel_meter" eval="{str(t["has_meter"])}"/>')
        out.append(f'        <field name="x_manufacture_year">{t["mfg_year"]}</field>')
        out.append(f'        <field name="x_service_interval_km">{t["interval"]}</field>')
        out.append(f'        <field name="x_operational_availability">{t["availability"]}</field>')
        if t["last_srv"]: out.append(f'        <field name="x_last_service_date">{t["last_srv"]}</field>')
        if t["lic_exp"]: out.append(f'        <field name="x_licence_expiry_date">{t["lic_exp"]}</field>')
        if t["fit_exp"]: out.append(f'        <field name="x_fitness_certificate_expiry">{t["fit_exp"]}</field>')
        if t["slp_exp"]: out.append(f'        <field name="x_safe_loading_pass_expiry">{t["slp_exp"]}</field>')
        if t["press_exp"]: out.append(f'        <field name="x_pressure_test_expiry">{t["press_exp"]}</field>')
        if t["wheel_date"]: out.append(f'        <field name="x_last_wheel_alignment_date">{t["wheel_date"]}</field>')
        out.append(f'        <field name="x_pto_type">{t["pto_type"]}</field>')
        if t["pto_location"]: out.append(f'        <field name="x_pto_location">{xml_escape(t["pto_location"])}</field>')
        out.append('    </record>')

    # 7. Power Units & Rigids
    out.append('''
    <!-- ============================================================== -->
    <!-- 7. POWER UNITS, RIGIDS & SUPPORT FLEET (FLEET SERVICE)        -->
    <!-- ============================================================== -->
''')
    for v in vehicles:
        out.append(f'    <record id="{v["xml_id"]}" model="fleet.vehicle">')
        out.append(f'        <field name="model_id" ref="{v["model_ref"]}"/>')
        out.append(f'        <field name="license_plate">{v["plate"]}</field>')
        out.append(f'        <field name="x_unit_classification">{v["classification"]}</field>')
        out.append(f'        <field name="x_max_volume_liters">{v["max_vol"]}</field>')
        out.append(f'        <field name="x_diesel_capacity">{v["diesel"]}</field>')
        out.append(f'        <field name="x_ulp_capacity">{v["ulp"]}</field>')
        out.append(f'        <field name="x_compartment_count">4</field>')
        out.append(f'        <field name="x_has_diesel_meter" eval="{str(v["has_meter"])}"/>')
        out.append(f'        <field name="x_geotab_device_id">GEO-{v["reg"]}</field>')
        out.append(f'        <field name="x_manufacture_year">{v["mfg_year"]}</field>')
        out.append(f'        <field name="odometer">{v["odometer"]}</field>')
        out.append(f'        <field name="x_last_service_km">{v["last_km"]}</field>')
        out.append(f'        <field name="x_service_interval_km">{v["interval"]}</field>')
        out.append(f'        <field name="x_next_service_km">{v["next_km"]}</field>')
        out.append(f'        <field name="x_km_until_service">{v["remaining_km"]}</field>')
        out.append(f'        <field name="x_service_status">{v["service_status"]}</field>')
        out.append(f'        <field name="x_operational_availability">{v["availability"]}</field>')
        if v["last_srv"]: out.append(f'        <field name="x_last_service_date">{v["last_srv"]}</field>')
        if v["lic_exp"]: out.append(f'        <field name="x_licence_expiry_date">{v["lic_exp"]}</field>')
        if v["fit_exp"]: out.append(f'        <field name="x_fitness_certificate_expiry">{v["fit_exp"]}</field>')
        if v["slp_exp"]: out.append(f'        <field name="x_safe_loading_pass_expiry">{v["slp_exp"]}</field>')
        if v["press_exp"]: out.append(f'        <field name="x_pressure_test_expiry">{v["press_exp"]}</field>')
        if v["wheel_date"]: out.append(f'        <field name="x_last_wheel_alignment_date">{v["wheel_date"]}</field>')
        out.append(f'        <field name="x_pto_type">{v["pto_type"]}</field>')
        if v["pto_location"]: out.append(f'        <field name="x_pto_location">{xml_escape(v["pto_location"])}</field>')
        if v["driver_ref"]: out.append(f'        <field name="driver_employee_id" ref="{v["driver_ref"]}"/>')
        if v["c1_ref"]: out.append(f'        <field name="x_trailer_comp1_id" ref="{v["c1_ref"]}"/>')
        if v["c2_ref"]: out.append(f'        <field name="x_trailer_comp2_id" ref="{v["c2_ref"]}"/>')
        
        # September 2026 fuel consumption metrics if available
        if v["sept"]:
            s = v["sept"]
            out.append(f'        <field name="x_expected_km_per_liter">{s["km_l"]}</field>')
            out.append(f'        <field name="x_actual_km_per_liter">{s["act_km_l"]}</field>')
            out.append(f'        <field name="x_sept_distance_km">{s["km"]}</field>')
            out.append(f'        <field name="x_sept_expected_fuel_l">{s["exp_fuel"]}</field>')
            out.append(f'        <field name="x_sept_actual_fuel_l">{s["act_fuel"]}</field>')
            out.append(f'        <field name="x_sept_excess_fuel_l">{s["excess"]}</field>')
            out.append(f'        <field name="x_otj_coc_fuel_price">25.98</field>')
            out.append(f'        <field name="x_sept_excess_nad_value">{s["nad"]}</field>')
        out.append('    </record>')

    out.append('''
    <!-- Legacy Demo Fleet Power Units (b84fb91 compatibility) -->
    <record id="vehicle_scania_r500" model="fleet.vehicle">
        <field name="model_id" ref="model_scania_r500"/>
        <field name="license_plate">N 4201 OT</field>
        <field name="x_unit_classification">prime_mover</field>
        <field name="x_max_volume_liters">42000.0</field>
        <field name="x_compartment_count">6</field>
        <field name="x_has_diesel_meter" eval="True"/>
        <field name="x_geotab_device_id">GT-NFD-01</field>
        <field name="x_manufacture_year">2021</field>
    </record>

    <record id="vehicle_actros_2645" model="fleet.vehicle">
        <field name="model_id" ref="model_actros_2645"/>
        <field name="license_plate">N 4202 OT</field>
        <field name="x_unit_classification">prime_mover</field>
        <field name="x_max_volume_liters">42000.0</field>
        <field name="x_compartment_count">7</field>
        <field name="x_has_diesel_meter" eval="False"/>
        <field name="x_geotab_device_id">GT-NFD-02</field>
        <field name="x_manufacture_year">2019</field>
    </record>

    <record id="vehicle_argosy" model="fleet.vehicle">
        <field name="model_id" ref="model_argosy"/>
        <field name="license_plate">N 1809 OT</field>
        <field name="x_unit_classification">prime_mover</field>
        <field name="x_max_volume_liters">36000.0</field>
        <field name="x_compartment_count">6</field>
        <field name="x_has_diesel_meter" eval="False"/>
        <field name="x_geotab_device_id">GT-NFD-03</field>
        <field name="x_manufacture_year">2008</field>
    </record>

    <record id="vehicle_axor_rigid" model="fleet.vehicle">
        <field name="model_id" ref="model_axor_rigid"/>
        <field name="license_plate">N 1750 OT</field>
        <field name="x_unit_classification">rigid_tanker</field>
        <field name="x_max_volume_liters">17500.0</field>
        <field name="x_compartment_count">4</field>
        <field name="x_has_diesel_meter" eval="True"/>
        <field name="x_geotab_device_id">GT-NFD-14</field>
        <field name="x_manufacture_year">2017</field>
    </record>

    <record id="vehicle_scania_rigid" model="fleet.vehicle">
        <field name="model_id" ref="model_scania_p360"/>
        <field name="license_plate">N 1601 OT</field>
        <field name="x_unit_classification">rigid_tanker</field>
        <field name="x_max_volume_liters">16000.0</field>
        <field name="x_compartment_count">4</field>
        <field name="x_has_diesel_meter" eval="True"/>
        <field name="x_geotab_device_id">GT-NFD-15</field>
        <field name="x_manufacture_year">2014</field>
    </record>

    <!-- ============================================================== -->
    <!-- 8. MAINTENANCE TEAMS, CATEGORIES & EQUIPMENT                  -->
    <!-- ============================================================== -->
    <record id="maintenance_team_otjiwarongo" model="maintenance.team">
        <field name="name">Otjiwarongo Mechanical Workshop</field>
    </record>

    
    <!-- Legacy Equipment Categories & Assets (b84fb91 compatibility) -->
    <record id="maintenance_cat_fleet_truck" model="maintenance.equipment.category">
        <field name="name">Bulk Fuel Fleet (Prime Movers &amp; Tankers)</field>
    </record>
    <record id="maintenance_cat_forecourt" model="maintenance.equipment.category">
        <field name="name">Retail Forecourt Equipment (Dispensers &amp; ATG)</field>
    </record>
    <record id="maintenance_cat_bulk_tank" model="maintenance.equipment.category">
        <field name="name">Bulk Depot &amp; Mine Client Storage Tanks</field>
    </record>

    <record id="equipment_scania_r500" model="maintenance.equipment">
        <field name="name">Scania R500 (N 4201 OT) - Powertrain &amp; Meter</field>
        <field name="category_id" ref="maintenance_cat_fleet_truck"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_scania_r500"/>
    </record>

    <record id="equipment_axor_rigid" model="maintenance.equipment">
        <field name="name">Mercedes Axor 17,500L (N 1750 OT) - Manifold &amp; Meter</field>
        <field name="category_id" ref="maintenance_cat_fleet_truck"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_axor_rigid"/>
    </record>

    <record id="equipment_petrosol_outjo_pump" model="maintenance.equipment">
        <field name="name">Petrosol Outjo - Wayne Helix 4-Nozzle Dispenser MPD-1</field>
        <field name="category_id" ref="maintenance_cat_forecourt"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">petrosol_forecourt_pump</field>
        <field name="x_site_partner_id" ref="partner_petrosol_outjo"/>
    </record>

    <record id="equipment_husab_tank" model="maintenance.equipment">
        <field name="name">Husab Mine Bulk Storage Tank T-01 (100,000L)</field>
        <field name="category_id" ref="maintenance_cat_bulk_tank"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">customer_bulk_tank</field>
        <field name="x_site_partner_id" ref="partner_husab_mine"/>
        <field name="x_tank_capacity_liters">100000.0</field>
    </record>

    <record id="equipment_depot_gantry" model="maintenance.equipment">
        <field name="name">Otjiwarongo Depot Loading Bay 1 - Bottom Loading Gantry</field>
        <field name="category_id" ref="maintenance_cat_bulk_tank"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">depot_gantry</field>
        <field name="x_tank_capacity_liters">500000.0</field>
    </record>

    <record id="cat_fleet_trucks" model="maintenance.equipment.category">
        <field name="name">Heavy Bulk Fuel Tankers &amp; Rigids</field>
    </record>

    <record id="cat_depot_installations" model="maintenance.equipment.category">
        <field name="name">Bulk Fuel Depot Gantries &amp; Tanks</field>
    </record>

    <record id="cat_retail_forecourt" model="maintenance.equipment.category">
        <field name="name">Petrosol Retail Forecourt Dispensers</field>
    </record>

    <record id="equipment_depot_gantry_bay1" model="maintenance.equipment">
        <field name="name">Otjiwarongo Depot Loading Bay 1 - Bottom Loading Gantry</field>
        <field name="category_id" ref="cat_depot_installations"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">depot_gantry</field>
        <field name="x_tank_capacity_liters">500000.0</field>
    </record>

    <record id="equipment_depot_gantry_bay2" model="maintenance.equipment">
        <field name="name">Otjiwarongo Depot Loading Bay 2 - Top/Bottom Dual Arm</field>
        <field name="category_id" ref="cat_depot_installations"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">depot_gantry</field>
        <field name="x_tank_capacity_liters">200000.0</field>
    </record>

    <record id="equipment_husab_tank1" model="maintenance.equipment">
        <field name="name">Husab Mine Bulk Storage Tank 1 (Diesel 50ppm)</field>
        <field name="category_id" ref="cat_depot_installations"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">customer_bulk_tank</field>
        <field name="x_site_partner_id" ref="partner_husab_mine"/>
        <field name="x_tank_capacity_liters">100000.0</field>
    </record>

    <record id="equipment_b2gold_tank1" model="maintenance.equipment">
        <field name="name">B2Gold Otjikoto Mine Tank 1 (Heavy Haul Diesel)</field>
        <field name="category_id" ref="cat_depot_installations"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">customer_bulk_tank</field>
        <field name="x_site_partner_id" ref="partner_b2gold"/>
        <field name="x_tank_capacity_liters">65000.0</field>
    </record>

    <record id="equipment_petrosol_pump1" model="maintenance.equipment">
        <field name="name">Petrosol Outjo Wayne Helix MPD Pump #1 (Diesel/ULP)</field>
        <field name="category_id" ref="cat_retail_forecourt"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">petrosol_forecourt_pump</field>
        <field name="x_site_partner_id" ref="partner_petrosol_retail"/>
    </record>

    <!-- Equipment linked to key demo vehicles -->
    <record id="equipment_vehicle_n7802ot" model="maintenance.equipment">
        <field name="name">Mercedes Actros 2646 (N 7802 OT) - Chassis &amp; Tank</field>
        <field name="category_id" ref="cat_fleet_trucks"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_n7802ot"/>
    </record>

    <record id="equipment_vehicle_n317ot" model="maintenance.equipment">
        <field name="name">Mercedes V-Series 407T 16,000L Rigid (N 317 OT)</field>
        <field name="category_id" ref="cat_fleet_trucks"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_n317ot"/>
    </record>

    <record id="equipment_vehicle_n12043ot" model="maintenance.equipment">
        <field name="name">Volvo FH520 Long-Haul Tanker (N 12043 OT)</field>
        <field name="category_id" ref="cat_fleet_trucks"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_n12043ot"/>
    </record>

    <record id="equipment_vehicle_n8966ot" model="maintenance.equipment">
        <field name="name">Mercedes Actros 2652 Bulk Tanker (N 8966 OT)</field>
        <field name="category_id" ref="cat_fleet_trucks"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_n8966ot"/>
    </record>

    <record id="equipment_vehicle_n12548ot" model="maintenance.equipment">
        <field name="name">Mercedes Axor Rigid Tanker (N 12548 OT)</field>
        <field name="category_id" ref="cat_fleet_trucks"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="x_asset_category">fleet_truck</field>
        <field name="x_linked_vehicle_id" ref="vehicle_n12548ot"/>
    </record>
''')

    # 9. Maintenance Requests (Real Job Cards from PROJECTS sheet)
    out.append('''
    <!-- ============================================================== -->
    <!-- 9. MAINTENANCE REQUESTS (WORKSHOP JOB CARDS)                  -->
    <!-- ============================================================== -->
    <record id="req_jc_1009" model="maintenance.request">
        <field name="name">JC-1009: Trek Links &amp; Turntable Pin Re-Torque</field>
        <field name="equipment_id" ref="equipment_vehicle_n12548ot"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="user_id" ref="base.user_admin"/>
        <field name="maintenance_type">corrective</field>
        <field name="x_job_card_number">JC-1009</field>
        <field name="x_workshop_location">workshop_otj</field>
        <field name="x_assigned_mechanic">green</field>
        <field name="x_job_type">repair</field>
        <field name="x_parts_supplier_id" ref="partner_henred"/>
        <field name="x_parts_ordered">True</field>
        <field name="x_parts_received">True</field>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">Workshop Job Card 1009: Disassemble B-double link turntable, replace kingpin locking jaw bushes, and torque mounting bolts.</field>
    </record>

    <record id="req_jc_1045" model="maintenance.request">
        <field name="name">JC-1045: Multi-Compartment Degas &amp; Internal Baffle Weld</field>
        <field name="equipment_id" ref="equipment_vehicle_n12043ot"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="user_id" ref="base.user_admin"/>
        <field name="maintenance_type">corrective</field>
        <field name="x_job_card_number">JC-1045</field>
        <field name="x_workshop_location">cwwa</field>
        <field name="x_assigned_mechanic">japie</field>
        <field name="x_job_type">degas</field>
        <field name="x_parts_supplier_id" ref="partner_smart_fuels"/>
        <field name="x_parts_ordered">True</field>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">Workshop Job Card 1045: Degas compartments 5, 6 &amp; 7 share, certify gas-free entry, and repair cracked internal baffle weld.</field>
    </record>

    <record id="req_jc_1110" model="maintenance.request">
        <field name="name">JC-1110: Hydraulic PTO Offloading Valve Leak Repair</field>
        <field name="equipment_id" ref="equipment_vehicle_n8966ot"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="user_id" ref="base.user_admin"/>
        <field name="maintenance_type">corrective</field>
        <field name="x_job_card_number">JC-1110</field>
        <field name="x_workshop_location">workshop_otj</field>
        <field name="x_assigned_mechanic">clive</field>
        <field name="x_job_type">repair</field>
        <field name="x_parts_supplier_id" ref="partner_mb_truck"/>
        <field name="x_parts_ordered">True</field>
        <field name="x_parts_received">True</field>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">Job Card 1110: Replace leaking hydraulic seal on auxiliary discharge pump, bleed hydraulic lines, and pressure-test offload manifold.</field>
    </record>

    <record id="req_jc_994" model="maintenance.request">
        <field name="name">JC-994: NaTIS Statutory Roadworthy Fitness Retest</field>
        <field name="equipment_id" ref="equipment_vehicle_n317ot"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="user_id" ref="base.user_admin"/>
        <field name="maintenance_type">preventive</field>
        <field name="x_job_card_number">JC-994</field>
        <field name="x_workshop_location">natis_otj</field>
        <field name="x_assigned_mechanic">manie</field>
        <field name="x_job_type">roadworthy</field>
        <field name="x_parts_supplier_id" ref="partner_indongo_toyota"/>
        <field name="x_parts_ordered">True</field>
        <field name="x_parts_received">True</field>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">Job Card 994: Present unit 317 at Natis OTJ for statutory fitness certificate renewal. Roller brake test and kingpin play check passed.</field>
    </record>

    <record id="req_jc_1088" model="maintenance.request">
        <field name="name">JC-1088: Safe Loading Pass (SLP) Recertification</field>
        <field name="equipment_id" ref="equipment_vehicle_n7802ot"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="user_id" ref="base.user_admin"/>
        <field name="maintenance_type">preventive</field>
        <field name="x_job_card_number">JC-1088</field>
        <field name="x_workshop_location">vivo_depo</field>
        <field name="x_assigned_mechanic">jonie</field>
        <field name="x_job_type">service</field>
        <field name="x_parts_supplier_id" ref="partner_nors"/>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">Job Card 1088: Gantry bottom-loading optical overfill sensor probe test and earth pin validation at Vivo Depo. SLP disk issued.</field>
    </record>

    <record id="req_petrosol_pump_calibration" model="maintenance.request">
        <field name="name">Petrosol Outjo Forecourt Pump Meter Recalibration</field>
        <field name="equipment_id" ref="equipment_petrosol_pump1"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="maintenance_type">preventive</field>
        <field name="x_service_agreement_type">free_retail_forecourt</field>
        <field name="x_site_partner_id" ref="partner_petrosol_retail"/>
        <field name="description">Subsidized dealer support: Annual flow meter accuracy verification using 20L proving can.</field>
    </record>

    <!-- Legacy Maintenance Requests (b84fb91 compatibility) -->
    <record id="req_scania_pm" model="maintenance.request">
        <field name="name">50,000km Preventive Chassis &amp; Manifold Service - Scania R500 (N 4201 OT)</field>
        <field name="equipment_id" ref="equipment_scania_r500"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="maintenance_type">preventive</field>
        <field name="priority">2</field>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">Routine 50,000km service for high-utilization mining haulage tractor.</field>
    </record>

    <record id="req_petrosol_outjo" model="maintenance.request">
        <field name="name">Monthly Dispenser Nozzle &amp; Meter Recalibration - Petrosol Outjo</field>
        <field name="equipment_id" ref="equipment_petrosol_outjo_pump"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="maintenance_type">preventive</field>
        <field name="priority">1</field>
        <field name="x_service_agreement_type">free_retail_forecourt</field>
        <field name="x_site_partner_id" ref="partner_petrosol_outjo"/>
        <field name="description">Subsidized dealer support: Annual flow meter accuracy verification using 20L proving can.</field>
    </record>

    <record id="req_husab_tank" model="maintenance.request">
        <field name="name">Semi-Annual Inspection &amp; Water Drain Check - Husab Mine Tank T-01</field>
        <field name="equipment_id" ref="equipment_husab_tank"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="maintenance_type">preventive</field>
        <field name="priority">2</field>
        <field name="x_service_agreement_type">customer_contract</field>
        <field name="x_site_partner_id" ref="partner_husab_mine"/>
        <field name="description">Mining contract compliance check: Sump water drain, ATG sensor calibration, overfill protection.</field>
    </record>

    <record id="req_axor_leakage" model="maintenance.request">
        <field name="name">URGENT: Inspect Tanker Manifold/Delivery Meter for Fuel Leakage - Mercedes-Benz Axor (DISP/2026/0102)</field>
        <field name="equipment_id" ref="equipment_axor_rigid"/>
        <field name="maintenance_team_id" ref="maintenance_team_otjiwarongo"/>
        <field name="maintenance_type">corrective</field>
        <field name="priority">3</field>
        <field name="x_service_agreement_type">internal_fleet</field>
        <field name="description">AUTOMATED LEAKAGE ALERT TRIGGERED: Net Discrepancy: 163.75 L (Exceeds 50L Safety Limit)</field>
    </record>

    <!-- ============================================================== -->
    <!-- 10. CARGO FUEL DISPATCH & LEAKAGE LOGS                        -->
    <!-- ============================================================== -->
    <record id="dispatch_log_001" model="nfd.fuel.dispatch.log">
        <field name="name">DISP/2026/0101</field>
        <field name="date">2026-09-02 06:30:00</field>
        <field name="vehicle_id" ref="vehicle_n7802ot"/>
        <field name="driver_id" ref="employee_mike"/>
        <field name="customer_id" ref="partner_b2gold"/>
        <field name="fuel_product_id" ref="product_diesel_50ppm"/>
        <field name="source_location_id" ref="location_depot_diesel_tank1"/>
        <field name="destination_location_id" ref="location_b2gold_mine"/>
        <field name="depot_loaded_liters">42000.0</field>
        <field name="truck_meter_delivered_liters">41895.0</field>
        <field name="customer_dip_received_liters">41890.0</field>
        <field name="temp_allowance_liters">105.0</field>
        <field name="net_variance_liters">0.0</field>
        <field name="leakage_status">normal</field>
        <field name="compartment_seal_numbers">NFD-SEAL-8891 to 8897</field>
        <field name="pre_trip_hse_passed">True</field>
        <field name="state">delivered</field>
        <field name="notes">Standard supply haulage to B2Gold Otjikoto Mine bulk tanks. Discrepancy within 0.25% thermal allowance.</field>
    </record>

    <record id="dispatch_log_002" model="nfd.fuel.dispatch.log">
        <field name="name">DISP/2026/0102</field>
        <field name="date">2026-09-04 07:15:00</field>
        <field name="vehicle_id" ref="vehicle_n12916ot"/>
        <field name="driver_id" ref="employee_simon"/>
        <field name="customer_id" ref="partner_husab_mine"/>
        <field name="fuel_product_id" ref="product_diesel_50ppm"/>
        <field name="source_location_id" ref="location_depot_diesel_tank1"/>
        <field name="destination_location_id" ref="location_husab_mine"/>
        <field name="depot_loaded_liters">38500.0</field>
        <field name="truck_meter_delivered_liters">38240.0</field>
        <field name="customer_dip_received_liters">38235.0</field>
        <field name="temp_allowance_liters">96.25</field>
        <field name="net_variance_liters">163.75</field>
        <field name="leakage_status">leakage_alert</field>
        <field name="compartment_seal_numbers">NFD-SEAL-9012 to 9015</field>
        <field name="pre_trip_hse_passed">True</field>
        <field name="state">investigation</field>
        <field name="notes">AUDIT TALKING POINT: Discrepancy of 163.75L exceeds 0.25% threshold (96.25L allowance). Automatically triggers Maintenance ticket for valve manifold inspection.</field>
    </record>

    <!-- ============================================================== -->
    <!-- 11. REFUEL & ODOMETER LOGSHEETS (nfd.fuel.consumption.log)    -->
    <!-- ============================================================== -->
    <record id="fcl_log_001" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0001</field>
        <field name="date">2026-09-01</field>
        <field name="vehicle_id" ref="vehicle_n7802ot"/>
        <field name="driver_id" ref="employee_mike"/>
        <field name="place">Depot</field>
        <field name="odometer_start">494635.0</field>
        <field name="odometer_end">495514.0</field>
        <field name="distance_traveled_km">879.0</field>
        <field name="fuel_liters">437.0</field>
        <field name="expected_km_per_liter">2.3</field>
        <field name="actual_km_per_liter">2.01</field>
        <field name="fuel_usage_difference">-0.29</field>
        <field name="expected_fuel_liters">382.17</field>
        <field name="excess_use_liters">54.83</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">1424.48</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">excess_burn</field>
        <field name="notes">Heavy B-double load to coastal mining corridor. High ambient headwind.</field>
    </record>

    <record id="fcl_log_002" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0002</field>
        <field name="date">2026-09-02</field>
        <field name="vehicle_id" ref="vehicle_n7802ot"/>
        <field name="driver_id" ref="employee_mike"/>
        <field name="place">Depot</field>
        <field name="odometer_start">495514.0</field>
        <field name="odometer_end">496464.0</field>
        <field name="distance_traveled_km">950.0</field>
        <field name="fuel_liters">480.0</field>
        <field name="expected_km_per_liter">2.3</field>
        <field name="actual_km_per_liter">1.98</field>
        <field name="fuel_usage_difference">-0.32</field>
        <field name="expected_fuel_liters">413.04</field>
        <field name="excess_use_liters">66.96</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">1739.62</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">excess_burn</field>
        <field name="notes">Excess fuel burn logged. Fuel drawn at Otjiwarongo Depot gantry.</field>
    </record>

    <record id="fcl_log_003" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0003</field>
        <field name="date">2026-09-02</field>
        <field name="vehicle_id" ref="vehicle_n11751ot"/>
        <field name="driver_id" ref="employee_andreas_i"/>
        <field name="place">Depot</field>
        <field name="odometer_start">291886.0</field>
        <field name="odometer_end">292526.0</field>
        <field name="distance_traveled_km">640.0</field>
        <field name="fuel_liters">315.0</field>
        <field name="expected_km_per_liter">2.2</field>
        <field name="actual_km_per_liter">2.03</field>
        <field name="fuel_usage_difference">-0.17</field>
        <field name="expected_fuel_liters">290.91</field>
        <field name="excess_use_liters">24.09</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">625.86</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">excess_burn</field>
        <field name="notes">Rigid tanker regional multi-drop replenishment.</field>
    </record>

    <record id="fcl_log_004" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0004</field>
        <field name="date">2026-09-03</field>
        <field name="vehicle_id" ref="vehicle_n11963ot"/>
        <field name="driver_id" ref="employee_conrall"/>
        <field name="place">Depot</field>
        <field name="odometer_start">512040.0</field>
        <field name="odometer_end">513100.0</field>
        <field name="distance_traveled_km">1060.0</field>
        <field name="fuel_liters">465.0</field>
        <field name="expected_km_per_liter">2.4</field>
        <field name="actual_km_per_liter">2.28</field>
        <field name="fuel_usage_difference">-0.12</field>
        <field name="expected_fuel_liters">441.67</field>
        <field name="excess_use_liters">23.33</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">606.11</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">excess_burn</field>
        <field name="notes">B2Gold Otjikoto Mine round-trip.</field>
    </record>

    <record id="fcl_log_005" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0005</field>
        <field name="date">2026-09-01</field>
        <field name="vehicle_id" ref="vehicle_n10544ot"/>
        <field name="driver_id" ref="employee_matheus_shikongo"/>
        <field name="place">Depot</field>
        <field name="odometer_start">430110.0</field>
        <field name="odometer_end">431050.0</field>
        <field name="distance_traveled_km">940.0</field>
        <field name="fuel_liters">395.0</field>
        <field name="expected_km_per_liter">2.5</field>
        <field name="actual_km_per_liter">2.38</field>
        <field name="fuel_usage_difference">-0.12</field>
        <field name="expected_fuel_liters">376.0</field>
        <field name="excess_use_liters">19.0</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">493.62</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">excess_burn</field>
        <field name="notes">Volvo FH440 long-haul corridor haulage.</field>
    </record>

    <record id="fcl_log_006" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0006</field>
        <field name="date">2026-09-02</field>
        <field name="vehicle_id" ref="vehicle_n2745ot"/>
        <field name="driver_id" ref="employee_laythonne"/>
        <field name="place">Depot</field>
        <field name="odometer_start">182400.0</field>
        <field name="odometer_end">182543.0</field>
        <field name="distance_traveled_km">143.0</field>
        <field name="fuel_liters">450.0</field>
        <field name="expected_km_per_liter">2.1</field>
        <field name="actual_km_per_liter">0.32</field>
        <field name="fuel_usage_difference">-1.78</field>
        <field name="expected_fuel_liters">68.1</field>
        <field name="excess_use_liters">381.9</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">9921.76</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">excess_burn</field>
        <field name="notes">Heavy idling / depot yard shunting without road travel.</field>
    </record>

    <record id="fcl_log_007" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0007</field>
        <field name="date">2026-09-03</field>
        <field name="vehicle_id" ref="vehicle_n12916ot"/>
        <field name="driver_id" ref="employee_simon"/>
        <field name="place">Depot</field>
        <field name="odometer_start">388299.0</field>
        <field name="odometer_end">389719.0</field>
        <field name="distance_traveled_km">1420.0</field>
        <field name="fuel_liters">472.0</field>
        <field name="expected_km_per_liter">2.5</field>
        <field name="actual_km_per_liter">3.01</field>
        <field name="fuel_usage_difference">0.51</field>
        <field name="expected_fuel_liters">568.0</field>
        <field name="excess_use_liters">-96.0</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">-2494.08</field>
        <field name="confirm_logsheet">unconfirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">PUP Trailer long-haul run - Star Saver (-96L). Flagged in unconfirmed logsheet audit queue</field>
    </record>

    <record id="fcl_log_008" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0008</field>
        <field name="date">2026-09-05</field>
        <field name="vehicle_id" ref="vehicle_n12916ot"/>
        <field name="driver_id" ref="employee_simon"/>
        <field name="place">Depot</field>
        <field name="odometer_start">389719.0</field>
        <field name="odometer_end">390833.0</field>
        <field name="distance_traveled_km">1114.0</field>
        <field name="fuel_liters">334.0</field>
        <field name="expected_km_per_liter">2.5</field>
        <field name="actual_km_per_liter">3.34</field>
        <field name="fuel_usage_difference">0.84</field>
        <field name="expected_fuel_liters">445.6</field>
        <field name="excess_use_liters">-111.6</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">-2899.37</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">Walvis Bay Corridor import run - Outstanding 3.34 KM/L efficiency</field>
    </record>

    <record id="fcl_log_009" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0009</field>
        <field name="date">2026-09-05</field>
        <field name="vehicle_id" ref="vehicle_n10684ot"/>
        <field name="driver_id" ref="employee_oscar"/>
        <field name="place">Depot</field>
        <field name="odometer_start">640804.0</field>
        <field name="odometer_end">642810.0</field>
        <field name="distance_traveled_km">2006.0</field>
        <field name="fuel_liters">626.0</field>
        <field name="expected_km_per_liter">2.7</field>
        <field name="actual_km_per_liter">3.2</field>
        <field name="fuel_usage_difference">0.5</field>
        <field name="expected_fuel_liters">742.96</field>
        <field name="excess_use_liters">-116.96</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">-3038.62</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">Star Saver long haul - 2006 km corridor round-trip (-117L saved)</field>
    </record>

    <record id="fcl_log_010" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0010</field>
        <field name="date">2026-09-11</field>
        <field name="vehicle_id" ref="vehicle_n13938ot"/>
        <field name="driver_id" ref="employee_lucas"/>
        <field name="place">Office</field>
        <field name="odometer_start">30266.0</field>
        <field name="odometer_end">30266.0</field>
        <field name="distance_traveled_km">0.0</field>
        <field name="fuel_liters">67.73</field>
        <field name="expected_km_per_liter">10.0</field>
        <field name="actual_km_per_liter">0.0</field>
        <field name="fuel_usage_difference">-10.0</field>
        <field name="expected_fuel_liters">0.0</field>
        <field name="excess_use_liters">67.73</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">1759.63</field>
        <field name="confirm_logsheet">unconfirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">odo_error</field>
        <field name="notes">Excel formula error audit point: Missing End Odometer caused -30,266 KM in spreadsheet. Blocked by Odoo validation.</field>
    </record>

    <record id="fcl_log_011" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0011</field>
        <field name="date">2026-09-12</field>
        <field name="vehicle_id" ref="vehicle_n13938ot"/>
        <field name="driver_id" ref="employee_lucas"/>
        <field name="place">Office</field>
        <field name="odometer_start">30266.0</field>
        <field name="odometer_end">30896.0</field>
        <field name="distance_traveled_km">630.0</field>
        <field name="fuel_liters">61.5</field>
        <field name="expected_km_per_liter">10.0</field>
        <field name="actual_km_per_liter">10.24</field>
        <field name="fuel_usage_difference">0.24</field>
        <field name="expected_fuel_liters">63.0</field>
        <field name="excess_use_liters">-1.5</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">-38.97</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">Ford Tremor verified post-audit: 10.24 KM/L on Otjiwarongo management route</field>
    </record>

    <record id="fcl_log_012" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0012</field>
        <field name="date">2026-09-03</field>
        <field name="vehicle_id" ref="vehicle_n12611ot"/>
        <field name="driver_id" ref="employee_johan_botes"/>
        <field name="place">Office</field>
        <field name="odometer_start">113760.0</field>
        <field name="odometer_end">114354.0</field>
        <field name="distance_traveled_km">594.0</field>
        <field name="fuel_liters">65.06</field>
        <field name="expected_km_per_liter">9.5</field>
        <field name="actual_km_per_liter">9.13</field>
        <field name="fuel_usage_difference">-0.37</field>
        <field name="expected_fuel_liters">62.53</field>
        <field name="excess_use_liters">2.53</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">65.73</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">Isuzu 1.9 D-MAX - Omitted from Excel Summary tab, fully tracked in Odoo ERP</field>
    </record>

    <!-- ============================================================== -->
    <!-- 12. PROJECTS & TIMESHEETS                                      -->
    <!-- ============================================================== -->
    <record id="project_workshop" model="project.project">
        <field name="name">Otjiwarongo Mechanical Workshop &amp; Fleet Maintenance</field>
        <field name="privacy_visibility">employees</field>
        <field name="allow_timesheets">True</field>
        <field name="billing_type">not_billable</field>
    </record>

    <record id="project_petrosol" model="project.project">
        <field name="name">Petrosol Retail Forecourt Maintenance &amp; Subsidies</field>
        <field name="privacy_visibility">employees</field>
        <field name="partner_id" ref="partner_petrosol_retail"/>
        <field name="allow_timesheets">True</field>
        <field name="billing_type">not_billable</field>
    </record>

    <record id="project_haulage" model="project.project">
        <field name="name">NFD Long-Distance Fuel Haulage &amp; Import Logistics</field>
        <field name="privacy_visibility">employees</field>
        <field name="allow_timesheets">True</field>
        <field name="billing_type">not_billable</field>
    </record>

    <!-- Tasks -->
    <record id="task_workshop_7802_service" model="project.task">
        <field name="name">Service &amp; Calibration: Mercedes Actros N 7802 OT</field>
        <field name="project_id" ref="project_workshop"/>
    </record>

    <record id="task_workshop_meter_calibration" model="project.task">
        <field name="name">Monthly Recalibration of Depot Gantry Bulk Meters</field>
        <field name="project_id" ref="project_workshop"/>
    </record>

    <record id="task_petrosol_outjo_pump" model="project.task">
        <field name="name">Forecourt Pump Calibration &amp; Nozzle Check (Outjo)</field>
        <field name="project_id" ref="project_petrosol"/>
        <field name="partner_id" ref="partner_petrosol_retail"/>
    </record>

    <record id="task_haulage_walvis_import" model="project.task">
        <field name="name">Walvis Bay Harbor Port to Otjiwarongo Tank Farm Inbound Haulage</field>
        <field name="project_id" ref="project_haulage"/>
    </record>

    <record id="task_haulage_b2gold" model="project.task">
        <field name="name">B2Gold Otjikoto Mine Daily Bulk Diesel Haulage</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="partner_id" ref="partner_b2gold"/>
    </record>

    <record id="task_haulage_husab" model="project.task">
        <field name="name">Husab Mine Bulk Diesel Haulage Corridor</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="partner_id" ref="partner_husab_mine"/>
    </record>

    <!-- Timesheets -->
    
    <record id="fcl_log_013" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0013</field>
        <field name="date">2026-09-14</field>
        <field name="vehicle_id" ref="vehicle_n13831ot"/>
        <field name="driver_id" ref="employee_lucas"/>
        <field name="place">Office</field>
        <field name="odometer_start">5621.0</field>
        <field name="odometer_end">5977.0</field>
        <field name="distance_traveled_km">356.0</field>
        <field name="fuel_liters">26.71</field>
        <field name="expected_km_per_liter">14.0</field>
        <field name="actual_km_per_liter">13.33</field>
        <field name="fuel_usage_difference">-0.67</field>
        <field name="expected_fuel_liters">25.43</field>
        <field name="excess_use_liters">1.28</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">33.25</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">Suzuki Carry depot local errands</field>
    </record>

    <record id="fcl_log_014" model="nfd.fuel.consumption.log">
        <field name="name">FCL/2026/0014</field>
        <field name="date">2026-09-06</field>
        <field name="vehicle_id" ref="vehicle_n11255ot"/>
        <field name="driver_id" ref="employee_laythonne"/>
        <field name="place">Walvis</field>
        <field name="odometer_start">412500.0</field>
        <field name="odometer_end">413950.0</field>
        <field name="distance_traveled_km">1450.0</field>
        <field name="fuel_liters">564.0</field>
        <field name="expected_km_per_liter">2.7</field>
        <field name="actual_km_per_liter">2.57</field>
        <field name="fuel_usage_difference">-0.13</field>
        <field name="expected_fuel_liters">537.04</field>
        <field name="excess_use_liters">26.96</field>
        <field name="otj_coc_fuel_price">25.98</field>
        <field name="nad_value">700.42</field>
        <field name="confirm_logsheet">confirmed</field>
        <field name="confirm_stock">confirmed</field>
        <field name="anomaly_flag">normal</field>
        <field name="notes">Walvis Bay fuel import haulage run - Volvo FH520</field>
    </record>

    <record id="ts_workshop_1" model="account.analytic.line">
        <field name="name">Full A-Service and fuel injector cleaning on Mercedes Actros 2646 (N 7802 OT)</field>
        <field name="project_id" ref="project_workshop"/>
        <field name="task_id" ref="task_workshop_7802_service"/>
        <field name="employee_id" ref="employee_green"/>
        <field name="date">2026-09-04</field>
        <field name="unit_amount">6.5</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_workshop_2" model="account.analytic.line">
        <field name="name">Calibrated bottom-loading LC Master Flow Meter 15 at Otjiwarongo Depot</field>
        <field name="project_id" ref="project_workshop"/>
        <field name="task_id" ref="task_workshop_meter_calibration"/>
        <field name="employee_id" ref="employee_jonie"/>
        <field name="date">2026-09-06</field>
        <field name="unit_amount">4.0</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_haulage_1" model="account.analytic.line">
        <field name="name">Bulk 50ppm Diesel haulage Walvis Bay Port to Otjiwarongo Tank Farm (Semi N 12916 OT + PUP)</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="task_id" ref="task_haulage_walvis_import"/>
        <field name="employee_id" ref="employee_simon"/>
        <field name="date">2026-09-05</field>
        <field name="unit_amount">12.5</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_haulage_4" model="account.analytic.line">
        <field name="name">Bulk fuel transport to Husab Mine Swakopmund depot (Mercedes Actros N 7802 OT)</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="task_id" ref="task_haulage_husab"/>
        <field name="employee_id" ref="employee_mike"/>
        <field name="date">2026-09-04</field>
        <field name="unit_amount">9.5</field>
        <field name="amount">0.0</field>
    </record>
''')

    out.append('''
    <!-- Legacy Project Tasks & Timesheets (b84fb91 compatibility) -->
    <record id="task_workshop_scania_pm" model="project.task">
        <field name="name">50,000km Preventive Chassis &amp; Manifold Service - Scania R500 (N 4201 OT)</field>
        <field name="project_id" ref="project_workshop"/>
        <field name="allocated_hours">8.0</field>
    </record>

    <record id="task_workshop_axor_leakage" model="project.task">
        <field name="name">Inspect Tanker Manifold/Delivery Meter for Fuel Leakage - Axor (DISP/2026/0102)</field>
        <field name="project_id" ref="project_workshop"/>
        <field name="allocated_hours">6.0</field>
    </record>

    <record id="task_petrosol_outjo_nozzle" model="project.task">
        <field name="name">Monthly Dispenser Nozzle &amp; Meter Recalibration - Petrosol Outjo</field>
        <field name="project_id" ref="project_petrosol"/>
        <field name="partner_id" ref="partner_petrosol_outjo"/>
        <field name="allocated_hours">6.0</field>
    </record>

    <record id="task_petrosol_khorixas_coldroom" model="project.task">
        <field name="name">ILAMO Convenience Store Cold Room &amp; Standby Generator Service - Khorixas</field>
        <field name="project_id" ref="project_petrosol"/>
        <field name="partner_id" ref="partner_petrosol_khorixas"/>
        <field name="allocated_hours">5.0</field>
    </record>

    <record id="task_haulage_northern" model="project.task">
        <field name="name">Northern Commercial Distribution Run (Ondangwa / Fort Sesfontein)</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="allocated_hours">16.0</field>
    </record>

    <record id="ts_petrosol_1" model="account.analytic.line">
        <field name="name">Wayne Helix 4-nozzle 20L prover can measure and calibration test (Free Forecourt Service Subsidy)</field>
        <field name="project_id" ref="project_petrosol"/>
        <field name="task_id" ref="task_petrosol_outjo_nozzle"/>
        <field name="employee_id" ref="employee_lukas_van_wyk"/>
        <field name="date">2026-09-08</field>
        <field name="unit_amount">5.0</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_petrosol_2" model="account.analytic.line">
        <field name="name">Quarterly servicing of ILAMO cold room compressor and 50kVA standby diesel generator</field>
        <field name="project_id" ref="project_petrosol"/>
        <field name="task_id" ref="task_petrosol_khorixas_coldroom"/>
        <field name="employee_id" ref="employee_lukas_van_wyk"/>
        <field name="date">2026-09-18</field>
        <field name="unit_amount">3.5</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_haulage_2" model="account.analytic.line">
        <field name="name">Walvis Bay to Otjiwarongo Bulk Diesel Tanker Import haulage (Volvo FH520 N 11255 OT)</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="task_id" ref="task_haulage_walvis_import"/>
        <field name="employee_id" ref="employee_laythonne"/>
        <field name="date">2026-09-09</field>
        <field name="unit_amount">13.0</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_haulage_3" model="account.analytic.line">
        <field name="name">Mining bulk diesel supply Otjiwarongo to B2Gold Otjikoto Mine (Scania R500 N 4201 OT)</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="task_id" ref="task_haulage_b2gold"/>
        <field name="employee_id" ref="employee_hendrik_shilongo"/>
        <field name="date">2026-09-10</field>
        <field name="unit_amount">8.0</field>
        <field name="amount">0.0</field>
    </record>

    <record id="ts_haulage_5" model="account.analytic.line">
        <field name="name">Northern retail and commercial replenishment: Otjiwarongo to Ondangwa &amp; Fort Sesfontein</field>
        <field name="project_id" ref="project_haulage"/>
        <field name="task_id" ref="task_haulage_northern"/>
        <field name="employee_id" ref="employee_gabriel"/>
        <field name="date">2026-09-07</field>
        <field name="unit_amount">11.0</field>
        <field name="amount">0.0</field>
    </record>
''')
    out.append('    </data>')
    out.append('</odoo>')
    
    xml_content = '\n'.join(out)
    
    # Write to /tmp/demo_data_generated.xml
    with open('/tmp/demo_data_generated.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    print(f"Generated /tmp/demo_data_generated.xml ({len(xml_content)} bytes)")

if __name__ == '__main__':
    main()
