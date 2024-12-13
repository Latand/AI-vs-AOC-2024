def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    machines = parse_data(data)
    prizes_won = 0
    min_tokens_spent = 0

    for machine in machines:
        # Try to solve the system of linear equations for both x and y axes
        a_x, a_y, b_x, b_y, x_prize, y_prize = machine

        # Calculate gcd of the moves (to check if solution is possible)
        g_x = gcd(a_x, b_x)
        g_y = gcd(a_y, b_y)

        # Check if the prize coordinates are divisible by the gcd of movements
        if x_prize % g_x != 0 or y_prize % g_y != 0:
            continue  # No solution possible for this machine

        # Find the optimal number of button presses using extended Euclidean algorithm
        # For each axis, calculate the least number of token cost

        # Apply extended Euclidean algorithm to solve the Diophantine equation
        x_tokens = solve_for_tokens(a_x, b_x, x_prize)
        y_tokens = solve_for_tokens(a_y, b_y, y_prize)

        # Add the total number of tokens used to win this prize
        total_tokens = x_tokens + y_tokens

        if total_tokens > 0:
            prizes_won += 1
            min_tokens_spent += total_tokens

    return min_tokens_spent


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    machines = parse_data(data)
    prizes_won = 0
    min_tokens_spent = 0

    for machine in machines:
        # Adjust prize position by adding 10^13 to both x and y
        a_x, a_y, b_x, b_y, x_prize, y_prize = machine
        x_prize += 10000000000000
        y_prize += 10000000000000

        # Same procedure as in part 1
        g_x = gcd(a_x, b_x)
        g_y = gcd(a_y, b_y)

        if x_prize % g_x != 0 or y_prize % g_y != 0:
            continue  # No solution possible for this machine

        x_tokens = solve_for_tokens(a_x, b_x, x_prize)
        y_tokens = solve_for_tokens(a_y, b_y, y_prize)

        total_tokens = x_tokens + y_tokens

        if total_tokens > 0:
            prizes_won += 1
            min_tokens_spent += total_tokens

    return min_tokens_spent


def parse_data(data: str):
    """
    Parse input data into a list of machine configurations
    """
    machines = []
    for line in data.splitlines():
        parts = line.split()
        a_x, a_y = map(int, parts[0].split("X")[1].split(","))
        b_x, b_y = map(int, parts[1].split("X")[1].split(","))
        x_prize, y_prize = map(int, parts[2].split("X")[1].split(","))
        machines.append((a_x, a_y, b_x, b_y, x_prize, y_prize))
    return machines


def solve_for_tokens(a, b, target):
    """
    Solve for the number of presses needed to reach the target with button A and B.
    """
    # Use extended Euclidean algorithm or a more efficient method to calculate the number of presses needed
    # Return the number of tokens spent (minimizing the cost for each axis separately)
    pass


def gcd(a, b):
    """
    Calculate the greatest common divisor of a and b
    """
    while b:
        a, b = b, a % b
    return a


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
