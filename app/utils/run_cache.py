import json
from pathlib import Path
from typing import Any


RUNS_DIR = Path(__file__).resolve().parents[2] / "data" / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)


def save_run(run_name: str, data: dict[str, Any]) -> Path:

    file_path = RUNS_DIR / f"{run_name}.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    return file_path


def load_run(run_name: str) -> dict[str, Any]:

    file_path = RUNS_DIR / f"{run_name}.json"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Saved run not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)