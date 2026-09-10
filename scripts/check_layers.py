import ast
import sys
from pathlib import Path

# 待项目填充：规则格式 (源前缀, 禁止导入前缀, 消息)
RULES: list[tuple[str, str, str]] = [
    # ("src/api", "src.repository", "api 不得直接依赖 repository"),
    # ("src/domain", "sqlalchemy", "domain 不得依赖 ORM"),
    # ("src/service", "requests", "service 不得直接 HTTP"),
]


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.errors: list[str] = []

    def _check(self, module: str, lineno: int) -> None:
        for prefix, banned, msg in RULES:
            if str(self.path).startswith(prefix) and module.startswith(banned):
                self.errors.append(f"{self.path}:{lineno} {msg}")

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._check(alias.name, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self._check(node.module, node.lineno)
        self.generic_visit(node)


def main() -> None:
    if not RULES:
        print("check_layers: no rules configured, skipping")
        return

    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
    errors: list[str] = []

    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        visitor = ImportVisitor(path)
        visitor.visit(tree)
        errors.extend(visitor.errors)

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print("Layer check passed")


if __name__ == "__main__":
    main()