import os
import re
import sys
import json
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path(__file__).parent / ".trae" / "skills"
REPORT_PATH = Path(__file__).parent / "test_report_deep.md"

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

CHAIN_KEYWORDS = {
    "读取用户": ["画像", "水平", "profile", "用户"],
    "复习队列": ["复习", "间隔", "SM2", "到期", "review"],
    "新知识推送": ["新词", "新知识", "新语法", "推送", "选择"],
    "用户互动": ["用户", "造句", "回答", "填空", "选择", "跟读", "朗读", "复述"],
    "反馈纠错": ["纠正", "反馈", "纠错", "自然度", "错因"],
    "复习安排": ["复习", "下次", "间隔", "队列", "复习时间"],
}

REQUIRED_SECTIONS = {
    "工作流程": ["工作流程", "流程", "步骤", "链路"],
    "输出格式": ["输出格式", "呈现格式", "格式"],
}

def check_chain_completeness(content, skill_name):
    issues = []
    chain_present = {}

    for chain_step, keywords in CHAIN_KEYWORDS.items():
        found = False
        for kw in keywords:
            if kw in content:
                found = True
                break
        chain_present[chain_step] = found

    missing = [k for k, v in chain_present.items() if not v]
    if len(missing) >= 4:
        issues.append(f"长链路不完整，缺少: {', '.join(missing)}")

    return chain_present, issues


def check_required_sections(content, skill_name):
    issues = []
    found_sections = {}

    for section, keywords in REQUIRED_SECTIONS.items():
        found = False
        for kw in keywords:
            if kw in content:
                found = True
                break
        found_sections[section] = found

    missing = [k for k, v in found_sections.items() if not v]
    if missing:
        issues.append(f"缺少必要章节: {', '.join(missing)}")

    return found_sections, issues


def check_output_format_quality(content, skill_name):
    issues = []
    brackets = re.findall(r'【[^】]+】', content)

    if len(brackets) < 3:
        issues.append(f"输出格式【】标记仅{len(brackets)}个，可能不够详细")

    code_blocks = re.findall(r'```[\s\S]*?```', content)
    if not code_blocks:
        issues.append("缺少代码块格式的输出模板")

    return len(brackets), len(code_blocks), issues


def check_role_definition(content, skill_name):
    issues = []

    has_role = bool(re.search(r'(你是一个|你是|你的角色|你的任务|你是一位)', content))
    if not has_role:
        issues.append("缺少角色定义（'你是一个/你是/你是一位'）")

    return has_role, issues


def check_interaction_design(content, skill_name):
    issues = []

    has_wait = bool(re.search(r'(等待用户|用户回答|用户完成|用户输入|你来|请用户)', content))
    if not has_wait:
        issues.append("缺少用户互动等待点，可能是一次性输出而非交互式")

    return has_wait, issues


def check_review_mechanism(content, skill_name):
    issues = []

    has_review = bool(re.search(r'(复习|间隔|SM2|下次复习|复习队列|复习时间)', content))
    if not has_review:
        issues.append("缺少复习机制描述")

    return has_review, issues


def check_content_length(content, skill_name):
    body_start = content.find("---", 3)
    if body_start == -1:
        return 0, ["无法解析body"]

    body = content[body_start + 3:].strip()
    char_count = len(body)
    issues = []

    if char_count < 300:
        issues.append(f"内容过短({char_count}字符)，prompt可能不够详细")
    elif char_count < 500:
        issues.append(f"内容偏短({char_count}字符)，建议补充更多细节")

    return char_count, issues


