#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送 - 统一入口脚本
提供友好的命令行界面，整合所有功能
"""

import argparse
import sys
import os
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent


def print_banner():
    """打印欢迎横幅"""
    banner = """
============================================
        WeChat Moments Auto Sender            
============================================
    """
    print(banner)


def action_notion(args):
    """从 Notion 读取并发送"""
    import subprocess
    
    cmd = ["python", str(SCRIPT_DIR / "send_from_notion.py")]
    if hasattr(args, 'dry_run') and args.dry_run:
        cmd.append("--dry-run")
    if hasattr(args, 'no_update') and args.no_update:
        cmd.append("--no-update")
    if hasattr(args, 'min_delay') and args.min_delay is not None:
        cmd.extend(["--min-delay", str(args.min_delay)])
    if hasattr(args, 'max_delay') and args.max_delay is not None:
        cmd.extend(["--max-delay", str(args.max_delay)])
    
    subprocess.run(cmd)


def action_send(args):
    """手动发送指定内容"""
    from send_by_image import send_moments
    
    success = send_moments(args.text, args.image, args.dry_run)
    sys.exit(0 if success else 1)


def action_test(args):
    """测试微信窗口检测"""
    from wechat_utils import ensure_wechat_ready, is_wechat_running, is_wechat_active
    
    print("\n=== WeChat Window Test ===")
    
    print("\n1. Checking WeChat process...")
    running = is_wechat_running()
    
    print("\n2. Checking if WeChat is active...")
    active = is_wechat_active()
    
    print("\n3. Full check (ensure ready)...")
    ready = ensure_wechat_ready()
    
    print("\n=== Test Results ===")
    print(f"Process running: {'OK' if running else 'FAIL'}")
    print(f"Window active: {'OK' if active else 'FAIL'}")
    print(f"Overall ready: {'OK' if ready else 'FAIL'}")
    
    if ready:
        print("\nSUCCESS: WeChat is ready!")
        return True
    else:
        print("\nFAILURE: WeChat not ready!")
        return False


def action_capture(args):
    """截取界面元素"""
    import subprocess
    cmd = ["python", str(SCRIPT_DIR / "capture_ui.py")]
    subprocess.run(cmd)


def action_generate(args):
    """生成内容"""
    from generate_content import generate_content
    
    content = generate_content()
    print(f"\nGenerated content:\n{content}")
    
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(content)
            print("Copied to clipboard!")
        except ImportError:
            print("Tip: Install pyperclip for clipboard support")


def action_help(args):
    """显示帮助信息"""
    parser.print_help()
    print("\nExamples:")
    print("  python run.py                      # Send from Notion (default)")
    print("  python run.py notion --dry-run     # Simulate run")
    print("  python run.py send --text 'hello'  # Send custom text")
    print("  python run.py test                 # Test WeChat window")
    print("  python run.py capture              # Capture UI elements")
    print("  python run.py generate             # Generate content")


def main():
    global parser
    
    parser = argparse.ArgumentParser(
        description="WeChat Moments Auto Sender - Unified Entry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                      # Send from Notion (default)
  python run.py notion --dry-run     # Simulate without sending
  python run.py send --text 'hello'  # Send custom content
  python run.py test                 # Test WeChat window detection
  python run.py capture              # Capture UI elements
  python run.py generate             # Generate moments content
        """
    )
    
    subparsers = parser.add_subparsers(dest="action", help="Action type")
    
    # notion - Send from Notion
    notion_parser = subparsers.add_parser("notion", help="Send from Notion")
    notion_parser.add_argument("--dry-run", action="store_true", help="Simulate only")
    notion_parser.add_argument("--no-update", action="store_true", help="Don't update status")
    notion_parser.add_argument("--min-delay", type=int, help="Min delay in minutes")
    notion_parser.add_argument("--max-delay", type=int, help="Max delay in minutes")
    
    # send - Send custom content
    send_parser = subparsers.add_parser("send", help="Send custom content")
    send_parser.add_argument("--text", required=True, help="Moments content")
    send_parser.add_argument("--image", help="Image path")
    send_parser.add_argument("--dry-run", action="store_true", help="Simulate only")
    
    # test - Test WeChat window
    test_parser = subparsers.add_parser("test", help="Test WeChat window detection")
    
    # capture - Capture UI elements
    capture_parser = subparsers.add_parser("capture", help="Capture UI elements")
    
    # generate - Generate content
    generate_parser = subparsers.add_parser("generate", help="Generate content")
    generate_parser.add_argument("--copy", action="store_true", help="Copy to clipboard")
    
    # help - Show help
    help_parser = subparsers.add_parser("help", help="Show this help")
    
    args = parser.parse_args()
    
    # Default action is notion
    if args.action is None:
        args.action = "notion"
    
    # Print banner
    print_banner()
    
    # Execute action
    actions = {
        "notion": action_notion,
        "send": action_send,
        "test": action_test,
        "capture": action_capture,
        "generate": action_generate,
        "help": action_help,
    }
    
    if args.action in actions:
        try:
            actions[args.action](args)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        print(f"Unknown action: {args.action}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()