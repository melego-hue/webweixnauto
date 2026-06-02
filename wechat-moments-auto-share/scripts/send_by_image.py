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

# Fix DPI scaling for 4K screens - MUST be before pyautogui import
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PerMonitorV2
except:
    pass

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


def get_edge_map(img_gray):
    """计算并模糊图像的 Canny 骨架边缘，提供对背景透明、无视色差、高宽容的特征匹配"""
    import cv2
    blurred = cv2.GaussianBlur(img_gray, (3, 3), 0)
    # 使用 Canny 算子提取边缘
    edges = cv2.Canny(blurred, 30, 100)
    # 对骨架线条进行微量模糊，创建缓和梯度，容忍 1-2 像素的缩放或渲染偏差
    edges_blurred = cv2.GaussianBlur(edges, (3, 3), 0)
    return edges_blurred


def bezier_move_to(target_x, target_y, duration=0.8):
    """使用三阶贝塞尔曲线模拟真人滑行轨迹移动鼠标（带有随机抖动与加减速）"""
    import random
    import time
    
    start_x, start_y = pyautogui.position()
    if start_x == target_x and start_y == target_y:
        return
        
    # 随机生成两个控制点，创造出自然的手部划行动作
    control_x1 = start_x + (target_x - start_x) * random.uniform(0.1, 0.4) + random.randint(-30, 30)
    control_y1 = start_y + (target_y - start_y) * random.uniform(0.1, 0.4) + random.randint(-30, 30)
    control_x2 = start_x + (target_x - start_x) * random.uniform(0.6, 0.9) + random.randint(-30, 30)
    control_y2 = start_y + (target_y - start_y) * random.uniform(0.6, 0.9) + random.randint(-30, 30)
    
    def get_bezier_point(t):
        x = (1-t)**3 * start_x + 3*(1-t)**2 * t * control_x1 + 3*(1-t) * t**2 * control_x2 + t**3 * target_x
        y = (1-t)**3 * start_y + 3*(1-t)**2 * t * control_y1 + 3*(1-t) * t**2 * control_y2 + t**3 * target_y
        return int(x), int(y)
        
    steps = int(duration * 60) # 仿真 60FPS 刷新率
    for i in range(steps + 1):
        t = i / steps
        # 缓动函数 Ease-In-Ease-Out，实现真人“起步慢-中间快-精准落点减速”
        t_smooth = t * t * (3 - 2 * t)
        bx, by = get_bezier_point(t_smooth)
        pyautogui.moveTo(bx, by)
        time.sleep(duration / steps)


