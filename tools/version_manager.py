#!/usr/bin/env python3
"""版本存档与回滚管理器

Usage:
    python version_manager.py --action <backup|rollback|list> --slug <slug> --base-dir <path> [--version <v>]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


FILES_TO_BACKUP = ["project.md", "persona.md", "SKILL.md", "meta.json"]


def backup(base_dir: str, slug: str) -> str:
    root = Path(base_dir) / slug
    meta_path = root / "meta.json"
    if not meta_path.exists():
        print("错误：meta.json 不存在", file=sys.stderr)
        sys.exit(1)

    with meta_path.open("r", encoding="utf-8") as handle:
        meta = json.load(handle)

    version = meta.get("version", "v0")
    backup_name = f"{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir = root / "versions" / backup_name
    backup_dir.mkdir(parents=True, exist_ok=True)

    for file_name in FILES_TO_BACKUP:
        source = root / file_name
        if source.exists():
            shutil.copy2(source, backup_dir / file_name)

    print(f"已备份版本 {backup_name} 到 {backup_dir}")
    return backup_name


def list_versions(base_dir: str, slug: str) -> None:
    versions_dir = Path(base_dir) / slug / "versions"
    if not versions_dir.is_dir():
        print("没有历史版本。")
        return

    versions = sorted(path.name for path in versions_dir.iterdir() if path.is_dir())
    if not versions:
        print("没有历史版本。")
        return

    print(f"历史版本（共 {len(versions)} 个）：\n")
    for version in reversed(versions):
        print(f"  {version}")


def rollback(base_dir: str, slug: str, version: str) -> None:
    root = Path(base_dir) / slug
    versions_dir = root / "versions"
    candidates = [path for path in versions_dir.iterdir() if path.is_dir() and path.name.startswith(version)]

    if not candidates:
        print(f"错误：找不到版本 {version}", file=sys.stderr)
        list_versions(base_dir, slug)
        sys.exit(1)

    target = sorted(candidates)[0]
    backup(base_dir, slug)
    for file_name in FILES_TO_BACKUP:
        source = target / file_name
        destination = root / file_name
        if source.exists():
            shutil.copy2(source, destination)

    print(f"已回滚到版本 {target.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="版本管理器")
    parser.add_argument("--action", required=True, choices=["backup", "rollback", "list"])
    parser.add_argument("--slug", required=True, help="甲方代号")
    parser.add_argument("--base-dir", default="./clients", help="基础目录")
    parser.add_argument("--version", help="回滚目标版本")
    args = parser.parse_args()

    if args.action == "backup":
        backup(args.base_dir, args.slug)
    elif args.action == "list":
        list_versions(args.base_dir, args.slug)
    elif args.action == "rollback":
        if not args.version:
            print("错误：rollback 需要 --version 参数", file=sys.stderr)
            sys.exit(1)
        rollback(args.base_dir, args.slug, args.version)


if __name__ == "__main__":
    main()
