#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UI Capture Tool - Capture WeChat UI elements
"""

import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
except ImportError:
    print("Please install: pip install pyautogui")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR.parent / "ui_images"


def capture_region(name, desc):
    """Capture screen region"""
    print(f"\nPreparing to capture: {desc}")
    print("Move mouse to TOP-LEFT corner of target area in 3 seconds...")
    time.sleep(3)

    x1, y1 = pyautogui.position()
    print(f"Top-left: ({x1}, {y1})")
    print("Now move mouse to BOTTOM-RIGHT corner...")
    time.sleep(3)

    x2, y2 = pyautogui.position()
    print(f"Bottom-right: ({x2}, {y2})")

    width = x2 - x1
    height = y2 - y1
    if width > 0 and height > 0:
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        save_path = IMAGES_DIR / f"{name}.png"
        screenshot.save(save_path)
        print(f"OK: Saved to: {save_path}")
    else:
        print("FAIL: Invalid region")


def main():
    IMAGES_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("WeChat Moments Capture Tool")
    print("=" * 60)
    print("\nNeed to capture following UI elements:")
    print("1. Moments icon (left navigation bar)")
    print("2. Camera button (moments page)")
    print("3. Add image option (first item in menu)")
    print("4. Publish button (top-right of editor)")

    items = [
        ("moments_icon", "Moments icon"),
        ("camera_btn", "Camera button"),
        ("add_image", "Add image option"),
        ("publish_btn", "Publish button"),
    ]

    for name, desc in items:
        input(f"\nPress Enter to capture [{desc}]...")
        capture_region(name, desc)

    print("\n" + "=" * 60)
    print("Capture completed!")
    print(f"Images saved to: {IMAGES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()