#!/usr/bin/env python3
"""聊天记录分析器

Usage:
    python chat_parser.py --file <path> --target <name> --output <output_path>
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


KEYWORDS = [
    "高级",
    "高级感",
    "老板",
    "预算",
    "节点",
    "上线",
    "品牌",
    "转化",
    "不行",
    "再来",
    "重做",
    "简单",
    "大气",
    "感觉",
    "方向",
]

VAGUE_PATTERNS = ["高级一点", "感觉不对", "先顺一顺", "再看看", "先不要定"]
PRESSURE_PATTERNS = ["今天", "尽快", "马上", "现在", "今晚", "明天一早", "先上线"]


def read_text(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)

    if file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            data = json.load(handle)
        return json.dumps(data, ensure_ascii=False, indent=2)

    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def extract_messages(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def count_patterns(text: str, patterns: list[str]) -> list[tuple[str, int]]:
    counts = [(pattern, text.count(pattern)) for pattern in patterns]
    return [item for item in counts if item[1] > 0]


def analyze(text: str, target: str) -> dict:
    messages = extract_messages(text)
    keyword_counts = Counter()
    for word in KEYWORDS:
        count = text.count(word)
        if count:
            keyword_counts[word] = count

    avg_length = round(sum(len(msg) for msg in messages) / len(messages), 1) if messages else 0.0
    question_count = text.count("?") + text.count("？")
    exclaim_count = text.count("!") + text.count("！")

    target_lines = [msg for msg in messages if target in msg] if target else []
    samples = target_lines[:10] if target_lines else messages[:10]

    return {
        "message_count": len(messages),
        "avg_length": avg_length,
        "top_keywords": keyword_counts.most_common(8),
        "vague_patterns": count_patterns(text, VAGUE_PATTERNS),
        "pressure_patterns": count_patterns(text, PRESSURE_PATTERNS),
        "question_count": question_count,
        "exclaim_count": exclaim_count,
        "samples": samples,
    }


def write_report(output_path: str, file_path: str, target: str, report: dict) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(f"# 聊天记录分析 — {target or '未指定对象'}\n\n")
        handle.write(f"来源文件：{file_path}\n")
        handle.write(f"消息条数：{report['message_count']}\n")
        handle.write(f"平均单条长度：{report['avg_length']}\n")
        handle.write(f"问号数量：{report['question_count']}\n")
        handle.write(f"感叹号数量：{report['exclaim_count']}\n\n")

        handle.write("## 高频关键词\n")
        if report["top_keywords"]:
            for word, count in report["top_keywords"]:
                handle.write(f"- {word}: {count} 次\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        handle.write("## 模糊反馈模式\n")
        if report["vague_patterns"]:
            for word, count in report["vague_patterns"]:
                handle.write(f"- {word}: {count} 次\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        handle.write("## 压力表达模式\n")
        if report["pressure_patterns"]:
            for word, count in report["pressure_patterns"]:
                handle.write(f"- {word}: {count} 次\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        handle.write("## 代表性样本\n")
        if report["samples"]:
            for index, sample in enumerate(report["samples"], start=1):
                handle.write(f"{index}. {sample}\n")
        else:
            handle.write("- [未识别]\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="聊天记录分析器")
    parser.add_argument("--file", required=True, help="输入文件路径")
    parser.add_argument("--target", default="", help="目标甲方名称")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    try:
        text = read_text(args.file)
    except FileNotFoundError:
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    report = analyze(text, args.target)
    write_report(args.output, args.file, args.target, report)
    print(f"分析完成，结果已写入 {args.output}")


if __name__ == "__main__":
    main()
