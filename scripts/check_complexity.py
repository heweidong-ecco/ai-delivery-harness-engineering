```python
import ast
import sys
from pathlib import Path

MAX_COMPLEXITY = 10
MAX_FUNCTION_LINES = 50
MAX_NESTING = 4


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.errors: list[str] = []
        self._depth = 0

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        lines = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
        if lines > MAX_FUNCTION_LINES:
            self.errors.append(
                f"{self.path}:{node.lineno} function {node.name} too long ({lines} lines)"
            )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self._depth += 1
        if self._depth > MAX_NESTING:
            self.errors.append(f"{self.path}:{node.lineno} nesting too deep")
        self.generic_visit(node)
        self._depth -= 1


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
    errors: list[str] = []

    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        visitor = ComplexityVisitor(path)
        visitor.visit(tree)
        errors.extend(visitor.errors)

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print("Complexity check passed")


if __name__ == "__main__":
    main()
