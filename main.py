#!/usr/bin/env python3
"""Vending Machine Pickup Line — make.fun bounty entry writer.

Writes a single-line pickup line (spoken by the vending machine itself)
to /output/entry.txt. Python 3 stdlib only, no network access.

Output directory fallback chain:
  1. $MAKEFUN_OUTPUT_DIR
  2. /output
  3. output/ inside this repo
  4. a temporary directory
"""

import os
import sys
import tempfile
from pathlib import Path

ENTRY_PART1 = "I've dropped a thousand snacks, but you just made my coil spin, my lights blink, and "
ENTRY_PART2 = "my exact change feel like a first date."

ENTRY = ENTRY_PART1 + ENTRY_PART2


def validate(text):
    """Entry gate: 1-200 chars, a single line, not whitespace-only."""
    return (
        isinstance(text, str)
        and 1 <= len(text) <= 200
        and "\n" not in text
        and "\r" not in text
        and text.strip() != ""
    )


def resolve_output_dir():
    """Return the first usable output directory in the fallback chain."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(Path(env_dir))
    candidates.append(Path("/output"))
    candidates.append(Path(__file__).resolve().parent / "output")
    candidates.append(Path(tempfile.gettempdir()) / "vending-pickup-output")

    last_error = None
    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write-probe"
            probe.write_text("", encoding="utf-8")
            probe.unlink()
            return candidate
        except OSError as exc:
            last_error = exc
            continue
    raise OSError(f"no writable output directory found: {last_error}")


def main():
    if not validate(ENTRY):
        print("entry failed validation", file=sys.stderr)
        sys.exit(1)
    out_dir = resolve_output_dir()
    out_path = out_dir / "entry.txt"
    # No trailing newline: the entry is exactly one line.
    out_path.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {out_path} ({len(ENTRY)} chars, {len(ENTRY.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
