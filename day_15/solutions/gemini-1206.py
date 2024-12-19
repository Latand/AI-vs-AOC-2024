def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    lines = data.splitlines()
    grid = []
    moves = ""
    for line in lines:
        if (
            line.startswith("#")
            or line.startswith(".")
            or line.startswith("O")
            or line.startswith("@")
        ):
            grid.append(list(line))
        elif line:
            moves = line
    return grid, moves


def find_robot(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "@":
                return r, c


def is_valid(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def move(grid, moves):
    robot_r, robot_c = find_robot(grid)
    grid[robot_r][robot_c] = "."

    dr = {"^": -1, "v": 1, "<": 0, ">": 0}
    dc = {"^": 0, "v": 0, "<": -1, ">": 1}

    for m in moves:
        nr, nc = robot_r + dr[m], robot_c + dc[m]
        if is_valid(grid, nr, nc) and grid[nr][nc] != "#":
            if grid[nr][nc] == "O":
                nnr, nnc = nr + dr[m], nc + dc[m]
                if is_valid(grid, nnr, nnc) and grid[nnr][nnc] == ".":
                    grid[nnr][nnc] = "O"
                    grid[nr][nc] = "."
                    robot_r, robot_c = nr, nc

            else:
                robot_r, robot_c = nr, nc

    grid[robot_r][robot_c] = "@"
    return grid


def calculate_gps_sum(grid):
    total_gps = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "O":
                total_gps += r * 100 + c
    return total_gps


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    grid, moves = parse_input(data)
    final_grid = move(grid, moves)
    return calculate_gps_sum(final_grid)


def resize_grid(grid):
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == "#":
                new_row.extend(["#", "#"])
            elif cell == "O":
                new_row.extend(["[", "]"])
            elif cell == ".":
                new_row.extend([".", "."])
            elif cell == "@":
                new_row.extend(["@", "."])
        new_grid.append(new_row)
    return new_grid


def move2(grid, moves):
    robot_r, robot_c = find_robot(grid)
    grid[robot_r][robot_c] = "."

    dr = {"^": -1, "v": 1, "<": 0, ">": 0}
    dc = {"^": 0, "v": 0, "<": -1, ">": 1}

    for m in moves:
        nr, nc = robot_r + dr[m], robot_c + dc[m]
        if is_valid(grid, nr, nc) and grid[nr][nc] != "#":
            if grid[nr][nc] == "[":
                nnr, nnc = nr + dr[m], nc + dc[m]

                if is_valid(grid, nnr, nnc) and (
                    grid[nnr][nnc] == "."
                    or (
                        m in "<>" and grid[nnr][nnc + 1 if m == ">" else nnc - 1] == "."
                    )
                ):
                    grid[nnr][nnc] = "["
                    grid[nnr][nnc + 1 if m == ">" else nnc - 1] = (
                        "]" if m in "<>" else "["
                    )

                    grid[nr][nc] = "."
                    grid[nr][nc + 1 if m == ">" else nc - 1] = "." if m in "<>" else "."
                    robot_r, robot_c = nr, nc

            else:
                robot_r, robot_c = nr, nc

    grid[robot_r][robot_c] = "@"
    return grid


def calculate_gps_sum2(grid):
    total_gps = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "[":
                total_gps += r * 100 + c
    return total_gps


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    grid, moves = parse_input(data)
    resized_grid = resize_grid(grid)
    final_grid = move2(resized_grid, moves)

    return calculate_gps_sum2(final_grid)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
