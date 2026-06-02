#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
定时调度模块
支持 Windows 计划任务 和 Python schedule 库两种方式
"""

import sys
import time
import random
import json
import subprocess
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
DB_MANAGER = SCRIPT_DIR / "db_manager.py"
SENDER = SCRIPT_DIR / "sender.py"
CONTENT_GEN = SCRIPT_DIR / "content_gen.py"
CLI = SCRIPT_DIR / "cli.py"


def run_send_job(category=None, dry_run=False):
    """
    执行一次发送任务

    Args:
        category: 文案分类，None 则随机
        dry_run: 仅模拟

    Returns:
        bool: 是否成功
    """
    sys.path.insert(0, str(SCRIPT_DIR))
    from db_manager import get_random_pending, mark_as_sent, log_send, get_pending_count
    from sender import send_moments_text

    pending_count = get_pending_count()
    if pending_count == 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 没有待发送文案，跳过")
        return False

    item = get_random_pending(category)
    if not item:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 没有符合条件的待发送文案")
        return False

    # Get image path from db if it exists
    db_image_path = item.get("image_path") if "image_path" in item.keys() else None

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 准备发送: {item['text'][:30]}...")

    ok, msg = send_moments_text(item["text"], image_path=db_image_path, dry_run=dry_run)

    if ok:
        mark_as_sent(item["id"])
        log_send(item["id"], item["text"], db_image_path or "matched_or_random", True)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 发送成功")
        
        # Remote status update callback
        source_id = item.get("source_id") if "source_id" in item.keys() else None
        source_type = item.get("source_type") if "source_type" in item.keys() else None
        
        if source_id and source_type and source_type != "local":
            try:
                # Add D:\weixin\wechat-moments-auto-v2\scripts to sys.path for import
                from pathlib import Path
                scripts_path = str(Path(r"D:\weixin\wechat-moments-auto-v2\scripts"))
                if scripts_path not in sys.path:
                    sys.path.insert(0, scripts_path)
                    
                import config
                from sync_sources import update_remote_status
                
                # Determine remote completed status
                status_completed = "完成"
                if "notion_v2" in source_type:
                    status_completed = config.NOTION_CONFIGS["v2"]["fields"]["status_completed"]
                elif "notion_luffy" in source_type:
                    status_completed = config.NOTION_CONFIGS["luffy"]["fields"]["status_completed"]
                elif source_type == "feishu":
                    status_completed = config.FEISHU_CONFIG["fields"]["status_completed"]
                
                update_remote_status(source_type, source_id, status_completed)
            except Exception as e:
                print(f"  [Warning] Remote status update failed: {e}")
    else:
        log_send(item["id"], item["text"], db_image_path or "matched_or_random", False, msg)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 发送失败: {msg}")

    return ok


def schedule_with_python(cron_expr, category=None, dry_run=False):
    """
    使用 Python schedule 库运行定时任务

    Args:
        cron_expr: cron 表达式，如 "0 8 * * *"（每天8点）
        category: 文案分类
        dry_run: 仅模拟
    """
    try:
        import schedule
    except ImportError:
        print("请先安装: pip install schedule")
        return

    # 解析 cron 表达式
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        print(f"无效的 cron 表达式: {cron_expr}")
        return

    minute, hour, day, month, weekday = parts

    def job():
        # 随机延迟 1-5 分钟，模拟真人行为
        delay = random.randint(60, 300)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 随机延迟 {delay} 秒...")
        time.sleep(delay)
        run_send_job(category, dry_run)

    # 设置定时
    if minute != "*" and hour != "*":
        schedule.every().day.at(f"{hour.zfill(2)}:{minute.zfill(2)}").do(job)
    elif hour != "*":
        schedule.every().day.at(f"{hour.zfill(2)}:00").do(job)
    else:
        schedule.every(int(minute) if minute != "*" else 60).minutes.do(job)

    print(f"定时任务已启动: {cron_expr}")
    print(f"分类: {category or '随机'}")
    print(f"模式: {'模拟' if dry_run else '真实发送'}")
    print("按 Ctrl+C 停止\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n定时任务已停止")


def create_windows_task(task_name, cron_expr, category=None, dry_run=False):
    """
    创建 Windows 计划任务

    Args:
        task_name: 任务名称
        cron_expr: cron 表达式
        category: 文案分类
        dry_run: 仅模拟

    Returns:
        bool: 是否成功
    """
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        print(f"无效的 cron 表达式: {cron_expr}")
        return False

    minute, hour, day, month, weekday = parts

    # 构建 schtasks 命令
    python_exe = sys.executable
    script_path = str(SCRIPT_DIR / "run_job.py")

    cmd_args = [python_exe, script_path]
    if category:
        cmd_args.extend(["--category", category])
    if dry_run:
        cmd_args.append("--dry-run")

    cmd_str = " ".join(f'"{a}"' for a in cmd_args)

    # 构建 schtasks 参数
    schtasks_args = [
        "schtasks",
        "/Create",
        "/F",  # 强制覆盖同名任务
        "/TN",
        task_name,
        "/TR",
        cmd_str,
        "/SC",
    ]

    # 确定调度类型
    if day == "*" and month == "*" and weekday == "*":
        # 每天
        schtasks_args.append("DAILY")
        if hour != "*":
            schtasks_args.extend(["/ST", f"{hour.zfill(2)}:{minute.zfill(2)}"])
    elif weekday != "*":
        # 每周
        schtasks_args.append("WEEKLY")
        day_map = {"0": "SUN", "1": "MON", "2": "TUE", "3": "WED", "4": "THU", "5": "FRI", "6": "SAT"}
        schtasks_args.extend(["/D", day_map.get(weekday, "MON")])
        if hour != "*":
            schtasks_args.extend(["/ST", f"{hour.zfill(2)}:{minute.zfill(2)}"])
    elif day != "*":
        # 每月
        schtasks_args.append("MONTHLY")
        schtasks_args.extend(["/D", day])
        if hour != "*":
            schtasks_args.extend(["/ST", f"{hour.zfill(2)}:{minute.zfill(2)}"])

    try:
        result = subprocess.run(schtasks_args, capture_output=True, text=True, encoding="gbk", errors="ignore")
        if result.returncode == 0:
            print(f"Windows 计划任务创建成功: {task_name}")
            print(f"  调度: {cron_expr}")
            print(f"  命令: {cmd_str}")
            return True
        else:
            print(f"创建失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"创建失败: {e}")
        return False


def delete_windows_task(task_name):
    """删除 Windows 计划任务"""
    try:
        result = subprocess.run(
            ["schtasks", "/Delete", "/TN", task_name, "/F"],
            capture_output=True,
            text=True,
            encoding="gbk",
            errors="ignore",
        )
        if result.returncode == 0:
            print(f"计划任务已删除: {task_name}")
            return True
        else:
            print(f"删除失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"删除失败: {e}")
        return False


def list_windows_tasks():
    """列出所有朋友圈相关的 Windows 计划任务"""
    try:
        result = subprocess.run(
            ["schtasks", "/Query", "/FO", "LIST"],
            capture_output=True,
            text=True,
            encoding="gbk",
            errors="ignore",
        )
        tasks = []
        for line in result.stdout.split("\n"):
            if "Moments" in line or "moments" in line or "朋友圈" in line:
                tasks.append(line.strip())
        return tasks
    except Exception as e:
        print(f"查询失败: {e}")
        return []


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="朋友圈定时调度")
    parser.add_argument("--cron", default="0 8 * * *", help="cron 表达式")
    parser.add_argument("--category", help="文案分类")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    parser.add_argument("--mode", choices=["python", "windows"], default="python", help="调度方式")
    parser.add_argument("--task-name", default="MomentsAutoSend", help="Windows 任务名称")

    args = parser.parse_args()

    if args.mode == "windows":
        create_windows_task(args.task_name, args.cron, args.category, args.dry_run)
    else:
        schedule_with_python(args.cron, args.category, args.dry_run)
