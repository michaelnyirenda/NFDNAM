# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def post_init_hook(env):
    """
    Post-installation hook to initialize realistic bulk fuel stock on hand
    at the Otjiwarongo Depot for NFD & Petrosol demo.
    """
    tank1_diesel = env.ref('nfd_petrosol_demo.location_tank_1_diesel', raise_if_not_found=False)
    tank2_ulp95 = env.ref('nfd_petrosol_demo.location_tank_2_ulp95', raise_if_not_found=False)
    workshop_store = env.ref('nfd_petrosol_demo.location_workshop_store', raise_if_not_found=False)

    product_diesel = env.ref('nfd_petrosol_demo.product_diesel_50ppm', raise_if_not_found=False)
    product_ulp95 = env.ref('nfd_petrosol_demo.product_ulp_95', raise_if_not_found=False)
    product_oil = env.ref('nfd_petrosol_demo.product_oil_15w40', raise_if_not_found=False)
    product_grease = env.ref('nfd_petrosol_demo.product_grease_ep2', raise_if_not_found=False)
    product_filter = env.ref('nfd_petrosol_demo.product_scania_filter_kit', raise_if_not_found=False)
    product_seal = env.ref('nfd_petrosol_demo.product_tanker_seal_kit', raise_if_not_found=False)

    stock_items = [
        (product_diesel, tank1_diesel, 485000.0),
        (product_ulp95, tank2_ulp95, 165000.0),
        (product_oil, workshop_store, 45.0),
        (product_grease, workshop_store, 60.0),
        (product_filter, workshop_store, 25.0),
        (product_seal, workshop_store, 30.0),
    ]

    for prod, loc, qty in stock_items:
        if prod and loc:
            try:
                env['stock.quant']._update_available_quantity(prod, loc, qty)
            except Exception:
                try:
                    quant = env['stock.quant'].create({
                        'product_id': prod.id,
                        'location_id': loc.id,
                        'inventory_quantity': qty,
                    })
                    quant.action_apply_inventory()
                except Exception:
                    pass
