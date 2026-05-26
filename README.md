# Japanese Learning Skills

100 reusable AI skills for Japanese learning, organized for Trae-style `.trae/skills` workflows and general prompt-based learning agents. The library covers beginner kana, vocabulary, grammar, listening, speaking, reading, writing, business Japanese, travel Japanese, JLPT preparation, long-term review, and learning reports.

This project is bilingual by design. Use the Chinese docs if you are a Chinese-speaking learner, and the English docs if you want to adapt the skills for an English-speaking workflow.

## What Is Included

- `100` Japanese learning skills in `.trae/skills/`
- A mirrored `skills/` directory for easier browsing and reuse
- A lightweight Python learning core in `japanese_agent_core.py`
- End-to-end validation scripts for skill structure, prompt quality, and review workflows
- Detailed Chinese and English usage guides, scene-based prompt recipes, and skill catalogs
- Apache-2.0 open source license

## Quick Start

1. Copy or keep the `.trae/skills/` directory in a Trae-compatible workspace.
2. Ask your AI assistant for the scene you want, for example:

```text
我是一名职场人，每天只有午休和通勤时间学日语。
请用 jp-learning-coordinator 帮我制定 4 周计划，
每天调用适合的 skill，重点是商务会话、邮件、敬语和口语纠错。
```

3. Start with one coordinator skill, then let it route to specialist skills:

```text
Use jlpt-coordinator to build a 90-day N3 plan.
For today, combine jlpt-n3-vocab, jlpt-n3-grammar, jlpt-listening,
and jp-vocab-review-deep. Keep the session under 25 minutes.
```

## Documentation

Chinese:

- [中文使用指南](docs/zh-CN/USAGE.md)
- [中文场景手册与 Prompt 示例](docs/zh-CN/SCENARIOS.md)
- [中文 Skill 目录](docs/zh-CN/SKILL_CATALOG.md)

English:

- [English Usage Guide](docs/en/USAGE.md)
- [Scenario Playbook and Prompt Recipes](docs/en/SCENARIOS.md)
- [English Skill Catalog](docs/en/SKILL_CATALOG.md)

## Main Learning Paths

| Path | Start With | Add These Skills |
|------|------------|------------------|
| Absolute beginner | `jp-learning-companion` | `gojuon-daily`, `hiragana-specialist`, `katakana-specialist`, `jp-romaji-transition` |
| Busy working learner | `jp-fragmented-schedule` | `lunch-jp-5min`, `jp-business-conversation`, `jp-email-writing`, `jp-keigo` |
| JLPT preparation | `jlpt-coordinator` | `jlpt-n5-vocab` to `jlpt-n1-vocab`, `jlpt-n5-grammar` to `jlpt-n1-grammar`, `jlpt-listening`, `jlpt-reading` |
| Travel to Japan | `jp-travel-survival` | `jp-travel-conversation`, `jp-restaurant`, `jp-station-transport`, `jp-hotel-stay` |
| Speaking improvement | `jp-speaking-practice` | `jp-role-play`, `jp-small-talk`, `jp-speaking-error-tracker`, `jp-pronunciation-checkin` |
| Reading and writing | `jp-daily-reading` | `jp-graded-reading`, `jp-news-reading`, `jp-diary`, `jp-writing-correction` |

## Test And Validation

Run the validation scripts from the repository root:

```bash
python3 test_all_skills.py
python3 test_deep_skills.py
python3 test_e2e_skills.py
```

Latest local validation before publishing:

- Basic skill and core test: `1111` passed, `0` failed, `1` warning
- Deep prompt chain test: `100/100` skills passed
- Full E2E test: `2214` assertions, `2177` passed, `0` failed, `37` warnings

The warnings are documentation-style signals, mostly missing explicit "Notes" or "Interaction mechanism" headings in otherwise valid skills.

## Repository Layout

```text
.
├── .trae/skills/              # Trae-compatible skill directory
├── skills/                    # Mirror of the skill files for browsing
├── docs/
│   ├── zh-CN/                 # Chinese docs
│   └── en/                    # English docs
├── japanese_agent_core.py     # SQLite profile, event, review, and report helpers
├── test_all_skills.py         # Basic structural and runtime checks
├── test_deep_skills.py        # Prompt chain quality checks
├── test_e2e_skills.py         # Full end-to-end validation
├── LICENSE
└── README.md
```

## License

Apache License 2.0. See [LICENSE](LICENSE).

