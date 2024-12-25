import re
from typing import List, Tuple


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def extract_valid_multiplications(text: str) -> List[Tuple[int, int]]:
    """
    Extract valid multiplication instructions from the text.
    Returns a list of tuples containing the two numbers to multiply.
    """
    # Pattern for valid mul instructions
    # Matches mul followed by exactly ( and two 1-3 digit numbers separated by comma
    pattern = r"mul\((1?\d{1,2}|2?\d{1,2}|3?\d{1,2}),(1?\d{1,2}|2?\d{1,2}|3?\d{1,2})\)"

    # Find all matches
    matches = re.finditer(pattern, text)

    # Extract number pairs
    multiplications = []
    for match in matches:
        instruction = match.group()
        # Extract numbers from the instruction
        nums = re.findall(r"\d+", instruction)
        if len(nums) == 2:
            multiplications.append((int(nums[0]), int(nums[1])))

    return multiplications


def extract_control_instructions(text: str) -> List[Tuple[str, int]]:
    """
    Extract do() and don't() instructions with their positions.
    Returns a list of tuples containing the instruction type and its position.
    """
    instructions = []

    # Find all do() and don't() instructions
    do_matches = [(m.start(), "do") for m in re.finditer(r"do\(\)", text)]
    dont_matches = [(m.start(), "don't") for m in re.finditer(r"don\'t\(\)", text)]

    # Combine and sort by position
    instructions = do_matches + dont_matches
    instructions.sort(key=lambda x: x[0])

    return instructions


def part1(data: str) -> int:
    """
    Solution for part 1: Sum all valid multiplication results
    """
    multiplications = extract_valid_multiplications(data)

    # Calculate sum of all multiplication results
    total = sum(x * y for x, y in multiplications)

    return total


def part2(data: str) -> int:
    """
    Solution for part 2: Sum multiplication results considering do/don't instructions
    """
    # Get all multiplications with their positions in the text
    mul_pattern = (
        r"mul\((1?\d{1,2}|2?\d{1,2}|3?\d{1,2}),(1?\d{1,2}|2?\d{1,2}|3?\d{1,2})\)"
    )
    mul_matches = [(m.start(), m.group()) for m in re.finditer(mul_pattern, data)]

    # Get all control instructions
    control_instructions = extract_control_instructions(data)

    total = 0
    enabled = True  # Initially enabled

    # Process each multiplication
    for mul_pos, mul_instruction in mul_matches:
        # Check if the multiplication's state should change based on previous instructions
        for ctrl_pos, ctrl_type in control_instructions:
            if ctrl_pos < mul_pos:
                enabled = ctrl_type == "do"
            else:
                break

        # If enabled, add the multiplication result
        if enabled:
            nums = [int(x) for x in re.findall(r"\d+", mul_instruction)]
            total += nums[0] * nums[1]

    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
