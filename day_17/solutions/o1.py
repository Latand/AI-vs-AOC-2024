import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def combo_operand_value(op, A, B, C):
    """Return the value of the combo operand."""
    if op <= 3:
        return op  # literal 0-3
    elif op == 4:
        return A
    elif op == 5:
        return B
    elif op == 6:
        return C
    else:
        # op == 7 should never appear in valid programs
        raise ValueError("Invalid combo operand 7 encountered.")


def run_program(A_init, B_init, C_init, program, collect_output=False):
    """Run the given program with initial registers and return final registers and output.
    If collect_output=True, returns output as a list of integers.
    """
    A, B, C = A_init, B_init, C_init
    IP = 0
    output = []

    while IP < len(program):
        opcode = program[IP]
        if IP + 1 >= len(program):
            # No operand means we halt
            break
        operand = program[IP + 1]

        # Instruction pointer normally advances by 2
        next_IP = IP + 2

        if opcode == 0:  # adv
            # operand is combo; denominator = 2^(combo_operand_value)
            denom_exp = combo_operand_value(operand, A, B, C)
            denom = 2**denom_exp
            A = A // denom
        elif opcode == 1:  # bxl
            # operand is literal
            B = B ^ operand
        elif opcode == 2:  # bst
            # operand is combo
            val = combo_operand_value(operand, A, B, C) % 8
            B = val
        elif opcode == 3:  # jnz
            # operand is literal
            if A != 0:
                next_IP = operand
        elif opcode == 4:  # bxc
            # XOR B and C, operand ignored
            B = B ^ C
        elif opcode == 5:  # out
            # combo operand, output value % 8
            val = combo_operand_value(operand, A, B, C) % 8
            output.append(val)
        elif opcode == 6:  # bdv
            # bdv same as adv but result stored in B
            denom_exp = combo_operand_value(operand, A, B, C)
            denom = 2**denom_exp
            B = A // denom
        elif opcode == 7:  # cdv
            # cdv same as adv but result stored in C
            denom_exp = combo_operand_value(operand, A, B, C)
            denom = 2**denom_exp
            C = A // denom
        else:
            # Invalid opcode
            break

        IP = next_IP

    if collect_output:
        return output
    else:
        return A, B, C


def part1(A, B, C, program):
    # Run the program with the given initial registers
    output = run_program(A, B, C, program, collect_output=True)
    return ",".join(map(str, output))


def part2(B, C, program):
    # We want the output of the program (with some A) to match the program exactly.
    # The program instructions are all 3-bit (0-7), so output must match exactly.
    target_output = program[:]  # we want the program output to match this exactly
    # Start from A=1 and go upward until we find a match
    A_candidate = 1
    while True:
        output = run_program(A_candidate, B, C, program, collect_output=True)
        if output == target_output:
            return A_candidate
        A_candidate += 1
        # Safety check: This might run long if no solution is found.
        # In AOC, usually a solution exists quickly.
        # If needed, add a limit or heuristic.


def main():
    data = read_input()
    # Parse input with regex
    # Expected format:
    # Register A: 729
    # Register B: 0
    # Register C: 0
    #
    # Program: 0,1,5,4,3,0
    #
    # (This is just an example format from the puzzle description.)
    reg_pattern = r"Register A:\s*(\d+)\s*Register B:\s*(\d+)\s*Register C:\s*(\d+)"
    prog_pattern = r"Program:\s*([\d,]+)"
    regs = re.search(reg_pattern, data, re.MULTILINE | re.DOTALL)
    prog = re.search(prog_pattern, data, re.MULTILINE | re.DOTALL)

    if not regs or not prog:
        raise ValueError("Input format not recognized.")

    A_init = int(regs.group(1))
    B_init = int(regs.group(2))
    C_init = int(regs.group(3))
    program = list(map(int, prog.group(1).split(",")))

    # Solve part 1
    result1 = part1(A_init, B_init, C_init, program)
    print(f"Part 1: {result1}")

    # Solve part 2
    # For part 2, we ignore the given initial A and try to find a new A that makes
    # the program output a copy of itself.
    # We keep B and C as given (usually they are 0,0 but let's not assume).
    result2 = part2(B_init, C_init, program)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
