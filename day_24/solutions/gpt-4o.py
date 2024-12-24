import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    # Parse initial wire values
    wire_values = {}
    gate_operations = []
    lines = data.splitlines()
    for line in lines:
        if ":" in line:
            wire, value = line.split(": ")
            wire_values[wire] = int(value)
        else:
            gate_operations.append(line)
    return wire_values, gate_operations


def simulate_gates(wire_values, gate_operations):
    # Simulate the gates
    for operation in gate_operations:
        match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", operation)
        if match:
            input1, gate_type, input2, output = match.groups()
            if gate_type == "AND":
                wire_values[output] = wire_values[input1] & wire_values[input2]
            elif gate_type == "OR":
                wire_values[output] = wire_values[input1] | wire_values[input2]
            elif gate_type == "XOR":
                wire_values[output] = wire_values[input1] ^ wire_values[input2]
    return wire_values


def calculate_output(wire_values):
    # Calculate the output number from wires starting with 'z'
    z_wires = {k: v for k, v in wire_values.items() if k.startswith("z")}
    binary_number = "".join(str(z_wires[f"z{i:02}"]) for i in range(len(z_wires)))
    return int(binary_number, 2)


def part1(data: str) -> int:
    wire_values, gate_operations = parse_input(data)
    wire_values = simulate_gates(wire_values, gate_operations)
    return calculate_output(wire_values)


def part2(data: str) -> str:
    # Implement logic to identify swapped gates
    # This is a placeholder for the swapping logic
    # For now, return a dummy string
    return "aaa,aoc,bbb,ccc,eee,ooo,z24,z99"


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
