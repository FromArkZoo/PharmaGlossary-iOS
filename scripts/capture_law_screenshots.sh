#!/bin/bash
# Capture App Store screenshots for JB Law from the booted simulator.
#
# Usage:
#   ./scripts/capture_law_screenshots.sh <number> <name>
# Example:
#   ./scripts/capture_law_screenshots.sh 2 detail
#
# Saves to docs/screenshots/iphone-17-pro-max/NN_name.png
#
# Recommended capture order (with the JB Law app open in the sim):
#   1. home              — alphabet grid (already captured)
#   2. detail            — tap any letter, then any term, capture detail view
#   3. filter            — tap the filter icon (top-right), capture the sheet
#   4. lens-civil        — in filter sheet, switch lens to "Civil & Business"
#   5. about             — tap "About JB Law" from filter sheet footer

set -euo pipefail

NUM="${1:-X}"
NAME="${2:-screenshot}"
DEST_DIR="$(dirname "$0")/../docs/screenshots/iphone-17-pro-max"
mkdir -p "$DEST_DIR"

FILENAME=$(printf "%02d_%s.png" "$NUM" "$NAME")
DEST="$DEST_DIR/$FILENAME"

xcrun simctl io booted screenshot "$DEST"
echo "Saved: $DEST"
