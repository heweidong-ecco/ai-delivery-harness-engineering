import json
import sys
from pathlib import Path


def main() -> None:
    report_path = Path(sys.argv[1])
    report = json.loads(report_path.read_text(encoding="utf-8"))
    summary = report.get("summary", {})

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    errors = summary.get("error", 0)

    if total <= 0:
        raise SystemExit("No tests collected")
    if failed or errors:
        raise SystemExit(f"Tests failed: failed={failed}, errors={errors}")
    if passed != total:
        raise SystemExit(f"Passed {passed} != total {total}")

    print(f"Pytest gate passed: total={total}, passed={passed}")


if __name__ == "__main__":
    main()
