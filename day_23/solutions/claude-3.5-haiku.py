from collections import defaultdict
from itertools import combinations


def read_input(file_path="../input.txt"):
    """
    Read the input file and parse the network connections.

    Returns:
    dict: A dictionary where keys are computers and values are sets of connected computers
    """
    network = defaultdict(set)
    with open(file_path, "r") as f:
        for line in f:
            computer1, computer2 = line.strip().split("-")
            network[computer1].add(computer2)
            network[computer2].add(computer1)
    return network


def find_triplet_connections(network):
    """
    Find all sets of three inter-connected computers.

    Args:
    network (dict): A dictionary of computer connections

    Returns:
    list: A list of computer triplets
    """
    triplets = []
    for computer, connections in network.items():
        # Find all potential combinations of two other computers
        for other1, other2 in combinations(connections, 2):
            # Check if the other two computers are also connected
            if other1 in network[other2]:
                # Sort the triplet to avoid duplicates
                triplet = sorted([computer, other1, other2])
                if triplet not in triplets:
                    triplets.append(triplet)
    return triplets


def part1(data: str) -> int:
    """
    Count the number of triplets where at least one computer
    starts with 't'.

    Args:
    data (str): Network connection data

    Returns:
    int: Number of qualifying triplets
    """
    network = read_input()
    triplets = find_triplet_connections(network)

    # Count triplets with at least one computer starting with 't'
    t_triplets = [
        triplet
        for triplet in triplets
        if any(computer.startswith("t") for computer in triplet)
    ]

    return len(t_triplets)


def find_clique(network):
    """
    Find the largest clique (fully connected subset) in the network.

    Args:
    network (dict): A dictionary of computer connections

    Returns:
    list: The largest set of fully connected computers
    """
    computers = list(network.keys())

    def is_clique(subset):
        """Check if all computers in the subset are connected to each other"""
        return all(
            other in network[computer]
            for computer in subset
            for other in subset
            if other != computer
        )

    # Try all possible subsets, starting from largest
    for size in range(len(computers), 1, -1):
        for subset in combinations(computers, size):
            if is_clique(subset):
                return list(subset)

    return []


def part2(data: str) -> str:
    """
    Find the password for the LAN party by getting
    the largest fully connected set of computers.

    Args:
    data (str): Network connection data

    Returns:
    str: Comma-separated password of computers in the clique
    """
    network = read_input()
    clique = find_clique(network)

    # Sort and join the computers to form the password
    return ",".join(sorted(clique))


def main():
    # Read the input data (though not used directly,
    # kept for consistency with problem template)
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
