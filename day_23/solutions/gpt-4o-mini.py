def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def build_graph(connections):
    graph = {}
    for connection in connections:
        a, b = connection.split("-")
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph


def find_triplets(graph):
    triplets = set()
    for a in graph:
        for b in graph[a]:
            for c in graph[b]:
                if c != a and c in graph[a]:
                    triplet = tuple(sorted([a, b, c]))
                    triplets.add(triplet)
    return triplets


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    connections = data
    graph = build_graph(connections)
    triplets = find_triplets(graph)
    return sum(
        1 for triplet in triplets if any(comp.startswith("t") for comp in triplet)
    )


def find_largest_connected_component(graph):
    visited = set()
    largest_component = set()

    def dfs(node, component):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.add(current)
                stack.extend(graph[current] - visited)

    for node in graph:
        if node not in visited:
            component = set()
            dfs(node, component)
            if len(component) > len(largest_component):
                largest_component = component

    return largest_component


def part2(data: str) -> str:
    """
    Solution for part 2
    """
    connections = data
    graph = build_graph(connections)
    largest_component = find_largest_connected_component(graph)
    return ",".join(sorted(largest_component))


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
