---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5316da29121965ff3a210e6dce425447_b99e060c5e2511f1bd025254006c9bbf
    ReservedCode1: fqTWrrvtlhLYhlZzIsKVhNC9ixkmniHQ016jn0keJkmroudfctZa83OphiBjd7OElN8+d1DpxZyVPxK7OiSKIwV+ILo65Vkns4TTvkSPjReNmJNupUnhzEmV9AS8VTAgwV8SCnQ2f4oonYfIeqOPjcsS6cJKVAJ42QfqNYvZb4YKtGGWFQj961AFjA8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5316da29121965ff3a210e6dce425447_b99e060c5e2511f1bd025254006c9bbf
    ReservedCode2: fqTWrrvtlhLYhlZzIsKVhNC9ixkmniHQ016jn0keJkmroudfctZa83OphiBjd7OElN8+d1DpxZyVPxK7OiSKIwV+ILo65Vkns4TTvkSPjReNmJNupUnhzEmV9AS8VTAgwV8SCnQ2f4oonYfIeqOPjcsS6cJKVAJ42QfqNYvZb4YKtGGWFQj961AFjA8=
---



# 朋友圈定时自动发送

完整的本地化朋友圈自动化方案：文案生成 → 本地存储 → 图像识别发送 → 定时调度，彻底脱离 Notion/云端依赖。

## 架构

```
用户(通过 Marvis) → SKILL.md(本文件) → cli.py(统一入口)
                                           ├── db_manager.py  → SQLite(本地文案库)
                                           ├── content_gen.py → 模板/LLM 文案生成
                                           ├── sender.py      → 图像识别发送(微信操控)
                                           └── scheduler.py   → 定时调度(Python/Win任务)
```

**核心原则**:
- 一切操作通过 `cli.py` 统一入口，这是用户与本 skill 的交互界面
- 文案完全本地化存储于 SQLite，不依赖外部 API
- 发送复用成熟的图像识别方案（wechat-moments-auto-v2/scripts/）
- LLM 生成由 Marvis（你）直接完成，无需额外配置

## 前置条件

确保以下依赖已安装：
```
pip install pyautogui pyperclip Pillow opencv-python schedule
```

微信必须保持登录状态，主窗口可见（支持最小化，发送时会自动激活）。

## 初始化

首次使用必须执行初始化，创建数据库：
```bash
python cli.py init
```

## 常用工作流

### 工作流 1：快速生成文案并发送

```bash
# 1. 生成 10 条随机文案入库
python cli.py generate -n 10

# 2. 随机发送一条
python cli.py send

# 3. 模拟发送（不实际发）
python cli.py send --dry-run
```

### 工作流 2：批量填充文案库

用户说"帮我填充朋友圈文案库"时，运行：
```bash
python cli.py generate -n 30
```

用户说"生成 20 条早安文案"时，运行：
```bash
python cli.py generate -c morning -n 20
```

### 工作流 3：定时自动发送

用户说"设置每天早上8点自动发朋友圈"时，选择以下方式之一：

**方式 A — Python schedule（推荐，轻量）**:
```bash
python cli.py schedule start --cron "0 8 * * *"
```

**方式 B — Windows 计划任务（系统级）**:
```bash
python cli.py schedule start --cron "0 8 * * *" --mode windows
```

停止定时任务：
```bash
python cli.py schedule stop --mode windows
```

查看定时任务：
```bash
python cli.py schedule list
```

### 工作流 4：手动添加/发送自定义文案

```bash
# 添加一条自定义文案
python cli.py add --text "今天去爬山了，风景超级好！" -c life

# 发送自定义文案（不经过本地库）
python cli.py send --text "周末愉快！" --dry-run
```

### 工作流 5：LLM 增强生成（通过 Marvis）

当用户希望用 LLM 生成更自然、更有创意的文案时，你（Marvis）应直接生成文案，然后通过命令行添加到库中。

**步骤**:
1. 你直接调用 LLM 能力生成中文朋友圈文案
2. 将生成的文案通过 `cli.py add --text "..."` 写入本地库
3. 告知用户已添加

