#!/usr/bin/env python3
"""会议纪要 / 转写解析器

Usage:
    python meeting_parser.py --file <path> --output <output_path>
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


STAKEHOLDERS = ["老板", "市场", "产品", "设计", "研发", "法务", "运营", "销售", "CEO"]
DECISION_HINTS = ["决定", "确认", "改", "先做", "不用", "保留", "删掉", "上线", "延期"]
ACTION_HINTS = ["待办", "TODO", "action", "跟进", "负责", "需要", "本周"]


def read_text(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)
    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def matching_lines(text: str, keywords: list[str]) -> list[str]:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line and any(keyword.lower() in line.lower() for keyword in keywords):
            lines.append(line)
    return lines[:12]


def write_report(output_path: str, file_path: str, text: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("# 会议纪要分析\n\n")
        handle.write(f"来源文件：{file_path}\n\n")

        handle.write("## 涉及的角色\n")
        stakeholders = matching_lines(text, STAKEHOLDERS)
        if stakeholders:
            for line in stakeholders:
                handle.write(f"- {line}\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        handle.write("## 决策相关片段\n")
        decisions = matching_lines(text, DECISION_HINTS)
        if decisions:
            for line in decisions:
                handle.write(f"- {line}\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        handle.write("## 待办与跟进\n")
        actions = matching_lines(text, ACTION_HINTS)
        if actions:
            for line in actions:
                handle.write(f"- {line}\n")
        else:
            handle.write("- [未识别]\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="会议纪要 / 转写解析器")
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
