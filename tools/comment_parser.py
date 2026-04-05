#!/usr/bin/env python3
"""批注 / 评论汇总解析器

Usage:
    python comment_parser.py --file <path> --output <output_path>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path


ADJECTIVES = [
    "高级",
    "大气",
    "简洁",
    "舒服",
    "有质感",
    "太满",
    "太乱",
    "太像活动页",
    "太互联网",
    "不够品牌",
]


def read_text(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)

    if file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            return json.dumps(json.load(handle), ensure_ascii=False, indent=2)

    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def write_report(output_path: str, file_path: str, text: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    adjective_counts = Counter()
    for adjective in ADJECTIVES:
        count = text.count(adjective)
        if count:
            adjective_counts[adjective] = count

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("# 批注 / 评论分析\n\n")
        handle.write(f"来源文件：{file_path}\n\n")

        handle.write("## 高频形容词\n")
        if adjective_counts:
            for word, count in adjective_counts.most_common():
                handle.write(f"- {word}: {count} 次\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        handle.write("## 代表性评论\n")
        if lines:
            for index, line in enumerate(lines[:12], start=1):
                handle.write(f"{index}. {line}\n")
        else:
            handle.write("- [未识别]\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="批注 / 评论汇总解析器")
    parser.add_argument("--file", required=True, help="输入文件路径")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    try:
        text = read_text(args.file)
    except FileNotFoundError:
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)

    write_report(args.output, args.file, text)
    print(f"分析完成，结果已写入 {args.output}")


if __name__ == "__main__":
    main()
