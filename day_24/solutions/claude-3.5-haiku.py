import re
from typing import Dict, List, Tuple, Optional


def parse_input(data: str) -> Tuple[Dict[str, int], List[str]]:
    """
    Parse the input into initial wire values and gate connections
    """
    # Split input into initial wire values and gate connections
    parts = data.split("\n\n") if "\n\n" in data else data.split("\n")

    # Parse initial wire values
    wire_values = {}
    gate_connections = []

    # Use regex to parse initial wire values
    wire_pattern = re.compile(r"(\w+): (\d+)")
    for line in parts[0].split("\n"):
        if line.strip():
            match = wire_pattern.match(line)
            if match:
                wire_values[match.group(1)] = int(match.group(2))

    # Use regex to parse gate connections
    gate_pattern = re.compile(r"^(\w+) (\w+) (\w+) -> (\w+)$")
    if len(parts) > 1:
        for line in parts[1].split("\n"):
            if line.strip():
                gate_connections.append(line)

    return wire_values, gate_connections


def simulate_gate_system(
    wire_values: Dict[str, int], gate_connections: List[str]
) -> Dict[str, int]:
    """
    Simulate the gate system and return the final wire values
    """
    # Tracks current wire values
    current_values: Dict[str, Optional[int]] = wire_values.copy()

    # Track which connections have been processed
    processed_connections = set()

    while len(processed_connections) < len(gate_connections):
        for connection in gate_connections:
            if connection in processed_connections:
                continue

            # Parse the connection
            match = re.match(r"^(\w+)? ?(\w+) (\w+) -> (\w+)$", connection)

            if not match:
                continue

            # Unpack the match groups
            gate_type = match.group(2)
            input1 = match.group(1) or match.group(3)
            input2 = match.group(3) if match.group(1) else match.group(1)
            output = match.group(4)

            # Check if inputs are available
            if (
                input1 not in current_values
                or current_values[input1] is None
                or input2 not in current_values
                or current_values[input2] is None
            ):
                continue

            # Apply gate logic
            val1 = current_values[input1]
            val2 = current_values[input2]

            if gate_type == "AND":
                current_values[output] = val1 & val2
            elif gate_type == "OR":
                current_values[output] = val1 | val2
            elif gate_type == "XOR":
                current_values[output] = val1 ^ val2

            processed_connections.add(connection)

    return current_values


def find_swapped_wires(
    wire_values: Dict[str, int], gate_connections: List[str]
) -> List[str]:
    """
    Find the swapped wire pairs that prevent correct addition
    """
    # Try all possible wire swap combinations
    from itertools import combinations

    # Find all potential output wires
    output_wires = set()
    for connection in gate_connections:
        match = re.search(r"-> (\w+)$", connection)
        if match:
            output_wires.add(match.group(1))

    output_wires = sorted(list(output_wires))

    # Try swapping different wire combinations
    for num_swaps in range(1, 5):  # Up to 4 pairs of swaps
        for swap_combo in combinations(output_wires, num_swaps * 2):
            # Create a copy of gate connections to modify
            modified_connections = gate_connections.copy()

            # Perform wire swaps
            for i in range(0, len(swap_combo), 2):
                # Find and swap wire outputs in connections
                for j, conn in enumerate(modified_connections):
                    modified_connections[j] = (
                        conn.replace(f"-> {swap_combo[i]}", f"-> TEMP{i}")
                        .replace(f"-> {swap_combo[i+1]}", f"-> {swap_combo[i]}")
                        .replace(f"-> TEMP{i}", f"-> {swap_combo[i+1]}")
                    )

            # Test if this swap configuration leads to correct addition
            try:
                result = simulate_gate_system(wire_values, modified_connections)

                # Check if z wires represent correct addition
                x_wires = [result.get(f"x{i:02d}", 0) for i in range(20)]
                y_wires = [result.get(f"y{i:02d}", 0) for i in range(20)]
                z_wires = [result.get(f"z{i:02d}", 0) for i in range(20)]

                # Convert binary wires to integers
                x_num = int("".join(map(str, x_wires[::-1])), 2)
                y_num = int("".join(map(str, y_wires[::-1])), 2)
                z_num = int("".join(map(str, z_wires[::-1])), 2)

                # Check if the addition is correct
                if x_num + y_num == z_num:
                    return sorted(swap_combo)

            except Exception:
                continue

    return []


def part1(data: str) -> int:
    """
    Simulate the gate system and produce the output
    """
    wire_values, gate_connections = parse_input(data)
    result = simulate_gate_system(wire_values, gate_connections)

    # Collect z wire values
    z_wires = [result.get(f"z{i:02d}", 0) for i in range(20)]

    # Convert binary representation to decimal
    return int("".join(map(str, z_wires[::-1])), 2)


def part2(data: str) -> str:
    """
    Find the swapped wires that prevent correct addition
    """
    wire_values, gate_connections = parse_input(data)
    swapped_wires = find_swapped_wires(wire_values, gate_connections)

    # Return comma-separated list of swapped wires
    return ",".join(swapped_wires)


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
