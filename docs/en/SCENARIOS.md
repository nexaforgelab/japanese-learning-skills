# Scenario Playbook And Prompt Recipes

Copy these prompts into your AI assistant and adjust the level, time budget, and goal. Start with a scenario prompt, then route into specialist skills as needed.

## Scenario 1: Busy Professional, 20 Minutes Per Day

Best for learners with a full-time job who need a realistic plan and workplace Japanese.

Recommended skills:

- `jp-fragmented-schedule`
- `lunch-jp-5min`
- `jp-business-conversation`
- `jp-email-writing`
- `jp-keigo`
- `jp-speaking-error-tracker`
- `bedtime-jp-review`

Daily rhythm:

| Time | Task | Skill |
|------|------|-------|
| Commute, 5 min | Listen and shadow one sentence | `jp-pronunciation-checkin` |
| Lunch, 5 min | One micro-task | `lunch-jp-5min` |
| After work, 10 min | Business dialogue or email | `jp-business-conversation` / `jp-email-writing` |
| Bedtime, 3 min | Review weak sentences | `bedtime-jp-review` |

Starter prompt:

```text
Use jp-fragmented-schedule.
I am a busy professional and can study Japanese for at most 20 minutes per day.
My goal is basic workplace communication within 6 months:
email, meeting small talk, phone confirmation, and simple reporting.
Split my study time into commute, lunch break, after work, and bedtime.
Build a 4-week plan and tell me which skills to use each day.
Every session must include review, one new expression, output, correction, and next review.
```

Daily practice prompt:

```text
Use jp-business-conversation for today's workplace Japanese session.
The scene is small talk before a meeting and confirming the agenda.
My level is N4. Give me 5 keywords, then role-play with me.
Ask only one line at a time and wait for my answer before correcting me.
```

Email prompt:

```text
Use jp-email-writing.
I need to write a Japanese email confirming an online meeting with a client next Wednesday at 15:00.
Give me a concise version and a formal version, and mark the honorific expressions.
Then ask me to write my own version and correct it.
```

## Scenario 2: Absolute Beginner Starting With Kana

Best for learners who cannot read kana yet or still rely on romaji.

Recommended skills:

- `gojuon-daily`
- `hiragana-specialist`
- `katakana-specialist`
- `voiced-unvoiced`
- `yoon-specialist`
- `long-double-sound`
- `jp-romaji-transition`
- `jp-kana-dictation`

Four-week path:

| Week | Focus | Skills |
|------|-------|--------|
| Week 1 | Hiragana recognition and writing | `hiragana-specialist`, `gojuon-daily` |
| Week 2 | Katakana and loanwords | `katakana-specialist`, `jp-gairaigo` |
| Week 3 | Voiced sounds and contracted sounds | `voiced-unvoiced`, `yoon-specialist` |
| Week 4 | Long vowels, double consonants, nasal sounds, dictation | `long-double-sound`, `jp-kana-dictation` |

Starter prompt:

```text
Use gojuon-daily.
I am an absolute beginner and want to master kana in 4 weeks.
Start with the あ row and teach only a small amount each day.
Each session should include recognition, writing memory, listening distinction, dictation, and review scheduling.
Do not let me depend on romaji. Start reducing romaji hints from day 3.
```

## Scenario 3: 90-Day JLPT Sprint

Best for learners with a clear exam date.

Recommended skills:

- `jlpt-coordinator`
- Level-specific vocabulary: `jlpt-n5-vocab` through `jlpt-n1-vocab`
- Level-specific grammar: `jlpt-n5-grammar` through `jlpt-n1-grammar`
- `jlpt-listening`
- `jlpt-reading`
- `jp-vocab-review-deep`
- `jp-grammar-error-tracker`

Starter prompt:

```text
Use jlpt-coordinator.
I will take JLPT N3 in 90 days.
I am currently around N4. I can study 30 minutes on weekdays and 90 minutes on weekends.
Build a backward plan with three phases: foundation repair, question-type training, and final review.
Specify which skills to use each day and how to divide vocabulary, grammar, listening, reading, and mistake review.
```

Daily prompt:

```text
Execute JLPT N3 week 2 day 3.
Combine jlpt-n3-vocab, jlpt-n3-grammar, jlpt-listening, and jp-vocab-review-deep.
Keep it under 30 minutes. Review wrong words first, teach new content, then give me a 5-question mini test.
After I answer, analyze mistakes and update tomorrow's review focus.
```

## Scenario 4: Survival Japanese Before Traveling To Japan

Best for short-term travel preparation.

Recommended skills:

