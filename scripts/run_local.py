#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送 - 本地Excel版本主入口
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
        WeChat Moments Auto Sender (Local)          
============================================
    """
    print(banner)

def action_local(args):
    """从本地Excel读取并发送"""
    import subprocess
    
    cmd = ["python", str(SCRIPT_DIR / "send_from_local.py")]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.no_update:
        cmd.append("--no-update")
    if args.min_delay is not None:
        cmd.extend(["--min-delay", str(args.min_delay)])
    if args.max_delay is not None:
        cmd.extend(["--max-delay", str(args.max_delay)])
    if args.content_id is not None:
        cmd.extend(["--content-id", str(args.content_id)])
    
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

def main():
    parser = argparse.ArgumentParser(
        description="微信朋友圈自动发送 - 本地Excel版本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_local.py local                   # 从本地Excel发送 (默认)
  python run_local.py local --dry-run        # 模拟运行
  python run_local.py local --min-delay 5    # 延迟5分钟发送
  python run_local.py send --text 'hello'    # 手动发送指定内容
  python run_local.py test                   # 测试微信窗口检测
  python run_local.py capture               # 截取界面元素
  python run_local.py generate              # 生成朋友圈内容
        """
    )
    
    subparsers = parser.add_subparsers(dest="action", help="操作类型")
    
    # local - 从本地Excel发送
    local_parser = subparsers.add_parser("local", help="从本地Excel发送")
    local_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    local_parser.add_argument("--no-update", action="store_true", help="不更新Excel状态")
    local_parser.add_argument("--min-delay", type=int, help="最小延迟（分钟）")
    local_parser.add_argument("--max-delay", type=int, help="最大延迟（分钟）")
    local_parser.add_argument("--content-id", type=int, help="指定ID发送（不随机选择）")
    
    # send - 手动发送指定内容
    send_parser = subparsers.add_parser("send", help="手动发送指定内容")
    send_parser.add_argument("--text", required=True, help="朋友圈内容")
    send_parser.add_argument("--image", help="图片路径")
    send_parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    # test - 测试微信窗口
    test_parser = subparsers.add_parser("test", help="测试微信窗口检测")
    
    # capture - 截取界面元素
    capture_parser = subparsers.add_parser("capture", help="截取界面元素")
    
    # generate - 生成内容
    generate_parser = subparsers.add_parser("generate", help="生成内容")
    generate_parser.add_argument("--copy", action="store_true", help="复制到剪贴板")
    
    args = parser.parse_args()
    
    # 默认操作是local
    if args.action is None:
        args.action = "local"
    
    # 打印横幅
    print_banner()
    
    # 执行操作
    actions = {
        "local": action_local,
        "send": action_send,
        "test": action_test,
        "capture": action_capture,
        "generate": action_generate,
    }
    
    if args.action in actions:
        try:
            actions[args.action](args)
        except KeyboardInterrupt:
            print("\n\n操作被用户取消")
            sys.exit(1)
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        print(f"未知操作: {args.action}")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()