import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def get_combo_value(operand, registers):
    if operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        return operand  # for 0-3


def simulate_program(initial_A, initial_B, initial_C, program):
    registers = {"A": initial_A, "B": initial_B, "C": initial_C}
    IP = 0
    outputs = []
    program_length = len(program)

    while IP < program_length:
        if IP + 1 >= program_length:
            break  # Invalid instruction, halt
        opcode = program[IP]
        operand = program[IP + 1]

        if opcode == 0:  # adv
            denominator = 2 ** get_combo_value(operand, registers)
            registers["A"] = registers["A"] // denominator
            IP += 2
        elif opcode == 1:  # bxl
            literal = operand
            registers["B"] = registers["B"] ^ literal
            IP += 2
        elif opcode == 2:  # bst
            combo = operand
            value = get_combo_value(combo, registers) % 8
            registers["B"] = value
            IP += 2
        elif opcode == 3:  # jnz
            literal = operand
            if registers["A"] != 0:
                IP = literal
            else:
                IP += 2
        elif opcode == 4:  # bxc
            # Ignore operand
            registers["B"] = registers["B"] ^ registers["C"]
            IP += 2
        elif opcode == 5:  # out
            combo = operand
            value = get_combo_value(combo, registers) % 8
            outputs.append(str(value))
            IP += 2
        elif opcode == 6:  # bdv
            denominator = 2 ** get_combo_value(operand, registers)
            registers["B"] = registers["A"] // denominator
            IP += 2
        elif opcode == 7:  # cdv
            denominator = 2 ** get_combo_value(operand, registers)
            registers["C"] = registers["A"] // denominator
            IP += 2
        else:
            IP += 2  # Invalid opcode, skip
    return ",".join(outputs)


def part1(data: str) -> str:
    reg_a_match = re.search(r"Register A: (\d+)", data)
    reg_b_match = re.search(r"Register B: (\d+)", data)
    reg_c_match = re.search(r"Register C: (\d+)", data)
    program_match = re.search(r"Program: (.*)", data)

    if not (reg_a_match and reg_b_match and reg_c_match and program_match):
        return "Invalid input format"

    A = int(reg_a_match.group(1))
    B = int(reg_b_match.group(1))
    C = int(reg_c_match.group(1))
    program_str = program_match.group(1)
    program = list(map(int, program_str.split(",")))

    output = simulate_program(A, B, C, program)
    return output


def part2(data: str) -> int:
    reg_a_match = re.search(r"Register A: (\d+)", data)
    reg_b_match = re.search(r"Register B: (\d+)", data)
    reg_c_match = re.search(r"Register C: (\d+)", data)
    program_match = re.search(r"Program: (.*)", data)

    if not (reg_a_match and reg_b_match and reg_c_match and program_match):
        return -1  # Invalid input format

    initial_A = int(reg_a_match.group(1))
    B = int(reg_b_match.group(1))
    C = int(reg_c_match.group(1))
    program_str = program_match.group(1)
    program = list(map(int, program_str.split(",")))

    # Find the smallest positive A
    for A in range(1, 1000000):  # Set a reasonable upper limit
        output = simulate_program(A, B, C, program)
        expected_output = ",".join(map(str, program))
        if output == expected_output:
            return A
    return -1  # Not found within the limit


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
