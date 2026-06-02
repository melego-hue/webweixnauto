# WeChat Moments Auto Sender v2 - Configuration Complete

## ✅ 配置完成

### Notion 配置
- **API Token**: `your_notion_api_token_here` ✅
- **Database ID**: `your_notion_database_id_here` ✅
- **数据库名称**: AI朋友圈文案 ✅

### 数据库结构
- **状态字段**: 发布状态
  - 选项: "未发布", "已发布"
- **内容字段**: AI朋友圈文案 (title)

### 图片配置
- **图片目录**: `D:\weixin\wechat-moments-auto\random-images\images`
- **图片数量**: 8 张
- **选择方式**: 随机选择
- **支持格式**: PNG, JPG, JPEG, GIF, BMP

### 功能特点
- ✅ 从 Notion 读取"未发布"状态的文案
- ✅ 随机选择图片（从8张图片中）
- ✅ 发送后自动更新状态为"已发布"
- ✅ 支持模拟运行（dry-run）

## 📋 使用方式

```bash
# 进入脚本目录
cd d:\weixin\wechat-moments-auto-v2\scripts

# 模拟测试（不实际发送）
python run.py notion --dry-run

# 实际发送
python run.py notion

# 立即发送（无延迟）
python run.py notion --min-delay 0 --max-delay 0
```

## ⚠️ 当前状态

数据库中当前所有内容都是"已发布"状态，所以暂时没有待发送的内容。

**解决方案**: 在 Notion 数据库中添加新的"未发布"状态的内容，然后运行发送命令。

## 🔄 与第一套的区别

| 项目 | 第一套 (v1) | 第二套 (v2) |
|------|-------------|-------------|
| **图片选择** | 博主匹配 | **随机选择** |
| **图片目录** | `images/` | `random-images/images/` |
| **数据库** | 路飞全自动发稿池V2.5 | AI朋友圈文案 |
| **博主识别** | 支持 | 不需要 |

## 📝 工作流程

1. 从 Notion 读取"未发布"状态的内容
2. 随机选择一张图片（从8张图片中）
3. 发送朋友圈
4. 更新 Notion 状态为"已发布"

---
**配置时间**: 2026-05-18 13:23
**状态**: ✅ 配置完成，等待添加内容
