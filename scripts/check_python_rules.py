"""Python Harness 规则检查。

规则注册表模式：每条规则独立函数，可单独启用/禁用。
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

# ============================================================
# 规则上下文
# ============================================================


@dataclass
class RuleContext:
    """规则执行上下文。"""

    path: Path
    tree: ast.AST
    errors: list[str] = field(default_factory=list)

    def report(self, lineno: int, rule_id: str, message: str) -> None:
        self.errors.append(f"{self.path}:{lineno} [{rule_id}] {message}")


# ============================================================
# 规则实现
# ============================================================

PRICE_HINTS = ("price", "amount", "money", "金额", "价格")
HTTP_METHODS = {"get", "post", "put", "delete", "patch", "request"}
HTTP_MODULES = {"requests", "httpx"}


def _is_float_annotation(node: ast.expr | None) -> bool:
    if node is None:
        return False
    if isinstance(node, ast.Name) and node.id == "float":
        return True
    if isinstance(node, ast.Attribute) and node.attr == "float":
        return True
    return False


def rule_price_no_float(ctx: RuleContext) -> None:
    """PRICE-001：价格/金额字段禁止 float。"""
    for node in ast.walk(ctx.tree):
        if isinstance(node, ast.arg):
            name = node.arg.lower()
            if any(h in name for h in PRICE_HINTS) and _is_float_annotation(node.annotation):
                ctx.report(node.lineno, "PRICE-001", f"价格/金额字段禁止 float: {node.arg}")
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                name = node.target.id.lower()
                if any(h in name for h in PRICE_HINTS) and _is_float_annotation(node.annotation):
                    ctx.report(node.lineno, "PRICE-001", f"价格/金额字段禁止 float: {name}")


def rule_http_timeout(ctx: RuleContext) -> None:
    """HTTP-001：外部 HTTP 调用必须设置 timeout。"""
    for node in ast.walk(ctx.tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if func.attr not in HTTP_METHODS:
            continue
        if not isinstance(func.value, ast.Name):
            continue
        if func.value.id not in HTTP_MODULES:
            continue
        if not any(kw.arg == "timeout" for kw in node.keywords):
            ctx.report(node.lineno, "HTTP-001", "外部 HTTP 调用必须设置 timeout")


def rule_no_bare_except(ctx: RuleContext) -> None:
    """ERR-001：禁止裸 except。"""
    for node in ast.walk(ctx.tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            ctx.report(node.lineno, "ERR-001", "禁止裸 except")


def rule_no_print(ctx: RuleContext) -> None:
    """LOG-001：禁止 print。"""
    for node in ast.walk(ctx.tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "print":
                ctx.report(node.lineno, "LOG-001", "禁止 print，请用 logging")


def rule_no_hardcoded_secrets(ctx: RuleContext) -> None:
    """SEC-001：禁止硬编码密钥。"""
    suspicious_names = {"password", "secret", "token", "api_key", "apikey"}
    for node in ast.walk(ctx.tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.lower() in suspicious_names:
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        if len(node.value.value) >= 8:
                            ctx.report(node.lineno, "SEC-001", f"疑似硬编码密钥: {target.id}")


def rule_no_naive_datetime(ctx: RuleContext) -> None:
    """TZ-001：禁止 naive datetime.now()。"""
    for node in ast.walk(ctx.tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "now":
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "datetime":
                        if not node.args and not any(kw.arg == "tz" for kw in node.keywords):
                            ctx.report(node.lineno, "TZ-001", "禁止 naive datetime.now()，请用 datetime.now(UTC)")
                if node.func.attr == "utcnow":
                    ctx.report(node.lineno, "TZ-001", "datetime.utcnow() 已废弃，请用 datetime.now(UTC)")


def rule_no_mutable_default(ctx: RuleContext) -> None:
    """PY-001：禁止可变默认参数。"""
    for node in ast.walk(ctx.tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults + node.args.kw_defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    ctx.report(node.lineno, "PY-001", f"函数 {node.name} 使用可变默认参数")
                elif isinstance(default, ast.Call):
                    if isinstance(default.func, ast.Name) and default.func.id in {"list", "dict", "set"}:
                        ctx.report(node.lineno, "PY-001", f"函数 {node.name} 使用可变默认参数")


def rule_no_eval_exec(ctx: RuleContext) -> None:
    """SEC-002：禁止 eval/exec。"""
    banned = {"eval", "exec", "compile", "__import__"}
    for node in ast.walk(ctx.tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in banned:
                ctx.report(node.lineno, "SEC-002", f"禁止使用 {node.func.id}")


# ============================================================
# 规则注册表
# ============================================================

RuleFunc = Callable[[RuleContext], None]

RULES: list[tuple[str, RuleFunc]] = [
    ("PRICE-001", rule_price_no_float),
    ("HTTP-001", rule_http_timeout),
    ("ERR-001", rule_no_bare_except),
    ("LOG-001", rule_no_print),
    ("SEC-001", rule_no_hardcoded_secrets),
    ("SEC-002", rule_no_eval_exec),
    ("TZ-001", rule_no_naive_datetime),
    ("PY-001", rule_no_mutable_default),
    # 待项目填充：
    # ("PRICE-002", rule_price_use_decimal),
    # ("DB-001", rule_no_select_star),
    # ("CACHE-001", rule_cache_ttl_required),
    # ...
]

# 可通过环境变量禁用的规则
DISABLED_RULES: set[str] = set()


# ============================================================
# 执行器
# ============================================================


def check_file(path: Path) -> list[str]:
    """检查单个文件。"""
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    try:
        tree = ast.parse(content, filename=str(path))
    except SyntaxError as e:
        return [f"{path}:{e.lineno} [SYNTAX] {e.msg}"]

    ctx = RuleContext(path=path, tree=tree)

    for rule_id, rule_func in RULES:
        if rule_id in DISABLED_RULES:
            continue
        try:
            rule_func(ctx)
        except Exception as e:  # noqa: BLE001
            ctx.report(0, rule_id, f"规则执行异常: {e}")

    return ctx.errors


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")

    if not root.exists():
        print(f"Path not found: {root}")
        raise SystemExit(1)

    errors: list[str] = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        errors.extend(check_file(path))

    if errors:
        print("\n".join(errors))
        print(f"\nTotal: {len(errors)} errors")
        raise SystemExit(1)

    print(f"Python harness rules passed ({len(RULES)} rules, {len(DISABLED_RULES)} disabled)")


if __name__ == "__main__":
    main()
