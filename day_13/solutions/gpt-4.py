def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def find_min_cost(xa, ya, xb, yb, xp, yp):
    # Solving Ax + By = G (G is gcd of xa/xb and ya/yb and must also divide xp and yp)
    g1, x1, y1 = gcd_extended(xa, xb)
    g2, x2, y2 = gcd_extended(ya, yb)

    if g1 != g2 or xp % g1 != 0 or yp % g1 != 0:
        return None  # No solution if gcds do not match or do not divide targets

    # Scale the solutions to meet the prize coordinates
    scale_x = xp // g1
    scale_y = yp // g1
    if scale_x != scale_y:
        return None  # The scaling factor must be the same for both equations to meet at the prize

    # General solution components
    x = x1 * scale_x
    y = y1 * scale_x
    k1, k2 = -yb // g1, xa // g1  # Coefficients for the general solution parameter k

    # Find the smallest positive k that makes x and y non-negative
    k = 0
    min_cost = float("inf")
    while (
        k < 10000
    ):  # Limit k to prevent infinite loops, adjust as necessary for larger ranges
        a = x + k * k1
        b = y + k * k2
        if a >= 0 and b >= 0:
            cost = 3 * a + b
            min_cost = min(min_cost, cost)
        k += 1

    return min_cost if min_cost != float("inf") else None


def part1(data):
    total_min_cost = 0
    prizes_won = 0
    for line in data:
        xa, ya, xb, yb, xp, yp = map(int, line.split())
        cost = find_min_cost(xa, ya, xb, yb, xp, yp)
        if cost is not None:
            total_min_cost += cost
            prizes_won += 1
    return total_min_cost


def part2(data):
    total_min_cost = 0
    prizes_won = 0
    offset = 10000000000000
    for line in data:
        xa, ya, xb, yb, xp, yp = map(int, line.split())
        cost = find_min_cost(xa, ya, xb, yb, xp + offset, yp + offset)
        if cost is not None:
            total_min_cost += cost
            prizes_won += 1
    return total_min_cost


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
