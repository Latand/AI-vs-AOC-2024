import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    pattern = r"mul\s*\(([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)"
    matches = re.findall(pattern, data)
    total = 0
    for x, y in matches:
        total += int(x) * int(y)
    return total


def part2(data: str) -> int:
    pattern = r"(do\(\)|don\'t\(\)|mul\s*\(([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\))"
    matches = re.findall(pattern, data)
    enabled = True
    total = 0
    for match in matches:
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif match[1] and match[2]:
            if enabled:
                x = int(match[1])
                y = int(match[2])
                total += x * y
    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
