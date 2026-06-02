# WeChat Moments Auto Sender v2 - 文件清单

## 📁 完整目录结构

```
D:\weixin\wechat-moments-auto-v2\
│
├── 📂 scripts/                          # 核心脚本目录
│   ├── run.py                           # 统一入口脚本 ⭐
│   ├── send_from_notion.py              # Notion 集成 ⭐
│   ├── send_by_image.py                 # 发送核心 ⭐
│   ├── wechat_utils.py                  # 窗口管理 ⭐
│   ├── config.py                        # 配置文件 ⭐
│   ├── capture_ui.py                    # 截图工具
│   ├── generate_content.py              # 内容生成
│   ├── generate_image.py               # 图片生成
│   ├── generate_moments_image.py       # 朋友圈图片生成
│   ├── main.py                          # 旧版主入口
│   ├── send_by_window.py                # 窗口版发送
│   ├── send_moments.py                 # 旧版发送
│   └── send_moments_v2.py              # 旧版发送v2
│
├── 📂 images/                          # 博主图片目录
│   ├── 路飞.png                         # 路飞博主头像
│   ├── 大元.png                         # 大元博主头像
│   └── 全哥.png                         # 全哥博主头像
│
├── 📂 ui_images/                       # 界面元素截图
│   ├── moments_icon.png                # 朋友圈图标
│   ├── camera_btn.png                  # 相机按钮
│   ├── publish_btn.png                 # 发表按钮
│   ├── moments_icon_new.png            # 新版朋友圈图标
│   └── moments_icon_old.png            # 旧版朋友圈图标
│
├── 📄 README.md                         # 项目说明文档
└── 📄 CONFIG_PENDING.md                # 配置待办清单
```

## ⭐ 核心文件说明

### 1. run.py - 统一入口
**功能**: 所有功能的统一入口
**重要性**: ⭐⭐⭐⭐⭐ (必须)

```bash
python run.py notion          # 从 Notion 发送
python run.py send --text "内容"  # 手动发送
python run.py test            # 测试微信窗口
python run.py help            # 显示帮助
```

### 2. send_from_notion.py - Notion 集成
**功能**: 与 Notion 数据库交互
**重要性**: ⭐⭐⭐⭐⭐ (必须)
**待配置**: 
- Notion API Token
- Database ID
- 字段名称

### 3. send_by_image.py - 发送核心
**功能**: 图像识别和自动发送
**重要性**: ⭐⭐⭐⭐⭐ (必须)
**特点**: 已配置完成，可直接使用

### 4. wechat_utils.py - 窗口管理
**功能**: 微信窗口检测和激活
**重要性**: ⭐⭐⭐⭐ (重要)
**特点**: 已配置完成，可直接使用

### 5. config.py - 配置文件
**功能**: 统一配置管理
**重要性**: ⭐⭐⭐⭐ (重要)
**特点**: 可集中管理所有配置

## 📦 辅助文件说明

### 截图工具
- `capture_ui.py` - 截取界面元素

### 内容生成
- `generate_content.py` - 生成文案
- `generate_image.py` - 生成图片
- `generate_moments_image.py` - 生成朋友圈图片

### 历史版本
- `main.py` - 旧版入口
- `send_moments.py` - 旧版发送
- `send_moments_v2.py` - 旧版发送v2
- `send_by_window.py` - 窗口版发送

## 🖼️ 图片文件说明

### 博主图片 (images/)
| 文件名 | 博主 | 用途 | 状态 |
|--------|------|------|------|
| 路飞.png | 路飞 | 朋友圈配图 | ✅ 已配置 |
| 大元.png | 大元 | 朋友圈配图 | ✅ 已配置 |
| 全哥.png | 全哥 | 朋友圈配图 | ✅ 已配置 |

### 界面截图 (ui_images/)
| 文件名 | 用途 | 状态 |
|--------|------|------|
| moments_icon.png | 朋友圈图标 | ✅ 已配置 |
| camera_btn.png | 相机按钮 | ✅ 已配置 |
| publish_btn.png | 发表按钮 | ✅ 已配置 |
| moments_icon_new.png | 新版图标（备用） | ✅ 已配置 |
| moments_icon_old.png | 旧版图标（备用） | ✅ 已配置 |

## 📝 文档文件说明

### 必读文档
1. **README.md** - 项目整体说明
2. **CONFIG_PENDING.md** - 配置待办清单

### 参考文档（第一套）
- `../wechat-moments-auto/README.md` - 完整使用文档
- `../wechat-moments-auto/QUICK_START.md` - 快速开始
- `../wechat-moments-auto/SUMMARY.md` - 使用总结

## 🔧 配置状态

### ✅ 已完成配置
- [x] 脚本文件复制
- [x] 图片文件复制
- [x] 界面截图复制
- [x] 微信窗口检测
- [x] 图像识别功能
- [x] 自动发送功能

### ⏳ 待配置
- [ ] Notion API Token
- [ ] Database ID
- [ ] 状态字段名称
- [ ] 内容字段名称
- [ ] 标题字段名称
- [ ] 博主关键词
- [ ] 博主图片（可选）

## 📊 与第一套对比

| 项目 | 第一套 (v1) | 第二套 (v2) |
|------|-------------|-------------|
| 路径 | `wechat-moments-auto/` | `wechat-moments-auto-v2/` |
| 脚本 | 13个核心脚本 | 13个核心脚本 |
| 图片 | 3张博主图片 | 3张博主图片 |
| 截图 | 5张界面截图 | 5张界面截图 |
| 文档 | 6个文档 | 2个文档 |
| 状态 | ✅ 正式可用 | ⏳ 待配置 |

## 🚀 下一步操作

### 1. 查看配置清单
```bash
cd d:\weixin\wechat-moments-auto-v2
cat CONFIG_PENDING.md
```

### 2. 配置 Notion
```bash
cd d:\weixin\wechat-moments-auto-v2\scripts
# 编辑 send_from_notion.py
```

### 3. 测试运行
```bash
# 测试微信窗口
python run.py test

# 模拟发送
python run.py notion --dry-run
```

### 4. 正式使用
```bash
# 实际发送
python run.py notion
```

---

**文件总数**: 18个
**核心脚本**: 13个
**图片文件**: 8个
**文档文件**: 2个
**创建时间**: 2026-05-18
**状态**: 待配置 Notion ID
