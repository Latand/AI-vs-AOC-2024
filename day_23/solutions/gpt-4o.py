import itertools
from collections import defaultdict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def part1(data: list[str]) -> int:
    connections = defaultdict(set)
    for line in data:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    # Find all sets of three interconnected computers
    sets_of_three = set()
    for a in connections:
        for b, c in itertools.combinations(connections[a], 2):
            if b in connections[c]:
                sets_of_three.add(tuple(sorted([a, b, c])))

    # Filter sets where at least one computer's name starts with 't'
    filtered_sets = [
        s for s in sets_of_three if any(comp.startswith("t") for comp in s)
    ]

    return len(filtered_sets)


def part2(data: list[str]) -> str:
    connections = defaultdict(set)
    for line in data:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    # Find the largest clique
    def is_clique(nodes):
        return all(b in connections[a] for a, b in itertools.combinations(nodes, 2))

    largest_clique = []
    for size in range(len(connections), 2, -1):
        for nodes in itertools.combinations(connections.keys(), size):
            if is_clique(nodes):
                largest_clique = nodes
                break
        if largest_clique:
            break

    # Sort and join the names to form the password
    return ",".join(sorted(largest_clique))


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
