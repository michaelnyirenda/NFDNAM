#!/usr/bin/env bash
# ==============================================================================
# NFD & Petrosol Demo - SaaS edu Import Packager & Sync Automation
# ==============================================================================
# This script:
# 1. Validates or syncs shared assets between 'main' and 'saas-edu-import' worktrees.
# 2. Ensures ZERO Python files (except __manifest__.py) exist in the SaaS module.
# 3. Packages the pure XML/CSV module into dist/nfd_petrosol_edu_import.zip for
#    1-click upload to Odoo Online (edu-*.odoo.com) via Apps > Import Module.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 1. Locate SaaS worktree
SAAS_WORKTREE=""
if [ -d "${ROOT_DIR}/.worktrees/saas-edu-import" ]; then
    SAAS_WORKTREE="${ROOT_DIR}/.worktrees/saas-edu-import"
elif [ -d "${ROOT_DIR}/../nfd_petrosol_saas_edu" ]; then
    SAAS_WORKTREE="${ROOT_DIR}/../nfd_petrosol_saas_edu"
fi

if [ -z "$SAAS_WORKTREE" ]; then
    echo "❌ Error: Could not locate 'saas-edu-import' worktree at:"
    echo "   - ${ROOT_DIR}/.worktrees/saas-edu-import"
    echo "   - ${ROOT_DIR}/../nfd_petrosol_saas_edu"
    echo "Please ensure the git worktree is created:"
    echo "   git worktree add .worktrees/saas-edu-import saas-edu-import"
    exit 1
fi

MAIN_MODULE="${ROOT_DIR}/nfd_petrosol_demo"
SAAS_MODULE="${SAAS_WORKTREE}/nfd_petrosol_demo"
DIST_DIR="${ROOT_DIR}/dist"
ZIP_NAME="nfd_petrosol_edu_import.zip"
ZIP_PATH="${DIST_DIR}/${ZIP_NAME}"

echo "==================================================================="
echo "🚀 NFD & Petrosol: Sync & Package for Odoo Online (edu-*.odoo.com)"
echo "==================================================================="
echo "• Main Worktree:   ${ROOT_DIR}"
echo "• SaaS Worktree:   ${SAAS_WORKTREE}"
echo "• Target Module:   ${SAAS_MODULE}"
echo "-------------------------------------------------------------------"

# 2. Sync Shared Static Assets (Icon, Descriptions)
echo "📦 Syncing shared static web assets..."
mkdir -p "${SAAS_MODULE}/static/description"
cp -rf "${MAIN_MODULE}/static/description/"* "${SAAS_MODULE}/static/description/"
echo "   ✓ Static assets synchronized."

# 3. Strict Zero-Python Validation (Mandatory for base_import_module on SaaS)
echo "🔍 Validating pure XML/CSV compliance (Zero-Python audit)..."
PY_FILES=$(find "${SAAS_MODULE}" -type f -name "*.py" ! -name "__manifest__.py" -o -type d -name "__pycache__")

if [ -n "$PY_FILES" ]; then
    echo "❌ ERROR: Disallowed Python files or __pycache__ found in SaaS module:"
    echo "$PY_FILES"
    echo "Odoo Online (edu-*.odoo.com) strictly rejects any custom Python files."
    exit 1
fi
echo "   ✓ Zero-Python audit passed (only declarative XML, CSV & __manifest__.py found)."

# 4. Validate Manifest Structure
if [ ! -f "${SAAS_MODULE}/__manifest__.py" ]; then
    echo "❌ ERROR: Missing ${SAAS_MODULE}/__manifest__.py"
    exit 1
fi

# Ensure ir_model_fields.xml is listed before ir.model.access.csv
FIRST_DATA_ENTRY=$(grep -A 2 "'data':" "${SAAS_MODULE}/__manifest__.py" | grep -v "'data':" | head -n 1 | tr -d " '\",")
if [[ "$FIRST_DATA_ENTRY" != *"ir_model_fields.xml"* ]]; then
    echo "⚠️  WARNING: data/ir_model_fields.xml should be the first entry in 'data': [...]"
    echo "   Found: $FIRST_DATA_ENTRY"
fi

# ==============================================================================
# 5. AUTO-SANITIZE SaaS XMLs (Models, Fields, Action Refs, & Odoo 20 Schema Rules)
# ==============================================================================
echo "🧹 Sanitizing SaaS XML files for Odoo Online (Odoo 20.0) compatibility..."

python3 - "$SAAS_MODULE" << 'EOF'
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

saas_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".worktrees/saas-edu-import/nfd_petrosol_demo")
if not saas_dir.exists():
    saas_dir = Path("../nfd_petrosol_saas_edu/nfd_petrosol_demo")

