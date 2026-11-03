"""Command-line interface for semantic-deduper."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from .grouping import group_duplicates, groups_to_pairs
from .matcher import find_near_duplicates
from .report import write_report
from .scanner import scan_directory
from .storage import ScanStore, load_store, save_store

DEFAULT_STORE = ".semantic_deduper_store.json"
DEFAULT_EXTENSIONS = (".txt", ".md")
DEFAULT_THRESHOLD = 0.85
DEFAULT_MIN_LENGTH = 20


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="semantic-deduper",
        description="Find near-duplicate notes and ideas in local text files using fuzzy matching.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser(
        "scan", help="Scan a directory and group near-duplicate files for review."
    )
    scan_parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory).",
    )
    scan_parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Similarity threshold 0.0-1.0 (default: {DEFAULT_THRESHOLD}).",
    )
    scan_parser.add_argument(
        "--min-length",
        type=int,
        default=DEFAULT_MIN_LENGTH,
        help=f"Ignore files shorter than this many characters (default: {DEFAULT_MIN_LENGTH}).",
    )
    scan_parser.add_argument(
        "--extensions",
        nargs="+",
        default=list(DEFAULT_EXTENSIONS),
        help=f"File extensions to include (default: {' '.join(DEFAULT_EXTENSIONS)}).",
    )
    scan_parser.add_argument(
        "--store",
        default=DEFAULT_STORE,
        help=f"Local JSON store path (default: {DEFAULT_STORE}).",
    )

    report_parser = subparsers.add_parser(
        "report", help="Write a CSV report from a previously saved local store."
    )
    report_parser.add_argument(
        "--store",
        default=DEFAULT_STORE,
        help=f"Local JSON store path (default: {DEFAULT_STORE}).",
    )
    report_parser.add_argument(
        "--output",
        default="dedupe_report.csv",
        help="CSV report output path (default: dedupe_report.csv).",
    )

    return parser


def cmd_scan(args: argparse.Namespace) -> int:
    if not 0.0 <= args.threshold <= 1.0:
        print(f"error: --threshold must be between 0.0 and 1.0, got {args.threshold}")
        return 2

    extensions = tuple(ext.lower() if ext.startswith(".") else f".{ext.lower()}"
                       for ext in args.extensions)

    files = scan_directory(args.directory, extensions=extensions, min_size=1)
    if not files:
        print(f"No text files found in {os.path.abspath(args.directory)}")
        _write_empty_store(args.store, args.directory, args.threshold, args.min_length)
        print(f"Empty store written to {args.store}")
        return 0

    texts = [f.content for f in files]
    matches = find_near_duplicates(
        texts, threshold=args.threshold, min_length=args.min_length
    )
    groups = group_duplicates(len(files), matches)

    print(f"Scanned {len(files)} text file(s) in {args.directory}")
    print(f"Near-duplicate candidate pairs: {len(matches)}")
    print(f"Review groups: {len(groups)}")

    store = ScanStore(
        scanned_at="",
        directory=os.path.abspath(args.directory),
        threshold=args.threshold,
        min_length=args.min_length,
        files=[
            {"path": f.path, "name": f.name, "size": f.size} for f in files
        ],
        pairs=[
            {"index_a": m.index_a, "index_b": m.index_b, "similarity": m.similarity}
            for m in matches
        ],
        groups=groups,
    )
    save_store(store, args.store)
    print(f"Local store written to {args.store}")
    return 0


def _write_empty_store(path: str, directory: str, threshold: float, min_length: int) -> None:
    from .storage import ScanStore, save_store
    store = ScanStore(
        scanned_at="",
        directory=os.path.abspath(directory),
        threshold=threshold,
        min_length=min_length,
    )
    save_store(store, path)


def cmd_report(args: argparse.Namespace) -> int:
    import os

    store = load_store(args.store)
    if store is None:
        print(f"error: no store found at {args.store} (run `semantic-deduper scan` first)")
        return 1

    # Re-hydrate file paths only; contents are not stored.
    files = store.files
    pairs = [
        (p["index_a"], p["index_b"], float(p["similarity"])) for p in store.pairs
    ]
    write_report(args.output, files, pairs, groups=store.groups)
    print(f"Wrote {len(pairs)} candidate pair(s) across {len(store.groups)} group(s) to {args.output}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "scan":
        import os
        return cmd_scan(args)
    if args.command == "report":
        return cmd_report(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
