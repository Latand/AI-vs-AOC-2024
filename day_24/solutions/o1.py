import re
from collections import defaultdict
import sys

sys.setrecursionlimit(100000)


def read_input():
    """
    Reads the puzzle input from ../input.txt
    """
    with open("../input.txt") as f:
        return f.read().strip()


# ============================================================
# PART 1
# ============================================================


def parse_input(data: str):
    """
    Parse the puzzle input into two sections:
      1) initial wire values
      2) gate definitions

    Returns:
      initial_values: dict of {wire_name -> int(0/1)}
      gates: list of tuples (in1, op, in2, out)
        where op is in {AND, OR, XOR}
    """
    # Regexes for parsing
    # Example lines for initial wires: "x00: 1"
    # Example lines for gates: "x00 AND y00 -> z00"
    wire_val_pattern = re.compile(r"^(\S+):\s*([01])\s*$")
    gate_pattern = re.compile(r"^(\S+)\s+(AND|OR|XOR)\s+(\S+)\s*->\s*(\S+)$")

    initial_values = {}
    gates = []

    lines = data.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Try matching wire initialization
        m_wire = wire_val_pattern.match(line)
        if m_wire:
            wire_name = m_wire.group(1)
            val_str = m_wire.group(2)
            initial_values[wire_name] = int(val_str)
            continue

        # Try matching gate definitions
        m_gate = gate_pattern.match(line)
        if m_gate:
            in1 = m_gate.group(1)
            op = m_gate.group(2)
            in2 = m_gate.group(3)
            out = m_gate.group(4)
            gates.append((in1, op, in2, out))
            continue

        # If none matched, we ignore or raise an error
        # But some puzzle inputs might have extra lines, so we just ignore them
        # print(f"WARNING: Unrecognized line: {line}")

    return initial_values, gates


def simulate_circuit(init_vals, gates):
    """
    Simulates the entire circuit (no loops) until stable.
    Returns a dict {wire -> 0/1 or None}

    - init_vals: dict of wire -> 0/1 (initially known wires)
    - gates: list of (in1, op, in2, out) describing the logic gates
    """
    # We'll collect all wire names encountered
    wire_values = defaultdict(lambda: None)
    # Set any initial wire values
    for w, v in init_vals.items():
        wire_values[w] = v

    # Because there are no loops, we can keep iterating until no changes.
    # A more efficient approach would be a topological sort, but let's do
    # repeated passes for simplicity.

    changed = True
    while changed:
        changed = False
        for w1, op, w2, out in gates:
            val1 = wire_values[w1]
            val2 = wire_values[w2]
            # We only operate if both inputs are known (not None)
            if val1 is not None and val2 is not None:
                if op == "AND":
                    new_val = 1 if (val1 == 1 and val2 == 1) else 0
                elif op == "OR":
                    new_val = 1 if (val1 == 1 or val2 == 1) else 0
                elif op == "XOR":
                    new_val = 1 if (val1 != val2) else 0
                else:
                    raise ValueError(f"Unknown operation {op}")

                if wire_values[out] is None or wire_values[out] != new_val:
                    wire_values[out] = new_val
                    changed = True

    return dict(wire_values)


def get_z_value(wire_values):
    """
    Gathers all wires that start with 'z', sorts them by the numeric suffix,
    and interprets them as a binary number (z00 is LSB, z01 is next, etc.).
    Returns that binary number as an integer.

    If a wire is missing or still None, treat it as 0 (though puzzle states
    it should eventually settle).
    """
    z_wires = []
    for w in wire_values:
        if w.startswith("z"):
            # parse the numeric suffix
            # e.g. z00 => 00
            suffix = w[1:]  # everything after 'z'
            # try to parse an integer
            # handle cases like z00, z01, z10, etc.
            try:
                idx = int(suffix)
                z_wires.append((idx, w))
            except ValueError:
                # if suffix isn't purely numeric, we skip it or put it at the end
                pass

    # sort by index
    z_wires.sort(key=lambda x: x[0])

    # Build the binary number (LSB = z00)
    bits = []
    for _, wname in z_wires:
        val = wire_values.get(wname, 0)
        if val is None:
            val = 0  # treat None as 0 if it never got resolved
        bits.append(str(val))

    # bits[0] is LSB => the string would be reversed if we just do ''.join(bits).
    # But to interpret as binary with bits[0] as LSB, we do:
    #   numeric_value = sum( (2^i)*bit_i )
    # We can just do it directly:
    result = 0
    for i, b in enumerate(bits):
        if b == "1":
            result += 1 << i

    return result


