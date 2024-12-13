from math import gcd
from functools import lru_cache


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def solve_claw_machine(xa, ya, xb, yb, px, py):
    """
    Finds the minimal cost to win a prize if possible.
    Returns the cost or None if the prize is unreachable.
    """

    @lru_cache(None)
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x1, y1 = extended_gcd(b, a % b)
        x, y = y1, x1 - (a // b) * y1
        return g, x, y

    # Solve for X axis
    gx, ax, bx = extended_gcd(xa, xb)
    if px % gx != 0:
        return None

    # Scale solution to match prize position on X axis
    kx = px // gx
    ax *= kx
    bx *= kx

    # Solve for Y axis
    gy, ay, by = extended_gcd(ya, yb)
    if py % gy != 0:
        return None

    ky = py // gy
    ay *= ky
    by *= ky

    # Ensure coefficients match for both dimensions
    scale = lcm(gx, gy)
    ax, bx = ax * (scale // gx), bx * (scale // gx)
    ay, by = ay * (scale // gy), by * (scale // gy)

    # Find minimum cost
    cost_a = ax * 3 + ay * 3
    cost_b = bx * 1 + by * 1

    return min(cost_a, cost_b) if cost_a > 0 and cost_b > 0 else None


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    machines = []
    for line in data.strip().split("\n\n"):
        lines = line.split("\n")
        xa, ya = map(int, lines[0].split(" ")[1::2])
        xb, yb = map(int, lines[1].split(" ")[1::2])
        px, py = map(int, lines[2].split("=")[1:])
        machines.append((xa, ya, xb, yb, px, py))

    total_tokens = 0
    for xa, ya, xb, yb, px, py in machines:
        result = solve_claw_machine(xa, ya, xb, yb, px, py)
        if result is not None:
            total_tokens += result

    return total_tokens


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    machines = []
    for line in data.strip().split("\n\n"):
        lines = line.split("\n")
        xa, ya = map(int, lines[0].split(" ")[1::2])
        xb, yb = map(int, lines[1].split(" ")[1::2])
        px, py = map(int, lines[2].split("=")[1:])
        # Apply unit conversion
        px += 10**12
        py += 10**12
        machines.append((xa, ya, xb, yb, px, py))

    total_tokens = 0
    for xa, ya, xb, yb, px, py in machines:
        result = solve_claw_machine(xa, ya, xb, yb, px, py)
        if result is not None:
            total_tokens += result

    return total_tokens


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
