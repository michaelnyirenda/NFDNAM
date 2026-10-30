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
docker exec nfd-odoo19 odoo -d nfd_demo -i base,fleet,maintenance,stock,hr,hr_skills,purchase,sale_management,account,project --stop-after-init
docker exec nfd-odoo19 odoo -d nfd_demo -i nfd_petrosol_demo --stop-after-init

# 3. Open Odoo in your browser
# URL: http://localhost:8069 (Database: nfd_demo)
```

Refer to [NFD_DEMO_SOP.md](NFD_DEMO_SOP.md) for full step-by-step guidance.

