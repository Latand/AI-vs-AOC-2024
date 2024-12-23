def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1: Counts the number of sets of three interconnected computers
    where at least one computer's name starts with 't'.
    """
    connections = {}
    for line in data.splitlines():
        a, b = line.strip().split("-")
        connections.setdefault(a, set()).add(b)
        connections.setdefault(b, set()).add(a)

    # Find all combinations of three computers
    from itertools import combinations

    count = 0
    for trio in combinations(connections.keys(), 3):
        a, b, c = trio
        if b in connections[a] and c in connections[a] and c in connections[b]:
            if any(computer.startswith("t") for computer in trio):
                count += 1
    return count


def part2(data: str) -> int:
    """
    Solution for part 2: Finds the largest set of interconnected computers and returns
    the sorted, comma-joined names as the password.
    """
    connections = {}
    for line in data.splitlines():
        a, b = line.strip().split("-")
        connections.setdefault(a, set()).add(b)
        connections.setdefault(b, set()).add(a)

    # Function to check if all nodes in the set are interconnected
    def is_clique(clique):
        for node in clique:
            if not set(clique) - {node} <= connections[node]:
                return False
        return True

    # Find the largest clique
    from itertools import combinations

    nodes = list(connections.keys())
    for size in range(len(nodes), 0, -1):
        for subset in combinations(nodes, size):
            if is_clique(subset):
                password = ",".join(sorted(subset))
                return password
    return 0  # Fallback in case no clique is found


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
