# NFD & Petrosol Petroleum Solutions - Odoo 19 Solution

End-to-end Odoo 19 implementation and demo suite for **Northern Fuel Distributors CC (NFD)** and **Petrosol Petroleum Solutions CC** (Otjiwarongo, Namibia).

## Repository Contents

- **`nfd_petrosol_demo/`**: Custom Odoo 19 module featuring:
  - Bulk fuel logistics and distribution (>4M L/month)
  - Meter vs. dip reconciliation with dynamic thermal variance allowance (0.25%)
  - Automated leakage detection (>50 L threshold) with 1-click corrective maintenance & scrap write-off
  - Fleet governance & automated vehicle replacement policy (Prime Movers < 18y, Tankers < 15y)
  - HESMS driver safety compliance (Dangerous Goods Hazchem, Defensive Driving, Medical Fitness) & Affirmative Action tracking
  - Customer bulk tank & retail forecourt maintenance management (CODO/DODO & ILAMO convenience stores)
- **`docker-compose.yml`**: Turnkey local environment orchestrating PostgreSQL 16 and Odoo 19 with the addon pre-mounted.
- **`NFD_DEMO_SOP.md`**: Standard Operating Procedure containing:
  - Local environment replication instructions (via Docker Compose / CLI)
  - Pre-flight checklist & smoke tests
  - 25-minute live demonstration script for Johan Botes (GM/Operations) and Pierre Fourie (Finance)
  - End-to-end QA functional test cases

## Quickstart (Local Setup)

```bash
# 1. Spin up PostgreSQL 16 and Odoo 19
docker compose up -d

# 2. Initialize database and install module with demo seed data
docker exec nfd-db psql -U odoo -d postgres -c "CREATE DATABASE nfd_demo OWNER odoo;"
docker exec nfd-odoo19 odoo -d nfd_demo --db_host=nfd-db --db_user=odoo --db_password=odoo_secure_db_pass -i base,fleet,maintenance,stock,hr,hr_skills,purchase,sale_management,account,project --stop-after-init
docker exec nfd-odoo19 odoo -d nfd_demo --db_host=nfd-db --db_user=odoo --db_password=odoo_secure_db_pass -i nfd_petrosol_demo --stop-after-init

# 3. Open Odoo in your browser
# URL: http://localhost:8069 (Database: nfd_demo)
```

## Quickstart (Odoo Online / edu-*.odoo.com SaaS)

If you are presenting on a free 90-day **Odoo Online Education (`edu-*.odoo.com`)** cloud instance:

```bash
# 1. Package the pure XML/CSV module from the saas-edu-import worktree
./scripts/sync_and_pack_saas.sh

# 2. Upload dist/nfd_petrosol_edu_import.zip in Odoo Online:
#    Settings > Activate Developer Mode > Apps > Import Module
```

## Dual-Branch Architecture

This repository uses Git Worktrees to maintain both environments side-by-side:
- **`main`**: Full Python/ORM Odoo 19 module (`nfd_petrosol_demo`) for local Docker and Odoo.sh development.
- **`saas-edu-import`**: 100% pure declarative XML/CSV module (`nfd_petrosol_demo`) with zero Python code, custom models/fields defined in `ir.model`/`ir.model.fields`, and inline sandboxed logic for Odoo Online SaaS.
  - Worktree path: `.worktrees/saas-edu-import` (or symlink `../nfd_petrosol_saas_edu`).

Refer to [NFD_DEMO_SOP.md](NFD_DEMO_SOP.md) for full step-by-step guidance.

