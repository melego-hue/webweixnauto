# 微信朋友圈自动发送技能

通过图像识别技术模拟用户操作，实现微信朋友圈自动发布。支持从 Notion 数据库读取内容、博主识别、图片匹配和定时发送。

## 功能特点

- **Notion 集成**：自动从 Notion 数据库读取待发布内容
- **博主识别**：根据名称关键词自动匹配博主，选择对应图片
- **图像识别**：通过截图识别界面元素，重启后无需重新配置
- **状态更新**：发送成功后自动更新 Notion 状态
- **定时任务**：支持配置定时自动发送

## 触发场景

- "发送微信朋友圈"
- "从 Notion 发朋友圈"
- "自动发朋友圈"
- "微信朋友圈定时发送"
- "帮我发个朋友圈"

## 使用方法

### 1. 从 Notion 自动发送

```bash
python scripts/send_from_notion.py
```

自动从 Notion 数据库读取状态为"未开始"的条目，识别博主后发送。

### 2. 手动发送指定内容

```bash
python scripts/send_by_image.py --text "朋友圈内容" --image "图片路径"
```

### 3. 模拟运行（不实际发送）

```bash
python scripts/send_from_notion.py --dry-run
```

## 配置要求

详细配置步骤请参考 [CONFIG.md](CONFIG.md)

### Notion 数据库字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 名称 | 标题 | 条目名称，需包含博主关键词 |
| AI小红书洗稿 | 文本 | 小红书风格文案（发送用） |
| 平台/状态 | 状态 | 未开始/已发布 |

### 博主识别规则

在 `scripts/send_from_notion.py` 中配置博主映射：

```python
BLOGGER_KEYWORDS = {
    "博主A": ["关键词1", "关键词2"],
    "博主B": ["关键词3"],
}
```

### 博主图片

将博主图片放入 `scripts/images/` 目录，命名规则：`博主A.png`、`博主B.png`

### 界面截图

首次使用或微信界面变化时，需要截取界面元素：

```bash
python scripts/capture_ui.py
```

截图保存到 `scripts/ui_images/` 目录，包括：
- `moments_icon.png` - 朋友圈入口图标
- `camera_btn.png` - 相机按钮
- `publish_btn.png` - 发表按钮

## API 配置

### 方式1：环境变量（推荐）

```bash
# Windows
set NOTION_API_KEY=your_notion_integration_token
set NOTION_DATABASE_ID=your_database_id

# Linux/Mac
export NOTION_API_KEY=your_notion_integration_token
export NOTION_DATABASE_ID=your_database_id
```

### 方式2：配置文件

设置环境变量 `CONFIG_FILE` 指向你的配置文件：

```bash
# Windows
set CONFIG_FILE=D:\path\to\.env

# Linux/Mac
export CONFIG_FILE=/path/to/.env
```

配置文件内容：
```
NOTION_API_KEY=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id
```

### 获取 Notion API Key

1. 访问 https://www.notion.so/my-integrations
2. 创建 Integration
3. 复制 Internal Integration Token
4. 在数据库页面添加连接：`...` → `Add connections` → 选择你的 Integration

## 依赖

```bash
pip install pyautogui pyperclip requests pillow
```

## 注意事项

1. **微信窗口**：发送时微信窗口需保持可见
2. **不要操作**：发送过程中不要移动鼠标或操作键盘
3. **安全停止**：如需中止，将鼠标移到屏幕左上角
4. **频率控制**：建议每天不超过 3-4 条
5. **封号风险**：存在一定的封号风险，请谨慎使用

## 故障排除

### 找不到界面元素

**原因**：微信界面变化或截图失效

**解决**：重新截取界面元素
```bash
python scripts/capture_ui.py
```

### 博主未识别

**原因**：名称不包含博主关键词

**解决**：在 Notion 中修改名称，添加博主关键词

### Notion API 错误

**原因**：API Key 未配置或失效

**解决**：
1. 检查环境变量 `NOTION_API_KEY` 和 `NOTION_DATABASE_ID` 是否设置
2. 确认 Notion Integration 已连接到数据库
3. 如使用配置文件，检查 `CONFIG_FILE` 环境变量是否正确

## 文件结构

```
wechat-moments-auto/
├── SKILL.md                    # 技能说明文件
├── CONFIG.md                   # 配置指南
├── .env.example                # 环境变量示例
├── README.md                   # 详细操作手册
└── scripts/
    ├── send_from_notion.py     # 从 Notion 读取并发送
    ├── send_by_image.py        # 图像识别发送核心
    ├── capture_ui.py           # 界面截图工具
    ├── debug_coords.py         # 坐标调试工具
    ├── debug_visual.py         # 可视化调试工具
    ├── ui_images/              # 界面元素截图
    └── images/                 # 博主图片
```

## 更新日志

- **2026-05-05**：初始版本，支持 Notion 集成、博主识别、自动发送
