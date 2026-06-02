#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WeChat Moments Auto Sender v2 - Random Images Version
Read content from Notion database and send to WeChat Moments with random images
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
import os
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID") or "your_notion_database_id_here"

# Field names from Notion database
STATUS_FIELD = "发布状态"
STATUS_PENDING = "未发布"
STATUS_COMPLETED = "已发布"
CONTENT_FIELD = "AI朋友圈文案"
TITLE_FIELD = "名称"

# Image directory for random selection (relative path)
IMAGES_DIR = Path(r"D:\weixin\wechat-moments-auto-v2\images")


def get_random_image():
    """Get a random image from the images directory"""
    if not IMAGES_DIR.exists():
        print(f"  WARNING: Image directory not found: {IMAGES_DIR}")
        return None
    
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    images = []
    
    for ext in image_extensions:
        images.extend(list(IMAGES_DIR.glob(f'*{ext}')))
        images.extend(list(IMAGES_DIR.glob(f'*{ext.upper()}')))
    
    if not images:
        print(f"  WARNING: No images found in {IMAGES_DIR}")
        return None
    
    selected_image = random.choice(images)
    print(f"  Randomly selected: {selected_image.name}")
    return str(selected_image.absolute())


def get_notion_token():
    """Get Notion API Token"""
    import os
    token = os.environ.get("NOTION_API_KEY") or os.environ.get("NOTION_TOKEN")
    if not token:
        config_file = Path("d:/AIWork/.env")
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8-sig") as f:
                    for line in f:
                        if line.startswith("NOTION_API_KEY"):
                            token = line.split("=", 1)[1].strip()
                            break
            except:
                pass
    return token or "your_notion_token_here"


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

            # Get content from AI朋友圈文案 (title field)
            content_prop = properties.get(CONTENT_FIELD, {})
            title_data = content_prop.get("title", [])
            content_text = "".join([t.get("plain_text", "") for t in title_data])
            content_text = content_text.replace("#", "").strip()

            if not content_text:
                continue

            # Get title
            title_prop = properties.get(TITLE_FIELD, {})
            title_data = title_prop.get("title", [])
            title_text = "".join([t.get("plain_text", "") for t in title_data])[:50]

            # Also check content for title if empty
            if not title_text:
                title_text = content_text[:50]

            # Get random image
            image_path = get_random_image()
            
            print(f"  OK: Found content")
            print(f"  Status: {status}")
            print(f"  Title: {title_text}")
            print(f"  Content: {content_text[:50]}...")

            return {
                "page_id": page_id,
                "title": title_text,
                "content": content_text,
                "image_path": image_path,
                "status": status,
                "completed_status": STATUS_COMPLETED
            }

        print("  No pending content found")
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
    print(f"WeChat Moments Sender v2 - Random Images")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
