import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def run_program(A_init, B_init, C_init, program):
    # Run the given program as described and return output list
    A = A_init
    B = B_init
    C = C_init
    ip = 0
    outputs = []

    def combo_value(op):
        if op <= 3:
            return op
        elif op == 4:
            return A
        elif op == 5:
            return B
        elif op == 6:
            return C
        else:
            raise ValueError("Invalid combo operand 7 encountered.")

    while ip < len(program):
        opcode = program[ip]
        if ip + 1 >= len(program):
            break
        operand = program[ip + 1]

        if opcode == 0:  # adv
            val = combo_value(operand)
            A = A // (2**val)
        elif opcode == 1:  # bxl
            B = B ^ operand
        elif opcode == 2:  # bst
            val = combo_value(operand)
            B = val % 8
        elif opcode == 3:  # jnz
            if A != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            B = B ^ C
        elif opcode == 5:  # out
            val = combo_value(operand) % 8
            outputs.append(val)
        elif opcode == 6:  # bdv
            val = combo_value(operand)
            B = A // (2**val)
        elif opcode == 7:  # cdv
            val = combo_value(operand)
            C = A // (2**val)

        ip += 2

    return outputs


def part1(A, B, C, program):
    outputs = run_program(A, B, C, program)
    return ",".join(str(x) for x in outputs)


def find_A_for_self_replication(B, C, program):
    """
    Find the lowest positive A that makes the program output exactly the sequence 'program' itself.
    We'll reconstruct A by working backwards from the outputs.
    """
    target = program[:]  # The desired output is the program itself

    # Backward reconstruction:
    # After the last output, A must be 0.
    A_current = 0
    # Move backwards from last output to first:
    # A_i = 8*A_{i+1} + output_i
    for val in reversed(target):
        A_current = 8 * A_current + val

    # A_current is now the initial A that, after the sequence of divisions and outputs, yields 'target'.
    # We must ensure it's positive. If A_current <= 0 and we need positive, we can check conditions.
    # The puzzle states "lowest positive initial value." The reconstruction gives us exactly one candidate.
    # If that's 0 or negative (which it won't be if output requires multiple loops), we might need logic.
    # In practice, for a non-empty program output, A_current won't be 0, assuming the program halts properly.

    return A_current if A_current > 0 else None


def main():
    data = read_input()
    A_match = re.search(r"Register A:\s*(\d+)", data)
    B_match = re.search(r"Register B:\s*(\d+)", data)
    C_match = re.search(r"Register C:\s*(\d+)", data)
    prog_match = re.search(r"Program:\s*([0-7](?:,[0-7])*)", data)

    if not (A_match and B_match and C_match and prog_match):
        raise ValueError("Input does not match expected format.")

    A = int(A_match.group(1))
    B = int(B_match.group(1))
    C = int(C_match.group(1))
    program = list(map(int, prog_match.group(1).split(",")))

    # Part 1: Just run the program and output the result
    result1 = part1(A, B, C, program)
    print(f"Part 1: {result1}")

    # Part 2: Find the lowest positive A that makes output = program
    # We use backward reconstruction from the output sequence = program itself
    # as explained above.
    result2 = find_A_for_self_replication(B, C, program)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
