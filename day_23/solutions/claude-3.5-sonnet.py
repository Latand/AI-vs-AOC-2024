from collections import defaultdict
from itertools import combinations


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def build_graph(data: str) -> dict:
    """
    Build an adjacency list representation of the network
    """
    graph = defaultdict(set)
    for line in data.split("\n"):
        a, b = line.strip().split("-")
        graph[a].add(b)
        graph[b].add(a)
    return graph


def find_connected_triples(graph: dict) -> set:
    """
    Find all sets of three computers that are all connected to each other
    """
    triples = set()
    # Get all possible combinations of three computers
    for a, b, c in combinations(graph.keys(), 3):
        # Check if they form a triangle (all connected to each other)
        if b in graph[a] and c in graph[a] and c in graph[b]:
            # Sort to ensure consistent ordering
            triple = tuple(sorted([a, b, c]))
            triples.add(triple)
    return triples


def part1(data: str) -> int:
    """
    Count triples containing at least one computer with name starting with 't'
    """
    graph = build_graph(data)
    triples = find_connected_triples(graph)

    # Filter triples that contain at least one computer starting with 't'
    t_triples = [
        triple for triple in triples if any(comp.startswith("t") for comp in triple)
    ]

    return len(t_triples)


def find_largest_clique(graph: dict) -> set:
    """
    Find the largest set of computers where each is connected to all others
    Uses a simple maximal clique algorithm
    """
    nodes = set(graph.keys())
    max_clique = set()

    def is_clique(nodes_set):
        # Check if all nodes in the set are connected to each other
        return all(all(v in graph[u] for v in nodes_set if u != v) for u in nodes_set)

    # Try all possible combinations of nodes, starting from largest
    for size in range(len(nodes), 3, -1):  # We know it's at least size 4 from problem
        for candidate in combinations(nodes, size):
            candidate_set = set(candidate)
            if is_clique(candidate_set):
                return candidate_set

    return max_clique


def part2(data: str) -> str:
    """
    Find the largest fully connected group and return their names as a comma-separated string
    """
    graph = build_graph(data)
    largest_group = find_largest_clique(graph)

    # Sort alphabetically and join with commas
    return ",".join(sorted(largest_group))


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
