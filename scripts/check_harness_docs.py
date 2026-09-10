from pathlib import Path

REQUIRED = [
    "harness/rules/project-structure.md",
    "harness/rules/dev-process.md",
    "harness/rules/coding-standard.md",
    "harness/rules/python-coding-standard.md",
    "harness/rules/python-layers.md",
    "harness/agent/application-owner.md",
    "harness/changes/_template/requirement-analysis.md",
    "harness/changes/_template/ci-result.md",
]


def main() -> None:
    missing = [p for p in REQUIRED if not Path(p).exists()]
    if missing:
        raise SystemExit("Missing harness docs:\n" + "\n".join(missing))
    print("Harness docs check passed")


if __name__ == "__main__":
    main()
