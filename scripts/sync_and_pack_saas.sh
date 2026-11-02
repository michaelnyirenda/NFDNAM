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

# 5. Build Distribution ZIP
mkdir -p "${DIST_DIR}"
rm -f "${ZIP_PATH}"

echo "📦 Packaging '${ZIP_NAME}'..."
(
    cd "${SAAS_WORKTREE}"
    zip -r -q "${ZIP_PATH}" "nfd_petrosol_demo" \
        -x "*.git*" \
        -x "*.DS_Store*" \
        -x "*__pycache__*" \
        -x "*.pyc" \
        -x "*.swp" \
        -x "*.swo"
)

ZIP_SIZE=$(du -h "${ZIP_PATH}" | cut -f1)
echo "   ✓ Successfully packaged: ${ZIP_PATH} (${ZIP_SIZE})"
echo "-------------------------------------------------------------------"
echo "📋 HOW TO IMPORT TO ODOO ONLINE (edu-*.odoo.com):"
echo "1. Log into your free 90-day education database: https://edu-<subdomain>.odoo.com"
echo "2. Navigate to: Settings > Developer Tools > Activate the developer mode."
echo "3. Go to Apps > Ensure standard apps (Fleet, Maintenance, Inventory, Employees) are installed."
echo "4. In Apps, click the top menu: 'Import Module' (or install 'base_import_module')."
echo "5. Upload file: dist/${ZIP_NAME}"
echo "6. Click 'Import Module' -> The NFD & Petrosol demo records will load automatically!"
echo "==================================================================="
