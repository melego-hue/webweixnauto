# WeChat Moments Auto Sender

微信朋友圈自动化发送工具 - 文档索引

## 📚 文档目录

### 🚀 快速开始
- **[QUICK_START.md](QUICK_START.md)** - 5分钟快速上手指南
- **[README.md](README.md)** - 完整项目文档（包含本地版本）
- **[README_local.md](README_local.md)** - 本地Excel版本完整文档

### 📖 详细指南
- **[SUMMARY.md](SUMMARY.md)** - 使用总结和验证报告
- **[SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)** - 核心脚本详细说明
- **[CHECKLIST.md](CHECKLIST.md)** - 功能检查清单
- **[LOCAL_GUIDE.md](LOCAL_GUIDE.md)** - 本地版本使用指南
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 部署指南
- **[FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md)** - 文件夹结构说明

## 🎯 你想要的

### 我想使用本地Excel版本
→ 阅读 **[LOCAL_GUIDE.md](LOCAL_GUIDE.md)** 和 **[README_local.md](README_local.md)**

### 我想快速开始使用
→ 阅读 **[QUICK_START.md](QUICK_START.md)**

### 我想了解完整功能
→ 阅读 **[README.md](README.md)**

### 我想知道如何配置和维护
→ 阅读 **[SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)**

### 我想查看测试结果和总结
→ 阅读 **[SUMMARY.md](SUMMARY.md)**

### 我想确认所有功能都正常
→ 查看 **[CHECKLIST.md](CHECKLIST.md)**

## 💡 快速命令

```bash
# 本地Excel版本
cd D:\工作流方法\wechat-moments-auto\scripts

# 生成Excel数据库
python generate_bulk_content.py --num 100

# 查看帮助
python run_local.py help

# 从本地Excel发送
python run_local.py local

# 模拟测试
python run_local.py local --dry-run
```

## 📞 获取帮助

1. **本地版本问题** → 查看 **[LOCAL_GUIDE.md](LOCAL_GUIDE.md)** 的解决方案
2. **常见问题** → 查看 **[README.md](README.md#常见问题)** 的 FAQ 部分
3. **故障排查** → 查看 **[QUICK_START.md](QUICK_START.md#故障排查)** 的解决方案
4. **详细配置** → 查看 **[SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)** 的配置说明
5. **代码问题** → 查看 **[CHECKLIST.md](CHECKLIST.md)** 的代码质量检查

## 📋 文档更新记录

| 日期 | 文档 | 更新内容 |
|------|------|---------|
| 2026-05-18 | README.md | 完整项目文档 v2.5 |
| 2026-05-18 | QUICK_START.md | 快速开始指南 |
| 2026-05-18 | SUMMARY.md | 使用总结和验证报告 |
| 2026-05-18 | SCRIPTS_GUIDE.md | 核心脚本详细说明 |
| 2026-05-18 | CHECKLIST.md | 功能检查清单 |
| 2026-05-18 | README_local.md | 本地Excel版本完整文档 |
| 2026-05-18 | LOCAL_GUIDE.md | 本地版本使用指南 |
| 2026-05-18 | DEPLOYMENT.md | 部署指南 |
| 2026-05-18 | FOLDER_STRUCTURE.md | 文件夹结构说明 |

## 🔧 核心文件

| 文件 | 说明 | 重要性 |
|------|------|--------|
| `content_database.xlsx` | Excel内容数据库 | ⭐⭐⭐⭐⭐ |
| `run_local.py` | 本地版本入口脚本 | ⭐⭐⭐⭐⭐ |
| `send_from_local.py` | 本地Excel发送核心模块 | ⭐⭐⭐⭐⭐ |
| `generate_bulk_content.py` | 批量内容生成脚本 | ⭐⭐⭐⭐⭐ |
| `send_by_image1.py` | 发送核心模块 | ⭐⭐⭐⭐⭐ |
| `wechat_utils.py` | 窗口管理工具 | ⭐⭐⭐⭐ |
| `config.py` | 配置文件 | ⭐⭐⭐⭐ |

## ⚠️ 注意事项

1. **李真图片缺失** - 需要添加 `images/李真.png`
2. **界面截图需更新** - 微信版本更新后重新截图
3. **Excel文件权限** - 确保脚本可以读写Excel文件
4. **定时任务配置** - Windows任务计划程序需要正确路径

## ✅ 下一步

### 本地Excel版本
1. 阅读 **[LOCAL_GUIDE.md](LOCAL_GUIDE.md)** 开始使用
2. 生成Excel数据库 `python generate_bulk_content.py --num 100`
3. 测试运行 `python run_local.py local --dry-run`
4. 执行首次发送 `python run_local.py local`

### Notion版本
1. 阅读 **[QUICK_START.md](QUICK_START.md)** 开始使用
2. 测试运行 `python run.py notion --dry-run`
3. 执行首次发送 `python run.py notion`

---

**版本**: v2.5 + 本地Excel版本  
**更新时间**: 2026-05-18  
**状态**: 正式可用
