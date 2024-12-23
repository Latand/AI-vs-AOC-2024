def read_input():
    with open("../input.txt") as f:
        return f.read().strip().split("\n")


def find_shortest_path(target_code):
    keypad_door = {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
    }
    keypad_robot = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}

    def is_valid(pos, keypad):
        if keypad == keypad_door:
            return pos in keypad_door.values()
        elif keypad == keypad_robot:
            return pos in keypad_robot.values()

    def get_moves(pos, keypad):
        moves = []

        if keypad == keypad_door:
            if is_valid((pos[0] - 1, pos[1]), keypad):
                moves.append(("^", (pos[0] - 1, pos[1])))
            if is_valid((pos[0] + 1, pos[1]), keypad):
                moves.append(("v", (pos[0] + 1, pos[1])))
            if is_valid((pos[0], pos[1] - 1), keypad):
                moves.append(("<", (pos[0], pos[1] - 1)))
            if is_valid((pos[0], pos[1] + 1), keypad):
                moves.append((">", (pos[0], pos[1] + 1)))
            moves.append(("A", pos))
        elif keypad == keypad_robot:
            if is_valid((pos[0] - 1, pos[1]), keypad):
                moves.append(("^", (pos[0] - 1, pos[1])))
            if is_valid((pos[0] + 1, pos[1]), keypad):
                moves.append(("v", (pos[0] + 1, pos[1])))
            if is_valid((pos[0], pos[1] - 1), keypad):
                moves.append(("<", (pos[0], pos[1] - 1)))
            if is_valid((pos[0], pos[1] + 1), keypad):
                moves.append((">", (pos[0], pos[1] + 1)))
            moves.append(("A", pos))

        return moves

    def solve_keypad(code):
        q = [("", keypad_door["A"])]
        visited = set()

        while q:
            path, current_pos = q.pop(0)
            if len(path) > 0 and path[-1] == "A":
                if len(path.replace("A", "")) == len(code):
                    temp_path = ""

                    for i in range(len(path)):
                        if path[i] != "A":
                            temp_path += path[i]
                        else:
                            temp_path += path[i]
                            if (
                                keypad_door[code[len(temp_path.replace("A", "")) - 1]]
                                != current_pos
                            ):
                                break

                    else:
                        return path

            visited.add((path, current_pos))
            for move, next_pos in get_moves(current_pos, keypad_door):
                if (path + move, next_pos) not in visited:
                    q.append((path + move, next_pos))
        return None

    def solve_robot(instructions):
        q = [("", keypad_robot["A"])]
        visited = set()

        while q:
            path, current_pos = q.pop(0)

            if len(path) > 0 and path[-1] == "A":
                if len(path.replace("A", "")) == len(instructions):
                    temp_path = ""

                    for i in range(len(path)):
                        if path[i] != "A":
                            temp_path += path[i]
                        else:
                            temp_path += path[i]

                            if (
                                keypad_robot[
                                    instructions[len(temp_path.replace("A", "")) - 1]
                                ]
                                != current_pos
                            ):
                                break

                    else:
                        return path

            visited.add((path, current_pos))
            for move, next_pos in get_moves(current_pos, keypad_robot):
                if (path + move, next_pos) not in visited:
                    q.append((path + move, next_pos))

        return None

    def solve_outer_robot(instructions):
        q = [("", keypad_robot["A"])]
        visited = set()

        while q:
            path, current_pos = q.pop(0)

            if len(path) > 0 and path[-1] == "A":
                if len(path.replace("A", "")) == len(instructions):
                    temp_path = ""

                    for i in range(len(path)):
                        if path[i] != "A":
                            temp_path += path[i]
                        else:
                            temp_path += path[i]

                            if (
                                keypad_robot[
                                    instructions[len(temp_path.replace("A", "")) - 1]
                                ]
                                != current_pos
                            ):
                                break

                    else:
                        return path

            visited.add((path, current_pos))
            for move, next_pos in get_moves(current_pos, keypad_robot):
                if (path + move, next_pos) not in visited:
                    q.append((path + move, next_pos))

        return None

    keypad_solution = solve_keypad(target_code)
    robot1_solution = solve_robot(keypad_solution)
    final_solution = solve_outer_robot(robot1_solution)

    return len(final_solution)


def part1(data):
    total_complexity = 0
    for code in data:
        shortest_length = find_shortest_path(code)
        numeric_part = int(code[:-1])
        total_complexity += shortest_length * numeric_part
    return total_complexity


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    main()
