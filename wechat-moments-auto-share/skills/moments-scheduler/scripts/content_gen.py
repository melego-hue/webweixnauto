#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本地化中文朋友圈文案生成器
支持模板生成 + LLM 增强生成，彻底脱离 Notion 依赖
"""

import random
from datetime import datetime

# ============================================================
# 中文朋友圈文案模板库（本地化）
# ============================================================

TEMPLATES = {
    "morning": [
        {"text": "早安，新的一天开始了", "emoji": "☀️", "tags": "早安,正能量"},
        {"text": "早晨的阳光是最好的礼物", "emoji": "🌅", "tags": "早安,阳光"},
        {"text": "每一个清晨都是一次新的开始", "emoji": "✨", "tags": "早安,励志"},
        {"text": "早起的鸟儿有虫吃，新的一天加油", "emoji": "🐦", "tags": "早安,加油"},
        {"text": "清晨的第一缕阳光，照进心里", "emoji": "💛", "tags": "早安,温暖"},
        {"text": "元气满满的一天从早餐开始", "emoji": "🥐", "tags": "早安,生活"},
        {"text": "今天也要做个开心的人", "emoji": "😊", "tags": "早安,开心"},
        {"text": "生活明朗，万物可爱，早安", "emoji": "🌸", "tags": "早安,美好"},
        {"text": "晨风拂面，心也跟着轻盈起来", "emoji": "🍃", "tags": "早安,清新"},
        {"text": "新的一天，请多关照", "emoji": "🙏", "tags": "早安,日常"},
    ],
    "noon": [
        {"text": "午饭时间到，记得好好吃饭", "emoji": "🍚", "tags": "中午,吃饭"},
        {"text": "上午辛苦了，中午好好犒劳自己", "emoji": "🍜", "tags": "中午,犒劳"},
        {"text": "午安，吃饱才有力气继续搬砖", "emoji": "💪", "tags": "中午,搬砖"},
        {"text": "今天的午餐有点丰盛", "emoji": "🥢", "tags": "中午,美食"},
        {"text": "午休一下，下午继续战斗", "emoji": "☕", "tags": "中午,午休"},
    ],
    "evening": [
        {"text": "下班了，今天也是充实的一天", "emoji": "🏠", "tags": "傍晚,下班"},
        {"text": "夕阳无限好，只是近黄昏", "emoji": "🌇", "tags": "傍晚,夕阳"},
        {"text": "一天的工作结束，享受属于自己的时间", "emoji": "🍵", "tags": "傍晚,放松"},
        {"text": "傍晚的风，吹走了一天的疲惫", "emoji": "🌬️", "tags": "傍晚,惬意"},
        {"text": "今天你过得怎么样？", "emoji": "🤔", "tags": "傍晚,互动"},
    ],
    "night": [
        {"text": "晚安，愿你好梦", "emoji": "🌙", "tags": "晚安,好梦"},
        {"text": "夜深了，是时候休息了", "emoji": "💤", "tags": "晚安,休息"},
        {"text": "今天的一切都过去了，明天会更好", "emoji": "🌟", "tags": "晚安,希望"},
        {"text": "安静的夜晚，适合思考人生", "emoji": "🌃", "tags": "晚安,思考"},
        {"text": "睡前原谅一切，醒来便是新生", "emoji": "🕯️", "tags": "晚安,治愈"},
        {"text": "熬夜的人都是有故事的人", "emoji": "📖", "tags": "晚安,夜猫子"},
        {"text": "月亮不睡你不睡，你是秃头小宝贝", "emoji": "🌝", "tags": "晚安,搞笑"},
    ],
    "motivation": [
        {"text": "生活不会辜负每一个努力的人", "emoji": "💪", "tags": "励志,努力"},
        {"text": "坚持就是胜利，加油！", "emoji": "🔥", "tags": "励志,坚持"},
        {"text": "你吃过的苦，终会照亮前行的路", "emoji": "🛤️", "tags": "励志,成长"},
        {"text": "相信自己，你比想象中更强大", "emoji": "⚡", "tags": "励志,自信"},
        {"text": "没有白走的路，每一步都算数", "emoji": "👣", "tags": "励志,积累"},
        {"text": "所有的为时已晚，都是恰逢其时", "emoji": "⏰", "tags": "励志,时机"},
        {"text": "你的坚持，终将美好", "emoji": "🌈", "tags": "励志,美好"},
        {"text": "做自己的太阳，无需凭借谁的光", "emoji": "☀️", "tags": "励志,独立"},
        {"text": "比你优秀的人比你还努力", "emoji": "🏃", "tags": "励志,竞争"},
        {"text": "今天的努力，是明天的底气", "emoji": "📈", "tags": "励志,未来"},
    ],
    "life": [
        {"text": "生活需要仪式感", "emoji": "✨", "tags": "生活,仪式感"},
        {"text": "简单的小确幸就是最好的生活", "emoji": "🍀", "tags": "生活,小确幸"},
        {"text": "享受每一个当下", "emoji": "🎈", "tags": "生活,当下"},
        {"text": "生活不止眼前的苟且，还有诗和远方", "emoji": "📝", "tags": "生活,诗意"},
        {"text": "人间烟火气，最抚凡人心", "emoji": "🏮", "tags": "生活,烟火"},
        {"text": "慢下来，才能看到生活的美", "emoji": "🐌", "tags": "生活,慢生活"},
        {"text": "好的生活，从好的心态开始", "emoji": "😌", "tags": "生活,心态"},
        {"text": "生活中的小美好，值得被记录", "emoji": "📸", "tags": "生活,记录"},
        {"text": "柴米油盐，皆是生活", "emoji": "🍳", "tags": "生活,日常"},
        {"text": "好好生活，慢慢相遇", "emoji": "🤝", "tags": "生活,从容"},
    ],
    "work": [
        {"text": "工作使我快乐（不是）", "emoji": "😂", "tags": "工作,搞笑"},
        {"text": "又是努力搬砖的一天", "emoji": "🧱", "tags": "工作,搬砖"},
        {"text": "电脑前的第八个小时，灵魂已出走", "emoji": "💻", "tags": "工作,疲惫"},
        {"text": "努力工作，认真生活", "emoji": "⚖️", "tags": "工作,平衡"},
        {"text": "今天的工作效率满分", "emoji": "💯", "tags": "工作,效率"},
        {"text": "同事说今天奶茶我请，我选择加班", "emoji": "🧋", "tags": "工作,奶茶"},
        {"text": "deadline 是最好的生产力", "emoji": "⏳", "tags": "工作,deadline"},
        {"text": "摸鱼是一门艺术", "emoji": "🐟", "tags": "工作,摸鱼"},
    ],
    "reflection": [
        {"text": "有些路，只能一个人走", "emoji": "🚶", "tags": "感悟,独行"},
        {"text": "人总要学会和自己和解", "emoji": "🫂", "tags": "感悟,和解"},
        {"text": "长大就是慢慢学会闭嘴", "emoji": "🤐", "tags": "感悟,成长"},
        {"text": "时间教会我们的，是珍惜", "emoji": "⌛", "tags": "感悟,珍惜"},
        {"text": "所谓成熟，就是习惯任何人的忽冷忽热", "emoji": "🌡️", "tags": "感悟,成熟"},
        {"text": "生活不是电影，没有那么多的不期而遇", "emoji": "🎬", "tags": "感悟,现实"},
    ],
    "humor": [
        {"text": "今日状态：人还在，魂已飞", "emoji": "👻", "tags": "搞笑,状态"},
        {"text": "穷得很稳定，胖得很均匀", "emoji": "😅", "tags": "搞笑,自嘲"},
        {"text": "今天也是凭实力单身的一天", "emoji": "🤷", "tags": "搞笑,单身"},
        {"text": "我的钱包就像洋葱，打开就想哭", "emoji": "🧅", "tags": "搞笑,钱包"},
        {"text": "世界上最美的四个字：今天周五", "emoji": "🎉", "tags": "搞笑,周五"},
        {"text": "我的特长：能吃能睡能花钱", "emoji": "🛒", "tags": "搞笑,特长"},
        {"text": "健身卡办了三年，从没去过，就当积德了", "emoji": "🏋️", "tags": "搞笑,健身"},
    ],
}

CATEGORIES = list(TEMPLATES.keys())

# 节日文案
FESTIVALS = {
    "01-01": {"text": "新年快乐！愿新的一年万事胜意 🎆", "category": "festival", "emoji": "🎆"},
    "02-14": {"text": "情人节快乐，愿你被爱包围 💕", "category": "festival", "emoji": "💕"},
    "03-08": {"text": "女神节快乐，做自己的女王 👑", "category": "festival", "emoji": "👑"},
    "05-01": {"text": "劳动节快乐，致敬每一个奋斗的你 💪", "category": "festival", "emoji": "💪"},
    "06-01": {"text": "儿童节快乐，愿你童心未泯 🎈", "category": "festival", "emoji": "🎈"},
    "10-01": {"text": "国庆快乐，祝祖国繁荣昌盛 🇨🇳", "category": "festival", "emoji": "🇨🇳"},
    "12-25": {"text": "圣诞快乐，愿温暖与你同在 🎄", "category": "festival", "emoji": "🎄"},
}

# ============================================================
# 生成逻辑
# ============================================================


def get_time_category():
    """根据当前时间返回文案分类"""
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
    """检查今天是否为节日"""
    today = datetime.now().strftime("%m-%d")
    return FESTIVALS.get(today)


def generate_from_template(category=None, count=1):
    """
    从模板库生成文案

    Args:
        category: 分类，None 则按时间自动选择
        count: 生成数量

    Returns:
        list[dict]: 文案列表
    """
    results = []

    # 优先检查节日
    festival = check_festival()
    if festival:
        return [festival]

    for _ in range(count):
        # 每条文案可能来自不同分类
        cat = category
        if cat is None:
            time_cat = get_time_category()
            pool_names = ["motivation", "life", "work", "humor", "reflection"]
            if random.random() < 0.3:
                pool_names.append(time_cat)
            cat = random.choice(pool_names)

        if cat not in TEMPLATES:
            cat = random.choice(list(TEMPLATES.keys()))

        t = random.choice(TEMPLATES[cat])
        results.append(
            {"text": t["text"], "category": cat, "emoji": t["emoji"], "tags": t["tags"], "source": "template"}
        )

    return results


def generate_llm_prompt(category=None, style="normal"):
    """
    生成 LLM 文案生成提示词

    Args:
        category: 分类
        style: 风格（normal/humor/literary/short）

    Returns:
        str: 提示词
    """
    style_map = {
        "normal": "自然亲切，像日常分享",
        "humor": "幽默搞笑，带点自嘲",
        "literary": "文艺清新，带点哲理",
        "short": "简短有力，一句话金句",
    }

    cat_name = {
        "morning": "早安",
        "noon": "中午",
        "evening": "傍晚",
        "night": "晚安",
        "motivation": "励志",
        "life": "生活感悟",
        "work": "工作日常",
        "reflection": "人生感悟",
        "humor": "搞笑",
    }.get(category, "日常分享")

    prompt = (
        f"请生成一条中文朋友圈文案，主题是「{cat_name}」，风格：{style_map.get(style, '自然亲切')}。\n"
        "要求：\n"
        "- 长度15-50字\n"
        "- 口语化，接地气，不要像AI写的\n"
        "- 适合配图发朋友圈\n"
        "- 可以适当使用网络流行语\n"
        "- 只输出文案本身，不要任何解释或引号\n"
        "- 不带 # 标签"
    )
    return prompt


def generate_with_llm(client_func, category=None, style="normal", count=1):
    """
    使用 LLM 生成文案

    Args:
        client_func: LLM 调用函数，接受 prompt 参数，返回生成的文本
        category: 分类
        style: 风格
        count: 生成数量

    Returns:
        list[dict]: 文案列表
    """
    results = []
    for _ in range(count):
        prompt = generate_llm_prompt(category, style)
        try:
            text = client_func(prompt)
            text = text.strip().strip('"').strip("'").strip("「").strip("」")
            results.append(
                {
                    "text": text,
                    "category": category or "custom",
                    "emoji": "",
                    "tags": "",
                    "source": "llm",
                }
            )
        except Exception as e:
            print(f"LLM 生成失败: {e}，使用模板兜底")
            results.extend(generate_from_template(category, 1))
    return results


def generate_mixed(category=None, count=5, llm_ratio=0.3, llm_func=None):
    """
    混合生成：模板 + LLM

    Args:
        category: 分类
        count: 生成总数
        llm_ratio: LLM 文案占比
        llm_func: LLM 调用函数

    Returns:
        list[dict]: 文案列表
    """
    llm_count = int(count * llm_ratio)
    template_count = count - llm_count

    results = []
    results.extend(generate_from_template(category, template_count))

    if llm_count > 0 and llm_func:
        results.extend(generate_with_llm(llm_func, category, "normal", llm_count))
    elif llm_count > 0:
        # LLM 不可用时，全部用模板
        results.extend(generate_from_template(category, llm_count))

    random.shuffle(results)
    return results


def bulk_fill_db(add_func, target_count=50, llm_func=None):
    """
    批量填充数据库到目标数量

    Args:
        add_func: db_manager.add_content 或 add_contents_batch
        target_count: 目标文案总数
        llm_func: LLM 调用函数
    """
    categories = list(TEMPLATES.keys())
    batch = []

    for _ in range(target_count):
        cat = random.choice(categories)
        items = generate_from_template(cat, 1)
        batch.append(items[0])

    add_func(batch)
    print(f"已批量生成 {target_count} 条文案")

    if llm_func:
        llm_batch = []
        for _ in range(max(5, target_count // 5)):
            cat = random.choice(categories)
            items = generate_with_llm(llm_func, cat, "normal", 1)
            llm_batch.append(items[0])
        add_func(llm_batch)
        print(f"已额外生成 {len(llm_batch)} 条 LLM 文案")


def generate_via_siliconflow(category=None, topic="任意主题", style="normal"):
    """
    使用 SiliconFlow API 直接调用 LLM (如 DeepSeek) 自动生成文案
    """
    import sys
    from pathlib import Path
    scripts_path = str(Path(r"D:\weixin\wechat-moments-auto-v2\scripts"))
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    import config
    import requests
    
    api_key = config.SILICONFLOW_API_KEY
    if not api_key:
        raise ValueError("未在 d:/AIWork/.env 中找到 SILICONFLOW_API_KEY，无法使用 AI 自动生成朋友圈。")
        
    model = config.SILICONFLOW_MODEL
    
    # 麦肯锡信任公式文案结构
    mck_formulas = {
        "professional": ("专业型", "故事案例 + 细节 + 美好结果", "1. 第一段场景化描述问题或咨询案列 (20-25字)；2. 引入你提供的高质量细节和专业动作；3. 展示客户得到的美好转变，结尾引导认同互动。"),
        "reliable": ("靠谱型", "失败故事 + 不服输过程 + 成功结果", "1. 讲自己曾经真实的踩坑或失败经历；2. 讲克服困难、坚持原则和死磕的靠谱过程；3. 拿到好结果后的自我复盘与核心感悟。"),
        "warm": ("温暖型", "生活场景 + 真实互动 + 情感连接", "1. 引入极富生活气息的日常场景；2. 描述两三句温馨的真实生活细节/段子；3. 点题人与人之间的温暖连接或价值观。"),
        "altruistic": ("利他型", "事件 + 细节 + 解释 + 价值观/金句", "1. 讲一件最近学到、看到的高价值干货事件；2. 掰碎了说明其中的运作机制和使用逻辑；3. 提炼一句直击心灵的金句，利他分享。"),
        "counter": ("反认知破圈", "打破错误认知 + 植入你的全新理念", "1. 先抛出行业内习以为常的毒鸡汤或错误认知，果断打破；2. 摆事实讲道理，讲出背后的真实本质；3. 植入你的正确理念和操作心智。"),
        "target": ("圈用户", "筛选目标人群 + 制造稀缺感/门槛", "1. 点名某几类有特定痛点的人群；2. 讲清这是一次只有少数名额的特别通道/测试服务；3. 建立加入门槛，发出明确行动指令 (如: 评论区扣1)。"),
        "intro_100": ("100字自我介绍", "深耕[领域][时间] + 踩坑经历 + 价值钩子", "1. 第一句简述你在某垂直领域做到了什么成就；2. 抛出自己踩过的几个关键大坑来拉近距离；3. 给出一个无懈可击的利他价值钩子，等待互动。")
    }
    
    prompt = ""
    if category in mck_formulas:
        name, formula, outline = mck_formulas[category]
        prompt = (
            f"请帮我撰写一条适合配图发布的朋友圈文案，主题是「{topic}」。\n"
            f"要求遵循【麦肯锡信任公式 - {name}】撰写：\n"
            f"- 核心公式：{formula}\n"
            f"- 结构设计：{outline}\n\n"
            f"【排版要求】\n"
            f"1. 第一段20-25字以内，场景化切入，吸引眼球。\n"
            f"2. 每段文字不超过3行，段与段之间空一行。\n"
            f"3. 结尾提炼一句金句或引导互动（认同类/好奇类/行动类）。\n\n"
            f"【语言风格】\n"
            f"- 完全口语化，像真人日常分享，拒绝过度包装和公关套话。\n"
            f"- 不要带任何 # 标签。\n"
            f"- 可以适当搭配 Emoji，但每段不超过 2 个。\n\n"
            f"请直接输出朋友圈文案内容本身，不要任何前缀解释或引号。"
        )
    else:
        prompt = generate_llm_prompt(category, style)
        if topic and topic != "任意主题":
            prompt += f"\n文案主题：{topic}"
            
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 800
    }
    
    url = "https://api.siliconflow.cn/v1/chat/completions"
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    if response.status_code != 200:
        raise ValueError(f"SiliconFlow API 错误 (HTTP {response.status_code}): {response.text}")
        
    res_json = response.json()
    text = res_json["choices"][0]["message"]["content"]
    text = text.strip().strip('"').strip("'").strip("「").strip("」")
    
    return {
        "text": text,
        "category": category or "custom",
        "emoji": "",
        "tags": "siliconflow,llm",
        "source": "llm"
    }


if __name__ == "__main__":
    # 测试
    items = generate_from_template(count=3)
    for item in items:
        print(f"[{item['category']}] {item['emoji']} {item['text']}")
    print(f"\nLLM Prompt 示例:\n{generate_llm_prompt('life', 'humor')}")
