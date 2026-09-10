import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("jsonschema not installed, skipping schema validation")
    sys.exit(0)


def validate(schema_path: Path, data_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(data_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [str(e.message) for e in validator.iter_errors(data)]


def main() -> None:
    root = Path("harness/schemas")
    data_dir = Path("harness/schemas/data")

    if not data_dir.exists():
        print("No schema data to validate")
        return

    errors: list[str] = []
    for data_file in data_dir.glob("*.json"):
        schema_file = root / f"{data_file.stem.split('-')[0]}-schema.json"
        if schema_file.exists():
            errors.extend(validate(schema_file, data_file))

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)

    print("Schema validation passed")


if __name__ == "__main__":
    main()