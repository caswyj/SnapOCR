#!/bin/bash
# Build script for Linux using PyInstaller

set -e

echo "Building SnapOCR for Linux..."

# Find the correct pip command
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "Error: pip not found. Please install Python first."
    exit 1
fi

echo "Using: $PIP_CMD"

# Check for PyInstaller
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller not found. Installing..."
    $PIP_CMD install pyinstaller
fi

# Create executable
python3 -m PyInstaller \
    --name "SnapOCR" \
    --onefile \
    --hidden-import "PIL._tkinter_finder" \
    --hidden-import "pytesseract" \
    --hidden-import "mss" \
    --hidden-import "snapocr" \
    --hidden-import "snapocr.main" \
    --hidden-import "snapocr.core.config" \
    --hidden-import "snapocr.core.ocr" \
    --hidden-import "snapocr.core.clipboard" \
    --hidden-import "snapocr.platform.base" \
    --hidden-import "snapocr.platform.linux" \
    --add-data "snapocr:snapocr" \
    --exclude-module "pynput" \
    --exclude-module "pyautogui" \
    run.py

echo ""
echo "Build complete!"
echo "Output: dist/SnapOCR"
echo ""
echo "Note: Tesseract OCR and screenshot tools must be installed:"
echo "  Ubuntu/Debian: sudo apt install tesseract-ocr tesseract-ocr-chi-sim scrot"
echo "  Fedora: sudo dnf install tesseract tesseract-langpack-chi_sim scrot"
