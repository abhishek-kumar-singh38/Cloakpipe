#!/usr/bin/env python3
"""CloakPipe defensive research CLI.

This CLI intentionally generates inert canary artifacts only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from core.cleanup import clean_output_directory
from core.host_evasion import generate_host_source, compile_host_source
from core.network_evasion import generate_network_corpus


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cloakpipe",
        description="Generate inert host and network canary artifacts for authorized defensive testing.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    network = subparsers.add_parser("network", help="Generate a fixed canary representation corpus.")
    network.add_argument("--output", type=Path, required=True, help="JSON output path.")
    network.add_argument(
        "--label",
        default="authorized-normalization-study",
        help="Human-readable label stored in the corpus metadata.",
    )

    host = subparsers.add_parser("host", help="Generate a transparent C diagnostic program.")
    host.add_argument("--output", type=Path, required=True, help="C source output path.")
    host.add_argument("--compile", action="store_true", help="Compile the generated diagnostic source.")
    host.add_argument("--compiler", default="cc", help="Compiler executable (default: cc).")

    clean = subparsers.add_parser("clean", help="Remove known generated files from output/.")
    clean.add_argument("--output-dir", type=Path, default=Path("output"))
    clean.add_argument("--yes", action="store_true", help="Skip the confirmation prompt.")

    return parser


def command_network(args: argparse.Namespace) -> int:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    corpus = generate_network_corpus(label=args.label)
    args.output.write_text(json.dumps(corpus, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(corpus['cases'])} inert network cases to {args.output}")
    return 0


def command_host(args: argparse.Namespace) -> int:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generate_host_source(), encoding="utf-8")
    print(f"Wrote benign host canary source to {args.output}")

    if args.compile:
        executable = args.output.with_suffix("")
        compile_host_source(args.output, executable, compiler=args.compiler)
        print(f"Compiled transparent diagnostic executable to {executable}")
    return 0


def command_clean(args: argparse.Namespace) -> int:
    if not args.output_dir.exists():
        print(f"Nothing to clean: {args.output_dir}")
        return 0
    if not args.output_dir.is_dir():
        raise ValueError(f"Refusing to clean non-directory: {args.output_dir}")
    if args.output_dir.name != "output":
        raise ValueError("Cleanup is restricted to a directory named 'output'.")
    if not args.yes and sys.stdin.isatty():
        answer = input(f"Remove known generated files from {args.output_dir}? [y/N] ")
        if answer.strip().lower() not in {"y", "yes"}:
            print("Cleanup cancelled.")
            return 0
    removed = clean_output_directory(args.output_dir)
    print(f"Removed {removed} generated file(s) from {args.output_dir}")
    return 0


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "network":
            return command_network(args)
        if args.command == "host":
            return command_host(args)
        if args.command == "clean":
            return command_clean(args)
    except (OSError, ValueError, RuntimeError, shutil.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())