import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def run_program(program, registers):
    ip = 0
    output = []
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  # adv
            registers["A"] = registers["A"] // (
                2 ** get_combo_operand_value(operand, registers)
            )
        elif opcode == 1:  # bxl
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:  # bst
            registers["B"] = get_combo_operand_value(operand, registers) % 8
        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:  # out
            output.append(get_combo_operand_value(operand, registers) % 8)
        elif opcode == 6:  # bdv
            registers["B"] = registers["A"] // (
                2 ** get_combo_operand_value(operand, registers)
            )
        elif opcode == 7:  # cdv
            registers["C"] = registers["A"] // (
                2 ** get_combo_operand_value(operand, registers)
            )

        ip += 2
    return output


def get_combo_operand_value(operand, registers):
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        raise ValueError("Invalid combo operand")


def parse_input(data):
    lines = data.split("\n")
    registers = {}
    program = []

    for line in lines:
        if "Register" in line:
            match = re.search(r"Register (\w): (\d+)", line)
            registers[match.group(1)] = int(match.group(2))
        elif "Program" in line:
            match = re.findall(r"(\d+)", line.split(":")[1])
            program = [int(x) for x in match]

    return registers, program


def part1(data: str) -> str:
    registers, program = parse_input(data)
    output = run_program(program, registers)
    return ",".join(map(str, output))


def part2(data: str) -> int:
    _, program = parse_input(data)

    initial_a = 0
    while True:
        initial_a += 1
        registers = {"A": initial_a, "B": 0, "C": 0}
        output = run_program(program, registers)
        if output == program:
            return initial_a


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
