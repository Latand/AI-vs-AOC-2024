#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 21 (Keypad Conundrum) - Part 1

We need to read several codes (lines) from ../input.txt. For each code,
we must determine the shortest sequence of *top-level* directional keypad
button presses that causes a final robot to type that code on the numeric keypad.

Each code is something like "029A" or "456A". The final "A" always appears,
and we treat the numeric part (ignoring leading zeroes) to multiply by
the length of the shortest sequence. Summing these products is our final answer.

Core constraints & puzzle logic:
--------------------------------
1) There are FOUR keypads in total:

   - Your keypad (the one *you* are pressing). It's a directional keypad with
       a 2-row x 3-column layout, but the top-left cell is a gap. Valid cells:

         Row 0: (0,0)=gap, (0,1)='^', (0,2)='A'
         Row 1: (1,0)='<', (1,1)='v', (1,2)='>'

       The "arm" starts aimed at 'A' (which is at (0,2)). You can press
       up/down/left/right *on your keypad* to move your arm to another valid cell
       (never can you move onto a gap), or press 'A' on *your* keypad to
       "activate" the button under your arm.

       When you press '^' / 'v' / '<' / '>' *on your keypad*, you move the arm
       on the *2nd-level robot's keypad* accordingly (if valid).
       When you press 'A' *on your keypad*, you "activate" the button that
       the *2nd-level robot's arm* is pointing at.

   - 2nd-level robot's keypad: also the same layout as above, also starting
       with the arm on 'A' at (0,2). Pressing '^' / 'v' / '<' / '>' here
       moves the 3rd-level robot's arm, pressing 'A' here "activates" the
       button the 3rd-level robot's arm is pointing at.

   - 3rd-level robot's keypad: again the same layout. Pressing '^' / 'v' / '<' / '>'
       here moves the final numeric keypad's arm; pressing 'A' here "presses"
       the numeric keypad button that the final numeric keypad's arm is pointing at.

   - The final numeric keypad (on the door) has this layout:

         +---+---+---+
         | 7 | 8 | 9 |   (row=0, col=0..2)
         +---+---+---+
         | 4 | 5 | 6 |   (row=1, col=0..2)
         +---+---+---+
         | 1 | 2 | 3 |   (row=2, col=0..2)
         +---+---+---+
             | 0 | A |   (row=3, col=1..2; col=0 is a gap)
             +---+---+

       The final robot's arm starts on 'A' at (3,2).
       Valid numeric keypad cells (row, col):
         (0,0)='7', (0,1)='8', (0,2)='9',
         (1,0)='4', (1,1)='5', (1,2)='6',
         (2,0)='1', (2,1)='2', (2,2)='3',
         (3,1)='0', (3,2)='A'
       (3,0) is a gap and cannot be aimed at.

2) If ever the "arm" on any keypad tries to move to a gap, the robot panics.
   So such moves are forbidden.

3) To type a code, e.g. "029A", the final sequence of presses on the numeric keypad
   must produce exactly the buttons '0', '2', '9', 'A' in that order.

4) The "complexity" of typing a code = (length of your top-level button press sequence)
   * (numeric part of the code ignoring leading zeros).
   For "029A", numeric part = 29. If the minimal top-level press sequence length is 68,
   complexity = 68 * 29 = 1972.

5) We do this for each code in the input and sum the complexities.

Approach:
---------
We will implement a breadth-first search (BFS) over the joint state space:

State = (
    my_keypad_pos,            # which cell on *your* directional keypad
    robot2_keypad_pos,        # which cell on the 2nd-level keypad
    robot3_keypad_pos,        # which cell on the 3rd-level keypad
    numeric_keypad_pos,       # which cell on the numeric keypad
    typed_count               # how many characters of the target code have been typed
)

- We start from:
  my_keypad_pos = 'A'  (which is coordinates (0,2) on your keypad)
  robot2_keypad_pos = 'A' (0,2)
  robot3_keypad_pos = 'A' (0,2)
  numeric_keypad_pos = 'A' (3,2 on numeric)
  typed_count = 0

