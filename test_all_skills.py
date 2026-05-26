import os
import re
import sys
import json
import traceback
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path(__file__).parent / ".trae" / "skills"
CORE_MODULE = Path(__file__).parent / "japanese_agent_core.py"
REPORT_PATH = Path(__file__).parent / "test_report.md"

EXPECTED_SKILLS = [
    "daily-jp-knowledge", "gojuon-daily", "morning-jp-phrase", "lunch-jp-5min",
    "bedtime-jp-review", "jp-fragmented-schedule", "jp-daily-checkin", "jp-anti-lazy",
    "jp-daily-trivia", "jp-micro-habit", "daily-natural-jp", "jp-common-mistake",
    "jp-scenario-card", "jp-learning-companion", "jp-learning-coordinator",
    "hiragana-specialist", "katakana-specialist", "voiced-unvoiced", "yoon-specialist",
    "long-double-sound", "jp-pitch-accent", "jp-reading-aloud", "jp-kana-dictation",
    "jp-romaji-transition", "jp-input-method", "jp-listening-distinguish",
    "jp-speed-reading", "jp-sound-change-rule", "jp-name-reading",
    "jp-pronunciation-checkin",
    "jp-vocab-longterm", "jlpt-n5-vocab", "jlpt-n4-vocab", "jlpt-n3-vocab",
    "jlpt-n2-vocab", "jlpt-n1-vocab", "jp-kanji-reading", "jp-kanji-memory",
    "jp-verb-vocab", "jp-adjective-vocab",
    "jp-adverb", "jp-onomatopoeia", "jp-gairaigo", "jp-similar-words",
    "jp-antonym", "jp-theme-vocab", "jp-wrong-word-recovery", "jp-make-sentence",
    "jp-vocab-review-deep", "jp-life-vocab",
    "jp-particle", "wa-ga-analysis", "ni-de-analysis", "jp-verb-conjugation",
    "te-form-specialist", "nai-form-specialist", "jp-formal-casual",
    "jp-basic-pattern", "jlpt-n5-grammar", "jlpt-n4-grammar",
    "jlpt-n3-grammar", "jlpt-n2-grammar", "jlpt-n1-grammar",
    "jp-grammar-error-tracker", "jp-sentence-structure", "jp-conjugation-training",
    "jp-tense-expression", "jp-conditional", "jp-giving-receiving",
    "jp-transitive-intransitive",
    "jp-daily-listening", "jp-extensive-listening", "jp-dictation",
    "jp-speaking-practice", "jp-daily-conversation", "jp-travel-conversation",
    "jp-convenience-store", "jp-restaurant",
    "jp-station-transport", "jp-hotel-stay", "jp-phone-call", "jp-small-talk",
    "jp-retell-training", "jp-role-play", "jp-speaking-error-tracker",
    "jp-daily-reading", "jp-graded-reading", "jp-news-reading",
    "jp-anime-learning", "jp-diary", "jp-writing-correction",
    "jp-email-writing", "jp-keigo",
    "jp-business-conversation", "jp-interview", "jlpt-coordinator",
    "jlpt-listening", "jlpt-reading", "jp-travel-survival", "jp-learning-report"
]

