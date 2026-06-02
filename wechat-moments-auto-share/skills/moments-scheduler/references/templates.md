---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5316da29121965ff3a210e6dce425447_bb81d1755e2511f1bd025254006c9bbf
    ReservedCode1: /pkTRUFxAkjF45CE3nZNoNYAkGl3sFAx2brN7QVDvuI37o3sjqwgJXVhBzvYlVfw+H6k2yNHE/vnqOtVz+r84zjkGeno0uQfh9XND+ig9Xy3ZzHoXjP9Zfqu6nDeYZ1Y1aq2J/8OgorE84kuWIhc4SDbWkAYmnWLnHdn/aYpdbPX3WWpNyw2icg+LDc=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5316da29121965ff3a210e6dce425447_bb81d1755e2511f1bd025254006c9bbf
    ReservedCode2: /pkTRUFxAkjF45CE3nZNoNYAkGl3sFAx2brN7QVDvuI37o3sjqwgJXVhBzvYlVfw+H6k2yNHE/vnqOtVz+r84zjkGeno0uQfh9XND+ig9Xy3ZzHoXjP9Zfqu6nDeYZ1Y1aq2J/8OgorE84kuWIhc4SDbWkAYmnWLnHdn/aYpdbPX3WWpNyw2icg+LDc=
---

# 朋友圈文案模板参考

## 分类说明

| 分类 | 说明 | 适用时段 |
|------|------|----------|
| morning | 早安正能量 | 5:00-12:00 |
| noon | 中午日常 | 12:00-14:00 |
| evening | 傍晚放松 | 14:00-18:00 |
| night | 晚安治愈 | 18:00-5:00 |
| motivation | 励志语录 | 全天 |
| life | 生活感悟 | 全天 |
| work | 工作日常 | 工作日 |
| reflection | 人生感悟 | 全天 |
| humor | 幽默搞笑 | 全天 |

## 风格说明

| 风格 | 特点 | 示例 |
|------|------|------|
| normal | 自然亲切，像日常分享 | "今天天气真好，心情也跟着好起来" |
| humor | 幽默自嘲，带网络流行语 | "今日状态：人还在，魂已飞" |
| literary | 文艺清新，带哲理 | "岁月静好，现世安稳" |
| short | 简短有力，一句话金句 | "生活明朗，万物可爱" |

## LLM 生成提示词模板

当需要 LLM 增强生成时，使用以下提示词结构：

```
请生成一条中文朋友圈文案，主题是「{分类}」，风格：{风格描述}。
要求：
- 长度15-50字
- 口语化，接地气，不要像AI写的
- 适合配图发朋友圈
- 可以适当使用网络流行语
- 只输出文案本身，不要任何解释或引号
- 不带 # 标签
```

## 最佳实践

1. **频次控制**: 一天1-2条为佳，不宜超过3条
2. **时段选择**: 
   - 早上 7:30-8:30（通勤/早餐时间）
   - 中午 12:00-13:00（午餐/午休时间）
   - 晚上 18:00-20:00（下班/晚饭时间）
   - 晚上 21:00-22:00（睡前放松时间）
3. **文案搭配**: 图文配合效果更佳，图片建议提前放入 images 目录
4. **内容多样性**: 避免连续发同一分类的文案，保持内容多元

## 定时调度 cron 表达式参考

| 需求 | cron 表达式 |
|------|-------------|
| 每天早上 8:00 | 0 8 * * * |
| 每天中午 12:00 | 0 12 * * * |
| 每天晚上 20:00 | 0 20 * * * |
| 工作日早上 8:00 | 0 8 * * 1-5 |
| 每隔 2 小时 | 0 */2 * * * |
| 每周一早上 8:00 | 0 8 * * 1 |
*（内容由AI生成，仅供参考）*
