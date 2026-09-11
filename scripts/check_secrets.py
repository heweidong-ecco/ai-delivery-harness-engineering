import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key"),
    (re.compile(r"(?i)api[_-]?key\s*=\s*['\"][^'\"]{16,}"), "API Key"),
    (re.compile(r"(?i)secret\s*=\s*['\"][^'\"]{8,}"), "Secret"),
    (re.compile(r"(?i)password\s*=\s*['\"][^'\"]{4,}"), "Password"),
    (re.compile(r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"), "Private Key"),
    (re.compile(r"(?i)bearer\s+[a-z0-9\-._~+/]+=*"), "Bearer Token"),
]

# 跳过的是**构建/工具产物**,不是源码。补验证时发现:原先只跳了 __pycache__ 与
# .pytest_cache,于是扫描会一路走进 .mypy_cache / .ruff_cache / .import_linter_cache /
# htmlcov —— 那些目录里存的是源码片段与缓存数据,既慢又没有意义,
# 而且一旦某个缓存格式改了(把源码字面量也存进去),测试夹具里的假密钥就会被误报。
# (这是一处**加固**,不是已确认的失败 —— 当前实测为 0 命中。)
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".import_linter_cache",
    "htmlcov",
}
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz"}
SKIP_FILES = {".env.example", "check_secrets.py"}

# 行级豁免(与 detect-secrets 同款约定)。
#
# 为什么需要它:本仓的**测试必须包含假密钥**才能验证"扫描器真的会拦"
# (`tests/test_scripts.py` 用 `AKIA...` 与 `-----BEGIN RSA PRIVATE KEY-----`
# 当夹具)。原先只能整文件跳过 —— 那等于让这个文件**永久盲区**;
# 用行级标记,既放行已知夹具、又继续盯住该文件里新出现的真密钥。
#
# 这是**刻意放宽**:标记只豁免"当前这一行",不是整文件。
ALLOWLIST_MARKER = "pragma: allowlist secret"


def scan_file(path: Path) -> list[str]:
    errors: list[str] = []
    if path.suffix in SKIP_EXTS or path.name in SKIP_FILES:
        return errors

    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return errors

    for lineno, line in enumerate(content.splitlines(), start=1):
        if ALLOWLIST_MARKER in line:
            continue
        for pattern, name in PATTERNS:
            if pattern.search(line):
                errors.append(f"{path}:{lineno} possible {name}")
    return errors


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    errors: list[str] = []

    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            errors.extend(scan_file(path))

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print("Secret scan passed")


if __name__ == "__main__":
    main()
