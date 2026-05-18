# 微信朋友圈自动发送 - 配置指南

## 快速开始

### 1. 安装依赖

```bash
pip install pyautogui pyperclip requests pillow
```

### 2. 配置 Notion API

#### 方式A：环境变量（推荐）

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

#### 方式B：配置文件

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

### 3. 获取 Notion 凭据

#### 获取 API Key

1. 访问 https://www.notion.so/my-integrations
2. 点击 "New integration"
3. 填写名称，选择工作区
4. 复制 "Internal Integration Token"（以 `secret_` 开头）

#### 获取数据库 ID

1. 打开你的 Notion 数据库页面
2. 点击右上角 `...` → `Copy link`
3. URL 格式为：`https://www.notion.so/your-workspace/DATABASE_ID?v=...`
4. 提取其中的 `DATABASE_ID` 部分

#### 连接 Integration 到数据库

1. 打开数据库页面
2. 点击右上角 `...` → `Add connections`
3. 选择你创建的 Integration

### 4. 配置博主映射

编辑 `scripts/send_from_notion.py`：

```python
BLOGGER_KEYWORDS = {
    "博主A": ["关键词1", "关键词2"],
    "博主B": ["关键词3"],
}
```

### 5. 准备博主图片

将图片放入 `scripts/images/` 目录，命名格式：`博主A.png`

### 6. 截取界面元素

首次使用需要截取微信界面元素：

```bash
python scripts/capture_ui.py
```

按提示截取：
- `moments_icon.png` - 朋友圈入口图标
- `camera_btn.png` - 相机按钮
- `publish_btn.png` - 发表按钮

## Notion 数据库字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 名称 | 标题 | 条目名称，需包含博主关键词 |
| AI小红书洗稿 | 文本 | 小红书风格文案（发送用） |
| 平台/状态 | 状态 | 未开始/已发布 |

## 使用示例

### 从 Notion 自动发送

```bash
python scripts/send_from_notion.py
```

### 模拟运行（不实际发送）

```bash
python scripts/send_from_notion.py --dry-run
```

### 手动发送指定内容

```bash
python scripts/send_by_image.py --text "朋友圈内容" --image "图片路径"
```

## 常见问题

### Q: 提示 "未找到 NOTION_API_KEY"

A: 检查环境变量是否正确设置，或配置文件路径是否正确

### Q: 提示 "博主未识别"

A: 在 `send_from_notion.py` 的 `BLOGGER_KEYWORDS` 中添加博主映射

### Q: 找不到界面元素

A: 重新运行 `capture_ui.py` 截取界面元素

### Q: 微信窗口未激活

A: 确保微信已启动，并检查快捷键 `Ctrl+Alt+W` 是否可用

## 注意事项

1. 发送时微信窗口需保持可见
2. 发送过程中不要操作鼠标键盘
3. 紧急停止：将鼠标移到屏幕左上角
4. 建议每天不超过 3-4 条
5. 存在封号风险，请谨慎使用
