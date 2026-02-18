# SnapOCR - Cross-Platform Screenshot OCR Tool

A cross-platform tool that captures a screenshot region, extracts text using OCR, and copies the result to clipboard. Supports **English, Chinese**, and **LaTeX conversion for mathematical formulas**.

## Features

- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Interactive Region Selection**: Drag your mouse to select any area of your screen
- **Multi-Language OCR**: English + Chinese (Simplified) support out of the box
- **LaTeX Conversion**: Convert mathematical formulas to LaTeX notation
- **Clipboard Integration**: Automatically copies extracted text to clipboard
- **Auto-Paste**: Optionally simulate Ctrl+V / Cmd+V after copying
- **Global Hotkeys**: Configure keyboard shortcuts to trigger capture
- **Easy Installation**: Package as standalone executable

## Quick Start

```bash
# Clone the repository
git clone https://github.com/caswyj/SnapOCR.git
cd SnapOCR

# Install dependencies
pip install -r requirements.txt

# Run SnapOCR
python -m snapocr
```

## Installation

### Prerequisites

#### Tesseract OCR

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.

**Linux (Ubuntu/Debian):**
```bash
sudo apt install tesseract-ocr tesseract-ocr-chi-sim
```

#### Python Dependencies

```bash
pip install -r requirements.txt
```

### Optional: LaTeX Conversion

For math formula to LaTeX conversion, uncomment these lines in `requirements.txt`:
```
pix2tex>=0.1.0
torch>=1.9.0
transformers>=4.0.0
```

Then reinstall:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Capture region and extract text
python -m snapocr

# Or using the module directly
python -c "from snapocr import SnapOCR; SnapOCR().run_once()"
```

### Command Line Options

```
usage: snapocr [-h] [--daemon] [--setup-hotkey] [--hotkey HOTKEY] [--lang LANG]
               [--latex] [--no-latex] [--auto-paste] [--no-auto-paste]
               [--config CONFIG] [--version]

SnapOCR - Cross-platform screenshot OCR tool

options:
  -h, --help            show this help message and exit
  --daemon, -d          Run in daemon mode with hotkey listener
  --setup-hotkey, -s    Run the hotkey setup wizard
  --hotkey HOTKEY, -k HOTKEY
                        Override hotkey (e.g., "ctrl+shift+o")
  --lang LANG, -l LANG  OCR language (e.g., "eng", "chi_sim", "eng+chi_sim")
  --latex               Enable LaTeX conversion for math formulas
  --no-latex            Disable LaTeX conversion
  --auto-paste          Enable auto-paste after copying
  --no-auto-paste       Disable auto-paste
  --config CONFIG, -c CONFIG
                        Path to config file
  --version, -v         show program's version number and exit
```

### Daemon Mode

Run in the background with a global hotkey:

```bash
python -m snapocr --daemon
```

Press `Ctrl+Shift+O` (default) to trigger capture. Press `Ctrl+C` to exit.

### Hotkey Setup

Configure your preferred keyboard shortcut:

```bash
python -m snapocr --setup-hotkey
```

### Python API

```python
from snapocr import SnapOCR, Config

# Create app with custom config
config = Config()
config.language = 'eng+chi_sim'
config.auto_paste = True
config.latex_conversion = True

app = SnapOCR(config)

# Single capture
text = app.capture_and_extract()

# Or run daemon mode
app.run_daemon()
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
  "auto_paste": true,
  "paste_delay_ms": 500,
  "latex_conversion": false,
  "tesseract_path": null,
  "show_notification": true
}
```

| Option | Description |
|--------|-------------|
| `hotkey` | Global hotkey combination |
| `language` | Tesseract language code(s) |
| `auto_paste` | Auto-paste after copying |
| `paste_delay_ms` | Delay before auto-paste |
| `latex_conversion` | Enable LaTeX OCR for math |
| `tesseract_path` | Custom Tesseract executable path |

## Platform-Specific Notes

### macOS

- Uses built-in `screencapture` command for screenshots
- Uses `pbcopy`/`pbpaste` for clipboard
- **Accessibility Permission**: Required for global hotkeys and auto-paste
  - System Preferences → Security & Privacy → Privacy → Accessibility

### Windows

- Uses `mss` library with tkinter overlay for region selection
- Uses `pyperclip` for clipboard operations
- May require pywin32 for window capture: `pip install pywin32`

### Linux

- Uses `scrot` (recommended) or ImageMagick `import` for screenshots
- Uses `xclip` or `xsel` for clipboard
- Install: `sudo apt install scrot xclip`

## Building Standalone Executables

### macOS

```bash
cd scripts
./build_macos.sh
```

Output: `dist/SnapOCR.app`

### Windows

```powershell
cd scripts
.\build_windows.ps1
```

Output: `dist\SnapOCR.exe`

## Project Structure

```
SnapOCR/
├── snapocr/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── ocr.py           # OCR + LaTeX extraction
│   │   ├── clipboard.py     # Clipboard + auto-paste
│   │   └── config.py        # Config management
│   ├── platform/
│   │   ├── base.py          # Abstract base classes
│   │   ├── linux.py         # Linux implementation
│   │   ├── macos.py         # macOS implementation
│   │   └── windows.py       # Windows implementation
│   └── hotkey/
│       ├── manager.py       # Hotkey registration
│       └── setup_wizard.py  # Interactive hotkey config
├── resources/
│   └── tessdata/            # Language data (eng, chi_sim)
├── scripts/
│   ├── build_macos.sh
│   └── build_windows.ps1
├── requirements.txt
└── README.md
```

## Troubleshooting

### "No text detected"

- Ensure the text in the screenshot is clear and readable
- Install appropriate Tesseract language packs
- Try adjusting the region selection

### "tesseract is not installed"

Install Tesseract OCR:
- **macOS**: `brew install tesseract`
- **Windows**: Download from UB Mannheim releases
- **Linux**: `sudo apt install tesseract-ocr`

### "Could not copy to clipboard"

- **Linux**: Install xclip: `sudo apt install xclip`
- **macOS**: Check Terminal has clipboard access in Security settings

### Hotkeys not working (macOS)

Grant Accessibility permission:
1. System Preferences → Security & Privacy → Privacy
2. Select "Accessibility"
3. Add Terminal or your Python IDE to the list

### LaTeX conversion not working

Ensure pix2tex and dependencies are installed:
```bash
pip install pix2tex torch transformers
```

## License

This project is open source. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
