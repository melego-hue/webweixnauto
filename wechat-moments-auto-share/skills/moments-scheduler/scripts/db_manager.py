#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本地 SQLite 文案数据库管理
表结构：content (id, category, text, tags, emoji, status, source, created_at, sent_at)
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

DB_DIR = Path(r"D:\weixin\wechat-moments-auto-v2\data")
DB_PATH = DB_DIR / "moments.db"

# 文案分类
CATEGORIES = ["morning", "noon", "evening", "night", "motivation", "life", "work", "festival", "custom"]

# 状态
STATUS_PENDING = "pending"
STATUS_SENT = "sent"
STATUS_SKIPPED = "skipped"

# 来源
SOURCE_MANUAL = "manual"
SOURCE_TEMPLATE = "template"
SOURCE_LLM = "llm"


def get_connection():
    """获取数据库连接"""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL DEFAULT 'custom',
            text TEXT NOT NULL,
            tags TEXT DEFAULT '',
            emoji TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            source TEXT NOT NULL DEFAULT 'manual',
            created_at TEXT NOT NULL,
            sent_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS send_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER,
            text TEXT NOT NULL,
            image_path TEXT,
            success INTEGER NOT NULL DEFAULT 0,
            error_msg TEXT,
            sent_at TEXT NOT NULL,
            FOREIGN KEY (content_id) REFERENCES content(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            cron_expr TEXT,
            enabled INTEGER NOT NULL DEFAULT 0,
            category TEXT DEFAULT 'random',
            min_delay INTEGER DEFAULT 5,
            max_delay INTEGER DEFAULT 15,
            last_run TEXT,
            created_at TEXT NOT NULL
        )
    """)
    
    # 自动升级：检查并添加新增列
    cursor.execute("PRAGMA table_info(content)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "image_path" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN image_path TEXT DEFAULT ''")
        print("  Database migration: added column 'image_path' to content table")
    if "source_type" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN source_type TEXT DEFAULT 'local'")
        print("  Database migration: added column 'source_type' to content table")
    if "source_id" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN source_id TEXT DEFAULT ''")
        print("  Database migration: added column 'source_id' to content table")
        
    conn.commit()
    conn.close()
    print("数据库初始化与迁移完成")


def add_content(text, category="custom", tags="", emoji="", source=SOURCE_MANUAL, image_path="", source_type="local", source_id=""):
    """添加文案"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO content (category, text, tags, emoji, status, source, created_at, image_path, source_type, source_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (category, text, tags, emoji, STATUS_PENDING, source, now, image_path, source_type, source_id),
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def add_contents_batch(items):
    """批量添加文案"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0
    for item in items:
        cursor.execute(
            "INSERT INTO content (category, text, tags, emoji, status, source, created_at, image_path, source_type, source_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                item.get("category", "custom"),
                item["text"],
                item.get("tags", ""),
                item.get("emoji", ""),
                STATUS_PENDING,
                item.get("source", SOURCE_MANUAL),
                now,
                item.get("image_path", ""),
                item.get("source_type", "local"),
                item.get("source_id", ""),
            ),
        )
        count += 1
    conn.commit()
    conn.close()
    return count


def get_random_pending(category=None):
    """随机获取一条未发送的文案"""
    conn = get_connection()
    cursor = conn.cursor()
    if category and category != "random":
        cursor.execute(
            "SELECT * FROM content WHERE status = ? AND category = ? ORDER BY RANDOM() LIMIT 1",
            (STATUS_PENDING, category),
        )
    else:
        cursor.execute(
            "SELECT * FROM content WHERE status = ? ORDER BY RANDOM() LIMIT 1",
            (STATUS_PENDING,),
        )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def mark_as_sent(content_id):
    """标记为已发送"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE content SET status = ?, sent_at = ? WHERE id = ?", (STATUS_SENT, now, content_id))
    conn.commit()
    conn.close()


def mark_as_skipped(content_id):
    """标记为跳过"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE content SET status = ? WHERE id = ?", (STATUS_SKIPPED, content_id))
    conn.commit()
    conn.close()


def get_stats():
    """获取统计信息"""
    conn = get_connection()
    cursor = conn.cursor()
    stats = {}

    # 总数
    cursor.execute("SELECT COUNT(*) FROM content")
    stats["total"] = cursor.fetchone()[0]

    # 各状态数量
    cursor.execute("SELECT status, COUNT(*) FROM content GROUP BY status")
    for row in cursor.fetchall():
        stats[row[0]] = row[1]

    # 各分类数量
    cursor.execute("SELECT category, COUNT(*) FROM content GROUP BY category")
    stats["by_category"] = [{"category": r[0], "count": r[1]} for r in cursor.fetchall()]

    # 最近发送
    cursor.execute("SELECT text, sent_at FROM content WHERE status = ? ORDER BY sent_at DESC LIMIT 5", (STATUS_SENT,))
    stats["recent"] = [{"text": r[0][:50], "sent_at": r[1]} for r in cursor.fetchall()]

    conn.close()
    return stats


def list_content(status=None, category=None, limit=20):
    """列出文案"""
    conn = get_connection()
    cursor = conn.cursor()
    conditions = []
    params = []

    if status:
        conditions.append("status = ?")
        params.append(status)
    if category:
        conditions.append("category = ?")
        params.append(category)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    cursor.execute(f"SELECT * FROM content {where} ORDER BY created_at DESC LIMIT ?", params + [limit])
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_content(keyword, limit=20):
    """搜索文案"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM content WHERE text LIKE ? OR tags LIKE ? ORDER BY created_at DESC LIMIT ?",
        (f"%{keyword}%", f"%{keyword}%", limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_pending_count():
    """获取未发送数量"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM content WHERE status = ?", (STATUS_PENDING,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def reset_all_pending():
    """将所有已发送重置为未发送"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE content SET status = ?, sent_at = NULL WHERE status = ?", (STATUS_PENDING, STATUS_SENT))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected


def log_send(content_id, text, image_path, success, error_msg=None):
    """记录发送日志"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO send_log (content_id, text, image_path, success, error_msg, sent_at) VALUES (?, ?, ?, ?, ?, ?)",
        (content_id, text, image_path, 1 if success else 0, error_msg, now),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    stats = get_stats()
    print(f"\n数据库统计:")
    print(f"  总文案数: {stats['total']}")
    print(f"  待发送: {stats.get('pending', 0)}")
    print(f"  已发送: {stats.get('sent', 0)}")
