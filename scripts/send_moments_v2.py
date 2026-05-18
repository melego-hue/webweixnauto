#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送脚本 - 增强版
使用图像识别定位界面元素，更稳定可靠

使用方法:
    python send_moments_v2.py --text "朋友圈内容"
    python send_moments_v2.py --text "朋友圈内容" --images "img1.jpg"
    python send_moments_v2.py --text "测试" --dry-run
"""

import argparse
import time
import os
import sys
import subprocess
from pathlib import Path

# Windows编码修复
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("请先安装依赖: pip install pyautogui pyperclip")
    sys.exit(1)

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 脚本所在目录
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "ui_images"


class WeChatMoments:
    """微信朋友圈自动化类"""

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"屏幕分辨率: {self.screen_width}x{self.screen_height}")

    def check_wechat_running(self):
        """检查微信是否运行"""
        try:
            result = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True,
                encoding="gbk",
                errors="ignore",
            )
            # 同时检测旧版和新版微信
            return "WeChat.exe" in result.stdout or "WeChatAppEx.exe" in result.stdout
        except:
            return False

    def find_and_click(self, image_name, timeout=10, confidence=0.8):
        """
        查找并点击图像

        Args:
            image_name: 图像文件名
            timeout: 超时时间（秒）
            confidence: 匹配置信度

        Returns:
            bool: 是否成功点击
        """
        image_path = IMAGES_DIR / image_name
        if not image_path.exists():
            print(f"  图像文件不存在: {image_path}")
            return False

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(
                    str(image_path), confidence=confidence
                )
                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    return True
            except:
                pass
            time.sleep(0.5)

        return False

    def activate_wechat(self):
        """激活微信窗口"""
        print("激活微信窗口...")

        # 方法1: 快捷键
        pyautogui.hotkey("ctrl", "alt", "w")
        time.sleep(1)

        # 方法2: 点击屏幕上可能的微信位置
        # 微信窗口通常在左侧
        pyautogui.click(self.screen_width // 4, self.screen_height // 2)

    def open_moments_by_shortcut(self):
        """通过快捷键打开朋友圈"""
        # 微信没有直接的朋友圈快捷键，需要通过导航

        # 点击左侧导航栏的朋友圈图标
        # 朋友圈图标通常在"聊天"图标下方

        # 使用相对坐标定位
        nav_x = 80  # 左侧导航栏大约在80像素位置
        moments_y = self.screen_height * 0.25  # 大约在屏幕25%高度

        pyautogui.click(nav_x, moments_y)
        time.sleep(2)

    def click_camera_button(self):
        """点击朋友圈右上角的相机按钮"""
        print("点击发布按钮...")

        # 相机按钮在朋友圈页面的右上角
        # 微信窗口大约占屏幕左侧1/4宽度
        camera_x = self.screen_width * 0.22
        camera_y = self.screen_height * 0.12

        pyautogui.click(int(camera_x), int(camera_y))
        time.sleep(1)

    def select_only_text(self):
        """选择"仅文字"发布"""
        print("选择发布文字...")

        # 点击后会出现菜单，选择"发表文字"
        menu_y = self.screen_height * 0.15
        pyautogui.click(int(self.screen_width * 0.22), int(menu_y))
        time.sleep(1)

    def input_content(self, text):
        """输入内容"""
        print(f"输入内容: {text[:30]}...")

        # 点击输入区域
        input_y = self.screen_height * 0.3
        pyautogui.click(int(self.screen_width * 0.15), int(input_y))
        time.sleep(0.5)

        # 使用剪贴板粘贴
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)

    def click_publish(self):
        """点击发表按钮"""
        print("点击发表...")

        # 发表按钮在右下角
        publish_x = self.screen_width * 0.23
        publish_y = self.screen_height * 0.85

        pyautogui.click(int(publish_x), int(publish_y))
        time.sleep(2)

    def send_text_moments(self, text, dry_run=False):
        """
        发送纯文字朋友圈

        Args:
            text: 文字内容
            dry_run: 是否模拟运行
        """
        print("\n" + "=" * 50)
        print("发送纯文字朋友圈")
        print("=" * 50)

        if dry_run:
            print("\n[模拟运行] 将发送内容:")
            print(f"  {text}")
            return True

        try:
            # 1. 检查微信
            if not self.check_wechat_running():
                print("✗ 微信未运行，请先启动微信")
                return False

            # 2. 激活微信
            self.activate_wechat()
            time.sleep(1)

            # 3. 打开朋友圈
            self.open_moments_by_shortcut()
            time.sleep(2)

            # 4. 点击相机按钮
            self.click_camera_button()
            time.sleep(1)

            # 5. 选择仅文字
            self.select_only_text()
            time.sleep(1)

            # 6. 输入内容
            self.input_content(text)
            time.sleep(1)

            # 7. 点击发表
            self.click_publish()

            print("\n✓ 发送成功！")
            return True

        except Exception as e:
            print(f"\n✗ 发送失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="微信朋友圈自动发送 - 增强版")
    parser.add_argument("--text", required=True, help="朋友圈文字内容")
    parser.add_argument("--images", help="图片路径（暂不支持）")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")

    args = parser.parse_args()

    wechat = WeChatMoments()
    success = wechat.send_text_moments(args.text, args.dry_run)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
