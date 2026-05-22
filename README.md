# WeChat Moments Auto Sender

微信朋友圈自动化发送工具 - 从 Notion 数据库自动读取内容并发送到朋友圈

## 功能特点

- ✅ 自动从 Notion 数据库读取待发布内容
- ✅ 根据博主关键词自动匹配图片
- ✅ 只发送有对应图片的内容，无图片自动跳过
- ✅ 发送成功后自动更新 Notion 状态
- ✅ 图像识别定位微信界面元素
- ✅ 增强的微信窗口检测和激活
- ✅ 支持模拟运行模式（dry-run）

## 目录结构

```
wechat-moments-auto/
├── images/                 # 博主图片目录
│   ├── 路飞.png           # 路飞博主头像
│   ├── 大元.png          # 大元博主头像
│   └── 全哥.png          # 全哥博主头像
├── ui_images/             # 界面元素截图（图像识别用）
│   ├── moments_icon.png   # 朋友圈图标
│   ├── camera_btn.png     # 相机按钮
│   └── publish_btn.png    # 发表按钮
└── scripts/               # Python 脚本
    ├── run.py             # 统一入口脚本
    ├── send_from_notion.py # Notion 集成核心模块
    ├── send_by_image.py    # 图像识别发送模块
    ├── wechat_utils.py     # 微信窗口管理工具
    ├── generate_content.py  # 内容生成器
    ├── capture_ui.py        # 界面截图工具
    └── config.py            # 配置文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests pyautogui Pillow opencv-python
```

### 2. 配置博主图片

将博主的头像图片放入 `images/` 目录，文件名对应博主名称：
- `路飞.png`
- `大元.png`
- `全哥.png`
- （可添加其他博主）

### 3. 配置 Notion

确保 Notion 数据库包含以下字段：
- `平台/状态` (status)：状态选项包含"未开始"、"完成"
- `AI朋友圈金句` (rich_text)：朋友圈文案内容
- `名称` (title)：标题（包含博主关键词用于识别）

### 4. 运行发送

```bash
# 从 Notion 自动获取并发送
python run.py notion

# 模拟运行（不实际发送）
python run.py notion --dry-run

# 手动发送指定内容
python run.py send --text "朋友圈内容"

# 测试微信窗口检测
python run.py test

# 生成朋友圈文案
python run.py generate

# 截取界面元素
python run.py capture
```

## 使用说明

### 发送流程

1. **读取 Notion**：从"路飞全自动发稿池V2.5"数据库读取"未开始"状态的内容
2. **博主识别**：根据标题中的关键词识别博主（路飞、大元、全哥等）
3. **图片匹配**：查找对应的博主图片，无图片则跳过
4. **发送朋友圈**：通过图像识别定位微信界面元素，自动发送
5. **状态更新**：发送成功后自动将 Notion 状态改为"完成"

### 博主关键词配置

在 `send_from_notion.py` 中修改 `BLOGGER_KEYWORDS`：

```python
BLOGGER_KEYWORDS = {
    "Luffy": ["不卖珠宝的路飞", "自己学易的路飞", "路飞"],
    "Dayuan": ["遇见大元", "大元"],
    "Quange": ["全哥"],
}
```

### 图片路径配置

在 `send_from_notion.py` 中修改图片目录：

```python
images_dir = Path("D:/weixin/wechat-moments-auto/images")
```

## 命令行参数

### notion 命令

```bash
python run.py notion [选项]

选项:
  --dry-run              模拟运行，不实际发送
  --no-update            不更新 Notion 状态
  --min-delay N          最小延迟（分钟），默认5
  --max-delay N          最大延迟（分钟），默认15
```

### send 命令

```bash
python run.py send --text "内容" [--image "图片路径"]

选项:
  --text TEXT            朋友圈文案
  --image PATH           图片路径（可选）
  --dry-run              模拟运行
```

### 其他命令

```bash
python run.py test        # 测试微信窗口检测
python run.py generate    # 生成朋友圈文案
python run.py capture    # 截取界面元素
python run.py help       # 显示帮助信息
```

