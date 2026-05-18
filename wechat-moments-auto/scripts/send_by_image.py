#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送 - 图像识别版
通过识别界面元素图片来定位点击位置
"""

import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("请先安装依赖: pip install pyautogui pyperclip")
    sys.exit(1)

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "ui_images"


def find_and_click(image_name, timeout=10, confidence=0.8):
    """
    查找并点击图像

    Args:
        image_name: 图像文件名（不含扩展名）
        timeout: 超时时间（秒）
        confidence: 匹配置信度 (0-1)

    Returns:
        bool: 是否成功点击
    """
    image_path = IMAGES_DIR / f"{image_name}.png"
    if not image_path.exists():
        print(f"  ✗ 图片不存在: {image_path}")
        print(f"  请先运行 capture_ui.py 截取界面元素")
        return False

    print(f"  查找: {image_name}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(str(image_path), confidence=confidence)
            if location:
                center = pyautogui.center(location)
                print(f"  ✓ 找到，点击: ({center.x}, {center.y})")
                pyautogui.click(center.x, center.y)
                return True
        except Exception as e:
            pass
        time.sleep(0.5)

    print(f"  ✗ 未找到: {image_name}")
    return False


def send_moments(text, image_path=None, dry_run=False):
    """
    发送朋友圈

    Args:
        text: 朋友圈内容
        image_path: 图片路径（可选）
        dry_run: 是否模拟运行
    """
    print("\n" + "=" * 50)
    print("微信朋友圈自动发送（图像识别版）")
    print("=" * 50)

    if dry_run:
        print(f"\n[模拟运行] 将发送: {text}")
        return True

    try:
        # 1. 激活微信窗口（快捷键）
        print("\n步骤1: 激活微信")
        pyautogui.hotkey("ctrl", "alt", "w")
        time.sleep(1)

        # 2. 点击朋友圈入口
        print("\n步骤2: 打开朋友圈")
        if not find_and_click("moments_icon", timeout=5):
            print("  提示: 请确保微信已打开")
            return False
        time.sleep(2)

        # 3. 点击相机按钮
        print("\n步骤3: 点击相机")
        if not find_and_click("camera_btn", timeout=5):
            return False
        time.sleep(1)

        # 4. 选择添加图片（按回车默认选中第一项）
        print("\n步骤4: 选择添加图片")
        print("  按回车选择第一项...")
        pyautogui.press("enter")
        time.sleep(1)

        # 5. 选择图片
        print("\n步骤5: 选择图片")
        if image_path and Path(image_path).exists():
            img = str(Path(image_path).absolute())
            print(f"  使用指定图片: {img}")
        else:
            # 从默认文件夹随机选择图片
            images_dir = SCRIPT_DIR / "images"
            if images_dir.exists():
                image_files = (
                    list(images_dir.glob("*.jpg"))
                    + list(images_dir.glob("*.png"))
                    + list(images_dir.glob("*.jpeg"))
                )
                if image_files:
                    import random

                    img = str(random.choice(image_files).absolute())
                    print(f"  随机选择图片: {img}")
                else:
                    print(f"  ✗ 图片文件夹为空: {images_dir}")
                    print(f"  请将图片放入该文件夹")
                    return False
            else:
                print(f"  ✗ 图片文件夹不存在: {images_dir}")
                return False

        # 输入图片路径
        pyperclip.copy(img)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(2)

        # 6. 输入文字
        print("\n步骤6: 输入文字")
        print(f"  内容: {text[:30]}...")
        pyperclip.copy(text)
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

        # 7. 点击发表按钮
        print("\n步骤7: 发表")
        if not find_and_click("publish_btn", timeout=5, confidence=0.9):
            print("  ✗ 未找到发表按钮")
            return False
        time.sleep(2)

        print("\n✓ 发送完成！")
        return True

    except Exception as e:
        print(f"\n✗ 发送失败: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="微信朋友圈自动发送")
    parser.add_argument("--text", required=True, help="朋友圈内容")
    parser.add_argument("--image", help="图片路径")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")

    args = parser.parse_args()
    success = send_moments(args.text, args.image, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
