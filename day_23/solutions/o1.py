def read_input():
    """
    Reads input from ../input.txt and returns it as a string.
    """
    with open("../input.txt", "r") as f:
        return f.read().strip()


def parse_graph(data: str):
    """
    Parses the input data (each line 'a-b' representing an undirected edge).
    Returns a dictionary where each key is a node (string),
    and each value is a set of neighbors (strings).
    """
    adjacency = {}
    lines = data.splitlines()
    for line in lines:
        left, right = line.split("-")
        if left not in adjacency:
            adjacency[left] = set()
        if right not in adjacency:
            adjacency[right] = set()
        adjacency[left].add(right)
        adjacency[right].add(left)
    return adjacency


def part1(data: str) -> int:
    """
    Part 1:
    1) Find all sets of three computers (triplets) that form a complete subgraph (triangle).
    2) Count how many such sets have at least one computer whose name starts with 't'.
    """
    adjacency = parse_graph(data)
    nodes = list(adjacency.keys())
    triangles = []

    # Check all combinations of 3 distinct nodes
    # A set of three is fully interconnected if every pair is connected
    # (i.e., each node in the triple is in adjacency sets of the other two).
    from itertools import combinations

    for combo in combinations(nodes, 3):
        n1, n2, n3 = combo
        if (
            n2 in adjacency[n1]
            and n3 in adjacency[n1]
            and n1 in adjacency[n2]
            and n3 in adjacency[n2]
            and n1 in adjacency[n3]
            and n2 in adjacency[n3]
        ):
            triangles.append(combo)

    # Count how many contain at least one 't' start
    count_t = 0
    for tri in triangles:
        if any(x.startswith("t") for x in tri):
            count_t += 1

    return count_t


def bron_kerbosch(R, P, X, adjacency, cliques):
    """
    Bron–Kerbosch algorithm to find all maximal cliques in an undirected graph.

    R, P, X are sets:
      - R is the current clique
      - P is the set of candidates to be added
      - X is the set of nodes that should not be added
    """
    if not P and not X:
        # Found a maximal clique
        cliques.append(R)
        return
    # We'll clone P here because we're modifying it in the loop
    for v in list(P):
        # Recurse with v added to R, and only neighbors of v remain in P and X
        bron_kerbosch(
            R | {v},
            P.intersection(adjacency[v]),
            X.intersection(adjacency[v]),
            adjacency,
            cliques,
        )
        P.remove(v)
        X.add(v)


def part2(data: str) -> str:
    """
    Part 2:
    1) Find the largest set of computers that are all connected to each other (maximum clique).
    2) Return them sorted alphabetically, joined by commas (the "password").
    """
    adjacency = parse_graph(data)
    all_nodes = set(adjacency.keys())

    # Use Bron–Kerbosch to find all maximal cliques, then pick the largest
    cliques = []
    bron_kerbosch(set(), set(all_nodes), set(), adjacency, cliques)

    # Find the largest clique (by size)
    largest_clique = max(cliques, key=len)
    # Sort and join by commas
    password = ",".join(sorted(largest_clique))
    return password


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
