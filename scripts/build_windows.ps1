# Build script for Windows .exe using PyInstaller
# Run this in PowerShell

Write-Host "Building SnapOCR for Windows..."

# Check for PyInstaller
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $pyinstaller) {
    Write-Host "PyInstaller not found. Installing..."
    pip install pyinstaller
}

# Create executable
pyinstaller `
    --name "SnapOCR" `
    --onefile `
    --windowed `
    --icon resources/icon.ico `
    --add-data "resources/tessdata;resources/tessdata" `
    --hidden-import "PIL._tkinter_finder" `
    --hidden-import "pytesseract" `
    --hidden-import "pynput" `
    --hidden-import "pyautogui" `
    --hidden-import "mss" `
    snapocr/main.py

Write-Host ""
Write-Host "Build complete!"
Write-Host "Output: dist\SnapOCR.exe"
Write-Host ""
Write-Host "Note: For distribution, you may want to:"
Write-Host "  1. Sign the executable with signtool"
Write-Host "  2. Create an installer with NSIS or Inno Setup"
Write-Host ""
Write-Host "Tesseract and tessdata need to be bundled separately or installed on the target machine."