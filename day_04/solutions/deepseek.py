def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


def part1(grid):
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
        (1, 1),  # Down-Right
        (1, -1),  # Down-Left
        (-1, 1),  # Up-Right
        (-1, -1),  # Up-Left
    ]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    count = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "X":
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    word = "X"
                    for _ in range(3):
                        if 0 <= x < rows and 0 <= y < cols:
                            word += grid[x][y]
                            x += dx
                            y += dy
                        else:
                            break
                    if word == "XMAS":
                        count += 1
            elif grid[i][j] == "S":
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    word = "S"
                    for _ in range(3):
                        if 0 <= x < rows and 0 <= y < cols:
                            word += grid[x][y]
                            x += dx
                            y += dy
                        else:
                            break
                    if word == "SAMX":
                        count += 1
    return count


def part2(grid):
    directions_pairs = [
        [(0, -1), (0, 1)],  # Left and Right
        [(-1, 0), (1, 0)],  # Up and Down
        [(-1, -1), (1, 1)],  # Up-Left and Down-Right
        [(-1, 1), (1, -1)],  # Up-Right and Down-Left
    ]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    count = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "A":
                for dir1, dir2 in directions_pairs:
                    dx1, dy1 = dir1
                    dx2, dy2 = dir2
                    x1, y1 = i + dx1, j + dy1
                    x2, y2 = i + dx2, j + dy2
                    word1 = ""
                    word2 = ""
                    for _ in range(3):
                        if 0 <= x1 < rows and 0 <= y1 < cols:
                            word1 += grid[x1][y1]
                            x1 += dx1
                            y1 += dy1
                        else:
                            break
                    for _ in range(3):
                        if 0 <= x2 < rows and 0 <= y2 < cols:
                            word2 += grid[x2][y2]
                            x2 += dx2
                            y2 += dy2
                        else:
                            break
                    if (word1 == "MAS" or word1 == "SAM") and (
                        word2 == "MAS" or word2 == "SAM"
                    ):
                        count += 1
    return count


def main():
    grid = read_input()

    result1 = part1(grid)
    print(f"Part 1: {result1}")

    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