示例：用户说"帮我用 AI 生成 5 条搞笑的早安文案"
→ 你直接生成 5 条文案，然后逐条执行：
```bash
python cli.py add --text "早安！今天也是元气满满（指元气都被抽干了）的一天呢" -c morning --tags "搞笑,早安"
python cli.py add --text "早上的我被闹钟叫醒，闹钟被我摔醒，我俩互不亏欠" -c morning --tags "搞笑,早安"
...
```

### 工作流 6：查看状态与管理

```bash
# 统计概览
python cli.py status

# 列出待发送
python cli.py list

# 列出已发送
python cli.py list -s sent

# 搜索文案
python cli.py search "早安"

# 重置已发送 → 待发送（可重新发一轮）
python cli.py reset
```

## 命令速查

| 命令 | 说明 |
|------|------|
| `init` | 初始化数据库 |
| `status` | 查看统计信息 |
| `generate -n 10` | 生成 10 条文案入库 |
| `generate -c morning -n 20` | 生成 20 条早安文案 |
| `add --text "..."` | 手动添加单条文案 |
| `add -b 20` | 批量生成 20 条 |
| `list` | 列出待发送文案 |
| `list -s sent` | 列出已发送文案 |
| `send` | 随机发送一条待发送文案 |
| `send --text "..."` | 发送自定义内容 |
| `send --dry-run` | 模拟发送 |
| `search "关键词"` | 搜索文案 |
| `reset` | 重置所有已发送状态 |
| `schedule start --cron "0 8 * * *"` | 设置定时任务 |
| `schedule stop --mode windows` | 停止定时任务 |
| `schedule list` | 查看定时任务 |

## LLM 生成指南（供 Marvis 使用）

当用户要求用 LLM 生成文案时，遵循以下规则：

1. **长度**: 15-50 字，一句话可搞定就不用两句话
2. **语气**: 口语化、接地气，避免 AI 痕迹（少用"在这个充满XX的时代"等套话）
3. **适配**: 生成后直接通过 `cli.py add --text "..."` 写入库，并告知用户
4. **分类**: 根据文案内容标记合适的 category
5. **批量**: 用户说"生成 N 条"时，一次性生成 N 条不同文案，逐条 add

**好的文案示例**:
- "周一综合症晚期，咖啡都救不回来"
- "今天天气很好，可惜我在上班"
- "长大后才明白，小时候想快点长大是最后悔的事"
- "今天的我：人模狗样地活着"

**避免的文案风格**:
- "在这个充满不确定性的世界里，我们要学会拥抱变化"（太 AI 味）
- "人生就像一场旅行，重要的不是目的地，而是沿途的风景"（太俗套）
- 大段排比句和华丽修饰词堆砌

## 图片配置

发送朋友圈时会从 `D:\weixin\wechat-moments-auto-v2\images\` 目录随机选取图片。
如需配特定图片，使用 `--image` 参数指定。

建议提前在 images 目录放入适合配朋友圈的图片（竖版 9:16 比例最佳）。

## 数据库位置

```
D:\weixin\wechat-moments-auto-v2\data\moments.db
```

包含三张表：
- `content`: 文案主表（分类、内容、状态、来源）
- `send_log`: 发送日志
- `schedule_config`: 定时任务配置

## 故障排查

| 问题 | 解决 |
|------|------|
| 发送失败 | 确认微信已登录、窗口未最小化到托盘 |
| UI 元素找不到 | 运行 `python D:\weixin\wechat-moments-auto-v2\scripts\capture_ui.py` 重新截图 |
| 没有待发送文案 | 运行 `generate -n 10` 填充库 |
| schedule 库未安装 | `pip install schedule` |
| 权限不足 | 以管理员身份运行终端创建 Windows 计划任务 |

## 从旧版（Notion）迁移

此 skill 是 `wechat-moments-auto-v2` 的升级版，完全替代了 `send_from_notion.py`。
迁移步骤：
1. `python cli.py init` 初始化新数据库
2. `python cli.py generate -n 100` 批量生成本地文案库
3. 使用 `python cli.py send` 替代原来的 `python send_from_notion.py`
4. 使用 `python cli.py schedule start` 替代原来的定时脚本
*（内容由AI生成，仅供参考）*
