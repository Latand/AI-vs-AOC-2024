def read_input():
    with open("../input.txt") as f:
        return f.read().strip().split("\n")


def parse_input(data):
    machines = []
    for line in data:
        parts = line.split(", ")
        a_move = tuple(map(int, parts[0].split(": X+")[1].split(", Y+")))
        b_move = tuple(map(int, parts[1].split(": X+")[1].split(", Y+")))
        prize = tuple(map(int, parts[2].split(": X=")[1].split(", Y=")))
        machines.append((a_move, b_move, prize))
    return machines


def solve_machine(a_move, b_move, prize, max_presses=100):
    """
    Find the minimum tokens to win a prize or return None if impossible.

    Solves using Linear Diophantine Equation (Bézout's identity)
    """
    x, y = prize

    def extended_gcd(a, b):
        """Returns (gcd, x, y) such that a*x + b*y = gcd"""
        if b == 0:
            return a, 1, 0
        else:
            gcd, x, y = extended_gcd(b, a % b)
            return gcd, y, x - (a // b) * y

    # Find gcd and coefficients for x and y
    gx1, gy1 = a_move[0], b_move[0]
    gx2, gy2 = a_move[1], b_move[1]

    gcd_x, cx, cy = extended_gcd(gx1, gx2)
    gcd_y, dx, dy = extended_gcd(gy1, gy2)

    # Check if solution exists
    if x % gcd_x != 0 or y % gcd_y != 0:
        return None

    # Find base solutions
    sol_x = x // gcd_x
    sol_y = y // gcd_y

    # Find multiples of coefficients
    def find_min_tokens(sol, cx, cy, gcd_x, gx1, gx2, max_tries=max_presses):
        for k in range(-max_tries, max_tries + 1):
            for m in range(-max_tries, max_tries + 1):
                a_presses = sol_x * cx + k * (gx2 // gcd_x)
                b_presses = sol_x * cy + m * (gx1 // gcd_x)

                if (
                    0 <= a_presses <= max_presses
                    and 0 <= b_presses <= max_presses
                    and a_presses * gx1 + b_presses * gx2 == x
                    and a_presses * gy1 + b_presses * gy2 == y
                ):
                    return a_presses, b_presses, a_presses * 3 + b_presses

        return None

    result = find_min_tokens(sol_x, cx, cy, gcd_x, gx1, gx2)
    return result


def part1(data: str) -> int:
    """
    Find the fewest tokens to win as many prizes as possible
    """
    machines = parse_input(data)
    total_tokens = 0
    machines_won = 0

    for machine in machines:
        result = solve_machine(machine[0], machine[1], machine[2])
        if result:
            machines_won += 1
            total_tokens += result[2]

    return total_tokens


def part2(data: str) -> int:
    """
    Find the fewest tokens to win as many prizes as possible
    with updated prize coordinates (+10000000000000 on both axes)
    """
    machines = parse_input(data)
    updated_machines = []

    for machine in machines:
        a_move, b_move, prize = machine
        updated_prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        updated_machines.append((a_move, b_move, updated_prize))

    total_tokens = 0
    machines_won = 0

    for machine in updated_machines:
        result = solve_machine(machine[0], machine[1], machine[2])
        if result:
            machines_won += 1
            total_tokens += result[2]

    return total_tokens


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")  # Solution: 31552

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