def part1(data: str) -> int:
    """
    Parse the circuit, simulate it once with the given initial values,
    and return the decimal number formed by wires starting with z.
    """
    init_vals, gates = parse_input(data)
    final_values = simulate_circuit(init_vals, gates)
    return get_z_value(final_values)


# ============================================================
# PART 2
# ============================================================


def gather_wires_and_gates(data: str):
    """
    Same parse as parse_input, but we also gather:
      - sets of x-wires, y-wires, z-wires
      - The maximum index we see for x, y, z
    We'll need this for the 'adder' check.
    """
    init_vals, gates = parse_input(data)

    # Gather all wire names:
    wires_in_gates = set()
    for i1, op, i2, o in gates:
        wires_in_gates.add(i1)
        wires_in_gates.add(i2)
        wires_in_gates.add(o)
    # Also add from init_vals
    wires_in_gates.update(init_vals.keys())

    # Distinguish them by prefix x, y, z
    x_wires = []
    y_wires = []
    z_wires = []
    for w in wires_in_gates:
        if w.startswith("x"):
            x_wires.append(w)
        elif w.startswith("y"):
            y_wires.append(w)
        elif w.startswith("z"):
            z_wires.append(w)

    # Sort them by their numeric suffix
    # e.g. x00 -> suffix = 00 -> int = 0
    def suffix_index(wn):
        # handle e.g. x00 => 0, x01 => 1, x10 => 10
        return int(wn[1:])  # skip the first char

    x_wires.sort(key=suffix_index)
    y_wires.sort(key=suffix_index)
    z_wires.sort(key=suffix_index)

    return init_vals, gates, x_wires, y_wires, z_wires


def simulate_with_forced_inputs(gates, forced_inputs):
    """
    Similar to simulate_circuit, but forced_inputs is a dict of wire->0/1
    that overrides any initial wire values from the puzzle.

    Returns final wire values.
    """
    from collections import defaultdict

    wire_values = defaultdict(lambda: None)
    # Set forced input values
    for w, v in forced_inputs.items():
        wire_values[w] = v

    changed = True
    while changed:
        changed = False
        for w1, op, w2, out in gates:
            val1 = wire_values[w1]
            val2 = wire_values[w2]
            if val1 is not None and val2 is not None:
                if op == "AND":
                    new_val = 1 if (val1 == 1 and val2 == 1) else 0
                elif op == "OR":
                    new_val = 1 if (val1 == 1 or val2 == 1) else 0
                elif op == "XOR":
                    new_val = 1 if (val1 != val2) else 0
                else:
                    raise ValueError(f"Unknown op {op}")

                if wire_values[out] is None or wire_values[out] != new_val:
                    wire_values[out] = new_val
                    changed = True

    return dict(wire_values)


def get_int_from_wires(wire_values, wires_sorted):
    """
    Given final wire_values dict (wire->0/1) and a sorted list of wires
    [lowest bit ... highest bit], produce an integer (interpreting wire i as bit i).
    """
    result = 0
    for i, w in enumerate(wires_sorted):
        bit = wire_values.get(w, 0)
        if bit is None:
            bit = 0
        if bit == 1:
            result |= 1 << i
    return result


