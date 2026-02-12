#!/usr/bin/env python3
"""Setup keyboard shortcut for SnapOCR."""

import subprocess
import os

def setup_hotkey():
    snapocr_path = "/home/wangyj/proj/extract/snapocr.py"

    # Get current custom keybindings
    result = subprocess.run(
        ["gsettings", "get", "org.gnome.settings-daemon.plugins.media-keys", "custom-keybindings"],
        capture_output=True, text=True
    )

    current = result.stdout.strip()

    if current == "@as []":
        # No existing keybindings
        new_bindings = "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"
    else:
        # Add new keybinding to existing ones
        new_bindings = current.replace("]", ", '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']")

    commands = [
        f"gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name 'SnapOCR'",
        f"gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command '/usr/bin/python3 {snapocr_path}'",
        f"gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding '<Ctrl>o'",
        f"gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \"{new_bindings}\""
    ]

    for cmd in commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print(f"OK: {cmd}")

    print("\nHotkey Ctrl+Z has been set up for SnapOCR.")
    print("You may need to log out and log back in for it to take effect.")

if __name__ == "__main__":
    setup_hotkey()
