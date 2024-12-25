def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(disk_map: str):
    """
    Parse the disk map into a list of file lengths and free space lengths.
    """
    parsed = []
    current_num = ""
    for char in disk_map:
        if current_num and char != current_num[0]:
            parsed.append(int(current_num))
            current_num = char
        else:
            current_num += char

    if current_num:
        parsed.append(int(current_num))

    return parsed


def compact_disk_block_by_block(disk_map: str) -> int:
    """
    Compact the disk by moving individual blocks to the leftmost free space.

    Part 1 solution.
    """
    # Convert disk map to a list where each character represents a block
    blocks = []
    file_id = 0
    for length_str in parse_disk_map(disk_map):
        blocks.extend(
            [str(file_id)] * length_str if length_str > 0 else ["."] * abs(length_str)
        )
        if length_str > 0:
            file_id += 1

    # Compact blocks
    while "." in blocks:
        # Find the last block that is not free space
        last_file_block_index = len(blocks) - 1
        while last_file_block_index >= 0 and blocks[last_file_block_index] == ".":
            last_file_block_index -= 1

        # If we can't move the last block, we're done
        if last_file_block_index < 0:
            break

        # Find the leftmost free space
        leftmost_free = blocks.index(".")

        # Swap the last block with the leftmost free space
        blocks[leftmost_free], blocks[last_file_block_index] = (
            blocks[last_file_block_index],
            blocks[leftmost_free],
        )

    # Calculate checksum
    checksum = 0
    for i, block in enumerate(blocks):
        if block != ".":
            checksum += i * int(block)

    return checksum


def compact_disk_whole_files(disk_map: str) -> int:
    """
    Compact the disk by moving whole files to the leftmost free space.

    Part 2 solution.
    """
    # Parse the disk map
    parsed_map = parse_disk_map(disk_map)

    # Create blocks representing the initial state
    blocks = []
    file_id = 0
    for length_str in parsed_map:
        blocks.extend(
            [str(file_id)] * length_str if length_str > 0 else ["."] * abs(length_str)
        )
        if length_str > 0:
            file_id += 1

    # Iterate from highest file ID to lowest
    max_file_id = max(int(block) for block in blocks if block != ".")

    for current_file_id in range(max_file_id, -1, -1):
        # Find the file blocks
        file_blocks = [
            i for i, block in enumerate(blocks) if block == str(current_file_id)
        ]

        if not file_blocks:
            continue

        file_length = len(file_blocks)

        # Find leftmost free space large enough
        left_space_start = None
        consecutive_free_count = 0
        for i in range(len(blocks)):
            if blocks[i] == ".":
                consecutive_free_count += 1
                if consecutive_free_count >= file_length:
                    left_space_start = i - file_length + 1
                    break
            else:
                consecutive_free_count = 0

        # If no space found, skip this file
        if left_space_start is None:
            continue

        # Move the whole file
        for j, block_index in enumerate(file_blocks):
            blocks[left_space_start + j] = str(current_file_id)
            blocks[block_index] = "."

    # Calculate checksum
    checksum = 0
    for i, block in enumerate(blocks):
        if block != ".":
            checksum += i * int(block)

    return checksum


def part1(data: str) -> int:
    """
    Solution for part 1: Compact disk block by block
    """
    return compact_disk_block_by_block(data)


def part2(data: str) -> int:
    """
    Solution for part 2: Compact disk whole files at a time
    """
    return compact_disk_whole_files(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