def check_adder_correctness(gates, x_wires, y_wires, z_wires, max_tests=16):
    """
    Checks if the given gates implement z = x + y (in binary), for a subset of
    possible x,y inputs. If the circuit is large, we won't test all combos but
    a subset that should catch swaps. If it passes all tested combos, we say True,
    else False.

    gates: list of (in1, op, in2, out)
    x_wires, y_wires, z_wires: sorted lists of wire names for bits
    max_tests: up to how many distinct x,y pairs to test (used for large circuits)

    Return True if for all tested combos the circuit does correct addition.
    """
    Nx = len(x_wires)
    Ny = len(y_wires)
    # If Nx+Ny is large, we can't test all combos. We'll do a small subset.

    # We'll build a list of interesting test inputs, focusing on small numbers,
    # extremes, etc.
    test_vals_x = set()
    test_vals_y = set()

    # Always test small range 0..(2^k-1) for k up to e.g. min(Nx,4)
    # then also test some extremes.
    limit_x = min(1 << Nx, max_tests)  # we won't exceed 2^Nx
    limit_y = min(1 << Ny, max_tests)  # we won't exceed 2^Ny

    # We'll choose e.g. 0..limit_x-1 for x, similarly for y,
    # plus maybe the max values if Nx or Ny is large.
    for i in range(limit_x):
        test_vals_x.add(i)
    if (1 << Nx) - 1 not in test_vals_x:
        test_vals_x.add((1 << Nx) - 1)
    for i in range(limit_y):
        test_vals_y.add(i)
    if (1 << Ny) - 1 not in test_vals_y:
        test_vals_y.add((1 << Ny) - 1)

    for xv in test_vals_x:
        for yv in test_vals_y:
            # Force these bits into x_wires, y_wires
            forced = {}
            for i, w in enumerate(x_wires):
                forced[w] = (xv >> i) & 1
            for i, w in enumerate(y_wires):
                forced[w] = (yv >> i) & 1

            final_vals = simulate_with_forced_inputs(gates, forced)
            # read z
            zv = get_int_from_wires(final_vals, z_wires)
            # check if zv == xv + yv
            if zv != (xv + yv):
                return False

    return True


