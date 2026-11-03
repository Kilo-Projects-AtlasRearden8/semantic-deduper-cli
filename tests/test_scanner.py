"""Tests for directory scanning."""

import os
import tempfile

from semantic_deduper.scanner import scan_directory


def test_scan_directory_picks_up_txt_and_md():
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "a.txt"), "w").write("hello world")
        open(os.path.join(tmp, "b.md"), "w").write("hello world")
        open(os.path.join(tmp, "c.csv"), "w").write("ignore,me")
        files = scan_directory(tmp)
        names = sorted(f.name for f in files)
        assert names == ["a.txt", "b.md"]
        assert all(f.content == "hello world" for f in files)


def test_scan_directory_skips_binary():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "bin.txt")
        with open(path, "wb") as handle:
            handle.write(bytes(range(256)))
        files = scan_directory(tmp)
        assert files == []
