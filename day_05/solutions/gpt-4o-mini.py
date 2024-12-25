from collections import defaultdict, deque
import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    # Split the input data into two sections
    sections = data.split("\n\n")
    rules_section = sections[0].splitlines()
    updates_section = sections[1].splitlines()

    rules = []
    for rule in rules_section:
        x, y = map(int, rule.split("|"))
        rules.append((x, y))

    updates = []
    for update in updates_section:
        updates.append(list(map(int, update.split(","))))

    return rules, updates


def validate_order(update, rules):
    """Check if the update is in correct order based on the rules"""
    position = {page: idx for idx, page in enumerate(update)}

    for x, y in rules:
        if x in position and y in position:
            if position[x] > position[y]:  # x appears after y, which is invalid
                return False
    return True


def find_middle(update):
    """Find the middle page of the update list"""
    return update[len(update) // 2]


def topological_sort(pages, rules):
    """Perform topological sorting to fix the order of the pages based on the rules"""
    adj_list = defaultdict(list)
    in_degree = defaultdict(int)

    # Build graph and in-degree count
    for x, y in rules:
        adj_list[x].append(y)
        in_degree[y] += 1
        if x not in in_degree:
            in_degree[x] = 0

    # Topological Sort using Kahn's Algorithm (BFS)
    queue = deque([page for page in pages if in_degree[page] == 0])
    sorted_order = []

    while queue:
        page = queue.popleft()
        sorted_order.append(page)

        for neighbor in adj_list[page]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order


def part1(data: str) -> int:
    rules, updates = parse_input(data)
    valid_updates = []

    # Check each update if it is in valid order
    for update in updates:
        if validate_order(update, rules):
            valid_updates.append(update)

    # Find middle page for each valid update and sum them
    return sum(find_middle(update) for update in valid_updates)


def part2(data: str) -> int:
    rules, updates = parse_input(data)
    incorrect_updates = []

    # Check each update and identify if it's incorrect
    for update in updates:
        if not validate_order(update, rules):
            incorrect_updates.append(update)

    # Reorder incorrect updates and find their middle pages
    reordered_middle_sum = 0
    for update in incorrect_updates:
        reordered = topological_sort(update, rules)
        reordered_middle_sum += find_middle(reordered)

    return reordered_middle_sum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
