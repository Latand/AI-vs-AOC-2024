import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    rules_str, updates_str = data.split("\n\n")
    rules = []
    for rule_str in rules_str.splitlines():
        match = re.match(r"(\d+)\|(\d+)", rule_str)
        if match:
            rules.append((int(match.group(1)), int(match.group(2))))
    updates = []
    for update_str in updates_str.splitlines():
        updates.append([int(page) for page in update_str.split(",")])
    return rules, updates


def is_correct_order(update, rules):
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if (update[j], update[i]) in rules:
                return False
    return True


def get_middle_page(update):
    return update[len(update) // 2]


def topological_sort(update, rules):
    in_degree = {page: 0 for page in update}
    graph = {page: [] for page in update}
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            graph[rule[0]].append(rule[1])
            in_degree[rule[1]] += 1

    queue = [page for page in update if in_degree[page] == 0]
    result = []
    while queue:
        page = queue.pop(0)
        result.append(page)
        for neighbor in graph[page]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(update) else update


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    rules, updates = parse_input(data)
    correct_updates = [update for update in updates if is_correct_order(update, rules)]
    middle_pages_sum = sum(get_middle_page(update) for update in correct_updates)
    return middle_pages_sum


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    rules, updates = parse_input(data)
    incorrect_updates = [
        update for update in updates if not is_correct_order(update, rules)
    ]
    sorted_incorrect_updates = [
        topological_sort(update, rules) for update in incorrect_updates
    ]
    middle_pages_sum = sum(
        get_middle_page(update) for update in sorted_incorrect_updates
    )
    return middle_pages_sum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
