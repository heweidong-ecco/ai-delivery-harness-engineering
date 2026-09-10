import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r"^(feat|fix|docs|ci|chore|rule|agent|test)(\(.+\))?: .{1,72}$"
)

ALLOWED = {"feat", "fix", "docs", "ci", "chore", "rule", "agent", "test"}


def main() -> None:
    msg_file = Path(sys.argv[1])
    first_line = msg_file.read_text(encoding="utf-8").splitlines()[0]

    if not PATTERN.match(first_line):
        print(f"Invalid commit message: {first_line}")
        print(f"Allowed types: {sorted(ALLOWED)}")
        raise SystemExit(1)

    print("Commit message check passed")


if __name__ == "__main__":
    main()