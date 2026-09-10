#!/usr/bin/env python3
"""check_layers —— 分层依赖契约校验。

反外审 H6/H14(2026-09-11)。原实现两个病:

  · `RULES` 是**空列表**,`:35-37` 直接 `print("no rules configured, skipping")`
    —— **比没有更坏**:它给出"这里检查过了"的虚假安全感。
  · `.importlinter` 里**声明了**分层契约(api→service→domain→repository→adapter),
    但全仓 Makefile / CI / pre-commit **没有任何地方运行 import-linter** ——
    契约等于没写。

现在:分层契约的**单一来源**是 `.importlinter`;本脚本读它,并委托真正的
`lint-imports` 执行。骨架期 `src/` 尚无分层包(它们由项目填充时创建),
此时**明确标注为「未实现」并说明何时自动生效**,不再静默通过。

用法:
    python scripts/check_layers.py [src]
退出码:0 = 通过(含"骨架期未实现"的显式标注);1 = 违反契约或缺少依赖;2 = 配置错误。
"""

from __future__ import annotations

import configparser
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".importlinter"


def read_contract() -> tuple[list[str], str]:
    """从 .importlinter 读出分层契约的层列表与契约名。"""
    if not CONFIG.is_file():
        print("::error::.importlinter 不存在 —— 分层契约未定义")
        sys.exit(2)

    parser = configparser.ConfigParser()
    parser.read(CONFIG, encoding="utf-8")

    for section in parser.sections():
        if (
            section.startswith("importlinter:contract:")
            and parser.get(section, "type", fallback="") == "layers"
        ):
            raw = parser.get(section, "layers", fallback="")
            layers = [ln.strip() for ln in raw.splitlines() if ln.strip()]
            return layers, parser.get(section, "name", fallback=section)
    print("::error::.importlinter 里没有 type = layers 的契约")
    sys.exit(2)


def existing_layers(layers: list[str]) -> list[str]:
    """哪些层在磁盘上真的存在(有 __init__.py)。"""
    found: list[str] = []
    for layer in layers:
        package = ROOT / layer.replace(".", "/")
        if (package / "__init__.py").is_file():
            found.append(layer)
    return found


def main() -> int:
    layers, contract = read_contract()
    if not layers:
        print("::error::.importlinter 的 layers 为空 —— 契约没有内容")
        return 2

    present = existing_layers(layers)

    if not present:
        # 骨架期如实标注:不假装检查过,也不假装通过。
        print("⚠ [UNIMPLEMENTED] 分层契约已声明但尚未生效(骨架期)。")
        print(f"   契约「{contract}」声明了 {len(layers)} 层:{', '.join(layers)}")
        print("   但 src/ 下这些包都还不存在 —— 它们由项目填充时创建。")
        print("   一旦 src/ 出现上述任一包,本门禁立即变为硬校验(调用 lint-imports)。")
        return 0

    lint_imports = shutil.which("lint-imports")
    if lint_imports is None:
        # 缺依赖应失败,不应放行。
        print("::error::src/ 已有分层代码,但未安装 import-linter —— 无法校验分层契约。")
        print('::error::请执行:pip install -e ".[dev]"(dev 依赖已含 import-linter)')
        return 1

    result = subprocess.run(
        [lint_imports, "--config", str(CONFIG)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)

    if result.returncode != 0:
        print(f"::error::分层契约「{contract}」被违反(见上方 lint-imports 输出)")
        return 1

    print(f"✅ 分层契约「{contract}」通过({len(present)}/{len(layers)} 层已存在)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
