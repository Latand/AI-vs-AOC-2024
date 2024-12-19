import re
from typing import List, Dict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


class ThreeBitComputer:
    def __init__(self, program: List[int], registers: Dict[str, int] = None):
        self.program = program
        self.registers = registers if registers else {"A": 0, "B": 0, "C": 0}
        self.ip = 0
        self.output = []

    def get_operand_value(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.registers["A"]
        elif operand == 5:
            return self.registers["B"]
        elif operand == 6:
            return self.registers["C"]
        else:
            raise ValueError(f"Invalid combo operand: {operand}")

    def execute_instruction(self, opcode: int, operand: int):
        if opcode == 0:  # adv
            denominator = 2 ** self.get_operand_value(operand)
            if denominator == 0:
                self.registers["A"] = 0
            else:
                self.registers["A"] = self.registers["A"] // denominator
            self.ip += 2
        elif opcode == 1:  # bxl
            self.registers["B"] ^= operand
            self.ip += 2
        elif opcode == 2:  # bst
            self.registers["B"] = operand % 8
            self.ip += 2
        elif opcode == 3:  # jnz
            if self.registers["A"] != 0:
                self.ip = operand
            else:
                self.ip += 2
        elif opcode == 4:  # bxc
            self.registers["B"] ^= self.registers["C"]
            self.ip += 2
        elif opcode == 5:  # out
            value = operand % 8
            self.output.append(str(value))
            self.ip += 2
        elif opcode == 6:  # bdv
            denominator = 2 ** self.get_operand_value(operand)
            if denominator == 0:
                self.registers["B"] = 0
            else:
                self.registers["B"] = self.registers["A"] // denominator
            self.ip += 2
        elif opcode == 7:  # cdv
            denominator = 2 ** self.get_operand_value(operand)
            if denominator == 0:
                self.registers["C"] = 0
            else:
                self.registers["C"] = self.registers["A"] // denominator
            self.ip += 2
        else:
            raise ValueError(f"Invalid opcode: {opcode}")

    def run(self):
        while self.ip < len(self.program):
            opcode = self.program[self.ip]
            if self.ip + 1 < len(self.program):
                operand = self.program[self.ip + 1]
            else:
                operand = 0  # Default operand if missing
            self.execute_instruction(opcode, operand)

    def get_output(self) -> str:
        return ",".join(self.output)


def parse_program(data: str) -> List[int]:
    return [int(num) for num in re.findall(r"\b\d+\b", data)]


def part1(data: str) -> str:
    program = parse_program(data)
    computer = ThreeBitComputer(program)
    computer.run()
    return computer.get_output()


def find_initial_A(program: List[int]) -> int:
    initial_A = 1
    while True:
        computer = ThreeBitComputer(program, registers={"A": initial_A, "B": 0, "C": 0})
        computer.run()
        output = computer.get_output().replace(",", "")
        program_str = ",".join(map(str, program))
        if output == program_str:
            return initial_A
        initial_A += 1
        if initial_A > 10**6:
            raise ValueError(
                "Suitable initial A value not found within reasonable range."
            )


def part2(data: str) -> int:
    program = parse_program(data)
    return find_initial_A(program)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
