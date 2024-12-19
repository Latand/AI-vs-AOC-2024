import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    # Example input parsing using regular expressions
    # Assuming input format: "Register A: 729\nRegister B: 0\nRegister C: 0\nProgram: 0,1,5,4,3,0"
    match = re.search(
        r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\nProgram: ([\d,]+)",
        data,
    )
    if match:
        reg_a = int(match.group(1))
        reg_b = int(match.group(2))
        reg_c = int(match.group(3))
        program = list(map(int, match.group(4).split(",")))
        return reg_a, reg_b, reg_c, program
    return None, None, None, []


def execute_program(reg_a, reg_b, reg_c, program):
    output = []
    ip = 0  # instruction pointer
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1] if ip + 1 < len(program) else 0

        if opcode == 0:  # adv
            denom = (
                2**operand
                if operand < 4
                else 2 ** (reg_a if operand == 4 else reg_b if operand == 5 else reg_c)
            )
            reg_a //= denom
        elif opcode == 1:  # bxl
            reg_b ^= operand
        elif opcode == 2:  # bst
            reg_b = operand % 8
        elif opcode == 3:  # jnz
            if reg_a != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            reg_b ^= reg_c
        elif opcode == 5:  # out
            output.append(operand % 8)
        elif opcode == 6:  # bdv
            denom = (
                2**operand
                if operand < 4
                else 2 ** (reg_a if operand == 4 else reg_b if operand == 5 else reg_c)
            )
            reg_b = reg_a // denom
        elif opcode == 7:  # cdv
            denom = (
                2**operand
                if operand < 4
                else 2 ** (reg_a if operand == 4 else reg_b if operand == 5 else reg_c)
            )
            reg_c = reg_a // denom

        ip += 2

    return ",".join(map(str, output))


def part1(data: str) -> int:
    reg_a, reg_b, reg_c, program = parse_input(data)
    output = execute_program(reg_a, reg_b, reg_c, program)
    print(f"Part 1 Output: {output}")
    return 0  # Placeholder return value


def part2(data: str) -> int:
    reg_a, reg_b, reg_c, program = parse_input(data)
    # Find the lowest positive initial value for register A
    for initial_a in range(1, 1000000):  # Arbitrary large number for search
        reg_a = initial_a
        output = execute_program(reg_a, reg_b, reg_c, program)
        if output == ",".join(map(str, program)):
            print(f"Part 2 Initial A: {initial_a}")
            return initial_a
    return 0  # Placeholder return value


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
