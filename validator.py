import json
import sys
from pathlib import Path

REQUIRED_KEYS = {"prompt_id", "turn_number", "model_a", "model_b", "winner", "rationale"}

def validate_record(record: dict, index: int) -> list[str]:
    errors = []
    missing = REQUIRED_KEYS - record.keys()
    if missing:
        errors.append(f"Row {index}: Missing keys {sorted(missing)}")
    if record.get("winner") not in {"model_a", "model_b", "tie"}:
        errors.append(f"Row {index}: Invalid winner value '{record.get('winner')}'")
    if len(str(record.get("rationale", "")).strip()) < 25:
        errors.append(f"Row {index}: Rationale too short for audit threshold")
    return errors

def main(file_path: str) -> None:
    data = json.loads(Path(file_path).read_text(encoding="utf-8"))
    all_errors = []
    for idx, item in enumerate(data, start=1):
        all_errors.extend(validate_record(item, idx))
    if all_errors:
        print("\n".join(all_errors))
        sys.exit(1)
    print(f"Validated {len(data)} evaluation records successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validator.py <path_to_json>")
        sys.exit(1)
    main(sys.argv[1])
