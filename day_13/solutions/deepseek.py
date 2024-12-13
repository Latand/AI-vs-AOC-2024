def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_machines(data):
    lines = data.splitlines()
    machines = []
    for i in range(0, len(lines), 3):
        lineA = lines[i]
        lineB = lines[i + 1]
        lineP = lines[i + 2]
        # Extract XA, YA from lineA
        partsA = lineA.split()
        XA = int(partsA[3].split("+")[1])
        YA = int(partsA[4].split("+")[1])
        # Extract XB, YB from lineB
        partsB = lineB.split()
        XB = int(partsB[3].split("+")[1])
        YB = int(partsB[4].split("+")[1])
        # Extract XP, YP from lineP
        partsP = lineP.split()
        XP = int(partsP[2].split("=")[1])
        YP = int(partsP[3].split("=")[1])
        machines.append((XA, YA, XB, YB, XP, YP))
    return machines


def part1(data: str) -> int:
    machines = parse_machines(data)
    total_cost = 0
    for machine in machines:
        XA, YA, XB, YB, XP, YP = machine
        D = XA * YB - XB * YA
        if D != 0:
            a = (XP * YB - XB * YP) / D
            b = (XA * YP - XP * YA) / D
            if a.is_integer() and b.is_integer():
                a = int(a)
                b = int(b)
                if 0 <= a <= 100 and 0 <= b <= 100:
                    cost = 3 * a + b
                    total_cost += cost
        else:
            if YB * XP == YP * XB:
                # Find a and b within [0,100] that minimize 3*a + b
                min_cost = float("inf")
                for a in range(0, 101):
                    if (XP - XA * a) % XB == 0:
                        b = (XP - XA * a) // XB
                        if b >= 0 and b <= 100:
                            cost = 3 * a + b
                            if cost < min_cost:
                                min_cost = cost
                if min_cost != float("inf"):
                    total_cost += min_cost
    return total_cost


def part2(data: str) -> int:
    machines = parse_machines(data)
    total_cost = 0
    offset = 10000000000000
    for machine in machines:
        XA, YA, XB, YB, XP, YP = machine
        XP += offset
        YP += offset
        D = XA * YB - XB * YA
        if D != 0:
            a = (XP * YB - XB * YP) / D
            b = (XA * YP - XP * YA) / D
            if a.is_integer() and b.is_integer():
                a = int(a)
                b = int(b)
                if a >= 0 and b >= 0:
                    cost = 3 * a + b
                    total_cost += cost
        else:
            if YB * XP == YP * XB:
                # Find a and b >= 0 that minimize 3*a + b
                # Placeholder for part two solution
                pass
    return total_cost


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
