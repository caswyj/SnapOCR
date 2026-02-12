#!/usr/bin/env python3
"""
Snapshot + OCR Extraction Tool

Captures a screenshot region selected by mouse drag,
uses OCR to extract text/code, and copies to clipboard.
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
    import pyperclip
except ImportError as e:
    print(f"Error: Missing Python dependency - {e}")
    print("Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)


def check_dependencies():
    """Check if required system tools are installed. Returns capture tool name."""
    # Check for screenshot tool (prefer scrot, fallback to import)
    capture_tool = None
    result = subprocess.run(['which', 'scrot'], capture_output=True)
    if result.returncode == 0:
        capture_tool = 'scrot'
    else:
        result = subprocess.run(['which', 'import'], capture_output=True)
        if result.returncode == 0:
            capture_tool = 'import'

    if not capture_tool:
        print("Error: No screenshot tool found.")
        print("Install one of: scrot (sudo apt install scrot)")
        print("              or ImageMagick (sudo apt install imagemagick)")
        sys.exit(1)

    # Check for tesseract
    result = subprocess.run(['which', 'tesseract'], capture_output=True)
    if result.returncode != 0:
        print("Error: 'tesseract' is not installed.")
        print("Install with: sudo apt install tesseract-ocr")
        sys.exit(1)

    return capture_tool


def select_region(capture_tool: str) -> str:
    """
    Capture a selected region using the available screenshot tool.
    Returns the path to the captured image file.
    """
    # Create temp file for screenshot
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'snapocr_temp.png')

    # Remove existing temp file if present
    if os.path.exists(temp_path):
        os.remove(temp_path)

    print("Select a region with your mouse (drag to select, Esc to cancel)...")

    if capture_tool == 'scrot':
        # Use scrot with -s for selection mode, -z for silent
        result = subprocess.run(
            ['scrot', '-s', '-z', temp_path],
            capture_output=True
        )
    else:  # import (ImageMagick)
        # import allows region selection with -silent flag
        result = subprocess.run(
            ['import', temp_path],
            capture_output=True
        )

    # Check if capture was successful
    if result.returncode != 0:
        print("Capture cancelled or failed.")
        sys.exit(0)

    if not os.path.exists(temp_path):
        print("No image captured.")
        sys.exit(0)

    return temp_path


def extract_text(image_path: str) -> str:
    """
    Use Tesseract OCR to extract text with preserved layout.

    Args:
        image_path: Path to the image file

    Returns:
        Extracted text string
    """
    try:
        # Load image
        image = Image.open(image_path)

        # Configure Tesseract for code/text extraction
        # --psm 6: Assume a single uniform block of text (preserves layout)
        # --oem 3: Default OCR Engine Mode (uses LSTM if available)
        custom_config = r'--oem 3 --psm 6'

        # Extract text
        text = pytesseract.image_to_string(image, config=custom_config)

        return text.strip()

    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""


def copy_to_clipboard(text: str) -> bool:
    """
    Copy extracted text to clipboard.

    Args:
        text: Text to copy

    Returns:
        True if successful, False otherwise
    """
    # Try xclip first (most reliable on Linux/X11)
    result = subprocess.run(['which', 'xclip'], capture_output=True)
    if result.returncode == 0:
        try:
            subprocess.run(
                ['xclip', '-selection', 'clipboard'],
                input=text.encode('utf-8'),
                check=True
            )
            return True
        except Exception as e:
            pass

    # Try xsel as fallback
    result = subprocess.run(['which', 'xsel'], capture_output=True)
    if result.returncode == 0:
        try:
            subprocess.run(
                ['xsel', '--clipboard', '--input'],
                input=text.encode('utf-8'),
                check=True
            )
            return True
        except Exception as e:
            pass

    # Try pyperclip as last resort
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        pass

    print("Error: Could not copy to clipboard.")
    print("Install xclip: sudo apt install xclip")
    return False


def main():
    """Main CLI entry point."""
    # Check system dependencies and get capture tool
    capture_tool = check_dependencies()

    # Capture screenshot region
    image_path = select_region(capture_tool)

    # Extract text via OCR
    print("Extracting text...")
    text = extract_text(image_path)

    if not text:
        print("No text detected in the selected region.")
        return

    # Copy to clipboard
    if copy_to_clipboard(text):
        print(f"Text copied to clipboard ({len(text)} characters)")
        print("-" * 40)
        print(text[:200] + "..." if len(text) > 200 else text)
        print("-" * 40)
    else:
        # Fallback: print to stdout
        print("-" * 40)
        print(text)
        print("-" * 40)

    # Cleanup temp file
    try:
        os.remove(image_path)
    except:
        pass


if __name__ == '__main__':
    main()
