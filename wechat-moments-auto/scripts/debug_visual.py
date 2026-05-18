#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈调试 - 可视化版本
一步步执行，让你看到每次点击的位置
"""

import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
    import pyperclip
    import win32gui
    import win32con
except ImportError:
    print("请先安装依赖: pip install pyautogui pyperclip pywin32")
    sys.exit(1)

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


def find_wechat_window():
    """查找微信窗口"""

    def callback(hwnd, hwnd_list):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "微信" in title:
                hwnd_list.append(hwnd)
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)

    if hwnd_list:
        hwnd = hwnd_list[0]
        rect = win32gui.GetWindowRect(hwnd)
        return hwnd, rect
    return None, None


def get_abs_pos(rect, rel_x, rel_y):
    """相对坐标转绝对坐标"""
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return int(left + width * rel_x), int(top + height * rel_y)


def move_and_show(rect, rel_x, rel_y, desc):
    """移动鼠标到位置并显示信息"""
    pos = get_abs_pos(rect, rel_x, rel_y)
    print(f"\n移动到: {desc}")
    print(f"  相对位置: ({rel_x:.2f}, {rel_y:.2f})")
    print(f"  绝对坐标: ({pos[0]}, {pos[1]})")

    # 先移动鼠标（不点击）
    pyautogui.moveTo(pos[0], pos[1], duration=0.5)

    # 让用户确认
    print("  请确认鼠标是否在正确位置上")
    return pos


def main():
    print("=" * 60)
    print("微信朋友圈调试工具 - 可视化版本")
    print("=" * 60)

    # 查找微信窗口
    hwnd, rect = find_wechat_window()
    if not rect:
        print("\n✗ 未找到微信窗口")
        return

    left, top, right, bottom = rect
    print(f"\n微信窗口: ({left}, {top}) 到 ({right}, {bottom})")
    print(f"窗口大小: {right - left} x {bottom - top}")

    print("\n" + "-" * 60)
    print("现在会依次移动鼠标到各个位置")
    print("请观察鼠标位置是否正确")
    print("如果不正确，告诉我应该往哪个方向调整")
    print("-" * 60)

    # 激活窗口
    try:
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass
    time.sleep(1)

    # 步骤1: 朋友圈入口
    input("\n按回车开始第一步: 朋友圈入口...")
    move_and_show(rect, 0.05, 0.25, "朋友圈入口")

    # 步骤2: 相机按钮
    input("\n按回车继续第二步: 相机按钮...")
    move_and_show(rect, 0.85, 0.08, "相机按钮")

    # 步骤3: 发表文字
    input("\n按回车继续第三步: 发表文字菜单...")
    move_and_show(rect, 0.85, 0.15, "发表文字")

    # 步骤4: 输入框
    input("\n按回车继续第四步: 输入框...")
    move_and_show(rect, 0.40, 0.30, "输入框")

    # 步骤5: 发表按钮
    input("\n按回车继续第五步: 发表按钮...")
    move_and_show(rect, 0.85, 0.90, "发表按钮")

    print("\n" + "=" * 60)
    print("调试完成！")
    print("请告诉我哪些位置不对，需要往哪个方向调整")
    print("=" * 60)


if __name__ == "__main__":
    main()