## 配置说明

### Notion API Token

在 `send_from_notion.py` 中修改：

```python
def get_notion_token():
    return ""  # 请填写你的Notion API Token（留空表示不使用Notion版本）
```

### 数据库 ID

在 `send_from_notion.py` 中修改：

```python
DATABASE_ID = ""  # 请填写你的Notion数据库ID（留空表示不使用Notion版本）
```

**注意：** 如果你使用本地Excel版本，这些ID可以留空，无需配置。

## 本地Excel版本

### Q: 提示"Skip: No image for blogger"
**A**: 当前博主没有对应的图片，请将博主头像放入 `images/` 目录

### Q: 图像识别失败
**A**: 确保 `ui_images/` 目录中的截图与当前微信界面一致，必要时重新截图

### Q: 微信窗口激活失败
**A**: 检查微信是否正常运行，尝试重新启动微信

## 更新日志

### v2.5 (2026-05-18)
- ✅ 支持从"路飞全自动发稿池V2.5"数据库读取内容
- ✅ 实现无图片自动跳过逻辑
- ✅ 增强微信窗口检测（多种激活策略）
- ✅ 添加图像识别重试机制
- ✅ 统一入口脚本 `run.py`

### v2.0 (2026-05-17)
- ✅ 基础自动化发送功能
- ✅ Notion 集成
- ✅ 博主识别和图片匹配
## 本地Excel版本

除了云端Notion版本，我们还提供了本地Excel版本，无需网络连接，完全本地运行。

### 本地版本特点

- ✅ **完全本地化**：使用Excel表格替代Notion数据库
- ✅ **批量内容生成**：支持生成上百条内容，类似多维表格
- ✅ **自动标注状态**：发送后自动标记为"已发布"
- ✅ **无需API**：无需Notion API Token

### 本地版本使用

```bash
# 进入本地版本脚本目录
cd scripts

# 生成Excel数据库（100条内容）
python generate_bulk_content.py --num 100

# 运行本地Excel版本
python run_local.py local

# 模拟运行
python run_local.py local --dry-run

# 指定延迟发送
python run_local.py local --min-delay 5 --max-delay 15
```

### 本地版本文件结构

```
wechat-moments-auto/
├── content_database.xlsx     # Excel内容数据库
├── README_local.md           # 本地版本完整文档
├── LOCAL_GUIDE.md            # 本地版本使用指南
├── images/                   # 博主图片目录
│   ├── 路飞.png             # 路飞博主头像
│   ├── 大元.png             # 大元博主头像
│   └── 全哥.png             # 全哥博主头像
├── scripts/                  # Python脚本
│   ├── run_local.py          # 本地版本入口脚本
│   ├── send_from_local.py    # 本地Excel发送核心模块
│   ├── generate_bulk_content.py # 批量内容生成脚本
│   └── test_local.py          # 本地版本测试脚本
```

### Excel数据库字段

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

### 批量内容生成

```bash
# 生成200条内容
python generate_bulk_content.py --num 200

# 添加到现有Excel
python generate_bulk_content.py --add --num 50

# 添加单个自定义内容
python generate_bulk_content.py --add --blogger "路飞" --content "自定义内容"
```

### 优势对比

| 功能 | Notion版本 | Excel本地版本 |
|------|------------|---------------|
| **依赖** | 需要Notion API | 无需网络连接 |
| **速度** | 网络请求延迟 | 本地读取，速度快 |
| **成本** | Notion付费版本 | 免费 |
| **扩展性** | 数据库限制 | Excel无限扩展 |
| **批量生成** | 手动添加 | 脚本批量生成 |
| **维护** | 云端维护 | 本地维护 |

## 技术支持

如遇到问题，请检查：
1. README_local.md 完整文档
2. LOCAL_GUIDE.md 使用指南
3. Excel数据库是否正确配置
4. 微信窗口状态
5. 博主图片是否存在