import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(disk_map_str: str) -> list[tuple[int, int]]:
    """
    Parses the disk map string into a list of tuples (file_size, free_space).
    """
    disk_map = []
    segments = re.findall(r"\d+", disk_map_str)
    for i in range(0, len(segments), 2):
        file_size = int(segments[i])
        free_space = int(segments[i + 1]) if i + 1 < len(segments) else 0
        disk_map.append((file_size, free_space))
    return disk_map


def create_disk(disk_map: list[tuple[int, int]]) -> list[int]:
    """
    Creates the initial disk representation as a list of file IDs or -1 for free space.
    """
    disk = []
    file_id = 0
    for file_size, free_space in disk_map:
        disk.extend([file_id] * file_size)
        disk.extend([-1] * free_space)
        file_id += 1
    return disk


def compact_disk_part1(disk: list[int]) -> list[int]:
    """
    Compacts the disk by moving individual blocks.
    """
    while True:
        moved = False
        for i in range(len(disk)):
            if disk[i] == -1:
                for j in range(i + 1, len(disk)):
                    if disk[j] != -1:
                        disk[i], disk[j] = disk[j], disk[i]
                        moved = True
                        break
            if moved:
                break
        if not moved:
            break
    return disk


def compact_disk_part2(disk: list[int], disk_map: list[tuple[int, int]]) -> list[int]:
    """
    Compacts the disk by moving whole files.
    """
    file_sizes = [file_size for file_size, _ in disk_map]
    file_ids = list(range(len(file_sizes) - 1, -1, -1))

    for file_id in file_ids:
        file_size = file_sizes[file_id]
        file_start = -1
        for i in range(len(disk)):
            if disk[i] == file_id:
                file_start = i
                break

        if file_start == -1:
            continue

        free_space_start = -1
        for i in range(file_start - 1, -1, -1):
            if disk[i] != -1:
                break
            free_space_end = i
            if free_space_end - free_space_start >= file_size:
                free_space_start = free_space_end - file_size
                break

        if free_space_start != -1 and free_space_end - free_space_start >= file_size:
            file_end = file_start
            while file_end < len(disk) and disk[file_end] == file_id:
                file_end += 1

            for i in range(file_size):
                disk[free_space_start + i] = file_id

            j = 0
            for i in range(file_start, file_end):
                if (
                    free_space_start + file_size + j < len(disk)
                    and free_space_start + file_size + j >= file_start
                ):
                    disk[i] = disk[free_space_start + file_size + j]
                else:
                    disk[i] = -1
                j += 1

    return disk


def calculate_checksum(disk: list[int]) -> int:
    """
    Calculates the filesystem checksum.
    """
    checksum = 0
    for i, file_id in enumerate(disk):
        if file_id != -1:
            checksum += i * file_id
    return checksum


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    disk_map = parse_disk_map(data)
    disk = create_disk(disk_map)
    compacted_disk = compact_disk_part1(disk)
    return calculate_checksum(compacted_disk)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    disk_map = parse_disk_map(data)
    disk = create_disk(disk_map)
    compacted_disk = compact_disk_part2(disk, disk_map)
    return calculate_checksum(compacted_disk)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
