#!/bin/bash
# Capture App Store screenshots for JB Law from the booted simulator.
#
# Usage:
#   ./scripts/capture_law_screenshots.sh <number> <name>
# Example:
#   ./scripts/capture_law_screenshots.sh 2 filter
#
# Saves to screenshots/iphone-17-pro-max/N_name.png — same naming as JB AI.
#
# Recommended capture order (mirror JB AI's 4-shot set):
#   1_home         — alphabet grid (already captured)
#   2_filter       — tap the filter icon (top-right), capture the sheet
#   3_basics       — in filter sheet, tap "Basics" lens to enter list view
#   4_term_NAME    — tap into a rich term (e.g. Miranda warning), capture detail

set -euo pipefail

NUM="${1:-X}"
NAME="${2:-screenshot}"
DEST_DIR="$(dirname "$0")/../screenshots/iphone-17-pro-max"
mkdir -p "$DEST_DIR"

FILENAME="${NUM}_${NAME}.png"
DEST="$DEST_DIR/$FILENAME"

xcrun simctl io booted screenshot "$DEST"
echo "Saved: $DEST"
