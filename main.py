#!/usr/bin/env python3
"""
Log File Cleaner

Scans directories for log files containing a target server name.
If a file contains the target string, any lines containing flagged
keywords are removed while preserving the rest of the file.

Usage:
    python main.py scan
    python main.py scan -d /path/to/logs
    python main.py scan --dry-run
    python main.py scan --all
"""

from pathlib import Path
import argparse
import os
import sys

# ---------------- CONFIG ---------------- #

FLAGGED_KEYWORDS = {
    "meteor",
    "xaero",
    "wurst",
    "baritone",
    "augustus",
    "vape",
}

TARGET_STRING = "SERVER NAME"

# ---------------------------------------- #


def contains_target(file_path: Path) -> bool:
    """
    Check whether the file contains the target string.
    """
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()
            return TARGET_STRING.lower() in content
    except Exception as e:
        print(f"[ERROR] Failed reading {file_path}: {e}")
        return False


def clean_file(file_path: Path, dry_run: bool = False, verbose: bool = False):
    """
    Remove lines containing flagged keywords.
    """
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        cleaned_lines = []
        removed_lines = []

        for line in lines:
            lower_line = line.lower()

            if any(keyword in lower_line for keyword in FLAGGED_KEYWORDS):
                removed_lines.append(line.rstrip())
                continue

            cleaned_lines.append(line)

        removed_count = len(removed_lines)

        if removed_count == 0:
            return

        if dry_run:
            print(f"[DRY RUN] {file_path} -> would remove {removed_count} lines")
        else:
            with file_path.open("w", encoding="utf-8") as f:
                f.writelines(cleaned_lines)

            print(f"[CLEANED] {file_path} -> removed {removed_count} lines")

        if verbose and removed_lines:
            for removed in removed_lines:
                print(f"  - {removed}")

    except Exception as e:
        print(f"[ERROR] Failed processing {file_path}: {e}")


def scan_directory(
    directory: str,
    verbose: bool = False,
    dry_run: bool = False,
    all_files: bool = False,
):
    """
    Scan a directory recursively for matching files.
    """
    base_path = Path(directory)

    if not base_path.exists():
        print(f"[ERROR] Directory does not exist: {base_path}")
        sys.exit(1)

    scanned = 0
    matched = 0

    for file_path in base_path.rglob("*"):
        if not file_path.is_file():
            continue

        scanned += 1

        if not all_files and file_path.suffix.lower() != ".log":
            continue

        if contains_target(file_path):
            matched += 1
            clean_file(
                file_path,
                dry_run=dry_run,
                verbose=verbose,
            )

    print("\nDone.")
    print(f"Files scanned : {scanned}")
    print(f"Files matched : {matched}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Recursive log file cleaner"
    )

    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan and clean log files",
    )

    scan_parser.add_argument(
        "-d",
        "--directory",
        default=".",
        help="Directory to scan (default: current directory)",
    )

    scan_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )

    scan_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show removed lines",
    )

    scan_parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all file types instead of only .log files",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        scan_directory(
            directory=args.directory,
            verbose=args.verbose,
            dry_run=args.dry_run,
            all_files=args.all,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()