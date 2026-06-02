---
name: moments-writer-pro
version: 2.0.0
description: 朋友圈智能工作流一站式控制台 - 支持AI文案公式生成、云端发稿池同步(Notion/飞书多维表格)、定时调度与GUI即时发送
tags: [wechat, moments, copywriting, 朋友圈, 私域, 飞书, Lark, Notion]
author: Claude Developer Agent
commands:
  - name: moments
    description: 朋友圈工作流一站式控制台
    parameters:
      - name: action
        description: 执行指令：generate(写文案), sync(同步Notion/飞书), schedule(管理定时任务), send(立即发送朋友圈), list(查看发送队列)
        required: true
      - name: type
        description: 文案公式类型 (仅generate)
        required: false
      - name: topic
        description: 文案主题 (仅generate)
        required: false
      - name: source
        description: 云端同步源 (仅sync: all, luffy, v2, feishu)
        required: false
      - name: schedule_action
        description: 定时控制指令 (仅schedule: start, stop, list)
        required: false
      - name: cron
        description: 定时 Cron 表达式 (仅schedule start)
        required: false
      - name: dry_run
        description: 是否仅模拟运行 (仅send/sync/schedule)
        required: false
      - name: limit
        description: 列出文案条数 (仅list)
        required: false
---

# 朋友圈智能控制台 Pro 🌟

基于**麦肯锡信任公式**与**私域变现核心方法论**，一站式整合本地数据存储（SQLite）、多云端数据源（Notion 发稿池 + 飞书多维表格）、Windows/Python 定时计划任务以及微信桌面客户端 GUI 自动化发送。

```
信任 = (专业度 × 可靠度 × 亲密度) / 自身利益
```

---

## 核心命令与功能

### 1. ✍️ 智能文案生成 (`action=generate`)
利用最科学的私域营销模型，为 AI 机器人生成专门的文案拟定 Prompt。

- `/moments action=generate type=story topic=深夜的一碗面` (故事代入型 - 真实温暖的故事切入)
- `/moments action=generate type=professional topic=如何优雅排版` (专业型)
- `/moments action=generate type=reliable topic=我的副业逆袭经历` (靠谱型)
- `/moments action=generate type=warm topic=清晨的第一杯手冲咖啡` (温暖型)
- `/moments action=generate type=altruistic topic=AI变现的三个硬核干货` (利他型)
- `/moments action=generate type=counter topic=打破摸鱼可耻的偏见` (反认知破圈)

### 2. 🔄 多云端同步 (`action=sync`)
一键将 Notion 数据库或飞书多维表格（Bitable）中「未开始/未发布」的朋友圈文案抓取至本地 SQLite 数据库队列。
*同步过程中自动识别博主（如 `路飞`、`大元`、`全哥`、`李真` 等）并匹配其专属宣传配图，无匹配则采用随机图片兜底，同时智能去重。*

- `/moments action=sync source=all` (同步所有 Notion 和 飞书 数据)
- `/moments action=sync source=luffy` (仅同步路飞发稿池)
- `/moments action=sync source=feishu dry_run=true` (模拟同步飞书数据)

### 3. 📅 自动调度配置 (`action=schedule`)
管理朋友圈定时发布计划。支持 Python 后台驻留进程与 Windows 系统任务计划程序（Schtasks）。

- `/moments action=schedule schedule_action=start cron="0 8 * * *"` (设定每天早上 8:00 发送)
- `/moments action=schedule schedule_action=list` (列出所有系统朋友圈计划任务)
- `/moments action=schedule schedule_action=stop` (停止当前的定时计划)

### 4. 🚀 微信一键发送 (`action=send`)
立刻从本地 SQLite 待发送队列中取出第一条文案与对应绑定的图片，自动激活微信客户端、进入朋友圈、填充内容并发布。
*发布成功后，系统会自动向 Notion 或 飞书 触发状态更新回调，将云端状态标为「完成/已发布」。*

- `/moments action=send` (执行真实微信发布)
- `/moments action=send dry_run=true` (仅模拟测试数据流)

### 5. 📊 队列列表与统计 (`action=list`)
查看本地 SQLite 的待发文案、已发送历史，以及各类别的统计详情。

- `/moments action=list limit=10` (查看最近10条待发送文案与日志统计)

---

## 本地数据库表结构 💾

本地 SQLite 数据库位于 `D:\weixin\wechat-moments-auto-v2\data\moments.db`：
1. `content`：存储朋友圈内容队列。包含文案、图片路径（`image_path`）、状态（`pending/sent/skipped`）、来源类型（`local/notion/feishu`）以及云端唯一 ID (`source_id`)。
2. `send_log`：存储发送成功/失败的历史日志与错误信息。
3. `schedule_config`：存储定时自动发送的表达式配置。
