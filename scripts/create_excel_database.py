#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建Excel表格作为本地内容数据库
"""

import pandas as pd
from datetime import datetime
import os

def create_content_database():
    """创建内容数据库Excel文件"""
    
    # 定义Excel表格结构
    data = {
        "ID": [1, 2, 3, 4, 5],
        "博主": ["路飞", "大元", "全哥", "路飞", "大元"],
        "内容": [
            "今天分享一个关于珠宝的思考，真正的价值不在于价格，而是情感连接。",
            "遇见美好，从心开始。每一天都是新的起点。",
            "创业路上，坚持是最重要的品质。不要轻易放弃！",
            "学习易经让我明白了生活的平衡之道。",
            "简单的快乐，才是生活的真谛。"
        ],
        "图片路径": [
            "images/路飞.png",
            "images/大元.png", 
            "images/全哥.png",
            "images/路飞.png",
            "images/大元.png"
        ],
        "状态": ["未发布", "未发布", "未发布", "未发布", "未发布"],
        "创建时间": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "发布时间": ["", "", "", "", ""],
        "备注": ["", "", "", "", ""]
    }
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存到Excel
    excel_path = os.path.join(os.path.dirname(__file__), "..", "content_database.xlsx")
    df.to_excel(excel_path, index=False)
    
    print(f"Excel表格已创建成功：{excel_path}")
    print("表格包含以下字段：")
    print("- ID: 唯一标识")
    print("- 博主: 博主名称（路飞、大元、全哥等）")
    print("- 内容: 朋友圈文案内容")
    print("- 图片路径: 对应博主图片路径")
    print("- 状态: 未发布/已发布")
    print("- 创建时间: 内容创建时间")
    print("- 发布时间: 实际发布时间")
    print("- 备注: 备注信息")
    
    print("\n使用方法：")
    print("1. 使用Excel或Python批量添加内容")
    print("2. 运行本地发送脚本时会读取状态为'未发布'的内容")
    print("3. 发送成功后状态自动更新为'已发布'，并记录发布时间")
    
    return excel_path

if __name__ == "__main__":
    create_content_database()