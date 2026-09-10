from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def harness_root(project_root: Path) -> Path:
    return project_root / "harness"


@pytest.fixture
def sample_req_dir(tmp_path: Path) -> Iterator[Path]:
    req_dir = tmp_path / "REQ-TEST"
    req_dir.mkdir()
    for name in [
        "requirement-analysis.md",
        "task-breakdown.md",
        "coding-report.md",
        "unit-test-report.md",
        "ci-result.md",
        "deploy-validation.md",
    ]:
        (req_dir / name).write_text("# placeholder\n", encoding="utf-8")
    yield req_dir