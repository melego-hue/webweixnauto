# WeChat Moments Auto Sender - 本地Excel版本

微信朋友圈自动化发送工具 - 本地Excel版本，无需Notion云端依赖

## 功能特点

- ✅ **本地Excel数据库**：使用Excel表格替代Notion数据库
- ✅ **批量内容生成**：支持通过脚本批量生成上百条内容
- ✅ **自动图片匹配**：根据博主名称自动匹配对应图片
- ✅ **状态自动更新**：发送成功后自动标记为"已发布"
- ✅ **延迟发送**：支持随机延迟发送，避免频繁发送
- ✅ **模拟测试**：支持dry-run模式进行测试

## 目录结构

```
wechat-moments-auto/
├── content_database.xlsx     # Excel内容数据库
├── images/                   # 博主图片目录
│   ├── 路飞.png             # 路飞博主头像
│   ├── 大元.png             # 大元博主头像
│   └── 全哥.png             # 全哥博主头像
├── ui_images/                # 界面元素截图（图像识别用）
│   ├── moments_icon.png      # 朋友圈图标
│   ├── camera_btn.png        # 相机按钮
│   └── publish_btn.png       # 发表按钮
├── scripts/                  # Python脚本
│   ├── run_local.py          # 本地版本入口脚本
│   ├── send_from_local.py    # 本地Excel发送核心模块
│   ├── send_by_image.py      # 图像识别发送模块
│   ├── generate_bulk_content.py # 批量内容生成脚本
│   ├── wechat_utils.py      # 微信窗口管理工具
│   └── config.py             # 配置文件
```

## Excel数据库结构

Excel表格包含以下字段：

| 字段 | 说明 |
|------|------|
| ID | 唯一标识符 |
| 博主 | 博主名称（路飞、大元、全哥、李真等） |
| 内容 | 朋友圈文案内容 |
| 图片路径 | 对应博主图片路径 |
| 状态 | 未发布/已发布 |
| 创建时间 | 内容创建时间 |
| 发布时间 | 实际发布时间 |
| 备注 | 备注信息 |

## 快速开始

### 1. 安装依赖

```bash
pip install pandas openpyxl requests pyautogui Pillow opencv-python
```

### 2. 准备博主图片

将博主的头像图片放入 `images/` 目录：
- `路飞.png` - 路飞博主
- `大元.png` - 大元博主  
- `全哥.png` - 全哥博主
- `李真.png` - 李真博主（可选）

### 3. 批量生成内容

```bash
# 生成100条内容
python generate_bulk_content.py --num 100

# 添加单个内容
python generate_bulk_content.py --add --blogger "路飞" --content "新的朋友圈内容"
```

### 4. 测试运行

```bash
# 进入脚本目录
cd scripts

# 测试微信窗口检测
python run_local.py test

# 模拟发送测试
python run_local.py local --dry-run
```

### 5. 正式发送

```bash
# 实际发送（会更新Excel状态）
python run_local.py local

# 延迟发送（5-15分钟随机延迟）
python run_local.py local --min-delay 5 --max-delay 15

# 指定ID发送
python run_local.py local --content-id 10
```

## 使用流程

### 日常使用流程

1. **准备内容**：
   - 使用Excel编辑内容
   - 或使用批量生成脚本
   - 确保"状态"字段为"未发布"

2. **准备图片**：
   - 确保博主对应的图片存在
   - 图片路径填写正确

3. **运行发送**：
   ```bash
   python run_local.py local
   ```

4. **查看结果**：
   - 检查朋友圈是否发送成功
   - Excel状态自动更新为"已发布"
   - 发布时间自动记录

### 批量生成流程

```bash
# 1. 生成初始内容库
python generate_bulk_content.py --num 200

# 2. 检查Excel文件
open content_database.xlsx

# 3. 根据需要手动编辑Excel
# 4. 运行发送
python run_local.py local

# 5. 定期添加新内容
python generate_bulk_content.py --add --num 50
```

## Excel操作指南

### 手动编辑Excel

1. **添加新内容**：
   - 在Excel中添加新行
   - 填写博主、内容、图片路径
   - 状态设为"未发布"

2. **修改内容**：
   - 直接修改Excel单元格
   - 保存文件

3. **状态管理**：
   - "未发布": 待发送
   - "已发布": 已发送成功
   - 发布时间自动记录

### 使用Python编辑

```python
import pandas as pd

# 读取Excel
df = pd.read_excel("content_database.xlsx")

# 添加新内容
new_row = {
    "ID": len(df) + 1,
    "博主": "路飞",
    "内容": "新的朋友圈内容",
    "图片路径": "images/路飞.png",
    "状态": "未发布",
    "创建时间": "2026-05-18 10:00:00",
    "发布时间": "",
    "备注": ""
}
df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# 保存Excel
df.to_excel("content_database.xlsx", index=False)
```

## 命令行参数

### local 命令

```bash
python run_local.py local [选项]

选项:
  --dry-run              模拟运行，不实际发送
  --no-update            不更新Excel状态
  --min-delay N          最小延迟（分钟），默认5
  --max-delay N          最大延迟（分钟），默认15
  --content-id N         指定ID发送（不随机选择）
```

### generate_bulk_content.py 命令

```bash
python generate_bulk_content.py [选项]

选项:
  --num N                生成数量，默认100
  --add                  添加到现有Excel
  --blogger NAME        指定博主名称
  --content TEXT        指定内容
  --image PATH          指定图片路径
```

## 常见问题

### Q: Excel文件找不到
**A**: 确保Excel文件在项目根目录，命名为 `content_database.xlsx`

### Q: 图片找不到
**A**: 确保博主图片在 `images/` 目录中，文件名与博主名称匹配

### Q: 状态更新失败
**A**: 检查Excel文件是否被其他程序打开，确保Python可以写入

### Q: 内容发送失败
**A**: 检查微信是否正常运行，尝试重新启动微信

## 自动化定时任务

可以使用Windows任务计划程序设置定时发送：

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发时间（如每天9:00）
4. 设置操作：启动程序 `python.exe`
5. 参数：`run_local.py local`
6. 起始位置：`D:\weixin\wechat-moments-auto\scripts`

## 优势对比

| 功能 | Notion版本 | Excel本地版本 |
|------|------------|---------------|
| **依赖** | 需要Notion API | 无需网络连接 |
| **速度** | 网络请求延迟 | 本地读取，速度快 |
| **成本** | Notion付费版本 | 免费 |
| **扩展性** | 数据库限制 | Excel无限扩展 |
| **批量生成** | 手动添加 | 脚本批量生成 |
| **维护** | 云端维护 | 本地维护 |

## 版本信息

**版本**: v3.0（本地Excel版本）
**更新时间**: 2026-05-18
**状态**: 正式可用