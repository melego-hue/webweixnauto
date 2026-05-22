#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
极简风格图片生成器
生成纯色背景+文字的图片
"""

import sys
import random
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("请先安装: pip install Pillow")
    sys.exit(1)

# 极简配色方案
COLOR_SCHEMES = [
    {"bg": (45, 52, 54), "text": (255, 255, 255)},  # 深灰 + 白
    {"bg": (30, 39, 46), "text": (253, 203, 110)},  # 深蓝 + 金
    {"bg": (48, 71, 94), "text": (255, 255, 255)},  # 深蓝灰 + 白
    {"bg": (46, 63, 95), "text": (241, 196, 15)},  # 靛蓝 + 黄
    {"bg": (33, 33, 33), "text": (255, 255, 255)},  # 黑 + 白
    {"bg": (52, 73, 94), "text": (236, 240, 241)},  # 蓝灰 + 浅白
    {"bg": (44, 62, 80), "text": (52, 152, 219)},  # 深蓝 + 亮蓝
    {"bg": (23, 32, 42), "text": (241, 196, 15)},  # 深黑 + 金
]

# 励志语录库
QUOTES = [
    "生活不止眼前的苟且\n还有诗和远方",
    "每一天都是新的开始",
    "保持热爱\n奔赴山海",
    "慢慢来\n比较快",
    "星光不问赶路人\n时光不负有心人",
    "愿你眼里有光\n心中有爱",
    "简单生活\n快乐自己",
    "心若向阳\n无畏悲伤",
    "人生没有白走的路\n每一步都算数",
    "温柔半两\n从容一生",
    "岁月静好\n现世安稳",
    "不负时光\n不负自己",
    "且行且珍惜",
    "活在当下\n珍惜眼前",
    "做自己的光\n不需要太亮",
]


def get_font(size):
    """获取字体"""
    # Windows 系统字体路径
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except:
                pass

    # 默认字体
    return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    """自动换行"""
    lines = []
    for line in text.split("\n"):
        if not line:
            lines.append("")
            continue

        current_line = ""
        for char in line:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        if current_line:
            lines.append(current_line)

    return lines


def generate_image(text=None, output_path=None):
    """
    生成极简风格图片

    Args:
        text: 图片文字（可选，不传则随机选择）
        output_path: 输出路径（可选）

    Returns:
        str: 生成的图片路径
    """
    # 图片尺寸 (9:16 竖版)
    width, height = 1080, 1920

    # 随机选择配色
    scheme = random.choice(COLOR_SCHEMES)

    # 创建图片
    img = Image.new("RGB", (width, height), scheme["bg"])
    draw = ImageDraw.Draw(img)

    # 选择文字
    if not text:
        text = random.choice(QUOTES)

    # 字体大小
    font_size = 60
    font = get_font(font_size)

    # 自动换行
    max_width = width - 200
    lines = wrap_text(text, font, max_width, draw)

    # 计算文字总高度
    line_height = font_size * 1.5
    total_height = len(lines) * line_height

    # 居中绘制
    y = (height - total_height) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (width - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, font=font, fill=scheme["text"])
        y += line_height

    # 添加底部日期
    date_font = get_font(30)
    date_text = datetime.now().strftime("%Y.%m.%d")
    date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
    date_x = (width - (date_bbox[2] - date_bbox[0])) // 2
    draw.text((date_x, height - 150), date_text, font=date_font, fill=scheme["text"])

    # 保存图片
    if not output_path:
        output_dir = Path(__file__).parent / "generated_images"
        output_dir.mkdir(exist_ok=True)
        output_path = (
            output_dir / f"moments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

    img.save(output_path, quality=95)
    print(f"  图片已生成: {output_path}")

    return str(output_path)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="生成极简风格图片")
    parser.add_argument("--text", help="图片文字")
    parser.add_argument("--output", help="输出路径")

    args = parser.parse_args()
    path = generate_image(args.text, args.output)
    print(f"\n生成完成: {path}")


if __name__ == "__main__":
    main()
