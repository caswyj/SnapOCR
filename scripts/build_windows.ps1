# Build script for Windows .exe using PyInstaller
# Run this in PowerShell

Write-Host "Building SnapOCR for Windows..."

# Find the correct pip command
$pipCmd = $null
if (Get-Command pip3 -ErrorAction SilentlyContinue) {
    $pipCmd = "pip3"
} elseif (Get-Command pip -ErrorAction SilentlyContinue) {
    $pipCmd = "pip"
} else {
    Write-Host "Error: pip not found. Please install Python first."
    exit 1
}

Write-Host "Using: $pipCmd"

# Check for PyInstaller
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $pyinstaller) {
    Write-Host "PyInstaller not found. Installing..."
    & $pipCmd install pyinstaller
}

# Create executable
pyinstaller `
    --name "SnapOCR" `
    --onefile `
    --windowed `
    --hidden-import "PIL._tkinter_finder" `
    --hidden-import "pytesseract" `
    --hidden-import "mss" `
    --hidden-import "snapocr" `
    --hidden-import "snapocr.main" `
    --hidden-import "snapocr.core.config" `
    --hidden-import "snapocr.core.ocr" `
    --hidden-import "snapocr.core.clipboard" `
    --hidden-import "snapocr.platform.base" `
    --hidden-import "snapocr.platform.windows" `
    --add-data "snapocr;snapocr" `
    --exclude-module "pynput" `
    --exclude-module "pyautogui" `
    run.py

Write-Host ""
Write-Host "Build complete!"
Write-Host "Output: dist\SnapOCR.exe"
Write-Host ""
Write-Host "Note: Tesseract OCR must be installed on the target machine."
Write-Host "Download from: https://github.com/UB-Mannheim/tesseract/wiki"
