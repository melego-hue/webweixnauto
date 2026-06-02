# 🌟 WeChat Moments Auto-Scheduler Pro (微信朋友圈智能发布控制台)

> 一款基于 **麦肯锡信任公式** 与 **私域变现核心方法论** 打造的微信朋友圈智能自动分发系统。
> 本项目完美整合了本地数据中心（SQLite 队列）、多端云发稿池（Notion 数据库 + 飞书多维表格）、SiliconFlow AI (DeepSeek) 智能创作引擎、以及**高安全仿真物理轨迹**的微信桌面端 GUI 自动分发机制。

---

## ✨ 核心功能亮点

### 1. ✍️ 麦肯锡信任公式 AI 智能创作 (`action=generate`)
- 内置专业级私域变现文案 Prompt 生成器。包含 7 大核心文案模型：
  - **专业型** (建立权威) | **靠谱型** (塑造信任) | **温暖型** (日常拉近) | **利他型** (硬核干货) | **反认知** (打破心智) | **圈用户** (精准招募) | **故事代入型** (冲突引发极强共鸣)
- **硅基流动 (SiliconFlow) API 深层对接**：支持一键调用 **DeepSeek-V3** 模型，全自动撰写朋友圈草稿并自动排队入库，智能识别文案中的博主姓名并匹配对应的本地配图资产。

### 2. 🔄 多云端协同发稿池与去重同步 (`action=sync`)
- 支持多部门协同作业。运营、文案策划可在 **Notion 数据库** 或 **飞书多维表格（Bitable）** 中进行朋友圈创作与审核，状态设为「未开始」。
- 本地引擎一键执行增量同步，支持基于 `source_id` 的**金融级去重检测**，完美规避多人/多终端运行时的重复发布和抢单风险。

### 3. 📅 定时自动调度与系统计划任务 (`action=schedule`)
- 支持 Python 后台 schedule 守护进程或直接配置 **Windows 系统计划任务（Schtasks）**，在后台静默自动运行发送任务，无需人工干预。

### 4. 🛡️ “金盾级”人机仿真 GUI 自动发送 (`action=send`)
为了对抗个人微信严格的客户端安全风控检测，本项目深度定制了**像素级人机仿真视觉引擎**：
- **Canny 骨架轮廓特征提取**：采用 OpenCV 的 Canny 算子及微量高斯模糊提取按钮的“线条骨架”。**完全无视微信界面的深色/浅色模式色差，并对 DPI 系统缩放（如 125% 或 150%）提供 100% 免疫的高精度匹配**，防止误触。
- **三阶贝塞尔曲线移鼠**：模拟真人握持鼠标在屏幕上加速、减速及天然细微抖动的滑行轨迹，拒绝常规软件的瞬间移动，规避微信的机器轨迹行为监控。
- **随机落点微移**：每次点击按钮时自动加入 $\pm 4$ 像素的物理落点偏移，保证每次点击坐标独一无二。
- **反应时延仿真**：关键操作间随机加入 `0.5 ~ 1.5` 秒的高斯反应时间，模拟人眼和人脑的物理迟滞。
- **自动状态回写闭环**：发送成功后，自动向 Notion 或飞书多维表格回写 `已发布/完成` 状态，形成完美的团队协作闭环。

---

## 📦 目录结构

```text
wechat-moments-auto-pro/
├── README.md                     # 详细操作与GitHub说明书
├── CONFIG_COMPLETE.md            # 配置文件指引
├── D:\weixin\wechat-moments-auto-v2\data\
│   └── moments.db               # 本地 SQLite 数据库 (已进行安全升级)
├── images/                       # 存放博主/团队的专属配图 (例如: 路飞.png, 大元.png)
├── ui_images/                    # UI 特征骨架基准参考图 (Canny 匹配用)
├── scripts/                      # 核心脚本目录
│   ├── config.py                 # 统一全局配置文件 (安全脱敏版)
│   ├── feishu_client.py          # 飞书多维表格 API 驱动客户端
│   ├── sync_sources.py           # Notion/飞书多端发稿池双向增量同步引擎
│   ├── wechat_utils.py           # 微信窗口句柄管理与唤醒激活策略
│   └── send_by_image.py          # 人机仿真的朋友圈 GUI 发送内核 (Canny 骨架比对 + 贝塞尔移鼠)
└── skills/                       # OpenClaw 技能集成包
    └── moments-scheduler/
        ├── manifest.json         # OpenClaw 技能清单规范
        ├── main.js               # OpenClaw 智能控制台核心脚本 (多进程桥接)
        └── SKILL.md              # 技能使用手册
```

---

## ⚙️ 快速配置与安全脱敏

本项目严格遵循敏感密钥分离原则，所有 API Key 与 Database ID 均从本地环境变量或配置文件中加载，**请勿将敏感密钥直接提交至 GitHub**。

### 1. 本地 `.env` 配置文件
请在您本地的 `d:/AIWork/.env`（或项目根目录创建 `.env` 文件，且在 `.gitignore` 中将其排除）中，配置您的专属密钥：

```ini
# 硅基流动 SiliconFlow API 密钥 (用于 AI 朋友圈文案自动生成)
SILICONFLOW_API_KEY=sk-your_siliconflow_api_key_here
AI_MODEL=deepseek-ai/DeepSeek-V3

# Notion 发稿池配置
NOTION_API_KEY=your_notion_integration_token_here
NOTION_DATABASE_ID=your_notion_database_id_here

# 飞书多维表格发稿池配置 (选填)
FEISHU_APP_ID=cli_your_feishu_app_id_here
FEISHU_APP_SECRET=your_feishu_app_secret_here
FEISHU_APP_TOKEN=your_feishu_bitable_app_token_here
FEISHU_TABLE_ID=your_feishu_table_id_here
```

### 2. 环境依赖安装
```bash
pip install pyautogui pyperclip requests pillow opencv-python numpy
```

---

## 🚀 朋友圈智能控制台使用指南

通过 OpenClaw 技能，您可以在聊天窗口中直接输入以下指令来控制整个工作流：

### 1. ✍️ AI 智能写作与入库
```text
/moments action=generate type=story topic=我和AI排版相识的第一个深夜
```
> 系统将自动调用 SiliconFlow 上的 DeepSeek 智能模型，根据麦肯锡故事公式自动拟稿、匹配博主配图，并自动加入本地 SQLite 发送队列！

### 2. 🔄 多云端同步
```text
/moments action=sync source=all
```
> 一键拉取 Notion 和 飞书 表格中所有的 Pending 文案，在本地完成金融级去重检测与博主配图绑定。

### 3. 📊 查看发稿队列与日志
```text
/moments action=list limit=10
```
> 显示本地数据库的状态统计（包括待发送、已发送数量及分类占比），并列出接下来的 10 条朋友圈明细。

### 4. 📅 自动调度管理
```text
/moments action=schedule schedule_action=start cron="0 8 * * *"
```
> 在 Windows 计划任务程序中设定每天早上 8:00 定时执行朋友圈发送，静默稳定运行。

### 5. 🚀 微信仿真发送
```text
/moments action=send dry_run=true
```
> 模拟运行一次朋友圈自动发布：自动置顶微信、进行 Canny 骨架对齐、贝塞尔滑行模拟，验证全流程数据是否通畅而不触发实际点击。去除 `dry_run=true` 即可直接发布！
