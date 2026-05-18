#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量内容生成脚本 - 通过大模型生成大量朋友圈内容并导入Excel
"""

import pandas as pd
import random
from datetime import datetime
from pathlib import Path

def generate_content_for_blogger(blogger_name):
    """根据博主名称生成内容"""
    
    # 不同博主的主题模板
    blogger_themes = {
        "路飞": ["珠宝", "易经", "创业", "学习", "人生感悟"],
        "大元": ["美好", "心灵", "生活", "情感", "正能量"],
        "全哥": ["创业", "坚持", "成功", "商业", "机遇"],
        "李真": ["艺术", "创作", "灵感", "美学", "品味"]
    }
    
    themes = blogger_themes.get(blogger_name, ["生活", "感悟", "分享"])
    
    # 内容模板
    templates = [
        f"今天分享一个关于{random.choice(themes)}的思考，真正的价值不在于表面，而是内在的品质。",
        f"遇见{random.choice(themes)}，从心开始。每一天都是新的起点。",
        f"{random.choice(themes)}的路上，坚持是最重要的品质。不要轻易放弃！",
        f"学习{random.choice(themes)}让我明白了生活的平衡之道。",
        f"简单的{random.choice(themes)}，才是生活的真谛。",
        f"分享一个关于{random.choice(themes)}的小故事，希望能给大家带来启发。",
        f"最近一直在思考{random.choice(themes)}的意义，有些感悟想和大家分享。",
        f"{random.choice(themes)}不仅仅是表面的东西，更重要的是内心的感受。",
        f"今天遇到一件关于{random.choice(themes)}的有趣事情，和大家分享一下。",
        f"{random.choice(themes)}的魅力在于它的多样性和包容性。"
    ]
    
    return random.choice(templates)

def generate_bulk_content(num_items=100):
    """批量生成内容"""
    
    print(f"开始生成 {num_items} 条朋友圈内容...")
    
    bloggers = ["路飞", "大元", "全哥", "李真"]
    data = []
    
    for i in range(1, num_items + 1):
        blogger = random.choice(bloggers)
        content = generate_content_for_blogger(blogger)
        
        # 确定图片路径
        if blogger == "路飞":
            image_path = "images/路飞.png"
        elif blogger == "大元":
            image_path = "images/大元.png"
        elif blogger == "全哥":
            image_path = "images/全哥.png"
        elif blogger == "李真":
            image_path = "images/李真.png"
        else:
            image_path = ""
        
        item = {
            "ID": i,
            "博主": blogger,
            "内容": content,
            "图片路径": image_path,
            "状态": "未发布",
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "发布时间": "",
            "备注": ""
        }
        
        data.append(item)
        
        print(f"生成第 {i} 条: {blogger} - {content[:30]}...")
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存到Excel
    excel_path = Path(__file__).parent.parent / "content_database.xlsx"
    df.to_excel(excel_path, index=False)
    
    print(f"\n批量生成完成！")
    print(f"共生成 {num_items} 条内容")
    print(f"Excel文件已保存到: {excel_path}")
    
    # 统计信息
    print("\n统计信息:")
    for blogger in bloggers:
        count = df[df["博主"] == blogger].shape[0]
        print(f"  {blogger}: {count} 条")
    
    return excel_path

def add_content_to_excel(content_data):
    """将内容添加到Excel数据库"""
    
    excel_path = Path(__file__).parent.parent / "content_database.xlsx"
    
    # 读取现有Excel
    try:
        df = pd.read_excel(excel_path)
    except:
        # 如果文件不存在，创建新的
        df = pd.DataFrame(columns=["ID", "博主", "内容", "图片路径", "状态", "创建时间", "发布时间", "备注"])
    
    # 添加新内容
    for item in content_data:
        # 生成新的ID
        new_id = df["ID"].max() + 1 if len(df) > 0 else 1
        
        new_row = {
            "ID": new_id,
            "博主": item["博主"],
            "内容": item["内容"],
            "图片路径": item.get("图片路径", ""),
            "状态": "未发布",
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "发布时间": "",
            "备注": item.get("备注", "")
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # 保存Excel
    df.to_excel(excel_path, index=False)
    
    print(f"添加了 {len(content_data)} 条新内容到 Excel")
    print(f"Excel文件已更新: {excel_path}")
    
    return excel_path

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="批量生成朋友圈内容")
    parser.add_argument("--num", type=int, default=100, help="生成数量")
    parser.add_argument("--add", action="store_true", help="添加到现有Excel")
    parser.add_argument("--blogger", help="指定博主名称")
    parser.add_argument("--content", help="指定内容")
    parser.add_argument("--image", help="指定图片路径")
    
    args = parser.parse_args()
    
    if args.add and (args.blogger or args.content):
        # 添加单个内容
        content_data = [{
            "博主": args.blogger or "路飞",
            "内容": args.content or generate_content_for_blogger(args.blogger or "路飞"),
            "图片路径": args.image or "",
            "备注": ""
        }]
        
        add_content_to_excel(content_data)
    elif args.add:
        # 添加批量内容
        generate_bulk_content(args.num)
    else:
        # 生成全新Excel
        generate_bulk_content(args.num)

if __name__ == "__main__":
    main()