/**
 * WeChat Moments Auto Scheduler Skill - Professional Edition
 * Supports AI copywriting generation, cloud syncing (Notion/Feishu), auto-scheduling, and immediate posting.
 */

const { exec } = require('child_process');
const path = require('path');

// Local script locations
const CLI_PATH = 'D:\\weixin\\wechat-moments-auto-v2\\skills\\moments-scheduler\\scripts\\cli.py';
const PYTHON_EXE = 'python'; // Fallback to python in PATH

// McKinsey Trust Copywriting Formula Definitions
const CONTENT_TYPES = {
  professional: {
    name: '专业型',
    formula: '故事案例 + 细节 + 美好结果',
    purpose: '建立权威，展示专业能力',
    outline: '1. 第一段场景化描述问题或咨询案列 (20-25字)\n2. 引入你提供的高质量细节和专业动作\n3. 展示客户得到的美好转变，结尾引导认同互动'
  },
  reliable: {
    name: '靠谱型',
    formula: '失败故事 + 不服输过程 + 成功结果',
    purpose: '建立信任，展示靠谱特质',
    outline: '1. 讲自己曾经真实的踩坑或失败经历\n2. 讲克服困难、坚持原则和死磕的靠谱过程\n3. 拿到好结果后的自我复盘与核心感悟'
  },
  warm: {
    name: '温暖型',
    formula: '生活场景 + 真实互动 + 情感连接',
    purpose: '建立亲密度，展示真实生活',
    outline: '1. 引入极富生活气息的日常场景 (如早餐、亲子、猫咪)\n2. 描述两三句温馨的真实生活细节/段子\n3. 点题人与人之间的温暖连接或价值观'
  },
  altruistic: {
    name: '利他型',
    formula: '事件 + 细节 + 解释 + 价值观/金句',
    purpose: '提供硬核干货，降低防备',
    outline: '1. 讲一件最近学到、看到的高价值干货事件\n2. 掰碎了说明其中的运作机制和使用逻辑\n3. 提炼一句直击心灵的金句，利他分享'
  },
  counter: {
    name: '反认知破圈',
    formula: '打破错误认知 + 植入你的全新理念',
    purpose: '清除行业偏见，重塑心智',
    outline: '1. 先抛出行业内习以为常的毒鸡汤或错误认知，果断打破\n2. 摆事实讲道理，讲出背后的真实本质\n3. 植入你的正确理念和操作心智'
  },
  target: {
    name: '圈用户',
    formula: '筛选目标人群 + 制造稀缺感/门槛',
    purpose: '精准招募，建立客户边界',
    outline: '1. 点名某几类有特定痛点的人群 (如: 正在副业迷茫的程序员)\n2. 讲清这是一次只有少数名额的特别通道/测试服务\n3. 建立加入门槛，发出明确行动指令 (如: 评论区扣1)'
  },
  intro_100: {
    name: '100字自我介绍',
    formula: '深耕[领域][时间] + 踩坑经历 + 价值钩子',
    purpose: '极速破冰，展示长期核心价值',
    outline: '1. 第一句简述你在某垂直领域做到了什么成就\n2. 抛出自己踩过的几个关键大坑来拉近距离\n3. 给出一个无懈可击的利他价值钩子，等待互动'
  },
  story: {
    name: '故事代入型',
    formula: '真实痛点故事 + 戏剧冲突/转折 + 最终解决 + 启发金句',
    purpose: '用极强的故事代入感打破用户防御，塑造深度共鸣',
    outline: '1. 第一段用极具画面感或冲突感的故事悬念切入\n2. 引入转折细节 (例如“直到前天发生了一件事...”)\n3. 讲述依靠专业动作/工具完美解决的过程，结尾升华出启发金句'
  }
};

/**
 * Execute local Python CLI command utility
 */
function runCliCommand(argsString) {
  return new Promise((resolve, reject) => {
    // Force active code page to UTF-8 on Windows command shell to prevent encoding gibberish
    const fullCmd = `chcp 65001 > nul && "${PYTHON_EXE}" "${CLI_PATH}" ${argsString}`;
    
    exec(fullCmd, { encoding: 'utf8' }, (error, stdout, stderr) => {
      if (error) {
        // Fallback check if Python isn't alias-linked
        if (error.message.includes('not found') || error.message.includes('不是内部或外部命令')) {
          return resolve(`❌ 运行失败: 系统找不到 python。请确保 Python 已加入您的系统环境变量 PATH 中。`);
        }
        return resolve(`❌ 运行出错:\n\`\`\`text\n${stderr || error.message}\n\`\`\``);
      }
      resolve(stdout.trim());
    });
  });
}

