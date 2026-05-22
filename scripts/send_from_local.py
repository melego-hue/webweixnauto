#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动发送 - 本地Excel版本
从本地Excel表格读取内容并发送到朋友圈
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime
import pandas as pd

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

# Excel数据库路径
EXCEL_DB_PATH = PROJECT_DIR / "content_database.xlsx"

# 状态字段定义
STATUS_PENDING = "未发布"
STATUS_COMPLETED = "已发布"

# 博主关键词映射
BLOGGER_KEYWORDS = {
    "Luffy": ["不卖珠宝的路飞", "自己学易的路飞", "自己造船的路飞", "路飞"],
    "Dayuan": ["遇见大元", "大元"],
    "Quange": ["全哥"],
    "Lizhen": ["李真"],
}

def get_blogger_by_name(name):
    """根据博主名称确定博主"""
    for blogger, keywords in BLOGGER_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name:
                return blogger
    return None

def get_blogger_image(blogger):
    """获取博主图片路径"""
    if not blogger:
        return None
    
    images_dir = PROJECT_DIR / "images"
    chinese_names = {"Luffy": "路飞", "Dayuan": "大元", "Quange": "全哥", "Lizhen": "李真"}
    
    for ext in [".png", ".jpg", ".jpeg"]:
        if blogger in chinese_names:
            image_path = images_dir / f"{chinese_names[blogger]}{ext}"
            if image_path.exists():
                return str(image_path.absolute())
        
        image_path = images_dir / f"{blogger}{ext}"
        if image_path.exists():
            return str(image_path.absolute())
    
    return None

def fetch_local_content():
    """从本地Excel读取待发布内容"""
    print("\n读取本地Excel数据库...")
    
    try:
        # 读取Excel文件
        df = pd.read_excel(EXCEL_DB_PATH)
        
        # 查找状态为"未发布"的内容
        pending_items = df[df["状态"] == STATUS_PENDING]
        
        if len(pending_items) == 0:
            print("  没有找到待发布的内容")
            return None
        
        # 随机选择一条待发布内容
        item_idx = random.randint(0, len(pending_items) - 1)
        item = pending_items.iloc[item_idx]
        
        # 获取博主信息
        blogger_name = item["博主"]
        blogger = get_blogger_by_name(blogger_name)
        
        # 获取图片路径
        image_path = get_blogger_image(blogger) if blogger else None
        
        # 如果Excel中有指定图片路径，优先使用
        excel_image_path = item["图片路径"]
        if excel_image_path and Path(excel_image_path).exists():
            image_path = excel_image_path
        
        # 跳过没有图片的内容
        if not image_path:
            print(f"  跳过: 博主 '{blogger or blogger_name or '未知'}' 没有对应的图片")
            return None
        
        # 获取内容
        content = item["内容"]
        if not content:
            print("  跳过: 内容为空")
            return None
        
        print(f"  找到内容:")
        print(f"    博主: {blogger_name}")
        print(f"    图片: {Path(image_path).name}")
        print(f"    内容: {content[:50]}...")
        
        return {
            "row_idx": item_idx,  # Excel行索引
            "id": item["ID"],
            "blogger_name": blogger_name,
            "blogger": blogger,
            "content": content,
            "image_path": image_path,
            "status": item["状态"],
            "created_time": item["创建时间"],
        }
    
    except Exception as e:
        print(f"  读取Excel失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_local_status(row_idx):
    """更新Excel中的状态"""
    print(f"\n更新Excel状态: 行 {row_idx}")
    
    try:
        # 读取Excel
        df = pd.read_excel(EXCEL_DB_PATH)
        
        # 更新状态和发布时间
        df.at[row_idx, "状态"] = STATUS_COMPLETED
        df.at[row_idx, "发布时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存Excel
        df.to_excel(EXCEL_DB_PATH, index=False)
        
        print(f"  成功: 状态更新为 '{STATUS_COMPLETED}'")
        return True
    
    except Exception as e:
        print(f"  更新Excel失败: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="从本地Excel发送朋友圈")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行，不实际发送")
    parser.add_argument("--no-update", action="store_true", help="不更新Excel状态")
    parser.add_argument("--min-delay", type=int, default=5, help="最小延迟（分钟）")
    parser.add_argument("--max-delay", type=int, default=15, help="最大延迟（分钟）")
    parser.add_argument("--content-id", type=int, help="指定ID发送（不随机选择）")
    args = parser.parse_args()
    
    print("=" * 50)
    print(f"本地Excel -> 微信朋友圈 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 延迟发送
    if args.max_delay > 0:
        delay_minutes = random.randint(args.min_delay, args.max_delay)
        delay_seconds = delay_minutes * 60
        print(f"\n随机延迟: {delay_minutes} 分钟...")
        print(f"实际发送时间: {(datetime.now().replace(second=0, microsecond=0) + __import__('datetime').timedelta(minutes=delay_minutes)).strftime('%H:%M')}")
        time.sleep(delay_seconds)
    
    # 读取内容
    item = fetch_local_content()
    if not item:
        print("\n没有找到可发布的内容")
        return
    
    if args.dry_run:
        print(f"\n[模拟运行] 将发送:")
        print(f"  ID: {item['id']}")
        print(f"  博主: {item['blogger_name']}")
        print(f"  图片: {item['image_path']}")
        print(f"  内容: {item['content'][:100]}...")
        print(f"  将更新状态为: {STATUS_COMPLETED}")
        return
    
    print("\n发送朋友圈...")
    from send_by_image import send_moments
    
    success = send_moments(item["content"], item["image_path"])
    
    if success:
        if not args.no_update:
            update_local_status(item["row_idx"])
        print("\n" + "=" * 50)
        print("成功: 所有操作完成!")
        print("=" * 50)
    else:
        print("\n失败: 发送失败")

if __name__ == "__main__":
    main()