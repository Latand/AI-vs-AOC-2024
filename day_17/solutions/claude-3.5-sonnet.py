import re
from typing import List, Tuple


def parse_input(data: str) -> Tuple[int, int, int, List[int]]:
    """Parse input using regexp to extract register values and program."""
    # Extract register values
    reg_pattern = r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)"
    reg_match = re.search(reg_pattern, data)
    if not reg_match:
        raise ValueError("Could not parse register values")

    reg_a = int(reg_match.group(1))
    reg_b = int(reg_match.group(2))
    reg_c = int(reg_match.group(3))

    # Extract program
    prog_pattern = r"Program: ([\d,]+)"
    prog_match = re.search(prog_pattern, data)
    if not prog_match:
        raise ValueError("Could not parse program")

    program = [int(x) for x in prog_match.group(1).split(",")]
    return reg_a, reg_b, reg_c, program


class Computer:
    def __init__(self, reg_a: int, reg_b: int, reg_c: int, program: List[int]):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.program = program
        self.ip = 0  # instruction pointer
        self.output = []

    def get_combo_value(self, operand: int) -> int:
        """Get value based on combo operand rules."""
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.reg_a
        elif operand == 5:
            return self.reg_b
        elif operand == 6:
            return self.reg_c
        else:
            raise ValueError(f"Invalid combo operand: {operand}")

    def run(self) -> List[int]:
        """Run the program and return output."""
        while self.ip < len(self.program):
            opcode = self.program[self.ip]
            operand = (
                self.program[self.ip + 1] if self.ip + 1 < len(self.program) else 0
            )

            if opcode == 0:  # adv
                self.reg_a //= 1 << self.get_combo_value(operand)
                self.ip += 2
            elif opcode == 1:  # bxl
                self.reg_b ^= operand
                self.ip += 2
            elif opcode == 2:  # bst
                self.reg_b = self.get_combo_value(operand) % 8
                self.ip += 2
            elif opcode == 3:  # jnz
                if self.reg_a != 0:
                    self.ip = operand
                else:
                    self.ip += 2
            elif opcode == 4:  # bxc
                self.reg_b ^= self.reg_c
                self.ip += 2
            elif opcode == 5:  # out
                self.output.append(self.get_combo_value(operand) % 8)
                self.ip += 2
            elif opcode == 6:  # bdv
                self.reg_b = self.reg_a // (1 << self.get_combo_value(operand))
                self.ip += 2
            elif opcode == 7:  # cdv
                self.reg_c = self.reg_a // (1 << self.get_combo_value(operand))
                self.ip += 2
            else:
                raise ValueError(f"Invalid opcode: {opcode}")

        return self.output


def part1(data: str) -> str:
    """Solve part 1: Run program and get output."""
    reg_a, reg_b, reg_c, program = parse_input(data)
    computer = Computer(reg_a, reg_b, reg_c, program)
    output = computer.run()
    return ",".join(str(x) for x in output)


def part2(data: str) -> int:
    """Solve part 2: Find lowest value of reg_a that outputs program."""
    _, reg_b, reg_c, program = parse_input(data)

    # Try values for register A until we find one that outputs the program
    for reg_a in range(1, 1000000):  # Reasonable upper limit
        computer = Computer(reg_a, reg_b, reg_c, program)
        output = computer.run()

        # Check if output matches program
        if len(output) == len(program) and all(x == y for x, y in zip(output, program)):
            return reg_a

    return -1


def main():
    data = open("../input.txt").read().strip()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
