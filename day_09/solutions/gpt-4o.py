def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(disk_map: str):
    """
    Parse the input string into a list of tuples representing files and free space.
    Each tuple contains (length, type), where type is either 'file' or 'space'.
    """
    parsed = []
    i = 0
    while i < len(disk_map):
        length = int(disk_map[i])
        if i % 2 == 0:
            parsed.append((length, "file"))
        else:
            parsed.append((length, "space"))
        i += 1
    return parsed


def construct_block_representation(parsed):
    """
    Construct the initial block representation based on the parsed input.
    """
    blocks = []
    file_id = 0
    for length, type_ in parsed:
        if type_ == "file":
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend([None] * length)
    return blocks


def compact_disk(blocks):
    """
    Compact the disk by moving each file block one at a time to the leftmost available space.
    """
    n = len(blocks)
    for i in range(n - 1, -1, -1):
        if blocks[i] is not None:
            file_id = blocks[i]
            blocks[i] = None
            # Find the leftmost free space
            for j in range(n):
                if blocks[j] is None:
                    blocks[j] = file_id
                    break
    return blocks


def calculate_checksum(blocks):
    """
    Calculate the checksum based on the final block representation.
    """
    checksum = 0
    for i, block in enumerate(blocks):
        if block is not None:
            checksum += i * block
    return checksum


def compact_disk_by_file(blocks):
    """
    Compact the disk by moving entire files to the leftmost available space that fits.
    """
    file_positions = {}
    # Determine file positions
    for i, block in enumerate(blocks):
        if block is not None:
            if block not in file_positions:
                file_positions[block] = []
            file_positions[block].append(i)

    # Move files in descending order of file ID
    for file_id in sorted(file_positions.keys(), reverse=True):
        file_blocks = file_positions[file_id]
        file_length = len(file_blocks)

        # Find the leftmost span of free space that can fit the file
        n = len(blocks)
        for start in range(n - file_length + 1):
            if all(blocks[start + k] is None for k in range(file_length)):
                # Move the file to this position
                for pos in file_blocks:
                    blocks[pos] = None
                for k in range(file_length):
                    blocks[start + k] = file_id
                break

    return blocks


def part1(data: str) -> int:
    parsed = parse_disk_map(data)
    blocks = construct_block_representation(parsed)
    compacted_blocks = compact_disk(blocks)
    return calculate_checksum(compacted_blocks)


def part2(data: str) -> int:
    parsed = parse_disk_map(data)
    blocks = construct_block_representation(parsed)
    compacted_blocks = compact_disk_by_file(blocks)
    return calculate_checksum(compacted_blocks)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
