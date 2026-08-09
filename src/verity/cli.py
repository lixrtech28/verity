"""Command-line interface for VERITY."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import Evidence, build_claims


def main() -> None:
    parser = argparse.ArgumentParser(description="Build traceable claims from approved evidence.")
    parser.add_argument("input", type=Path, help="JSON file containing an evidence array")
    args = parser.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    evidence = [Evidence(**item) for item in payload.get("evidence", [])]
    print(build_claims(evidence).to_json())


if __name__ == "__main__":
    main()
