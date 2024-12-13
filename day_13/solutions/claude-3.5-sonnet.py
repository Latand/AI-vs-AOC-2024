def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_machine(lines):
    """Parse a single machine's configuration."""
    button_a = lines[0].split(": ")[1].split(", ")
    button_b = lines[1].split(": ")[1].split(", ")
    prize = lines[2].split(": ")[1].split(", ")

    return {
        "a": (int(button_a[0].split("+")[1]), int(button_a[1].split("+")[1])),
        "b": (int(button_b[0].split("+")[1]), int(button_b[1].split("+")[1])),
        "prize": (int(prize[0].split("=")[1]), int(prize[1].split("=")[1])),
    }


def solve_diophantine(a1, a2, b1, b2, c1, c2, max_tries=100):
    """
    Solve the system of Diophantine equations:
    a1*x + b1*y = c1
    a2*x + b2*y = c2
    Returns (x, y) if solution exists within max_tries, None otherwise
    """
    # Try all combinations up to max_tries
    for x in range(max_tries + 1):
        for y in range(max_tries + 1):
            if (a1 * x + b1 * y == c1) and (a2 * x + b2 * y == c2):
                return (x, y)
    return None


def calculate_tokens(presses):
    """Calculate total tokens needed given button presses."""
    if presses is None:
        return float("inf")
    return 3 * presses[0] + presses[1]


def part1(data: str) -> int:
    """Find minimum tokens needed to win all possible prizes."""
    machines = [parse_machine(machine.split("\n")) for machine in data.split("\n\n")]

    total_tokens = 0
    for machine in machines:
        # Get button movements and prize coordinates
        ax, ay = machine["a"]
        bx, by = machine["b"]
        px, py = machine["prize"]

        # Solve system of equations
        presses = solve_diophantine(ax, bx, px, ay, by, py)
        tokens = calculate_tokens(presses)

        if tokens != float("inf"):
            total_tokens += tokens

    return total_tokens


def part2(data: str) -> int:
    """Same as part1 but with adjusted prize coordinates."""
    OFFSET = 10_000_000_000_000

    # Parse input and adjust prize coordinates
    machines = []
    for machine in data.split("\n\n"):
        parsed = parse_machine(machine.split("\n"))
        parsed["prize"] = (parsed["prize"][0] + OFFSET, parsed["prize"][1] + OFFSET)
        machines.append(parsed)

    total_tokens = 0
    for machine in machines:
        # Extract coordinates
        ax, ay = machine["a"]
        bx, by = machine["b"]
        px, py = machine["prize"]

        # Find greatest common divisor of button movements
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        # Check if solution exists using GCD
        gcd_x = gcd(ax, bx)
        gcd_y = gcd(ay, by)

        if px % gcd_x == 0 and py % gcd_y == 0:
            # Use extended Euclidean algorithm to find solution
            def extended_gcd(a, b):
                if a == 0:
                    return b, 0, 1
                gcd, x1, y1 = extended_gcd(b % a, a)
                x = y1 - (b // a) * x1
                y = x1
                return gcd, x, y

            # Solve for x-coordinate
            _, mx, nx = extended_gcd(ax, bx)
            k_x = px // gcd_x
            x = mx * k_x

            # Solve for y-coordinate
            _, my, ny = extended_gcd(ay, by)
            k_y = py // gcd_y
            y = my * k_y

            # Calculate tokens needed
            if x >= 0 and y >= 0:
                total_tokens += 3 * x + y

    return total_tokens


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
