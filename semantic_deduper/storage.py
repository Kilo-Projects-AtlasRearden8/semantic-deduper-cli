"""Local JSON storage of scan results."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class ScanStore:
    scanned_at: str
    directory: str
    threshold: float
    min_length: int
    files: list[dict] = field(default_factory=list)
    pairs: list[dict] = field(default_factory=list)
    groups: list[list[int]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ScanStore":
        if not isinstance(data, dict):
            raise ValueError("store JSON must be an object")
        return cls(
            scanned_at=data.get("scanned_at", ""),
            directory=data.get("directory", ""),
            threshold=float(data.get("threshold", 0.85)),
            min_length=int(data.get("min_length", 20)),
            files=list(data.get("files", [])),
            pairs=list(data.get("pairs", [])),
            groups=[list(g) for g in data.get("groups", [])],
        )


def save_store(store: ScanStore, path: str) -> None:
    """Persist the scan store as JSON at ``path`` (local storage only)."""

    store.scanned_at = datetime.now(timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(store.to_dict(), handle, indent=2, sort_keys=True)


def load_store(path: str) -> ScanStore | None:
    """Load a scan store from ``path``. Returns None if missing or invalid."""

    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return ScanStore.from_dict(json.load(handle))
    except (OSError, json.JSONDecodeError, ValueError, KeyError):
        return None
