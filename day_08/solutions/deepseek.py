import math
from math import gcd


def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


def parse_antennas(grid):
    antennas = {}
    H = len(grid)
    W = len(grid[0]) if H > 0 else 0
    for y in range(H):
        for x in range(W):
            freq = grid[y][x]
            if freq != ".":
                if freq not in antennas:
                    antennas[freq] = []
                antennas[freq].append((x, y))
    return antennas, W, H


def compute_part1_antinodes(antennas, W, H):
    antinodes = set()
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                A = positions[i]
                B = positions[j]
                # Compute P1 = 2B - A
                P1_x = 2 * B[0] - A[0]
                P1_y = 2 * B[1] - A[1]
                if 0 <= P1_x < W and 0 <= P1_y < H:
                    antinodes.add((P1_x, P1_y))
                # Compute P2 = (A + 2B)/3
                if (A[0] + 2 * B[0]) % 3 == 0 and (A[1] + 2 * B[1]) % 3 == 0:
                    P2_x = (A[0] + 2 * B[0]) // 3
                    P2_y = (A[1] + 2 * B[1]) // 3
                    if 0 <= P2_x < W and 0 <= P2_y < H:
                        antinodes.add((P2_x, P2_y))
    return antinodes


def compute_part2_antinodes(antennas, W, H):
    antinodes = set()
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
        # Find all unique lines defined by pairs of antennas
        lines = set()
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                A = positions[i]
                B = positions[j]
                # Compute standardized line equation
                x1, y1 = A
                x2, y2 = B
                A_line = y2 - y1
                B_line = x1 - x2
                C_line = x2 * y1 - x1 * y2
                # Compute GCD of A, B, and C
                gcd_val = gcd(gcd(abs(A_line), abs(B_line)), abs(C_line))
                A_std = A_line // gcd_val
                B_std = B_line // gcd_val
                C_std = C_line // gcd_val
                # Ensure A is non-negative, and if A=0, B is positive
                if A_std < 0 or (A_std == 0 and B_std < 0):
                    A_std = -A_std
                    B_std = -B_std
                    C_std = -C_std
                lines.add((A_std, B_std, C_std))
        # For each unique line, find all grid points on the line within bounds
        for A, B, C in lines:
            if B != 0:
                # y = (-A*x - C)/B
                for x in range(W):
                    numerator = -A * x - C
                    if numerator % B != 0:
                        continue
                    y = numerator // B
                    if 0 <= y < H:
                        antinodes.add((x, y))
            elif A != 0:
                # Vertical line: x = -C/A
                if -C % A != 0:
                    continue
                x = -C // A
                if 0 <= x < W:
                    for y in range(H):
                        antinodes.add((x, y))
            else:
                # Invalid line (A=0 and B=0), should not happen
                continue
    return antinodes


def main():
    grid = read_input()
    antennas, W, H = parse_antennas(grid)
    antinodes_part1 = compute_part1_antinodes(antennas, W, H)
    print(f"Part 1: {len(antinodes_part1)}")
    antinodes_part2 = compute_part2_antinodes(antennas, W, H)
    print(f"Part 2: {len(antinodes_part2)}")


if __name__ == "__main__":
    main()
