# 中文场景手册与 Prompt 示例

下面的场景可以直接复制给你的 AI 助手。建议先用场景 prompt 启动，再根据当天反馈调用更细的 skill。

## 场景 1：职场人每天 20 分钟学日语

适合：上班忙、晚上容易累、需要长期稳定进步的人。

推荐 skill：

- `jp-fragmented-schedule`
- `lunch-jp-5min`
- `jp-business-conversation`
- `jp-email-writing`
- `jp-keigo`
- `jp-speaking-error-tracker`
- `bedtime-jp-review`

学习节奏：

| 时间 | 内容 | Skill |
|------|------|-------|
| 通勤 5 分钟 | 听 1 句、跟读 2 次 | `jp-pronunciation-checkin` |
| 午休 5 分钟 | 一个微任务 | `lunch-jp-5min` |
| 下班后 10 分钟 | 商务场景对话或邮件 | `jp-business-conversation` / `jp-email-writing` |
| 睡前 3 分钟 | 复习错句 | `bedtime-jp-review` |

启动 prompt：

```text
请使用 jp-fragmented-schedule。
我是一名职场人，平时很忙，每天最多 20 分钟学日语。
目标是 6 个月内能做基础职场沟通：邮件、会议寒暄、电话确认、简单汇报。
请把我的时间拆成通勤、午休、下班后、睡前四段，
安排 4 周计划，并说明每天调用哪些 skill。
每次学习都要有：复习、一个新表达、一次输出、纠错、下次复习。
```

日常练习 prompt：

```text
今天按职场日语路线训练。
请调用 jp-business-conversation，场景是会议开始前的寒暄和确认议程。
我的水平是 N4，请先给 5 个关键词，再和我角色扮演。
每次只问一句，等我回答后再纠错。
```

邮件专项 prompt：

```text
请调用 jp-email-writing。
我需要写一封日语邮件：向客户确认下周三 15:00 的线上会议。
请给我简洁版和正式版，标出敬语表达。
然后让我仿写一封，你再帮我纠错。
```

## 场景 2：零基础从五十音开始

适合：完全不会假名、还依赖罗马音的人。

推荐 skill：

- `gojuon-daily`
- `hiragana-specialist`
- `katakana-specialist`
- `voiced-unvoiced`
- `yoon-specialist`
- `long-double-sound`
- `jp-romaji-transition`
- `jp-kana-dictation`

4 周路线：

| 周 | 重点 | Skill |
|----|------|-------|
| 第 1 周 | 平假名认读与默写 | `hiragana-specialist`, `gojuon-daily` |
| 第 2 周 | 片假名和外来语 | `katakana-specialist`, `jp-gairaigo` |
| 第 3 周 | 浊音、半浊音、拗音 | `voiced-unvoiced`, `yoon-specialist` |
| 第 4 周 | 长音、促音、拨音、听写 | `long-double-sound`, `jp-kana-dictation` |

启动 prompt：

```text
请使用 gojuon-daily。
我是零基础，想 4 周掌握五十音。
请从あ行开始，每天只学少量假名。
每次包含认读、手写记忆、听辨、默写和复习安排。
不要让我依赖罗马音，第三天开始逐步减少罗马音提示。
```

## 场景 3：90 天 JLPT 备考

适合：目标明确、需要考试倒排计划的人。

推荐 skill：

- `jlpt-coordinator`
- 对应等级词汇：`jlpt-n5-vocab` 到 `jlpt-n1-vocab`
- 对应等级语法：`jlpt-n5-grammar` 到 `jlpt-n1-grammar`
- `jlpt-listening`
- `jlpt-reading`
- `jp-vocab-review-deep`
- `jp-grammar-error-tracker`

启动 prompt：

```text
请使用 jlpt-coordinator。
我的目标是 90 天后参加 JLPT N3。
现在大约 N4，工作日每天 30 分钟，周末每天 90 分钟。
请给我倒排计划，分成基础补齐、题型训练、冲刺复盘三阶段。
每天明确调用哪些 skill，并安排词汇、语法、听力、阅读和错题复习比例。
```

每日 prompt：

```text
今天执行 JLPT N3 第 2 周第 3 天计划。
请组合 jlpt-n3-vocab、jlpt-n3-grammar、jlpt-listening 和 jp-vocab-review-deep。
控制在 30 分钟内，先复习错词，再学新内容，最后做 5 题小测。
我回答后请分析错因并更新明天复习重点。
```

## 场景 4：赴日前旅行生存日语

适合：短期出行、希望能解决真实问题的人。

