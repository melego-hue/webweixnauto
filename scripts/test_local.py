#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试本地Excel版本功能
"""

import pandas as pd
from pathlib import Path

def test_excel_database():
    """测试Excel数据库"""
    
    excel_path = Path(__file__).parent.parent / "content_database.xlsx"
    
    print(f"\n=== Excel数据库测试 ===")
    print(f"Excel文件路径: {excel_path}")
    
    try:
        df = pd.read_excel(excel_path)
        print(f"读取成功，共有 {len(df)} 条记录")
        
        print("\n字段检查:")
        for column in df.columns:
            print(f"  {column}: {df[column].dtype}")
        
        print("\n数据预览:")
        print(df.head())
        
        print("\n状态统计:")
        status_counts = df["状态"].value_counts()
        for status, count in status_counts.items():
            print(f"  {status}: {count} 条")
        
        print("\n博主统计:")
        blogger_counts = df["博主"].value_counts()
        for blogger, count in blogger_counts.items():
            print(f"  {blogger}: {count} 条")
        
        return True
        
    except Exception as e:
        print(f"读取Excel失败: {e}")
        return False

def test_image_paths():
    """测试图片路径"""
    
    images_dir = Path(__file__).parent.parent / "images"
    
    print(f"\n=== 图片路径测试 ===")
    print(f"图片目录: {images_dir}")
    
    bloggers = ["路飞", "大元", "全哥", "李真"]
    
    for blogger in bloggers:
        image_path = images_dir / f"{blogger}.png"
        if image_path.exists():
            print(f"  {blogger}: ✓ 图片存在 ({image_path.name})")
        else:
            print(f"  {blogger}: ✗ 图片不存在")
    
    return True

def test_send_from_local():
    """测试本地发送功能"""
    
    print(f"\n=== 本地发送功能测试 ===")
    
    try:
        from send_from_local import fetch_local_content
        
        item = fetch_local_content()
        if item:
            print(f"读取到内容:")
            print(f"  ID: {item['id']}")
            print(f"  博主: {item['blogger_name']}")
            print(f"  图片: {item['image_path']}")
            print(f"  内容: {item['content'][:50]}...")
            print(f"  状态: {item['status']}")
            return True
        else:
            print("没有找到可发布的内容")
            return False
            
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def test_bulk_generator():
    """测试批量生成功能"""
    
    print(f"\n=== 批量生成功能测试 ===")
    
    try:
        from generate_bulk_content import generate_content_for_blogger
        
        bloggers = ["路飞", "大元", "全哥", "李真"]
        
        for blogger in bloggers:
            content = generate_content_for_blogger(blogger)
            print(f"  {blogger}: {content[:30]}...")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def main():
    """主测试函数"""
    
    print("=" * 50)
    print("本地Excel版本功能测试")
    print("=" * 50)
    
    tests = [
        ("Excel数据库", test_excel_database),
        ("图片路径", test_image_paths),
        ("本地发送", test_send_from_local),
        ("批量生成", test_bulk_generator),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n测试: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    
    passed_count = 0
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed_count += 1
    
    print(f"\n总共 {len(results)} 项测试，{passed_count} 项通过")
    
    if passed_count == len(results):
        print("\n🎉 所有测试通过，本地版本功能正常！")
    else:
        print("\n⚠️ 部分测试失败，请检查配置")

if __name__ == "__main__":
    main()