#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送 - 窗口定位版
自动获取微信窗口位置，计算相对坐标
"""

import sys
import time
import subprocess
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pyautogui
    import pyperclip
    import win32gui
    import win32con
except ImportError as e:
    print(f"请先安装依赖: pip install pyautogui pyperclip pywin32")
    print(f"缺少: {e}")
    sys.exit(1)

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


class WeChatMoments:
    """微信朋友圈自动化 - 窗口定位版"""

    def __init__(self):
        self.hwnd = None
        self.window_rect = None
        self.window_width = 0
        self.window_height = 0

    def find_wechat_window(self):
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
            self.hwnd = hwnd_list[0]
            self.window_rect = win32gui.GetWindowRect(self.hwnd)
            left, top, right, bottom = self.window_rect
            self.window_width = right - left
            self.window_height = bottom - top
            return True
        return False

    def print_window_info(self):
        """打印窗口信息"""
        if self.window_rect:
            left, top, right, bottom = self.window_rect
            print(f"\n微信窗口信息:")
            print(f"  位置: ({left}, {top}) 到 ({right}, {bottom})")
            print(f"  大小: {self.window_width} x {self.window_height}")

    def get_abs_pos(self, rel_x, rel_y):
        """
        将相对坐标转换为绝对坐标
        rel_x, rel_y: 相对于窗口左上角的百分比位置 (0-1)
        """
        if not self.window_rect:
            return None
        left, top = self.window_rect[0], self.window_rect[1]
        abs_x = int(left + self.window_width * rel_x)
        abs_y = int(top + self.window_height * rel_y)
        return abs_x, abs_y

    def click_at(self, rel_x, rel_y, desc=""):
        """点击相对位置"""
        pos = self.get_abs_pos(rel_x, rel_y)
        if pos:
            print(f"  点击 {desc}: ({pos[0]}, {pos[1]})")
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.5)
            return True
        return False

    def _create_default_image(self, path):
        """创建一个简单的默认图片"""
        try:
            from PIL import Image

            # 创建一个简单的渐变图片
            img = Image.new("RGB", (800, 800), color=(70, 130, 180))
            img.save(path)
            print(f"  已创建默认图片: {path}")
        except Exception as e:
            print(f"  创建图片失败: {e}")

    def activate_window(self):
        """激活微信窗口"""
        if self.hwnd:
            try:
                win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(self.hwnd)
                time.sleep(0.5)
                return True
            except:
                pass

        # 备用方法：快捷键
        pyautogui.hotkey("ctrl", "alt", "w")
        time.sleep(1)

    def send_moments(self, text, image_path=None, dry_run=False):
        """
        发送朋友圈

        Args:
            text: 朋友圈内容
            image_path: 图片路径（可选）
            dry_run: 是否模拟运行
        """
        print("\n" + "=" * 50)
        print("微信朋友圈自动发送")
        print("=" * 50)

        # 保存图片路径
        self.image_path = image_path

        # 查找微信窗口
        if not self.find_wechat_window():
            print("✗ 未找到微信窗口，请确保微信已打开")
            return False

        self.print_window_info()

        if dry_run:
            print(f"\n[模拟运行] 将发送: {text}")
            print("\n将要点击的位置:")
            self._print_click_positions()
            return True

        try:
            # 1. 激活窗口
            print("\n步骤1: 激活微信窗口")
            self.activate_window()
            time.sleep(1)

            # 2. 点击朋友圈入口（左侧导航栏）
            print("\n步骤2: 打开朋友圈")
            # 朋友圈图标在左侧导航栏，大约在窗口高度的35%位置
            self.click_at(0.05, 0.35, "朋友圈入口")
            time.sleep(2)

            # 3. 点击相机按钮
            print("\n步骤3: 点击相机按钮")
            self.click_at(0.41, 0.32, "相机按钮")
            time.sleep(1)

            # 4. 选择"添加图片"（第一个选项）
            print("\n步骤4: 选择添加图片")
            # 点击第一个选项（添加图片）
            self.click_at(0.41, 0.38, "添加图片选项")
            time.sleep(1)

            # 5. 选择图片文件
            print("\n步骤5: 选择图片")
            # 使用用户指定的图片或默认图片
            if self.image_path and Path(self.image_path).exists():
                image_path = str(Path(self.image_path).absolute())
                print(f"  使用指定图片: {image_path}")
            else:
                # 使用默认图片
                default_image = Path(__file__).parent / "default_image.jpg"
                if not default_image.exists():
                    print("  创建默认图片...")
                    self._create_default_image(default_image)
                image_path = str(default_image)
                print(f"  使用默认图片: {image_path}")

            # 在文件选择对话框中输入图片路径
            time.sleep(1)
            pyperclip.copy(image_path)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(1)

            # 6. 确认选择图片
            print("\n步骤6: 确认图片")
            # 按"完成"按钮 - 在文件选择对话框中点击打开
            pyautogui.press("enter")
            time.sleep(2)

            # 等待图片加载到朋友圈编辑界面
            print("  等待图片加载...")
            time.sleep(2)

            # 7. 输入文字内容
            print("\n步骤7: 输入文字")
            # 直接粘贴文字（朋友圈编辑界面默认焦点在输入框）
            print(f"  输入内容: {text[:30]}...")
            pyperclip.copy(text)
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(1)

            # 8. 点击发表
            print("\n步骤8: 点击发表")
            # 发表按钮在右上角
            self.click_at(0.85, 0.15, "发表按钮")
            time.sleep(2)

            print("\n✓ 发送完成！")
            return True

        except Exception as e:
            print(f"\n✗ 发送失败: {e}")
            return False

    def _print_click_positions(self):
        """打印所有点击位置"""
        positions = [
            (0.05, 0.25, "朋友圈入口"),
            (0.85, 0.08, "相机按钮"),
            (0.85, 0.15, "发表文字"),
            (0.40, 0.30, "输入框"),
            (0.85, 0.90, "发表按钮"),
        ]
        for rel_x, rel_y, desc in positions:
            pos = self.get_abs_pos(rel_x, rel_y)
            print(f"  {desc}: ({pos[0]}, {pos[1]})")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="微信朋友圈自动发送")
    parser.add_argument("--text", required=True, help="朋友圈内容")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")

    args = parser.parse_args()

    wechat = WeChatMoments()
    success = wechat.send_moments(args.text, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
