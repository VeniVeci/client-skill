#!/usr/bin/env python3
"""PRD / brief 解析器

Usage:
    python brief_parser.py --file <path> --output <output_path>
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


KEYWORD_GROUPS = {
    "核心目标": ["目标", "目的", "转化", "增长", "品牌", "GMV", "留资"],
    "预算约束": ["预算", "成本", "资源", "ROI"],
    "时间节点": ["时间", "节点", "排期", "上线", "交付", "deadline", "本周", "下周", "周一", "周二", "周三", "周四", "周五"],
    "红线禁区": ["不要", "禁止", "必须", "不能", "法务", "风险"],
}


def read_text(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)

    if file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            return json.dumps(json.load(handle), ensure_ascii=False, indent=2)

    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def extract_lines(text: str, keywords: list[str]) -> list[str]:
    results = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and any(keyword.lower() in stripped.lower() for keyword in keywords):
            results.append(stripped)
    return results[:10]


def write_report(output_path: str, file_path: str, text: str) -> None:
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    headings = [line.strip() for line in text.splitlines() if re.match(r"^\s{0,3}(#|\d+\.|[一二三四五六七八九十]+、)", line)]

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("# Brief / PRD 分析\n\n")
        handle.write(f"来源文件：{file_path}\n\n")

        handle.write("## 识别到的标题\n")
        if headings:
            for heading in headings[:12]:
                handle.write(f"- {heading}\n")
        else:
            handle.write("- [未识别]\n")
        handle.write("\n")

        for title, keywords in KEYWORD_GROUPS.items():
            handle.write(f"## {title}\n")
            lines = extract_lines(text, keywords)
            if lines:
                for line in lines:
                    handle.write(f"- {line}\n")
            else:
                handle.write("- [未识别]\n")
            handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="PRD / brief 解析器")
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
