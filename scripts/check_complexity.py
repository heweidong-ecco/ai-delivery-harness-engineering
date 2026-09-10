"""复杂度检查：函数长度、嵌套深度、圈复杂度。"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

MAX_FUNCTION_LINES = 50
MAX_NESTING = 4
MAX_CYCLOMATIC = 10
MAX_FUNCTION_ARGS = 5
MAX_BRANCHES = 12

BRANCH_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.ExceptHandler,
    ast.With,
    ast.AsyncWith,
    ast.BoolOp,
    ast.IfExp,
    ast.comprehension,
    ast.Match,
    ast.Try,
)


def cyclomatic_complexity(node: ast.AST) -> int:
    """计算圈复杂度：1 + 分支数。"""
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, BRANCH_NODES):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
    return complexity


def max_nesting(node: ast.AST, depth: int = 0) -> int:
    """计算最大嵌套深度。"""
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)):
            max_depth = max(max_depth, max_nesting(child, depth + 1))
        else:
            max_depth = max(max_depth, max_nesting(child, depth))
    return max_depth


def count_branches(node: ast.AST) -> int:
    """统计分支数。"""
    count = 0
    for child in ast.walk(node):
        if isinstance(child, BRANCH_NODES):
            count += 1
    return count


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.errors: list[str] = []

    def _report(self, lineno: int, rule_id: str, message: str) -> None:
        self.errors.append(f"{self.path}:{lineno} [{rule_id}] {message}")

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        # 函数长度
        if node.end_lineno and node.lineno:
            lines = node.end_lineno - node.lineno + 1
            if lines > MAX_FUNCTION_LINES:
                self._report(
                    node.lineno,
                    "CPLX-001",
                    f"函数 {node.name} 过长 ({lines} 行, 上限 {MAX_FUNCTION_LINES})",
                )

        # 参数数量
        args = node.args
        total_args = len(args.args) + len(args.posonlyargs) + len(args.kwonlyargs)
        if args.vararg:
            total_args += 1
        if args.kwarg:
            total_args += 1
        if total_args > MAX_FUNCTION_ARGS:
            self._report(
                node.lineno,
                "CPLX-002",
                f"函数 {node.name} 参数过多 ({total_args} 个, 上限 {MAX_FUNCTION_ARGS})",
            )

        # 圈复杂度
        complexity = cyclomatic_complexity(node)
        if complexity > MAX_CYCLOMATIC:
            self._report(
                node.lineno,
                "CPLX-003",
                f"函数 {node.name} 圈复杂度过高 ({complexity}, 上限 {MAX_CYCLOMATIC})",
            )

        # 嵌套深度
        nesting = max_nesting(node)
        if nesting > MAX_NESTING:
            self._report(
                node.lineno,
                "CPLX-004",
                f"函数 {node.name} 嵌套过深 ({nesting}, 上限 {MAX_NESTING})",
            )

        # 分支数
        branches = count_branches(node)
        if branches > MAX_BRANCHES:
            self._report(
                node.lineno,
                "CPLX-005",
                f"函数 {node.name} 分支过多 ({branches}, 上限 {MAX_BRANCHES})",
            )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")

    if not root.exists():
        print(f"Path not found: {root}")
        raise SystemExit(1)

    errors: list[str] = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        visitor = ComplexityVisitor(path)
        visitor.visit(tree)
        errors.extend(visitor.errors)

    if errors:
        print("\n".join(errors))
        print(f"\nTotal: {len(errors)} errors")
        raise SystemExit(1)

    print(
        f"Complexity check passed "
        f"(function<={MAX_FUNCTION_LINES} lines, "
        f"nesting<={MAX_NESTING}, "
        f"cyclomatic<={MAX_CYCLOMATIC}, "
        f"args<={MAX_FUNCTION_ARGS})"
    )


if __name__ == "__main__":
    main()