推荐 skill：

- `jp-travel-survival`
- `jp-travel-conversation`
- `jp-convenience-store`
- `jp-restaurant`
- `jp-station-transport`
- `jp-hotel-stay`
- `jp-phone-call`

7 天路线：

| 天 | 场景 |
|----|------|
| Day 1 | 机场、入境、问路 |
| Day 2 | 便利店和付款 |
| Day 3 | 餐厅点餐和忌口 |
| Day 4 | 车站、换乘、买票 |
| Day 5 | 酒店入住和寄存行李 |
| Day 6 | 电话预约和改时间 |
| Day 7 | 综合角色扮演 |

启动 prompt：

```text
请使用 jp-travel-survival。
我 14 天后去日本旅行，日语 N5，目标是能在便利店、餐厅、车站、酒店解决问题。
请给我 7 天速成计划。
每天只教最必要的表达，并安排角色扮演。
遇到我说错时，请给更自然但仍然简单的说法。
```

餐厅 prompt：

```text
请调用 jp-restaurant。
场景：我在居酒屋，两个人，想点饮料、三道菜，最后分开付款。
请你扮演店员，一次只说一句日语。
我回答后请纠正数量、助词和礼貌度。
```

## 场景 5：想把动漫兴趣变成日语学习

适合：喜欢动漫，但不想只记台词的人。

推荐 skill：

- `jp-anime-learning`
- `daily-natural-jp`
- `jp-small-talk`
- `jp-formal-casual`
- `jp-retell-training`
- `jp-speaking-practice`

启动 prompt：

```text
请使用 jp-anime-learning。
我喜欢动漫，想通过自然对话学习日语，但不要使用真实作品台词。
请生成一段原创动漫风格短对话，难度 N4。
先解释口语表达，再让我复述，然后把台词改成现实生活中也自然的说法。
```

## 场景 6：商务日语与求职面试

适合：准备日企、赴日工作、客户沟通的人。

推荐 skill：

- `jp-business-conversation`
- `jp-email-writing`
- `jp-keigo`
- `jp-phone-call`
- `jp-interview`
- `jp-formal-casual`

启动 prompt：

```text
请使用 jp-interview。
我准备日语求职面试，目标岗位是软件工程师。
请先模拟 5 个常见问题：自我介绍、项目经验、离职原因、强项弱项、未来规划。
每次只问一个问题，等我用日语回答后，
请从语法、自然度、敬语、内容结构四个维度评分并改写。
```

## 场景 7：听力和口语突破

适合：看得懂但听不懂、想开口但容易卡住的人。

推荐 skill：

- `jp-daily-listening`
- `jp-extensive-listening`
- `jp-listening-distinguish`
- `jp-speaking-practice`
- `jp-role-play`
- `jp-retell-training`
- `jp-speaking-error-tracker`

启动 prompt：

```text
请使用 jp-daily-listening 和 jp-retell-training。
我的问题是看得懂但听不懂，也说不出来。
请给我一段 N4 难度短音频脚本式材料：
第一遍只让我听关键词，第二遍让我复述大意。
我复述后，请纠正表达，并把我的错误加入口语错误追踪。
```

## 场景 8：中高级阅读和写作提升

适合：N3 以上，想读新闻、写文章、提高自然度的人。

推荐 skill：

- `jp-news-reading`
- `jp-sentence-structure`
- `jp-writing-correction`
- `jp-diary`
- `jp-keigo`
- `jp-learning-report`

启动 prompt：

```text
请使用 jp-news-reading。
我的水平是 N2，想训练新闻阅读和观点表达。
请给我一篇短新闻风格材料，标出 3 个关键词和 2 个长句结构。
读完后问我 3 个理解题，再让我用日语写 3 句观点。
最后请调用 jp-writing-correction 纠正我的表达。
```

## 场景 9：错误复盘和长期保持

适合：学过很多但总是重复犯错的人。

推荐 skill：

- `jp-common-mistake`
- `jp-grammar-error-tracker`
- `jp-speaking-error-tracker`
- `jp-wrong-word-recovery`
- `jp-vocab-review-deep`
- `jp-learning-report`

启动 prompt：

```text
请使用 jp-learning-report 和 jp-grammar-error-tracker。
这是我本周常错内容：は/が、に/で、动词て形、敬语邮件结尾。
请帮我归类错误，找出最高频的 3 个问题。
然后安排下周每天 15 分钟的纠错计划，
每一天都要有复习、专项练习、造句、反馈和下次复习。
```

