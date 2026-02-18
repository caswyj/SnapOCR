"""
macOS platform-specific implementations.
"""

import os
import subprocess
import tempfile
from typing import Optional, Callable

from .base import (
    BaseScreenshotCapture,
    BaseClipboardManager,
    BaseHotkeyManager,
)


class MacOSScreenshotCapture(BaseScreenshotCapture):
    """macOS screenshot capture using built-in screencapture command."""

    def __init__(self):
        """Initialize macOS screenshot capture."""
        self._temp_dir = tempfile.gettempdir()

    def _get_temp_path(self) -> str:
        """Get a temporary file path for screenshot."""
        return os.path.join(self._temp_dir, 'snapocr_temp.png')

    def select_region(self) -> Optional[str]:
        """
        Capture a selected screen region using screencapture.

        Returns:
            Path to captured image or None if cancelled.
        """
        temp_path = self._get_temp_path()

        # Remove existing temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        print("Select a region with your mouse (drag to select, Esc to cancel)...")

        # Use macOS screencapture command
        # -i: interactive mode (user selects region)
        # -r: don't play sound
        # -x: don't play sound (alternative flag)
        result = subprocess.run(
            ['screencapture', '-i', '-r', temp_path],
            capture_output=True
        )

        # screencapture returns 0 on success, non-zero if cancelled
        if result.returncode != 0:
            return None

        if os.path.exists(temp_path):
            return temp_path
        return None

    def capture_full_screen(self) -> Optional[str]:
        """Capture the full screen."""
        temp_path = self._get_temp_path()

        if os.path.exists(temp_path):
            os.remove(temp_path)

        # -x: don't play sound
        result = subprocess.run(
            ['screencapture', '-x', temp_path],
            capture_output=True
        )

        if result.returncode == 0 and os.path.exists(temp_path):
            return temp_path
        return None

    def capture_window(self) -> Optional[str]:
        """Capture the currently focused window."""
        temp_path = self._get_temp_path()

        if os.path.exists(temp_path):
            os.remove(temp_path)

        # -l: capture window by ID (0 for focused window doesn't work, need to get window ID)
        # -o: capture window only (no shadow)
        # -w: select window interactively
        result = subprocess.run(
            ['screencapture', '-o', '-w', '-x', temp_path],
            capture_output=True
        )

        if result.returncode == 0 and os.path.exists(temp_path):
            return temp_path
        return None


class MacOSClipboardManager(BaseClipboardManager):
    """macOS clipboard manager using pbcopy and pbpaste."""

    def copy(self, text: str) -> bool:
        """Copy text to clipboard using pbcopy."""
        try:
            process = subprocess.Popen(
                ['pbcopy', 'w'],
                stdin=subprocess.PIPE,
                env={**os.environ, 'LANG': 'en_US.UTF-8'}
            )
            process.communicate(text.encode('utf-8'))
            return process.returncode == 0
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False

    def paste(self) -> str:
        """Get text from clipboard using pbpaste."""
        try:
            result = subprocess.run(
                ['pbpaste'],
                capture_output=True,
                text=True,
                env={**os.environ, 'LANG': 'en_US.UTF-8'}
            )
            return result.stdout
        except Exception as e:
            print(f"Error reading clipboard: {e}")
            return ""

    def simulate_paste(self) -> bool:
        """Simulate Cmd+V paste."""
        try:
            import pyautogui
            pyautogui.hotkey('command', 'v')
            return True
        except Exception as e:
            print(f"Error simulating paste: {e}")
            return False


class MacOSHotkeyManager(BaseHotkeyManager):
    """macOS hotkey manager using pynput."""

    def __init__(self):
        """Initialize hotkey manager."""
        self._hotkeys = {}
        self._listener = None
        self._running = False

    def _normalize_hotkey(self, hotkey: str) -> str:
        """Normalize hotkey string for pynput format."""
        hotkey = hotkey.lower().strip()

        # macOS-specific replacements
        replacements = {
            'ctrl': '<ctrl>',
            'alt': '<alt>',
            'shift': '<shift>',
            'cmd': '<cmd>',
            'command': '<cmd>',
            'super': '<cmd>',
            'win': '<cmd>',
            'meta': '<cmd>',
            'option': '<alt>',
        }

        parts = hotkey.replace(' ', '').split('+')
        normalized_parts = []

        for part in parts:
            if part in replacements:
                normalized_parts.append(replacements[part])
            elif len(part) == 1:
                normalized_parts.append(part)
            else:
                normalized_parts.append(f'<{part}>')

        return '+'.join(normalized_parts)

    def register(self, hotkey: str, callback: Callable[[], None]) -> bool:
        """Register a global hotkey."""
        try:
            normalized = self._normalize_hotkey(hotkey)
            self._hotkeys[normalized] = callback

            # Restart listener if running
            if self._running:
                self.stop()
                self.start()

            return True
        except Exception as e:
            print(f"Error registering hotkey: {e}")
            return False

    def unregister(self, hotkey: str) -> bool:
        """Unregister a hotkey."""
        try:
            normalized = self._normalize_hotkey(hotkey)
            if normalized in self._hotkeys:
                del self._hotkeys[normalized]

                # Restart listener if running
                if self._running:
                    self.stop()
                    self.start()

            return True
        except Exception as e:
            print(f"Error unregistering hotkey: {e}")
            return False

    def start(self) -> None:
        """Start listening for hotkeys."""
        if self._running:
            return

        try:
            from pynput import keyboard

            # Create hotkey listeners
            if self._hotkeys:
                self._listener = keyboard.GlobalHotKeys(self._hotkeys)
                self._listener.start()
                self._running = True
        except Exception as e:
            print(f"Error starting hotkey listener: {e}")
            print("Note: On macOS, you may need to grant Accessibility permissions.")
            print("System Preferences > Security & Privacy > Privacy > Accessibility")

    def stop(self) -> None:
        """Stop listening for hotkeys."""
        if self._listener:
            self._listener.stop()
            self._listener = None
        self._running = False

    def is_registered(self, hotkey: str) -> bool:
        """Check if hotkey is registered."""
        normalized = self._normalize_hotkey(hotkey)
        return normalized in self._hotkeys