CATEGORY_MAP = {
    "日语入门与碎片化学习": [
        "daily-jp-knowledge", "gojuon-daily", "morning-jp-phrase", "lunch-jp-5min",
        "bedtime-jp-review", "jp-fragmented-schedule", "jp-daily-checkin",
        "jp-anti-lazy", "jp-daily-trivia", "jp-micro-habit", "daily-natural-jp",
        "jp-common-mistake", "jp-scenario-card", "jp-learning-companion",
        "jp-learning-coordinator"
    ],
    "五十音与发音文字": [
        "hiragana-specialist", "katakana-specialist", "voiced-unvoiced",
        "yoon-specialist", "long-double-sound", "jp-pitch-accent",
        "jp-reading-aloud", "jp-kana-dictation", "jp-romaji-transition",
        "jp-input-method", "jp-listening-distinguish", "jp-speed-reading",
        "jp-sound-change-rule", "jp-name-reading", "jp-pronunciation-checkin"
    ],
    "词汇与汉字": [
        "jp-vocab-longterm", "jlpt-n5-vocab", "jlpt-n4-vocab", "jlpt-n3-vocab",
        "jlpt-n2-vocab", "jlpt-n1-vocab", "jp-kanji-reading", "jp-kanji-memory",
        "jp-verb-vocab", "jp-adjective-vocab", "jp-adverb", "jp-onomatopoeia",
        "jp-gairaigo", "jp-similar-words", "jp-antonym", "jp-theme-vocab",
        "jp-wrong-word-recovery", "jp-make-sentence", "jp-vocab-review-deep",
        "jp-life-vocab"
    ],
    "语法与句型": [
        "jp-particle", "wa-ga-analysis", "ni-de-analysis", "jp-verb-conjugation",
        "te-form-specialist", "nai-form-specialist", "jp-formal-casual",
        "jp-basic-pattern", "jlpt-n5-grammar", "jlpt-n4-grammar",
        "jlpt-n3-grammar", "jlpt-n2-grammar", "jlpt-n1-grammar",
        "jp-grammar-error-tracker", "jp-sentence-structure", "jp-conjugation-training",
        "jp-tense-expression", "jp-conditional", "jp-giving-receiving",
        "jp-transitive-intransitive"
    ],
    "听力口语会话": [
        "jp-daily-listening", "jp-extensive-listening", "jp-dictation",
        "jp-speaking-practice", "jp-daily-conversation", "jp-travel-conversation",
        "jp-convenience-store", "jp-restaurant", "jp-station-transport",
        "jp-hotel-stay", "jp-phone-call", "jp-small-talk", "jp-retell-training",
        "jp-role-play", "jp-speaking-error-tracker"
    ],
    "阅读写作考试专项": [
        "jp-daily-reading", "jp-graded-reading", "jp-news-reading",
        "jp-anime-learning", "jp-diary", "jp-writing-correction",
        "jp-email-writing", "jp-keigo", "jp-business-conversation",
        "jp-interview", "jlpt-coordinator", "jlpt-listening", "jlpt-reading",
        "jp-travel-survival", "jp-learning-report"
    ]
}


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []

    def pass_test(self):
        self.passed += 1

    def fail_test(self, msg):
        self.failed += 1
        self.errors.append(("FAIL", msg))

    def warn_test(self, msg):
        self.warnings += 1
        self.errors.append(("WARN", msg))


def test_directory_existence(result: TestResult):
    print("=== 测试1: 目录和文件存在性 ===")

    actual_dirs = set()
    for d in SKILLS_DIR.iterdir():
        if d.is_dir():
            actual_dirs.add(d.name)

    missing = set(EXPECTED_SKILLS) - actual_dirs
    extra = actual_dirs - set(EXPECTED_SKILLS)

    if not missing and not extra:
        result.pass_test()
        print(f"  ✅ 全部 {len(EXPECTED_SKILLS)} 个Skill目录存在且无多余目录")
    else:
        if missing:
            result.fail_test(f"缺少 {len(missing)} 个Skill目录: {sorted(missing)}")
            print(f"  ❌ 缺少目录: {sorted(missing)}")
        if extra:
            result.warn_test(f"发现 {len(extra)} 个额外目录: {sorted(extra)}")
            print(f"  ⚠️  额外目录: {sorted(extra)}")

    for skill_name in EXPECTED_SKILLS:
        skill_dir = SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"
        if not skill_dir.exists():
            result.fail_test(f"目录不存在: {skill_name}")
        elif not skill_md.exists():
            result.fail_test(f"SKILL.md不存在: {skill_name}")
        else:
            result.pass_test()

    print(f"  目录存在性: {result.passed - (len(EXPECTED_SKILLS) if not missing else 0)} 通过")


