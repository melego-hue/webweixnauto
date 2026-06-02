#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Multi-Source WeChat Moments Synchronizer
Fetches pending moments from Notion and Feishu and feeds them into local SQLite queue.
Supports blogger image matching and deduplication.
"""

import sys
import argparse
import random
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

# Windows encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# Import local modules
import config
from feishu_client import FeishuBitableClient

# We need to import db_manager functions, which are located in skills/moments-scheduler/scripts
MOMENTS_SCHEDULER_DIR = SCRIPT_DIR.parent / "skills" / "moments-scheduler" / "scripts"
if str(MOMENTS_SCHEDULER_DIR) not in sys.path:
    sys.path.insert(0, str(MOMENTS_SCHEDULER_DIR))

import db_manager

# Ensure SQLite is initialized
db_manager.init_db()


def get_blogger_by_text(text):
    """Determine blogger name from a given text string using config.py mappings"""
    if not text:
        return None
    for blogger, keywords in config.BLOGGER_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return blogger
    return None


def get_blogger_image(blogger):
    """Locate and return the specific image path for a matched blogger"""
    if not blogger:
        return None
    
    images_dir = Path(config.IMAGES_DIR)
    if not images_dir.exists():
        return None

    # Get the Chinese filename corresponding to the blogger
    chinese_name = config.BLOGGER_IMAGES.get(blogger, blogger)

    # Search for files named after the blogger with standard extensions
    for ext in [".png", ".jpg", ".jpeg"]:
        # Try Chinese name
        img_path = images_dir / f"{chinese_name}{ext}"
        if img_path.exists():
            return str(img_path.absolute())
        # Try English key
        img_path = images_dir / f"{blogger}{ext}"
        if img_path.exists():
            return str(img_path.absolute())

    return None


def get_random_image():
    """Get a random image path from the images directory as a fallback"""
    images_dir = Path(config.IMAGES_DIR)
    if not images_dir.exists():
        return None
    
    exts = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    images = []
    for ext in exts:
        images.extend(list(images_dir.glob(f'*{ext}')))
        images.extend(list(images_dir.glob(f'*{ext.upper()}')))
        
    if not images:
        return None
        
    return str(random.choice(images).absolute())


def is_already_imported(source_type, source_id):
    """Check if the source_id has already been synchronized in SQLite database"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM content WHERE source_type = ? AND source_id = ?",
        (source_type, source_id)
    )
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists


