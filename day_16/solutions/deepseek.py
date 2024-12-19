import sys
import heapq


def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


def find_positions(maze, start="S", end="E"):
    for y, row in enumerate(maze):
        for x, ch in enumerate(row):
            if ch == start:
                start_pos = (x, y)
            if ch == end:
                end_pos = (x, y)
    return start_pos, end_pos


def get_neighbors(maze, x, y, direction):
    dirs = {"E": (1, 0), "S": (0, 1), "W": (-1, 0), "N": (0, -1)}
    dx, dy = dirs[direction]
    next_x, next_y = x + dx, y + dy
    if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze):
        if maze[next_y][next_x] != "#":
            return [(next_x, next_y, direction, 1)]
    neighbors = []
    left_dir = {"E": "N", "N": "W", "W": "S", "S": "E"}[direction]
    neighbors.append((x, y, left_dir, 1000))
    right_dir = {"E": "S", "S": "W", "W": "N", "N": "E"}[direction]
    neighbors.append((x, y, right_dir, 1000))
    return neighbors


def dijkstra(maze, start_state, end_pos):
    heap = []
    heapq.heappush(heap, (0, start_state))
    cost = {start_state: 0}
    while heap:
        current_cost, current_state = heapq.heappop(heap)
        if current_state[:2] == end_pos:
            return current_cost, cost
        if current_cost > cost.get(current_state, float("inf")):
            continue
        for neighbor in get_neighbors(maze, *current_state):
            nx, ny, nd, nc = neighbor
            next_state = (nx, ny, nd)
            total_cost = current_cost + nc
            if total_cost < cost.get(next_state, float("inf")):
                cost[next_state] = total_cost
                heapq.heappush(heap, (total_cost, next_state))
    return float("inf"), cost


def backward_dijkstra(maze, end_state, start_pos):
    heap = []
    heapq.heappush(heap, (0, end_state))
    cost = {end_state: 0}
    while heap:
        current_cost, current_state = heapq.heappop(heap)
        if current_state[:2] == start_pos:
            continue
        if current_cost > cost.get(current_state, float("inf")):
            continue
        for direction in ["E", "S", "W", "N"]:
            neighbors = get_neighbors(maze, *current_state[:2], direction)
            for neighbor in neighbors:
                nx, ny, nd, nc = neighbor
                if (nx, ny, nd) == current_state:
                    continue
                next_state = (nx, ny, nd)
                total_cost = current_cost + nc
                if total_cost < cost.get(next_state, float("inf")):
                    cost[next_state] = total_cost
                    heapq.heappush(heap, (total_cost, next_state))
    return cost


def part1(maze, start_pos, end_pos):
    start_state = (start_pos[0], start_pos[1], "E")
    minimal_cost, _ = dijkstra(maze, start_state, end_pos)
    return minimal_cost


def part2(maze, start_pos, end_pos, minimal_cost, forward_cost, backward_cost):
    tiles = set()
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] in ["S", ".", "E"]:
                for direction in ["E", "S", "W", "N"]:
                    state = (x, y, direction)
                    if state in forward_cost and state in backward_cost:
                        if forward_cost[state] + backward_cost[state] == minimal_cost:
                            tiles.add((x, y))
    return len(tiles)


def main():
    maze = read_input()
    start_pos, end_pos = find_positions(maze)
    minimal_cost, forward_cost = dijkstra(
        maze, (start_pos[0], start_pos[1], "E"), end_pos
    )
    print(f"Part 1: {minimal_cost}")
    backward_cost = backward_dijkstra(maze, (end_pos[0], end_pos[1], "E"), start_pos)
    tile_count = part2(
        maze, start_pos, end_pos, minimal_cost, forward_cost, backward_cost
    )
    print(f"Part 2: {tile_count}")


if __name__ == "__main__":
    main()
