import sys
import re
from collections import defaultdict, deque


def read_input():
    """
    Reads the puzzle input from ../input.txt.

    The input contains two sections:
    1) A list of ordering rules in the form "X|Y"
       (meaning X must come before Y if both are present).
    2) A list of updates (comma-separated page numbers).

    We assume there is no explicit blank line separator between
    the rules and the updates. Instead, we'll read lines until
    we encounter a line that doesn't contain the '|' character;
    at that point, we'll assume we've reached the updates.
    """
    with open("../input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def parse_input(lines):
    """
    Parse lines into two parts:
      - ordering_rules: list of (X, Y) meaning X|Y
      - updates: list of lists, each sub-list is an update's page numbers
    """
    ordering_rules = []
    updates = []

    # Read rules until we hit something that doesn't match the "X|Y" pattern
    rule_pattern = re.compile(r"^(\d+)\|(\d+)$")

    i = 0
    # Parse as many rules as we can
    while i < len(lines):
        m = rule_pattern.match(lines[i])
        if not m:
            break  # we've reached the updates
        x, y = m.groups()
        ordering_rules.append((int(x), int(y)))
        i += 1

    # The rest are updates, which should be comma-separated numbers
    while i < len(lines):
        update_str = lines[i]
        # Some lines might be empty if there was extra spacing, just skip if so
        if update_str:
            pages = [int(num.strip()) for num in update_str.split(",")]
            updates.append(pages)
        i += 1

    return ordering_rules, updates


def check_update_correct(pages, constraints):
    """
    Check if the given list of pages (an update) is in correct order
    according to the constraints.

    constraints is a list of tuples (X, Y) meaning X must be before Y
    if both X and Y appear in pages.

    Return True if correct, False otherwise.
    """
    # Build a quick lookup: page -> index in the update
    page_pos = {}
    for idx, p in enumerate(pages):
        page_pos[p] = idx

    # For each constraint that *applies*, check the order
    for x, y in constraints:
        if x in page_pos and y in page_pos:
            if page_pos[x] > page_pos[y]:
                return False
    return True


def reorder_update(pages, constraints):
    """
    Reorder the pages of a single update so that they satisfy all
    applicable constraints, by performing a topological sort of the
    pages involved in this update.

    Return a new list of pages in a correct topological order.
    """
    # Subgraph: for the pages in this update, build adjacency
    # We only consider constraints (x -> y) if x and y are in 'pages'.
    pages_set = set(pages)
    adj = defaultdict(list)
    in_degree = defaultdict(int)

    # Initialize in_degree for each page in the update to 0
    for p in pages:
        in_degree[p] = 0

    # Build graph edges
    for x, y in constraints:
        if x in pages_set and y in pages_set:
            adj[x].append(y)
            in_degree[y] += 1

    # Topological sort (Kahn's Algorithm)
    # We'll collect pages in a stable order if we queue them in ascending numeric order
    # to keep the final order deterministic, although the puzzle doesn't specify ties.
    # But the example strongly suggests a single correct topological order (no ties).
    queue = deque(sorted([p for p in pages if in_degree[p] == 0]))
    result = []

    while queue:
        # pop from the left
        node = queue.popleft()
        result.append(node)

        for nei in adj[node]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                # Insert in sorted order; for large sets, we could do a binary insert,
                # but here, the number of pages in an update is small, so linear insert is okay.
                # Or we can collect them and sort, but let's just do a naive approach:
                # We'll append then re-sort the queue. This ensures stable ascending order.
                queue.append(nei)
                # Re-sort the queue to keep ascending
                queue = deque(sorted(queue))

    # 'result' should now contain all pages, if there's no cycle
    return result


def get_middle_value(pages):
    """
    Return the middle page number from the list of pages.
    For a list of length L, the middle is the element at index L//2
    using 0-based indexing (which corresponds to the "middle" in 1-based).
    Example: For [75,47,61,53,29] (length=5), L//2=2 (0-based), pages[2]=61.
    """
    L = len(pages)
    return pages[L // 2]


def part1(data):
    """
    Part 1:
    - Determine which updates are already in the correct order.
    - Sum their "middle page number".

    Steps:
    1) Parse input into (constraints, updates)
    2) For each update, check if it is correct.
    3) If correct, find its middle page and accumulate.
    4) Return the sum.
    """
    constraints, updates = data
    total = 0

    for pages in updates:
        if check_update_correct(pages, constraints):
            total += get_middle_value(pages)

    return total


def part2(data):
    """
    Part 2:
    - For each incorrectly-ordered update, reorder it using a topological sort
      restricted to the pages in that update.
    - Sum their middle page number from the corrected ordering.
    """
    constraints, updates = data
    total = 0

    for pages in updates:
        if not check_update_correct(pages, constraints):
            correct_order = reorder_update(pages, constraints)
            total += get_middle_value(correct_order)

    return total


def main():
    lines = read_input()
    parsed_data = parse_input(lines)

    result1 = part1(parsed_data)
    print(f"Part 1: {result1}")

    result2 = part2(parsed_data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
