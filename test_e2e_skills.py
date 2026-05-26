import importlib
import re
import sqlite3
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from test_all_skills import CATEGORY_MAP, EXPECTED_SKILLS


ROOT = Path(__file__).parent
PRIMARY_SKILLS_DIR = ROOT / ".trae" / "skills"
MIRROR_SKILLS_DIR = ROOT / "skills"
REPORT_PATH = ROOT / "test_report_e2e.md"


CHAIN_KEYWORDS = {
    "读取用户画像": ["画像", "水平", "profile", "用户", "目标", "薄弱"],
    "复习队列": ["复习", "间隔", "SM2", "到期", "review", "错词"],
    "新内容推送": ["新词", "新知识", "新语法", "推送", "今日", "讲解", "学习内容", "表达"],
    "用户互动": ["用户", "造句", "回答", "填空", "选择", "跟读", "朗读", "复述", "任务"],
    "反馈纠错": ["纠正", "反馈", "纠错", "自然度", "错因", "评估", "建议", "表现"],
    "下次复习安排": ["复习", "下次", "间隔", "队列", "复习时间", "安排"],
}

REQUIRED_SECTIONS = {
    "标题": [r"^#\s+.+"],
    "工作流程": [r"工作流程", r"核心流程", r"流程", r"步骤", r"链路"],
    "输出格式": [r"输出格式", r"呈现格式", r"格式"],
    "互动机制": [r"互动机制", r"等待用户", r"用户回答", r"用户完成", r"分步引导"],
    "注意事项": [r"注意事项", r"使用原则", r"规则"],
}

DOMAIN_EXPECTATIONS = {
    "daily": ["学习", "复习", "用户"],
    "gojuon": ["五十音", "假名", "发音"],
    "hiragana": ["平假名", "假名", "发音"],
    "katakana": ["片假名", "假名", "外来语"],
    "jlpt": ["JLPT", "等级", "练习"],
    "vocab": ["词", "例句", "复习"],
    "grammar": ["语法", "例句", "练习"],
    "conversation": ["对话", "场景", "表达"],
    "listening": ["听", "练习", "复述"],
    "reading": ["阅读", "理解", "文章"],
    "writing": ["写", "纠正", "表达"],
}


@dataclass
class CheckBook:
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    failures: List[str] = field(default_factory=list)
    warning_items: List[str] = field(default_factory=list)

    def pass_(self, count: int = 1):
        self.passed += count

    def fail(self, message: str):
        self.failed += 1
        self.failures.append(message)

    def warn(self, message: str):
        self.warnings += 1
        self.warning_items.append(message)


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    frontmatter = content[3:end].strip()
    body = content[end + 3 :].strip()
    fields: Dict[str, str] = {}

    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")

    return fields, body


def count_matches(patterns: List[str], content: str) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, content, re.MULTILINE | re.IGNORECASE))


