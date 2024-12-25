from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    """
    Parse input into a graph of dependencies and list of updates
    Returns: (dependencies_graph, updates)
    """
    # Split into rules and updates
    rules_section, updates_section = data.split("\n\n")

    # Parse rules into a graph
    dependencies = defaultdict(set)
    for line in rules_section.split("\n"):
        before, after = map(int, line.split("|"))
        dependencies[before].add(after)

    # Parse updates
    updates = []
    for line in updates_section.split("\n"):
        update = list(map(int, line.split(",")))
        updates.append(update)

    return dependencies, updates


def is_valid_order(pages: List[int], dependencies: Dict[int, Set[int]]) -> bool:
    """
    Check if the given order of pages satisfies all dependencies
    """
    page_positions = {page: i for i, page in enumerate(pages)}

    # Check each dependency
    for page in pages:
        if page in dependencies:
            # For each page that should come after current page
            for after_page in dependencies[page]:
                # Skip if the after_page is not in current update
                if after_page not in page_positions:
                    continue
                # If dependency is violated, return False
                if page_positions[page] > page_positions[after_page]:
                    return False

    return True


def get_correct_order(pages: List[int], dependencies: Dict[int, Set[int]]) -> List[int]:
    """
    Return the correct order of pages using Kahn's algorithm
    """
    # Build reverse graph and calculate in-degrees
    reverse_deps = defaultdict(set)
    in_degree = defaultdict(int)

    # Consider only pages in the current update
    pages_set = set(pages)

    for page in dependencies:
        for after_page in dependencies[page]:
            if page in pages_set and after_page in pages_set:
                reverse_deps[after_page].add(page)
                in_degree[page] += 0  # Ensure the key exists
                in_degree[after_page] += 1

    # Initialize queue with pages that have no dependencies
    queue = deque([page for page in pages if in_degree[page] == 0])
    result = []

    # Process queue
    while queue:
        page = queue.popleft()
        result.append(page)

        # Remove edges from graph
        if page in dependencies:
            for after_page in dependencies[page]:
                if after_page in pages_set:
                    in_degree[after_page] -= 1
                    if in_degree[after_page] == 0:
                        queue.append(after_page)

    return result


def get_middle_number(numbers: List[int]) -> int:
    """Get the middle number from a list"""
    return numbers[len(numbers) // 2]


def part1(data: str) -> int:
    """
    Find sum of middle numbers from correctly ordered updates
    """
    dependencies, updates = parse_input(data)

    middle_sum = 0
    for update in updates:
        if is_valid_order(update, dependencies):
            middle_sum += get_middle_number(update)

    return middle_sum


def part2(data: str) -> int:
    """
    Find sum of middle numbers from reordered incorrect updates
    """
    dependencies, updates = parse_input(data)

    middle_sum = 0
    for update in updates:
        if not is_valid_order(update, dependencies):
            correct_order = get_correct_order(update, dependencies)
            middle_sum += get_middle_number(correct_order)

    return middle_sum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
