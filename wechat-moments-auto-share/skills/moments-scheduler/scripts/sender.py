#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
朋友圈发送模块 - 封装现有的图像识别发送方案
"""

import sys
import os
import random
from pathlib import Path

# 将现有脚本路径加入 sys.path
EXISTING_SCRIPTS = Path(r"D:\weixin\wechat-moments-auto-v2\scripts")
if str(EXISTING_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(EXISTING_SCRIPTS))


def get_random_image():
    """从 images 目录随机选取图片"""
    images_dir = Path(r"D:\weixin\wechat-moments-auto-v2\images")
    if not images_dir.exists():
        return None

    exts = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
    images = []
    for ext in exts:
        images.extend(images_dir.glob(f"*{ext}"))
        images.extend(images_dir.glob(f"*{ext.upper()}"))

    if not images:
        return None

    return str(random.choice(images).absolute())


def get_matched_or_random_image(text, image_path=None):
    """获取相匹配的博主图片，若无则随机选取"""
    if image_path and Path(image_path).exists():
        return str(Path(image_path).absolute())

    # 将 D:\weixin\wechat-moments-auto-v2\scripts 加入 path 用以导入 sync_sources
    import sys
    scripts_path = str(Path(r"D:\weixin\wechat-moments-auto-v2\scripts"))
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)

    try:
        from sync_sources import get_blogger_by_text, get_blogger_image
        blogger = get_blogger_by_text(text)
        if blogger:
            matched = get_blogger_image(blogger)
            if matched:
                print(f"  ✓ 匹配博主「{blogger}」的专属图片: {Path(matched).name}")
                return matched
    except Exception as e:
        print(f"  [Warning] 博主图片匹配出错: {e}")

    # 兜底：随机选择图片
    img = get_random_image()
    if img:
        print(f"  ✓ 未匹配到博主，使用随机兜底图片: {Path(img).name}")
        return img

    return None


def send_moments_text(text, image_path=None, dry_run=False):
    """
    发送朋友圈

    Args:
        text: 文案内容
        image_path: 图片路径，None 则随机/博主匹配选取
        dry_run: 仅模拟，不实际发送

    Returns:
        tuple: (success: bool, message: str)
    """
    img = get_matched_or_random_image(text, image_path)

    if dry_run:
        return True, f"[模拟] 文案: {text[:30]}... | 图片: {img or '无图片'}"

    # 检测微信进程
    from wechat_utils import ensure_wechat_ready

    if not ensure_wechat_ready():
        return False, "微信未就绪，请确认微信已登录且在运行"

    # 发送
    from send_by_image import send_moments

    success = send_moments(text, img)

    if success:
        return True, f"发送成功: {text[:30]}..."
    else:
        return False, "发送失败，请检查微信窗口状态"


def send_moments_batch(items, dry_run=False):
    """
    批量发送

    Args:
        items: 文案列表，每项 {text, image_path}
        dry_run: 仅模拟

    Returns:
        list: 发送结果列表
    """
    results = []
    for i, item in enumerate(items):
        print(f"\n发送第 {i+1}/{len(items)} 条...")
        ok, msg = send_moments_text(item["text"], item.get("image_path"), dry_run)
        results.append({"success": ok, "message": msg, "text": item["text"][:30]})
        if not ok:
            print(f"  失败，停止批量发送")
            break
    return results


if __name__ == "__main__":
    ok, msg = send_moments_text("这是一条测试文案", dry_run=True)
    print(f"结果: {ok} - {msg}")