- `jp-travel-survival`
- `jp-travel-conversation`
- `jp-convenience-store`
- `jp-restaurant`
- `jp-station-transport`
- `jp-hotel-stay`
- `jp-phone-call`

Seven-day path:

| Day | Scene |
|-----|-------|
| Day 1 | Airport, immigration, directions |
| Day 2 | Convenience store and payment |
| Day 3 | Restaurants and dietary restrictions |
| Day 4 | Stations, transfers, tickets |
| Day 5 | Hotel check-in and luggage storage |
| Day 6 | Phone reservations and schedule changes |
| Day 7 | Integrated role-play |

Starter prompt:

```text
Use jp-travel-survival.
I will travel to Japan in 14 days. My Japanese level is N5.
I need to handle convenience stores, restaurants, train stations, and hotels.
Build a 7-day crash plan.
Teach only the most necessary expressions each day and include role-play.
When I make mistakes, give me a more natural but still simple version.
```

Restaurant prompt:

```text
Use jp-restaurant.
Scene: I am at an izakaya with one friend. I want to order drinks, three dishes, and pay separately.
You are the staff. Say only one Japanese line at a time.
After I answer, correct quantity expressions, particles, and politeness.
```

## Scenario 5: Learning Through Anime-Style Dialogue

Best for learners who enjoy anime but want transferable Japanese, not memorized lines.

Recommended skills:

- `jp-anime-learning`
- `daily-natural-jp`
- `jp-small-talk`
- `jp-formal-casual`
- `jp-retell-training`
- `jp-speaking-practice`

Starter prompt:

```text
Use jp-anime-learning.
I like anime and want to learn natural Japanese through dialogue, but do not use real copyrighted lines.
Create an original anime-style short dialogue at N4 level.
Explain the spoken expressions, ask me to retell it, then rewrite the dialogue into natural real-life Japanese.
```

## Scenario 6: Business Japanese And Interviews

Best for learners preparing for Japanese companies, work in Japan, or client communication.

Recommended skills:

- `jp-business-conversation`
- `jp-email-writing`
- `jp-keigo`
- `jp-phone-call`
- `jp-interview`
- `jp-formal-casual`

Starter prompt:

```text
Use jp-interview.
I am preparing for a Japanese job interview for a software engineer role.
Simulate 5 common questions: self-introduction, project experience, reason for changing jobs, strengths and weaknesses, and future goals.
Ask only one question at a time. After I answer in Japanese,
score grammar, naturalness, honorifics, and answer structure, then rewrite my answer.
```

## Scenario 7: Listening And Speaking Breakthrough

Best for learners who can read but cannot hear or speak smoothly.

Recommended skills:

- `jp-daily-listening`
- `jp-extensive-listening`
- `jp-listening-distinguish`
- `jp-speaking-practice`
- `jp-role-play`
- `jp-retell-training`
- `jp-speaking-error-tracker`

Starter prompt:

```text
Use jp-daily-listening and jp-retell-training.
My problem is that I can read Japanese but cannot understand spoken Japanese or respond smoothly.
Give me a short N4-level listening script:
first ask me to catch keywords, then ask me to retell the main idea.
After I retell it, correct my expression and add my mistakes to speaking error tracking.
```

## Scenario 8: Intermediate And Advanced Reading/Writing

Best for N3+ learners who want news reading, opinion output, and natural writing.

Recommended skills:

- `jp-news-reading`
- `jp-sentence-structure`
- `jp-writing-correction`
- `jp-diary`
- `jp-keigo`
- `jp-learning-report`

Starter prompt:

```text
Use jp-news-reading.
My level is N2 and I want to train news reading and opinion expression.
Give me a short news-style passage, mark 3 keywords and 2 long sentence structures.
After I read it, ask 3 comprehension questions, then ask me to write 3 Japanese opinion sentences.
Finally use jp-writing-correction to correct my output.
```

## Scenario 9: Mistake Review And Long-Term Retention

Best for learners who know a lot but repeat the same mistakes.

Recommended skills:

- `jp-common-mistake`
- `jp-grammar-error-tracker`
- `jp-speaking-error-tracker`
- `jp-wrong-word-recovery`
- `jp-vocab-review-deep`
- `jp-learning-report`

Starter prompt:

```text
Use jp-learning-report and jp-grammar-error-tracker.
These are my frequent mistakes this week: は/が, に/で, verb te-form, and email closing honorifics.
Classify the errors and identify the top 3 recurring problems.
Then build a 15-minute-per-day correction plan for next week.
Each day must include review, focused practice, sentence making, feedback, and next review.
```

