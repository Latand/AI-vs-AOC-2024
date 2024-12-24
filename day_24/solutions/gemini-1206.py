import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def simulate(initial_values, gates):
    values = initial_values.copy()
    while True:
        updated = False
        for gate in gates:
            inputs = [values.get(inp, None) for inp in gate["inputs"]]
            if all(inp is not None for inp in inputs):
                if gate["type"] == "AND":
                    result = 1 if all(inp == 1 for inp in inputs) else 0
                elif gate["type"] == "OR":
                    result = 1 if any(inp == 1 for inp in inputs) else 0
                elif gate["type"] == "XOR":
                    result = 1 if sum(inputs) % 2 == 1 else 0
                else:
                    raise ValueError(f"Unknown gate type: {gate['type']}")

                if values.get(gate["output"], None) != result:
                    values[gate["output"]] = result
                    updated = True
        if not updated:
            break
    return values


def parse_input(data):
    initial_values = {}
    gates = []
    initial_values_lines, gates_lines = data.split("\n\n")

    for line in initial_values_lines.split("\n"):
        match = re.match(r"(\w+): (\d)", line)
        if match:
            wire, value = match.groups()
            initial_values[wire] = int(value)

    for line in gates_lines.split("\n"):
        match = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line)
        if match:
            inp1, gate_type, inp2, output = match.groups()
            gates.append({"type": gate_type, "inputs": [inp1, inp2], "output": output})

    return initial_values, gates


def part1(data: str) -> int:
    initial_values, gates = parse_input(data)
    final_values = simulate(initial_values, gates)

    z_wires = sorted([wire for wire in final_values if wire.startswith("z")])
    binary_str = "".join(str(final_values[wire]) for wire in z_wires[::-1])
    return int(binary_str, 2)


def part2(data: str) -> str:
    initial_values, gates = parse_input(data)
    num_x = len([wire for wire in initial_values if wire.startswith("x")])
    num_y = len([wire for wire in initial_values if wire.startswith("y")])
    num_z = len(
        set([gate["output"] for gate in gates if gate["output"].startswith("z")])
    )

    swapped_wires = []
    for i in range(1 << (num_x + num_y)):
        x_vals = {}
        y_vals = {}
        temp_initial_values = {}
        for j in range(num_x):
            x_vals[f"x{j:02}"] = (i >> j) & 1
            temp_initial_values[f"x{j:02}"] = (i >> j) & 1
        for j in range(num_y):
            y_vals[f"y{j:02}"] = (i >> (j + num_x)) & 1
            temp_initial_values[f"y{j:02}"] = (i >> (j + num_x)) & 1

        x_num = int(
            "".join(str(x_vals[f"x{j:02}"]) for j in range(num_x - 1, -1, -1)), 2
        )
        y_num = int(
            "".join(str(y_vals[f"y{j:02}"]) for j in range(num_y - 1, -1, -1)), 2
        )
        expected_z_num = x_num + y_num
        expected_z_binary = bin(expected_z_num)[2:].zfill(num_z)

        final_values = simulate(temp_initial_values, gates)
        actual_z_binary = "".join(
            str(final_values.get(f"z{j:02}", 0)) for j in range(num_z - 1, -1, -1)
        )

        if actual_z_binary != expected_z_binary:
            diff_bits = [
                j for j in range(num_z) if actual_z_binary[j] != expected_z_binary[j]
            ]
            swapped_wires.append(diff_bits)

    potential_swaps = {}
    for i in range(len(swapped_wires)):
        for j in range(i + 1, len(swapped_wires)):
            s1 = set(swapped_wires[i])
            s2 = set(swapped_wires[j])
            if len(s1.intersection(s2)) == 0 and len(s1) == len(s2):
                key = tuple(sorted(list(s1) + list(s2)))
                potential_swaps[key] = potential_swaps.get(key, 0) + 1

    swaps = []
    for k, v in potential_swaps.items():
        if v > 50:
            swaps.append(k)

    swapped_wires_names = []

    for gate in gates:
        for swap in swaps:
            if int(gate["output"][1:]) in swap:
                swapped_wires_names.append(gate["output"])

    swapped_wires_names = sorted(list(set(swapped_wires_names)))
    return ",".join(swapped_wires_names)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
