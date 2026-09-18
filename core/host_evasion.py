"""Benign host-side canary source generation and compiler checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .network_evasion import CANARY


def generate_host_source() -> str:
    """Return transparent C source that prints the fixed canary."""
    template_path = Path(__file__).resolve().parent.parent / "templates" / "canary.c"
    template = template_path.read_text(encoding="utf-8")
    return template.replace("{{CLOAKPIPE_CANARY}}", CANARY)


def compile_host_source(source_path: Path, executable_path: Path, compiler: str = "cc") -> None:
    """Compile only the generated diagnostic C program.

    No linker or runtime flags are accepted from callers. The command is
    intentionally constrained to a normal console executable.
    """
    if source_path.suffix != ".c":
        raise ValueError("Host source must have a .c extension.")
    executable_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        compiler,
        "-std=c11",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-O2",
        str(source_path),
        "-o",
        str(executable_path),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Compiler not found: {compiler}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "compiler failed").strip()
        raise RuntimeError(detail) from exc