from typing import List, Dict, Set
from itertools import combinations


def read_input() -> str:
    """Read the input file."""
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str) -> tuple[Dict[int, Set[int]], List[List[int]]]:
    """
    Parse the input into ordering rules and updates.

    Returns:
    - A dictionary of page ordering rules (page must come before its value pages)
    - A list of updates (each update is a list of page numbers)
    """
    # Split input into lines
    lines = data.split("\n")

    # Find the empty line separating rules and updates
    separator_index = lines.index("")

    # Parse ordering rules
    ordering_rules = {}
    for rule in lines[:separator_index]:
        before, after = map(int, rule.split("|"))

        if before not in ordering_rules:
            ordering_rules[before] = set()
        ordering_rules[before].add(after)

    # Parse updates
    updates = []
    for update in lines[separator_index + 1 :]:
        updates.append(list(map(int, update.split(","))))

    return ordering_rules, updates


def is_valid_order(pages: List[int], rules: Dict[int, Set[int]]) -> bool:
    """
    Check if a given page order is valid according to the rules.

    A page order is valid if for any rule x|y, x appears before y.
    """
    # Create a dictionary of page indices for quick lookup
    page_indices = {page: index for index, page in enumerate(pages)}

    # Check each rule
    for before, after_set in rules.items():
        # If both pages are in the current update
        if before in page_indices and any(after in page_indices for after in after_set):
            # Check which 'after' pages violate the rule
            for after in after_set:
                if (
                    after in page_indices
                    and page_indices[before] >= page_indices[after]
                ):
                    return False

    return True


def find_valid_order(pages: List[int], rules: Dict[int, Set[int]]) -> List[int]:
    """
    Find a valid order for the pages that satisfies all applicable rules.

    If a rule involves a page not in the current update, it is ignored.
    """
    from itertools import permutations

    for perm in permutations(pages):
        if is_valid_order(list(perm), rules):
            return list(perm)

    return pages  # Fallback, though this shouldn't happen per problem description


def part1(data: str) -> int:
    """
    Solve part 1: Find middle page numbers of correctly ordered updates.
    """
    # Parse the input
    rules, updates = parse_input(data)

    # Find middle pages of correctly ordered updates
    middle_pages = []
    for update in updates:
        if is_valid_order(update, rules):
            # Find middle page index (using integer division for 0-based indexing)
            middle_index = len(update) // 2
            middle_pages.append(update[middle_index])

    return sum(middle_pages)


def part2(data: str) -> int:
    """
    Solve part 2: Find middle page numbers of correctly ordered updates
    after rearranging incorrectly ordered updates.
    """
    # Parse the input
    rules, updates = parse_input(data)

    # Find middle pages of correctly and incorrectly ordered updates
    middle_pages = []
    for update in updates:
        if not is_valid_order(update, rules):
            # Find a valid order for the update
            corrected_update = find_valid_order(update, rules)

            # Find middle page index (using integer division for 0-based indexing)
            middle_index = len(corrected_update) // 2
            middle_pages.append(corrected_update[middle_index])

    return sum(middle_pages)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
