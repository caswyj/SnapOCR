#!/usr/bin/env python3
"""
SnapOCR Entry Point for PyInstaller packaging.
This file uses absolute imports to work correctly when bundled.
"""

import sys
import os

# Add the package path when running from source
if __name__ == '__main__':
    # When bundled by PyInstaller, the package is at the root
    if getattr(sys, 'frozen', False):
        # Running as bundled app
        bundle_dir = sys._MEIPASS
        sys.path.insert(0, bundle_dir)

from snapocr.main import main

if __name__ == '__main__':
    sys.exit(main())