- We want typed_count == len(code) as our goal condition.

- From a state, we can do 5 possible top-level actions:
  ['^', 'v', '<', '>', 'A']

  * If we pick '^', 'v', '<', '>' (a direction), we attempt to move my_keypad_pos
    in that direction on your keypad. If it's valid (not a gap, in-bounds), we get
    a new state with that updated my_keypad_pos, everything else same, cost +1.

  * If we pick 'A', then we see what *my_keypad_pos* is pointing at on your keypad.
    Suppose my_keypad_pos = '^'. That means the 2nd-level keypad sees a '^' press,
    and tries to move robot2_keypad_pos up if valid. If it's valid, we get a new state
    with robot2_keypad_pos changed, cost +1. Everything else same.

    But if my_keypad_pos = 'A', that means we "press A" on the 2nd-level keypad,
    so we see what robot2_keypad_pos is. If that is '^', we move robot3_keypad_pos up,
    etc. If it's 'A', we see what robot3_keypad_pos is... if that is '^', we move the
    numeric keypad's arm, etc. If eventually we get to pressing 'A' on the numeric
    keypad (the 4th level), that means we type the button that the numeric keypad
    arm is currently pointing at. We check if that matches the next needed character
    in the code. If yes, typed_count increments by 1; if no, that path is invalid.

We do a BFS until typed_count == len(code). The first time we reach that typed_count,
we have our minimal cost. Multiply that cost by the integer value of the code's digits
(ignoring leading zeroes). That is the code's complexity.

We repeat for each code in the input and sum the complexities.

Implementation notes:
---------------------
- Because the BFS is repeated for each code, and codes are presumably short, this
  is still computationally feasible. If the input is large, some caching or advanced
  trick might be needed, but for typical puzzle inputs, BFS is fine.

- We carefully define adjacency for each keypad so that no moves can go to a gap.
- We then code the BFS for a given code, returning the minimal length of the top-level
  button sequence that types that code.