def sync_notion(config_key, dry_run=False):
    """Synchronize a specific Notion database config"""
    notion_cfg = config.NOTION_CONFIGS.get(config_key)
    if not notion_cfg:
        print(f"Error: Notion config key '{config_key}' not found.")
        return 0

    token = notion_cfg["token"]
    db_id = notion_cfg["database_id"]
    fields = notion_cfg["fields"]
    source_type = f"notion_{config_key}"

    print(f"\n--- Syncing Notion Database [{config_key}] ---")
    print(f"Database ID: {db_id}")

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        url = f"https://api.notion.com/v1/databases/{db_id}/query"
        # Query 100 recent pages
        payload = {
            "sorts": [{"timestamp": "created_time", "direction": "descending"}],
            "page_size": 100,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code != 200:
            print(f"  FAIL: Notion API returned HTTP {response.status_code}")
            return 0

        results = response.json().get("results", [])
        if not results:
            print("  No pages found in database.")
            return 0

        imported_count = 0
        for page in results:
            page_id = page["id"]
            properties = page["properties"]

            # 1. Check status
            status_prop = properties.get(fields["status"], {})
            status = ""
            if status_prop.get("type") == "status":
                status = status_prop.get("status", {}).get("name", "")
            elif status_prop.get("type") == "select":
                status = status_prop.get("select", {}).get("name", "")

            # Only sync pending posts
            if status != fields["status_pending"]:
                continue

            # 2. Check if already imported to prevent duplicates
            if is_already_imported(source_type, page_id):
                continue

            # 3. Get content text (handles both rich_text and title types in Notion)
            content_prop = properties.get(fields["content"], {})
            content_data = []
            if content_prop.get("type") == "title":
                content_data = content_prop.get("title", [])
            elif content_prop.get("type") == "rich_text":
                content_data = content_prop.get("rich_text", [])
            
            content_text = "".join([t.get("plain_text", "") for t in content_data])
            content_text = content_text.replace("#", "").strip()

            if not content_text:
                continue

            # 4. Get title/name
            title_prop = properties.get(fields["title"], {})
            title_data = title_prop.get("title", []) if title_prop.get("type") == "title" else title_prop.get("rich_text", [])
            title_text = "".join([t.get("plain_text", "") for t in title_data])[:100]

            # Fallback title to content excerpt
            if not title_text:
                title_text = content_text[:30]

            # 5. Blogger Image Matching
            blogger = get_blogger_by_text(title_text) or get_blogger_by_text(content_text)
            image_path = get_blogger_image(blogger)
            
            if image_path:
                img_desc = f"Matched Blogger: {blogger} ({Path(image_path).name})"
            else:
                image_path = get_random_image()
                img_desc = f"Random Fallback: {Path(image_path).name if image_path else 'None'}"

            print(f"  Found pending Moment (ID: {page_id[:8]}):")
            print(f"    Title: {title_text}")
            print(f"    Content: {content_text[:40]}...")
            print(f"    Image: {img_desc}")

            if not dry_run:
                db_manager.add_content(
                    text=content_text,
                    category="custom",
                    tags=f"{config_key},notion",
                    emoji="",
                    source=db_manager.SOURCE_MANUAL,
                    image_path=image_path or "",
                    source_type=source_type,
                    source_id=page_id
                )
            imported_count += 1

        print(f"  ✓ Sync finished. Imported {imported_count} new items.")
        return imported_count

    except Exception as e:
        print(f"  FAIL: Notion sync failed: {e}")
        return 0


def sync_feishu(dry_run=False):
    """Synchronize Feishu Bitable"""
    fs_cfg = config.FEISHU_CONFIG
    source_type = "feishu"

    print("\n--- Syncing Feishu Bitable ---")
    print(f"App Token: {fs_cfg['app_token']}")
    print(f"Table ID: {fs_cfg['table_id']}")

    if fs_cfg["app_id"] == "cli_a72c1c68f23f500d" or fs_cfg["app_secret"].startswith("o83C3u7r6XwV"):
        print("  WARNING: Feishu app credentials appear to be placeholders. Skipping...")
        return 0

    try:
        client = FeishuBitableClient(fs_cfg["app_id"], fs_cfg["app_secret"])
        records = client.fetch_records(
            app_token=fs_cfg["app_token"],
            table_id=fs_cfg["table_id"],
            filter_field=fs_cfg["fields"]["status"],
            filter_value=fs_cfg["fields"]["status_pending"]
        )

        if not records:
            print("  No pending records found in Feishu.")
            return 0

        imported_count = 0
        for rec in records:
            record_id = rec["record_id"]
            fields = rec["fields"]

            # Double check status just in case client-side filter is bypassed
            status_val = fields.get(fs_cfg["fields"]["status"], "")
            if isinstance(status_val, list):
                status_str = ",".join([str(v) for v in status_val])
            elif isinstance(status_val, dict):
                status_str = str(status_val.get("text", ""))
            else:
                status_str = str(status_val)
                
            if status_str.strip() != fs_cfg["fields"]["status_pending"]:
                continue

            # Check duplication
            if is_already_imported(source_type, record_id):
                continue

            # Get Content (can be rich_text list or simple string)
            content_val = fields.get(fs_cfg["fields"]["content"], "")
            if isinstance(content_val, list):
                content_text = "".join([x.get("text", "") for x in content_val if isinstance(x, dict)])
            else:
                content_text = str(content_val)
            content_text = content_text.replace("#", "").strip()

            if not content_text:
                continue

            # Get Title
            title_val = fields.get(fs_cfg["fields"]["title"], "")
            if isinstance(title_val, list):
                title_text = "".join([x.get("text", "") for x in title_val if isinstance(x, dict)])
            else:
                title_text = str(title_val)
            title_text = title_text[:100]

            if not title_text:
                title_text = content_text[:30]

            # Blogger matching
            blogger = get_blogger_by_text(title_text) or get_blogger_by_text(content_text)
            image_path = get_blogger_image(blogger)
            
            if image_path:
                img_desc = f"Matched Blogger: {blogger} ({Path(image_path).name})"
            else:
                image_path = get_random_image()
                img_desc = f"Random Fallback: {Path(image_path).name if image_path else 'None'}"

            print(f"  Found pending Moment (ID: {record_id}):")
            print(f"    Title: {title_text}")
            print(f"    Content: {content_text[:40]}...")
            print(f"    Image: {img_desc}")

            if not dry_run:
                db_manager.add_content(
                    text=content_text,
                    category="custom",
                    tags="feishu,bitable",
                    emoji="",
                    source=db_manager.SOURCE_MANUAL,
                    image_path=image_path or "",
                    source_type=source_type,
                    source_id=record_id
                )
            imported_count += 1

        print(f"  ✓ Sync finished. Imported {imported_count} new items.")
        return imported_count

    except Exception as e:
        print(f"  FAIL: Feishu sync failed: {e}")
        return 0


def update_remote_status(source_type, source_id, status_completed):
    """
    Callback function triggered after successful local send.
    Updates the status back in Notion or Feishu.
    """
    print(f"\nUpdating remote status for [{source_type}] (ID: {source_id}) to: {status_completed}")
    
    try:
        # Notion update
        if source_type.startswith("notion_"):
            config_key = source_type.replace("notion_", "")
            notion_cfg = config.NOTION_CONFIGS.get(config_key)
            if not notion_cfg:
                return False
                
            headers = {
                "Authorization": f"Bearer {notion_cfg['token']}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            }
            url = f"https://api.notion.com/v1/pages/{source_id}"
            payload = {"properties": {notion_cfg["fields"]["status"]: {"status": {"name": status_completed}}}}
            
            response = requests.patch(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print("  ✓ Remote status updated successfully in Notion")
                return True
            else:
                # Some tables use select field instead of status field, try fallback payload
                payload_select = {"properties": {notion_cfg["fields"]["status"]: {"select": {"name": status_completed}}}}
                response_select = requests.patch(url, headers=headers, json=payload_select, timeout=10)
                if response_select.status_code == 200:
                    print("  ✓ Remote status updated successfully in Notion (select fallback)")
                    return True
                print(f"  FAIL: Notion status update failed (HTTP {response.status_code})")
                return False
                
        # Feishu update
        elif source_type == "feishu":
            fs_cfg = config.FEISHU_CONFIG
            client = FeishuBitableClient(fs_cfg["app_id"], fs_cfg["app_secret"])
            success = client.update_record_status(
                app_token=fs_cfg["app_token"],
                table_id=fs_cfg["table_id"],
                record_id=source_id,
                status_field=fs_cfg["fields"]["status"],
                status_value=status_completed
            )
            return success
            
    except Exception as e:
        print(f"  FAIL: Remote status update error: {e}")
        return False
    return False


def main():
    parser = argparse.ArgumentParser(description="Multi-Source WeChat Moments Synchronizer")
    parser.add_argument(
        "--source",
        choices=["all", "luffy", "v2", "feishu"],
        default="all",
        help="Select synchronization source (default: all)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run: scan only, do not write to local SQLite queue"
    )

    args = parser.parse_args()

    print("=" * 60)
    print(f"WeChat Moments Sync Console - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if args.dry_run:
        print("[DRY RUN MODE - SCAN ONLY]")
    print("=" * 60)

    total_imported = 0

    if args.source in ["all", "luffy"]:
        total_imported += sync_notion("luffy", args.dry_run)
        
    if args.source in ["all", "v2"]:
        total_imported += sync_notion("v2", args.dry_run)

    if args.source in ["all", "feishu"]:
        total_imported += sync_feishu(args.dry_run)

    print("\n" + "=" * 60)
    print(f"Summary: Sync complete. Imported {total_imported} new items to SQLite queue.")
    print("=" * 60)


if __name__ == "__main__":
    main()
