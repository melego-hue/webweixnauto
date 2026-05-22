#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
截图工具 - 帮助截取微信界面元素
"""

import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
except ImportError:
    print("请先安装: pip install pyautogui")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "ui_images"


def capture_region(name, desc):
    """截取屏幕区域"""
    print(f"\n准备截取: {desc}")
    print("3秒后开始，请把鼠标移到目标区域的【左上角】...")
    time.sleep(3)

    x1, y1 = pyautogui.position()
    print(f"左上角: ({x1}, {y1})")
    print("现在把鼠标移到【右下角】...")
    time.sleep(3)

    x2, y2 = pyautogui.position()
    print(f"右下角: ({x2}, {y2})")

    # 截图
    width = x2 - x1
    height = y2 - y1
    if width > 0 and height > 0:
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        save_path = IMAGES_DIR / f"{name}.png"
        screenshot.save(save_path)
        print(f"✓ 已保存: {save_path}")
    else:
        print("✗ 区域无效")


def main():
    # 创建目录
    IMAGES_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("微信朋友圈截图工具")
    print("=" * 60)
    print("\n需要截取以下界面元素:")
    print("1. 朋友圈入口图标（微信左侧导航栏）")
    print("2. 相机按钮（朋友圈页面）")
    print("3. 添加图片选项（点击相机后的菜单第一项）")
    print("4. 发表按钮（朋友圈编辑页面右上角）")

    items = [
        ("moments_icon", "朋友圈入口图标"),
        ("camera_btn", "相机按钮"),
        ("add_image", "添加图片选项"),
        ("publish_btn", "发表按钮"),
    ]

    for name, desc in items:
        input(f"\n按回车开始截取【{desc}】...")
        capture_region(name, desc)

    print("\n" + "=" * 60)
    print("截图完成！")
    print(f"图片保存在: {IMAGES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
