def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(data: str) -> list[tuple[int, int]]:
    """Parse the disk map into a list of (file_length, space_length) tuples."""
    lengths = [int(x) for x in data]
    return list(zip(lengths[::2], lengths[1::2]))


def create_block_layout(
    file_space_pairs: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Convert file/space pairs into a list of (position, file_id) tuples."""
    blocks = []
    current_pos = 0
    file_id = 0

    for file_len, space_len in file_space_pairs:
        # Add file blocks
        for _ in range(file_len):
            blocks.append((current_pos, file_id))
            current_pos += 1
        # Skip space blocks
        current_pos += space_len
        file_id += 1

    return blocks


def calculate_checksum(blocks: list[tuple[int, int]]) -> int:
    """Calculate checksum by multiplying position by file ID."""
    return sum(pos * file_id for pos, file_id in blocks)


def part1(data: str) -> int:
    """Move individual blocks from end to leftmost free space."""
    file_space_pairs = parse_disk_map(data)
    blocks = create_block_layout(file_space_pairs)

    # Convert blocks to a list where -1 represents empty space
    disk = [-1] * (sum(x + y for x, y in file_space_pairs))
    for pos, file_id in blocks:
        disk[pos] = file_id

    # Process blocks from right to left
    for i in range(len(disk) - 1, -1, -1):
        if disk[i] == -1:
            continue

        # Find leftmost empty space
        for j in range(len(disk)):
            if disk[j] == -1:
                # Move block
                disk[j] = disk[i]
                disk[i] = -1
                break

    # Create final block layout for checksum calculation
    final_blocks = [(i, file_id) for i, file_id in enumerate(disk) if file_id != -1]
    return calculate_checksum(final_blocks)


def get_file_blocks(disk: list[int], file_id: int) -> list[int]:
    """Get all positions of blocks belonging to a file."""
    return [i for i, fid in enumerate(disk) if fid == file_id]


def can_move_file(disk: list[int], start_pos: int, file_size: int) -> int:
    """Check if a file can be moved to a position and return the leftmost valid position."""
    for pos in range(start_pos):
        # Check if there's enough consecutive free space
        if all(disk[i] == -1 for i in range(pos, min(pos + file_size, len(disk)))):
            if pos + file_size <= len(disk):
                return pos
    return -1


def part2(data: str) -> int:
    """Move whole files to leftmost possible position."""
    file_space_pairs = parse_disk_map(data)
    blocks = create_block_layout(file_space_pairs)

    # Initialize disk with -1 as empty space
    disk = [-1] * (sum(x + y for x, y in file_space_pairs))
    for pos, file_id in blocks:
        disk[pos] = file_id

    # Get maximum file ID
    max_file_id = max(file_id for _, file_id in blocks)

    # Process files in decreasing order of file ID
    for file_id in range(max_file_id, -1, -1):
        file_blocks = get_file_blocks(disk, file_id)
        if not file_blocks:
            continue

        file_size = len(file_blocks)
        start_pos = min(file_blocks)

        # Find leftmost position where the whole file can fit
        new_pos = can_move_file(disk, start_pos, file_size)

        if new_pos != -1 and new_pos < start_pos:
            # Clear old positions
            for pos in file_blocks:
                disk[pos] = -1

            # Move file to new position
            for i in range(file_size):
                disk[new_pos + i] = file_id

    # Create final block layout for checksum calculation
    final_blocks = [(i, file_id) for i, file_id in enumerate(disk) if file_id != -1]
    return calculate_checksum(final_blocks)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
