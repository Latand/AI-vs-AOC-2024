import math


def read_input():
    """
    Reads the puzzle input from ../input.txt
    Returns:
        A list of strings representing the map rows.
    """
    with open("../input.txt") as f:
        return [line.rstrip("\n") for line in f]


def in_bounds(r, c, max_r, max_c):
    """Check if (r, c) is within the map bounds."""
    return 0 <= r < max_r and 0 <= c < max_c


def part1(data):
    """
    Part 1:
    An antinode occurs at any point that is perfectly in line with two antennas
    of the same frequency if one antenna is twice as far away from that point as the other.

    Mathematically, for two distinct antenna positions A and B (same frequency),
    the two antinode positions are:
       P1 = 2A - B
       P2 = 2B - A
    (vector subtraction in terms of row, col coordinates).
    We only count those positions if they lie within the grid.

    Returns:
        The count of unique antinode positions in the grid.
    """

    rows = len(data)
    cols = len(data[0]) if rows > 0 else 0

    # Collect positions of each frequency in a dictionary:
    # freq_positions[freq] = [(r1,c1), (r2,c2), ...]
    freq_positions = {}
    for r in range(rows):
        for c in range(cols):
            ch = data[r][c]
            if ch != ".":
                freq_positions.setdefault(ch, []).append((r, c))

    antinodes = set()

    # For each frequency, examine all pairs of antennas
    for freq, positions in freq_positions.items():
        # Need at least two antennas to form an antinode
        if len(positions) < 2:
            continue
        # Consider all pairs
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                # Compute the two possible antinodes
                # P1 = (2*r1 - r2, 2*c1 - c2)
                # P2 = (2*r2 - r1, 2*c2 - c1)
                p1 = (2 * r1 - r2, 2 * c1 - c2)
                p2 = (2 * r2 - r1, 2 * c2 - c1)

                # Check bounds and add to set if valid
                if in_bounds(p1[0], p1[1], rows, cols):
                    antinodes.add(p1)
                if in_bounds(p2[0], p2[1], rows, cols):
                    antinodes.add(p2)

    return len(antinodes)


def part2(data):
    """
    Part 2:
    An antinode occurs at any grid position that is in line with at least two antennas
    of the same frequency, regardless of their distance apart.

    In other words, for each frequency f, for each pair of distinct antennas (A, B),
    every integer point P on the line passing through A and B (within the grid) is an antinode.

    Additionally, an antenna's own position is also counted if it is in line with at least
    one other antenna of the same frequency (i.e. if that antenna is not unique).
    (In practice, this also falls out naturally from enumerating all points on lines that
    pass through at least two distinct antenna positions.)

    Returns:
        The count of unique antinode positions in the grid.
    """

    rows = len(data)
    cols = len(data[0]) if rows > 0 else 0

    freq_positions = {}
    for r in range(rows):
        for c in range(cols):
            ch = data[r][c]
            if ch != ".":
                freq_positions.setdefault(ch, []).append((r, c))

    antinodes = set()

    # For each frequency, find all lines formed by pairs of antennas
    for freq, positions in freq_positions.items():
        if len(positions) < 2:
            # If there's only one antenna of this frequency, it can't form a line
            continue

        # All antennas of this frequency are guaranteed antinodes,
        # since each is "in line" with at least one other (by having >=2 total).
        for ant_r, ant_c in positions:
            antinodes.add((ant_r, ant_c))

        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                # Direction vector
                dr = r2 - r1
                dc = c2 - c1

                # Reduce to step of gcd
                g = math.gcd(dr, dc)
                dr //= g
                dc //= g

                # We'll generate all points on the line between min_k and max_k.
                # The line equation in param form:
                #   (r, c) = (r1, c1) + k*(dr, dc)
                #
                # We'll find the range of k that keeps r, c in the grid.

                # Helper function to get the valid range of k for one dimension.
                # We want r1 + k*dr in [0, rows-1], similarly c1 + k*dc in [0, cols-1].

                def get_k_range(start, d, min_val, max_val):
                    """
                    For 'start + k*d' to be in [min_val, max_val],
                    solve inequalities:
                        min_val <= start + k*d <= max_val
                    Return (kmin, kmax) as integer bounds (inclusive).
                    If no valid k, return (None, None).
                    """
                    if d == 0:
                        # Then start must already be in range for all k
                        if min_val <= start <= max_val:
                            # Any k is valid, but that doesn't help in a finite grid
                            # We'll return a large range for k in that dimension.
                            return (-(10**10), 10**10)  # effectively "infinite" range
                        else:
                            # No possible k
                            return (None, None)
                    else:
                        # Solve min_val <= start + k*d and start + k*d <= max_val
                        # For d > 0:
                        #   k >= (min_val - start)/d
                        #   k <= (max_val - start)/d
                        # For d < 0, the inequalities flip in sign.
                        kmin_float = (min_val - start) / d
                        kmax_float = (max_val - start) / d
                        if d < 0:
                            # Flip
                            kmin_float, kmax_float = kmax_float, kmin_float

                        # We want integer k range
                        kmin = math.ceil(kmin_float)
                        kmax = math.floor(kmax_float)
                        if kmin > kmax:
                            return (None, None)
                        return (kmin, kmax)

                # Now get k range from row dimension
                kr1, kr2 = get_k_range(r1, dr, 0, rows - 1)
                # and from column dimension
                kc1, kc2 = get_k_range(c1, dc, 0, cols - 1)

                if kr1 is None or kc1 is None:
                    # No valid range in at least one dimension
                    continue

                # Intersect the ranges
                kmin = max(kr1, kc1)
                kmax = min(kr2, kc2)
                if kmin is None or kmax is None:
                    continue
                if kmin > kmax:
                    continue

                # For all k in [kmin, kmax], add that point
                for k in range(kmin, kmax + 1):
                    rr = r1 + k * dr
                    cc = c1 + k * dc
                    antinodes.add((rr, cc))

    return len(antinodes)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
