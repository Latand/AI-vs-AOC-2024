import re
from typing import List, Tuple, Dict
from collections import defaultdict, deque


def read_input() -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    """
    Reads the input file and returns the ordering rules and updates.

    Returns:
        Tuple containing:
            - List of tuples representing ordering rules (X, Y) meaning X must come before Y.
            - List of updates, each update is a list of page numbers.
    """
    with open("../input.txt", "r") as f:
        content = f.read().strip()

    if not content:
        return [], []

    # Split the input into rules and updates based on double newline
    sections = content.split("\n\n")
    if len(sections) < 2:
        rules_section = sections[0]
        updates_section = ""
    else:
        rules_section, updates_section = sections[:2]

    # Parse rules
    rules = []
    for line in rules_section.strip().split("\n"):
        match = re.match(r"(\d+)\|(\d+)", line.strip())
        if match:
            x, y = int(match.group(1)), int(match.group(2))
            rules.append((x, y))

    # Parse updates
    updates = []
    for line in updates_section.strip().split("\n"):
        if line.strip():
            pages = [
                int(page.strip())
                for page in line.strip().split(",")
                if page.strip().isdigit()
            ]
            updates.append(pages)

    return rules, updates


def is_correct_order(update: List[int], rules: List[Tuple[int, int]]) -> bool:
    """
    Checks if the given update is in the correct order based on the rules.

    Args:
        update: List of page numbers in the update.
        rules: List of ordering rules as tuples (X, Y).

    Returns:
        True if the update is correctly ordered, False otherwise.
    """
    page_index = {page: idx for idx, page in enumerate(update)}
    for x, y in rules:
        if x in page_index and y in page_index:
            if page_index[x] >= page_index[y]:
                return False
    return True


def reorder_update(update: List[int], rules: List[Tuple[int, int]]) -> List[int]:
    """
    Reorders the given update to satisfy the ordering rules using topological sort.

    Args:
        update: List of page numbers in the update.
        rules: List of ordering rules as tuples (X, Y).

    Returns:
        A reordered list of page numbers that satisfies the ordering rules.
    """
    # Build graph
    graph = defaultdict(list)  # adjacency list
    in_degree = defaultdict(int)
    pages_in_update = set(update)

    for x, y in rules:
        if x in pages_in_update and y in pages_in_update:
            graph[x].append(y)
            in_degree[y] += 1

    # Initialize queue with nodes having in-degree 0
    queue = deque([page for page in update if in_degree[page] == 0])

    sorted_order = []
    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_order) != len(update):
        raise ValueError("Cycle detected or invalid ordering rules.")

    return sorted_order


def get_middle_page(update: List[int]) -> int:
    """
    Returns the middle page number of the update.

    If the number of pages is even, returns the lower middle.

    Args:
        update: List of page numbers.

    Returns:
        The middle page number.
    """
    n = len(update)
    middle_index = (n - 1) // 2
    return update[middle_index]


def part1(data: str) -> int:
    """
    Solves Part One of the Advent of Code Day 5 challenge.

    Determines which updates are already in the correct order and
    adds up their middle page numbers.

    Args:
        data: The input data as a string.

    Returns:
        The sum of the middle page numbers of correctly ordered updates.
    """

    # Override read_input to accept data as a string
    def read_input_from_string(
        input_str: str,
    ) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
        if not input_str:
            return [], []

        sections = input_str.strip().split("\n\n")
        if len(sections) < 2:
            rules_section = sections[0]
            updates_section = ""
        else:
            rules_section, updates_section = sections[:2]

        rules = []
        for line in rules_section.strip().split("\n"):
            match = re.match(r"(\d+)\|(\d+)", line.strip())
            if match:
                x, y = int(match.group(1)), int(match.group(2))
                rules.append((x, y))

        updates = []
        for line in updates_section.strip().split("\n"):
            if line.strip():
                pages = [
                    int(page.strip())
                    for page in line.strip().split(",")
                    if page.strip().isdigit()
                ]
                updates.append(pages)

        return rules, updates

    rules, updates = read_input_from_string(data)
    total = 0
    for update in updates:
        if is_correct_order(update, rules):
            middle = get_middle_page(update)
            total += middle
    return total


def part2(data: str) -> int:
    """
    Solves Part Two of the Advent of Code Day 5 challenge.

    Reorders the incorrectly ordered updates based on the rules and
    adds up their middle page numbers after reordering.

    Args:
        data: The input data as a string.

    Returns:
        The sum of the middle page numbers of correctly reordered updates.
    """

    # Override read_input to accept data as a string
    def read_input_from_string(
        input_str: str,
    ) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
        if not input_str:
            return [], []

        sections = input_str.strip().split("\n\n")
        if len(sections) < 2:
            rules_section = sections[0]
            updates_section = ""
        else:
            rules_section, updates_section = sections[:2]

        rules = []
        for line in rules_section.strip().split("\n"):
            match = re.match(r"(\d+)\|(\d+)", line.strip())
            if match:
                x, y = int(match.group(1)), int(match.group(2))
                rules.append((x, y))

        updates = []
        for line in updates_section.strip().split("\n"):
            if line.strip():
                pages = [
                    int(page.strip())
                    for page in line.strip().split(",")
                    if page.strip().isdigit()
                ]
                updates.append(pages)

        return rules, updates

    rules, updates = read_input_from_string(data)
    total = 0
    for update in updates:
        if not is_correct_order(update, rules):
            try:
                reordered = reorder_update(update, rules)
                middle = get_middle_page(reordered)
                total += middle
            except ValueError:
                # If there's a cycle or invalid ordering, skip this update
                continue
    return total


def main():
    data = read_input()
    # Combine rules and updates back into a single string separated by double newline
    if not data[0] and not data[1]:
        input_str = ""
    else:
        rules_str = "\n".join([f"{x}|{y}" for x, y in data[0]])
        updates_str = "\n".join([",".join(map(str, update)) for update in data[1]])
        input_str = f"{rules_str}\n\n{updates_str}"

    result1 = part1(input_str)
    print(f"Part 1: {result1}")

    result2 = part2(input_str)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
