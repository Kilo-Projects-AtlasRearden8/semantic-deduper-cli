"""Fuzzy matching logic for near-duplicate detection.

Standard library only (difflib). No network, no API keys, no external models.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    """A candidate near-duplicate pair."""

    index_a: int
    index_b: int
    similarity: float


def shingles(text: str, size: int = 3) -> set[str]:
    """Return the set of character shingles (n-grams) of ``text``."""
    text = text.lower()
    if len(text) < size:
        return {text} if text else set()
    return {text[i : i + size] for i in range(len(text) - size + 1)}


def shingle_overlap(a: str, b: str, size: int = 3) -> float:
    """Jaccard overlap of shingle sets between two texts (0.0 to 1.0)."""

    set_a = shingles(a, size)
    set_b = shingles(b, size)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def text_similarity(a: str, b: str) -> float:
    """SequenceMatcher similarity ratio between two texts (0.0 to 1.0)."""

    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def _length_ratio_ok(a: str, b: str, threshold: float) -> bool:
    """Cheap pre-filter: similarity cannot exceed this length-based bound."""

    if not a or not b:
        return False
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    # SequenceMatcher ratio is bounded above by 2*shorter/(len_a + len_b)
    # when the shorter string appears verbatim inside the longer one.
    return (2 * len(shorter) / (len(a) + len(b))) >= threshold


def find_near_duplicates(
    texts: list[str],
    threshold: float = 0.85,
    min_length: int = 20,
    shingle_prefilter: float = 0.5,
) -> list[Match]:
    """Return all pairs of near-duplicate texts above ``threshold``.

    Uses a cheap shingle pre-filter plus an exact SequenceMatcher pass so the
    exact quadratic scan only runs on plausible pairs.
    """

    matches: list[Match] = []
    n = len(texts)
    for i in range(n):
        text_a = texts[i]
        if len(text_a) < min_length:
            continue
        for j in range(i + 1, n):
            text_b = texts[j]
            if len(text_b) < min_length:
                continue
            if not _length_ratio_ok(text_a, text_b, threshold):
                continue
            if shingle_prefilter > 0:
                if shingle_overlap(text_a, text_b) < shingle_prefilter:
                    continue
            similarity = text_similarity(text_a, text_b)
            if similarity >= threshold:
                matches.append(Match(index_a=i, index_b=j, similarity=similarity))
    matches.sort(key=lambda m: (-m.similarity, m.index_a, m.index_b))
    return matches
