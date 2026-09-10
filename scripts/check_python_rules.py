import ast
import sys
from pathlib import Path



PRICE_HINTS = ("price", "amount", "money", "金额", "价格")
HTTP_METHODS = {"get", "post", "put", "delete", "patch", "request"}
HTTP_MODULES = {"requests", "httpx"}


class Visitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.errors: list[str] = []

    def _is_float(self, node: ast.expr | None) -> bool:
        if node is None:
            return False
        if isinstance(node, ast.Name) and node.id == "float":
            return True
        if isinstance(node, ast.Attribute) and node.attr == "float":
            return True
        return False

    def visit_arg(self, node: ast.arg) -> None:
        name = node.arg.lower()
        if any(h in name for h in PRICE_HINTS) and self._is_float(node.annotation):
            self.errors.append(
                f"{self.path}:{node.lineno} 价格/金额字段禁止使用 float: {node.arg}"
            )
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        name = ""
        if isinstance(node.target, ast.Name):
            name = node.target.id.lower()
        if any(h in name for h in PRICE_HINTS) and self._is_float(node.annotation):
            self.errors.append(
                f"{self.path}:{node.lineno} 价格/金额字段禁止使用 float: {name}"
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr in HTTP_METHODS:
            if isinstance(func.value, ast.Name) and func.value.id in HTTP_MODULES:
                if not any(kw.arg == "timeout" for kw in node.keywords):
                    self.errors.append(
                        f"{self.path}:{node.lineno} 外部 HTTP 调用必须设置 timeout"
                    )
        self.generic_visit(node)


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
    errors: list[str] = []

    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        visitor = Visitor(path)
        visitor.visit(tree)
        errors.extend(visitor.errors)

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print("Python harness rules passed")


if __name__ == "__main__":
    main()
