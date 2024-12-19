import heapq


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def neighbors(x, y, w, h):
    # Just helper for adjacency if needed
    # Not directly used here, but we have a more direct logic in the search.
    for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if 0 <= nx < w and 0 <= ny < h:
            yield nx, ny


def part1(data: str) -> int:
    """
    Solve part 1: Find the minimal cost to reach E from S, starting facing East.
    """

    # Parse the input maze
    maze = data.split("\n")
    h = len(maze)
    w = len(maze[0])

    start = None
    end = None
    for y in range(h):
        for x in range(w):
            c = maze[y][x]
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)

    # Directions: 0=North,1=East,2=South,3=West
    # dx, dy for moving forward in these directions
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # We'll run Dijkstra over states: (x, y, dir)
    # Distances dictionary: dist[(x,y,dir)] = minimal cost
    dist = {}
    # Priority queue: (cost, x, y, dir)
    pq = []
    # Starting facing East (dir=1)
    start_state = (start[0], start[1], 1)
    dist[start_state] = 0
    heapq.heappush(pq, (0, start[0], start[1], 1))

    # We'll store parents for part 2 recovery
    # However, we only need parent links if we want to explicitly reconstruct paths.
    # For marking all minimal path states, we will do a backward graph search later,
    # so we should store graph edges as we relax them.
    # Instead, we can store just dist and the maze, and recompute edges later when doing backward step.
    # But storing all edges might be large. We'll do a backward search by re-checking conditions.
    # For that, we must know the minimal distances after Dijkstra finishes.

    while pq:
        cost, x, y, d = heapq.heappop(pq)
        if dist.get((x, y, d), float("inf")) < cost:
            continue
        # If we reached end tile at any direction, we keep going to fill dist table completely,
        # but we know the minimal cost at least.
        # We'll finalize after pq is empty or after we pop all minimal solutions.

        # Try moving forward
        dx, dy = dirs[d]
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] != "#":
            ncost = cost + 1
            if ncost < dist.get((nx, ny, d), float("inf")):
                dist[(nx, ny, d)] = ncost
                heapq.heappush(pq, (ncost, nx, ny, d))

        # Try turning left (d - 1 mod 4)
        ld = (d - 1) % 4
        lcost = cost + 1000
        if lcost < dist.get((x, y, ld), float("inf")):
            dist[(x, y, ld)] = lcost
            heapq.heappush(pq, (lcost, x, y, ld))

        # Try turning right (d + 1 mod 4)
        rd = (d + 1) % 4
        rcost = cost + 1000
        if rcost < dist.get((x, y, rd), float("inf")):
            dist[(x, y, rd)] = rcost
            heapq.heappush(pq, (rcost, x, y, rd))

    # Find minimal cost at E (over all directions)
    end_cost = min(dist.get((end[0], end[1], d), float("inf")) for d in range(4))
    return end_cost


