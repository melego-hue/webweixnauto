#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈坐标调试工具
帮助你找到正确的点击位置

使用方法:
    python debug_coords.py
    然后按照提示操作，移动鼠标到目标位置，记录坐标
"""

import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
except ImportError:
    print("请先安装: pip install pyautogui")
    sys.exit(1)

print("=" * 60)
print("微信朋友圈坐标调试工具")
print("=" * 60)
print()
print("使用说明:")
print("1. 把鼠标移动到目标位置")
print("2. 等待3秒，程序会显示当前坐标")
print("3. 记录下坐标值")
print()
print("需要定位的位置:")
print("  - 朋友圈入口图标（微信左侧导航栏）")
print("  - 朋友圈页面的相机/发布按钮")
print("  - 发表文字菜单项")
print("  - 输入框位置")
print("  - 发表按钮")
print()
print("3秒后开始...")
print()

time.sleep(3)

print("\n按 Ctrl+C 退出\n")
print("-" * 60)

try:
    last_pos = None
    while True:
        x, y = pyautogui.position()
        if (x, y) != last_pos:
            print(f"当前坐标: X={x:4d}, Y={y:4d}")
            last_pos = (x, y)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n已退出")
