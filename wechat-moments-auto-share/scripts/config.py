#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration for WeChat Moments Auto Sender
统一配置文件 - 支持多 Notion 数据库与飞书多维表格
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path("D:/weixin/wechat-moments-auto-v2")
IMAGES_DIR = PROJECT_ROOT / "images"
UI_IMAGES_DIR = PROJECT_ROOT / "ui_images"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def _load_env():
    """Load configuration from d:/AIWork/.env"""
    env_vars = {}
    env_path = Path("d:/AIWork/.env")
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            env_vars[parts[0].strip()] = parts[1].strip()
        except Exception as e:
            print(f"[Warning] Failed to load .env: {e}")
    return env_vars


ENV_VARS = _load_env()

# Notion Multi-Database Configuration
NOTION_CONFIGS = {
    "luffy": {
        "token": ENV_VARS.get("NOTION_API_KEY_LUFFY", "your_luffy_token_here"),
        "database_id": ENV_VARS.get("NOTION_DATABASE_ID_LUFFY", "your_luffy_db_id_here"),  # 路飞全自动发稿池V2.5
        "fields": {
            "status": "平台/状态",
            "content": "AI朋友圈金句",
            "title": "名称",
            "status_pending": "未开始",
            "status_completed": "完成",
        }
    },
    "v2": {
        "token": ENV_VARS.get("NOTION_API_KEY", "your_notion_token_here"),
        "database_id": ENV_VARS.get("NOTION_DATABASE_ID", "your_notion_db_id_here"),
        "fields": {
            "status": "发布状态",
            "content": "AI朋友圈文案",
            "title": "名称",
            "status_pending": "未发布",
            "status_completed": "已发布",
        }
    }
}

# Keep original fields for backward compatibility (defaults to 'luffy')
NOTION_API_TOKEN = NOTION_CONFIGS["luffy"]["token"]
DATABASE_ID = NOTION_CONFIGS["luffy"]["database_id"]
NOTION_FIELDS = NOTION_CONFIGS["luffy"]["fields"]

# SiliconFlow API Credentials (for automated McKinsey Trust copywriting generation)
SILICONFLOW_API_KEY = ENV_VARS.get("SILICONFLOW_API_KEY", "your_siliconflow_key_here")
# Default to DeepSeek-V3 on SiliconFlow, fallback to deepseek-chat
SILICONFLOW_MODEL = ENV_VARS.get("AI_MODEL", "deepseek-ai/DeepSeek-V3")


# Feishu Bitable (Lark Multidimensional Table) Configuration
FEISHU_CONFIG = {
    # Replace these with your real custom app credentials if needed
    "app_id": "cli_a72c1c68f23f500d",
    "app_secret": "o83C3u7r6XwVn5t4h3g2f1e0d9c8b7a6",
    # The Bitable App Token (found in the Bitable URL: /base/[APP_TOKEN])
    "app_token": "bascnN87a9b8c7d6e5f4g3h2i1j",
    # The Table ID of your Bitable sheet (found in Table tab or properties)
    "table_id": "tblx7f8e9a0b1c2d",
    "fields": {
        "status": "发布状态",         # Single Option field
        "content": "AI朋友圈文案",    # Text field
        "title": "名称",              # Text field (blogger recognition)
        "status_pending": "未开始",
        "status_completed": "完成",
    }
}

# Blogger keywords mapping for matching images
BLOGGER_KEYWORDS = {
    "Luffy": ["不卖珠宝的路飞", "自己学易的路飞", "自己造船的路飞", "路飞"],
    "Dayuan": ["遇见大元", "大元"],
    "Quange": ["全哥"],
    "Lizhen": ["李真"],
}

# Blogger to image name mapping
BLOGGER_IMAGES = {
    "Luffy": "路飞",
    "Dayuan": "大元",
    "Quange": "全哥",
    "Lizhen": "李真",
}

# Image recognition settings for pyautogui
IMAGE_RECOGNITION = {
    "confidence": 0.7,
    "max_retries": 2,
    "search_timeout": 5,
}

# Timing settings for auto posting
DEFAULT_MIN_DELAY = 5  # minutes
DEFAULT_MAX_DELAY = 15  # minutes

# WeChat activation strategies
WECHAT_ACTIVATION = {
    "max_retries": 2,
    "shortcut": "ctrl+alt+w",
}

