#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
独立任务执行脚本 - 供 Windows 计划任务调用
用法: python run_job.py [--category morning] [--dry-run]
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from scheduler import run_send_job

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="执行一次朋友圈发送任务")
    parser.add_argument("--category", help="文案分类")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    args = parser.parse_args()

    run_send_job(args.category, args.dry_run)
（内容由AI生成，仅供参考）
