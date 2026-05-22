#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WeChat Window Utilities Module
Enhanced WeChat window detection and activation
"""

import subprocess
import time
import os
import ctypes
from ctypes import wintypes

try:
    import pyautogui
except ImportError:
    print("Please install: pip install pyautogui")
    raise

user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9


def is_wechat_running():
    """Check if WeChat is running (supports multiple versions)"""
    try:
        result = subprocess.run(
            ["tasklist"],
            capture_output=True,
            text=True,
            encoding="gbk",
            errors="ignore"
        )
        processes = ["WeChat.exe", "WeChatAppEx.exe", "WeChatWeb.exe"]
        running = any(p in result.stdout for p in processes)
        if running:
            print("  OK: WeChat process found")
        else:
            print("  FAIL: WeChat process not found")
        return running
    except Exception as e:
        print(f"  ERROR: Process check failed: {e}")
        return False


def get_wechat_window_handle():
    """Get WeChat window handle (prioritize visible windows)"""
    HWND = wintypes.HWND
    
    def callback(hwnd, extra):
        try:
            if not user32.IsWindowVisible(hwnd):
                return True
            
            length = user32.GetWindowTextLengthA(hwnd)
            if length == 0:
                return True
            
            buffer = ctypes.create_string_buffer(length + 1)
            user32.GetWindowTextA(hwnd, buffer, length + 1)
            title = buffer.value.decode('gbk', errors='ignore')
            
            if 'WeChat' in title or '微信' in title:
                extra.append(hwnd)
        except:
            pass
        return True
    
    windows = []
    user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, HWND, ctypes.py_object)(callback), windows)
    
    if windows:
        print(f"  OK: Found WeChat window handle: {hex(windows[0])}")
        return windows[0]
    return None


def is_wechat_window_visible():
    """Check if WeChat window is visible"""
    hwnd = get_wechat_window_handle()
    if hwnd:
        return user32.IsWindowVisible(hwnd)
    return False


def restore_wechat_window():
    """Restore WeChat window from minimized state"""
    hwnd = get_wechat_window_handle()
    if hwnd:
        try:
            user32.ShowWindow(hwnd, SW_RESTORE)
            time.sleep(0.5)
            user32.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            print("  OK: WeChat window restored")
            return True
        except Exception as e:
            print(f"  ERROR: Failed to restore window: {e}")
    return False


def get_active_window_title():
    """Get active window title"""
    try:
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthA(hwnd)
        buffer = ctypes.create_string_buffer(length + 1)
        user32.GetWindowTextA(hwnd, buffer, length + 1)
        return buffer.value.decode('gbk', errors='ignore')
    except:
        return ""


def is_wechat_active():
    """Check if WeChat is the active window"""
    title = get_active_window_title()
    is_active = 'WeChat' in title or '微信' in title
    if is_active:
        print("  OK: WeChat window is active")
    return is_active


class WeChatActivator:
    """WeChat window activator with multiple strategies"""
    
    def __init__(self):
        self.strategies = [
            (self._activate_by_shortcut, "Keyboard Shortcut (Ctrl+Alt+W)"),
            (self._activate_by_window_handle, "Window Handle"),
            (self._activate_by_taskbar, "Taskbar Click"),
            (self._activate_by_start_menu, "Launch WeChat"),
        ]
    
    def _activate_by_shortcut(self):
        """Strategy 1: Use keyboard shortcut Ctrl+Alt+W"""
        try:
            pyautogui.hotkey("ctrl", "alt", "w")
            time.sleep(1)
            return is_wechat_active()
        except Exception as e:
            print(f"    Failed: {e}")
            return False
    
    def _activate_by_window_handle(self):
        """Strategy 2: Use window handle"""
        try:
            hwnd = get_wechat_window_handle()
            if hwnd:
                user32.ShowWindow(hwnd, SW_RESTORE)
                user32.SetForegroundWindow(hwnd)
                time.sleep(1)
                return is_wechat_active()
            return False
        except Exception as e:
            print(f"    Failed: {e}")
            return False
    
    def _activate_by_taskbar(self):
        """Strategy 3: Click taskbar (search from right to left)"""
        try:
            screen_width, screen_height = pyautogui.size()
            taskbar_height = 40
            
            for x in range(screen_width - 20, 50, -30):
                pyautogui.moveTo(x, screen_height - taskbar_height // 2)
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(0.5)
                if is_wechat_active():
                    return True
            return False
        except Exception as e:
            print(f"    Failed: {e}")
            return False
    
    def _activate_by_start_menu(self):
        """Strategy 4: Launch WeChat from start menu"""
        try:
            paths = [
                r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
                r"C:\Program Files\Tencent\WeChat\WeChat.exe",
                r"D:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
                r"D:\Program Files\Tencent\WeChat\WeChat.exe",
            ]
            
            for path in paths:
                if os.path.exists(path):
                    print(f"    Launching: {path}")
                    subprocess.Popen(path)
                    time.sleep(5)
                    return is_wechat_active()
            
            print("    Not found: WeChat installation path")
            return False
        except Exception as e:
            print(f"    Failed: {e}")
            return False
    
    def activate(self, max_retries=2):
        """Try to activate WeChat window (multiple strategies)"""
        print("\nActivating WeChat window...")
        
        for attempt in range(max_retries):
            print(f"  Attempt {attempt + 1}/{max_retries}")
            for strategy, name in self.strategies:
                print(f"    Trying: {name}")
                if strategy():
                    print("  OK: WeChat window activated successfully")
                    return True
                time.sleep(0.5)
        
        print("  FAIL: All activation strategies failed")
        return False


def ensure_wechat_ready():
    """Ensure WeChat window is ready"""
    print("\n" + "=" * 50)
    print("Checking WeChat Status")
    print("=" * 50)
    
    if not is_wechat_running():
        print("  WeChat not running, trying to start...")
        activator = WeChatActivator()
        if not activator.activate():
            print("  FAIL: Cannot start WeChat")
            return False
    
    if not is_wechat_active():
        print("  WeChat not active, trying to activate...")
        activator = WeChatActivator()
        if not activator.activate():
            print("  FAIL: Cannot activate WeChat window")
            return False
    
    time.sleep(1)
    print("  OK: WeChat is ready")
    return True


if __name__ == "__main__":
    ensure_wechat_ready()