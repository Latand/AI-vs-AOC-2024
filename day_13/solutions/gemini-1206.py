def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def solve_machine(ax, ay, bx, by, px, py):
    """
    Solves for the number of A and B presses to reach the prize.
    Returns (a_presses, b_presses) or None if no solution is found.
    """
    # We have two equations:
    # ax * a_presses + bx * b_presses = px
    # ay * a_presses + by * b_presses = py

    # Solve for a_presses in terms of b_presses from the first equation:
    # a_presses = (px - bx * b_presses) / ax

    # Substitute into the second equation:
    # ay * ((px - bx * b_presses) / ax) + by * b_presses = py
    # ay * px - ay * bx * b_presses + by * b_presses * ax = py * ax
    # b_presses * (by * ax - ay * bx) = py * ax - ay * px
    # b_presses = (py * ax - ay * px) / (by * ax - ay * bx)

    # Check for division by zero or negative presses
    denominator = by * ax - ay * bx
    if denominator == 0:
        return None

    b_presses = (py * ax - ay * px) / denominator
    if b_presses < 0 or b_presses != int(b_presses):
        return None

    b_presses = int(b_presses)

    # Solve for a_presses
    a_presses = (px - bx * b_presses) / ax
    if a_presses < 0 or a_presses != int(a_presses):
        return None

    a_presses = int(a_presses)

    return (a_presses, b_presses)


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    lines = data.split("\n\n")
    winnable_machines = []
    total_cost = 0

    for machine_data in lines:
        lines_data = machine_data.split("\n")
        ax, ay = map(
            int,
            lines_data[0]
            .split(":")[1]
            .strip()
            .replace("X+", "")
            .replace("Y+", "")
            .split(", "),
        )
        bx, by = map(
            int,
            lines_data[1]
            .split(":")[1]
            .strip()
            .replace("X+", "")
            .replace("Y+", "")
            .split(", "),
        )
        px, py = map(
            int,
            lines_data[2]
            .split(":")[1]
            .strip()
            .replace("X=", "")
            .replace("Y=", "")
            .split(", "),
        )

        solution = solve_machine(ax, ay, bx, by, px, py)

        if solution:
            a_presses, b_presses = solution
            cost = a_presses * 3 + b_presses * 1
            winnable_machines.append((cost, a_presses, b_presses))

    for cost, _, _ in winnable_machines:
        total_cost += cost

    return total_cost


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    lines = data.split("\n\n")
    winnable_machines = []
    total_cost = 0

    for machine_data in lines:
        lines_data = machine_data.split("\n")
        ax, ay = map(
            int,
            lines_data[0]
            .split(":")[1]
            .strip()
            .replace("X+", "")
            .replace("Y+", "")
            .split(", "),
        )
        bx, by = map(
            int,
            lines_data[1]
            .split(":")[1]
            .strip()
            .replace("X+", "")
            .replace("Y+", "")
            .split(", "),
        )
        px, py = map(
            int,
            lines_data[2]
            .split(":")[1]
            .strip()
            .replace("X=", "")
            .replace("Y=", "")
            .split(", "),
        )

        px += 10000000000000
        py += 10000000000000

        solution = solve_machine(ax, ay, bx, by, px, py)

        if solution:
            a_presses, b_presses = solution
            cost = a_presses * 3 + b_presses * 1
            winnable_machines.append((cost, a_presses, b_presses))

    for cost, _, _ in winnable_machines:
        total_cost += cost

    return total_cost


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
