#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
朋友圈图片生成器 - 商业短视频封面风格
1. AI生成人物底图
2. 添加主标题、副标题、底部小字
"""

import sys
import random
import json
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("请先安装: pip install Pillow")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent

# 配色方案
COLOR_SCHEMES = [
    {
        "title": (255, 255, 255),
        "subtitle": (220, 53, 69),
        "bottom": (255, 255, 255),
    },  # 白+红+白
    {
        "title": (255, 215, 0),
        "subtitle": (255, 255, 255),
        "bottom": (200, 200, 200),
    },  # 金+白+灰
    {
        "title": (255, 255, 255),
        "subtitle": (0, 191, 255),
        "bottom": (255, 255, 255),
    },  # 白+蓝+白
]

# AI生成人物的提示词模板
PERSON_PROMPTS = [
    "young Asian woman, white t-shirt and jeans, sitting relaxed, natural expression, soft lighting, cinematic, high quality",
    "young Asian woman, casual outfit, standing pose, gentle smile, studio lighting, photorealistic",
    "young Asian woman, simple clothing, relaxed posture, looking at camera, professional photography",
]


def get_font(size, bold=False):
    """获取字体"""
    font_paths = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except:
                pass
    return ImageFont.load_default()


def generate_person_image(output_path):
    """
    调用AI生成人物图片

    Args:
        output_path: 输出路径

    Returns:
        bool: 是否成功
    """
    print("  正在AI生成人物图片...")

    # 调用 baidu-image-gen 技能
    try:
        import subprocess

        prompt = random.choice(PERSON_PROMPTS)

        # 调用图片生成脚本
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                f'''
import sys
sys.path.insert(0, r"{SCRIPT_DIR.parent.parent.parent.parent.parent}\\baidu-image-gen\\scripts")
from generate import generate_image
generate_image(
    prompt="{prompt}",
    output_path=r"{output_path}",
    width=720,
    height=1280
)
''',
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if Path(output_path).exists():
            print(f"  AI图片已生成: {output_path}")
            return True
        else:
            print(f"  AI生成失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  AI生成出错: {e}")
        return False


def create_gradient_background(width, height):
    """创建深灰到黑色渐变背景"""
    img = Image.new("RGB", (width, height))
    for y in range(height):
        # 从深灰(50,50,50)渐变到黑色(20,20,20)
        ratio = y / height
        r = int(50 - 30 * ratio)
        g = int(50 - 30 * ratio)
        b = int(50 - 30 * ratio)
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    return img


def add_text_to_image(base_img, main_title, subtitle, bottom_text):
    """
    在图片上添加文字

    Args:
        base_img: 底图
        main_title: 主标题
        subtitle: 副标题
        bottom_text: 底部小字
    """
    width, height = base_img.size
    draw = ImageDraw.Draw(base_img)

    # 选择配色
    colors = random.choice(COLOR_SCHEMES)

    # 添加半透明遮罩（让文字更清晰）
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 100))
    base_img = base_img.convert("RGBA")
    base_img = Image.alpha_composite(base_img, overlay)
    draw = ImageDraw.Draw(base_img)

    # 主标题（大字，白色或金色）
    title_font = get_font(80, bold=True)
    title_lines = main_title.split("\n")
    y = int(height * 0.15)
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        x = (width - (bbox[2] - bbox[0])) // 2
        # 添加阴影效果
        draw.text((x + 2, y + 2), line, font=title_font, fill=(0, 0, 0, 180))
        draw.text((x, y), line, font=title_font, fill=colors["title"] + (255,))
        y += 90

    # 副标题（红色粗体）
    if subtitle:
        subtitle_font = get_font(50, bold=True)
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        x = (width - (bbox[2] - bbox[0])) // 2
        y = int(height * 0.35)
        draw.text((x + 2, y + 2), subtitle, font=subtitle_font, fill=(0, 0, 0, 180))
        draw.text(
            (x, y), subtitle, font=subtitle_font, fill=colors["subtitle"] + (255,)
        )

    # 底部小字（白色居中）
    if bottom_text:
        bottom_font = get_font(30)
        bbox = draw.textbbox((0, 0), bottom_text, font=bottom_font)
        x = (width - (bbox[2] - bbox[0])) // 2
        y = int(height * 0.88)
        draw.text((x, y), bottom_text, font=bottom_font, fill=colors["bottom"] + (255,))

    # 添加日期
    date_font = get_font(24)
    date_text = datetime.now().strftime("%Y.%m.%d")
    bbox = draw.textbbox((0, 0), date_text, font=date_font)
    x = (width - (bbox[2] - bbox[0])) // 2
    draw.text(
        (x, int(height * 0.94)), date_text, font=date_font, fill=(150, 150, 150, 255)
    )

    return base_img.convert("RGB")


def generate_moments_image(
    main_title=None, subtitle=None, bottom_text=None, output_path=None
):
    """
    生成朋友圈图片

    Args:
        main_title: 主标题（必填）
        subtitle: 副标题（可选）
        bottom_text: 底部小字（可选）
        output_path: 输出路径（可选）

    Returns:
        str: 生成的图片路径
    """
    print("\n生成朋友圈图片...")

    # 图片尺寸 (9:16 竖版)
    width, height = 720, 1280

    # 默认文字
    if not main_title:
        main_title = "每一天\n都是新的开始"
    if not subtitle:
        subtitle = "保持热爱"
    if not bottom_text:
        bottom_text = "愿你我都能成为更好的自己"

    # 输出路径
    if not output_path:
        output_dir = SCRIPT_DIR / "generated_images"
        output_dir.mkdir(exist_ok=True)
        output_path = (
            output_dir / f"moments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

    # 尝试AI生成人物底图
    person_img_path = SCRIPT_DIR / "temp_person.jpg"
    ai_success = False

    try:
        ai_success = generate_person_image(str(person_img_path))
    except:
        pass

    if ai_success and person_img_path.exists():
        # 使用AI生成的图片
        base_img = Image.open(person_img_path)
        base_img = base_img.resize((width, height))
        # 清理临时文件
        person_img_path.unlink()
    else:
        # 使用渐变背景
        print("  使用渐变背景...")
        base_img = create_gradient_background(width, height)

    # 添加文字
    final_img = add_text_to_image(base_img, main_title, subtitle, bottom_text)

    # 保存
    final_img.save(output_path, quality=95)
    print(f"  图片已生成: {output_path}")

    return str(output_path)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="生成朋友圈图片")
    parser.add_argument("--title", help="主标题")
    parser.add_argument("--subtitle", help="副标题")
    parser.add_argument("--bottom", help="底部小字")
    parser.add_argument("--output", help="输出路径")

    args = parser.parse_args()
    path = generate_moments_image(args.title, args.subtitle, args.bottom, args.output)
    print(f"\n生成完成: {path}")


if __name__ == "__main__":
    main()
