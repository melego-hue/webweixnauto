#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 Notion 读取朋友圈内容并发送
根据名称自动选择对应博主的图片
无法识别博主的条目自动跳过
"""

import sys
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent

# 博主名称关键词映射（用户需根据实际情况修改）
# 示例：BLOGGER_KEYWORDS = {"博主A": ["关键词1", "关键词2"], "博主B": ["关键词3"]}
BLOGGER_KEYWORDS = {
    # 在此处添加你的博主映射
    # "博主名称": ["名称关键词1", "名称关键词2"],
}


def get_blogger_by_name(name):
    """根据名称判断博主"""
    for blogger, keywords in BLOGGER_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name:
                return blogger
    return None


def get_blogger_image(blogger):
    """获取博主对应的图片路径"""
    if not blogger:
        return None
    images_dir = SCRIPT_DIR / "images"
    for ext in [".png", ".jpg", ".jpeg"]:
        image_path = images_dir / f"{blogger}{ext}"
        if image_path.exists():
            return str(image_path.absolute())
    return None


def get_notion_token():
    """获取 Notion API Token"""
    import os

    # 优先从环境变量读取
    token = os.environ.get("NOTION_API_KEY") or os.environ.get("NOTION_TOKEN")

    # 如果环境变量不存在，尝试从配置文件读取
    if not token:
        # 用户可在环境变量 CONFIG_FILE 指定配置文件路径
        config_file = os.environ.get("CONFIG_FILE")
        if config_file and Path(config_file).exists():
            with open(config_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("NOTION_API_KEY"):
                        token = line.split("=", 1)[1].strip()
                        break

    return token


def fetch_notion_content():
    """从 Notion 获取待发送内容，自动跳过无法识别博主的条目"""
    print("\n从 Notion 获取内容...")

    try:
        import requests
        import os

        token = get_notion_token()
        if not token:
            print("  ✗ 未找到 NOTION_API_KEY")
            print("  请设置环境变量 NOTION_API_KEY 或在配置文件中配置")
            return None

        # 从环境变量读取数据库ID
        database_id = os.environ.get("NOTION_DATABASE_ID")
        if not database_id:
            print("  ✗ 未找到 NOTION_DATABASE_ID")
            print("  请设置环境变量 NOTION_DATABASE_ID")
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        # 查询多条，以便跳过无法识别的
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        payload = {
            "filter": {"property": "平台/状态", "status": {"equals": "未开始"}},
            "sorts": [{"timestamp": "created_time", "direction": "descending"}],
            "page_size": 10,
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"  ✗ Notion API 错误: {response.status_code}")
            return None

        results = response.json().get("results", [])
        if not results:
            print("  没有找到待发送的内容")
            return None

        # 遍历找到第一个能识别博主的条目
        for page in results:
            page_id = page["id"]
            properties = page["properties"]

            title = properties.get("名称", {}).get("title", [])
            title_text = title[0]["plain_text"] if title else "无标题"

            content = properties.get("AI小红书洗稿", {}).get("rich_text", [])
            content_text = (
                "".join([t["plain_text"] for t in content]) if content else ""
            )

            if not content_text:
                continue

            # 判断博主
            blogger = get_blogger_by_name(title_text)
            if not blogger:
                print(f"  跳过 '{title_text}' (无法识别博主)")
                continue

            image_path = get_blogger_image(blogger)

            print(f"  ✓ 找到内容: {title_text}")
            print(f"  博主: {blogger}")
            if image_path:
                print(f"  图片: {Path(image_path).name}")
            print(f"  内容: {content_text[:50]}...")

            return {
                "page_id": page_id,
                "title": title_text,
                "content": content_text,
                "blogger": blogger,
                "image_path": image_path,
            }

        print("  没有找到可发送的内容（博主未识别）")
        return None

    except Exception as e:
        print(f"  ✗ 获取失败: {e}")
        return None


def update_notion_status(page_id, status="已发布"):
    """更新 Notion 页面状态"""
    print(f"\n更新 Notion 状态为: {status}")

    try:
        import requests

        token = get_notion_token()
        if not token:
            return False

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"properties": {"平台/状态": {"status": {"name": status}}}}

        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"  ✓ 状态已更新")
            return True
        return False

    except Exception as e:
        print(f"  ✗ 更新失败: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="从 Notion 读取并发送朋友圈")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    parser.add_argument("--no-update", action="store_true", help="发送后不更新状态")
    args = parser.parse_args()

    print("=" * 50)
    print(f"Notion → 微信朋友圈 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    item = fetch_notion_content()
    if not item:
        print("\n没有待发送的内容")
        return

    if args.dry_run:
        print(f"\n[模拟运行] 将发送:")
        print(f"  标题: {item['title']}")
        print(f"  博主: {item['blogger']}")
        print(f"  图片: {item['image_path'] or '无'}")
        print(f"  内容: {item['content'][:100]}...")
        return

    print("\n开始发送朋友圈...")
    from send_by_image import send_moments

    success = send_moments(item["content"], item["image_path"])

    if success:
        if not args.no_update:
            update_notion_status(item["page_id"], "已发布")
        print("\n" + "=" * 50)
        print("✓ 全部完成！")
        print("=" * 50)
    else:
        print("\n✗ 发送失败")


if __name__ == "__main__":
    main()
