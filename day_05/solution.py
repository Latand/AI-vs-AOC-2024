def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    """Parse input into rules and updates."""
    sections = data.split("\n\n")
    rules = [tuple(map(int, rule.split("|"))) for rule in sections[0].split("\n")]
    updates = [list(map(int, update.split(","))) for update in sections[1].split("\n")]
    return rules, updates


def is_update_valid(update: list[int], rules: list[tuple[int, int]]) -> bool:
    """Check if an update is in valid order based on rules."""
    # Create a mapping of which pages must come before others
    dependencies = {}
    for before, after in rules:
        dependencies.setdefault(after, set()).add(before)

    # Check each page's position against its dependencies
    for i, page in enumerate(update):
        # Check if this page has dependencies
        if page in dependencies:
            required_before = dependencies[page]
            # Ensure all required pages are before the current page
            for req_page in required_before:
                if req_page in update:
                    if update.index(req_page) >= i:
                        return False
    return True


def reorder_update(update: list[int], rules: list[tuple[int, int]]) -> list[int]:
    """Reorder an update according to the rules using topological sort."""
    # Create adjacency list
    graph = {}
    for before, after in rules:
        if before in update and after in update:
            graph.setdefault(before, set()).add(after)
            graph.setdefault(after, set())

    # Initialize in-degree count
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

    # Topological sort
    queue = [node for node in graph if in_degree[node] == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Add any remaining numbers that weren't part of dependencies
    remaining = [x for x in update if x not in result]
    result.extend(remaining)

    return result


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    rules, updates = parse_input(data)

    # Find valid updates and their middle pages
    valid_middle_pages = [
        update[len(update) // 2] for update in updates if is_update_valid(update, rules)
    ]

    return sum(valid_middle_pages)


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    rules, updates = parse_input(data)

    # Find invalid updates and reorder them
    middle_sums = 0
    for update in updates:
        if not is_update_valid(update, rules):
            reordered = reorder_update(update, rules)
            middle_sums += reordered[len(reordered) // 2]

    return middle_sums


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
