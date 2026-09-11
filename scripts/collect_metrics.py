import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def git_count(pattern: str) -> int:
    result = subprocess.run(
        ["git", "log", "--oneline", f"--grep={pattern}"],
        capture_output=True,
        text=True,
    )
    return len([line for line in result.stdout.splitlines() if line.strip()])


def main() -> None:
    out_dir = Path("harness/metrics/data")
    out_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "collected_at": datetime.now(UTC).isoformat(),
        "rule_commits": git_count("rule:"),
        "agent_commits": git_count("agent:"),
        "docs_commits": git_count("docs:"),
        "fix_commits": git_count("fix:"),
    }

    out_file = out_dir / f"metrics-{datetime.now(UTC):%Y%m%d}.json"
    # 末尾带换行 —— 与 scripts/stage_gate.py 同因(空跑-4):输出应满足
    # `end-of-file-fixer`。本目录被 gitignore,故钩子看不到,属同类潜在问题一并修掉。
    out_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Metrics written to {out_file}")


if __name__ == "__main__":
    main()
