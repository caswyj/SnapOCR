#!/bin/bash
# Build script for macOS .app bundle using PyInstaller

set -e

echo "Building SnapOCR for macOS..."

# Check for PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Create .app bundle
pyinstaller \
    --name "SnapOCR" \
    --windowed \
    --onefile \
    --icon resources/icon.icns \
    --add-data "resources/tessdata:resources/tessdata" \
    --hidden-import "PIL._tkinter_finder" \
    --hidden-import "pytesseract" \
    --hidden-import "pynput" \
    --hidden-import "pyautogui" \
    --hidden-import "mss" \
    --osx-bundle-identifier "com.snapocr.app" \
    snapocr/main.py

echo ""
echo "Build complete!"
echo "Output: dist/SnapOCR.app"
echo ""
echo "Note: You may need to codesign the app for distribution:"
echo "  codesign --deep --force --verify --verbose dist/SnapOCR.app"