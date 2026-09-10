import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: audit_log.py <event> <detail>")
        raise SystemExit(1)

    event = sys.argv[1]
    detail = sys.argv[2]

    out_dir = Path("harness/audit")
    out_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    out_file = out_dir / f"{now:%Y%m%d-%H%M%S}-{event}.md"
    out_file.write_text(
        f"# {event}\n\n- 时间：{now.isoformat()}\n- 详情：{detail}\n",
        encoding="utf-8",
    )
    print(f"Audit written to {out_file}")


if __name__ == "__main__":
    main()
