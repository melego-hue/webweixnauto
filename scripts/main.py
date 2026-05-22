#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送 - 主入口
整合内容生成和发送功能

使用方法:
    python main.py                    # 自动生成内容并发送
    python main.py --text "自定义内容" # 发送指定内容
    python main.py --dry-run          # 模拟运行
    python main.py --generate-only    # 只生成内容，不发送
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# Windows编码修复
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent


def generate_content():
    """生成朋友圈内容"""
    from generate_content import generate_content as gen

    return gen()


def send_moments(text, images=None, dry_run=False):
    """发送朋友圈"""
    from send_by_image import send_moments as send

    return send(text, images, dry_run)


def main():
    parser = argparse.ArgumentParser(description="微信朋友圈自动发送")
    parser.add_argument("--text", help="自定义朋友圈内容")
    parser.add_argument("--images", help="图片路径（暂不支持）")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行，不实际发送")
    parser.add_argument(
        "--generate-only", action="store_true", help="只生成内容，不发送"
    )

    args = parser.parse_args()

    print("=" * 50)
    print(f"微信朋友圈自动发送 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 生成或使用自定义内容
    if args.text:
        content = args.text
        print(f"\n使用自定义内容: {content[:50]}...")
    else:
        print("\n自动生成内容...")
        content = generate_content()
        print(f"生成内容: {content}")

    if args.generate_only:
        print("\n[仅生成模式] 内容已生成，未发送")
        print(f"\n内容: {content}")
        return

    # 发送
    print("\n准备发送...")
    success = send_moments(content, args.images, args.dry_run)

    if success:
        print("\n✓ 任务完成！")
    else:
        print("\n✗ 任务失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