def find_swapped_pairs_for_adder(gates, x_wires, y_wires, z_wires):
    """
    We know exactly 4 pairs of gates have had their output wires swapped.
    A gate's output can only appear in at most one swapped pair.

    We will attempt a (potentially large) backtracking / search:
      1) We consider all pairs of gates G_i, G_j (with i<j).
      2) We try picking 4 distinct such pairs to swap the outputs.
      3) After applying those swaps, we check if the circuit is correct (z = x+y).
         - we do a partial test using check_adder_correctness
      4) If correct, we revert the swaps and record the pairs that worked.

    Because the puzzle states there's a unique solution, we stop when we find it.

    This can be very expensive if there are many gates, but it's the straightforward method.

    Returns: A list of 4 pairs ( (wireA, wireB), (wireC, wireD), (wireE, wireF), (wireG, wireH) )
             where each is the swapped wire outputs. If none found, returns [].
    """
    # Build a list of gates with indices
    # gates[i] = (in1, op, in2, out)
    G = len(gates)
    if G < 8:
        # If fewer than 8 gates, we can't even swap 4 pairs of distinct outputs.
        return []

    # Precompute a fast copy of gates (mutable version):
    gates_mod = [list(g) for g in gates]  # each gate is [in1, op, in2, out]

    # We'll pick all possible pairs of gates i<j in a list
    # Then we need to pick exactly 4 distinct pairs from that list such that
    # no gate is repeated (because a gate's output can't be swapped multiple times).
    all_pairs = []
    for i in range(G):
        for j in range(i + 1, G):
            all_pairs.append((i, j))
    # We could do a backtracking that picks 4 distinct pairs among these.
    # Then for each pair, we swap the outputs. Then test. If correct => done.

    # Because this can be huge, we do a depth-limited search.
    # We'll store solutions as we go.
    found_solution = []

    # We'll define a recursive function
    def backtrack(idx, chosen_pairs, used_gates):
        nonlocal found_solution
        if found_solution:  # if we found a solution, skip
            return
        if len(chosen_pairs) == 4:
            # Apply these 4 swaps
            swap_set = []
            for gi, gj in chosen_pairs:
                # swap gates_mod[gi].out and gates_mod[gj].out
                outA = gates_mod[gi][3]
                outB = gates_mod[gj][3]
                gates_mod[gi][3], gates_mod[gj][3] = outB, outA
                swap_set.append((gi, gj))

            # Now test correctness
            if check_adder_correctness(gates_mod, x_wires, y_wires, z_wires):
                found_solution = chosen_pairs[:]
                # revert swaps so we can continue searching (or stop)
                for gi, gj in reversed(chosen_pairs):
                    outA = gates_mod[gi][3]
                    outB = gates_mod[gj][3]
                    gates_mod[gi][3], gates_mod[gj][3] = outB, outA
                return

            # revert swaps
            for gi, gj in reversed(chosen_pairs):
                outA = gates_mod[gi][3]
                outB = gates_mod[gj][3]
                gates_mod[gi][3], gates_mod[gj][3] = outB, outA

            return

        if idx >= len(all_pairs):
            return

        # We have two choices: either skip this pair or use it (if possible)
        # 1) skip
        backtrack(idx + 1, chosen_pairs, used_gates)
        if found_solution:
            return

        # 2) try to use all_pairs[idx], if it doesn't conflict with used_gates
        (gi, gj) = all_pairs[idx]
        if (gi not in used_gates) and (gj not in used_gates):
            # pick it
            chosen_pairs.append((gi, gj))
            used_gates.add(gi)
            used_gates.add(gj)
            backtrack(idx + 1, chosen_pairs, used_gates)
            if found_solution:
                return
            # revert
            chosen_pairs.pop()
            used_gates.remove(gi)
            used_gates.remove(gj)

    backtrack(0, [], set())

    if not found_solution:
        return []

    # found_solution is a list of 4 pairs of (gi, gj)
    # we must return the swapped wire names from these pairs
    swapped_wires = []
    for gi, gj in found_solution:
        # original gates' outputs in the *original* list:
        outA = gates[gi][3]
        outB = gates[gj][3] if False else gates[gj][3]  # fix a minor var name
        # ^ minor correction: let's store them from gates, not gates_mod
        outA = gates[gi][3]
        outB = gates[gj][3]
        swapped_wires.append((outA, outB))

    return swapped_wires


def part2(data: str) -> str:
    """
    We know the circuit is intended to be an adder for any x,y.
    Exactly four pairs of gate outputs have been swapped.

    We want to find which wires are swapped. We then sort the
    eight wire names and return them joined by commas.

    If no solution is found, return an empty string or some notice.
    """
    init_vals, gates, x_wires, y_wires, z_wires = gather_wires_and_gates(data)

    # If the circuit is already correct (no swaps needed), we can check first:
    if check_adder_correctness(gates, x_wires, y_wires, z_wires):
        # Then no pairs need swapping => solution is empty
        return ""

    # Otherwise, find the 4 pairs.
    swaps = find_swapped_pairs_for_adder(gates, x_wires, y_wires, z_wires)
    if not swaps:
        # No solution found
        return ""

    # We have a list of 4 pairs of (wireA, wireB).
    # We want to produce 8 wires, sorted by name.
    wire_list = []
    for wa, wb in swaps:
        wire_list.append(wa)
        wire_list.append(wb)

    wire_list.sort()
    return ",".join(wire_list)


def main():
    data = read_input()

    # Part 1
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2
    # (this might be expensive; for large puzzles it might take a long time)
    result2 = part2(data)
    # If result2 is empty string, either no solution or circuit was already correct.
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
