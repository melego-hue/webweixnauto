#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
朋友圈定时自动发送 - 统一命令行入口
"""

import sys
import argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from db_manager import (
    init_db,
    add_content,
    add_contents_batch,
    get_random_pending,
    get_stats,
    get_pending_count,
    list_content,
    search_content,
    reset_all_pending,
    STATUS_PENDING,
    STATUS_SENT,
)
from content_gen import (
    generate_from_template,
    generate_with_llm,
    generate_mixed,
    bulk_fill_db,
    TEMPLATES,
    CATEGORIES as GEN_CATEGORIES,
)
from sender import send_moments_text
from scheduler import run_send_job, schedule_with_python, create_windows_task, delete_windows_task

CATEGORIES = list(TEMPLATES.keys()) + ["professional", "reliable", "warm", "altruistic", "counter", "target", "intro_100"]

BANNER = """
============================================
   朋友圈定时自动发送 v2.0
   WeChat Moments Auto Scheduler           
============================================"""


def cmd_init(args):
    """初始化数据库"""
    init_db()
    print("数据库初始化完成")
    print(f"数据库路径: D:\\weixin\\wechat-moments-auto-v2\\data\\moments.db")


def cmd_status(args):
    """查看统计"""
    stats = get_stats()
    print(f"\n朋友圈文案统计")
    print(f"{'='*40}")
    print(f"  总文案数: {stats['total']}")
    for status_name, status_label in [("pending", "待发送"), ("sent", "已发送"), ("skipped", "已跳过")]:
        count = stats.get(status_name, 0)
        print(f"  {status_label}: {count}")

    print(f"\n分类统计:")
    for item in stats.get("by_category", []):
        print(f"  {item['category']}: {item['count']} 条")

    recent = stats.get("recent", [])
    if recent:
        print(f"\n最近发送:")
        for r in recent[:5]:
            print(f"  [{r['sent_at']}] {r['text']}")


def cmd_add(args):
    """添加文案"""
    if args.batch:
        batch_size = args.batch
        items = generate_from_template(args.category, batch_size)
        count = add_contents_batch(items)
        print(f"已从模板库生成并添加 {count} 条文案（分类: {args.category or '随机'}）")

        if args.llm:
            print("提示: LLM 生成功能需要在主程序（Marvis）中调用，命令行暂不支持直接调用 LLM。")
            print("      请使用 Marvis 的 generate 指令来使用 LLM 增强生成。")
    else:
        text = args.text
        if not text:
            print("请使用 --text 指定文案内容，或使用 --batch 批量生成")
            return
        cid = add_content(text, args.category or "custom", args.tags or "", args.emoji or "")
        print(f"已添加文案 (ID: {cid}): {text[:50]}")


def cmd_generate(args):
    """生成文案并加入库"""
    if args.llm:
        import time
        from content_gen import generate_via_siliconflow
        from sync_sources import get_blogger_by_text, get_blogger_image, get_random_image
        
        count = args.count or 1
        print(f"正在通过 SiliconFlow API 调用 AI 智能生成文案 (分类: {args.category or 'custom'}，数量: {count})...")
        
        for i in range(count):
            try:
                item = generate_via_siliconflow(args.category, "任意主题", args.style or "normal")
                text = item["text"]
                
                # 匹配博主配图
                blogger = get_blogger_by_text(text)
                image_path = get_blogger_image(blogger)
                if not image_path:
                    image_path = get_random_image()
                    
                cid = add_content(
                    text=text,
                    category=args.category or "custom",
                    tags="siliconflow,llm",
                    emoji="",
                    source=SOURCE_LLM,
                    image_path=image_path or "",
                    source_type="local_llm",
                    source_id=f"sf_{int(time.time())}_{i}"
                )
                
                print(f"\n[AI 生成并入库成功] ID: {cid}")
                print(f"  匹配图片: {Path(image_path).name if image_path else '无'}")
                print(f"  文案内容:\n{'-'*30}\n{text}\n{'-'*30}")
            except Exception as e:
                print(f"❌ AI 生成失败: {e}")
    else:
        # 本地模板库生成，同时适配图片匹配
        from sync_sources import get_blogger_by_text, get_blogger_image, get_random_image
        count = args.count or 5
        items = generate_from_template(args.category, count)
        
        # 补充模板文案的图片和源信息
        for item in items:
            blogger = get_blogger_by_text(item["text"])
            image_path = get_blogger_image(blogger)
            if not image_path:
                image_path = get_random_image()
            item["image_path"] = image_path or ""
            item["source_type"] = "local_template"
            item["source_id"] = ""
            
        added = add_contents_batch(items)
        print(f"已从模板库生成并添加 {added} 条文案到本地库\n")
        
        for item in items:
            print(f"  [{item['category']}] {item['emoji']} {item['text'][:60]}...")


def cmd_list(args):
    """列出文案"""
    status = args.status or STATUS_PENDING
    items = list_content(status=status, category=args.category, limit=args.limit or 20)

    if not items:
        print(f"没有找到文案（状态: {status}）")
        return

    status_map = {STATUS_PENDING: "待发送", STATUS_SENT: "已发送", "skipped": "已跳过"}
    print(f"\n文案列表 ({status_map.get(status, status)}，共 {len(items)} 条)\n")

    for item in items:
        status_str = "✓" if item["status"] == STATUS_SENT else "○" if item["status"] == "skipped" else "●"
        print(f"  [{item['id']}] {status_str} [{item['category']}] {item['emoji']} {item['text'][:60]}")


def cmd_send(args):
    """发送朋友圈"""
    if args.text:
        ok, msg = send_moments_text(args.text, args.image, args.dry_run)
        print(f"{'[模拟] ' if args.dry_run else ''}{msg}")
    else:
        pending = get_pending_count()
        if pending == 0:
            print("没有待发送的文案，请先用 generate 或 add 添加文案")
            return
        ok = run_send_job(args.category, args.dry_run)
        if not ok:
            print("发送失败")


def cmd_schedule(args):
    """设置定时任务"""
    cron = args.cron or "0 8 * * *"

    if args.action == "start":
        if args.mode == "windows":
            task_name = args.task_name or "MomentsAutoSend"
            create_windows_task(task_name, cron, args.category, args.dry_run)
        else:
            print(f"启动 Python 定时调度: {cron}")
            schedule_with_python(cron, args.category, args.dry_run)

    elif args.action == "stop":
        if args.mode == "windows":
            task_name = args.task_name or "MomentsAutoSend"
            delete_windows_task(task_name)
        else:
            print("Python 定时调度请在运行窗口按 Ctrl+C 停止")

    elif args.action == "list":
        from scheduler import list_windows_tasks

        tasks = list_windows_tasks()
        if tasks:
            print("\n朋友圈相关计划任务:")
            for t in tasks:
                print(f"  {t}")
        else:
            print("没有找到朋友圈相关的计划任务")


def cmd_search(args):
    """搜索文案"""
    items = search_content(args.keyword, args.limit or 20)
    if not items:
        print(f"没有找到包含「{args.keyword}」的文案")
        return

    print(f"\n搜索结果: 「{args.keyword}」（共 {len(items)} 条）\n")
    for item in items:
        status_str = "✓" if item["status"] == STATUS_SENT else "○"
        print(f"  [{item['id']}] {status_str} [{item['category']}] {item['text'][:60]}")


def cmd_reset(args):
    """重置所有已发送为未发送"""
    count = reset_all_pending()
    print(f"已将 {count} 条已发送文案重置为待发送")


def cmd_sync(args):
    """同步外部数据源 (Notion, 飞书)"""
    import sys
    from pathlib import Path
    scripts_path = str(Path(r"D:\weixin\wechat-moments-auto-v2\scripts"))
    
    # We call sync_sources.py as a subprocess to cleanly print all logs
    python_exe = sys.executable
    sync_script = str(Path(scripts_path) / "sync_sources.py")
    
    cmd_args = [python_exe, sync_script, "--source", args.source]
    if args.dry_run:
        cmd_args.append("--dry-run")
        
    import subprocess
    print(f"开始同步外部数据源 (源: {args.source})...")
    subprocess.run(cmd_args)


def main():
    parser = argparse.ArgumentParser(
        description="朋友圈定时自动发送",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py init                          # 初始化数据库
  python cli.py generate                      # 生成5条文案
  python cli.py generate -c morning -n 10     # 生成10条早安文案
  python cli.py add --text "今天天气真好"     # 手动添加文案
  python cli.py add -b 10                     # 批量生成10条
  python cli.py sync                          # 同步所有 Notion/飞书 数据
  python cli.py sync --source luffy           # 只同步路飞发稿池
  python cli.py send                          # 随机发送一条
  python cli.py send --text "自定义内容"      # 发送自定义内容
  python cli.py send --dry-run                # 模拟发送
  python cli.py status                        # 查看统计
  python cli.py list                          # 列出待发送
  python cli.py list -s sent                  # 列出已发送
  python cli.py search "早安"                 # 搜索文案
  python cli.py reset                         # 重置发送状态
  python cli.py schedule start --cron "0 8 * * *"   # 每天早上8点
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    sp_init = subparsers.add_parser("init", help="初始化数据库")

    # status
    sp_status = subparsers.add_parser("status", help="查看统计信息")

    # sync
    sp_sync = subparsers.add_parser("sync", help="同步外部数据源 (Notion, 飞书)")
    sp_sync.add_argument("--source", choices=["all", "luffy", "v2", "feishu"], default="all", help="数据源")
    sp_sync.add_argument("--dry-run", action="store_true", help="模拟同步，不写入本地库")

    # add
    sp_add = subparsers.add_parser("add", help="添加文案")
    sp_add.add_argument("--text", help="文案内容")
    sp_add.add_argument("--category", "-c", choices=CATEGORIES, help="文案分类")
    sp_add.add_argument("--tags", help="标签，逗号分隔")
    sp_add.add_argument("--emoji", help="表情符号")
    sp_add.add_argument("--batch", "-b", type=int, help="批量生成数量")
    sp_add.add_argument("--llm", action="store_true", help="同时使用 LLM 生成")

    # generate
    sp_gen = subparsers.add_parser("generate", help="生成文案")
    sp_gen.add_argument("--category", "-c", choices=CATEGORIES, help="文案分类")
    sp_gen.add_argument("--count", "-n", type=int, default=5, help="生成数量")
    sp_gen.add_argument("--llm", action="store_true", help="使用 LLM 增强")
    sp_gen.add_argument("--style", choices=["normal", "humor", "literary", "short"], default="normal", help="文案风格")

    # list
    sp_list = subparsers.add_parser("list", help="列出文案")
    sp_list.add_argument("--status", "-s", choices=[STATUS_PENDING, STATUS_SENT, "skipped"], help="状态筛选")
    sp_list.add_argument("--category", "-c", choices=CATEGORIES, help="分类筛选")
    sp_list.add_argument("--limit", "-n", type=int, help="数量限制")

    # send
    sp_send = subparsers.add_parser("send", help="发送朋友圈")
    sp_send.add_argument("--text", help="自定义文案（留空则随机取一条待发送）")
    sp_send.add_argument("--image", help="图片路径")
    sp_send.add_argument("--category", "-c", choices=CATEGORIES, help="分类筛选")
    sp_send.add_argument("--dry-run", action="store_true", help="模拟发送")

    # schedule
    sp_sch = subparsers.add_parser("schedule", help="定时任务管理")
    sp_sch.add_argument("action", choices=["start", "stop", "list"], help="操作")
    sp_sch.add_argument("--cron", default="0 8 * * *", help="cron 表达式")
    sp_sch.add_argument("--category", "-c", choices=CATEGORIES, help="文案分类")
    sp_sch.add_argument("--mode", choices=["python", "windows"], default="python", help="调度方式")
    sp_sch.add_argument("--task-name", default="MomentsAutoSend", help="Windows 任务名称")
    sp_sch.add_argument("--dry-run", action="store_true", help="模拟发送")

    # search
    sp_search = subparsers.add_parser("search", help="搜索文案")
    sp_search.add_argument("keyword", help="搜索关键词")
    sp_search.add_argument("--limit", "-n", type=int, help="数量限制")

    # reset
    sp_reset = subparsers.add_parser("reset", help="重置所有已发送为未发送")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    print(BANNER)

    commands = {
        "init": cmd_init,
        "status": cmd_status,
        "sync": cmd_sync,
        "add": cmd_add,
        "generate": cmd_generate,
        "list": cmd_list,
        "send": cmd_send,
        "schedule": cmd_schedule,
        "search": cmd_search,
        "reset": cmd_reset,
    }

    if args.command in commands:
        try:
            commands[args.command](args)
        except KeyboardInterrupt:
            print("\n操作已取消")
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback

            traceback.print_exc()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
