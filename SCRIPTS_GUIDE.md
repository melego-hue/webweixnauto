# 核心脚本说明

## 核心文件

### 1. run.py - 统一入口
主入口脚本，提供所有功能的命令行接口。

```bash
python run.py notion              # 从 Notion 发送
python run.py send --text "内容"  # 手动发送
python run.py test                # 测试微信窗口
python run.py help                # 显示帮助
```

### 2. send_from_notion.py - Notion 集成
负责与 Notion 数据库交互：
- 读取待发布内容
- 识别博主
- 匹配图片
- 更新发布状态

**关键配置**：
- `DATABASE_ID`: Notion 数据库 ID
- `BLOGGER_KEYWORDS`: 博主关键词映射
- `get_notion_token()`: Notion API Token

### 3. send_by_image.py - 发送核心
基于图像识别的微信朋友圈发送：
- 微信窗口检测和激活
- 图像识别定位界面元素
- 自动操作（点击、输入等）
- 发送重试机制

**关键配置**：
- `UI_IMAGES_DIR`: 界面元素截图目录
- `find_and_click()`: 图像识别点击函数

### 4. wechat_utils.py - 微信窗口管理
增强的微信窗口检测和管理：
- 进程检测（支持多版本）
- 窗口可见性检测
- 多种激活策略
- 多屏幕支持

**关键类**：
- `WeChatActivator`: 微信窗口激活器

### 5. config.py - 配置文件
统一的配置管理：
- 路径配置
- Notion 配置
- 博主配置
- 图像识别设置

## 辅助脚本

### generate_content.py
自动生成朋友圈文案

### capture_ui.py
截取微信界面元素用于图像识别

## 文件依赖关系

```
run.py (入口)
  ├── send_from_notion.py (Notion集成)
  │     └── 使用: requests, config
  ├── send_by_image.py (发送核心)
  │     ├── wechat_utils.py (窗口管理)
  │     └── 使用: pyautogui, cv2, config
  └── wechat_utils.py (窗口管理)
        └── 使用: ctypes, subprocess, config
```

## 配置优先级

1. `config.py` - 基础配置（路径、Token等）
2. `send_from_notion.py` - Notion相关配置
3. `send_by_image.py` - 图像识别配置
4. `wechat_utils.py` - 窗口管理配置

## 自定义扩展

### 添加新博主

1. 在 `send_from_notion.py` 的 `BLOGGER_KEYWORDS` 中添加关键词
2. 在 `get_blogger_image()` 中添加图片名称映射
3. 在 `images/` 目录添加博主头像

### 修改界面元素

1. 运行 `python run.py capture` 截取新元素
2. 将截图保存到 `ui_images/` 目录
3. 在 `send_by_image.py` 中更新元素名称映射

### 调整发送逻辑

修改 `send_by_image.py` 中的 `send_moments()` 函数：
- 调整等待时间
- 修改操作顺序
- 添加新的发送步骤

## 调试技巧

### 启用详细日志

在关键函数中添加 print 语句：
```python
print(f"[DEBUG] Step 1: {variable}")
```

### 测试单独功能

```bash
# 测试 Notion 连接
python -c "from send_from_notion import fetch_notion_content; print(fetch_notion_content())"

# 测试图像识别
python -c "from send_by_image import find_and_click; print(find_and_click('moments_icon'))"

# 测试窗口检测
python run.py test
```

### 查看 Notion 数据

```python
import requests
from send_from_notion import get_notion_token, DATABASE_ID

token = get_notion_token()
headers = {'Authorization': f'Bearer {token}', 'Notion-Version': '2022-06-28'}
response = requests.post(f'https://api.notion.com/v1/databases/{DATABASE_ID}/query', headers=headers)
print(response.json())
```

## 维护建议

1. **定期更新界面截图**：微信版本更新后需要重新截取
2. **备份配置文件**：保存关键配置的副本
3. **监控发送日志**：关注发送成功率和失败原因
4. **测试环境验证**：重大更新前先在测试环境验证
