#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WeChat Moments Auto Sender - Notion Integration
Read content from Notion database and send to WeChat Moments
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
DATABASE_ID = ""  # 请填写你的Notion数据库ID（留空表示不使用Notion版本）

# Field names from 路飞全自动发稿池V2.5
STATUS_FIELD = "平台/状态"
STATUS_PENDING = "未开始"
STATUS_COMPLETED = "完成"
CONTENT_FIELD = "AI朋友圈金句"
TITLE_FIELD = "名称"

BLOGGER_KEYWORDS = {
    "Luffy": ["不卖珠宝的路飞", "自己学易的路飞", "自己造船的路飞", "路飞"],
    "Dayuan": ["遇见大元", "大元"],
    "Quange": ["全哥"],
    "Lizhen": ["李真"],
}


def get_blogger_by_name(name):
    """Determine blogger from name"""
    for blogger, keywords in BLOGGER_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name:
                return blogger
    return None


def get_blogger_image(blogger):
    """Get blogger image path"""
    if not blogger:
        return None
    images_dir = Path("D:/weixin/wechat-moments-auto/images")
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


def get_notion_token():
    """Get Notion API Token"""
    return ""  # 请填写你的Notion API Token（留空表示不使用Notion版本）


def fetch_notion_content():
    """Fetch pending content from Notion"""
    print("\nFetching content from Notion...")

    try:
        import requests

        token = get_notion_token()
        if not token:
            print("  FAIL: NOTION_API_KEY not found")
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        payload = {
            "sorts": [{"timestamp": "created_time", "direction": "descending"}],
            "page_size": 50,
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"  FAIL: Notion API error: {response.status_code}")
            return None

        results = response.json().get("results", [])
        if not results:
            print("  No content found in database")
            return None

        for page in results:
            page_id = page["id"]
            properties = page["properties"]

            # Get status
            status_prop = properties.get(STATUS_FIELD, {})
            status = status_prop.get("status", {}).get("name", "")
            
            # Only process pending content
            if status != STATUS_PENDING:
                continue

            # Get content from AI朋友圈金句 (rich_text field)
            content_prop = properties.get(CONTENT_FIELD, {})
            rich_text_data = content_prop.get("rich_text", [])
            content_text = "".join([t.get("plain_text", "") for t in rich_text_data])
            content_text = content_text.replace("#", "").strip()

            if not content_text:
                continue

            # Get title for blogger recognition
            title_prop = properties.get(TITLE_FIELD, {})
            title_data = title_prop.get("title", [])
            title_text = "".join([t.get("plain_text", "") for t in title_data])[:50]

            # Also check content for blogger keywords
            if not title_text:
                title_text = content_text[:50]

            blogger = get_blogger_by_name(title_text)

            image_path = get_blogger_image(blogger) if blogger else None

            # Skip if no image available
            if not image_path:
                print(f"  Skip: No image for blogger '{blogger or 'Unknown'}', continuing...")
                continue

            print(f"  OK: Found content")
            print(f"  Status: {status}")
            print(f"  Blogger: {blogger}")
            print(f"  Image: {Path(image_path).name}")
            print(f"  Content: {content_text[:50]}...")

            return {
                "page_id": page_id,
                "title": title_text,
                "content": content_text,
                "blogger": blogger,
                "image_path": image_path,
                "status": status,
                "completed_status": STATUS_COMPLETED
            }

        print("  No pending content found (all items without images were skipped)")
        return None

    except Exception as e:
        print(f"  FAIL: Fetch failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def update_notion_status(page_id, status):
    """Update Notion page status"""
    print(f"\nUpdating Notion status to: {status}")

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
        payload = {"properties": {STATUS_FIELD: {"status": {"name": status}}}}

        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"  OK: Status updated")
            return True
        else:
            print(f"  FAIL: Update failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"  FAIL: Update failed: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Send moments from Notion")
    parser.add_argument("--dry-run", action="store_true", help="Simulate only")
    parser.add_argument("--no-update", action="store_true", help="Don't update status")
    parser.add_argument("--min-delay", type=int, default=5, help="Min delay in minutes")
    parser.add_argument("--max-delay", type=int, default=15, help="Max delay in minutes")
    args = parser.parse_args()

    print("=" * 50)
    print(f"Notion -> WeChat Moments - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    if args.max_delay > 0:
        delay_minutes = random.randint(args.min_delay, args.max_delay)
        delay_seconds = delay_minutes * 60
        print(f"\nRandom delay: {delay_minutes} minutes...")
        print(f"Actual send time: {(datetime.now().replace(second=0, microsecond=0) + __import__('datetime').timedelta(minutes=delay_minutes)).strftime('%H:%M')}")
        time.sleep(delay_seconds)

    item = fetch_notion_content()
    if not item:
        print("\nNo pending content")
        return

    if args.dry_run:
        print(f"\n[Dry Run] Will send:")
        print(f"  Title: {item['title']}")
        print(f"  Blogger: {item['blogger']}")
        print(f"  Image: {item['image_path'] or 'None'}")
        print(f"  Content: {item['content'][:100]}...")
        print(f"  Will update status to: {item['completed_status']}")
        return

    print("\nSending moments...")
    from send_by_image import send_moments

    success = send_moments(item["content"], item["image_path"])

    if success:
        if not args.no_update:
            update_notion_status(item["page_id"], item["completed_status"])
        print("\n" + "=" * 50)
        print("SUCCESS: All done!")
        print("=" * 50)
    else:
        print("\nFAIL: Send failed")


if __name__ == "__main__":
    main()
