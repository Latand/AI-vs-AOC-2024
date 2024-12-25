import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
    total = 0
    for match in matches:
        total += int(match[0]) * int(match[1])
    return total


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    total = 0
    enabled = True
    i = 0
    while i < len(data):
        if data[i : i + 3] == "mul":
            match = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", data[i:])
            if match and enabled:
                total += int(match.group(1)) * int(match.group(2))
            if match:
                i += len(match.group(0))
            else:
                i += 1
        elif data[i : i + 4] == "do()":
            enabled = True
            i += 4
        elif data[i : i + 6] == "don't()":
            enabled = False
            i += 6
        else:
            i += 1

    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
