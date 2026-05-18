#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WeChat Moments Auto Sender - Image Recognition Version
Locate elements by image recognition
"""

import sys
import time
import random
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("Please install: pip install pyautogui pyperclip")
    sys.exit(1)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR.parent / "ui_images"


def find_and_click(image_name, timeout=10, confidence=0.8, max_retries=2):
    """
    Find and click image with retry support

    Args:
        image_name: Image filename without extension
        timeout: Timeout in seconds
        confidence: Match confidence (0-1)
        max_retries: Maximum retries

    Returns:
        bool: Success or not
    """
    image_path = IMAGES_DIR / f"{image_name}.png"
    if not image_path.exists():
        print(f"  FAIL: Image not found: {image_path}")
        print(f"  Tip: Run capture_ui.py to capture UI elements")
        return False

    for attempt in range(max_retries):
        print(f"  Finding: {image_name} (attempt {attempt + 1}/{max_retries})...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
                if location:
                    center = pyautogui.center(location)
                    print(f"  OK: Found, clicking: ({center.x}, {center.y})")
                    pyautogui.click(center.x, center.y)
                    return True
            except Exception as e:
                pass
            time.sleep(0.3)

        print(f"  FAIL: Not found: {image_name}")
        if attempt < max_retries - 1:
            print(f"  Waiting 1 second before retry...")
            time.sleep(1)

    return False


def send_moments(text, image_path=None, dry_run=False):
    """
    Send moments

    Args:
        text: Moments content
        image_path: Image path (optional)
        dry_run: Simulate only
    """
    print("\n" + "=" * 50)
    print("WeChat Moments Auto Sender (Image Recognition)")
    print("=" * 50)

    if dry_run:
        print(f"\n[Dry Run] Will send: {text}")
        return True

    from wechat_utils import ensure_wechat_ready
    if not ensure_wechat_ready():
        print("  FAIL: WeChat not ready")
        return False

    try:
        print("\nStep 2: Open Moments")
        if not find_and_click("moments_icon", timeout=5, confidence=0.7):
            print("  Tip: Ensure WeChat main window is visible")
            return False
        time.sleep(2)

        print("\nStep 3: Click Camera")
        if not find_and_click("camera_btn", timeout=5, confidence=0.7):
            return False
        time.sleep(1)

        print("\nStep 4: Select Add Image")
        print("  Pressing Enter to select first option...")
        pyautogui.press("enter")
        time.sleep(1)

        print("\nStep 5: Select Image")
        if image_path and Path(image_path).exists():
            img = str(Path(image_path).absolute())
            print(f"  Using specified image: {img}")
        else:
            images_dir = SCRIPT_DIR.parent / "images"
            if images_dir.exists():
                image_files = (
                    list(images_dir.glob("*.jpg"))
                    + list(images_dir.glob("*.png"))
                    + list(images_dir.glob("*.jpeg"))
                )
                if image_files:
                    img = str(random.choice(image_files).absolute())
                    print(f"  Randomly selected: {img}")
                else:
                    print(f"  FAIL: Images folder empty: {images_dir}")
                    print(f"  Tip: Put images in this folder")
                    return False
            else:
                print(f"  FAIL: Images folder not found: {images_dir}")
                return False

        pyperclip.copy(img)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(2)

        print("\nStep 6: Input Text")
        print(f"  Content: {text[:30]}...")
        pyperclip.copy(text)
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        print("\nStep 7: Publish")
        if not find_and_click("publish_btn", timeout=5, confidence=0.9):
            print("  FAIL: Publish button not found")
            return False
        time.sleep(2)

        print("\nSUCCESS: Sent!")
        return True

    except Exception as e:
        print(f"\nERROR: Send failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="WeChat Moments Auto Sender")
    parser.add_argument("--text", required=True, help="Moments content")
    parser.add_argument("--image", help="Image path")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only")

    args = parser.parse_args()
    success = send_moments(args.text, args.image, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()