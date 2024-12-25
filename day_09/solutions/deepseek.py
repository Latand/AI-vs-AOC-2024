def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(s: str) -> list:
    disk = []
    file_id = 0
    i = 0
    while i < len(s):
        file_length = int(s[i])
        free_length = int(s[i + 1]) if i + 1 < len(s) else 0
        disk.extend([file_id] * file_length)
        disk.extend(["."] * free_length)
        file_id += 1
        i += 2
    return disk


def compact_part1(disk: list) -> list:
    file_blocks = [block for block in disk if block != "."]
    compacted_disk = file_blocks + ["."] * (len(disk) - len(file_blocks))
    return compacted_disk


def compact_part2(disk: list) -> list:
    # Identify files: list of (start, length, file_id)
    files = []
    current_pos = 0
    while current_pos < len(disk):
        if disk[current_pos] != ".":
            file_id = disk[current_pos]
            length = 1
            current_pos += 1
            while current_pos < len(disk) and disk[current_pos] == file_id:
                length += 1
                current_pos += 1
            files.append((file_id, length))
        else:
            current_pos += 1
    # Sort files by decreasing file_id
    files_sorted = sorted(files, key=lambda x: -x[0])
    # Identify free spaces: list of (start, end, length)
    free_spans = []
    start = 0
    while start < len(disk):
        if disk[start] == ".":
            end = start
            while end < len(disk) and disk[end] == ".":
                end += 1
            free_spans.append((start, end - 1, end - start))
            start = end
        else:
            start += 1
    # Create a copy of disk for modification
    new_disk = disk.copy()
    # Move files
    for file_id, file_length in files_sorted:
        # Find the leftmost free span that can fit the file
        for span in free_spans:
            if span[2] >= file_length:
                # Move the file to this span
                # Find the original positions of the file blocks
                original_positions = [i for i, x in enumerate(disk) if x == file_id]
                # Replace the free span with the file blocks
                for j in range(span[0], span[0] + file_length):
                    new_disk[j] = file_id
                # Set the original positions to '.'
                for pos in original_positions:
                    if new_disk[pos] == file_id:
                        new_disk[pos] = "."
                # Update free spans
                free_spans.remove(span)
                if span[2] > file_length:
                    free_spans.append(
                        (span[0] + file_length, span[1], span[2] - file_length)
                    )
                break
    return new_disk


def calculate_checksum(disk: list) -> int:
    checksum = 0
    for pos, block in enumerate(disk):
        if block != ".":
            checksum += pos * block
    return checksum


def part1(data: str) -> int:
    disk = parse_disk_map(data)
    compacted_disk = compact_part1(disk)
    checksum = calculate_checksum(compacted_disk)
    return checksum


def part2(data: str) -> int:
    disk = parse_disk_map(data)
    compacted_disk = compact_part2(disk)
    checksum = calculate_checksum(compacted_disk)
    return checksum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
