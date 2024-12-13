def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    # Parse input format. The puzzle example suggests lines describing:
    # Button A: X+Ax, Y+Ay
    # Button B: X+Bx, Y+By
    # Prize: X=Px, Y=Py
    #
    # Actual parsing depends on the puzzle input format. Here we assume
    # lines come in groups of three lines per machine or a known pattern.
    #
    # We'll make a guess that the input format is similar to the example:
    # Button A: X+Ax, Y+Ay
    # Button B: X+Bx, Y+By
    # Prize: X=Px, Y=Py
    # repeated for each machine.

    lines = [line.strip() for line in data.split("\n") if line.strip()]
    machines = []
    i = 0
    while i < len(lines):
        # Example line for A: "Button A: X+94, Y+34"
        # We'll parse Ax, Ay from that line:
        A_line = lines[i]
        B_line = lines[i + 1]
        P_line = lines[i + 2]

        # Parse A_line
        # Format: "Button A: X+94, Y+34"
        # We can split by ':' and ',' and '+' to extract integers
        # A_line.split(':')[1] -> " X+94, Y+34"
        # Strip and split further
        partA = A_line.split(":")[1].strip().split(",")
        # partA[0] = "X+94"
        # partA[1] = "Y+34"
        Ax = int(partA[0].split("+")[1])
        Ay = int(partA[1].split("+")[1])

        # Parse B_line similarly
        partB = B_line.split(":")[1].strip().split(",")
        Bx = int(partB[0].split("+")[1])
        By = int(partB[1].split("+")[1])

        # Parse P_line:
        # "Prize: X=8400, Y=5400"
        partP = P_line.split(":")[1].strip().split(",")
        Px = int(partP[0].split("=")[1])
        Py = int(partP[1].split("=")[1])

        machines.append((Ax, Ay, Bx, By, Px, Py))
        i += 3

    return machines


def solve_machine(Ax, Ay, Bx, By, Px, Py):
    """
    Solve the system:
    a*Ax + b*Bx = Px
    a*Ay + b*By = Py

    for nonnegative integers a,b. We also want to minimize 3*a + b.

    We'll use a linear algebra approach:

    From the first equation:
    a*Ax + b*Bx = Px
    b = (Px - a*Ax)/Bx   ... (if Bx != 0)

    Substitute into second:
    a*Ay + ((Px - a*Ax)/Bx)*By = Py
    a*Ay + (By/Bx)*Px - (By*Ax/Bx)*a = Py
    a*(Ay - (By*Ax)/Bx) = Py - (By/Bx)*Px
    a = [Py - (By/Bx)*Px] / [Ay - (By*Ax)/Bx]

    We need to be careful about division and integrality.

    Alternatively, solve using a matrix method:

    | Ax  Bx | | a | = | Px |
    | Ay  By | | b |   | Py |

    Using Cramer's rule:
    det = Ax*By - Ay*Bx
    a = (Px*By - Py*Bx)/det
    b = (Ax*Py - Ay*Px)/det

    Both a and b must be integers and >= 0.

    If there's no integral solution, return None.

    If integral solutions exist, this gives exactly one solution because it's a system of 2 equations and 2 unknowns.
    """
    det = Ax * By - Ay * Bx
    if det == 0:
        return None

    # Solve for a and b using Cramer's rule:
    # a = (Px*By - Py*Bx)/det
    # b = (Ax*Py - Ay*Px)/det
    # Must check divisibility
    numerator_a = Px * By - Py * Bx
    numerator_b = Ax * Py - Ay * Px

    if numerator_a % det != 0 or numerator_b % det != 0:
        return None

    a = numerator_a // det
    b = numerator_b // det

    if a < 0 or b < 0:
        return None

    # cost = 3*a + b
    cost = 3 * a + b
    return cost


def solve_all_machines(data: str, offset_x=0, offset_y=0):
    machines = parse_input(data)
    solutions = []
    for Ax, Ay, Bx, By, Px, Py in machines:
        Px_off = Px + offset_x
        Py_off = Py + offset_y
        cost = solve_machine(Ax, Ay, Bx, By, Px_off, Py_off)
        if cost is not None:
            solutions.append(cost)

    if len(solutions) == 0:
        # No prizes can be won
        return 0

    # According to the puzzle narrative, we want to win as many as possible.
    # If multiple are solvable, we presumably win them all since there's no indication we need to choose a subset.
    # Summing all costs of all solvable machines:
    # If there's a scenario where you must choose a subset to minimize cost, you'd do that here.
    # The puzzle as described seems to just sum them (based on original explanation).
    return sum(solutions)


def part1(data: str) -> int:
    # Part 1: no offset
    return solve_all_machines(data, 0, 0)


def part2(data: str) -> int:
    # Part 2: offset by 10000000000000
    return solve_all_machines(data, 10_000_000_000_000, 10_000_000_000_000)


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