def find_and_click(image_name, timeout=10, confidence=0.8, max_retries=2):
    """
    通过 Canny 骨架特征图及人机仿真方式匹配并点击 UI 元素
    """
    image_path = IMAGES_DIR / f"{image_name}.png"
    if not image_path.exists():
        print(f"  FAIL: Image not found: {image_path}")
        print(f"  Tip: Run capture_ui.py to capture UI elements")
        return False

    import cv2
    import numpy as np

    template_color = cv2.imread(str(image_path))
    if template_color is None:
        print(f"  FAIL: Cannot read image: {image_path}")
        return False
    template_gray = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)
    tH, tW = template_gray.shape
    
    # 提取模板的 Canny 骨架图
    template_edges = get_edge_map(template_gray)

    for attempt in range(max_retries):
        print(f"  Finding: {image_name} (attempt {attempt + 1}/{max_retries})...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                screenshot = pyautogui.screenshot()
                screenshot_np = np.array(screenshot)
                screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
                
                # 提取当前屏幕截图的 Canny 骨架图
                screenshot_edges = get_edge_map(screenshot_gray)

                # 多尺度骨架特征匹配
                best_val = 0
                best_loc = None
                best_scale = 1.0

                for scale in np.arange(0.8, 1.25, 0.05):
                    w = int(tW * scale)
                    h = int(tH * scale)
                    if w < 5 or h < 5 or w > screenshot_edges.shape[1] or h > screenshot_edges.shape[0]:
                        continue
                    resized = cv2.resize(template_edges, (w, h))
                    result = cv2.matchTemplate(screenshot_edges, resized, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(result)
                    if max_val > best_val:
                        best_val = max_val
                        best_loc = max_loc
                        best_scale = scale

                # 骨架比对阈值：对背景无关的骨架，0.80 已经极其安全且排他
                if best_val >= confidence:
                    center_x = best_loc[0] + int(tW * best_scale) // 2
                    center_y = best_loc[1] + int(tH * best_scale) // 2
                    
                    # 人机仿真：在按钮区域内引入随机偏移（+/- 4 像素），防止机器固定落点特征
                    offset_x = random.randint(-4, 4)
                    offset_y = random.randint(-4, 4)
                    final_x = center_x + offset_x
                    final_y = center_y + offset_y
                    
                    print(f"  OK: 找到元素 [{image_name}] (骨架相似度={best_val:.3f}), 正在进行贝塞尔仿真移鼠并点击: ({final_x}, {final_y})")
                    
                    # 仿真移动鼠标
                    bezier_move_to(final_x, final_y, duration=random.uniform(0.5, 1.0))
                    pyautogui.click()
                    
                    # 点击后的反应时间延时（0.5s - 1.5s 随机），模拟真人反应
                    time.sleep(random.uniform(0.5, 1.5))
                    return True
                else:
                    pass  # Not found, keep trying
            except Exception as e:
                pass
            time.sleep(0.3)

        print(f"  FAIL: Not found: {image_name} (best={best_val:.3f})")
        if attempt < max_retries - 1:
            print(f"  Waiting 1 second before retry...")
            time.sleep(1)

    return False


def wait_for_user_idle(idle_seconds=5):
    """
    检测用户是否正在操作电脑。如果在操作，则静默等待，直至用户完全闲置。
    """
    print(f"\n[占线检测] 正在确认您当前是否在使用电脑（避免抢占物理鼠标）...")
    last_pos = pyautogui.position()
    idle_start = time.time()
    
    while True:
        current_pos = pyautogui.position()
        # 如果鼠标位置发生偏移，说明用户在使用电脑，重新计时
        if current_pos != last_pos:
            last_pos = current_pos
            idle_start = time.time()
            print("  [占线] 检测到您的鼠标在移动，AI 助手已自动暂停等待...", end="\r")
        
        # 闲置时间达到设定值，可以安全介入
        if time.time() - idle_start >= idle_seconds:
            print("\n  [安全] 检测到您已闲置，AI 助手开始闪击执行...")
            break
        time.sleep(1)


def show_windows_toast(title, message):
    """
    使用 PowerShell 调用 Windows NotifyIcon，弹出原生气泡通知（免第三方依赖）
    """
    import subprocess
    ps_cmd = (
        f"[void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); "
        f"$notification = New-Object System.Windows.Forms.NotifyIcon; "
        f"$notification.Icon = [System.Drawing.SystemIcons]::Information; "
        f"$notification.BalloonTipIcon = 'Info'; "
        f"$notification.BalloonTipTitle = '{title}'; "
        f"$notification.BalloonTipText = '{message}'; "
        f"$notification.Visible = $True; "
        f"$notification.ShowBalloonTip(5000)"
    )
    try:
        subprocess.Popen(["powershell", "-Command", ps_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"  [Warning] Toast notify failed: {e}")


def send_feishu_notification(title, message):
    """
    向飞书机器人发送推送通知（通过 .env 中配置的 FEISHU_WEBHOOK_URL）
    """
    import requests
    # 优先加载配置
    env_path = Path("d:/AIWork/.env")
    webhook_url = None
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    if line.strip().startswith("FEISHU_WEBHOOK_URL="):
                        webhook_url = line.split("=", 1)[1].strip()
                        break
        except:
            pass
            
    if webhook_url:
        try:
            payload = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": [
                                [
                                    {"tag": "text", "text": message}
                                ]
                            ]
                        }
                    }
                }
            }
            response = requests.post(webhook_url, json=payload, timeout=5)
            if response.status_code == 200:
                print("  [通知] 飞书推送成功！")
                return True
        except Exception as e:
            print(f"  [Warning] Feishu notification failed: {e}")
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

    # 新增：占线退避检测，确保用户不处于活跃操作状态
    wait_for_user_idle(idle_seconds=5)

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
        if not find_and_click("publish_btn", timeout=5, confidence=0.7):
            print("  FAIL: Publish button not found")
            return False
        time.sleep(2)

        print("\nStep 8: Close Moments Window")
        pyautogui.press("esc")
        time.sleep(1)

        # 发送成功通知
        notify_title = "微信朋友圈发送成功 🚀"
        notify_msg = f"已成功发表朋友圈且已自动关闭窗口！\n文案：{text[:35]}..."
        show_windows_toast(notify_title, notify_msg)
        send_feishu_notification(notify_title, notify_msg)

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