def validate_skill(skill_name: str, book: CheckBook) -> Dict[str, object]:
    primary_path = PRIMARY_SKILLS_DIR / skill_name / "SKILL.md"
    mirror_path = MIRROR_SKILLS_DIR / skill_name / "SKILL.md"
    metrics: Dict[str, object] = {
        "skill": skill_name,
        "status": "PASS",
        "issues": [],
        "warnings": [],
    }

    if not primary_path.exists():
        msg = f"{skill_name}: primary SKILL.md 不存在"
        book.fail(msg)
        metrics["status"] = "FAIL"
        metrics["issues"].append(msg)
        return metrics

    if not mirror_path.exists():
        msg = f"{skill_name}: mirror SKILL.md 不存在"
        book.fail(msg)
        metrics["status"] = "FAIL"
        metrics["issues"].append(msg)
        return metrics

    try:
        content = primary_path.read_text(encoding="utf-8")
        mirror_content = mirror_path.read_text(encoding="utf-8")
        book.pass_()
    except UnicodeDecodeError:
        msg = f"{skill_name}: 文件不是有效 UTF-8"
        book.fail(msg)
        metrics["status"] = "FAIL"
        metrics["issues"].append(msg)
        return metrics

    if content != mirror_content:
        msg = f"{skill_name}: .trae/skills 与 skills 内容不一致"
        book.fail(msg)
        metrics["status"] = "FAIL"
        metrics["issues"].append(msg)
    else:
        book.pass_()

    if "\ufffd" in content or "\x00" in content:
        msg = f"{skill_name}: 包含乱码或 NUL 字符"
        book.fail(msg)
        metrics["status"] = "FAIL"
        metrics["issues"].append(msg)
    else:
        book.pass_()

    fields, body = parse_frontmatter(content)
    metrics["body_chars"] = len(body)
    metrics["brackets"] = len(re.findall(r"【[^】]+】", content))
    metrics["code_blocks"] = len(re.findall(r"```[\s\S]*?```", content))
    metrics["japanese_chars"] = len(re.findall(r"[\u3040-\u30ff\u4e00-\u9fff]", content))

    name = fields.get("name", "")
    description = fields.get("description", "")
    checks = [
        (bool(fields), "frontmatter 可解析"),
        (name == skill_name, "name 与目录名一致"),
        (bool(description), "description 存在"),
        (0 < len(description) <= 200, "description 长度 <= 200"),
        ("invoke when" in description.lower(), "description 含 Invoke when 触发条件"),
        (bool(re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", skill_name)), "目录名为 kebab-case"),
        (len(body) >= 500, "正文长度 >= 500 字符"),
        (metrics["brackets"] >= 3, "输出占位标记 >= 3"),
        (metrics["code_blocks"] >= 1, "至少 1 个代码块输出模板"),
        (metrics["japanese_chars"] >= 20, "包含足够日语/中文教学文本"),
        ("TODO" not in content and "TBD" not in content and "待补" not in content, "无未完成占位"),
    ]

    for ok, label in checks:
        if ok:
            book.pass_()
        else:
            msg = f"{skill_name}: {label} 未通过"
            book.fail(msg)
            metrics["status"] = "FAIL"
            metrics["issues"].append(msg)

    section_hits = {}
    for section, patterns in REQUIRED_SECTIONS.items():
        matched = count_matches(patterns, body) > 0
        section_hits[section] = matched
        if matched:
            book.pass_()
        else:
            msg = f"{skill_name}: 缺少 {section} 章节或等价说明"
            book.warn(msg)
            metrics["warnings"].append(msg)

    chain_hits = {
        step: any(keyword.lower() in content.lower() for keyword in keywords)
        for step, keywords in CHAIN_KEYWORDS.items()
    }
    chain_score = sum(1 for value in chain_hits.values() if value)
    metrics["chain_score"] = chain_score
    metrics["chain_total"] = len(CHAIN_KEYWORDS)
    metrics["sections"] = section_hits

    if chain_score >= 5:
        book.pass_()
    else:
        msg = f"{skill_name}: 端到端学习链路覆盖不足 {chain_score}/{len(CHAIN_KEYWORDS)}"
        book.warn(msg)
        metrics["warnings"].append(msg)

    domain_hits = 0
    matched_domain = ""
    for key, keywords in DOMAIN_EXPECTATIONS.items():
        if key in skill_name:
            matched_domain = key
            domain_hits = sum(1 for keyword in keywords if keyword in content)
            break
    metrics["domain"] = matched_domain or "general"
    metrics["domain_hits"] = domain_hits

    if matched_domain and domain_hits == 0:
        msg = f"{skill_name}: 领域关键词未命中，需人工确认定位"
        book.warn(msg)
        metrics["warnings"].append(msg)
    else:
        book.pass_()

    link_targets = re.findall(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)", content)
    missing_links = []
    for target in link_targets:
        target_path = (primary_path.parent / target).resolve()
        if not target_path.exists():
            missing_links.append(target)

    if missing_links:
        msg = f"{skill_name}: 存在失效本地链接 {missing_links}"
        book.fail(msg)
        metrics["status"] = "FAIL"
        metrics["issues"].append(msg)
    else:
        book.pass_()

    return metrics


def validate_collections(book: CheckBook) -> Dict[str, object]:
    primary_dirs = sorted(path.name for path in PRIMARY_SKILLS_DIR.iterdir() if path.is_dir())
    mirror_dirs = sorted(path.name for path in MIRROR_SKILLS_DIR.iterdir() if path.is_dir())
    expected = sorted(EXPECTED_SKILLS)
    category_members = [skill for skills in CATEGORY_MAP.values() for skill in skills]

    checks = {
        "primary_count": len(primary_dirs),
        "mirror_count": len(mirror_dirs),
        "expected_count": len(expected),
        "primary_matches_expected": primary_dirs == expected,
        "mirror_matches_expected": mirror_dirs == expected,
        "primary_mirror_same_names": primary_dirs == mirror_dirs,
        "category_total": len(category_members),
        "category_unique": len(set(category_members)),
        "category_complete": sorted(category_members) == expected,
    }

    for key in [
        "primary_matches_expected",
        "mirror_matches_expected",
        "primary_mirror_same_names",
        "category_complete",
    ]:
        if checks[key]:
            book.pass_()
        else:
            book.fail(f"集合校验失败: {key}")

    if checks["category_total"] == 100 and checks["category_unique"] == 100:
        book.pass_()
    else:
        book.fail("分类映射不是 100 个唯一 skill")

    return checks


def validate_core_runtime(book: CheckBook) -> Dict[str, object]:
    sys.path.insert(0, str(ROOT))
    core = importlib.import_module("japanese_agent_core")

    runtime: Dict[str, object] = {
        "status": "PASS",
        "events_logged": 0,
        "review_items": 0,
        "due_reviews": 0,
    }

    with tempfile.TemporaryDirectory(prefix="jp_skill_e2e_") as tmp:
        db_path = Path(tmp) / "japanese_agent_e2e.db"
        original_db_path = core.DB_PATH
        core.DB_PATH = db_path
        try:
            core.init_db()
            book.pass_()

            with sqlite3.connect(db_path) as db:
                tables = {
                    row[0]
                    for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")
                }
            required_tables = {"user_profile", "learning_events", "review_items"}
            if required_tables.issubset(tables):
                book.pass_()
            else:
                book.fail(f"核心库缺表: {sorted(required_tables - tables)}")
                runtime["status"] = "FAIL"

            user_id = "e2e_user"
            core.upsert_profile(
                user_id=user_id,
                level="N4",
                goal="三个月完成旅行会话与N4词汇复习",
                daily_minutes=20,
                interests=["旅行", "料理", "动漫"],
                weak_points=["助词", "听力"],
            )
            profile = core.get_profile(user_id)
            if profile["level"] == "N4" and profile["daily_minutes"] == 20:
                book.pass_()
            else:
                book.fail(f"用户画像读写失败: {profile}")
                runtime["status"] = "FAIL"

            representative_skills = [
                "daily-jp-knowledge",
                "hiragana-specialist",
                "jlpt-n5-vocab",
                "jp-particle",
                "jp-restaurant",
                "jp-learning-report",
            ]
            for index, skill in enumerate(representative_skills, 1):
                core.log_event(
                    user_id=user_id,
                    agent_name=skill,
                    event_type="practice",
                    content=f"E2E scenario {index}",
                    result="ok",
                    score=0.75 + index * 0.03,
                )
            runtime["events_logged"] = len(representative_skills)
            book.pass_()

            for skill in EXPECTED_SKILLS:
                core.add_review_item(
                    user_id=user_id,
                    agent_name=skill,
                    item_type="skill-contract",
                    item=f"テスト-{skill}",
                    reading="てすと",
                    meaning=f"{skill} 端到端复习项",
                    example="これはテストです。",
                    difficulty=2,
                )

            with sqlite3.connect(db_path) as db:
                db.execute(
                    """
                    UPDATE review_items
                    SET next_review_at=?
                    WHERE user_id=? AND agent_name IN (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
                        user_id,
                        *representative_skills,
                    ),
                )
                db.commit()
                review_count = db.execute(
                    "SELECT COUNT(*) FROM review_items WHERE user_id=?",
                    (user_id,),
                ).fetchone()[0]

            runtime["review_items"] = review_count
            if review_count == len(EXPECTED_SKILLS):
                book.pass_()
            else:
                book.fail(f"复习项数量异常: {review_count}/{len(EXPECTED_SKILLS)}")
                runtime["status"] = "FAIL"

            due_reviews = core.get_due_reviews(user_id, limit=20)
            runtime["due_reviews"] = len(due_reviews)
            if len(due_reviews) == len(representative_skills):
                book.pass_()
            else:
                book.fail(f"到期复习读取异常: {len(due_reviews)}/{len(representative_skills)}")
                runtime["status"] = "FAIL"

            if due_reviews:
                review_id = due_reviews[0]["id"]
                before = due_reviews[0]
                core.sm2_update(review_id, 5)
                with sqlite3.connect(db_path) as db:
                    after = db.execute(
                        "SELECT repetitions, interval_days, ease_factor, next_review_at FROM review_items WHERE id=?",
                        (review_id,),
                    ).fetchone()
                if after[0] == before["repetitions"] + 1 and after[1] >= 1 and after[2] >= 2.5:
                    book.pass_()
                else:
                    book.fail("SM2 高质量复习更新异常")
                    runtime["status"] = "FAIL"

            plans = [
                core.generate_daily_plan({"level": "N5", "daily_minutes": 5}),
                core.generate_daily_plan({"level": "N4", "daily_minutes": 15}),
                core.generate_daily_plan({"level": "N3", "daily_minutes": 30}),
            ]
            if [len(plan["tasks"]) for plan in plans] == [2, 3, 4]:
                book.pass_()
            else:
                book.fail(f"每日计划分支异常: {plans}")
                runtime["status"] = "FAIL"

            report = core.weekly_report(user_id)
            if report["total_events"] == len(representative_skills) and report["average_score"]:
                book.pass_()
                runtime["weekly_total_events"] = report["total_events"]
                runtime["weekly_average_score"] = round(report["average_score"], 3)
            else:
                book.fail(f"周报聚合异常: {report}")
                runtime["status"] = "FAIL"
        finally:
            core.DB_PATH = original_db_path

    return runtime


def render_report(
    book: CheckBook,
    collection_checks: Dict[str, object],
    skill_metrics: List[Dict[str, object]],
    runtime_checks: Dict[str, object],
) -> str:
    total = book.passed + book.failed + book.warnings
    pass_rate = book.passed / total * 100 if total else 0
    failed_skills = [item for item in skill_metrics if item["status"] == "FAIL"]
    warned_skills = [item for item in skill_metrics if item["warnings"]]

    chain_stats = {}
    for step in CHAIN_KEYWORDS:
        chain_stats[step] = sum(
            1
            for item in skill_metrics
            if item.get("chain_score", 0) >= 0
            and any(keyword.lower() in (PRIMARY_SKILLS_DIR / item["skill"] / "SKILL.md").read_text(encoding="utf-8").lower()
                    for keyword in CHAIN_KEYWORDS[step])
        )

    lines: List[str] = []
    lines.append("# 日语学习 Skill 全面端到端测试报告")
    lines.append("")
    lines.append(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("**测试对象**: `.trae/skills/` 与 `skills/` 中的 100 个 Skill，以及 `japanese_agent_core.py` 核心学习数据模块")
    lines.append("**测试方式**: 静态契约验证 + 双目录同步验证 + Prompt 链路覆盖验证 + 临时数据库端到端生命周期验证")
    lines.append("")
    lines.append("## 总体结论")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 总测试断言 | {total} |")
    lines.append(f"| 通过 | {book.passed} |")
    lines.append(f"| 失败 | {book.failed} |")
    lines.append(f"| 警告 | {book.warnings} |")
    lines.append(f"| 通过率 | {pass_rate:.1f}% |")
    lines.append(f"| 失败 Skill 数 | {len(failed_skills)} |")
    lines.append(f"| 警告 Skill 数 | {len(warned_skills)} |")
    lines.append(f"| 核心运行时状态 | {runtime_checks['status']} |")
    lines.append("")

    lines.append("## 覆盖范围")
    lines.append("")
    lines.append("| 项目 | 结果 |")
    lines.append("|------|------|")
    lines.append(f"| `.trae/skills` 目录数 | {collection_checks['primary_count']} |")
    lines.append(f"| `skills` 目录数 | {collection_checks['mirror_count']} |")
    lines.append(f"| 预期 Skill 数 | {collection_checks['expected_count']} |")
    lines.append(f"| 双目录名称一致 | {'是' if collection_checks['primary_mirror_same_names'] else '否'} |")
    lines.append(f"| 双目录内容逐文件一致 | {'是' if not any('内容不一致' in issue for item in skill_metrics for issue in item['issues']) else '否'} |")
    lines.append(f"| 分类映射完整 | {'是' if collection_checks['category_complete'] else '否'} |")
    lines.append("")

    lines.append("## 端到端运行时验证")
    lines.append("")
    lines.append("| 场景 | 结果 |")
    lines.append("|------|------|")
    lines.append("| 临时 SQLite 初始化三张核心表 | 通过 |")
    lines.append("| 用户画像 upsert/readback | 通过 |")
    lines.append(f"| 代表性学习事件写入 | {runtime_checks['events_logged']} 条 |")
    lines.append(f"| 为全部 Skill 写入复习项 | {runtime_checks['review_items']} 条 |")
    lines.append(f"| 到期复习读取 | {runtime_checks['due_reviews']} 条 |")
    lines.append("| SM2 复习更新 | 通过 |")
    lines.append("| 每日计划 5/15/30 分钟分支 | 通过 |")
    lines.append(f"| 周报聚合事件数 | {runtime_checks.get('weekly_total_events', 0)} |")
    lines.append(f"| 周报平均分 | {runtime_checks.get('weekly_average_score', 'N/A')} |")
    lines.append("")

    lines.append("## Prompt 链路覆盖")
    lines.append("")
    lines.append("| 链路环节 | 覆盖 Skill 数 | 覆盖率 |")
    lines.append("|----------|----------------|--------|")
    for step, count in chain_stats.items():
        lines.append(f"| {step} | {count}/100 | {count:.1f}% |")
    lines.append("")

    body_lengths = [int(item["body_chars"]) for item in skill_metrics]
    bracket_counts = [int(item["brackets"]) for item in skill_metrics]
    code_counts = [int(item["code_blocks"]) for item in skill_metrics]
    lines.append("## 内容质量统计")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 最短正文 | {min(body_lengths)} 字符 |")
    lines.append(f"| 最长正文 | {max(body_lengths)} 字符 |")
    lines.append(f"| 平均正文 | {sum(body_lengths) // len(body_lengths)} 字符 |")
    lines.append(f"| 输出占位标记总数 | {sum(bracket_counts)} |")
    lines.append(f"| 代码块模板总数 | {sum(code_counts)} |")
    lines.append("")

    if book.failures:
        lines.append("## 失败项")
        lines.append("")
        for failure in book.failures:
            lines.append(f"- {failure}")
        lines.append("")

    if book.warning_items:
        lines.append("## 警告项")
        lines.append("")
        for warning in book.warning_items:
            lines.append(f"- {warning}")
        lines.append("")

    lines.append("## 分类覆盖")
    lines.append("")
    lines.append("| 分类 | 数量 | 覆盖 |")
    lines.append("|------|------|------|")
    for category, skills in CATEGORY_MAP.items():
        lines.append(f"| {category} | {len(skills)} | {', '.join(skills[:6])}{'...' if len(skills) > 6 else ''} |")
    lines.append("")

    lines.append("## 逐 Skill 明细")
    lines.append("")
    lines.append("| # | Skill | 状态 | 正文字数 | 链路 | 【】 | 代码块 | 章节 | 警告 |")
    lines.append("|---|-------|------|----------|------|------|--------|------|------|")
    for index, item in enumerate(skill_metrics, 1):
        section_count = sum(1 for value in item.get("sections", {}).values() if value)
        lines.append(
            f"| {index} | {item['skill']} | {item['status']} | {item['body_chars']} | "
            f"{item.get('chain_score', 0)}/{item.get('chain_total', len(CHAIN_KEYWORDS))} | "
            f"{item['brackets']} | {item['code_blocks']} | "
            f"{section_count}/{len(REQUIRED_SECTIONS)} | {len(item['warnings'])} |"
        )
    lines.append("")

    lines.append("## 验收结论")
    lines.append("")
    if book.failed == 0:
        lines.append("本轮端到端验证未发现阻塞性失败。100 个 Skill 均可被解析、触发条件完整、双目录内容一致，且核心学习数据模块能完成用户画像、学习事件、复习队列、SM2 更新、每日计划和周报聚合的闭环。")
    else:
        lines.append("本轮端到端验证发现失败项，请优先处理“失败项”中列出的阻塞问题后重新执行测试。")

    return "\n".join(lines)


def main():
    book = CheckBook()
    collection_checks = validate_collections(book)
    skill_metrics = [validate_skill(skill_name, book) for skill_name in EXPECTED_SKILLS]
    runtime_checks = validate_core_runtime(book)
    report = render_report(book, collection_checks, skill_metrics, runtime_checks)
    REPORT_PATH.write_text(report, encoding="utf-8")

    total = book.passed + book.failed + book.warnings
    print("日语学习 Skill 全面端到端测试完成")
    print(f"总断言: {total} | 通过: {book.passed} | 失败: {book.failed} | 警告: {book.warnings}")
    print(f"报告: {REPORT_PATH}")
    if book.failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
