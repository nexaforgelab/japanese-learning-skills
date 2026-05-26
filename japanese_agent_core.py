import sqlite3
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).parent / "japanese_agent.db"


def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def now():
    return datetime.utcnow().isoformat()


def init_db():
    db = conn()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        user_id TEXT PRIMARY KEY,
        level TEXT DEFAULT 'N5',
        goal TEXT DEFAULT '',
        daily_minutes INTEGER DEFAULT 10,
        interests TEXT DEFAULT '[]',
        weak_points TEXT DEFAULT '[]',
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        agent_name TEXT,
        event_type TEXT,
        content TEXT,
        result TEXT,
        score REAL,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS review_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        agent_name TEXT,
        item_type TEXT,
        item TEXT,
        reading TEXT,
        meaning TEXT,
        example TEXT,
        difficulty INTEGER DEFAULT 2,
        interval_days INTEGER DEFAULT 1,
        ease_factor REAL DEFAULT 2.5,
        repetitions INTEGER DEFAULT 0,
        next_review_at TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    db.commit()
    db.close()


def upsert_profile(
    user_id: str,
    level: str = "N5",
    goal: str = "",
    daily_minutes: int = 10,
    interests: Optional[List[str]] = None,
    weak_points: Optional[List[str]] = None
):
    interests = interests or []
    weak_points = weak_points or []

    db = conn()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO user_profile
    (user_id, level, goal, daily_minutes, interests, weak_points, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        level=excluded.level,
        goal=excluded.goal,
        daily_minutes=excluded.daily_minutes,
        interests=excluded.interests,
        weak_points=excluded.weak_points,
        updated_at=excluded.updated_at
    """, (
        user_id,
        level,
        goal,
        daily_minutes,
        json.dumps(interests, ensure_ascii=False),
        json.dumps(weak_points, ensure_ascii=False),
        now(),
        now()
    ))

    db.commit()
    db.close()


def get_profile(user_id: str) -> Dict[str, Any]:
    db = conn()
    row = db.execute(
        "SELECT * FROM user_profile WHERE user_id=?",
        (user_id,)
    ).fetchone()
    db.close()

    if not row:
        return {
            "user_id": user_id,
            "level": "N5",
            "goal": "",
            "daily_minutes": 10,
            "interests": [],
            "weak_points": []
        }

    return {
        "user_id": row["user_id"],
        "level": row["level"],
        "goal": row["goal"],
        "daily_minutes": row["daily_minutes"],
        "interests": json.loads(row["interests"] or "[]"),
        "weak_points": json.loads(row["weak_points"] or "[]")
    }


def log_event(
    user_id: str,
    agent_name: str,
    event_type: str,
    content: str,
    result: str = "",
    score: Optional[float] = None
):
    db = conn()
    db.execute("""
    INSERT INTO learning_events
    (user_id, agent_name, event_type, content, result, score, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, agent_name, event_type, content, result, score, now()))
    db.commit()
    db.close()


def add_review_item(
    user_id: str,
    agent_name: str,
    item_type: str,
    item: str,
    reading: str = "",
    meaning: str = "",
    example: str = "",
    difficulty: int = 2
):
    db = conn()
    next_review = datetime.utcnow() + timedelta(days=1)
    db.execute("""
    INSERT INTO review_items
    (user_id, agent_name, item_type, item, reading, meaning, example, difficulty,
     interval_days, ease_factor, repetitions, next_review_at, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        agent_name,
        item_type,
        item,
        reading,
        meaning,
        example,
        difficulty,
        1,
        2.5,
        0,
        next_review.isoformat(),
        now(),
        now()
    ))
    db.commit()
    db.close()


def get_due_reviews(user_id: str, agent_name: Optional[str] = None, limit: int = 10):
    db = conn()

    if agent_name:
        rows = db.execute("""
        SELECT * FROM review_items
        WHERE user_id=? AND agent_name=? AND next_review_at<=?
        ORDER BY next_review_at ASC
        LIMIT ?
        """, (user_id, agent_name, now(), limit)).fetchall()
    else:
        rows = db.execute("""
        SELECT * FROM review_items
        WHERE user_id=? AND next_review_at<=?
        ORDER BY next_review_at ASC
        LIMIT ?
        """, (user_id, now(), limit)).fetchall()

    db.close()
    return [dict(r) for r in rows]


def sm2_update(review_id: int, quality: int):
    quality = max(0, min(5, quality))

    db = conn()
    row = db.execute(
        "SELECT * FROM review_items WHERE id=?",
        (review_id,)
    ).fetchone()

    if not row:
        db.close()
        return

    ease = row["ease_factor"]
    interval = row["interval_days"]
    reps = row["repetitions"]

    if quality < 3:
        reps = 0
        interval = 1
    else:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        else:
            interval = math.ceil(interval * ease)

        reps += 1
        ease = ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        ease = max(1.3, ease)

    next_review = datetime.utcnow() + timedelta(days=interval)

    db.execute("""
    UPDATE review_items
    SET interval_days=?, ease_factor=?, repetitions=?, next_review_at=?, updated_at=?
    WHERE id=?
    """, (
        interval,
        ease,
        reps,
        next_review.isoformat(),
        now(),
        review_id
    ))

    db.commit()
    db.close()


def generate_daily_plan(profile: Dict[str, Any]) -> Dict[str, Any]:
    level = profile.get("level", "N5")
    daily_minutes = profile.get("daily_minutes", 10)

    if daily_minutes <= 5:
        tasks = ["复习", "一句口语输出"]
    elif daily_minutes <= 15:
        tasks = ["复习", "新知识", "小测"]
    else:
        tasks = ["复习", "新知识", "听力/口语", "输出练习"]

    return {
        "level": level,
        "daily_minutes": daily_minutes,
        "tasks": tasks,
        "created_at": now()
    }


def weekly_report(user_id: str):
    since = datetime.utcnow() - timedelta(days=7)
    db = conn()
    rows = db.execute("""
    SELECT * FROM learning_events
    WHERE user_id=? AND created_at>=?
    """, (user_id, since.isoformat())).fetchall()
    db.close()

    total = len(rows)
    scores = [r["score"] for r in rows if r["score"] is not None]
    avg_score = sum(scores) / len(scores) if scores else None

    event_count = {}
    for r in rows:
        event_count[r["event_type"]] = event_count.get(r["event_type"], 0) + 1

    return {
        "total_events": total,
        "average_score": avg_score,
        "event_count": event_count,
        "suggestion": "如果输出练习较少，下周增加造句、朗读、角色扮演。"
    }


if __name__ == "__main__":
    init_db()
    upsert_profile(
        user_id="demo",
        level="N5",
        goal="3个月掌握基础日语会话",
        daily_minutes=15,
        interests=["动漫", "旅行", "职场"]
    )
    print(generate_daily_plan(get_profile("demo")))