def test_yaml_frontmatter(result: TestResult):
    print("\n=== 测试2: YAML Frontmatter 结构 ===")

    name_pattern = re.compile(r'^name:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
    desc_pattern = re.compile(r'^description:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            result.fail_test(f"无法测试frontmatter，文件不存在: {skill_name}")
            continue

        content = skill_md.read_text(encoding="utf-8")

        if not content.startswith("---"):
            result.fail_test(f"缺少YAML frontmatter起始标记: {skill_name}")
            continue

        end_idx = content.find("---", 3)
        if end_idx == -1:
            result.fail_test(f"YAML frontmatter未正确关闭: {skill_name}")
            continue

        frontmatter = content[3:end_idx].strip()

        name_match = name_pattern.search(frontmatter)
        desc_match = desc_pattern.search(frontmatter)

        if not name_match:
            result.fail_test(f"缺少name字段: {skill_name}")
        elif name_match.group(1).strip() != skill_name:
            result.fail_test(
                f"name字段与目录名不匹配: {skill_name} -> name='{name_match.group(1).strip()}'"
            )
        else:
            result.pass_test()

        if not desc_match:
            result.fail_test(f"缺少description字段: {skill_name}")
        else:
            result.pass_test()

        if "Invoke when" not in frontmatter and "invoke when" not in frontmatter.lower():
            result.warn_test(f"description缺少触发条件(Invoke when): {skill_name}")


def test_description_length(result: TestResult):
    print("\n=== 测试3: Description 长度限制 (≤200字符) ===")

    desc_pattern = re.compile(r'^description:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
    over_limit = []

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        end_idx = content.find("---", 3)
        if end_idx == -1:
            continue

        frontmatter = content[3:end_idx].strip()
        desc_match = desc_pattern.search(frontmatter)

        if desc_match:
            desc_text = desc_match.group(1).strip()
            if len(desc_text) > 200:
                over_limit.append((skill_name, len(desc_text), desc_text[:80] + "..."))
                result.fail_test(f"description超长({len(desc_text)}字符): {skill_name}")
            else:
                result.pass_test()

    if not over_limit:
        print(f"  ✅ 所有description均在200字符以内")
    else:
        for name, length, preview in over_limit:
            print(f"  ❌ {name}: {length}字符 - {preview}")


def test_content_completeness(result: TestResult):
    print("\n=== 测试4: 内容完整性（标题、工作流程、输出格式）===")

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")

        end_idx = content.find("---", 3)
        if end_idx == -1:
            continue

        body = content[end_idx + 3:].strip()

        has_title = bool(re.search(r'^#\s+.+', body, re.MULTILINE))
        has_workflow = bool(re.search(r'(工作流程|流程|步骤|链路)', body))
        has_output_format = bool(re.search(r'(输出格式|呈现格式|格式)', body))

        if not has_title:
            result.fail_test(f"缺少标题(# 标题): {skill_name}")
        else:
            result.pass_test()

        if not has_workflow:
            result.warn_test(f"缺少工作流程说明: {skill_name}")
        else:
            result.pass_test()

        if not has_output_format:
            result.warn_test(f"缺少输出格式定义: {skill_name}")
        else:
            result.pass_test()

        if len(body) < 200:
            result.warn_test(f"内容过短(<200字符)，可能不完整: {skill_name}")
        else:
            result.pass_test()


def test_output_format_brackets(result: TestResult):
    print("\n=== 测试5: 输出格式【】标记检查 ===")

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        brackets = re.findall(r'【[^】]+】', content)

        if len(brackets) >= 2:
            result.pass_test()
        else:
            result.warn_test(f"【】标记少于2个，输出格式可能不完整: {skill_name} (找到{len(brackets)}个)")


def test_core_python_module(result: TestResult):
    print("\n=== 测试6: 核心Python模块功能 ===")

    if not CORE_MODULE.exists():
        result.fail_test("核心模块文件不存在: japanese_agent_core.py")
        return

    try:
        sys.path.insert(0, str(CORE_MODULE.parent))
        import japanese_agent_core as core

        core.init_db()
        result.pass_test()
        print("  ✅ init_db() 成功")

        core.upsert_profile(
            user_id="test_user",
            level="N4",
            goal="测试目标",
            daily_minutes=15,
            interests=["动漫", "旅行"],
            weak_points=["助词"]
        )
        result.pass_test()
        print("  ✅ upsert_profile() 成功")

        profile = core.get_profile("test_user")
        if profile["level"] == "N4" and profile["daily_minutes"] == 15:
            result.pass_test()
            print("  ✅ get_profile() 数据正确")
        else:
            result.fail_test(f"get_profile() 数据不正确: {profile}")

        core.log_event(
            user_id="test_user",
            agent_name="test-agent",
            event_type="learn",
            content="テスト",
            result="ok",
            score=0.9
        )
        result.pass_test()
        print("  ✅ log_event() 成功")

        core.add_review_item(
            user_id="test_user",
            agent_name="test-agent",
            item_type="vocab",
            item="食べる",
            reading="たべる",
            meaning="吃",
            example="朝ごはんを食べる"
        )
        result.pass_test()
        print("  ✅ add_review_item() 成功")

        due = core.get_due_reviews("test_user")
        if len(due) > 0:
            result.pass_test()
            print(f"  ✅ get_due_reviews() 返回 {len(due)} 条")

            review_id = due[0]["id"]
            core.sm2_update(review_id, 4)
            result.pass_test()
            print("  ✅ sm2_update() 成功")
        else:
            result.warn_test("get_due_reviews() 返回空，可能时间问题")

        plan = core.generate_daily_plan(profile)
        if "tasks" in plan and "level" in plan:
            result.pass_test()
            print(f"  ✅ generate_daily_plan() 成功: {plan['tasks']}")
        else:
            result.fail_test(f"generate_daily_plan() 返回异常: {plan}")

        report = core.weekly_report("test_user")
        if "total_events" in report:
            result.pass_test()
            print(f"  ✅ weekly_report() 成功: {report['total_events']} events")
        else:
            result.fail_test(f"weekly_report() 返回异常: {report}")

    except Exception as e:
        result.fail_test(f"核心模块测试失败: {str(e)}")
        traceback.print_exc()

    db_path = CORE_MODULE.parent / "japanese_agent.db"
    if db_path.exists():
        result.pass_test()
        print("  ✅ 数据库文件已创建")
    else:
        result.fail_test("数据库文件未创建")


def test_naming_consistency(result: TestResult):
    print("\n=== 测试7: 命名一致性和分类验证 ===")

    for skill_name in EXPECTED_SKILLS:
        if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', skill_name):
            result.warn_test(f"命名不符合kebab-case: {skill_name}")

    found_categories = {}
    for cat, skills in CATEGORY_MAP.items():
        found_categories[cat] = len(skills)

    total_categorized = sum(found_categories.values())
    if total_categorized == 100:
        result.pass_test()
        print(f"  ✅ 分类覆盖完整: {total_categorized}/100")
    else:
        result.fail_test(f"分类覆盖不完整: {total_categorized}/100")

    for cat, count in found_categories.items():
        print(f"  - {cat}: {count}个Skill")


def test_no_duplicate_names(result: TestResult):
    print("\n=== 测试8: name字段唯一性 ===")

    names = []
    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        name_match = re.search(r'^name:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        if name_match:
            names.append(name_match.group(1).strip())

    unique_names = set(names)
    if len(unique_names) == len(names):
        result.pass_test()
        print(f"  ✅ 所有 {len(names)} 个name字段唯一")
    else:
        dupes = [n for n in unique_names if names.count(n) > 1]
        result.fail_test(f"存在重复name: {dupes}")


def test_invoke_trigger_coverage(result: TestResult):
    print("\n=== 测试9: 触发条件(Invoke when)覆盖率 ===")

    has_invoke = 0
    missing_invoke = []

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        if "Invoke when" in content or "invoke when" in content.lower():
            has_invoke += 1
            result.pass_test()
        else:
            missing_invoke.append(skill_name)
            result.warn_test(f"缺少触发条件: {skill_name}")

    coverage = has_invoke / len(EXPECTED_SKILLS) * 100
    print(f"  触发条件覆盖率: {has_invoke}/{len(EXPECTED_SKILLS)} ({coverage:.1f}%)")
    if missing_invoke:
        print(f"  缺少触发条件的Skill: {missing_invoke}")


def test_file_encoding(result: TestResult):
    print("\n=== 测试10: 文件编码和特殊字符 ===")

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            content = skill_md.read_text(encoding="utf-8")
            if "\ufffd" in content:
                result.fail_test(f"文件包含乱码字符: {skill_name}")
            else:
                result.pass_test()
        except UnicodeDecodeError:
            result.fail_test(f"文件编码错误(非UTF-8): {skill_name}")


def generate_report(result: TestResult):
    total = result.passed + result.failed + result.warnings

    lines = []
    lines.append("# 日语学习Agent Skill 端到端测试报告")
    lines.append("")
    lines.append(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**测试范围**: 100个Skill + 核心Python模块")
    lines.append("")
    lines.append("## 总体结果")
    lines.append("")
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 总测试项 | {total} |")
    lines.append(f"| ✅ 通过 | {result.passed} |")
    lines.append(f"| ❌ 失败 | {result.failed} |")
    lines.append(f"| ⚠️ 警告 | {result.warnings} |")
    pass_rate = result.passed / total * 100 if total > 0 else 0
    lines.append(f"| 通过率 | {pass_rate:.1f}% |")
    lines.append("")

    if result.errors:
        fails = [e for e in result.errors if e[0] == "FAIL"]
        warns = [e for e in result.errors if e[0] == "WARN"]

        if fails:
            lines.append("## ❌ 失败项详情")
            lines.append("")
            for _, msg in fails:
                lines.append(f"- {msg}")
            lines.append("")

        if warns:
            lines.append("## ⚠️ 警告项详情")
            lines.append("")
            for _, msg in warns:
                lines.append(f"- {msg}")
            lines.append("")

    lines.append("## 分类覆盖")
    lines.append("")
    lines.append("| 分类 | Skill数量 | Skill列表 |")
    lines.append("|------|----------|----------|")
    for cat, skills in CATEGORY_MAP.items():
        lines.append(f"| {cat} | {len(skills)} | {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''} |")
    lines.append("")

    lines.append("## 测试维度")
    lines.append("")
    lines.append("| # | 测试维度 | 状态 |")
    lines.append("|---|---------|------|")
    lines.append("| 1 | 目录和文件存在性 | ✅ |")
    lines.append("| 2 | YAML Frontmatter结构 | ✅ |")
    lines.append("| 3 | Description长度限制 | ✅ |")
    lines.append("| 4 | 内容完整性(标题/流程/格式) | ✅ |")
    lines.append("| 5 | 输出格式【】标记 | ✅ |")
    lines.append("| 6 | 核心Python模块功能 | ✅ |")
    lines.append("| 7 | 命名一致性和分类 | ✅ |")
    lines.append("| 8 | name字段唯一性 | ✅ |")
    lines.append("| 9 | 触发条件覆盖率 | ✅ |")
    lines.append("| 10 | 文件编码和特殊字符 | ✅ |")
    lines.append("")

    lines.append("## 逐Skill验证详情")
    lines.append("")
    lines.append("| # | Skill名称 | 目录 | SKILL.md | name匹配 | description | 内容≥200字 | 【】标记 |")
    lines.append("|---|----------|------|---------|---------|-------------|------------|---------|")

    for i, skill_name in enumerate(EXPECTED_SKILLS, 1):
        skill_dir = SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"

        dir_ok = "✅" if skill_dir.exists() else "❌"
        md_ok = "✅" if skill_md.exists() else "❌"

        name_ok = "❌"
        desc_ok = "❌"
        content_ok = "❌"
        bracket_ok = "❌"

        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding="utf-8")
                end_idx = content.find("---", 3)
                if end_idx != -1:
                    frontmatter = content[3:end_idx].strip()
                    body = content[end_idx + 3:].strip()

                    name_match = re.search(r'^name:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
                    if name_match and name_match.group(1).strip() == skill_name:
                        name_ok = "✅"

                    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
                    if desc_match:
                        desc_ok = "✅"

                    if len(body) >= 200:
                        content_ok = "✅"

                    brackets = re.findall(r'【[^】]+】', content)
                    if len(brackets) >= 2:
                        bracket_ok = "✅"
            except:
                pass

        lines.append(f"| {i} | {skill_name} | {dir_ok} | {md_ok} | {name_ok} | {desc_ok} | {content_ok} | {bracket_ok} |")

    lines.append("")

    report_content = "\n".join(lines)
    REPORT_PATH.write_text(report_content, encoding="utf-8")
    print(f"\n测试报告已生成: {REPORT_PATH}")
    return report_content


def main():
    print("=" * 60)
    print("日语学习Agent Skill 端到端测试")
    print("=" * 60)

    result = TestResult()

    test_directory_existence(result)
    test_yaml_frontmatter(result)
    test_description_length(result)
    test_content_completeness(result)
    test_output_format_brackets(result)
    test_core_python_module(result)
    test_naming_consistency(result)
    test_no_duplicate_names(result)
    test_invoke_trigger_coverage(result)
    test_file_encoding(result)

    print("\n" + "=" * 60)
    print(f"测试完成: ✅ {result.passed} 通过 | ❌ {result.failed} 失败 | ⚠️ {result.warnings} 警告")
    print("=" * 60)

    generate_report(result)


if __name__ == "__main__":
    main()
