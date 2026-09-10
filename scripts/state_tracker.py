import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: state_tracker.py <REQ> <stage> <status>")
        raise SystemExit(1)

    req, stage, status = sys.argv[1], sys.argv[2], sys.argv[3]

    out_dir = Path("harness/state")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / f"{req}.json"
    now = datetime.now(timezone.utc).isoformat()

    if out_file.exists():
        data = json.loads(out_file.read_text(encoding="utf-8"))
    else:
        data = {"req": req, "history": []}

    data["stage"] = stage
    data["status"] = status
    data["updated_at"] = now
    data["history"].append({"stage": stage, "status": status, "at": now})

    out_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"State updated: {out_file}")


if __name__ == "__main__":
    main()
