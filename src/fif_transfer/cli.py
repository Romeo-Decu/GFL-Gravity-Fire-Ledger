"""Command-line interface for the FiF deterministic assessment core."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .engine import AssessmentInputError, assess


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m fif_transfer",
        description="Run a deterministic FiF evidence-transfer assessment."
    )
    parser.add_argument("--ruleset", required=True, help="Path to a versioned ruleset JSON file.")
    parser.add_argument("--request", required=True, help="Path to an assessment request JSON file.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    args = parser.parse_args(argv)
    try:
        ruleset = json.loads(Path(args.ruleset).read_text(encoding="utf-8"))
        request = json.loads(Path(args.request).read_text(encoding="utf-8"))
        result = assess(request, ruleset)
    except (OSError, json.JSONDecodeError, AssessmentInputError) as exc:
        print(f"FiF assessment error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
