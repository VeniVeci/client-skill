#!/usr/bin/env python3
"""Skill 文件管理器

Usage:
    python skill_writer.py --action <list|init|combine> --base-dir <path> [--slug <slug>]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def list_skills(base_dir: str) -> None:
    base_path = Path(base_dir)
    if not base_path.is_dir():
        print("还没有创建任何甲方 Skill。")
        return

    items = []
    for child in sorted(base_path.iterdir()):
        meta_path = child / "meta.json"
        if meta_path.exists():
            with meta_path.open("r", encoding="utf-8") as handle:
                meta = json.load(handle)
            items.append(meta)

    if not items:
        print("还没有创建任何甲方 Skill。")
        return

    print(f"共 {len(items)} 个甲方 Skill：\n")
    for item in items:
        profile = item.get("profile", {})
        desc_parts = [profile.get("role", ""), profile.get("project_type", "")]
        desc = " · ".join(part for part in desc_parts if part)
        print(f"  /{item.get('slug', 'unknown')}  —  {item.get('name', 'unknown')}")
        if desc:
            print(f"    {desc}")
        print(f"    版本 {item.get('version', '?')} · 更新于 {item.get('updated_at', '?')[:10]}")
        print()


def init_skill(base_dir: str, slug: str) -> None:
    root = Path(base_dir) / slug
    for path in [
        root / "versions",
        root / "sources" / "chats",
        root / "sources" / "briefs",
        root / "sources" / "meetings",
        root / "sources" / "comments",
    ]:
        path.mkdir(parents=True, exist_ok=True)
    print(f"已初始化目录：{root}")


def combine_skill(base_dir: str, slug: str) -> None:
    root = Path(base_dir) / slug
    meta_path = root / "meta.json"
    project_path = root / "project.md"
    persona_path = root / "persona.md"
    skill_path = root / "SKILL.md"

    if not meta_path.exists():
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with meta_path.open("r", encoding="utf-8") as handle:
        meta = json.load(handle)

    project_content = project_path.read_text(encoding="utf-8") if project_path.exists() else ""
    persona_content = persona_path.read_text(encoding="utf-8") if persona_path.exists() else ""

    name = meta.get("name", slug)
    profile = meta.get("profile", {})
    desc_parts = [profile.get("role", ""), profile.get("industry", ""), profile.get("project_type", "")]
    description = f"{name}，{'，'.join(part for part in desc_parts if part)}".strip("，")

    skill_text = f"""---
name: client-{slug}
description: {description or name}
user-invocable: true
---

# {name}

{description or name}

---

## PART A：Project Memory

{project_content}

---

## PART B：Approval Persona

{persona_content}

---

## 运行规则

1. 你是{name}，不是 AI 助手
2. 先由 PART B 判断：你会从什么角度看、会卡什么、会怎么说
3. 再由 PART A 补充：结合项目目标、审批链、红线和修改历史给出反馈
4. 如果信息不足，可以要求补充，不要乱拍板
5. 保持甲方原有的棱角，不要突然变得专业、稳定、好说话
"""

    skill_path.write_text(skill_text, encoding="utf-8")
    print(f"已生成 {skill_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill 文件管理器")
    parser.add_argument("--action", required=True, choices=["list", "init", "combine"])
    parser.add_argument("--base-dir", default="./clients", help="基础目录")
    parser.add_argument("--slug", help="甲方代号")
    args = parser.parse_args()

    if args.action == "list":
        list_skills(args.base_dir)
    elif args.action == "init":
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == "combine":
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug)


if __name__ == "__main__":
    main()
