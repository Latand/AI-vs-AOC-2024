def read_input():
    """
    Reads the puzzle input (a single line) from ../input.txt
    """
    with open("../input.txt") as f:
        return f.read().strip()


def parse_disk_map(disk_map_str: str):
    """
    Given the puzzle input string (digits alternating between
    file-length and free-length), build and return a list of blocks.

    Each element in the returned list is either:
      - An integer file ID (0, 1, 2, ...)
      - None (representing free space)

    Also returns the number of files encountered.
    """
    blocks = []
    toggle_file = True  # True => next digit = file-length, False => free-length
    current_file_id = 0

    for ch in disk_map_str:
        length = int(ch)
        if toggle_file:
            # Add 'length' blocks for the current file ID
            for _ in range(length):
                blocks.append(current_file_id)
            current_file_id += 1
        else:
            # Add 'length' free blocks
            for _ in range(length):
                blocks.append(None)
        # Flip from file to free, or free to file
        toggle_file = not toggle_file

    # current_file_id is the total number of file segments
    return blocks, current_file_id


def checksum(blocks):
    """
    Compute the filesystem checksum:
      sum over all (index * fileID) for blocks that contain a file (not None).
    """
    total = 0
    for i, val in enumerate(blocks):
        if val is not None:
            total += i * val
    return total


def compact_one_block_at_a_time(blocks):
    """
    Part 1 simulation:
    Move file blocks one-by-one from the rightmost file block
    to the leftmost free space, until no free block precedes any file block.

    This modifies `blocks` in-place.
    """
    n = len(blocks)
    # We repeatedly find:
    #  - i = the leftmost free block
    #  - j = the rightmost file block that is strictly to the right of i
    #  Move that block from j to i, then continue until i >= j or no such pairs.

    i = 0  # candidate for leftmost free
    j = n - 1  # candidate for rightmost file

    while True:
        # Advance i to the next free block
        while i < n and blocks[i] is not None:
            i += 1
        # Retreat j to the next file block
        while j >= 0 and blocks[j] is None:
            j -= 1

        if i < j and 0 <= i < n and 0 <= j < n:
            # Move one file-block from j -> i
            blocks[i] = blocks[j]
            blocks[j] = None

            # Move i forward for the next iteration,
            # move j backward for the next iteration
            i += 1
            j -= 1
        else:
            # No more valid moves
            break


def part1(disk_map_str: str) -> int:
    """
    Part 1:
      1) Parse the disk map
      2) Simulate one-block-at-a-time compaction
      3) Compute the checksum of the resulting arrangement
    """
    blocks, _ = parse_disk_map(disk_map_str)
    compact_one_block_at_a_time(blocks)
    return checksum(blocks)


def find_leftmost_free_span(blocks, max_right_index, length_needed):
    """
    Part 2 helper:
      Find a contiguous run of `length_needed` free blocks (None)
      which lies *entirely* to the left of `max_right_index`.

    If found, return the start index of that free span; otherwise None.
    """
    # We'll scan from index 0 up to (max_right_index - length_needed)
    # and look for a run of length_needed Nones.
    if length_needed == 0:
        return None  # moving a file of length 0 doesn't make sense (or do nothing)
    upper_bound = max_right_index - length_needed
    if upper_bound < 0:
        return None  # not enough space to the left at all

    consecutive = 0
    start = 0
    for i in range(0, max_right_index):
        if blocks[i] is None:
            consecutive += 1
        else:
            # reset
            consecutive = 0
            start = i + 1

        if consecutive == length_needed:
            # Found a suitable span [start .. i]
            return start
        if i >= upper_bound:
            # If we've gotten this far, no need to continue checking beyond
            # (since we won't have enough room to the left)
            break

    return None


def compact_whole_files(blocks, num_files):
    """
    Part 2 simulation:
      Move files in descending file ID order. Each file is moved *once* if possible.
      The file must move entirely to a free span (contiguous None blocks) strictly
      to the left of where the file currently starts. If no such span is large
      enough, the file does not move.

    This modifies `blocks` in-place.
    """
    # First, figure out where each file currently sits (start, end).
    # Each file ID from 0..(num_files-1) was created contiguously in parse_disk_map.
    # We'll find the min_index and max_index for each file.
    # (Because in the original layout, each file is guaranteed contiguous.)
    file_positions = [None] * num_files  # file_positions[fid] = (start, end)

    # Scan once to find each file's (start_index, end_index)
    # Because each file is contiguous in the *original* layout,
    # the first block we see for file f is its start, and we keep going until we
    # see a different ID or run out.
    i = 0
    n = len(blocks)
    fid = 0

    while i < n and fid < num_files:
        if blocks[i] == fid:
            start = i
            # move forward until we see a different ID or end
            while i < n and blocks[i] == fid:
                i += 1
            end = i - 1
            file_positions[fid] = (start, end)
            fid += 1
        else:
            i += 1

    # Now move each file (highest ID first) if possible
    for file_id in reversed(range(num_files)):
        start_idx, end_idx = file_positions[file_id]
        length = end_idx - start_idx + 1
        # Find the leftmost free span to the left of start_idx that can fit 'length'
        new_start = find_leftmost_free_span(blocks, start_idx, length)
        if new_start is not None:
            # We can move the file to [new_start .. new_start + length - 1]
            # 1) free up the old location
            for i in range(start_idx, end_idx + 1):
                blocks[i] = None
            # 2) fill the new span
            new_end = new_start + length - 1
            for i in range(new_start, new_end + 1):
                blocks[i] = file_id
            # 3) update the recorded position
            file_positions[file_id] = (new_start, new_end)


def part2(disk_map_str: str) -> int:
    """
    Part 2:
      1) Parse the disk map again (fresh layout)
      2) Move entire files from highest ID to lowest if possible
      3) Compute the checksum
    """
    blocks, num_files = parse_disk_map(disk_map_str)
    compact_whole_files(blocks, num_files)
    return checksum(blocks)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
