# SnapOCR - Screenshot OCR Tool

A simple command-line tool that captures a screenshot region selected by mouse drag, extracts text using OCR (Optical Character Recognition), and copies the result to your clipboard.

## Features

- **Interactive Region Selection**: Drag your mouse to select any area of your screen
- **OCR Text Extraction**: Uses Tesseract OCR to extract text from screenshots
- **Clipboard Integration**: Automatically copies extracted text to clipboard
- **Keyboard Shortcut Support**: Can be triggered with a custom keyboard shortcut

## Prerequisites

### System Dependencies

This tool requires several system packages. Install them with:

```bash
# Tesseract OCR engine (required for text recognition)
sudo apt install tesseract-ocr

# Screenshot tool (scrot is recommended)
sudo apt install scrot

# Clipboard support (xclip or xsel)
sudo apt install xclip

# Optional: Additional Tesseract language packs
# For Chinese (Simplified):
sudo apt install tesseract-ocr-chi-sim
# For Chinese (Traditional):
sudo apt install tesseract-ocr-chi-tra
# For other languages, use:
sudo apt install tesseract-ocr-[lang-code]
```

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pytesseract Pillow pyperclip
```

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:caswyj/extract.git
   cd extract
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify system dependencies are installed:
   ```bash
   # Check Tesseract
   tesseract --version

   # Check scrot
   scrot --version
   ```

## Usage

### Basic Usage

Run the script directly:

```bash
python3 snapocr.py
```

Then:
1. Your mouse cursor will change to a crosshair
2. Click and drag to select the region containing text
3. Release the mouse button to capture
4. The extracted text will be displayed and copied to clipboard

### Example

```
$ python3 snapocr.py
Select a region with your mouse (drag to select, Esc to cancel)...
Extracting text...
Text copied to clipboard (127 characters)
----------------------------------------
This is the extracted text from your screenshot.
It will be automatically copied to your clipboard.
----------------------------------------
```

## Setting Up Keyboard Shortcut

You can configure a keyboard shortcut to launch SnapOCR instantly.

### Automatic Setup (GNOME)

Run the setup script:

```bash
python3 setup_hotkey.py
```

This will configure `Super+O` (Windows key + O) as the shortcut.

### Manual Setup (GNOME)

1. Open **Settings** → **Keyboard** → **Custom Shortcuts**
2. Click the **+** button to add a new shortcut
3. Fill in the fields:
   - **Name**: `SnapOCR`
   - **Command**: `/usr/bin/python3 /path/to/snapocr.py`
   - **Shortcut**: Press your desired key combination (e.g., `Ctrl+Q` or `Super+O`)

### Manual Setup (Other Desktop Environments)

**KDE Plasma:**
1. Go to **System Settings** → **Shortcuts** → **Custom Shortcuts**
2. Click **Edit** → **New** → **Global Shortcut** → **Command/URL**
3. Set the trigger and action

**i3wm:**
Add to your `~/.config/i3/config`:
```
bindsym $mod+o exec /usr/bin/python3 /path/to/snapocr.py
```

## Troubleshooting

### "No screenshot tool found"

Install scrot:
```bash
sudo apt install scrot
```

### "tesseract is not installed"

Install Tesseract OCR:
```bash
sudo apt install tesseract-ocr
```

### "Could not copy to clipboard"

Install xclip:
```bash
sudo apt install xclip
```

### "Missing Python dependency"

Install Python dependencies:
```bash
pip install pytesseract Pillow pyperclip
```

### OCR Accuracy Issues

- Ensure the text in the screenshot is clear and not too small
- Install appropriate language packs for Tesseract
- For code/monospace text, the tool uses `--psm 6` which works well for uniform text blocks

## How It Works

1. **Capture**: Uses `scrot -s` to interactively capture a screen region
2. **Process**: Passes the image to Tesseract OCR with optimized settings
3. **Output**: Extracts text and copies it to clipboard using `xclip` or `pyperclip`
4. **Cleanup**: Removes temporary screenshot files

## Project Structure

```
extract/
├── snapocr.py          # Main OCR tool script
├── setup_hotkey.py     # Keyboard shortcut configuration script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## License

This project is open source. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
