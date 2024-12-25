from collections import defaultdict, deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data):
    rules_section, updates_section = data.split("\n\n")
    rules = []
    for line in rules_section.splitlines():
        x, y = map(int, line.split("|"))
        rules.append((x, y))

    updates = []
    for line in updates_section.splitlines():
        updates.append(list(map(int, line.split(","))))

    return rules, updates


def build_graph(rules):
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for x, y in rules:
        graph[x].append(y)
        in_degree[y] += 1
        if x not in in_degree:
            in_degree[x] = 0

    return graph, in_degree


def is_correct_order(update, graph, in_degree):
    # Create a copy of in_degree for this update
    current_in_degree = in_degree.copy()
    order = []
    queue = deque()

    # Initialize the queue with nodes that have no incoming edges
    for node in update:
        if current_in_degree[node] == 0:
            queue.append(node)

    while queue:
        if len(queue) > 1:
            return False  # Non-deterministic order (shouldn't happen in valid topological order)

        current = queue.popleft()
        order.append(current)

        for neighbor in graph[current]:
            if neighbor in update:  # Only consider edges relevant to this update
                current_in_degree[neighbor] -= 1
                if current_in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return len(order) == len(update) and order == update


def topological_sort(update, graph, in_degree):
    current_in_degree = in_degree.copy()
    queue = deque()
    order = []

    for node in update:
        if current_in_degree[node] == 0:
            queue.append(node)

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in graph[current]:
            if neighbor in update:
                current_in_degree[neighbor] -= 1
                if current_in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return order


def find_middle_page(update):
    return update[len(update) // 2]


def part1(data):
    rules, updates = parse_input(data)
    graph, in_degree = build_graph(rules)

    middle_sum = 0
    for update in updates:
        if is_correct_order(update, graph, in_degree):
            middle_sum += find_middle_page(update)

    return middle_sum


def part2(data):
    rules, updates = parse_input(data)
    graph, in_degree = build_graph(rules)

    middle_sum = 0
    for update in updates:
        if not is_correct_order(update, graph, in_degree):
            sorted_update = topological_sort(update, graph, in_degree)
            middle_sum += find_middle_page(sorted_update)

    return middle_sum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
