import re
from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    # Parse initial wire values
    wire_values = {}
    gate_ops = []
    lines = data.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ":" in line:
            # Initial wire value
            match = re.match(r"(\w+): (\d)", line)
            if match:
                wire, val = match.groups()
                wire_values[wire] = int(val)
            i += 1
        else:
            # Gate operation
            match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", line)
            if match:
                in1, op, in2, out = match.groups()
                gate_ops.append((out, op, in1, in2))
            i += 1

    # Simulate the gates
    gates = deque(gate_ops)
    temp_gates = deque()
    while gates:
        out, op, in1, in2 = gates.popleft()
        if in1 in wire_values and in2 in wire_values:
            val1 = wire_values[in1]
            val2 = wire_values[in2]
            if op == "AND":
                result = val1 & val2
            elif op == "OR":
                result = val1 | val2
            elif op == "XOR":
                result = val1 ^ val2
            else:
                result = 0
            wire_values[out] = result
        else:
            temp_gates.append((out, op, in1, in2))
        if not gates:
            gates, temp_gates = temp_gates, gates

    # Collect z wires
    z_wires = [wire for wire in wire_values if wire.startswith("z")]
    z_wires_sorted = sorted(z_wires, key=lambda x: int(x[1:]))
    binary_str = "".join(str(wire_values[w]) for w in z_wires_sorted)
    decimal_num = int(binary_str, 2)
    return decimal_num


def part2(data: str) -> str:
    # Parse initial wire values and gate operations
    wire_values = {}
    gate_ops = []
    lines = data.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ":" in line:
            # Initial wire value
            match = re.match(r"(\w+): (\d)", line)
            if match:
                wire, val = match.groups()
                wire_values[wire] = int(val)
            i += 1
        else:
            # Gate operation
            match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", line)
            if match:
                in1, op, in2, out = match.groups()
                gate_ops.append((out, op, in1, in2))
            i += 1

    # Simulate the gates
    gates = deque(gate_ops)
    temp_gates = deque()
    while gates:
        out, op, in1, in2 = gates.popleft()
        if in1 in wire_values and in2 in wire_values:
            val1 = wire_values[in1]
            val2 = wire_values[in2]
            if op == "AND":
                result = val1 & val2
            elif op == "OR":
                result = val1 | val2
            elif op == "XOR":
                result = val1 ^ val2
            else:
                result = 0
            wire_values[out] = result
        else:
            temp_gates.append((out, op, in1, in2))
        if not gates:
            gates, temp_gates = temp_gates, gates

    # Collect z wires
    z_wires = [wire for wire in wire_values if wire.startswith("z")]
    z_wires_sorted = sorted(z_wires, key=lambda x: int(x[1:]))
    binary_str = "".join(str(wire_values[w]) for w in z_wires_sorted)
    current_sum = int(binary_str, 2)

    # Calculate correct sum based on x and y wires
    x_wires = [wire for wire in wire_values if wire.startswith("x")]
    y_wires = [wire for wire in wire_values if wire.startswith("y")]
    x_wires_sorted = sorted(x_wires, key=lambda x: int(x[1:]))
    y_wires_sorted = sorted(y_wires, key=lambda x: int(x[1:]))
    x_bits = [str(wire_values[w]) for w in x_wires_sorted]
    y_bits = [str(wire_values[w]) for w in y_wires_sorted]
    x_num = int("".join(x_bits), 2)
    y_num = int("".join(y_bits), 2)
    correct_sum = x_num + y_num

    # Identify which z wires are incorrect
    z_positions = {int(w[1:]): w for w in z_wires_sorted}
    max_z_pos = max(z_positions.keys())
    correct_binary = bin(correct_sum)[2:].zfill(max_z_pos + 1)
    current_binary = binary_str
    differences = [
        i for i in range(len(correct_binary)) if correct_binary[i] != current_binary[i]
    ]

    # Find pairs of z wires that need to be swapped
    swapped_wires = []
    for pos in differences:
        wire1 = z_positions[pos]
        for pos2 in range(pos + 1, len(correct_binary)):
            if (
                correct_binary[pos2] == current_binary[pos]
                and current_binary[pos2] == correct_binary[pos]
            ):
                wire2 = z_positions[pos2]
                swapped_wires.extend([wire1, wire2])
                # Swap the values in wire_values
                wire_values[wire1], wire_values[wire2] = (
                    wire_values[wire2],
                    wire_values[wire1],
                )
                # Check if this fixes the sum
                binary_str = "".join(str(wire_values[w]) for w in z_wires_sorted)
                new_sum = int(binary_str, 2)
                if new_sum == correct_sum:
                    return ",".join(sorted([wire1, wire2]))
                # Swap back if not fixed
                wire_values[wire1], wire_values[wire2] = (
                    wire_values[wire2],
                    wire_values[wire1],
                )

    # If no swaps fix the sum, return the list of potential swapped wires
    return ",".join(sorted(swapped_wires))


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
