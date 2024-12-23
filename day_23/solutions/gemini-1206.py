def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def build_graph(data: str):
    graph = {}
    for line in data.split("\n"):
        u, v = line.split("-")
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
    return graph


def find_triangles(graph):
    triangles = []
    nodes = list(graph.keys())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            for k in range(j + 1, len(nodes)):
                u, v, w = nodes[i], nodes[j], nodes[k]
                if v in graph[u] and w in graph[u] and w in graph[v]:
                    triangles.append(tuple(sorted((u, v, w))))
    return triangles


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    graph = build_graph(data)
    triangles = find_triangles(graph)
    count = 0
    for triangle in triangles:
        if any(node.startswith("t") for node in triangle):
            count += 1
    return count


def find_max_clique(graph):
    max_clique = []
    nodes = list(graph.keys())

    def is_clique(subset):
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                if subset[j] not in graph[subset[i]]:
                    return False
        return True

    def find_cliques(current_clique, remaining_nodes):
        nonlocal max_clique
        if not remaining_nodes:
            if is_clique(current_clique) and len(current_clique) > len(max_clique):
                max_clique = current_clique[:]
            return

        node = remaining_nodes[0]

        find_cliques(current_clique, remaining_nodes[1:])

        can_add = True
        for existing_node in current_clique:
            if node not in graph[existing_node]:
                can_add = False
                break

        if can_add:
            find_cliques(current_clique + [node], remaining_nodes[1:])

    find_cliques([], nodes)
    return max_clique


def part2(data: str) -> str:
    """
    Solution for part 2
    """
    graph = build_graph(data)
    max_clique = find_max_clique(graph)
    return ",".join(sorted(max_clique))


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
