import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r'["\']中文["\']'), "硬编码中文"),
    (re.compile(r"datetime\.now\(\)"), "naive datetime"),
    (re.compile(r"datetime\.utcnow\(\)"), "已废弃 utcnow"),
]

SKIP = {"tests", ".venv", "venv"}


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
    errors: list[str] = []

    for path in root.rglob("*.py"):
        if any(s in path.parts for s in SKIP):
            continue
        content = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(content.splitlines(), start=1):
            for pattern, name in PATTERNS:
                if pattern.search(line):
                    errors.append(f"{path}:{lineno} {name}")

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print("i18n check passed")


if __name__ == "__main__":
    main()
