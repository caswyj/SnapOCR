"""
OCR text extraction with LaTeX conversion support.
"""

import os
import re
from typing import Optional, Tuple
from PIL import Image

try:
    import pytesseract
except ImportError:
    pytesseract = None

# Lazy-loaded LaTeX OCR model
_latex_model = None


def _get_latex_model():
    """Lazy load the LaTeX OCR model."""
    global _latex_model
    if _latex_model is None:
        try:
            from pix2tex.cli import LatexOCR
            _latex_model = LatexOCR()
        except ImportError:
            print("Warning: pix2tex not installed. LaTeX conversion unavailable.")
            return None
        except Exception as e:
            print(f"Warning: Could not load LaTeX model: {e}")
            return None
    return _latex_model


def detect_math_content(text: str) -> bool:
    """
    Detect if text contains mathematical content.

    Args:
        text: The extracted text to analyze.

    Returns:
        True if mathematical content is detected.
    """
    # Common mathematical symbols and patterns
    math_patterns = [
        r'[=+\-*/^]',  # Basic operators
        r'[∑∫∏∂∇]',    # Calculus symbols
        r'[α-ωΑ-Ω]',   # Greek letters
        r'\\frac',     # LaTeX fractions
        r'\\sqrt',     # Square roots
        r'\\sum',      # Summation
        r'\\int',      # Integral
        r'[x-z]\s*[=^]',  # Variables with operators
        r'\d+\s*[xy]\s*=',  # Equations
        r'\([x-z]\)',  # Variables in parentheses
        r'\\[a-zA-Z]+',  # LaTeX commands
    ]

    for pattern in math_patterns:
        if re.search(pattern, text):
            return True
    return False


def contains_math_symbols(image: Image.Image) -> bool:
    """
    Heuristic check if image likely contains mathematical formulas.

    Args:
        image: PIL Image to analyze.

    Returns:
        True if image likely contains math.
    """
    # Convert to grayscale for analysis
    gray = image.convert('L')

    # Quick OCR to check for math symbols
    if pytesseract is None:
        return False

    try:
        # Quick scan with basic config
        text = pytesseract.image_to_string(gray, config='--psm 6')
        return detect_math_content(text)
    except Exception:
        return False


def extract_text(
    image_path: str,
    language: str = 'eng+chi_sim',
    tesseract_path: Optional[str] = None,
    latex_mode: bool = False,
    auto_detect_math: bool = True
) -> Tuple[str, Optional[str]]:
    """
    Extract text from an image using OCR with optional LaTeX conversion.

    Args:
        image_path: Path to the image file.
        language: Tesseract language code(s), e.g., 'eng', 'chi_sim', 'eng+chi_sim'.
        tesseract_path: Optional path to Tesseract executable.
        latex_mode: Force LaTeX conversion for the entire image.
        auto_detect_math: Automatically detect and convert math regions.

    Returns:
        Tuple of (extracted_text, latex_result) where latex_result may be None.
    """
    if pytesseract is None:
        raise ImportError("pytesseract is not installed. Install with: pip install pytesseract")

    # Set Tesseract path if provided
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Load image
    image = Image.open(image_path)

    # Configure Tesseract for optimal text extraction
    # --oem 3: Use LSTM neural net engine
    # --psm 6: Assume single uniform block of text
    custom_config = r'--oem 3 --psm 6'

    # Check if requested language is available
    try:
        available_langs = pytesseract.get_languages()
        requested_langs = language.split('+')
        missing_langs = [lang for lang in requested_langs if lang not in available_langs]

        if missing_langs:
            print(f"Warning: Language data not found: {missing_langs}")
            print(f"Available languages: {available_langs}")
            # Fall back to available languages
            available_requested = [lang for lang in requested_langs if lang in available_langs]
            if available_requested:
                language = '+'.join(available_requested)
            else:
                language = 'eng' if 'eng' in available_langs else available_langs[0]
                print(f"Using fallback language: {language}")
    except Exception:
        pass  # Continue with requested language

    # Extract text
    try:
        text = pytesseract.image_to_string(
            image,
            lang=language,
            config=custom_config
        )
        text = text.strip()
    except Exception as e:
        print(f"Error during OCR: {e}")
        text = ""

    # LaTeX conversion
    latex_result = None

    if latex_mode or (auto_detect_math and contains_math_symbols(image)):
        model = _get_latex_model()
        if model is not None:
            try:
                latex_result = model(image)
                if latex_result:
                    latex_result = latex_result.strip()
            except Exception as e:
                print(f"Warning: LaTeX conversion failed: {e}")

    return text, latex_result


def format_result(text: str, latex: Optional[str] = None) -> str:
    """
    Format the OCR result with optional LaTeX.

    Args:
        text: The extracted text.
        latex: Optional LaTeX result.

    Returns:
        Formatted result string.
    """
    result_parts = []

    if text:
        result_parts.append(text)

    if latex:
        result_parts.append(f"\n[LaTeX]: {latex}")

    return '\n'.join(result_parts).strip()