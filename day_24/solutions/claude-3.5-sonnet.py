import re
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Gate:
    op: str
    input1: str
    input2: str
    output: str


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str) -> Tuple[Dict[str, int], List[Gate]]:
    # Split input into initial values and gate definitions
    sections = data.strip().split("\n\n")
    initial_values = {}
    gates = []

    # Parse initial values section
    for line in sections[0].split("\n"):
        match = re.match(r"(\w+): (\d+)", line)
        if match:
            wire, value = match.groups()
            initial_values[wire] = int(value)

    # Parse gates section
    for line in sections[1].split("\n"):
        match = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", line)
        if match:
            input1, op, input2, output = match.groups()
            gates.append(Gate(op, input1, input2, output))

    return initial_values, gates


def simulate_circuit(
    initial_values: Dict[str, int],
    gates: List[Gate],
    swaps: List[Tuple[str, str]] = None,
) -> Dict[str, int]:
    wire_values = initial_values.copy()
    wire_dependencies = defaultdict(set)
    gate_outputs = {}

    # Build dependency graph
    for gate in gates:
        wire_dependencies[gate.output].add(gate.input1)
        wire_dependencies[gate.output].add(gate.input2)
        gate_outputs[gate.output] = gate

    # Apply swaps if provided
    if swaps:
        for wire1, wire2 in swaps:
            if wire1 in gate_outputs and wire2 in gate_outputs:
                gate1 = gate_outputs[wire1]
                gate2 = gate_outputs[wire2]
                gate1.output, gate2.output = gate2.output, gate1.output

    # Process gates until no more changes
    while len(wire_values) < len(wire_dependencies) + len(initial_values):
        for gate in gates:
            if gate.output in wire_values:
                continue

            if gate.input1 in wire_values and gate.input2 in wire_values:
                val1 = wire_values[gate.input1]
                val2 = wire_values[gate.input2]

                if gate.op == "AND":
                    wire_values[gate.output] = val1 & val2
                elif gate.op == "OR":
                    wire_values[gate.output] = val1 | val2
                elif gate.op == "XOR":
                    wire_values[gate.output] = val1 ^ val2

    return wire_values


def get_z_value(wire_values: Dict[str, int]) -> int:
    z_wires = sorted([wire for wire in wire_values if wire.startswith("z")])
    result = 0
    for wire in z_wires:
        result = (result << 1) | wire_values[wire]
    return result


def part1(data: str) -> int:
    initial_values, gates = parse_input(data)
    wire_values = simulate_circuit(initial_values, gates)
    return get_z_value(wire_values)


def try_swap_combination(
    initial_values: Dict[str, int], gates: List[Gate], swap_pairs: List[Tuple[str, str]]
) -> bool:
    # Test if the circuit performs addition correctly with these swaps
    wire_values = simulate_circuit(initial_values, gates, swap_pairs)

    # Get x, y, and z values as binary numbers
    x_bits = [wire_values.get(f"x{i:02d}", 0) for i in range(32)]
    y_bits = [wire_values.get(f"y{i:02d}", 0) for i in range(32)]
    z_bits = [wire_values.get(f"z{i:02d}", 0) for i in range(32)]

    # Convert to integers
    x_val = sum(bit << i for i, bit in enumerate(x_bits))
    y_val = sum(bit << i for i, bit in enumerate(y_bits))
    z_val = sum(bit << i for i, bit in enumerate(z_bits))

    return z_val == x_val + y_val


def part2(data: str) -> str:
    initial_values, gates = parse_input(data)
    all_outputs = {gate.output for gate in gates}

    # Try all possible combinations of 4 pairs of swaps
    for i in range(len(gates)):
        for j in range(i + 1, len(gates)):
            for k in range(j + 1, len(gates)):
                for l in range(k + 1, len(gates)):
                    for m in range(l + 1, len(gates)):
                        for n in range(m + 1, len(gates)):
                            for o in range(n + 1, len(gates)):
                                for p in range(o + 1, len(gates)):
                                    swap_pairs = [
                                        (gates[i].output, gates[j].output),
                                        (gates[k].output, gates[l].output),
                                        (gates[m].output, gates[n].output),
                                        (gates[o].output, gates[p].output),
                                    ]

                                    if try_swap_combination(
                                        initial_values, gates, swap_pairs
                                    ):
                                        # Return sorted list of swapped wires
                                        swapped_wires = sorted(
                                            sum(([w1, w2] for w1, w2 in swap_pairs), [])
                                        )
                                        return ",".join(swapped_wires)

    return "No solution found"


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
