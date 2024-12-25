def read_input():
    with open("../input.txt") as f:
        lines = [line.strip() for line in f if line.strip()]
    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            rules.append(line)
        else:
            updates.append(line)
    # Parse rules into (X, Y) pairs
    rules_list = []
    for rule in rules:
        X_str, Y_str = rule.split("|")
        X = int(X_str)
        Y = int(Y_str)
        rules_list.append((X, Y))
    # Parse updates into list of lists of integers
    updates_list = []
    for update in updates:
        pages = list(map(int, update.split(",")))
        updates_list.append(pages)
    return rules_list, updates_list


def main():
    rules, updates = read_input()
    sum_middle = 0
    for update in updates:
        pos = {page: idx for idx, page in enumerate(update)}
        valid = True
        for X, Y in rules:
            if X in pos and Y in pos:
                if pos[X] >= pos[Y]:
                    valid = False
                    break
        if valid:
            middle_index = len(update) // 2
            middle_page = update[middle_index]
            sum_middle += middle_page
    print(sum_middle)


if __name__ == "__main__":
    main()
