# 微信朋友圈自动发送 Agent

## 简介

这是一个自动从 Notion 读取内容并发送到微信朋友圈的自动化工具。通过图像识别技术定位微信界面元素，实现稳定的自动化发送。

## 功能特点

- **Notion 集成**：自动从 Notion 数据库读取待发布内容
- **博主识别**：根据名称自动识别博主，选择对应图片
- **图像识别**：通过截图识别界面元素，重启后无需重新配置
- **状态更新**：发送成功后自动更新 Notion 状态为"已发布"
- **定时任务**：支持配置定时自动发送

## 目录结构

```
wechat-moments-auto/
├── SKILL.md                    # 技能说明文件
├── CONFIG.md                   # 配置指南
├── README.md                   # 本操作手册
├── .env.example                # 环境变量示例
└── scripts/
    ├── main.py                 # 主入口（手动发送）
    ├── send_from_notion.py     # 从 Notion 读取并发送
    ├── send_by_image.py        # 图像识别发送核心
    ├── generate_content.py     # 内容生成器
    ├── generate_image.py       # 极简图片生成器
    ├── generate_moments_image.py # 商业风格图片生成器
    ├── capture_ui.py           # 界面截图工具
    ├── debug_coords.py         # 坐标调试工具
    ├── debug_visual.py         # 可视化调试工具
    ├── ui_images/              # 界面元素截图
    │   ├── moments_icon.png    # 朋友圈入口图标
    │   ├── camera_btn.png      # 相机按钮
    │   └── publish_btn.png     # 发表按钮
    ├── images/                 # 博主图片（用户配置）
    │   └── 博主A.png           # 示例：博主图片
    └── generated_images/       # 生成的图片（自动创建）
```

## 使用方法

### 1. 从 Notion 自动发送

```bash
python send_from_notion.py
```

### 2. 手动发送指定内容

```bash
python main.py --text "朋友圈内容"
```

### 3. 模拟运行（不实际发送）

```bash
python send_from_notion.py --dry-run
```

## Notion 配置

### 数据库字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 名称 | 标题 | 条目名称，需包含博主关键词 |
| 原始文稿 | 文本 | 原始内容 |
| AI小红书洗稿 | 文本 | 小红书风格文案（发送用） |
| AI朋友圈金句 | 文本 | 朋友圈金句 |
| 短视频脚本 | 文本 | 短视频脚本 |
| 平台/状态 | 状态 | 未开始/进行中/已发布 |

### 博主识别规则

在 `scripts/send_from_notion.py` 中配置博主映射：

```python
BLOGGER_KEYWORDS = {
    "博主A": ["关键词1", "关键词2"],
    "博主B": ["关键词3"],
}
```

系统会根据 Notion 条目的名称字段匹配博主关键词，自动选择对应的图片。

### 状态流转

```
未开始 → 发送成功 → 已发布
```

## 图片配置

### 博主图片

将博主图片放入 `scripts/images/` 目录，命名规则：

```
博主A.png  → 博主A的图片
博主B.png  → 博主B的图片
```

支持格式：png、jpg、jpeg

**注意**：图片名称需与 `send_from_notion.py` 中 `BLOGGER_KEYWORDS` 的键名一致。

### 界面截图

如果微信界面变化导致识别失败，重新截取界面元素：

```bash
python capture_ui.py
```

截图保存到 `scripts/ui_images/` 目录。

## API 配置

详细配置步骤请参考 [CONFIG.md](../CONFIG.md)

### 方式1：环境变量（推荐）

**Windows:**
```cmd
set NOTION_API_KEY=secret_xxxxxxxxxxxxx
set NOTION_DATABASE_ID=xxxxxxxxxxxxxxxx
```

**Linux/Mac:**
```bash
export NOTION_API_KEY=secret_xxxxxxxxxxxxx
export NOTION_DATABASE_ID=xxxxxxxxxxxxxxxx
```

### 方式2：配置文件

创建 `.env` 文件：
```
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxx
```

设置环境变量指向配置文件：
```bash
# Windows
set CONFIG_FILE=D:\path\to\.env

# Linux/Mac
export CONFIG_FILE=/path/to/.env
```

### 获取 Notion API Key

1. 访问 https://www.notion.so/my-integrations
2. 创建 Integration
3. 复制 Internal Integration Token（以 `secret_` 开头）
4. 在数据库页面添加连接：`...` → `Add connections` → 选择你的 Integration

### 获取数据库 ID

1. 打开你的 Notion 数据库页面
2. 点击右上角 `...` → `Copy link`
3. URL 格式为：`https://www.notion.so/your-workspace/DATABASE_ID?v=...`
4. 提取其中的 `DATABASE_ID` 部分

## 定时任务

配置定时任务实现每天自动发送：

```bash
# 示例：每天 8:00、12:00、18:00、21:00 发送
# 需要通过系统定时任务或调度工具配置
```

## 注意事项

1. **微信窗口**：发送时微信窗口需保持可见
2. **不要操作**：发送过程中不要移动鼠标或操作键盘
3. **安全停止**：如需中止，将鼠标移到屏幕左上角
4. **频率控制**：建议每天不超过 3-4 条
5. **图片准备**：确保博主图片已放入对应目录

## 故障排除

### 问题：找不到界面元素

**原因**：微信界面变化或截图失效

**解决**：重新截取界面元素
```bash
python capture_ui.py
```

### 问题：博主未识别

**原因**：名称不包含博主关键词

**解决**：
1. 在 Notion 中修改名称，添加博主关键词
2. 或在 `send_from_notion.py` 中添加新的关键词

### 问题：Notion API 错误

**原因**：API Key 未配置或失效

**解决**：
1. 检查环境变量 `NOTION_API_KEY` 和 `NOTION_DATABASE_ID` 是否设置
2. 确认 Notion Integration 已连接到数据库
3. 如使用配置文件，检查 `CONFIG_FILE` 环境变量是否正确

## 更新日志

- **2026-05-05**：初始版本，支持 Notion 集成、博主识别、自动发送