Let's implement it below.
"""

from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


# ------------------------------------------------------------------
# 1) Define each keypad's layout and adjacency
# ------------------------------------------------------------------

# -- A) "Directional" keypad layout for your keypad, robot2, robot3
#     It's effectively the same shape for all three:
#       (0,0)=gap, (0,1)='^', (0,2)='A'
#       (1,0)='<', (1,1)='v', (1,2)='>'
#
# We'll store these as coordinate->char, plus an adjacency map that
# moves us among valid coordinates only.

dir_keys = {(0, 1): "^", (0, 2): "A", (1, 0): "<", (1, 1): "v", (1, 2): ">"}

# We also want a reverse map to quickly get the coordinate from character:
dir_pos_of_char = {}
for k, v in dir_keys.items():
    dir_pos_of_char[v] = k


# Precompute adjacency for the directional keypad:
# i.e. from each valid cell, if we press '^', we see if (row-1, col) is valid, etc.
def build_dir_adjacency():
    adjacency = {}
    for (r, c), ch in dir_keys.items():
        moves = {}
        # up:
        nr, nc = r - 1, c
        if (nr, nc) in dir_keys:
            moves["^"] = (nr, nc)
        # down:
        nr, nc = r + 1, c
        if (nr, nc) in dir_keys:
            moves["v"] = (nr, nc)
        # left:
        nr, nc = r, c - 1
        if (nr, nc) in dir_keys:
            moves["<"] = (nr, nc)
        # right:
        nr, nc = r, c + 1
        if (nr, nc) in dir_keys:
            moves[">"] = (nr, nc)
        adjacency[(r, c)] = moves
    return adjacency


dir_adjacency = build_dir_adjacency()

# -- B) Numeric keypad layout (final robot)
#     3 columns x 4 rows, with a gap at row=3,col=0
#     Valid:
#       (0,0)='7', (0,1)='8', (0,2)='9'
#       (1,0)='4', (1,1)='5', (1,2)='6'
#       (2,0)='1', (2,1)='2', (2,2)='3'
#       (3,1)='0', (3,2)='A'
#
num_keys = {
    (0, 0): "7",
    (0, 1): "8",
    (0, 2): "9",
    (1, 0): "4",
    (1, 1): "5",
    (1, 2): "6",
    (2, 0): "1",
    (2, 1): "2",
    (2, 2): "3",
    (3, 1): "0",
    (3, 2): "A",
}

num_pos_of_char = {}
for k, v in num_keys.items():
    num_pos_of_char[v] = k


def build_num_adjacency():
    adjacency = {}
    for (r, c), ch in num_keys.items():
        moves = {}
        # up
        nr, nc = r - 1, c
        if (nr, nc) in num_keys:
            moves["^"] = (nr, nc)
        # down
        nr, nc = r + 1, c
        if (nr, nc) in num_keys:
            moves["v"] = (nr, nc)
        # left
        nr, nc = r, c - 1
        if (nr, nc) in num_keys:
            moves["<"] = (nr, nc)
        # right
        nr, nc = r, c + 1
        if (nr, nc) in num_keys:
            moves[">"] = (nr, nc)
        adjacency[(r, c)] = moves
    return adjacency


num_adjacency = build_num_adjacency()

# ------------------------------------------------------------------
# BFS for a single code
# ------------------------------------------------------------------


def shortest_top_level_presses_for_code(code: str) -> int:
    """
    Returns the minimum number of top-level button presses needed
    (on *your* directional keypad) to produce the final typed sequence
    = code (like "029A") on the numeric keypad.

    We do a BFS over the state space:
      (my_pos, robot2_pos, robot3_pos, numeric_pos, typed_count)
    and transitions are the 5 possible top-level actions: '^','v','<','>','A'.

    If typed_count == len(code), we've successfully typed the code.
    """

    # We'll parse the code into a list of characters, e.g. ['0','2','9','A']
    code_chars = list(code)
    code_length = len(code_chars)

    # Starting positions on each keypad:
    start_my_pos = (0, 2)  # 'A' on your keypad
    start_robot2_pos = (0, 2)  # 'A'
    start_robot3_pos = (0, 2)  # 'A'
    start_num_pos = (3, 2)  # 'A' on numeric keypad
    start_typed_count = 0

    from collections import deque

    queue = deque()
    visited = set()

    start_state = (
        start_my_pos,
        start_robot2_pos,
        start_robot3_pos,
        start_num_pos,
        start_typed_count,
    )
    queue.append((start_state, 0))  # (state, costSoFar)
    visited.add(start_state)

    while queue:
        (my_pos, r2_pos, r3_pos, num_pos, tcount), cost = queue.popleft()

        if tcount == code_length:
            # We've typed the entire code
            return cost  # BFS ensures minimal cost

        # Explore all possible top-level presses:
        for top_press in ["^", "v", "<", ">", "A"]:
            # If top_press is a direction, attempt to move my_pos accordingly:
            if top_press in ["^", "v", "<", ">"]:
                # see if we can move my_pos on your keypad
                if top_press in dir_adjacency[my_pos]:
                    new_my_pos = dir_adjacency[my_pos][top_press]
                    new_state = (new_my_pos, r2_pos, r3_pos, num_pos, tcount)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, cost + 1))
            else:
                # top_press == 'A'
                # We "activate" whatever is under my_pos on your keypad
                my_char = dir_keys[my_pos]  # '^','v','<','>','A'
                # This means the 2nd-level keypad experiences a "press" of my_char
                # If my_char is a direction, we move r2_pos
                # If my_char is 'A', we "activate" r2_pos on the 2nd-level keypad, etc.
                # This is a small chain of up to 3 steps of logic.

                # We'll implement a small function to "apply_press" at one keypad.
                # If the keypad press is a direction, we move that keypad's arm.
                # If it's 'A', we apply_press on the next keypad, etc.
                # The next keypad is either robot2, robot3, or numeric.
                # We'll do it with a nested function.
                def apply_press(
                    keypad_pos, press, adjacency_map, keys_map, next_keypad_func
                ):
                    """
                    Attempt to apply 'press' on a directional keypad whose
                    current aimed position is 'keypad_pos'.

                    - If press is '^','v','<','>', we move 'keypad_pos' if valid.
                    - If press is 'A', we read which char is at 'keypad_pos' and pass that to next_keypad_func.

                    Returns: (new_keypad_pos, typed_increment, success_boolean)

                      typed_increment is how many characters got typed on the numeric keypad by this press
                      (usually 0 or 1).
                      success_boolean indicates if the move is valid or not (False if we go into a gap
                      or mismatch typed character).
                    """
                    if press in ["^", "v", "<", ">"]:
                        # move the arm
                        if press not in adjacency_map[keypad_pos]:
                            return (keypad_pos, 0, False)  # invalid move
                        return (adjacency_map[keypad_pos][press], 0, True)
                    else:
                        # press == 'A'
                        # so we "activate" the position. That means we see which button is at 'keypad_pos'
                        ch = keys_map[keypad_pos]  # e.g. '^','v','<','>','A'
                        return next_keypad_func(ch)

                def apply_press_robot2(r2_pos, press):
                    # The 2nd-level keypad uses dir_adjacency, dir_keys
                    # If press is direction, we move r2_pos
                    # If press is 'A', we see what's at r2_pos, then pass that to robot3
                    def next_robot3_func(ch_r2):
                        # pressing 'ch_r2' on the 3rd-level keypad
                        return apply_press_robot3(r3_pos, ch_r2)

                    return apply_press(
                        r2_pos, press, dir_adjacency, dir_keys, next_robot3_func
                    )

                def apply_press_robot3(r3_pos, press):
                    # The 3rd-level keypad uses dir_adjacency, dir_keys
                    # If press is direction, we move r3_pos
                    # If press is 'A', we see what's at r3_pos, then pass that to numeric
                    def next_numeric_func(ch_r3):
                        # pressing 'ch_r3' on the numeric keypad
                        return apply_press_numeric(num_pos, ch_r3)

                    return apply_press(
                        r3_pos, press, dir_adjacency, dir_keys, next_numeric_func
                    )

                def apply_press_numeric(num_pos, press):
                    """
                    The numeric keypad uses num_adjacency, num_keys. If press is a direction,
                    move num_pos. If press is 'A', we press the button at num_pos, which is
                    either '0'-'9' or 'A'.
                    We must check if that matches code_chars[tcount].
                    """
                    if press in ["^", "v", "<", ">"]:
                        if press not in num_adjacency[num_pos]:
                            return (num_pos, 0, False)
                        return (num_adjacency[num_pos][press], 0, True)
                    else:
                        # press == 'A'
                        # "press the numeric keypad button" at num_pos
                        char_at_num = num_keys[num_pos]  # e.g. '0','1','2',...,'A'
                        # We want to see if it matches code_chars[tcount]
                        # If matches, typed_count increments by 1, else path is invalid
                        needed_char = code_chars[tcount]
                        if char_at_num == needed_char:
                            return (num_pos, 1, True)
                        else:
                            return (num_pos, 0, False)

                # Now apply my_char on the 2nd-level robot:
                new_r2_pos, inc2, ok2 = apply_press_robot2(r2_pos, my_char)
                if not ok2:
                    continue  # invalid move, skip
                # typed_increment from that call
                typed2 = inc2

                # If the 2nd-level press was "A" on that keypad, it cascades to the 3rd-level, etc.
                # But we've already embedded that cascade in apply_press. We only get a single
                # typed_increment out, because at most we typed once at the numeric keypad.
                # Also note that robot3_pos or numeric_pos might have changed, so we must track them.

                # But we only get the new r3_pos, num_pos from the nested call, so let's refine:
                # Actually we must store the intermediate states from that chain. We'll do it step-by-step.

                # For that step-by-step, let's just replicate the logic more manually:
                # Step 1: apply_press(r2_pos, my_char) => might do a direction or an 'A'
                #   if direction => new r2_pos
                #   if 'A' => we apply the next...
                #
                # Actually let's do a single "chain" function:

                def chain_press(r2_p, r3_p, num_p, tcount_cur, press_2):
                    """
                    We press `press_2` on the 2nd-level keypad.
                    This might cause:
                     - a move of r2_p, or
                     - an 'A' press => we press what's at r2_p on the 3rd-level,
                       which might cause:
                         - a move of r3_p, or
                         - an 'A' press => we press what's at r3_p on the numeric,
                           which might cause:
                             - a move of num_p, or
                             - an 'A' press => we attempt to type code_chars[tcount_cur].
                    Returns new_r2_p, new_r3_p, new_num_p, typed_increment, success
                    """
                    # 2nd-level
                    if press_2 in ["^", "v", "<", ">"]:
                        # move r2_p
                        if press_2 not in dir_adjacency[r2_p]:
                            return (r2_p, r3_p, num_p, 0, False)
                        return (dir_adjacency[r2_p][press_2], r3_p, num_p, 0, True)
                    else:
                        # press_2 == 'A'
                        # read what's at r2_p
                        ch_r2 = dir_keys[r2_p]
                        # apply that to robot3
                        # 3rd-level
                        if ch_r2 in ["^", "v", "<", ">"]:
                            if ch_r2 not in dir_adjacency[r3_p]:
                                return (r2_p, r3_p, num_p, 0, False)
                            return (r2_p, dir_adjacency[r3_p][ch_r2], num_p, 0, True)
                        else:
                            # ch_r2 == 'A'
                            # read what's at r3_p
                            ch_r3 = dir_keys[r3_p]
                            if ch_r3 in ["^", "v", "<", ">"]:
                                # move num_p
                                if ch_r3 not in num_adjacency[num_p]:
                                    return (r2_p, r3_p, num_p, 0, False)
                                return (
                                    r2_p,
                                    r3_p,
                                    num_adjacency[num_p][ch_r3],
                                    0,
                                    True,
                                )
                            else:
                                # ch_r3 == 'A'
                                # that means press the numeric keypad button at num_p
                                char_at_num = num_keys[num_p]
                                # check if it matches code_chars[tcount_cur]
                                if char_at_num == code_chars[tcount_cur]:
                                    return (r2_p, r3_p, num_p, 1, True)
                                else:
                                    return (r2_p, r3_p, num_p, 0, False)

                new_r2, new_r3, new_num, typed_inc, ok = chain_press(
                    r2_pos, r3_pos, num_pos, tcount, my_char
                )
                if not ok:
                    continue

                # Now we have new_r2, new_r3, new_num, typed_inc
                new_tcount = tcount + typed_inc
                new_state = (my_pos, new_r2, new_r3, new_num, new_tcount)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, cost + 1))

    # If we exhaust BFS without typed_count == len(code), then there's no solution.
    # The puzzle statement suggests there's always a solution, but we'll just return large.
    return 999999999


def part1(data: list[str]) -> int:
    """
    Given the lines of input (each a code like '029A', '980A', ...),
    find the sum of complexities for all codes.
    Complexity = (length of minimal top-level press sequence) * (numeric portion ignoring leading zeros).
    """
    total_complexity = 0
    for code in data:
        # parse numeric portion ignoring leading zeros:
        # code is something like '029A' or '456A'. We'll slice off the trailing 'A'.
        # everything except the last char is digits.
        digits = code[:-1]  # e.g. '029'
        # convert ignoring leading zeros:
        if digits == "":
            num_val = 0
        else:
            num_val = int(digits) if digits.isdigit() else 0

        # find BFS minimal cost:
        cost = shortest_top_level_presses_for_code(code)
        complexity = cost * num_val
        total_complexity += complexity

    return total_complexity


def part2(data: list[str]) -> int:
    """
    The puzzle narrative suggests there's a Part 2, but it's not described here.
    We'll leave this empty or return 0 for now.
    """
    return 0


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # If there's a Part 2, implement it or leave as 0 / placeholder
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
