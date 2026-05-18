#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
朋友圈内容生成器
自动生成适合发朋友圈的内容
"""

import random
from datetime import datetime

# 内容模板库
TEMPLATES = {
    "morning": [
        "早安☀️ 新的一天，新的开始",
        "又是元气满满的一天💪",
        "清晨的阳光，是最好的礼物🌅",
        "早安，今天也要加油鸭！",
        "每一个清晨都是新的希望✨",
    ],
    "noon": [
        "中午好☀️ 记得好好吃饭",
        "忙碌的上午结束了，午餐时间到🍽️",
        "午后时光，一杯咖啡的惬意☕",
        "中午休息一下，下午继续冲💪",
    ],
    "evening": [
        "傍晚的晚霞，总是那么美🌅",
        "下班啦！今天也是充实的一天",
        "夕阳无限好，只是近黄昏🌇",
        "傍晚的微风，带走一天的疲惫",
    ],
    "night": [
        "晚安，愿美梦相伴🌙",
        "结束了一天，好好休息💤",
        "夜深了，该休息了晚安⭐",
        "今天也很棒，晚安世界🌙",
    ],
    "motivation": [
        "生活不会辜负每一个努力的人💪",
        "坚持就是胜利，加油！",
        "每一次努力，都是未来的铺垫✨",
        "相信自己，你比想象中更强大",
        "梦想还是要有的，万一实现了呢🌟",
    ],
    "life": [
        "生活需要仪式感✨",
        "简单的快乐，就是最好的生活",
        "享受当下的每一刻",
        "生活不止眼前的苟且，还有诗和远方",
        "平凡的日子里，也有小确幸🌸",
    ],
    "work": [
        "工作使我快乐（假的）😂",
        "打工人，打工魂，打工都是人上人💪",
        "今天也是搬砖的一天",
        "努力工作，认真生活",
        "工作再忙，也要记得喝水休息☕",
    ],
}

# 节日祝福（可根据需要扩展）
FESTIVALS = {
    "01-01": "新年快乐！🎆",
    "02-14": "情人节快乐💕",
    "05-01": "劳动节快乐！致敬每一位劳动者💪",
    "10-01": "国庆节快乐！🇨🇳",
}


def get_time_category():
    """根据当前时间获取时段分类"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 14:
        return "noon"
    elif 14 <= hour < 18:
        return "evening"
    else:
        return "night"


def check_festival():
    """检查今天是否是节日"""
    today = datetime.now().strftime("%m-%d")
    return FESTIVALS.get(today)


def generate_content():
    """
    生成朋友圈内容

    Returns:
        str: 生成的内容
    """
    # 先检查节日
    festival_content = check_festival()
    if festival_content:
        return festival_content

    # 根据时间选择模板
    time_category = get_time_category()

    # 随机选择一个主题
    themes = [time_category, "motivation", "life", "work"]
    selected_theme = random.choice(themes)

    # 从模板中随机选择
    if selected_theme in TEMPLATES:
        content = random.choice(TEMPLATES[selected_theme])
    else:
        content = random.choice(TEMPLATES["life"])

    return content


def main():
    content = generate_content()
    print(content)
    return content


if __name__ == "__main__":
    main()
