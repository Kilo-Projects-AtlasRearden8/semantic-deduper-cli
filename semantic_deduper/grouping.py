"""Union-find clustering of near-duplicate matches into review groups."""


def group_duplicates(count: int, matches) -> list[list[int]]:
    """Cluster document indices into groups using the given pairwise matches.

    Returns a list of groups, each a sorted list of document indices.
    Singletons (documents with no matches) are omitted.
    """

    parent = list(range(count))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for match in matches:
        union(match.index_a, match.index_b)

    groups: dict[int, list[int]] = {}
    for index in range(count):
        root = find(index)
        if root != index:
            groups.setdefault(root, []).append(index)

    result = []
    for members in groups.values():
        root = find(members[0])
        result.append(sorted([root] + members))
    result.sort(key=lambda g: (-len(g), g[0]))
    return result


def groups_to_pairs(groups: list[list[int]], matches) -> list[tuple[int, int, float]]:
    """Flatten groups back into the match pairs they contain, scored."""

    score = {(m.index_a, m.index_b): m.similarity for m in matches}
    pairs: list[tuple[int, int, float]] = []
    for group in groups:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                pairs.append((a, b, score.get((a, b), score.get((b, a), 0.0))))
    pairs.sort(key=lambda p: (-p[2], p[0], p[1]))
    return pairs
