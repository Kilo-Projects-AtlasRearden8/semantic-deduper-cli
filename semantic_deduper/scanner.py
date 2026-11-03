"""Scan a directory for text files and extract their contents."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TextFile:
    path: str
    name: str
    content: str
    size: int


def read_text_file(path: str) -> str | None:
    """Read a text file, returning None if it cannot be decoded as text."""

    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError):
        return None


def scan_directory(
    directory: str,
    extensions: tuple[str, ...] = (".txt", ".md"),
    min_size: int = 1,
) -> list[TextFile]:
    """Recursively scan ``directory`` for text files with the given extensions."""

    files: list[TextFile] = []
    directory = os.path.abspath(directory)
    for root, _dirs, names in os.walk(directory):
        for name in sorted(names):
            if not name.lower().endswith(extensions):
                continue
            full_path = os.path.join(root, name)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                continue
            if size < min_size:
                continue
            content = read_text_file(full_path)
            if content is None:
                continue
            files.append(
                TextFile(
                    path=full_path,
                    name=name,
                    content=content,
                    size=size,
                )
            )
    files.sort(key=lambda f: f.path)
    return files
