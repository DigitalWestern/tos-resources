#!/bin/bash
#
# install-hooks.sh
# Run once after cloning to install git hooks for this project.
#
# Usage:  bash scripts/install-hooks.sh
#

set -e

# ── Resolve paths ──────────────────────────────────────────────────
# Find the repo root (where .git lives), regardless of where this
# script is called from.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$REPO_ROOT" ]; then
    echo "Error: not inside a git repository."
    exit 1
fi

HOOKS_DIR="$REPO_ROOT/.git/hooks"
SOURCE_DIR="$REPO_ROOT/scripts"

# ── Install pre-push hook ─────────────────────────────────────────
# Copies scripts/pre-push into .git/hooks/ and makes it executable.
# If a pre-push hook already exists, backs it up first.

if [ -f "$HOOKS_DIR/pre-push" ] && [ ! -f "$HOOKS_DIR/pre-push.bak" ]; then
    # Don't overwrite without a backup, but skip if backup already exists
    # (means we installed before)
    cp "$HOOKS_DIR/pre-push" "$HOOKS_DIR/pre-push.bak"
    echo "Backed up existing pre-push hook to .git/hooks/pre-push.bak"
fi

cp "$SOURCE_DIR/pre-push" "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-push"

echo "Installed pre-push hook."
echo ""
echo "What it does:"
echo "  - Scans outgoing commits for exposed secrets and API keys"
echo "  - Checks for hardcoded passwords"
echo "  - Flags possible sensitive personal data"
echo "  - Verifies local asset references in HTML files"
echo ""
echo "To bypass on a specific push:  git push --no-verify"
echo ""
echo "Done."
