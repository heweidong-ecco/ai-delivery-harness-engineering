#!/usr/bin/env python3
"""validate_schemas —— JSON Schema 自检 + 数据校验。

反外审 H6/H9(2026-09-11)。原实现两个病:

  · `:5-9` 在 jsonschema **未安装**时 `sys.exit(0)` —— **缺依赖却算通过**;
  · `:23-25` 在 `harness/schemas/data/` 不存在时直接 return(该目录确实不存在)
    —— 于是这个门禁**永远空转**,却看起来"检查过了"。

现在分两件事,且都如实汇报:

  ① **Schema 自检(始终执行,真校验)**:`harness/schemas/*.json` 必须是合法的
     JSON Schema(draft 2020-12)。这一条今天就能真的跑起来。
  ② **数据校验(有数据才跑)**:`harness/schemas/data/*.json` 各自套对应 schema;
     目录不存在时**明确标注「未实现」**,不静默通过。

用法:
    python scripts/validate_schemas.py
退出码:0 = 通过(含无数据时的显式标注);1 = 校验失败或缺少依赖;2 = 配置错误。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    # 缺依赖应 fail,不应 pass(原实现这里是 exit(0))。
    print("::error::未安装 jsonschema —— 无法校验 schema。")
    print('::error::请执行:pip install -e ".[dev]"(dev 依赖已含 jsonschema)')
    sys.exit(1)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "harness" / "schemas"
DATA_DIR = SCHEMA_DIR / "data"


def check_schema_files() -> list[str]:
    """① Schema 自检:每个 *.json 都必须是合法的 JSON Schema。"""
    errors: list[str] = []
    for schema_file in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            schema = json.loads(schema_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_file.name}: 不是合法 JSON({exc})")
            continue
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            errors.append(f"{schema_file.name}: 不是合法的 JSON Schema({exc.message})")
    return errors


def check_data_files() -> tuple[list[str], int]:
    """② 数据校验:返回 (错误列表, 校验过的数据文件数)。"""
    if not DATA_DIR.is_dir():
        return [], 0

    errors: list[str] = []
    checked = 0
    for data_file in sorted(DATA_DIR.glob("*.json")):
        schema_file = SCHEMA_DIR / f"{data_file.stem.split('-')[0]}-schema.json"
        if not schema_file.is_file():
            errors.append(f"{data_file.name}: 找不到对应的 schema({schema_file.name})")
            continue
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        data = json.loads(data_file.read_text(encoding="utf-8"))
        checked += 1
        for error in jsonschema.Draft202012Validator(schema).iter_errors(data):
            location = "/".join(str(p) for p in error.absolute_path) or "(根)"
            errors.append(f"{data_file.name} @ {location}: {error.message}")
    return errors, checked


def main() -> int:
    if not SCHEMA_DIR.is_dir():
        print(f"::error::schema 目录不存在: {SCHEMA_DIR}")
        return 2

    errors = check_schema_files()
    data_errors, checked = check_data_files()
    errors.extend(data_errors)

    if errors:
        print(f"Schema 校验 FAILED({len(errors)} 项):")
        for error in errors:
            print(f"  - {error}")
        return 1

    schema_count = len(list(SCHEMA_DIR.glob("*.json")))
    if checked == 0:
        print(f"✅ Schema 自检通过({schema_count} 个 schema 均为合法 JSON Schema)")
        print(
            "⚠ [UNIMPLEMENTED] harness/schemas/data/ 不存在 —— "
            "尚无数据文件可校验;放入数据后本门禁自动开始校验。"
        )
    else:
        print(f"✅ Schema 校验通过({schema_count} 个 schema,{checked} 个数据文件)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