def part2(data: str) -> int:
    """
    For part 2: Identify all tiles that are part of at least one best path.
    We'll run the same Dijkstra, then perform a backward search from the end states.
    """

    maze = data.split("\n")
    h = len(maze)
    w = len(maze[0])

    start = None
    end = None
    for y in range(h):
        for x in range(w):
            c = maze[y][x]
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)

    # Directions: 0=North,1=East,2=South,3=West
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # Dijkstra again, but we need to keep dist for backward check
    dist = {}
    pq = []
    start_state = (start[0], start[1], 1)
    dist[start_state] = 0
    heapq.heappush(pq, (0, start[0], start[1], 1))

    while pq:
        cost, x, y, d = heapq.heappop(pq)
        if dist.get((x, y, d), float("inf")) < cost:
            continue

        # Move forward
        dx, dy = dirs[d]
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] != "#":
            ncost = cost + 1
            if ncost < dist.get((nx, ny, d), float("inf")):
                dist[(nx, ny, d)] = ncost
                heapq.heappush(pq, (ncost, nx, ny, d))

        # Turn left
        ld = (d - 1) % 4
        lcost = cost + 1000
        if lcost < dist.get((x, y, ld), float("inf")):
            dist[(x, y, ld)] = lcost
            heapq.heappush(pq, (lcost, x, y, ld))

        # Turn right
        rd = (d + 1) % 4
        rcost = cost + 1000
        if rcost < dist.get((x, y, rd), float("inf")):
            dist[(x, y, rd)] = rcost
            heapq.heappush(pq, (rcost, x, y, rd))

    # Minimal cost at end
    end_cost = min(dist.get((end[0], end[1], d), float("inf")) for d in range(4))

    # Now we find all states that are on any minimal path.
    # We'll do a backward search:
    # A state s is on a minimal path if there exists a next state n such that:
    # dist[s] + cost(s->n) = dist[n] and dist[n] is part of minimal path towards the end.
    # We'll start from all (end[0], end[1], d) states that have dist == end_cost and go backwards.
    # To go backwards, we consider the inverse of each action:
    # Forward step: (x,y,d)->(nx,ny,d) cost 1 if (nx,ny) is forward in direction d
    # From n: we find s that could have led to n with cost 1 or 1000 accordingly.

    # Let's collect all states that lead to minimal end states
    # We'll use a queue and a set of minimal_path_states
    from collections import deque

    minimal_path_states = set()
    q = deque()

    # Initialize queue with end states that have the minimal cost
    for d in range(4):
        if dist.get((end[0], end[1], d), float("inf")) == end_cost:
            minimal_path_states.add((end[0], end[1], d))
            q.append((end[0], end[1], d))

    # To go backward:
    # For a given state (x,y,d), possible predecessors:
    # 1) Another state (x,y,d') that turned into direction d with cost 1000. That means dist[x,y,d'] + 1000 = dist[x,y,d].
    #    So check if dist[x,y,d'] = dist[x,y,d]-1000.
    #    That means from (x,y,d') we turned right or left to get (x,y,d).
    # 2) A state (x-dx,y-dy,d) that moved forward into (x,y,d). If dist[x-dx,y-dy,d] + 1 = dist[x,y,d], that is a predecessor.

    while q:
        x, y, d = q.popleft()
        current_dist = dist[(x, y, d)]

        # Check for turning predecessors:
        # If we arrived here from turning right or left, then from (x,y,d2) with cost current_dist-1000
        # (x,y,d2) should have a dist of current_dist-1000.
        # Which d2 could lead to d by a single turn?
        # Two possibilities: turning left from d2 gives d, or turning right from d2 gives d.
        # Turning left: if d = (d2 -1)%4, then d2 = (d+1)%4
        # Turning right: if d = (d2+1)%4, then d2 = (d-1)%4
        d_left_pred = (d + 1) % 4  # if we turned left from d_left_pred, we get d
        d_right_pred = (d - 1) % 4  # if we turned right from d_right_pred, we get d

        # Check left predecessor
        if dist.get((x, y, d_left_pred), float("inf")) == current_dist - 1000:
            if (x, y, d_left_pred) not in minimal_path_states:
                minimal_path_states.add((x, y, d_left_pred))
                q.append((x, y, d_left_pred))

        # Check right predecessor
        if dist.get((x, y, d_right_pred), float("inf")) == current_dist - 1000:
            if (x, y, d_right_pred) not in minimal_path_states:
                minimal_path_states.add((x, y, d_right_pred))
                q.append((x, y, d_right_pred))

        # Check forward predecessor:
        # If we moved forward into (x,y) from (px,py) with same direction d:
        # px = x - dx[d], py = y - dy[d]
        dx_, dy_ = dirs[d]
        px, py = x - dx_, y - dy_
        if 0 <= px < w and 0 <= py < h and maze[py][px] != "#":
            if dist.get((px, py, d), float("inf")) == current_dist - 1:
                if (px, py, d) not in minimal_path_states:
                    minimal_path_states.add((px, py, d))
                    q.append((px, py, d))

    # Now minimal_path_states contains all states (x,y,d) that can be on a minimal path.
    # We need to count how many unique tiles are on these minimal paths.
    tiles_on_minimal_path = set((x, y) for (x, y, d) in minimal_path_states)

    # Count tiles that are not walls
    # The puzzle states we only care about tiles that are non-wall (S, ., E).
    # But minimal_path_states should never include walls anyway. Just to be safe, we can filter:
    count = 0
    for x, y in tiles_on_minimal_path:
        if maze[y][x] != "#":
            count += 1

    return count


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
