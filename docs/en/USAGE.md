# English Usage Guide

This repository is a modular AI skill library for learning Japanese. It is not a linear textbook. It is a team of 100 reusable learning agents: coordinators, kana trainers, vocabulary coaches, grammar specialists, speaking partners, writing correctors, travel coaches, business Japanese coaches, and JLPT planners.

## Who This Is For

- Absolute beginners who need kana, pronunciation, basic words, and simple sentence patterns.
- Busy professionals who need a realistic plan around commute, lunch breaks, and evenings.
- JLPT learners preparing for N5 through N1.
- Travelers who need restaurant, station, hotel, convenience store, and phone-call Japanese.
- Business learners who need meetings, email, phone calls, honorifics, interviews, and client communication.
- Intermediate and advanced learners who want news reading, writing correction, retelling, and natural expression practice.

## Installation

For Trae-style skill workflows, keep or copy `.trae/skills/` into the workspace root. Each skill lives in its own directory with a `SKILL.md` file.

The repository also includes a mirrored `skills/` directory for easier browsing and reuse. The two directories are validated to contain identical skill files.

## Basic Invocation

Call a skill by name:

```text
Use jp-restaurant to train me to order ramen in Japanese.
My level is N5. Ask me step by step and wait for my answers.
Do not give the whole dialogue at once.
```

Or start with a coordinator:

```text
Use jp-learning-coordinator.
My goal is to handle travel and basic workplace communication in Japanese within 6 months.
I can study 20 minutes per day. Build this week's plan and specify which skills to use each day.
```

## Recommended Learning Loop

A good session should not stop at explanation. Use this loop:

1. Read the learner profile: goal, level, time budget, weak points, and interests.
2. Review a few due items.
3. Teach a small new item.
4. Ask the learner to answer, make a sentence, shadow, choose, or retell.
5. Correct mistakes and explain why.
6. Add weak points to the review queue.
7. Summarize and schedule the next review.

Reusable prompt:

```text
Make this session a closed learning loop:
review 3 previous weak points, teach 1 new item,
give me 2 interactive tasks, wait for my answer,
then correct my output and schedule the next review.
My level is N4 and I only have 15 minutes today.
```

## Choosing The Right Skill

| Goal | Start With |
|------|------------|
| I need a full plan | `jp-learning-coordinator` |
| I want a long-term coach | `jp-learning-companion` |
| I only have fragmented time | `jp-fragmented-schedule` |
| I am preparing for JLPT | `jlpt-coordinator` |
| I am traveling to Japan | `jp-travel-survival` |
| I want to improve speaking | `jp-speaking-practice` |
| I want to fix recurring mistakes | `jp-common-mistake` or `jp-grammar-error-tracker` |
| I need Japanese email writing | `jp-email-writing` |
| I need business Japanese | `jp-business-conversation` |

## Data And Review Core

`japanese_agent_core.py` provides a lightweight SQLite learning core:

- User profile: level, goal, daily minutes, interests, weak points
- Learning events: activity, result, score
- Review items: item, reading, meaning, example, due time
- SM2-style spaced repetition update
- Daily plan generation
- Weekly report aggregation

Run validation:

```bash
python3 test_all_skills.py
python3 test_deep_skills.py
python3 test_e2e_skills.py
```

## Practical Advice

- Learn only 1 to 3 new items per session.
- Always produce something: a sentence, a spoken attempt, a retelling, or a choice answer.
- Ask for both "why it is wrong" and "a more natural version" when correcting.
- Do not use the same rhythm for work, travel, and exam goals.
- Run `jp-learning-report` weekly so the system does not become endless input without review.

