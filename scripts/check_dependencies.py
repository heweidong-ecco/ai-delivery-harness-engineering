import subprocess
import sys


def main() -> None:
    result = subprocess.run(
        ["pip-audit", "--strict"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)
    print("Dependency audit passed")


if __name__ == "__main__":
    main()
