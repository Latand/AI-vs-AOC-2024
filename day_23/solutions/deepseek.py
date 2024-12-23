def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    from itertools import combinations

    # Build the graph
    graph = {}
    for line in data.splitlines():
        a, b = line.strip().split("-")
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)

    # Find all triplets
    nodes = list(graph.keys())
    triplets = combinations(nodes, 3)

    count = 0
    for triplet in triplets:
        a, b, c = triplet
        # Check if a is connected to b and c, b is connected to c
        if b in graph[a] and c in graph[a] and c in graph[b]:
            # Check if at least one starts with 't'
            if a.startswith("t") or b.startswith("t") or c.startswith("t"):
                count += 1
    return count


def part2(data: str) -> str:
    from itertools import combinations

    # Build the graph
    graph = {}
    for line in data.splitlines():
        a, b = line.strip().split("-")
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)

    # Function to find the largest clique
    def largest_clique(graph, nodes, current_clique):
        if not nodes:
            return current_clique
        # Choose the node with the smallest degree
        u = min(nodes, key=lambda x: len(graph[x]))
        # Find neighbors of u that are also in nodes
        neighbors = graph[u].intersection(nodes)
        # Explore cliques that include u
        for v in neighbors:
            # Find neighbors of v that are also in neighbors
            next_neighbors = neighbors.intersection(graph[v])
            # Recurse with the updated clique and next neighbors
            candidate_clique = largest_clique(
                graph, next_neighbors, current_clique + [v]
            )
            if len(candidate_clique) > len(largest_clique.clique):
                largest_clique.clique = candidate_clique
        # Explore cliques that exclude u
        candidate_clique = largest_clique(graph, nodes - {u}, current_clique)
        if len(candidate_clique) > len(largest_clique.clique):
            largest_clique.clique = candidate_clique
        return largest_clique.clique

    # Initialize the largest clique
    largest_clique.clique = []
    # Start the recursion
    max_clique = largest_clique(graph, set(graph.keys()), [])
    if len(max_clique) > len(largest_clique.clique):
        largest_clique.clique = max_clique
    # Sort and join the names
    password = ",".join(sorted(largest_clique.clique))
    return password


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