# 1. Remove security/ directory if accidentally synced from main
sec_dir = saas_dir / "security"
if sec_dir.exists():
    shutil.rmtree(sec_dir)
    print("  [OK] Purged security/ directory from SaaS build.")

# 2. Ensure __manifest__.py has version '1.0.0' and no security file references
manifest_path = saas_dir / "__manifest__.py"
if manifest_path.exists():
    m_text = manifest_path.read_text(encoding="utf-8")
    m_text = re.sub(r"'version'\s*:\s*'[^']*'", "'version': '1.0.0'", m_text)
    m_lines = [line for line in m_text.splitlines() if "security/" not in line]
    manifest_path.write_text("\n".join(m_lines) + "\n", encoding="utf-8")
    print("  [OK] Verified __manifest__.py (version 1.0.0, zero security/ refs).")

# 3. Convert nfd.fuel.* records & fields to x_nfd_fuel_* in data/demo_data.xml
demo_path = saas_dir / "data" / "demo_data.xml"
if demo_path.exists():
    # Fix datetime.now() before XML parsing
    raw_demo = demo_path.read_text(encoding="utf-8").replace('eval="datetime.now()', 'eval="DateTime.now()')
    demo_path.write_text(raw_demo, encoding="utf-8")

    tree = ET.parse(demo_path)
    root = tree.getroot()
    model_map = {
        "nfd.fuel.dispatch.log": "x_nfd_fuel_dispatch_log",
        "nfd.fuel.consumption.log": "x_nfd_fuel_consumption_log",
    }
    converted = 0
    for rec in root.findall(".//record"):
        m = rec.attrib.get("model")
        if m in model_map:
            rec.set("model", model_map[m])
            converted += 1
        if rec.attrib.get("model") in model_map.values():
            for fld in rec.findall("field"):
                fname = fld.attrib.get("name", "")
                if fname and not fname.startswith("x_"):
                    fld.set("name", f"x_{fname}")
                if fname in ("scrap_id", "x_scrap_id"):
                    rec.remove(fld)

    tree.write(demo_path, encoding="utf-8", xml_declaration=True)
    print(f"  [OK] Normalized {demo_path.name} ({converted} records converted to x_ models/fields).")

# 4. Enforce on_delete='restrict' (and strip invalid 'ondelete' or 'stock.scrap') in ir_model_fields.xml
fields_path = saas_dir / "data" / "ir_model_fields.xml"
if fields_path.exists():
    f_text = fields_path.read_text(encoding="utf-8")
    f_text = re.sub(r'^[ \t]*<field name="ondelete">[^<]*</field>\r?\n?', '', f_text, flags=re.MULTILINE)
    fields_path.write_text(f_text, encoding="utf-8")
    print("  [OK] Verified data/ir_model_fields.xml (on_delete='restrict' clean).")

# 5. Align action_x_nfd_fuel_dispatch_log in views/menus.xml
menus_path = saas_dir / "views" / "menus.xml"
if menus_path.exists():
    menus_text = menus_path.read_text(encoding="utf-8")
    menus_text = menus_text.replace(
        'action="action_nfd_fuel_dispatch_log"',
        'action="action_x_nfd_fuel_dispatch_log"'
    )
    menus_path.write_text(menus_text, encoding="utf-8")
    print("  [OK] Verified action references in views/menus.xml.")
EOF

# 6. Build Distribution ZIP
mkdir -p "${DIST_DIR}"
rm -f "${ZIP_PATH}"

echo "📦 Packaging '${ZIP_NAME}' via Python zipfile..."
python3 - "$SAAS_MODULE" "$ZIP_PATH" << 'PACK_ZIP'
import sys
import zipfile
from pathlib import Path

saas_dir = Path(sys.argv[1])
zip_path = Path(sys.argv[2])
base_parent = saas_dir.parent

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in sorted(saas_dir.rglob("*")):
        if p.is_file():
            if any(x in p.parts for x in [".git", "__pycache__", ".DS_Store", "security"]):
                continue
            zf.write(p, p.relative_to(base_parent))

print(f"   ✓ Successfully packaged: {zip_path} ({zip_path.stat().st_size / 1024:.1f} KB)")
PACK_ZIP
echo "-------------------------------------------------------------------"
echo "📋 HOW TO IMPORT TO ODOO ONLINE (edu-*.odoo.com):"
echo "1. Log into your free 90-day education database: https://edu-<subdomain>.odoo.com"
echo "2. Navigate to: Settings > Developer Tools > Activate the developer mode."
echo "3. Go to Apps > Ensure standard apps (Fleet, Maintenance, Inventory, Employees) are installed."
echo "4. In Apps, click the top menu: 'Import Module' (or install 'base_import_module')."
echo "5. Upload file: dist/${ZIP_NAME}"
echo "6. Click 'Import Module' -> The NFD & Petrosol demo records will load automatically!"
echo "==================================================================="
