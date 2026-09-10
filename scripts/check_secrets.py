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

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}
SKIP_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz"}
SKIP_FILES = {".env.example", "check_secrets.py"}


def scan_file(path: Path) -> list[str]:
    errors: list[str] = []
    if path.suffix in SKIP_EXTS or path.name in SKIP_FILES:
        return errors

    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return errors

    for lineno, line in enumerate(content.splitlines(), start=1):
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