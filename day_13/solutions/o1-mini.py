def read_input():
    with open("../input.txt") as f:
        content = f.read().strip()
    machines = []
    for block in content.split("\n\n"):
        lines = block.strip().split("\n")
        button_a = lines[0].split(": ")[1].split(", ")
        button_b = lines[1].split(": ")[1].split(", ")
        prize = lines[2].split(": ")[1].split(", ")
        delta_x_a = int(button_a[0][2:])
        delta_y_a = int(button_a[1][2:])
        delta_x_b = int(button_b[0][2:])
        delta_y_b = int(button_b[1][2:])
        x_p = int(prize[0][2:])
        y_p = int(prize[1][2:])
        machines.append(
            {
                "delta_x_a": delta_x_a,
                "delta_y_a": delta_y_a,
                "delta_x_b": delta_x_b,
                "delta_y_b": delta_y_b,
                "x_p": x_p,
                "y_p": y_p,
            }
        )
    return machines


def part1(data: list) -> int:
    """
    Solution for part 1 using brute-force search within 100 button presses.
    """
    total_tokens = 0
    for machine in data:
        delta_x_a = machine["delta_x_a"]
        delta_y_a = machine["delta_y_a"]
        delta_x_b = machine["delta_x_b"]
        delta_y_b = machine["delta_y_b"]
        x_p = machine["x_p"]
        y_p = machine["y_p"]
        min_cost = None
        for a in range(0, 101):
            remaining_x = x_p - a * delta_x_a
            remaining_y = y_p - a * delta_y_a
            if remaining_x < 0 or remaining_y < 0:
                continue
            if delta_x_b == 0:
                if remaining_x != 0:
                    continue
                if delta_y_b == 0:
                    if remaining_y != 0:
                        continue
                    b = 0
                else:
                    if remaining_y % delta_y_b != 0:
                        continue
                    b = remaining_y // delta_y_b
            else:
                if remaining_x % delta_x_b != 0:
                    continue
                b = remaining_x // delta_x_b
                if delta_y_a * a + delta_y_b * b != y_p:
                    continue
            if b < 0 or b > 100:
                continue
            cost = 3 * a + b
            if min_cost is None or cost < min_cost:
                min_cost = cost
        if min_cost is not None:
            total_tokens += min_cost
    return total_tokens


def part2(data: list) -> int:
    """
    Solution for part 2 using mathematical approach to handle large button presses.
    """
    total_tokens = 0
    shift = 10**13
    for machine in data:
        delta_x_a = machine["delta_x_a"]
        delta_y_a = machine["delta_y_a"]
        delta_x_b = machine["delta_x_b"]
        delta_y_b = machine["delta_y_b"]
        x_p = machine["x_p"] + shift
        y_p = machine["y_p"] + shift

        # Solve the system:
        # a * delta_x_a + b * delta_x_b = x_p
        # a * delta_y_a + b * delta_y_b = y_p

        # Calculate determinant
        det = delta_x_a * delta_y_b - delta_x_b * delta_y_a
        if det == 0:
            continue  # No unique solution

        # Use Cramer's rule
        a_num = x_p * delta_y_b - delta_x_b * y_p
        b_num = delta_x_a * y_p - delta_y_a * x_p

        if det < 0:
            det = -det
            a_num = -a_num
            b_num = -b_num

        if a_num % det != 0 or b_num % det != 0:
            continue  # Non-integer solution

        a = a_num // det
        b = b_num // det

        if a < 0 or b < 0:
            continue  # Negative presses not allowed

        cost = 3 * a + b
        total_tokens += cost
    return total_tokens


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
