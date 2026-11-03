"""CSV report generation from stored scan results."""

import csv
import os
from typing import Iterable

from .matcher import Match


def write_report(
    output_path: str,
    files: list,
    pairs: Iterable[tuple[int, int, float]],
    groups: list[list[int]] | None = None,
) -> str:
    """Write a CSV report of near-duplicate candidates and return ``output_path``.

    Columns: group_id,file_a_index,file_b_index,similarity,file_a,file_b
    """

    group_of: dict[int, int] = {}
    if groups:
        for gid, group in enumerate(groups, start=1):
            for index in group:
                group_of[index] = gid

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "group_id",
                "file_a_index",
                "file_b_index",
                "similarity",
                "file_a",
                "file_b",
            ]
        )
        for index_a, index_b, similarity in pairs:
            def _path(item):
                if isinstance(item, dict):
                    return item.get("path", str(item))
                return getattr(item, "path", str(item))

            writer.writerow(
                [
                    group_of.get(index_a, ""),
                    index_a,
                    index_b,
                    f"{similarity:.4f}",
                    _path(files[index_a]),
                    _path(files[index_b]),
                ]
            )
    return output_path
