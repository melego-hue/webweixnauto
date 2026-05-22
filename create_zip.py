#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信朋友圈自动化工作流打包脚本
将整个项目打包成压缩包
"""

import os
import zipfile
import datetime

def create_zip():
    """创建项目压缩包"""
    project_dir = "D:/工作流方法/wechat-moments-auto"
    zip_filename = f"wechat-moments-auto-{datetime.datetime.now().strftime('%Y%m%d')}.zip"
    zip_path = os.path.join(project_dir, zip_filename)
    
    print(f"正在打包项目到: {zip_path}")
    
    # 创建zip文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加所有文件
        for root, dirs, files in os.walk(project_dir):
            # 跳过__pycache__目录
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                file_path = os.path.join(root, file)
                # 跳过zip文件本身
                if file_path == zip_path:
                    continue
                
                # 计算相对路径
                arcname = os.path.relpath(file_path, project_dir)
                zipf.write(file_path, arcname)
                print(f"  ✓ {arcname}")
    
    print(f"\n打包完成!")
    print(f"压缩包大小: {os.path.getsize(zip_path)} bytes")
    print(f"文件路径: {zip_path}")
    return zip_path

if __name__ == "__main__":
    zip_path = create_zip()