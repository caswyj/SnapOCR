# SnapOCR - Cross-Platform Screenshot OCR Tool

A cross-platform tool that captures a screenshot region, extracts text using OCR, and copies the result to clipboard. Supports **English, Chinese**, and **LaTeX conversion for mathematical formulas**.

## Features

- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Interactive Region Selection**: Drag your mouse to select any area of your screen
- **Multi-Language OCR**: English + Chinese (Simplified) support out of the box
- **LaTeX Conversion**: Convert mathematical formulas to LaTeX notation
- **Clipboard Integration**: Automatically copies extracted text to clipboard
- **Self-Contained**: Tesseract OCR bundled - no external dependencies required
- **System Shortcuts**: Use native OS keyboard shortcuts to launch

## Download

Download the latest release from [GitHub Releases](https://github.com/caswyj/SnapOCR/releases):

| Platform | File |
|----------|------|
| macOS (Apple Silicon) | `SnapOCR-macOS-arm64.zip` |
| Windows | `SnapOCR.exe` |
| Linux | `SnapOCR` |

## Quick Start

### From Release (Recommended)

1. Download the appropriate file for your platform
2. **macOS**: Extract and move `SnapOCR.app` to Applications
3. **Windows**: Run `SnapOCR.exe` directly
4. **Linux**: `chmod +x SnapOCR && ./SnapOCR`

### From Source

```bash
# Clone the repository
git clone https://github.com/caswyj/SnapOCR.git
cd SnapOCR

# Install dependencies
pip install -r requirements.txt

# Run SnapOCR
python -m snapocr
```

## Usage

### Basic Usage

Run the application, then:
1. Select a region on your screen by dragging
2. Release to capture and perform OCR
3. Extracted text is automatically copied to clipboard

### Command Line Options

```
usage: snapocr [-h] [--lang LANG] [--latex] [--no-latex] [--config CONFIG] [--version]

SnapOCR - Cross-platform screenshot OCR tool

options:
  -h, --help            show this help message and exit
  --lang LANG, -l LANG  OCR language (e.g., "eng", "chi_sim", "eng+chi_sim")
  --latex               Enable LaTeX conversion for math formulas
  --no-latex            Disable LaTeX conversion
  --config CONFIG, -c CONFIG
                        Path to config file
  --version, -v         show program's version number and exit
```

### Python API

```python
from snapocr import SnapOCR, Config

# Create app with custom config
config = Config()
config.language = 'eng+chi_sim'
config.latex_conversion = True

app = SnapOCR(config)

# Capture and extract text
text = app.capture_and_extract()
print(f"Extracted: {text}")
```

## Setting Up Keyboard Shortcuts

Use your operating system's native shortcut features to launch SnapOCR with a keyboard shortcut.

### macOS

**Method 1: Shortcuts.app (Recommended, macOS 12+)**

1. Open **Shortcuts** app
2. Click **+** to create a new shortcut
3. Search for "Open App" and select it
4. Choose **SnapOCR**
5. Click the **ℹ** button → **Add Keyboard Shortcut**
6. Press your desired combination (e.g., `⌘⇧O`)
7. Name the shortcut "SnapOCR"

**Method 2: Automator + Services**

1. Open **Automator** → File → New → Quick Action
2. Set "Workflow receives" to "no input"
3. Add "Run Shell Script" action
4. Enter: `/Applications/SnapOCR.app/Contents/MacOS/SnapOCR`
5. Save as "SnapOCR Capture"
6. Go to **System Settings** → **Keyboard** → **Keyboard Shortcuts** → **Services**
7. Find "SnapOCR Capture" and set your shortcut

### Windows

**Method 1: Shortcut Properties**

1. Right-click `SnapOCR.exe` → Create shortcut
2. Right-click the shortcut → Properties
3. Click in the "Shortcut key" field
4. Press your combination (e.g., `Ctrl+Shift+O`)
5. Click OK

**Method 2: PowerToys (Recommended)**

1. Install [Microsoft PowerToys](https://github.com/microsoft/PowerToys)
2. Open PowerToys → Keyboard Manager
3. Click "Remap a shortcut"
4. Add new mapping:
   - Shortcut: `Ctrl + Shift + O`
   - Action: Start Program → Select `SnapOCR.exe`
5. Save

### Linux

**GNOME (Ubuntu, Fedora, etc.)**

1. Open **Settings** → **Keyboard**
2. Scroll down → **View and Customize Shortcuts**
3. Click **Custom Shortcuts** → **Add Shortcut**
4. Name: `SnapOCR`
5. Command: `/path/to/SnapOCR`
6. Set your shortcut (e.g., `Ctrl+Shift+O`)

**KDE Plasma**

1. Open **System Settings** → **Shortcuts**
2. Click **Edit** → **New** → **Global Shortcut** → **Command/URL**
3. Set trigger to your preferred shortcut
4. Set action to: `/path/to/SnapOCR`

**i3 / sway**

Add to your config (`~/.config/i3/config` or `~/.config/sway/config`):
```
bindsym $mod+Shift+o exec /path/to/SnapOCR
```

## Configuration

Config file locations:
- **macOS**: `~/Library/Application Support/SnapOCR/config.json`
- **Windows**: `%APPDATA%/SnapOCR/config.json`
- **Linux**: `~/.config/snapocr/config.json`

### Configuration Options

```json
{
  "hotkey": "ctrl+shift+o",
  "language": "eng+chi_sim",
  "latex_conversion": false,
  "tesseract_path": null,
  "show_notification": true
}
```

| Option | Description |
|--------|-------------|
| `language` | Tesseract language code(s) |
| `latex_conversion` | Enable LaTeX OCR for math |
| `tesseract_path` | Custom Tesseract path (optional, uses bundled version by default) |

## Supported Languages

SnapOCR includes English (`eng`) and Simplified Chinese (`chi_sim`) by default. To add more languages:

1. Download trained data from [tessdata](https://github.com/tesseract-ocr/tessdata)
2. Place `.traineddata` files in the `tessdata` directory:
   - **macOS**: `SnapOCR.app/Contents/Resources/tessdata/`
   - **Windows**: Same directory as `SnapOCR.exe`
   - **Linux**: Same directory as the executable

## Building from Source

### Prerequisites

- Python 3.9+
- Tesseract OCR (for development)

```bash
# macOS
brew install tesseract tesseract-lang

# Linux
sudo apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim

# Windows - download from UB Mannheim
```

### Build

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build for current platform
python -m PyInstaller SnapOCR.spec
```

Or use the platform-specific scripts:
- **macOS**: `./scripts/build_macos.sh`
- **Windows**: `.\scripts\build_windows.ps1`
- **Linux**: `./scripts/build_linux.sh`

## Project Structure

```
SnapOCR/
├── snapocr/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── ocr.py           # OCR + LaTeX extraction
│   │   ├── clipboard.py     # Clipboard operations
│   │   └── config.py        # Config management
│   └── platform/
│       ├── base.py          # Abstract base classes
│       ├── linux.py         # Linux implementation
│       ├── macos.py         # macOS implementation
│       ├── macos_native.py  # macOS native APIs
│       └── windows.py       # Windows implementation
├── resources/
│   ├── Info.plist           # macOS app metadata
│   └── SnapOCR.entitlements # macOS sandbox entitlements
├── scripts/
│   ├── build_macos.sh
│   ├── build_windows.ps1
│   └── build_linux.sh
├── .github/workflows/
│   └── build.yml            # Cross-platform CI/CD
├── requirements.txt
└── README.md
```

## Troubleshooting

### "No text detected"

- Ensure the text in the screenshot is clear and readable
- Try adjusting the region selection for better contrast
- Check if the correct language is configured

### macOS: "Screen Recording" permission required

1. **System Settings** → **Privacy & Security** → **Screen Recording**
2. Add SnapOCR to the allowed apps

### macOS: App is "damaged" or "unidentified developer"

```bash
xattr -cr /Applications/SnapOCR.app
```

### Windows: SmartScreen warning

Click "More info" → "Run anyway"

### Linux: Screenshot not working

Ensure you have a screenshot tool installed:
```bash
# Ubuntu/Debian
sudo apt install scrot

# Or use mss (bundled)
```

### LaTeX conversion not working

Install additional dependencies:
```bash
pip install pix2tex torch transformers
```

## License

This project is open source. See the LICENSE file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [pytesseract](https://github.com/madmaze/pytesseract) - Python wrapper
- [Pillow](https://python-pillow.org/) - Image processing
- [mss](https://github.com/BoboTiG/python-mss) - Cross-platform screenshots