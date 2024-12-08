def read_input() -> str:
    """Read and return the input data from input.txt."""
    with open("input.txt") as f:
        return f.read().strip()


def calculate_antinode_positions(data: str) -> int:
    """
    Calculate the number of possible antinode positions based on antenna pairs.

    An antinode position is calculated for each pair of antennas with the same frequency.
    For each antenna pair (A, B), there are two possible antinode positions:
    - One at distance 2 from B through A
    - One at distance 2 from A through B
    """
    grid = data.split("\n")
    grid_height = len(grid)
    grid_width = max(len(row) for row in grid)

    # Group antenna positions by their frequency
    antennas_by_frequency = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != ".":
                antennas_by_frequency.setdefault(char, []).append((x, y))

    antinode_positions = set()

    # Calculate antinode positions for each pair of antennas with the same frequency
    for frequency, antenna_positions in antennas_by_frequency.items():
        num_antennas = len(antenna_positions)
        if num_antennas < 2:
            continue  # Skip frequencies with less than 2 antennas

        for i in range(num_antennas):
            for j in range(i + 1, num_antennas):
                antenna1 = antenna_positions[i]
                antenna2 = antenna_positions[j]

                # Calculate antinode through antenna1 (at distance 2 from antenna2)
                antinode1_x = 2 * antenna2[0] - antenna1[0]
                antinode1_y = 2 * antenna2[1] - antenna1[1]

                # Calculate antinode through antenna2 (at distance 2 from antenna1)
                antinode2_x = 2 * antenna1[0] - antenna2[0]
                antinode2_y = 2 * antenna1[1] - antenna2[1]

                # Add antinode positions if they're within grid bounds
                if 0 <= antinode1_x < grid_width and 0 <= antinode1_y < grid_height:
                    antinode_positions.add((antinode1_x, antinode1_y))

                if 0 <= antinode2_x < grid_width and 0 <= antinode2_y < grid_height:
                    antinode_positions.add((antinode2_x, antinode2_y))

    return len(antinode_positions)


def part1(data: str) -> int:
    """Solve part 1: Calculate the total number of possible antinode positions."""
    return calculate_antinode_positions(data)


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    # TODO: Implement part 2 solution
    pass


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
