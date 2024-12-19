import re


def read_input():
    with open("../input.txt", "r") as f:
        return f.read().strip()


def run_program(program, initial_a=0, initial_b=0, initial_c=0):
    # Convert program to list of integers
    program = list(map(int, program.split(",")))

    # Initialize registers
    registers = {"A": initial_a, "B": initial_b, "C": initial_c}

    # Output list to collect values from out instructions
    output = []

    # Instruction pointer
    ip = 0

    while ip < len(program):
        # Check if we can read an opcode and operand
        if ip + 1 >= len(program):
            break

        opcode = program[ip]
        operand = program[ip + 1]

        # Determine operand value based on its type
        def get_operand_value(op):
            if 0 <= op <= 3:
                return op
            elif op == 4:
                return registers["A"]
            elif op == 5:
                return registers["B"]
            elif op == 6:
                return registers["C"]
            return 0

        # Execute instructions based on opcode
        if opcode == 0:  # adv: division
            power = 2 ** get_operand_value(operand)
            registers["A"] = registers["A"] // power

        elif opcode == 1:  # bxl: bitwise XOR with literal
            registers["B"] ^= operand

        elif opcode == 2:  # bst: set B to operand % 8
            registers["B"] = operand % 8

        elif opcode == 3:  # jnz: jump if A is not zero
            if registers["A"] != 0:
                ip = operand
                continue

        elif opcode == 4:  # bxc: bitwise XOR B with C
            registers["B"] ^= registers["C"]

        elif opcode == 5:  # out: output value
            output.append(get_operand_value(operand))

        elif opcode == 6:  # bdv: division result to B
            power = 2 ** get_operand_value(operand)
            registers["B"] = registers["A"] // power

        elif opcode == 7:  # cdv: division result to C
            power = 2 ** get_operand_value(operand)
            registers["C"] = registers["A"] // power

        # Move instruction pointer
        ip += 2

    return output


def part1(data):
    # Calculate output with initial registers
    output = run_program(data, initial_a=729)
    return ",".join(map(str, output))


def part2(data):
    # Find lowest A that produces a copy of the program
    for a in range(1, 1_000_000):
        output = run_program(data, initial_a=a)
        output_str = ",".join(map(str, output))

        # Check if output matches the original program
        if output_str == data:
            return a

    return None


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
