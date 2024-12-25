def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(disk_map: str):
    """
    Parses the disk map string into a list of blocks.
    Each block is either a file ID (integer) or None for free space.
    """
    blocks = []
    file_id = 0
    is_file = True  # Start with a file

    i = 0
    while i < len(disk_map):
        length = int(disk_map[i])
        if is_file:
            for _ in range(length):
                blocks.append(file_id)
            file_id += 1
        else:
            for _ in range(length):
                blocks.append(None)
        is_file = not is_file
        i += 1

    return blocks


def part1(data: str) -> int:
    """
    Part 1:
    Move file blocks one at a time from the end to the leftmost free space.
    Calculate the filesystem checksum after compacting.
    """
    blocks = parse_disk_map(data)

    def move_blocks(blocks):
        """
        Moves file blocks one at a time from the end to the leftmost free space.
        Returns the modified blocks.
        """
        # Iterate from left to right, keeping track of the next free position
        next_free = 0
        for current in range(len(blocks)):
            if blocks[current] is not None:
                if current != next_free:
                    # Move the block to the next free position
                    blocks[next_free] = blocks[current]
                    blocks[current] = None
                next_free += 1
        return blocks

    # Continuously move blocks until no changes occur
    previous = None
    while previous != blocks:
        previous = blocks.copy()
        blocks = move_blocks(blocks)

    # Calculate checksum
    checksum = 0
    for position, file_id in enumerate(blocks):
        if file_id is not None:
            checksum += position * file_id

    return checksum


def part2(data: str) -> int:
    """
    Part 2:
    Move whole files to the leftmost span of free space that can fit the file.
    Move files in order of decreasing file ID.
    Calculate the filesystem checksum after compacting.
    """
    blocks = parse_disk_map(data)

    # Identify files and their positions
    from collections import defaultdict

    file_positions = defaultdict(list)
    for idx, block in enumerate(blocks):
        if block is not None:
            file_positions[block].append(idx)

    # Sort file IDs in decreasing order
    sorted_file_ids = sorted(file_positions.keys(), reverse=True)

    for file_id in sorted_file_ids:
        # Get current positions of the file
        positions = file_positions[file_id]
        file_length = len(positions)

        # Find the leftmost span of free space that can fit the file
        # We need to find a consecutive sequence of None with length >= file_length
        # starting from the left
        start = 0
        while start <= len(blocks) - file_length:
            span = blocks[start : start + file_length]
            if all(block is None for block in span):
                break
            start += 1
        else:
            # No suitable span found
            continue

        # Current start of the file
        current_start = positions[0]

        if start < current_start:
            # Move the file
            # Set the new positions to file_id
            for i in range(file_length):
                blocks[start + i] = file_id
            # Set the old positions to None
            for pos in positions:
                blocks[pos] = None
            # Update file_positions
            file_positions[file_id] = list(range(start, start + file_length))

    # Calculate checksum
    checksum = 0
    for position, file_id in enumerate(blocks):
        if file_id is not None:
            checksum += position * file_id

    return checksum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
