import re
from typing import Dict, List, Tuple


class GateSystem:
    def __init__(self):
        self.wires: Dict[str, int] = {}
        self.gates: List[Tuple[str, str, str, str]] = []

    def parse_input(self, data: str):
        sections = data.splitlines()
        # Parse initial wire values
        for line in sections:
            if ":" in line:
                wire, value = line.split(":")
                self.wires[wire.strip()] = int(value.strip())
            else:
                # Parse gate operations
                match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", line)
                if match:
                    input1, operation, input2, output = match.groups()
                    self.gates.append((input1, operation, input2, output))

    def evaluate_gate(self, input1: int, operation: str, input2: int) -> int:
        if operation == "AND":
            return input1 & input2
        elif operation == "OR":
            return input1 | input2
        elif operation == "XOR":
            return input1 ^ input2
        return 0

    def process_gates(self):
        for input1, operation, input2, output in self.gates:
            if input1 in self.wires and input2 in self.wires:
                result = self.evaluate_gate(
                    self.wires[input1], operation, self.wires[input2]
                )
                self.wires[output] = result

    def get_result(self) -> int:
        # Combine the bits from wires starting with 'z'
        result = 0
        for i in range(len(self.wires)):
            if f"z" in self.wires:
                print(f"z{i:02}", self.wires[f"z{i:02}"])
                result |= self.wires[f"z{i:02}"] << i
        return result


def read_input() -> str:
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    system = GateSystem()
    system.parse_input(data)
    system.process_gates()
    return system.get_result()


def part2(data: str) -> int:
    # For part 2, we would need to implement the logic for swapping gates
    # This is a placeholder for the actual implementation
    return 0  # Replace with actual logic


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
