"""Tests for the fuzzy matching logic."""

from semantic_deduper.matcher import (
    find_near_duplicates,
    shingle_overlap,
    text_similarity,
)


def test_text_similarity_identical_is_one():
    assert text_similarity("hello world", "hello world") == 1.0


def test_text_similarity_empty_is_zero():
    # difflib defines similarity of two empty strings as 1.0
    assert text_similarity("", "") == 1.0
    assert text_similarity("hello", "") == 0.0


def test_text_similarity_completely_different_is_low():
    assert text_similarity("abcdef", "xyz123") < 0.5


def test_text_similarity_near_duplicate_is_high():
    a = "The quick brown fox jumps over the lazy dog."
    b = "The quick brown fox jump over the lazy dog."
    assert text_similarity(a, b) > 0.9


def test_shingle_overlap_identical_is_one():
    assert shingle_overlap("hello", "hello") == 1.0


def test_shingle_overlap_disjoint_is_zero():
    assert shingle_overlap("abc", "xyz") == 0.0


def test_find_near_duplicates_identical_pair():
    texts = ["note one content here", "note one content here", "totally different thing"]
    matches = find_near_duplicates(texts, threshold=0.85)
    assert len(matches) == 1
    assert matches[0].index_a == 0
    assert matches[0].index_b == 1
    assert matches[0].similarity == 1.0


def test_find_near_duplicates_threshold_filters():
    texts = [
        "the quick brown fox jumps over",
        "the quick brown fox jumps over",
        "the quick brown fox",
        "completely unrelated stuff here",
    ]
    strict = find_near_duplicates(texts, threshold=0.99, min_length=1)
    loose = find_near_duplicates(texts, threshold=0.6, min_length=1)
    assert len(strict) == 1
    assert len(loose) > len(strict)


def test_find_near_duplicates_min_length_filters():
    texts = ["short", "short", "a much longer piece of text that is repeated", "a much longer piece of text that is repeated"]
    matches = find_near_duplicates(texts, threshold=0.85, min_length=20)
    indices = {(m.index_a, m.index_b) for m in matches}
    assert (0, 1) not in indices
    assert (2, 3) in indices


def test_find_near_duplicates_sorted_by_similarity():
    texts = ["abc", "ab", "a"]
    matches = find_near_duplicates(texts, threshold=0.5, min_length=1)
    similarities = [m.similarity for m in matches]
    assert similarities == sorted(similarities, reverse=True)