/**
 * Main command handler
 */
async function momentsWriter(args) {
  const action = args.action || 'generate';

  // 1. GENERATE COPYWRITING ACTION
  if (action === 'generate') {
    const type = args.type;
    const topic = args.topic || '任意主题';

    if (type && CONTENT_TYPES[type]) {
      const info = CONTENT_TYPES[type];
      return `💡 **[系统提示] 麦肯锡信任朋友圈文案设计生成器**

您当前选择的公式是：**${info.name}**
- **核心公式**：\`${info.formula}\`
- **写作目的**：${info.purpose}
- **建议主题**：${topic}

---

👉 **请点击下方复制以下 Prompt，让我（AI）为您生成最专业的朋友圈文案：**

\`\`\`text
请帮我撰写一条专业朋友圈文案。

【文案主题】
${topic}

【公式类型】
${info.name} (公式: ${info.formula})

【结构设计】
${info.outline}

【排版要求】
1. 第一段20-25字以内，极具吸引力，场景化痛点切入。
2. 每段文字不超过3行，段与段之间必须空一行。
3. 结尾用直击灵魂的金句或互动引导（好奇、行动、认同类）。

【语言风格】
- 完全口语化表达，像真实的人在分享，绝对不要AI腔调或过度公关。
- 不要使用任何 # 标签。
- 适当用一些生动的 Emoji 增加活力，但每段不要超过2个。

直接输出文案内容，不要解释。
\`\`\`

*(生成后，你可以使用 \`/moments action=list\` 检查待发送列表，或通过其它后台同步工具将其排队发送！)*`;
    } else {
      // Quick fallback: list available McKinsey formulas or perform local template copy gen
      const typeList = Object.keys(CONTENT_TYPES).map(t => `- \`${t}\`: ${CONTENT_TYPES[t].name} (${CONTENT_TYPES[t].purpose})`).join('\n');
      return `❌ 请选择正确的 \`type\` 参数以生成麦肯锡信任公式朋友圈！

**支持的公式类型 (\`type\`):**
${typeList}

**用法示例:**
\`/moments action=generate type=professional topic=如何高效使用AI智能排版\``;
    }
  }

  // 2. SYNCHRONIZE DATA FROM CLOUD SOURCES
  if (action === 'sync') {
    const source = args.source || 'all';
    const dryRun = args.dry_run ? ' --dry-run' : '';
    
    const output = await runCliCommand(`sync --source ${source}${dryRun}`);
    return `🔄 **数据源同步控制台**
${output}`;
  }

  // 3. SCHEDULE CRON TASKS
  if (action === 'schedule') {
    const scheduleAction = args.schedule_action || 'list';
    const cron = args.cron ? ` --cron "${args.cron}"` : '';
    const dryRun = args.dry_run ? ' --dry-run' : '';

    if (scheduleAction === 'start' && !args.cron) {
      return `❌ 启动定时任务时，请通过 \`cron\` 参数提供 Cron 表达式（例如: cron="0 8 * * *"）`;
    }

    const output = await runCliCommand(`schedule ${scheduleAction}${cron}${dryRun}`);
    return `📅 **定时自动调度控制台**
${output}`;
  }

  // 4. IMMEDIATE GUI SEND
  if (action === 'send') {
    const dryRun = args.dry_run ? ' --dry-run' : '';
    
    const output = await runCliCommand(`send${dryRun}`);
    return `🚀 **朋友圈发布控制台**
${output}`;
  }

  // 5. LIST SENDING QUEUE & RECENT LOGS
  if (action === 'list') {
    const limit = args.limit || 10;
    
    // We fetch pending items first, then summarize
    const output = await runCliCommand(`list --limit ${limit}`);
    const statusOutput = await runCliCommand(`status`);
    
    return `📊 **发稿池待发队列及状态总览**

\`\`\`text
${statusOutput}
\`\`\`

**待发送朋友圈明细 (最大 ${limit} 条):**
${output}`;
  }

  return `❌ 未知指令: ${action}`;
}

module.exports = { momentsWriter, CONTENT_TYPES };
