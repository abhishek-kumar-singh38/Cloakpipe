"""Conservative cleanup helpers for generated lab artifacts."""

from __future__ import annotations

from pathlib import Path

KNOWN_GENERATED_FILES = {
    "network-corpus.json",
    "host-canary.c",
    "host-canary",
    "host-canary.exe",
}


def clean_output_directory(output_dir: Path) -> int:
    """Remove only known generated files directly inside output_dir."""
    resolved = output_dir.resolve()
    if resolved.name != "output":
        raise ValueError("Cleanup is restricted to a directory named 'output'.")

    removed = 0
    for name in KNOWN_GENERATED_FILES:
        candidate = resolved / name
        if candidate.is_file() or candidate.is_symlink():
            candidate.unlink()
            removed += 1
    return removed