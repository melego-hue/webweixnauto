# 快速开始指南

## 5分钟快速上手

### 第一步：检查环境

确保已安装 Python 3.7+ 和必要的依赖：

```bash
python --version
pip install requests pyautogui Pillow opencv-python
```

### 第二步：配置博主图片

将博主头像放入 `images/` 目录：
- `路飞.png` - 路飞博主
- `大元.png` - 大元博主  
- `全哥.png` - 全哥博主

**注意**：文件名必须与代码中的博主名称匹配

### 第三步：测试运行

```bash
# 进入脚本目录
cd scripts

# 测试微信窗口检测
python run.py test

# 模拟发送测试
python run.py notion --dry-run
```

### 第四步：正式发送

```bash
# 实际发送（会更新 Notion 状态）
python run.py notion

# 或指定延迟后发送
python run.py notion --min-delay 5 --max-delay 10
```

## 日常使用流程

1. **准备文案**：在 Notion 数据库中添加"未开始"状态的内容
2. **配置图片**：确保对应博主有头像图片
3. **运行发送**：`python run.py notion`
4. **查看结果**：检查朋友圈是否发送成功，Notion 状态是否更新

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `python run.py notion` | 从 Notion 发送 |
| `python run.py notion --dry-run` | 模拟发送测试 |
| `python run.py send --text "内容"` | 手动发送 |
| `python run.py test` | 测试微信窗口 |
| `python run.py help` | 显示帮助 |

## 故障排查

### 问题1：提示"No image for blogger"
**解决**：为该博主添加头像图片到 `images/` 目录

### 问题2：图像识别失败
**解决**：运行 `python run.py capture` 重新截取界面元素

### 问题3：微信激活失败
**解决**：
1. 确保微信已启动并登录
2. 检查 `Ctrl+Alt+W` 快捷键是否被其他程序占用
3. 手动将微信窗口置于前台

### 问题4：Notion 连接失败
**解决**：
1. 检查 API Token 是否有效
2. 确认数据库已分享给集成
3. 检查网络连接

## 高级配置

### 添加新博主

编辑 `send_from_notion.py` 中的 `BLOGGER_KEYWORDS`：

```python
BLOGGER_KEYWORDS = {
    "Luffy": ["路飞"],
    "Dayuan": ["大元"],
    "新博主": ["关键词1", "关键词2"],
}
```

同时在 `get_blogger_image` 函数中添加图片名称映射。

### 修改延迟时间

```bash
# 立即发送
python run.py notion --min-delay 0 --max-delay 0

# 延迟10-20分钟
python run.py notion --min-delay 10 --max-delay 20
```

### 跳过状态更新

```bash
python run.py notion --no-update
```

## 自动化定时任务

可以使用 Windows 任务计划程序设置定时发送：

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发时间（如每天 9:00）
4. 设置操作：启动程序 `python.exe`，参数：`run.py notion`
5. 设置起始位置：`D:\weixin\wechat-moments-auto\scripts`

## 技术支持

如遇到问题，请检查：
1. README.md 完整文档
2. 控制台错误信息
3. Notion 数据库状态
4. 微信窗口状态
