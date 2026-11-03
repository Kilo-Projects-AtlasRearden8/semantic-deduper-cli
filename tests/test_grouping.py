"""Tests for duplicate grouping logic."""

from semantic_deduper.grouping import group_duplicates
from semantic_deduper.matcher import Match


def test_group_duplicates_merges_chain():
    matches = [
        Match(0, 1, 0.9),
        Match(1, 2, 0.9),
        Match(4, 5, 0.8),
    ]
    groups = group_duplicates(6, matches)
    assert sorted([sorted(g) for g in groups]) == [[0, 1, 2], [4, 5]]


def test_group_duplicates_no_matches_empty():
    assert group_duplicates(4, []) == []


def test_group_duplicates_singletons_omitted():
    matches = [Match(0, 3, 0.9)]
    groups = group_duplicates(5, matches)
    assert groups == [[0, 3]]
