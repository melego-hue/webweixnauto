#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration for WeChat Moments Auto Sender
统一配置文件
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path("D:/weixin/wechat-moments-auto")
IMAGES_DIR = PROJECT_ROOT / "images"
UI_IMAGES_DIR = PROJECT_ROOT / "ui_images"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Notion Configuration
NOTION_API_TOKEN = "ntn_p65367370428mJhjCSr1SHNrMVxmqVwQFTjx3zBG0cl5xc"
DATABASE_ID = "3391859e-b112-80b9-948c-c1cbc77b46a3"  # 路飞全自动发稿池V2.5

# Field names from Notion database
NOTION_FIELDS = {
    "status": "平台/状态",
    "content": "AI朋友圈金句",
    "title": "名称",
    "status_pending": "未开始",
    "status_completed": "完成",
}

# Blogger keywords mapping
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

# Image recognition settings
IMAGE_RECOGNITION = {
    "confidence": 0.7,
    "max_retries": 2,
    "search_timeout": 5,
}

# Timing settings
DEFAULT_MIN_DELAY = 5  # minutes
DEFAULT_MAX_DELAY = 15  # minutes

# WeChat activation strategies
WECHAT_ACTIVATION = {
    "max_retries": 2,
    "shortcut": "ctrl+alt+w",
}
