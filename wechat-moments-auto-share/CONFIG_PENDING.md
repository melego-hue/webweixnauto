# WeChat Moments Auto Sender v2

## 项目信息
- **版本**: v2.0
- **状态**: 待配置
- **Notion ID**: 等待配置

## 配置说明

### 1. Notion 配置
在 `scripts/send_from_notion.py` 中修改：

```python
def get_notion_token():
    return "your_new_api_token_here"

DATABASE_ID = "your_new_database_id_here"
```

### 2. 字段配置
根据新的 Notion 数据库修改字段名：

```python
STATUS_FIELD = "新的状态字段名"
STATUS_PENDING = "未开始"
STATUS_COMPLETED = "完成"
CONTENT_FIELD = "新的内容字段名"
TITLE_FIELD = "新的标题字段名"
```

### 3. 博主配置
根据需要修改博主关键词：

```python
BLOGGER_KEYWORDS = {
    "博主1": ["关键词1", "关键词2"],
    "博主2": ["关键词3"],
}
```

## 文件说明

### 核心脚本
- `run.py` - 统一入口
- `send_from_notion.py` - Notion 集成
- `send_by_image.py` - 发送核心
- `wechat_utils.py` - 窗口管理
- `config.py` - 配置文件

### 目录结构
```
wechat-moments-auto-v2/
├── scripts/         # 脚本目录
│   ├── run.py
│   ├── send_from_notion.py
│   ├── send_by_image.py
│   └── wechat_utils.py
├── images/          # 博主图片
└── ui_images/       # 界面截图
```

## 使用方式

```bash
# 进入脚本目录
cd d:\weixin\wechat-moments-auto-v2\scripts

# 配置完成后测试
python run.py test

# 模拟发送
python run.py notion --dry-run

# 实际发送
python run.py notion
```

## 待配置项目

- [ ] Notion API Token
- [ ] Database ID
- [ ] 字段名称
- [ ] 博主关键词
- [ ] 博主图片

---
**创建时间**: 2026-05-18
**状态**: 等待配置 Notion ID
