# 部署指南 - 本地Excel版本

## 完整部署步骤

### 第一步：环境准备

```bash
# 1. 安装Python 3.7+
python --version

# 2. 安装依赖包
pip install pandas openpyxl requests pyautogui Pillow opencv-python

# 3. 验证安装
pip list | grep -E "pandas|openpyxl|requests|pyautogui|Pillow|opencv"
```

### 第二步：文件夹结构准备

1. **创建目录结构**
   ```
   wechat-moments-auto/
   ├── images/
   ├── scripts/
   ├── ui_images/
   ├── random-images/
   ```

2. **准备博主图片**
   - 将博主头像图片放入 `images/` 目录
   - 文件名格式：`博主名称.png`
   - 图片大小建议：200x200像素以上

3. **准备界面截图**
   - 运行截图工具：`python run.py capture`
   - 截图保存到 `ui_images/` 目录

### 第三步：Excel数据库初始化

```bash
# 生成初始Excel数据库（100条内容）
python generate_bulk_content.py --num 100

# 查看Excel文件
open content_database.xlsx

# 验证Excel内容
python test_local.py
```

### 第四步：微信配置

1. **启动微信**：确保微信已启动并登录
2. **窗口位置**：确保微信窗口可见
3. **快捷键测试**：测试 `Ctrl+Alt+W` 快捷键是否正常

### 第五步：测试运行

```bash
# 测试微信窗口检测
python run_local.py test

# 模拟发送测试
python run_local.py local --dry-run

# 实际发送测试
python run_local.py local
```

## 批量内容生成

### 生成大量内容

```bash
# 生成500条内容
python generate_bulk_content.py --num 500

# 添加到现有Excel（100条）
python generate_bulk_content.py --add --num 100

# 添加单个自定义内容
python generate_bulk_content.py --add --blogger "路飞" --content "自定义朋友圈内容"
```

### Excel编辑建议

1. **内容分类**：可以根据博主分类内容
2. **时间安排**：可以设置不同的发布时间
3. **优先级管理**：可以添加优先级字段
4. **内容质量**：定期筛选和优化内容

## 定时任务配置

### Windows任务计划程序

1. 打开"任务计划程序"
2. 点击"创建基本任务"
3. 设置任务名称：`微信朋友圈自动发送`
4. 设置触发时间：每天9:00
5. 设置操作：启动程序
6. 程序路径：`python.exe`
7. 参数：`run_local.py local`
8. 起始位置：`D:\工作流方法\wechat-moments-auto\scripts`
9. 完成创建

### 定时任务优化

1. **多时段发送**：可以设置多个触发时间
   - 上午9:00
   - 中午12:00
   - 下午18:00

2. **随机延迟**：使用脚本内置的随机延迟
   ```bash
   python run_local.py local --min-delay 5 --max-delay 15
   ```

3. **内容筛选**：可以修改脚本，只发送特定博主的内容

## 监控和维护

### 监控Excel状态

```bash
# 查看Excel统计信息
python -c "
import pandas as pd
df = pd.read_excel('content_database.xlsx')
print('总记录数:', len(df))
print('未发布:', df[df['状态']=='未发布'].shape[0])
print('已发布:', df[df['状态']=='已发布'].shape[0])
"

# 查看最近发布时间
python -c "
import pandas as pd
df = pd.read_excel('content_database.xlsx')
published = df[df['状态']=='已发布']
if len(published) > 0:
    print('最近发布时间:', published['发布时间'].max())
"
```

### 定期维护

1. **备份Excel**：每周备份一次Excel文件
2. **清理图片**：定期清理无用的图片
3. **更新截图**：微信更新后重新截图
4. **检查依赖**：定期更新Python包

## 故障排查

### Excel读取失败

```bash
# 检查Excel文件是否存在
ls content_database.xlsx

# 检查文件权限
python -c "import os; print(os.access('content_database.xlsx', os.R_OK))"
python -c "import os; print(os.access('content_database.xlsx', os.W_OK))"
```

### 图片匹配失败

```bash
# 检查图片文件
ls images/

# 检查图片路径
python -c "
from pathlib import Path
images_dir = Path('images')
for blogger in ['路飞', '大元', '全哥', '李真']:
    for ext in ['png', 'jpg', 'jpeg']:
        path = images_dir / f'{blogger}.{ext}'
        print(f'{blogger}.{ext}: {path.exists()}')
"
```

### 微信发送失败

```bash
# 测试微信窗口
python run_local.py test

# 重新截图
python run.py capture
```

## 扩展功能

### 添加新博主

1. **准备图片**：将新博主头像放入 `images/` 目录
2. **修改脚本**：更新 `send_from_local.py` 中的博主关键词映射
3. **生成内容**：使用 `generate_bulk_content.py` 生成新博主内容

### 自定义内容模板

修改 `generate_bulk_content.py` 中的内容生成函数：

```python
def generate_content_for_blogger(blogger_name):
    # 自定义不同博主的内容风格
    if blogger_name == "路飞":
        templates = ["珠宝相关内容", "易经相关内容"]
    elif blogger_name == "大元":
        templates = ["心灵相关内容", "情感相关内容"]
    elif blogger_name == "全哥":
        templates = ["创业相关内容", "商业相关内容"]
    elif blogger_name == "李真":
        templates = ["艺术相关内容", "美学相关内容"]
```

### Excel字段扩展

可以添加更多字段到Excel：

```python
# 添加分类字段
df["分类"] = "生活感悟"

# 添加优先级字段
df["优先级"] = 1

# 添加发送次数字段
df["发送次数"] = 0
```

## 性能优化

### 批量处理优化

```bash
# 批量生成内容时分批处理
python generate_bulk_content.py --num 1000

# 分批发送内容
python run_local.py local --content-id 1
python run_local.py local --content-id 2
python run_local.py local --content-id 3
```

### 缓存优化

```python
# 图片路径缓存
image_cache = {}
def get_blogger_image_cached(blogger):
    if blogger in image_cache:
        return image_cache[blogger]
    # ... 查找图片
    image_cache[blogger] = image_path
    return image_path
```

## 总结

本地Excel版本提供了：
1. **完全本地化**：无需网络连接
2. **批量管理**：支持生成上百条内容
3. **自动化标注**：发送后自动标记状态
4. **灵活扩展**：可以随时添加新功能
5. **定时任务**：支持Windows任务计划程序

部署完成后，系统可以自动运行，无需人工干预。