def main():
    print("=" * 70)
    print("日语学习Agent Skill 深度端到端测试")
    print("=" * 70)

    all_results = {}
    total_issues = 0
    total_warnings = 0

    for skill_name in EXPECTED_SKILLS:
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.exists():
            all_results[skill_name] = {"status": "MISSING", "issues": ["SKILL.md不存在"]}
            total_issues += 1
            continue

        content = skill_md.read_text(encoding="utf-8")
        issues = []

        chain_present, chain_issues = check_chain_completeness(content, skill_name)
        issues.extend(chain_issues)

        sections_found, section_issues = check_required_sections(content, skill_name)
        issues.extend(section_issues)

        bracket_count, code_block_count, format_issues = check_output_format_quality(content, skill_name)
        issues.extend(format_issues)

        has_role, role_issues = check_role_definition(content, skill_name)
        issues.extend(role_issues)

        has_wait, interaction_issues = check_interaction_design(content, skill_name)
        issues.extend(interaction_issues)

        has_review, review_issues = check_review_mechanism(content, skill_name)
        issues.extend(review_issues)

        char_count, length_issues = check_content_length(content, skill_name)
        issues.extend(length_issues)

        critical_issues = [i for i in issues if "缺少" in i or "不完整" in i]
        warning_issues = [i for i in issues if "缺少" not in i and "不完整" not in i]

        total_issues += len(critical_issues)
        total_warnings += len(warning_issues)

        all_results[skill_name] = {
            "status": "PASS" if not critical_issues else "ISSUE",
            "chain_present": chain_present,
            "sections_found": sections_found,
            "bracket_count": bracket_count,
            "code_block_count": code_block_count,
            "has_role": has_role,
            "has_interaction": has_wait,
            "has_review": has_review,
            "char_count": char_count,
            "critical_issues": critical_issues,
            "warnings": warning_issues,
        }

    lines = []
    lines.append("# 日语学习Agent Skill 深度端到端测试报告")
    lines.append("")
    lines.append(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**测试范围**: 100个Skill的prompt链路完整性深度验证")
    lines.append("")
    lines.append("## 总体结果")
    lines.append("")

    pass_count = sum(1 for r in all_results.values() if r["status"] == "PASS")
    issue_count = sum(1 for r in all_results.values() if r["status"] == "ISSUE")
    missing_count = sum(1 for r in all_results.values() if r["status"] == "MISSING")

    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 完全通过 | {pass_count} |")
    lines.append(f"| 存在问题 | {issue_count} |")
    lines.append(f"| 文件缺失 | {missing_count} |")
    lines.append(f"| 严重问题总数 | {total_issues} |")
    lines.append(f"| 警告总数 | {total_warnings} |")
    lines.append("")

    lines.append("## 测试维度说明")
    lines.append("")
    lines.append("| 维度 | 说明 |")
    lines.append("|------|------|")
    lines.append("| 长链路完整性 | 检查是否包含读取用户→复习→新知识→互动→反馈→复习安排的完整链路 |")
    lines.append("| 必要章节 | 检查是否包含工作流程和输出格式章节 |")
    lines.append("| 输出格式质量 | 检查【】标记数量和代码块模板 |")
    lines.append("| 角色定义 | 检查是否有明确的Agent角色定义 |")
    lines.append("| 交互设计 | 检查是否有用户互动等待点 |")
    lines.append("| 复习机制 | 检查是否描述了复习/间隔重复机制 |")
    lines.append("| 内容长度 | 检查prompt内容是否足够详细 |")
    lines.append("")

    if issue_count > 0 or missing_count > 0:
        lines.append("## ❌ 存在问题的Skill")
        lines.append("")
        for skill_name, result in all_results.items():
            if result["status"] in ("ISSUE", "MISSING"):
                lines.append(f"### {skill_name}")
                if "critical_issues" in result:
                    for issue in result["critical_issues"]:
                        lines.append(f"- ❌ {issue}")
                if "warnings" in result:
                    for issue in result["warnings"]:
                        lines.append(f"- ⚠️ {issue}")
                lines.append("")

    lines.append("## 逐Skill详细验证")
    lines.append("")
    lines.append("| # | Skill | 链路 | 章节 | 【】 | 代码块 | 角色 | 交互 | 复习 | 字数 | 问题 | 警告 |")
    lines.append("|---|-------|------|------|------|--------|------|------|------|------|------|------|")

    for i, skill_name in enumerate(EXPECTED_SKILLS, 1):
        r = all_results[skill_name]

        if r["status"] == "MISSING":
            lines.append(f"| {i} | {skill_name} | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 0 | 1 | 0 |")
            continue

        chain_score = sum(1 for v in r["chain_present"].values() if v)
        chain_total = len(r["chain_present"])
        chain_icon = "✅" if chain_score >= chain_total - 1 else "⚠️"

        section_score = sum(1 for v in r["sections_found"].values() if v)
        section_total = len(r["sections_found"])
        section_icon = "✅" if section_score == section_total else "⚠️"

        bracket_icon = "✅" if r["bracket_count"] >= 3 else "⚠️"
        code_icon = "✅" if r["code_block_count"] >= 1 else "⚠️"
        role_icon = "✅" if r["has_role"] else "⚠️"
        interact_icon = "✅" if r["has_interaction"] else "⚠️"
        review_icon = "✅" if r["has_review"] else "⚠️"

        crit_count = len(r.get("critical_issues", []))
        warn_count = len(r.get("warnings", []))

        lines.append(
            f"| {i} | {skill_name} | {chain_icon}({chain_score}/{chain_total}) | "
            f"{section_icon}({section_score}/{section_total}) | "
            f"{bracket_icon}({r['bracket_count']}) | {code_icon}({r['code_block_count']}) | "
            f"{role_icon} | {interact_icon} | {review_icon} | "
            f"{r['char_count']} | {crit_count} | {warn_count} |"
        )

    lines.append("")

    lines.append("## 链路覆盖率统计")
    lines.append("")
    chain_stats = {}
    for chain_step in CHAIN_KEYWORDS.keys():
        count = sum(
            1 for r in all_results.values()
            if r.get("chain_present", {}).get(chain_step, False)
        )
        chain_stats[chain_step] = count

    lines.append("| 链路环节 | 覆盖Skill数 | 覆盖率 |")
    lines.append("|---------|------------|--------|")
    for step, count in chain_stats.items():
        rate = count / len(EXPECTED_SKILLS) * 100
        icon = "✅" if rate >= 90 else "⚠️" if rate >= 70 else "❌"
        lines.append(f"| {step} | {count}/{len(EXPECTED_SKILLS)} | {icon} {rate:.1f}% |")
    lines.append("")

    lines.append("## 字数分布")
    lines.append("")
    char_counts = [
        r["char_count"] for r in all_results.values()
        if r["status"] != "MISSING"
    ]
    if char_counts:
        lines.append(f"| 统计项 | 值 |")
        lines.append(f"|--------|-----|")
        lines.append(f"| 最短 | {min(char_counts)} 字符 |")
        lines.append(f"| 最长 | {max(char_counts)} 字符 |")
        lines.append(f"| 平均 | {sum(char_counts)//len(char_counts)} 字符 |")
        lines.append(f"| 中位数 | {sorted(char_counts)[len(char_counts)//2]} 字符 |")

        short_skills = [
            name for name, r in all_results.items()
            if r.get("char_count", 0) < 500 and r["status"] != "MISSING"
        ]
        if short_skills:
            lines.append("")
            lines.append("### 字数偏短的Skill (<500字符)")
            for s in short_skills:
                lines.append(f"- {s}: {all_results[s]['char_count']}字符")
    lines.append("")

    report_content = "\n".join(lines)
    REPORT_PATH.write_text(report_content, encoding="utf-8")
    print(f"\n深度测试报告已生成: {REPORT_PATH}")

    print(f"\n{'='*70}")
    print(f"深度测试完成:")
    print(f"  ✅ 完全通过: {pass_count}")
    print(f"  ⚠️ 存在问题: {issue_count}")
    print(f"  ❌ 文件缺失: {missing_count}")
    print(f"  严重问题: {total_issues}")
    print(f"  警告: {total_warnings}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
