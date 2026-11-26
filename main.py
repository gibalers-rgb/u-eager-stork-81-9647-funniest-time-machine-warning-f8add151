"""Funniest Time Machine Warning Label — entry program.

Writes a single one-line warning label for a time machine to the output
path (OUTPUT_PATH env var, default /output/entry.txt). Standard library
only, deterministic, no network.
"""

import os

ENTRY = (
    "WARNING: Do not approach yourself. "
    "If approached by yourself, remain calm. "
    "One of you is an imposter, and it is you."
)

MAX_CHARS = 120


def validate(text: str) -> None:
    """Enforce the competition gate: 1-120 chars, one line, not blank."""
    if not text or text.strip() == "":
        raise SystemExit("entry is empty or whitespace-only")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def main() -> None:
    validate(ENTRY)
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY)
    # Round-trip check: what landed on disk must be exactly the entry,
    # so a partial write or encoding slip fails loudly instead of
    # submitting a corrupted label.
    with open(out_path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != ENTRY:
        raise SystemExit("round-trip mismatch: file content differs from entry")
    print(f"wrote {len(ENTRY)} characters to {out_path}")


if __name__ == "__main__":
    main()
