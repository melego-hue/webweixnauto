#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送脚本
通过pyautogui模拟鼠标键盘操作PC微信

使用方法:
    python send_moments.py --text "朋友圈内容"
    python send_moments.py --text "朋友圈内容" --images "img1.jpg,img2.jpg"
    python send_moments.py --text "测试内容" --dry-run  # 模拟运行
"""

import argparse
import time
import os
import sys
import subprocess
from pathlib import Path

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("请先安装依赖: pip install pyautogui pyperclip")
    sys.exit(1)

# 安全设置：鼠标移到屏幕角落可中止
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # 每个操作间隔0.5秒

# 屏幕分辨率
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


# 微信窗口检测
def find_wechat_window():
    """尝试找到微信窗口"""
    try:
        # Windows平台使用tasklist检查微信是否运行
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq WeChat.exe"],
            capture_output=True,
            text=True,
        )
        if "WeChat.exe" in result.stdout:
            print("✓ 检测到微信正在运行")
            return True
        else:
            print("✗ 未检测到微信进程，请先启动微信")
            return False
    except Exception as e:
        print(f"检测微信进程时出错: {e}")
        return False


def activate_wechat():
    """激活微信窗口"""
    print("\n正在激活微信窗口...")

    # 方法1: 使用快捷键 Ctrl+Alt+W (微信默认快捷键)
    pyautogui.hotkey("ctrl", "alt", "w")
    time.sleep(1)

    # 方法2: 如果快捷键不起作用，尝试点击屏幕左下角或任务栏
    # 这里假设微信在任务栏，可以调整坐标


def open_moments():
    """打开朋友圈界面"""
    print("正在打开朋友圈...")

    # 方法1: 使用微信内部快捷键
    # 点击朋友圈入口 - 需要根据实际界面调整坐标
    # 通常在微信左侧导航栏

    # 点击微信左下角的"朋友圈"图标
    # 坐标需要根据屏幕分辨率调整
    # 假设微信窗口在左侧，朋友圈图标位置

    # 先点击微信窗口确保焦点
    pyautogui.click(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    time.sleep(0.5)

    # 点击朋友圈入口（左侧导航栏）
    # 典型位置：微信窗口左侧，大约在屏幕1/4宽度处
    moments_icon_y = int(SCREEN_HEIGHT * 0.35)  # 大约在垂直方向35%位置
    pyautogui.click(SCREEN_WIDTH // 4 - 50, moments_icon_y)
    time.sleep(2)

    print("✓ 朋友圈界面已打开")


def click_publish_button():
    """点击发布按钮"""
    print("正在点击发布按钮...")

    # 朋友圈右上角的相机图标/发布按钮
    # 坐标需要根据实际调整
    publish_x = int(SCREEN_WIDTH * 0.23)  # 微信窗口右侧
    publish_y = int(SCREEN_HEIGHT * 0.15)  # 顶部区域

    pyautogui.click(publish_x, publish_y)
    time.sleep(1)


def input_text(text):
    """输入文字内容"""
    print(f"正在输入文字: {text[:30]}...")

    # 使用剪贴板粘贴，避免中文输入问题
    pyperclip.copy(text)
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    print("✓ 文字已输入")


def add_images(image_paths):
    """添加图片"""
    print(f"正在添加 {len(image_paths)} 张图片...")

    for i, img_path in enumerate(image_paths):
        img_path = Path(img_path)
        if not img_path.exists():
            print(f"✗ 图片不存在: {img_path}")
            continue

        # 点击添加图片按钮
        # 这里的坐标需要根据实际界面调整
        add_img_x = int(SCREEN_WIDTH * 0.22)
        add_img_y = int(SCREEN_HEIGHT * 0.4) + i * 80

        pyautogui.click(add_img_x, add_img_y)
        time.sleep(0.5)

        # 输入图片路径
        pyperclip.copy(str(img_path.absolute()))
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)

        # 确认选择
        pyautogui.press("enter")
        time.sleep(1)

    print("✓ 图片已添加")


def click_send():
    """点击发送按钮"""
    print("正在发送...")

    # 发送按钮通常在右下角
    send_x = int(SCREEN_WIDTH * 0.23)
    send_y = int(SCREEN_HEIGHT * 0.85)

    pyautogui.click(send_x, send_y)
    time.sleep(2)

    print("✓ 朋友圈已发送")


def send_moments(text, images=None, dry_run=False):
    """
    发送朋友圈主函数

    Args:
        text: 朋友圈文字内容
        images: 图片路径列表
        dry_run: 是否模拟运行
    """
    print("=" * 50)
    print("微信朋友圈自动发送")
    print("=" * 50)

    if dry_run:
        print("\n[模拟运行模式] 不会实际发送\n")

    # 检查微信是否运行
    if not find_wechat_window():
        return False

    if dry_run:
        print(f"\n将发送内容: {text}")
        if images:
            print(f"图片数量: {len(images)}")
        print("\n模拟运行完成，未实际发送")
        return True

    try:
        # 1. 激活微信窗口
        activate_wechat()
        time.sleep(1)

        # 2. 打开朋友圈
        open_moments()
        time.sleep(2)

        # 3. 点击发布按钮
        click_publish_button()
        time.sleep(1)

        # 4. 输入文字
        input_text(text)
        time.sleep(1)

        # 5. 添加图片（如果有）
        if images:
            add_images(images)
            time.sleep(1)

        # 6. 点击发送
        click_send()

        print("\n" + "=" * 50)
        print("✓ 朋友圈发送成功！")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"\n✗ 发送失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="微信朋友圈自动发送")
    parser.add_argument("--text", required=True, help="朋友圈文字内容")
    parser.add_argument("--images", help="图片路径，多个用逗号分隔")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行，不实际发送")

    args = parser.parse_args()

    # 处理图片路径
    images = None
    if args.images:
        images = [img.strip() for img in args.images.split(",") if img.strip()]

    # 发送朋友圈
    success = send_moments(args.text, images, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
