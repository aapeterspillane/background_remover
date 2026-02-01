#!/bin/bash
# Create a DMG file for macOS distribution

set -e

APP_NAME="Background Remover"
DMG_NAME="BackgroundRemover"
VERSION="1.0.0"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_DIR/dist"
APP_PATH="$DIST_DIR/$APP_NAME.app"

if [ ! -d "$APP_PATH" ]; then
    echo "Error: App bundle not found at $APP_PATH"
    echo "Run build_macos.py first."
    exit 1
fi

DMG_PATH="$DIST_DIR/${DMG_NAME}-${VERSION}.dmg"

echo "Creating DMG: $DMG_PATH"

# Remove old DMG if exists
rm -f "$DMG_PATH"

# Create DMG
hdiutil create -volname "$APP_NAME" \
    -srcfolder "$APP_PATH" \
    -ov -format UDZO \
    "$DMG_PATH"

echo "DMG created: $DMG_PATH"
